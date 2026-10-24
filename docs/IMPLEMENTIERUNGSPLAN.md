# Projektauftrag und Bestandsaufnahme

Basis: bereitgestellte AGENTS.md, umgesetzt auf dem vorhandenen lokalen ESP_Klima-Projekt.
Ein anderes Repository und ein anderer Testsensor wurden bislang nicht angegeben.

## Vorhanden

- PlatformIO espressif32 7.1.3, Arduino, ESP32-S3 DevKitC als Builddefinition, 16 MB Flash.
- USB CDC, COM6, 115200 Baud; Build, Upload und Empfang am realen Board erfolgreich.
- I2C auf SDA42/SCL41, 100 kHz. SCD41 Temp/RH mit Antwortlaenge, CRC und Befehlswartezeit.
- DFRobot_SCD4X 1.0.1 fuer bisherige Startbefehle; Messwerte zuletzt direkt ueber Wire gelesen.
- TCA9554 0x20, Output 0x01, Konfiguration 0x03, HIGH=EIN; Schreiben mit Wiederholung.
- Bislang zwei Grenzwertrelais. Keine DI-, Modbus-, Ethernet-, Kalibrier- oder Servicearchitektur.
- CO2-Sensorteil laut Projektkontext beschaedigt; keine weitere CO2-Diagnose oder Prozessnutzung.

## Auftrag

Den vorhandenen Treiber modular weiterverwenden. TEST_MODE mit Temp/RH entwickeln;
HCHO_MODE und externe Zweipunktkorrektur fuer den spaeteren SFA40 vorbereiten.
R1=Alarm, R2=Stoerung, R3=Bereit. Alle acht Relais und DI zentral verwalten.
RS485 soll ein lesbares Modbus-RTU-Slave-Registerabbild bereitstellen.
Ethernet soll lokalen Status und abgesicherten Servicebetrieb bereitstellen.
Netzwerkausfall darf die lokale Steuerung nicht blockieren. Ungueltige Messwerte bleiben
als ungueltig gekennzeichnet. Keine produktive HCHO-Freigabe ohne realen Sensortest.

## Reihenfolge

1. Sensorzustandsautomat, BoardIO, Alarm/Fault/Ready, Konfiguration, USB-Service;
   reine Logik-Selbsttests, kompilieren, seriellen Start pruefen.
2. Acht entprellte DI, Langdruck-Ereignisse DI1/2, Modbus RTU mit zentraler Registermap;
   Protokolltests und Build. Physischer RS485-Mastertest separat dokumentieren.
3. Ethernet W5500 in eigener Task, Webstatus und kontrollierte Servicekommandos;
   NVS-Kalibrierungsschicht und HCHO-Erweiterungspunkt. Build und Hardwarestart.
4. Verifikation und verbleibende physische Abnahmeschritte dokumentieren.

## Verifizierte Boardbelegung

Quelle: https://www.waveshare.com/wiki/ESP32-S3-ETH-8DI-8RO

- DI1..8: GPIO4..11. Aktiv LOW / INPUT_PULLUP auch in der ESPHome-Referenzimplementierung:
  https://github.com/esphome/devices.esphome.io/blob/main/src/docs/devices/Waveshare-ESP32-S3-ETH-8DI-8RO/index.md
- RS485: TX17/RX18, Hardware-Richtungsumschaltung laut Waveshare-Produktbeschreibung.
- W5500: INT12, MOSI13, MISO14, SCLK15, CS16.
- SDA42/SCL41 aus dem bereits funktionierenden Aufbau.

RS485-Kommunikation wurde am 24.10.2026 mit dem USB-Master COM9 erfolgreich geprueft.
Physische DI-Polaritaet und alle Relaiskontakte sind noch einzeln zu pruefen.
Softwarezustaende ersetzen diese Tests nicht; siehe PRUEFPROTOKOLL.md.
