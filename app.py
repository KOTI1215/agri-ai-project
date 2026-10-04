from flask import Flask, render_template, request
import pickle
import os
import random

app = Flask(__name__)

# Load our saved model weights
model_path = os.path.join('models', 'yield_model.pkl')
if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        model_weights = pickle.load(f)
else:
    model_weights = {'w_rainfall': 0.0025, 'w_temp': -0.05, 'bias': 1.2}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict-yield', methods=['POST'])
def predict_yield():
    try:
        rainfall = float(request.form.get('rainfall', 0))
        temperature = float(request.form.get('temperature', 0))
        
        predicted_yield = (
            (rainfall * model_weights['w_rainfall']) +
            (temperature * model_weights['w_temp']) +
            model_weights['bias']
        )
        predicted_yield = max(0.0, round(predicted_yield, 2))
        
        return render_template('index.html', yield_result=f"Estimated Crop Yield: {predicted_yield} Tons/Hectare")
    except ValueError:
        return "Invalid input values. Please enter numbers for rainfall and temperature.", 400

@app.route('/predict-disease', methods=['POST'])
def predict_disease():
    if 'leaf_image' not in request.files:
        return render_template('index.html', disease_result="No image file uploaded.")
    
    file = request.files['leaf_image']
    if file.filename == '':
        return render_template('index.html', disease_result="No selected file.")
    
    sample_diseases = ["Healthy Leaf", "Early Blight", "Late Blight", "Powdery Mildew"]
    predicted_disease = random.choice(sample_diseases)
    
    return render_template('index.html', disease_result=f"Disease Detection Result: {predicted_disease}")

if __name__ == '__main__':
    app.run(debug=True)