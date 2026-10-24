#include <Arduino.h>
#include <DFRobot_SCD4X.h>
#include <Wire.h>
#include <math.h>

constexpr uint8_t SDA_PIN = 42;
constexpr uint8_t SCL_PIN = 41;
constexpr uint8_t TCA_ADDRESS = 0x20;
constexpr uint8_t OUTPUT_REGISTER = 0x01;
constexpr uint8_t CONFIG_REGISTER = 0x03;
constexpr uint8_t RELAY1_MASK = 0x01;
constexpr uint8_t RELAY2_MASK = 0x02;
constexpr uint32_t SENSOR_INTERVAL_MS = 5000;
constexpr uint32_t RETRY_INTERVAL_MS = 1000;

DFRobot_SCD4X SCD4X(&Wire, SCD4X_I2C_ADDR);
uint8_t relayOutputs = 0;
uint8_t requestedOutputs = 0;
bool relaysReady = false;
uint32_t lastSensorRead = 0;
uint32_t lastRelayAttempt = 0;

bool writeRegister(uint8_t reg, uint8_t value) {
  Wire.beginTransmission(TCA_ADDRESS);
  Wire.write(reg);
  Wire.write(value);
  return Wire.endTransmission() == 0;
}

bool initializeRelays() {
  // HIGH = EIN. Ausgangswerte vor der Richtung setzen.
  if (!writeRegister(OUTPUT_REGISTER, 0x00)) return false;
  // Acht Relaisausgaenge; unbenutzte Relais 3 bis 8 bleiben AUS.
  if (!writeRegister(CONFIG_REGISTER, 0x00)) return false;
  relayOutputs = 0;
  return true;
}

void updateRelays(uint32_t now) {
  if (relaysReady && requestedOutputs == relayOutputs) return;
  if (now - lastRelayAttempt < RETRY_INTERVAL_MS) return;
  lastRelayAttempt = now;

  if (!relaysReady) {
    relaysReady = initializeRelays();
    if (!relaysReady) {
      Serial.println("TCA9554 nicht erreichbar");
      return;
    }
    Serial.println("Relais initialisiert: beide AUS");
  }
  if (requestedOutputs == relayOutputs) return;
  if (!writeRegister(OUTPUT_REGISTER, requestedOutputs)) {
    Serial.println("TCA9554 Schreibfehler; erneuter Versuch folgt");
    return;
  }

  const uint8_t changed = relayOutputs ^ requestedOutputs;
  relayOutputs = requestedOutputs;
  if (changed & RELAY1_MASK) {
    Serial.println((relayOutputs & RELAY1_MASK) ? "Relais 1 EIN" : "Relais 1 AUS");
  }
  if (changed & RELAY2_MASK) {
    Serial.println((relayOutputs & RELAY2_MASK) ? "Relais 2 EIN" : "Relais 2 AUS");
  }
}

// SCD4x benoetigt zwischen Befehl und Antwort mindestens 1 ms.
// Zusaetzlich Laenge und CRC jedes empfangenen Datenwortes pruefen.
bool readSensorWords(uint16_t command, uint16_t* words, uint8_t count) {
  Wire.beginTransmission(SCD4X_I2C_ADDR);
  Wire.write(static_cast<uint8_t>(command >> 8));
  Wire.write(static_cast<uint8_t>(command));
  const uint8_t error = Wire.endTransmission();
  if (error != 0) {
    Serial.print("SCD41 I2C Schreibfehler: ");
    Serial.println(error);
    return false;
  }
  delay(2);
  const uint8_t expected = count * 3;
  const uint8_t received = Wire.requestFrom(SCD4X_I2C_ADDR, expected);
  if (received != expected) {
    Serial.print("SCD41 Antwort zu kurz: ");
    Serial.print(received);
    Serial.print(" / ");
    Serial.println(expected);
    while (Wire.available()) Wire.read();
    return false;
  }
  for (uint8_t index = 0; index < count; ++index) {
    const uint8_t bytes[2] = {
      static_cast<uint8_t>(Wire.read()), static_cast<uint8_t>(Wire.read())
    };
    const uint8_t receivedCrc = Wire.read();
    uint8_t crc = 0xFF;
    for (uint8_t byte : bytes) {
      crc ^= byte;
      for (uint8_t bit = 0; bit < 8; ++bit) {
        crc = (crc & 0x80) ? (crc << 1) ^ 0x31 : crc << 1;
      }
    }
    if (crc != receivedCrc) {
      Serial.println("SCD41 CRC-Fehler; Messung verworfen");
      while (Wire.available()) Wire.read();
      return false;
    }
    words[index] = (static_cast<uint16_t>(bytes[0]) << 8) | bytes[1];
  }
  return true;
}

