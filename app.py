from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime

app = Flask(__name__)

# Configure SQLite Database for History Log
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farming_v2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class HistoryRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(50), nullable=False)
    input_details = db.Column(db.String(200), nullable=False)
    result_details = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.String(50), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Create database tables
with app.app_context():
    db.create_all()

# Helper function for smart irrigation advice
def get_irrigation_advice(temp, humidity, condition):
    condition_lower = condition.lower()
    if 'rain' in condition_lower or 'shower' in condition_lower:
        return "Rain detected or expected. Irrigation is NOT recommended to prevent over-watering."
    elif temp > 35 and humidity < 40:
        return "High temperature and low humidity conditions! Heavy irrigation is advised during early morning or late evening."
    elif temp > 30:
        return "Moderate to high temperature. Regular scheduled irrigation is recommended."
    else:
        return "Weather conditions are stable. Standard moderate irrigation will suffice."

@app.route('/')
def index():
    history = HistoryRecord.query.order_by(HistoryRecord.id.desc()).all()
    # Passing temp=None ensures Jinja doesn't throw an undefined error on initial page load
    return render_template('index.html', history=history, temp=None)

@app.route('/weather', methods=['POST'])
def weather_advisory():
    city = request.form.get('city')
    api_key = "ed74c3c9c0a6178094737c755b201224"  # Replace with your actual OpenWeatherMap API key

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    history = HistoryRecord.query.order_by(HistoryRecord.id.desc()).all()

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        condition = data['weather'][0]['description']
        city_name = data['name']

        irrigation_advice = get_irrigation_advice(temp, humidity, condition)

        # Save to history log
        new_record = HistoryRecord(
            record_type='Weather & Irrigation Advisory',
            input_details=f'City: {city_name}',
            result_details=f'Temp: {temp}°C, Humidity: {humidity}%, Condition: {condition}'
        )
        db.session.add(new_record)
        db.session.commit()

        return render_template(
            'index.html',
            city=city_name,
            temp=temp,
            humidity=humidity,
            condition=condition,
            irrigation_advice=irrigation_advice,
            history=HistoryRecord.query.order_by(HistoryRecord.id.desc()).all()
        )
    else:
        return render_template(
            'index.html',
            error="Error fetching weather data. Please check city name.",
            temp=None,
            history=history
        )

@app.route('/fertilizer', methods=['POST'])
def fertilizer_recommendation():
    crop = request.form.get('crop')
    n = request.form.get('nitrogen')
    p = request.form.get('phosphorus')
    k = request.form.get('potassium')

    recommendation = f"Recommended fertilizer application for {crop} based on NPK levels."

    new_record = HistoryRecord(
        record_type='Fertilizer Recommendation',
        input_details=f'Crop: {crop} (N:{n}, P:{p}, K:{k})',
        result_details=recommendation
    )
    db.session.add(new_record)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/pest', methods=['POST'])
def pest_advisory():
    symptom = request.form.get('symptom')
    advice = f"Treatment advisory for symptom: {symptom}. Apply organic pesticide or consult local agronomist."

    new_record = HistoryRecord(
        record_type='Pest & Disease Advisory',
        input_details=f'Symptom: {symptom}',
        result_details=advice
    )
    db.session.add(new_record)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)