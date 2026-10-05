from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form.get('city')
    else:
        city = request.args.get('city', 'Vizianagaram')
        
    api_key = "ed74c3c9c0a6178094737c755b201224"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    weather_data = None
    error_message = None
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            weather_data = response.json()
        else:
            error_message = f"Could not find weather data for '{city}'."
    except Exception as e:
        error_message = "Network error: Unable to connect to OpenWeather map."

    return render_template('weather.html', weather=weather_data, error=error_message)

@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    if request.method == 'POST':
        city = request.form.get('city')
        crop = request.form.get('crop', 'Paddy')
    else:
        city = request.args.get('city', 'Vizianagaram')
        crop = request.args.get('crop', 'Paddy')
        
    api_key = "ed74c3c9c0a6178094737c755b201224"
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    
    forecast_data = None
    error_message = None
    estimated_yield = None
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            forecast_data = response.json()
            temp_avg = sum(item['main']['temp'] for item in forecast_data['list'][:8]) / 8
            if crop == 'Paddy':
                estimated_yield = round(22 - abs(temp_avg - 28) * 0.5, 2)
            elif crop == 'Maize':
                estimated_yield = round(25 - abs(temp_avg - 24) * 0.6, 2)
            else:
                estimated_yield = round(18 - abs(temp_avg - 26) * 0.4, 2)
        else:
            error_message = f"Could not fetch forecast data for '{city}'."
    except Exception as e:
        error_message = "Network error: Unable to connect to OpenWeather map."

    return render_template('forecast.html', forecast=forecast_data, error=error_message, city=city, crop=crop, est_yield=estimated_yield)

@app.route('/fertilizer', methods=['GET', 'POST'])
def fertilizer():
    recommendation = None
    crop = "Paddy"
    soil = "Alluvial"
    
    if request.method == 'POST':
        crop = request.form.get('crop', 'Paddy')
        soil = request.form.get('soil', 'Alluvial')
        
        if crop == 'Paddy':
            recommendation = "Nitrogen (N): 120 kg/ha, Phosphorus (P): 60 kg/ha, Potassium (P2O5): 40 kg/ha. Apply Nitrogen in 3 split doses."
        elif crop == 'Maize':
            recommendation = "Nitrogen (N): 150 kg/ha, Phosphorus (P): 75 kg/ha, Potassium (P2O5): 40 kg/ha. Ensure adequate drainage."
        else:
            recommendation = "Nitrogen (N): 100 kg/ha, Phosphorus (P): 50 kg/ha, Potassium (P2O5): 50 kg/ha. Use balanced fertilizers."
            
    return render_template('fertilizer.html', recommendation=recommendation, crop=crop, soil=soil)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)