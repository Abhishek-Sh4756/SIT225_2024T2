#include <Arduino.h>

int ledPin = LED_BUILTIN; 

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 
  pinMode(ledPin, OUTPUT); // Set the LED pin as output to control the blinking of LED
}

void loop() {
  if (Serial.available() > 0) {
    int numBlinks = Serial.parseInt(); // Read the number sent by the Python script
    for (int i = 0; i < numBlinks; i++) {
      digitalWrite(ledPin, HIGH); // Turn LED on
      delay(1000); // Wait for a second
      digitalWrite(ledPin, LOW); // Turn LED off
      delay(1000); 
    }
    int randomNum = random(1, 10); // Generate a random number between 1 and 10
    Serial.println(randomNum); // Send the random number back to the Python script
  }
}

