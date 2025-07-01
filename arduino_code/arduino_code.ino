#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>

// === Pin Definitions ===
#define PH_PIN A0
#define TURBIDITY_PIN A1
#define TDS_PIN A2
#define DHT_PIN 2
#define ONE_WIRE_BUS 3

#define DHTTYPE DHT11
DHT dht(DHT_PIN, DHTTYPE);

// DS18B20 (Water Temp)
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature waterTempSensor(&oneWire);

// GPS on D4 (RX) and D5 (TX)
SoftwareSerial gpsSerial(4, 5); // RX, TX
TinyGPSPlus gps;

// Timing
unsigned long lastReadTime = 0;
const unsigned long readInterval = 3000; // 3 seconds

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
  dht.begin();
  waterTempSensor.begin();

  Serial.println("=== RiverScout Sensor Data Collection ===");
}

void loop() {
  // Continuously feed GPS data
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  // Every 3 seconds, read and print sensor data
  if (millis() - lastReadTime >= readInterval) {
    lastReadTime = millis();

    // === Read DHT Sensor ===
    float temp_air = dht.readTemperature();
    float humidity_air = dht.readHumidity();
    if (isnan(temp_air) || isnan(humidity_air)) {
      Serial.println("⚠️ Failed to read from DHT sensor!");
      temp_air = 0;
      humidity_air = 0;
    }

    // === Read DS18B20 ===
    waterTempSensor.requestTemperatures();
    float temp_water = waterTempSensor.getTempCByIndex(0);

    // === Analog Sensors (Raw Values) ===
    int phRaw = analogRead(PH_PIN);
    int turbidityRaw = analogRead(TURBIDITY_PIN);
    int tdsRaw = analogRead(TDS_PIN);


    float pH = -0.02 * phRaw + 22.3;
    float turbidity = 0.002111832 * turbidityRaw * turbidityRaw - 3.16399 * turbidityRaw + 1159.576;
    float tds = 2.0155 * tdsRaw;

    // === GPS Data ===
    float latitude =  12.923647758185743;
    float longitude = 77.50039711125889 ;
    int satCount = 0;
    float speed = 0;
    float altitude = 0;

    if (gps.location.isValid() && gps.location.isUpdated()) {
      latitude = gps.location.lat();
      longitude = gps.location.lng();
    }

    if (gps.satellites.isValid()) {
      satCount = gps.satellites.value();
    }

    if (gps.speed.isValid()) {
      speed = gps.speed.kmph();
    }

    if (gps.altitude.isValid()) {
      altitude = gps.altitude.meters();
    }

    // === Human-Readable Debug Output ===
    Serial.println("\n📡 RiverScout Sensor Readings:");
    Serial.println("---------------------------------");

    Serial.print("📍 Location   : ");
    Serial.print("Lat: ");
    Serial.print(latitude, 6);
    Serial.print(" | Lon: ");
    Serial.println(longitude, 6);

    Serial.print("🛰️ Satellites : ");
    Serial.println(satCount);

    Serial.print("🚗 Speed      : ");
    Serial.print(speed);
    Serial.println(" km/h");

    Serial.print("🗻 Altitude   : ");
    Serial.print(altitude);
    Serial.println(" m");

    Serial.print("🌡️ Water Temp : ");
    Serial.print(temp_water);
    Serial.println(" °C");

    Serial.print("🌡️ Air Temp   : ");
    Serial.print(temp_air);
    Serial.println(" °C");

    Serial.print("💧 Humidity   : ");
    Serial.print(humidity_air);
    Serial.println(" %");

    Serial.print("🧪 pH Value   : ");
    Serial.println(pH);

    Serial.print("🫧 Turbidity  : ");
    Serial.println(turbidity);

    Serial.print("🌊 TDS Value  : ");
    Serial.println(tds);

    Serial.println("---------------------------------");

    // === Machine-Readable Output to ESP ===
    String dataPacket = "lat=" + String(latitude, 6) +
                        "&lon=" + String(longitude, 6) +
                        "&sat=" + String(satCount) +
                        "&speed=" + String(speed, 2) +
                        "&alt=" + String(altitude, 2) +
                        "&temp_water=" + String(temp_water, 2) +
                        "&temp_air=" + String(temp_air, 2) +
                        "&humidity=" + String(humidity_air, 2) +
                        "&ph=" + String(pH) +
                        "&turbidity=" + String(turbidity) +
                        "&tds=" + String(tds);

    Serial.println(dataPacket);  // ESP reads this line
  }
}
