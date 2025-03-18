# import paho.mqtt.client as mqtt
# import json
# import redis
# from datetime import datetime, timezone

# # 🔹 MQTT Configuration (HiveMQ)
# MQTT_BROKER = "30de0bc86b6746809e2ddf90ea985a4f.s1.eu.hivemq.cloud"
# MQTT_PORT = 8883
# MQTT_TOPIC = "sensor/gyroscope"
# MQTT_USER = "hivemq.webclient.1742277085499"
# MQTT_PASSWORD = "*z32eR?gyOA0Wm%U.H4k"

# # 🔹 Redis Configuration
# REDIS_URL = "redis://default:X9jbUvTHaHFjMDUh0ltqmWANtr5PvWPa@redis-16428.c259.us-central1-2.gce.redns.redis-cloud.com:16428"
# r = redis.from_url(REDIS_URL)

# # 🔹 MQTT Callbacks
# def on_connect(mqtt_client, userdata, flags, rc, properties=None):
#     if rc == 0:
#         print("✅ Connected to MQTT Broker!")
#         mqtt_client.subscribe(MQTT_TOPIC)
#     else:
#         print(f"❌ MQTT Connection Failed! Error Code: {rc}")

# def on_message(mqtt_client, userdata, msg):
#     try:
#         data = json.loads(msg.payload.decode())  # Decode the JSON data received from MQTT
#         print(f"📩 Received: {data}")

#         if all(k in data for k in ["x", "y", "z"]):  # Check if data contains x, y, z
#             timestamp = datetime.now(timezone.utc).isoformat()  # Get the timestamp in ISO format
#             redis_data = {
#                 "timestamp": timestamp,
#                 "x": float(data["x"]),
#                 "y": float(data["y"]),
#                 "z": float(data["z"]),
#             }
            
#             # Store data in Redis (as a hash)
#             redis_key = f"gyroscope:{timestamp}"
#             r.hmset(redis_key, redis_data)
#             print(f"✅ Data Written to Redis: {redis_data}")
#         else:
#             print("❌ Invalid Data Format!")
#     except json.JSONDecodeError:
#         print("❌ JSON Decode Error!")
#     except Exception as e:
#         print(f"❌ Redis Write Error: {repr(e)}")

# # 🔹 Initialize MQTT Client
# mqtt_client = mqtt.Client()
# mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
# mqtt_client.tls_set()

# mqtt_client.on_connect = on_connect
# mqtt_client.on_message = on_message

# # 🔹 Start MQTT & Listen
# print("🔗 Connecting to MQTT Broker...")
# mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
# mqtt_client.loop_forever()









# import pandas as pd
# import redis
# import json

# # 🔹 Redis Configuration
# redis_url = "redis://default:X9jbUvTHaHFjMDUh0ltqmWANtr5PvWPa@redis-16428.c259.us-central1-2.gce.redns.redis-cloud.com:16428"
# redis_client = redis.StrictRedis.from_url(redis_url, decode_responses=True)  # Replace with your Redis server address

# # 🔹 Check if Redis is connected
# try:
#     if redis_client.ping():
#         print("✅ Successfully connected to Redis!")
# except redis.ConnectionError as e:
#     print(f"❌ Redis connection failed: {e}")
#     exit()

# # 🔹 Fetch Data from Redis (using the correct pattern)
# keys = redis_client.keys("gyroscope:*")  # Fetch all keys starting with 'gyroscope:'

# # Log the found keys to see what we're dealing with
# print(f"Found {len(keys)} keys: {keys}")

# # 🔹 Prepare Data to Convert to CSV
# data_list = []
# for key in keys:
#     try:
#         # Check the type of the key first
#         key_type = redis_client.type(key)
#         print(f"Key: {key}, Type: {key_type}")

#         if key_type == 'string':
#             # If the key holds a string (expected case)
#             stored_data = redis_client.get(key)
#             print(f"Fetched string data: {stored_data}")
#             if stored_data:
#                 data = json.loads(stored_data)  # Parse the JSON string back to a Python dict
#                 data_list.append(data)

#         elif key_type == 'hash':
#             # If the key holds a hash (e.g., a dictionary of fields)
#             stored_data = redis_client.hgetall(key)  # Fetch all fields in the hash
#             print(f"Fetched hash data: {stored_data}")
#             if stored_data:
#                 # Convert the hash to a dict (if it's in the format we expect)
#                 data_list.append(stored_data)

#         elif key_type == 'list':
#             # If the key holds a list (you would need to handle each list item appropriately)
#             stored_data = redis_client.lrange(key, 0, -1)  # Fetch all list elements
#             print(f"Fetched list data: {stored_data}")
#             for item in stored_data:
#                 # Assuming each item is a JSON string, parse it
#                 data_list.append(json.loads(item))

#         else:
#             print(f"Skipping key {key} with unsupported type {key_type}")

#     except Exception as e:
#         print(f"Error retrieving data from Redis for key {key}: {e}")

# # 🔹 Convert to Pandas DataFrame
# if data_list:
#     df = pd.DataFrame(data_list)

