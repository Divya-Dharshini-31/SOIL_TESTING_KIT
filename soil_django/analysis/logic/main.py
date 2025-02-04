import serial
import json
import time
from analysis.logic.crop_rec import get_crop_recommendation, get_crop_accuracy
from analysis.logic.fertilizer_recommendation import recommend_fertilizer, get_fertilizer_accuracy
from analysis.logic.soil_analysis import (
    predict_soil_type, predict_npk, calculate_soil_score, 
    soil_suitability_message, get_soil_type_accuracy, predict_salinity
)
from analysis.models import SoilAnalysis, CropRecommendation, FertilizerRecommendation

import serial
import json
import time

# Define Arduino Serial Port
SERIAL_PORT = "COM3"  # Change this to the correct port (e.g., COM3 for Windows or /dev/ttyACM0 for Linux)
BAUD_RATE = 9600

def get_arduino_data():
    try:
        # Establish serial connection with Arduino
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Allow time for connection to stabilize

        # Check if data is available from Arduino
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()  # Read line from serial and decode it
            print(f"Received data from Arduino: {data}")  # Debug: print the received data
            sensor_data = json.loads(data)  # Convert JSON to Python dictionary
            return sensor_data
    except json.JSONDecodeError:
        print("Invalid JSON data received from Arduino.")
    except Exception as e:
        print(f"Error: {e}")
    
    return None

# Function to get data from Arduino or default values
def get_user_input():
    sensor_data = get_arduino_data()
    if sensor_data:
        # Get values from the Arduino sensor data
        moisture = sensor_data["Moisture"]
        temperature = sensor_data["Temperature"]
        humidity = sensor_data["Humidity"]
    else:
        # Fallback to default values in case of sensor error
        print("Warning: Using default values due to Arduino read error!")
        moisture, temperature, humidity = 10.48588446, 23.58667047, 82.36453234
    
    # Manually input pH and EC (Electrical Conductivity)
    ph = 5.630674577
    ec = 0.463015249
    
    return {
        'Electrical Conductivity (dS/m)': ec,
        'Moisture (%)': moisture,
        'pH': ph,
        'Temperature (°C)': temperature,
        'Humidity (%)': humidity        
    }





# Function to store predictions into SQLite database
def store_predictions(predicted_soil_type, npk, soil_score, suitability_message, salinity, recommended_crop, recommended_fertilizer):
    # Store Soil Analysis Data
    SoilAnalysis.objects.create(
        soil_type=predicted_soil_type,
        nitrogen=npk['Nitrogen'],
        phosphorus=npk['Phosphorus'],
        potassium=npk['Potassium'],
        soil_score=soil_score
    )
    # Store Crop Recommendation Data
    CropRecommendation.objects.create(
        soil_type=predicted_soil_type,
        recommended_crop=recommended_crop
    )
    # Store Fertilizer Recommendation Data
    FertilizerRecommendation.objects.create(
        soil_type=predicted_soil_type,
        recommended_fertilizer=recommended_fertilizer
    )
    print("Predicted data successfully stored in the database!")

# Main function to run the entire analysis
def run_soil_analysis():
    # Get user input (Arduino sensor data or default values)
    user_input = get_user_input()

    # Perform soil analysis predictions
    predicted_soil_type = predict_soil_type(user_input)
    npk = predict_npk(user_input, predicted_soil_type)
    soil_score = calculate_soil_score(npk)
    suitability_message = soil_suitability_message(soil_score)
    salinity = predict_salinity(user_input, predicted_soil_type)
    recommended_crop = get_crop_recommendation(user_input, predicted_soil_type, npk, salinity)
    recommended_fertilizer = recommend_fertilizer(user_input, predicted_soil_type, npk, salinity, recommended_crop)

    # Store the analysis results in the database
    store_predictions(predicted_soil_type, npk, soil_score, suitability_message, salinity, recommended_crop, recommended_fertilizer)

    # Print the results to the console
    print("\n--- Soil Analysis Results ---")
    print(f"Predicted Soil Type: {predicted_soil_type}")
    print(f"Predicted Nitrogen: {npk['Nitrogen']:.2f} mg/kg")
    print(f"Predicted Phosphorus: {npk['Phosphorus']:.2f} mg/kg")
    print(f"Predicted Potassium: {npk['Potassium']:.2f} mg/kg")
    print(f"Predicted Salinity: {salinity:.2f} ppm")
    print(f"Soil Score: {soil_score:.2f}")
    print(f"Soil Suitability Message: {suitability_message}")
    print(f"Recommended Crop: {recommended_crop}")
    print(f"Recommended Fertilizer: {recommended_fertilizer}")
    print(f"Fertilizer Model Accuracy: {get_fertilizer_accuracy():.2%}")

# Run the soil analysis when the script is executed
if __name__ == "__main__":
    run_soil_analysis()
