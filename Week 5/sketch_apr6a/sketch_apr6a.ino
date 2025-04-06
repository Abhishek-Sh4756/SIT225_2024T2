#include <Wire.h>
#include <LSM6DS3.h>

LSM6DS3 myIMU(I2C_MODE, 0x6A);

void setup() {
    Serial.begin(9600); 
    while (!Serial);    // Wait for Serial Monitor to open 

  
    if (myIMU.begin() != 0) {
        Serial.println("Failed to initialize LSM6DS3 sensor!");
        while (1); 
    }
    Serial.println("LSM6DS3 sensor initialized successfully.");
    Serial.println("Gyroscope Data (X, Y, Z) in dps:");
}

void loop() {
    // Read gyroscope data (X, Y, Z)
    float gyroX = myIMU.readFloatGyroX();
    float gyroY = myIMU.readFloatGyroY();
    float gyroZ = myIMU.readFloatGyroZ();

    // Print data to Serial Monitor
    Serial.print("X: ");
    Serial.print(gyroX, 2); // Print with 2 decimal places
    Serial.print(" dps | Y: ");
    Serial.print(gyroY, 2);
    Serial.print(" dps | Z: ");
    Serial.print(gyroZ, 2);
    Serial.println(" dps");

    delay(100); // Delay between readings (adjust as needed)
}