#     # Optional: Rename 'timestamp' column to proper format if necessary
#     if 'timestamp' in df.columns:
#         df['timestamp'] = pd.to_datetime(df['timestamp'])

#     # 🔹 Save to CSV
#     df.to_csv("gyroscope_dataRedis.csv", index=False)
#     print("✅ Data saved to 'gyroscope_dataRedis.csv'")
# else:
#     print("⚠️ No data found in Redis!")








import pandas as pd
import redis
import matplotlib.pyplot as plt
import json

# 🔹 Redis Configuration
redis_url = "redis://default:X9jbUvTHaHFjMDUh0ltqmWANtr5PvWPa@redis-16428.c259.us-central1-2.gce.redns.redis-cloud.com:16428"
redis_client = redis.StrictRedis.from_url(redis_url, decode_responses=True)  # Replace with your Redis server address

# 🔹 Check if Redis is connected
try:
    if redis_client.ping():
        print("✅ Successfully connected to Redis!")
except redis.ConnectionError as e:
    print(f"❌ Redis connection failed: {e}")
    exit()

# 🔹 Fetch Data from Redis (using the correct pattern)
keys = redis_client.keys("gyroscope:*")  # Fetch all keys starting with 'gyroscope:'

# Log the found keys to see what we're dealing with
print(f"Found {len(keys)} keys: {keys}")

# 🔹 Prepare Data to Convert to CSV
data_list = []
for key in keys:
    try:
        # Check the type of the key first
        key_type = redis_client.type(key)
        print(f"Key: {key}, Type: {key_type}")

        if key_type == 'string':
            # If the key holds a string (expected case)
            stored_data = redis_client.get(key)
            print(f"Fetched string data: {stored_data}")
            if stored_data:
                data = json.loads(stored_data)  # Parse the JSON string back to a Python dict
                data_list.append(data)

        elif key_type == 'hash':
            # If the key holds a hash (e.g., a dictionary of fields)
            stored_data = redis_client.hgetall(key)  # Fetch all fields in the hash
            print(f"Fetched hash data: {stored_data}")
            if stored_data:
                # Convert the hash to a dict (if it's in the format we expect)
                data_list.append(stored_data)

        elif key_type == 'list':
            # If the key holds a list (you would need to handle each list item appropriately)
            stored_data = redis_client.lrange(key, 0, -1)  # Fetch all list elements
            print(f"Fetched list data: {stored_data}")
            for item in stored_data:
                # Assuming each item is a JSON string, parse it
                data_list.append(json.loads(item))

        else:
            print(f"Skipping key {key} with unsupported type {key_type}")

    except Exception as e:
        print(f"Error retrieving data from Redis for key {key}: {e}")

# 🔹 Data Cleaning
if data_list:
    # Convert data to pandas DataFrame
    df = pd.DataFrame(data_list)

    # Check if we have 'x', 'y', 'z' columns and clean them
    if 'x' in df.columns and 'y' in df.columns and 'z' in df.columns:
        # Handle missing values
        df.fillna(method='ffill', inplace=True)  # Fill missing values with the last valid
        df.fillna(0, inplace=True)  # If still missing, replace with 0
        
        # Convert timestamp to readable format if 'timestamp' exists
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Remove duplicate entries (if any)
        df.drop_duplicates(inplace=True)

        # Save cleaned data to CSV
        df.to_csv("cleaned_gyroscope_dataRedis.csv", index=False)
        print("✅ Cleaned data saved to 'cleaned_gyroscope_dataRedis.csv'")

        # 🔹 Plot: Separate Graphs for X, Y, Z axes
        fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

        axs[0].plot(df["timestamp"], df["x"], color="red")
        axs[0].set_title("X-Axis Gyroscope Readings")
        axs[0].set_ylabel("X Value")
        axs[0].grid(True)

        axs[1].plot(df["timestamp"], df["y"], color="green")
        axs[1].set_title("Y-Axis Gyroscope Readings")
        axs[1].set_ylabel("Y Value")
        axs[1].grid(True)

        axs[2].plot(df["timestamp"], df["z"], color="blue")
        axs[2].set_title("Z-Axis Gyroscope Readings")
        axs[2].set_ylabel("Z Value")
        axs[2].set_xlabel("Timestamp")
        axs[2].grid(True)

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # 🔹 Plot: Combined Graph for all axes (X, Y, Z)
        plt.figure(figsize=(12, 6))
        plt.plot(df["timestamp"], df["x"], label="X-axis", color="red")
        plt.plot(df["timestamp"], df["y"], label="Y-axis", color="green")
        plt.plot(df["timestamp"], df["z"], label="Z-axis", color="blue")

        plt.xlabel("Timestamp")
        plt.ylabel("Gyroscope Readings")
        plt.title("Gyroscope Sensor Data Over Time (Combined)")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

    else:
        print("⚠️ Missing required columns 'x', 'y', or 'z' in the data!")
else:
    print("⚠️ No data found in Redis!")
