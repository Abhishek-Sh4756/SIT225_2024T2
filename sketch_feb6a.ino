const int trigpin = 9;
const int echopin = 10; #Defines the pins connected to the trigger (trigpin) and echo (echopin) pins of the ultrasonic sensor.

int readfrom_ultrasonic()
{
  long duration;
  int distance;

  digitalWrite(trigpin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigpin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigpin, LOW);

  duration = pulseIn(echopin, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}
#Sends a short pulse (trigger signal) from the trigger pin.
Measures the time it takes for the pulse to bounce back to the echo pin (duration) and calculates the distance
void setup()
{

  pinMode(trigpin, OUTPUT);
  pinMode(echopin, INPUT);
  Serial.begin(9600);
}

void loop()
{
  Serial.print("Distance: ");
  Serial.println(readfrom_ultrasonic());
  delay(1000); #Repeatedly measures the distance and prints it to the serial monitor every second
}

