import paho.mqtt.client as mqtt
from pymongo import MongoClient
import pandas as pd
import time
import json

# MQTT broker details
broker = "30de0bc86b6746809e2ddf90ea985a4f.s1.eu.hivemq.cloud"  # HiveMQ URL
port = 8883  # Secure MQTT port (TLS)
topic = "sensor/gyroscope"  # MQTT topic

# MongoDB connection details
mongo_client = MongoClient("mongodb+srv://abhishek172006:or3LcQebfRNNTEFK@cluster0.a6i1u.mongodb.net/")  # MongoDB URI
db = mongo_client["gyroscope_data"]  # Database name
collection = db["readings"]  # Collection name

# Initialize the MQTT client
mqtt_client = mqtt.Client()  # MQTT client initialization
mqtt_client.tls_set()  # Enable TLS for secure MQTT connection

# Function to handle successful connection to MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to the MQTT Broker!")
        client.subscribe(topic)  # Subscribe to the specified topic
    else:
        print(f"Connection failed, return code {rc}")

# Function to handle incoming messages from the MQTT broker
def on_message(client, userdata, message):
    try:
        # Decode the received MQTT message and parse the payload
        received_data = json.loads(message.payload.decode())
        received_data["timestamp"] = time.time()  # Add current timestamp to the data
        print(f"Received data: {received_data}")
        
        # Insert the data into MongoDB
        collection.insert_one(received_data)  # Use the correct variable here
    except Exception as e:
        print(f"Error processing the incoming message: {e}")

# Configure MQTT client with username, password, and callbacks
mqtt_client.username_pw_set("hivemq.webclient.1742277085499", "*z32eR?gyOA0Wm%U.H4k")  # Provide MQTT credentials
mqtt_client.on_connect = on_connect  # Attach connect handler
mqtt_client.on_message = on_message  # Attach message handler

# Connect to the MQTT broker
mqtt_client.connect(broker, port)

# Start the MQTT loop and collect data for 30 minutes
print("Starting data collection...")
start_time = time.time()
mqtt_client.loop_start()  # Begin the non-blocking loop
while time.time() - start_time < 30 * 60:  # Collect data for 30 minutes
    time.sleep(1)
mqtt_client.loop_stop()  # Stop the MQTT loop once data collection is complete
print("Data collection completed. Please check MongoDB for the stored data.")

# Step 6: Retrieve all data from MongoDB and export to CSV
print("Exporting collected data to CSV...")
all_data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB default "_id" field
data_frame = pd.DataFrame(all_data)  # Convert data into a Pandas DataFrame

# Export raw data to a CSV file
csv_output_file = "gyroscope_raw_data.csv"
data_frame.to_csv(csv_output_file, index=False)
print(f"Raw data exported successfully to {csv_output_file}")

# Step 7: Clean the collected data
print("Cleaning the collected data...")
data_frame = data_frame.dropna()  # Remove rows containing any missing values
data_frame = data_frame[data_frame.applymap(lambda x: isinstance(x, (int, float))).all(1)]  # Keep only numeric rows

# Export the cleaned data to a new CSV file
cleaned_csv_output_file = "gyroscope_cleaned_data.csv"
data_frame.to_csv(cleaned_csv_output_file, index=False)
print(f"Cleaned data exported successfully to {cleaned_csv_output_file}")

import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient

# MongoDB connection details
mongo_client = MongoClient("mongodb+srv://abhishek172006:or3LcQebfRNNTEFK@cluster0.a6i1u.mongodb.net/")  # MongoDB URI
db = mongo_client["gyroscope_data"]  # Database name
collection = db["readings"]  # Collection name

# Step 1: Retrieve all data from MongoDB
print("Retrieving collected data from MongoDB...")
all_data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB default "_id" field
data_frame = pd.DataFrame(all_data)  # Convert data into a Pandas DataFrame

# Step 2: Plot the raw data (assuming x, y, z and timestamp columns exist)
if not data_frame.empty:
    # Convert timestamp to a readable format
    data_frame['timestamp'] = pd.to_datetime(data_frame['timestamp'], unit='s')

    # Step 3: Separate Graphs for X, Y, Z axes
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    axs[0].plot(data_frame['timestamp'], data_frame['x'], color="red")
    axs[0].set_title("X-Axis Gyroscope Readings")
    axs[0].set_ylabel("X Value")
    axs[0].grid(True)

    axs[1].plot(data_frame['timestamp'], data_frame['y'], color="green")
    axs[1].set_title("Y-Axis Gyroscope Readings")
    axs[1].set_ylabel("Y Value")
    axs[1].grid(True)

    axs[2].plot(data_frame['timestamp'], data_frame['z'], color="blue")
    axs[2].set_title("Z-Axis Gyroscope Readings")
    axs[2].set_ylabel("Z Value")
    axs[2].set_xlabel("Timestamp")
    axs[2].grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Step 4: Combined Graph for X, Y, Z axes over time
    plt.figure(figsize=(12, 6))
    plt.plot(data_frame['timestamp'], data_frame['x'], label="X-axis", color="red")
    plt.plot(data_frame['timestamp'], data_frame['y'], label="Y-axis", color="green")
    plt.plot(data_frame['timestamp'], data_frame['z'], label="Z-axis", color="blue")

    plt.xlabel("Timestamp")
    plt.ylabel("Gyroscope Readings")
    plt.title("Gyroscope Sensor Data Over Time (Combined)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

else:
    print("⚠️ No data found in MongoDB!")

