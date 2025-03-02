import serial
import time
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('task-ca681-firebase-adminsdk-fbsvc-58d9a55c9d.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://task-ca681-default-rtdb.firebaseio.com/' #This part iteracts with the firebase
})

ser = serial.Serial('COM7', 9600)  #Adjusted serial port and the baud rate
ser.flushInput()

def parse_data(data):
   
    components = data.split(' | ')#This line splits the data strings into components based on '|'
    if len(components) == 3:
        try:
            x = float(components[0].split(': ')[1])
            y = float(components[1].split(': ')[1])
            z = float(components[2].split(': ')[1])
            return x, y, z
        except ValueError as e:
            print(f"Error extracting float values: {e}")
    return None, None, None
try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()#This reads line of data from the serial port.
            print(f"Received data: {data}") #This receives the data
            x, y, z = parse_data(data)# This parses the data string to extract the x, y, z
            if x is not None and y is not None and z is not None:
                timestamp = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
                data_json = {
                    'timestamp': timestamp,
                    'x': x,
                    'y': y,
                    'z': z
                }
                start_time = time.time()
                db.reference('gyroscope_data').push(data_json)
                end_time = time.time()
                upload_time = end_time - start_time
                print(f"Uploaded data: {data_json} in {upload_time:.4f} seconds") 
            else:
                print(f"Error parsing data: {data}")
finally:
    ser.close()#This ensure that the serial port is closed when the script exits.

import csv
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate('task-ca681-firebase-adminsdk-fbsvc-58d9a55c9d.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://task-ca681-default-rtdb.firebaseio.com/'
})

# Query data from Firebase
data_ref = db.reference('gyroscope_data')
data = data_ref.get()

# Save data to CSV
with open('gyroscope_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'x', 'y', 'z'])
    for key, value in data.items():
        writer.writerow([value['timestamp'], value['x'], value['y'], value['z']])

print("Data has been successfully saved to gyroscope_data.csv")


import pandas as pd

# Read CSV
data = pd.read_csv('gyroscope_data.csv')

# Clean data (remove rows with non-number or empty fields)
cleaned_data = data.dropna()
cleaned_data = cleaned_data[(cleaned_data['x'].apply(lambda x: isinstance(x, (int, float)))) &
                            (cleaned_data['y'].apply(lambda x: isinstance(x, (int, float)))) &
                            (cleaned_data['z'].apply(lambda x: isinstance(x, (int, float))))]

# Save cleaned data back to CSV
cleaned_data.to_csv('gyroscope_data_cleaned.csv', index=False)

print("Cleaned data has been successfully saved to gyroscope_data_cleaned.csv")

import pandas as pd
import matplotlib.pyplot as plt

# Read cleaned CSV
data = pd.read_csv('gyroscope_data_cleaned.csv')

# Plot x, y, z separately
plt.figure()
data['x'].plot(title='Gyroscope X Data')
plt.figure()
data['y'].plot(title='Gyroscope Y Data')
plt.figure()
data['z'].plot(title='Gyroscope Z Data')

# Combined plot
plt.figure()
data[['x', 'y', 'z']].plot(title='Gyroscope XYZ Data')

plt.show()

print("Plots have been generated successfully.")
