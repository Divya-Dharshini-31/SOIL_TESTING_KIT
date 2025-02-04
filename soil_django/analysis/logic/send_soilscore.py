import serial
import requests
import time

# Initialize serial communication with Arduino (adjust the port as needed)
ser = serial.Serial('COM3', 9600)  # Replace COM3 with your Arduino port

# URL of the Django view that sends the soil score
url = 'http://127.0.0.1:8000/soil-analysis/'

while True:
    # Read data from Arduino
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        print(f"Received Data: {data}")

        # Convert the data into a dictionary (adjust this part based on your Arduino output)
        try:
            data_dict = eval(data)  # Convert the JSON string into a dictionary
            print(f"Sending Data: {data_dict}")  # Log the data being sent
        except Exception as e:
            print(f"Error parsing data: {e}")
            continue

        # Send the data to Django via POST request
        try:
            response = requests.post(url, data=data_dict)

            # Check if the data was successfully sent
            if response.status_code == 200:
                print("Data successfully sent to Django.")

                # Now retrieve the soil score from Django (get it from the response)
                soil_score = response.json().get('soil_score', None)

                if soil_score is not None:
                    # Send the soil score back to Arduino
                    ser.write(str(soil_score).encode())  # Send soil score as a string
                    print(f"Sent soil score {soil_score} back to Arduino.")
                else:
                    print("Soil score not found in response.")
            else:
                print(f"Failed to send data to Django. Status code: {response.status_code}")
                print(f"Response content: {response.text}")  # Log the error message
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to Django: {e}")
    
    time.sleep(2)  # Adjust the delay time as needed