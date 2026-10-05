from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    # Dynamically grab the city from the submitted form (POST) or URL parameter (GET)
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
            error_message = f"Could not find weather data for '{city}'. Please check the city name."
    except Exception as e:
        error_message = "Network error: Unable to connect to OpenWeather map."

    return render_template('weather.html', weather=weather_data, error=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)