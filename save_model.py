import joblib

# Assume `model` is your trained machine learning model
model = 'soil_analysis.py'  # Replace with your trained model
joblib.dump(model, 'soil_model.pkl')
print("Model saved as soil_model.pkl")