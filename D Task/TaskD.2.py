import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from datetime import datetime, timezone

# 🔹 MQTT Configuration (HiveMQ)
MQTT_BROKER = "0d8eb4634b0d4b27ada26dc0fe9ee54f.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "sensor/gyroscope"
MQTT_USER = "hivemq.webclient.1742039592442"
MQTT_PASSWORD = "*z32eR?gyOA0Wm%U.H4k"

# 🔹 InfluxDB Configuration
INFLUXDB_URL = "https://us-east-1-1.aws.cloud2.influxdata.com/"
INFLUXDB_TOKEN = "hjOk4Xn6qAc3VL5d7ju75-Q1jgPhUV9D6UJ6mcJB1KfYaHuNoWAZ8Bcs3DsUfFntB96YhAB4fmC284zfPVzEnw=="
INFLUXDB_ORG = "57248786c86cc209"  # Replace with your actual org name
INFLUXDB_BUCKET = "gyro"

# 🔹 Connect to InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# 🔹 MQTT Callbacks
def on_connect(mqtt_client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        mqtt_client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ MQTT Connection Failed! Error Code: {rc}")

def on_message(mqtt_client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"📩 Received: {data}")

        if all(k in data for k in ["x", "y", "z"]):
            point = (
                Point("gyroscope")
                .field("x", float(data["x"]))
                .field("y", float(data["y"]))
                .field("z", float(data["z"]))
                .time(datetime.now(timezone.utc), WritePrecision.NS)
            )
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            print("✅ Data Written to InfluxDB")
        else:
            print("❌ Invalid Data Format!")
    except json.JSONDecodeError:
        print("❌ JSON Decode Error!")
    except Exception as e:
        print(f"❌ InfluxDB Write Error: {repr(e)}")

# 🔹 Initialize MQTT Client
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.tls_set()

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# 🔹 Start MQTT & Listen
print("🔗 Connecting to MQTT Broker...")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_forever()





import pandas as pd
from influxdb_client import InfluxDBClient

# 🔹 InfluxDB Configuration
INFLUXDB_URL = "https://us-east-1-1.aws.cloud2.influxdata.com/"
INFLUXDB_TOKEN = "hjOk4Xn6qAc3VL5d7ju75-Q1jgPhUV9D6UJ6mcJB1KfYaHuNoWAZ8Bcs3DsUfFntB96YhAB4fmC284zfPVzEnw=="
INFLUXDB_ORG = "57248786c86cc209"
INFLUXDB_BUCKET = "gyro"

# 🔹 Connect to InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()

# 🔹 Query Data from InfluxDB
query = f"""
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -24h)  // Fetch last 24 hours of data
  |> filter(fn: (r) => r._measurement == "gyroscope")
  |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn: "_value")
  |> keep(columns: ["_time", "x", "y", "z"])
"""

result = query_api.query_data_frame(query)

# 🔹 Convert to CSV
if not result.empty:
    result.rename(columns={"_time": "timestamp"}, inplace=True)  # Rename timestamp column
    result.to_csv("gyroscope_data.csv", index=False)
    print("✅ Data saved to 'gyroscope_data.csv'")
else:
    print("⚠️ No data found in InfluxDB!")





import pandas as pd
from influxdb_client import InfluxDBClient

# 🔹 InfluxDB Configuration
INFLUXDB_URL = "https://us-east-1-1.aws.cloud2.influxdata.com/"
INFLUXDB_TOKEN = "hjOk4Xn6qAc3VL5d7ju75-Q1jgPhUV9D6UJ6mcJB1KfYaHuNoWAZ8Bcs3DsUfFntB96YhAB4fmC284zfPVzEnw=="
INFLUXDB_ORG = "57248786c86cc209"
INFLUXDB_BUCKET = "gyro"

# 🔹 Connect to InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()

# 🔹 Query Data from InfluxDB
query = f"""
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -24h)  // Fetch last 24 hours of data
  |> filter(fn: (r) => r._measurement == "gyroscope")
  |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn: "_value")
  |> keep(columns: ["_time", "x", "y", "z"])
"""

result = query_api.query_data_frame(query)

# 🔹 Data Cleaning
if not result.empty:
    # Rename timestamp column
    result.rename(columns={"_time": "timestamp"}, inplace=True)
    
    # Convert timestamp to readable format
    result["timestamp"] = pd.to_datetime(result["timestamp"]).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Handle missing values (fill with previous values or zero if no previous value)
    result.fillna(method='ffill', inplace=True)
    result.fillna(0, inplace=True)  # If still missing, replace with 0
    
    # Remove duplicate entries (if any)
    result.drop_duplicates(inplace=True)
    
    # Save cleaned data to CSV
    result.to_csv("cleaned_gyroscope_data.csv", index=False)
    
    print("✅ Cleaned data saved to 'cleaned_gyroscope_data.csv'")
else:
    print("⚠️ No data found in InfluxDB!")




import pandas as pd
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient

# 🔹 InfluxDB Configuration
INFLUXDB_URL = "https://us-east-1-1.aws.cloud2.influxdata.com/"
INFLUXDB_TOKEN = "hjOk4Xn6qAc3VL5d7ju75-Q1jgPhUV9D6UJ6mcJB1KfYaHuNoWAZ8Bcs3DsUfFntB96YhAB4fmC284zfPVzEnw=="
INFLUXDB_ORG = "57248786c86cc209"
INFLUXDB_BUCKET = "gyro"

# 🔹 Connect to InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()

# 🔹 Query Data from InfluxDB
query = f"""
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -24h)  // Fetch last 24 hours of data
  |> filter(fn: (r) => r._measurement == "gyroscope")
  |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn: "_value")
  |> keep(columns: ["_time", "x", "y", "z"])
"""

result = query_api.query_data_frame(query)

# 🔹 Data Cleaning
if not result.empty:
    # Rename timestamp column
    result.rename(columns={"_time": "timestamp"}, inplace=True)
    
    # Convert timestamp to readable format
    result["timestamp"] = pd.to_datetime(result["timestamp"])
    
    # Handle missing values
    result.fillna(method='ffill', inplace=True)  # Fill missing values with last valid
    result.fillna(0, inplace=True)  # If still missing, replace with 0
    
    # Remove duplicate entries
    result.drop_duplicates(inplace=True)
    
    # Save cleaned data to CSV
    result.to_csv("cleaned_gyroscope_data.csv", index=False)
    
    print("✅ Cleaned data saved to 'cleaned_gyroscope_data.csv'")

    # 🔹 Plot: Separate Graphs
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    axs[0].plot(result["timestamp"], result["x"], color="red")
    axs[0].set_title("X-Axis Gyroscope Readings")
    axs[0].set_ylabel("X Value")
    axs[0].grid(True)

    axs[1].plot(result["timestamp"], result["y"], color="green")
    axs[1].set_title("Y-Axis Gyroscope Readings")
    axs[1].set_ylabel("Y Value")
    axs[1].grid(True)

    axs[2].plot(result["timestamp"], result["z"], color="blue")
    axs[2].set_title("Z-Axis Gyroscope Readings")
    axs[2].set_ylabel("Z Value")
    axs[2].set_xlabel("Timestamp")
    axs[2].grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 🔹 Plot: Combined Graph
    plt.figure(figsize=(12, 6))
    plt.plot(result["timestamp"], result["x"], label="X-axis", color="red")
    plt.plot(result["timestamp"], result["y"], label="Y-axis", color="green")
    plt.plot(result["timestamp"], result["z"], label="Z-axis", color="blue")

    plt.xlabel("Timestamp")
    plt.ylabel("Gyroscope Readings")
    plt.title("Gyroscope Sensor Data Over Time (Combined)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

else:
    print("⚠️ No data found in InfluxDB!")
