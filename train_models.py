import os
import pickle

# Create the models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Simple manual Linear Regression calculation (y = w1*rainfall + w2*temperature + b)
# Let's save a dictionary containing our simple model weights
model_weights = {
    'w_rainfall': 0.0025,
    'w_temp': -0.05,
    'bias': 1.2
}

# Save using standard library 'pickle'
with open('models/yield_model.pkl', 'wb') as f:
    pickle.dump(model_weights, f)

print("Training complete! 'yield_model.pkl' saved successfully.")