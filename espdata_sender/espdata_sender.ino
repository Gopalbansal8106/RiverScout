#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi
const char* ssid = "gopal";
const char* password = "gopal8106";

// Flask server
const char* server = "http://192.168.73.65:5000/upload"; // Change IP if needed

// Arduino Serial on UART1
#define ARDUINO_RX 16
#define ARDUINO_TX 17
HardwareSerial arduinoSerial(1);

// === Add these for 15-second delay ===
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 8000; // 8 seconds
String latestDataLine = "";

void setup() {
  Serial.begin(115200);
  arduinoSerial.begin(9600, SERIAL_8N1, ARDUINO_RX, ARDUINO_TX);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ Connected to WiFi");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Read and store latest valid data line
  if (arduinoSerial.available()) {
    String line = arduinoSerial.readStringUntil('\n');
    line.trim();
    Serial.print("📥 Received from Arduino: ");
    Serial.println(line);

    if (line.startsWith("lat=")) {
      latestDataLine = line;
    }
  }

  // Send once every 15 seconds if valid data is available
  if (millis() - lastSendTime >= sendInterval && latestDataLine != "") {
    sendToServer(latestDataLine);
    lastSendTime = millis();
  }
}

void sendToServer(String dataLine) {
  StaticJsonDocument<512> doc;

  while (dataLine.length()) {
    int ampIndex = dataLine.indexOf('&');
    String pair = (ampIndex == -1) ? dataLine : dataLine.substring(0, ampIndex);
    int eqIndex = pair.indexOf('=');

    if (eqIndex != -1) {
      String key = pair.substring(0, eqIndex);
      String value = pair.substring(eqIndex + 1);

      // Rename fields
      if (key == "lat") key = "latitude";
      else if (key == "lon") key = "longitude";
      else if (key == "temp_air") key = "temperature_air";
      else if (key == "temp_water") key = "temperature_water";
      else if (key == "humidity") key = "humidity_air";
      else if (key == "sat" || key == "speed" || key == "alt") {
        dataLine = (ampIndex == -1) ? "" : dataLine.substring(ampIndex + 1);
        continue; // Skip these
      }

      if (key == "latitude" || key == "longitude" || key == "ph" || key == "turbidity" ||
          key == "temperature_water" || key == "tds" || key == "temperature_air" || key == "humidity_air") {
        doc[key] = value.toFloat();
      }
    }

    if (ampIndex == -1) break;
    dataLine = dataLine.substring(ampIndex + 1);
  }

  String jsonData;
  serializeJson(doc, jsonData);
  Serial.println("➡️ Sending JSON:");
  Serial.println(jsonData);

  WiFiClient client;
  HTTPClient http;
  http.begin(client, server);
  http.addHeader("Content-Type", "application/json");

  int code = http.POST(jsonData);
  if (code > 0) {
    Serial.print("✅ Response Code: ");
    Serial.println(code);
    Serial.println("📥 Server: " + http.getString());
  } else {
    Serial.print("❌ POST failed: ");
    Serial.println(http.errorToString(code));
  }

  http.end();
}
