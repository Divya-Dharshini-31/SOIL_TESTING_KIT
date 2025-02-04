import pandas as pd
import os
# Define the path to the data folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "analysis", "data")
# Load the CSV datasets
df_soil = pd.read_csv(os.path.join(DATA_PATH, "soil_data.csv"))
df_nutrients = pd.read_csv(os.path.join(DATA_PATH, "nutrients.csv"))
df_climate = pd.read_csv(os.path.join(DATA_PATH, "climate_data.csv"))
df_crop_fertilizer = pd.read_csv(os.path.join(DATA_PATH, "crop_fertilizer.csv"))

# Display first few rows to verify loading
print(df_soil.head())
print(df_nutrients.head())
print(df_climate.head())
print(df_crop_fertilizer.head())
# Merge datasets based on common columns

# Merge soil data with nutrients data on 'Soil Type'
df_merged = pd.merge(df_soil, df_nutrients, on="Soil Type", how="outer")

# Merge the result with climate data on 'Temperature'
df_merged = pd.merge(df_merged, df_climate, on="Temperature", how="outer")

# Merge the result with crop fertilizer data on 'Soil Type'
df_final = pd.merge(df_merged, df_crop_fertilizer, on="Soil Type", how="outer")

# Display first few rows of the merged data
print(df_final.head())
# Fill missing numerical values with the mean of the respective column
df_final.fillna(df_final.mean(), inplace=True)

# Fill missing categorical values with "Unknown"
df_final.fillna("Unknown", inplace=True)

# Display the cleaned-up data
print(df_final.head())
# Save the final dataset to a CSV file
df_final.to_csv(os.path.join(DATA_PATH, "final_dataset.csv"), index=False)

# Print confirmation message
print("Merged dataset saved successfully as 'final_dataset.csv'!")
