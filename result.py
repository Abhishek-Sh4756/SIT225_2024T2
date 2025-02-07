import pandas as pd #import pandas and matplotlib 
import matplotlib.pyplot as plt

filename = "Data_collection.csv"
df = pd.read_csv(filename)  #Reads the sensor data from a CSV file named Data_collection.csv into a DataFrame called df.

df['Timestamp'] = pd.to_datetime(df['Time'], format="%Y%m%d%H%M%S") #Converts the 'Time' column into datetime objects, allowing you to work with time-series data more effectively.

df['Distance in (cm)'] = df['Distance in (cm)'].astype(str).str.extract(r'(\d+)') #Extracts numeric values from the 'Distance in (cm)' column, ensuring the distance measurements are in a usable format.

df['Smoothed_Distance'] = df['Distance in (cm)'].rolling(window=5, min_periods=1).mean()

plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Smoothed_Distance'], markersize=1, linestyle='-', color='b') #Applies a rolling average with a window size of 5 to the distance readings, creating a new column Smoothed_Distance to smooth out fluctuations in the data.
plt.xlabel('Time')
plt.ylabel('Distance (cm)')
plt.title('Ultrasonic Sensor Readings (Smoothed)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show() #Displays the plot
