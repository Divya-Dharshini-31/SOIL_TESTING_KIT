import pandas as pd

# Load the dataset
file_path = r"C:\Users\msvic\OneDrive\Desktop\SOIL_TESTING_KIT\soil_django\SoilAnalysisModel\data\new_soil_data.csv" # Replace with your file path
data = pd.read_csv(file_path)

# 1. Count missing (null) values in the dataset
missing_values = data.isnull().sum()
print("Missing (null) values in each column:")
print(missing_values)

# 2. Count inappropriate values based on the expected ranges
# Define expected ranges for parameters (e.g., values that should not be negative or out of realistic bounds)

# Parameters and their logical range for inappropriate values
invalid_values_count = {}

# Checking for inappropriate values
# Example: negative moisture values or temperature outside expected ranges
for column in data.columns:
    if column == 'Electrical Conductivity (dS/m)':
        invalid_values_count[column] = data[column].lt(0).sum()  # Count negative values
    elif column == 'Moisture (%)':
        invalid_values_count[column] = data[column].lt(0).sum()  # Count negative values
    elif column == 'pH':
        invalid_values_count[column] = data[column].lt(0).sum()  # Count negative values
    elif column == 'Temperature (°C)':
        invalid_values_count[column] = data[column].lt(-50).sum()  # Count temperature values below -50°C
    elif column == 'Salinity (ppm)':
        invalid_values_count[column] = data[column].lt(0).sum()  # Count negative salinity values
    elif column == 'Humidity (%)':
        invalid_values_count[column] = data[column].lt(0).sum()  # Count negative humidity values
    elif column == 'Nitrogen (mg/kg)':
        invalid_values_count[column] = data[column].lt(0).sum()  # Count negative nitrogen values
    elif column == 'Phosphorus (mg/kg)':
        invalid_values_count[column] = data[column].lt(0).sum()  # Count negative phosphorus values
    elif column == 'Potassium (mg/kg)':
        invalid_values_count[column] = data[column].lt(0).sum()  # Count negative potassium values

# Print the counts of inappropriate values
print("\nInappropriate values (e.g., negative or out of range values):")
for column, count in invalid_values_count.items():
    print(f"{column}: {count} invalid values")

