#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "gopal";
const char* password = "gopal8106";
const String serverUrl = "http://192.168.116.65:5000/upload";


WiFiClient client;  // Create a WiFiClient object

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(client, serverUrl);  // Updated: pass the WiFiClient and URL
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"latitude\":22.5726,\"longitude\":88.3639,"
                      "\"ph\":7.1,\"turbidity\":3.4,\"temperature_water\":24.2,"
                      "\"tds\":300,\"gas\":50,\"temperature_air\":32.1,\"humidity_air\":45}";

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      Serial.print("Response: ");
      Serial.println(http.getString());
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }

  delay(10000); // Wait 10 seconds before sending the next request
}
