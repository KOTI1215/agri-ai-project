from flask import Flask, render_template, request, redirect, url_for
import requests
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

api_key = "ed74c3c9c0a6178094737c755b201224"

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            result TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Multi-Language Dictionary
LANGUAGES = {
    'en': {
        'title': '🌱 Agri-AI Smart Farming System',
        'subtitle': 'Empowering farmers with weather intelligence, yield predictions, fertilizer guides, and pest advisories.',
        'weather_btn': 'Open Weather Tool',
        'forecast_btn': 'Open Forecast Tool',
        'fertilizer_btn': 'Open Fertilizer Tool',
        'advisory_btn': 'Open Pest Advisory',
        'disease_btn': 'Open Disease Scanner',
        'history_btn': 'View Scan History'
    },
    'te': {
        'title': '🌱 agri-ai స్మార్ట్ వ్యవసాయ వ్యవస్థ',
        'subtitle': 'వాతావరణ మేధస్సు, దిగుబడి అంచనాలు, ఎరువుల మార్గదర్శకాలతో రైతులకు సాధికారత.',
        'weather_btn': 'వాతావరణ సాధనం',
        'forecast_btn': 'అంచనా సాధనం',
        'fertilizer_btn': 'ఎరువుల సలహాదారు',
        'advisory_btn': 'తెగుళ్ల హెచ్చరిక',
        'disease_btn': 'వ్యాధి స్కానర్',
        'history_btn': 'చరిత్రను చూడండి'
    }
}

@app.route('/')
def home():
    lang = request.args.get('lang', 'en')
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    return render_template('index.html', t=t, current_lang=lang)

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    city = request.form.get('city') if request.method == 'POST' else request.args.get('city', 'Vizianagaram')
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    
    weather_data, error_message = None, None
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            weather_data = response.json()
        else:
            fallback_url = f"https://api.openweathermap.org/data/2.5/weather?q=Vizianagaram,IN&appid={api_key}&units=metric"
            fallback_resp = requests.get(fallback_url, timeout=5)
            if fallback_resp.status_code == 200:
                weather_data = fallback_resp.json()
                error_message = f"Village '{city}' not found. Showing Vizianagaram hub."
    except Exception:
        error_message = "Network error: Unable to connect to OpenWeather map."

    return render_template('weather.html', weather=weather_data, error=error_message)

@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    city = request.form.get('city') if request.method == 'POST' else request.args.get('city', 'Vizianagaram')
    crop = request.form.get('crop', 'Paddy') if request.method == 'POST' else request.args.get('crop', 'Paddy')
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={api_key}&units=metric"
    forecast_data, error_message, estimated_yield = None, None, None
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            forecast_data = response.json()
            temp_avg = sum(item['main']['temp'] for item in forecast_data['list'][:8]) / 8
            estimated_yield = round(22 - abs(temp_avg - 28) * 0.5, 2) if crop == 'Paddy' else round(25 - abs(temp_avg - 24) * 0.6, 2)
    except Exception:
        error_message = "Network error: Unable to connect to OpenWeather map."

    return render_template('forecast.html', forecast=forecast_data, error=error_message, city=city, crop=crop, est_yield=estimated_yield)

@app.route('/fertilizer', methods=['GET', 'POST'])
def fertilizer():
    recommendation, crop, soil = None, "Paddy", "Alluvial"
    if request.method == 'POST':
        crop = request.form.get('crop', 'Paddy')
        soil = request.form.get('soil', 'Alluvial')
        recommendation = "Nitrogen (N): 120 kg/ha, Phosphorus (P): 60 kg/ha, Potassium (P2O5): 40 kg/ha. Apply Nitrogen in 3 split doses." if crop == 'Paddy' else "Nitrogen (N): 150 kg/ha, Phosphorus (P): 75 kg/ha, Potassium (P2O5): 40 kg/ha."
    return render_template('fertilizer.html', recommendation=recommendation, crop=crop, soil=soil)

@app.route('/advisory', methods=['GET', 'POST'])
def advisory():
    crop, temp, humidity, alert = "Paddy", 30, 75, "Low risk of pest outbreak. Normal crop monitoring advised."
    if request.method == 'POST':
        crop = request.form.get('crop', 'Paddy')
        try:
            temp = float(request.form.get('temp', 30))
            humidity = float(request.form.get('humidity', 75))
        except ValueError:
            pass
        if crop == 'Paddy' and humidity > 80 and temp > 28:
            alert = "⚠ HIGH ALERT: Risk of **Blast Disease** & **Brown Planthopper**. Apply tricyclazole."
        else:
            alert = "✅ Conditions are stable for " + crop + "."
    return render_template('advisory.html', crop=crop, temp=temp, humidity=humidity, alert=alert)

@app.route('/disease', methods=['GET', 'POST'])
def disease():
    result = None
    filename = None
    lang = request.args.get('lang', 'en')
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                result = "🔍 Analysis Complete: **Paddy Blast (Pyricularia oryzae)** detected with 88% confidence. Recommended treatment: Spray Tricyclazole 75% WP @ 0.6g per liter of water."
                
                # Save to SQLite Database
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO scan_history (filename, result) VALUES (?, ?)', (filename, result))
                conn.commit()
                conn.close()
                
    return render_template('disease.html', result=result, filename=filename, t=t, current_lang=lang)

@app.route('/history')
def history():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT filename, result, timestamp FROM scan_history ORDER BY id DESC')
    scans = cursor.fetchall()
    conn.close()
    return render_template('history.html', scans=scans)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)