#include "DHT.h"

#define DHTPIN 2      // Digital pin connected to DHT
#define DHTTYPE DHT22 

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("DHT22 Temperature and Humidity Data Logger");
  dht.begin();
}

void loop() {
  delay(2000);  
  
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();  
  
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  
  // Print CSV format
  Serial.print(millis() / 1000);  // Time in seconds
  Serial.print(",");
  Serial.print(temperature);
  Serial.print(",");
  Serial.println(humidity);
  
  // Human-readable format
  Serial.print("Temp: ");
  Serial.print(temperature);
  Serial.print("°C\tHumidity: ");
  Serial.print(humidity);
  Serial.println("%");
}