void readSensor() {
  uint16_t ready = 0;
  if (!readSensorWords(SCD4X_GET_DATA_READY_STATUS, &ready, 1)) return;
  if ((ready & 0x07FF) == 0) {
    Serial.println("Noch keine Messdaten.");
    return;
  }
  DFRobot_SCD4X::sSensorMeasurement_t data = {};
  uint16_t words[3] = {};
  if (!readSensorWords(SCD4X_READ_MEASUREMENT, words, 3)) return;
  data.CO2ppm = words[0];
  data.temp = -45.0f + 175.0f * words[1] / 65535.0f;
  data.humidity = 100.0f * words[2] / 65535.0f;
  if (!isfinite(data.temp) || data.temp < -45.0f || data.temp > 130.0f ||
      !isfinite(data.humidity) || data.humidity < 0 || data.humidity > 100) {
    Serial.print("Ungueltige Messdaten: CO2=");
    Serial.print(data.CO2ppm);
    Serial.print(" | Temperatur=");
    Serial.print(data.temp);
    Serial.print(" | Feuchte=");
    Serial.println(data.humidity);
    return;
  }

  Serial.print("CO2: ");
  if (data.CO2ppm == 0) {
    Serial.print("ungueltig (0 ppm)");
  } else {
    Serial.print(data.CO2ppm);
    Serial.print(" ppm");
  }
  Serial.print(" | Temperatur: ");
  Serial.print(data.temp, 1);
  Serial.print(" C | Feuchte: ");
  Serial.print(data.humidity, 1);
  Serial.println(" %");

  requestedOutputs = 0;
  if (data.humidity < 30.0f || data.humidity > 50.0f) requestedOutputs |= RELAY1_MASK;
  if (data.temp < 15.0f || data.temp > 23.0f) requestedOutputs |= RELAY2_MASK;
}

void setup() {
  Serial.begin(115200);
  delay(2000);
  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(100000);
  relaysReady = initializeRelays();
  lastRelayAttempt = millis();
  if (!relaysReady) Serial.println("TCA9554 nicht erreichbar");

  while (!SCD4X.begin()) {
    Serial.println("SCD41 nicht erreichbar");
    updateRelays(millis());
    delay(3000);
  }
  Serial.println("SCD41 erkannt!");
  SCD4X.enablePeriodMeasure(SCD4X_STOP_PERIODIC_MEASURE);
  delay(500);
  const uint16_t status = SCD4X.performSelfTest();
  Serial.print("SCD41 Selbsttest: ");
  Serial.print(status);
  Serial.print(" | Hex: 0x");
  Serial.println(status, HEX);
  SCD4X.enablePeriodMeasure(SCD4X_START_PERIODIC_MEASURE);
  Serial.println("Periodische Messung gestartet.");
  lastSensorRead = millis();
}

void loop() {
  const uint32_t now = millis();
  if (now - lastSensorRead >= SENSOR_INTERVAL_MS) {
    lastSensorRead = now;
    readSensor();
  }
  updateRelays(now);
  delay(1);
}
