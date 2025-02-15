#include "arduino_secrets.h"
#include "thingProperties.h"
#include <Arduino_LSM6DS3.h>

const int ledPin = 13;

const float shakeThreshold = 2.0;
const int shakeDuration = 2000; 

unsigned long shakeStartTime = 0;

void setup() {
  Serial.begin(9600);
  delay(1500);

  pinMode(ledPin, OUTPUT);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    Serial.print("X: ");
    Serial.print(x);
    Serial.print(" | Y: ");
    Serial.print(y);
    Serial.print(" | Z: ");
    Serial.println(z);


    if (abs(x) > shakeThreshold || abs(y) > shakeThreshold || abs(z) > shakeThreshold) {
      if (shakeStartTime == 0) {
        shakeStartTime = millis(); 
      } else if (millis() - shakeStartTime >= shakeDuration) {
        alarm = true; 
        digitalWrite(ledPin, HIGH); 
      }
    } else {
      shakeStartTime = 0; 
      alarm = false; 
      digitalWrite(ledPin, LOW);
    }
  }

  delay(100);
}

void onAlarmChange() {
 
  if (alarm) {
    Serial.println("ALARM: Shaking detected!");
  } else {
    Serial.println("Alarm reset.");
  }
}



