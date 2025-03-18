#include <WiFiNINA.h>
#include <WiFiSSLClient.h>  
#include <PubSubClient.h>
#include <Arduino_LSM6DS3.h>  

// Wi-Fi credentials
const char* ssid = "Aristotle";
const char* password = "CUPunjab";

// HiveMQ MQTT broker details
const char* mqtt_server = "30de0bc86b6746809e2ddf90ea985a4f.s1.eu.hivemq.cloud";  
const int mqtt_port = 8883;  // TLS-secured port

const char* mqtt_user = "hivemq.webclient.1742277085499";
const char* mqtt_password = "*z32eR?gyOA0Wm%U.H4k";  
const char* topic = "sensor/gyroscope";  

WiFiSSLClient wifiClient;  // ✅ *Using WiFiSSLClient for TLS*
PubSubClient client(wifiClient);

void connectWiFi() {
    Serial.print("Connecting to WiFi...");
    int attempts = 0;
    while (WiFi.begin(ssid, password) != WL_CONNECTED) {
        Serial.print(".");
        delay(3000);
        attempts++;
        if (attempts > 10) {
            Serial.println("\nWiFi Connection Failed! Restarting...");
            NVIC_SystemReset();  // ✅ Restart Arduino Nano 33 IoT
        }
    }
    Serial.println("\nConnected to WiFi!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());  // Show IP for debugging
}

void connectMQTT() {
    client.setServer(mqtt_server, mqtt_port);
    
    while (!client.connected()) {
        Serial.print("Connecting to MQTT... ");

        if (client.connect("Nano33IoT_Client", mqtt_user, mqtt_password)) {
            Serial.println("Connected to MQTT!");
        } else {
            Serial.print("Failed, rc=");
            Serial.print(client.state());
            Serial.println(" Retrying in 5 seconds...");
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    while (!Serial);  // Wait for Serial Monitor to open

    connectWiFi();  // ✅ Connect to WiFi
    connectMQTT();  // ✅ Connect to MQTT

    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1);
    }
    Serial.println("IMU initialized.");
}

void loop() {
    if (!client.connected()) {
        connectMQTT();
    }
    client.loop();  

    float x, y, z;
    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(x, y, z);

        // Format message as JSON
        char payload[100];
        snprintf(payload, sizeof(payload), "{ \"x\": %.2f, \"y\": %.2f, \"z\": %.2f }", x, y, z);

        client.publish(topic, payload);  // ✅ Publish data
        Serial.println("Published: " + String(payload));
    }

    delay(2000);  // Send data every 2 seconds
}
