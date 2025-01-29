import serial
import time
import random # Generates random number

arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1) #This helps to open serial port and helps to connect with the arduino

while True:
    num_to_send = random.randint(1, 10) 
    
    # Log and send the number to Arduino
    print(f"Sending number to Arduino: {num_to_send}") 
    arduino.write(f"{num_to_send}\n".encode()) #Sends the generated number to the Arduino over the serial connection. The number is then encoded to bytes 
                                                                     
    
    # Waits for the Arduino to send back a number
    while True:
        if arduino.in_waiting > 0:
            received_num = int(arduino.readline().decode().strip()) #Converts bytes received from arduino in string
            print(f"Received number from Arduino: {received_num}")
            break
    
    # Sleep for the received number of seconds
    print(f"Sleeping for {received_num} seconds")
    time.sleep(received_num)
    print("Finished sleeping")
