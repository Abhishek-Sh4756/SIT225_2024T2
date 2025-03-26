import serial
import csv
import time


SERIAL_PORT = "COM7"  
BAUD_RATE = 9600


ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  


with open("sensor_data.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Temperature", "Humidity"])  

    try:
        while True:
            data = ser.readline().decode().strip()  
            if data:
                values = data.split(",")
                if len(values) == 2:
                    temperature, humidity = values
                    writer.writerow([float(temperature), float(humidity)])
                    print(f"Saved: {temperature}°C, {humidity}%")
    except KeyboardInterrupt:
        print("Data collection stopped.")
    finally:
        ser.close()

 