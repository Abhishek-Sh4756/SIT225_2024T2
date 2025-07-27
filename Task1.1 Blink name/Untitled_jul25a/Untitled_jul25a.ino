#include "arduino_secrets.h"
#include "thingProperties.h"

const int ledPin = LED_BUILTIN;

void setup() {
  pinMode(ledPin, OUTPUT);

  Serial.begin(9600);

  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();

  blinkMorse("ABHISHEK");
  delay(5000); 
}

void onLedStateChange() {
  if (ledState == true) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }
}

void blinkMorse(String name) {
  for (int i = 0; i < name.length(); i++) {
    char letter = toupper(name.charAt(i));
    Serial.print("Blinking letter: ");
    Serial.println(letter);
    blinkLetter(letter);
    delay(1000); // Space between letters
  }
}


void blinkDot() {
  digitalWrite(ledPin, HIGH);
  delay(250);
  digitalWrite(ledPin, LOW);
  delay(250);
}

// Dash = long blink
void blinkDash() {
  digitalWrite(ledPin, HIGH);
  delay(750);
  digitalWrite(ledPin, LOW);
  delay(250);
}

void blinkLetter(char letter) {
  switch (letter) {
    case 'A': blinkDot(); blinkDash(); break;
    case 'B': blinkDash(); blinkDot(); blinkDot(); blinkDot(); break;
    case 'H': blinkDot(); blinkDot(); blinkDot(); blinkDot(); break;
    case 'I': blinkDot(); blinkDot(); break;
    case 'S': blinkDot(); blinkDot(); blinkDot(); break;
    case 'E': blinkDot(); break;
    case 'K': blinkDash(); blinkDot(); blinkDash(); break;
    default: break; 
  }
}
