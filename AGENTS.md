# AGENTS.md — Formaldehyd-Sensor / Waveshare ESP32-S3

## Zweck dieser Datei

Diese Datei ist der verbindliche Projektkontext für neue Coding-Agents. Bitte zuerst den bestehenden Code und `platformio.ini` prüfen und **funktionierende Teile weiterverwenden**, statt das Projekt unnötig neu aufzubauen.

Ziel ist ein robuster Formaldehyd-Sensor-Prototyp auf Basis des **Waveshare ESP32-S3-ETH-8DI-8RO**. Der Code soll bereits jetzt die Hardware-Funktionen des Boards vollständig vorbereiten: **RS485/Modbus RTU, 8 digitale Eingänge, 8 Relais, Ethernet/Host, USB-C-Service und I²C-Sensorik**.

---

# 1. Aktueller Hardwarestand

## Controller

Waveshare **ESP32-S3-ETH-8DI-8RO**

Wichtige Hardware-Schnittstellen:

- 24-V-DC-Versorgung über den 2-poligen Power-Anschluss
- RS485 über separaten 3-poligen Anschluss: A / B / GND
- 8 digitale Eingänge
- 8 Relaisausgänge
- Ethernet / RJ45
- USB-C für Programmierung und Service
- I²C für Sensorik
- Wi-Fi / Bluetooth sind vorhanden, aber aktuell nicht Kern der Installation

Die 10-polige DI-Klemmeneinheit ist physisch:

1. COM
2. DGND
3. DI1
4. DI2
5. DI3
6. DI4
7. DI5
8. DI6
9. DI7
10. DI8

Diese 10 Klemmen gehören als **eine Einheit** zusammen.

## I²C

Bisher verwendete Pins am ESP32-S3:

- SDA = GPIO42
- SCL = GPIO41

Falls im bestehenden Projekt bereits eine funktionierende Pinbelegung vorhanden ist, hat diese Vorrang.

## Relais

Das Board besitzt 8 Relais.

Bereits getestete Grundfunktion:
- Relais lassen sich aus dem ESP32-Code schalten.
- Die Relais werden auf dem Waveshare-Board über den vorhandenen I/O-Expander angesteuert.
- Bestehenden funktionierenden Relaistreiber nicht ohne Grund ersetzen.

Vorgesehene Standardbelegung:

- Relay 1 = Alarm
- Relay 2 = Störung
- Relay 3 = Bereit / Betrieb
- Relay 4–8 = Reserve / spätere Funktionen / Test

Die Software soll trotzdem **alle 8 Relais vollständig unterstützen**.

---

# 2. Warum CO₂ aktuell NICHT verwendet wird

Der CO₂-Sensor war nur ein **Testaufbau**, nicht der eigentliche Projektsensor.

Verwendet wurde ein Sensirion/DFRobot **SCD41** als temporärer I²C-Test.

Beim ersten Aufbau wurde der Sensor versehentlich falsch versorgt bzw. falsch angeschlossen. Danach zeigte sich folgendes Verhalten:

- I²C-Adresse `0x62` wurde weiterhin erkannt.
- Temperatur und relative Feuchte konnten gelesen werden.
- CO₂ blieb jedoch bei `0 ppm`.
- Der SCD41-Selbsttest lieferte einen Fehlerwert (`0x44` / dezimal 68).
- Der I²C-Bus selbst wurde anschließend mit einem anderen Temperatur-/Feuchtesensor erfolgreich geprüft.

Daraus folgt:

**Der CO₂-Messwert ist nicht vertrauenswürdig und wird im Projekt nicht weiter verwendet.**

Wichtig für den neuen Agent:

- Keine Zeit in die Reparatur der CO₂-Funktion investieren.
- Keine CO₂-Alarmierung implementieren.
- CO₂ nicht als gültigen Prozesswert über Modbus veröffentlichen.
- Keine Logik von einem CO₂-Wert abhängig machen.
- Falls alter CO₂-Code im Repository vorhanden ist, deaktivieren oder sauber kapseln.
- Keine `0 ppm` als realen CO₂-Wert anzeigen.
- CO₂ ist **kein Bestandteil der finalen Formaldehyd-Anwendung**.

---

# 3. Aktueller Testbetrieb

Der endgültige Formaldehydsensor ist der **Sensirion SFA40**.

Bis die komplette HCHO-Funktion getestet wird, verwenden wir einen funktionierenden **I²C-Temperatur-/Feuchtesensor** als Testsignal.

Aktuell werden daher nur verwendet:

- Temperatur
- relative Feuchte

Diese Werte dienen **nicht als finale Prozessgröße**, sondern ausschließlich dazu, die komplette Steuerungslogik zu testen:

- Sensor lesen
- Grenzwertlogik
- Alarm setzen/zurücksetzen
- Störung erzeugen
- Bereit-Signal
- Relais schalten
- digitale Eingänge prüfen
- Modbus-Werte übertragen
- Host/Weboberfläche testen
- Diagnose und Logging prüfen

Es muss im Code klar zwischen folgenden Betriebsarten unterschieden werden:

```text
TEST_MODE
    Temperatur / Feuchte als Testsignal

HCHO_MODE
    SFA40 Formaldehydmessung als reale Prozessgröße
```

Der Testmodus darf die spätere HCHO-Implementierung nicht verbauen.

---

# 4. Finales Ziel mit SFA40

Der SFA40 ist der eigentliche Formaldehydsensor.

Projektziel:

- kontinuierliche HCHO-Messung
- Alarmgrenze: 300 ppb
- Rohwert behalten
- korrigierten Messwert berechnen
- Alarm auf Basis des korrigierten HCHO-Werts
- Übergabe an GLS / Leitsystem über RS485 Modbus RTU
- zusätzliche potentialfreie Relaiskontakte

Spätere 2-Punkt-Kalibrierung:

- ZERO = 0 ppb
- SPAN = 300 ppb

Die interne Sensirion-Werkskalibrierung soll **nicht überschrieben** werden.

Die Kalibrierung wird als Korrekturschicht im ESP32 gespeichert.

Benötigte Daten:

- raw HCHO
- corrected HCHO
- Zero-Referenz
- gemessener Raw-Wert bei Zero
- Span-Referenz = 300 ppb
- gemessener Raw-Wert bei Span
- Calibration active
- optional Datum / Zeit der letzten Kalibrierung

Persistente Speicherung bevorzugt über `Preferences` / NVS.

---

# 5. Digitale Eingänge DI1–DI8

Alle 8 digitalen Eingänge sollen im Code vorhanden sein.

Vorgesehene Nutzung:

- DI1 = ZERO-Service-Taster
- DI2 = SPAN-Service-Taster
- DI3–DI8 = frei / Reserve / zukünftige externe Meldungen

Für jeden Eingang:

- Zustand lesen
- entprellen
- Status im Host anzeigen
- Status über Modbus verfügbar machen
- optional Ereignis im Log erzeugen

ZERO und SPAN dürfen nicht durch einen kurzen versehentlichen Tastendruck ausgelöst werden.

Empfehlung:

- langer Tastendruck, z. B. 5 Sekunden
- nur im Service-/Kalibriermodus
- visuelle/serielle Bestätigung vor Speicherung

---

# 6. Relais 1–8

Der Code soll alle acht Relais zentral verwalten.

Mindestens:

```text
R1 = Alarm
R2 = Störung
R3 = Bereit
R4 = Reserve
R5 = Reserve
R6 = Reserve
R7 = Reserve
R8 = Reserve
```

Wichtig:

- Relais nicht an mehreren Stellen im Programm direkt schalten.
- Eine zentrale `RelayManager`-/Board-I/O-Schicht verwenden.
- Automatische Prozesslogik und manueller Servicetest sauber trennen.
- Manueller Relaistest nur im Servicebetrieb.
- Relaiszustände über Host und Modbus sichtbar machen.

Spätere Failsafe-Logik soll ohne großen Umbau möglich sein.

---

# 7. Alarm- und Statuslogik

Zentrale Zustände vorsehen:

```text
READY
ALARM
FAULT
SERVICE
CALIBRATION
TEST_MODE
```

## Im aktuellen Testmodus

Temperatur und/oder Feuchte dürfen als künstliche Grenzwertquelle verwendet werden.

Die Schwellwerte müssen konfigurierbar sein.

Beispiel:

```text
Testwert überschreitet Testgrenze
    -> Alarm = EIN
    -> Relay 1 = EIN

Sensorfehler / I2C-Timeout
    -> Fault = EIN
    -> Relay 2 = EIN

System initialisiert und Sensor gültig
    -> Ready = EIN
    -> Relay 3 = EIN
```

Die Temperatur-/Feuchte-Grenze ist ausschließlich ein Funktionstest.

## Im späteren HCHO-Betrieb

```text
corrected_HCHO >= 300 ppb
    -> Alarm

Sensor nicht erreichbar / ungültige Daten / interner Fehler
    -> Störung

System vollständig betriebsbereit
    -> Bereit
```

Alarmhysterese und Rücksetzstrategie sollen konfigurierbar vorbereitet werden.

---

# 8. RS485 / Modbus RTU

RS485 muss als vollwertige Schnittstelle in die Software integriert werden.

Ziel:

```text
ESP32
 -> UART
 -> onboard RS485
 -> A / B / GND
 -> GLS / BMS / Leitsystem
```

Initiale Modbus-Einstellungen, sofern im bestehenden Projekt nichts anderes definiert ist:

- Modbus RTU Slave
- Slave ID: 1
- Baudrate: 9600
- 8 Datenbits
- keine Parität
- 1 Stopbit

Die bestehenden bzw. offiziellen Waveshare-Pins sind zu verwenden.  
Keine GPIOs raten. Vor Änderungen vorhandenen Code und Waveshare-Dokumentation prüfen.

## Empfohlene Registerstruktur

Wenn noch keine Registermap verbindlich existiert, eine zentrale Registermap anlegen.

Beispiel:

```text
40001  System Status
40002  Operating Mode
40003  Fault Code

40010  Temperature x100
40011  Relative Humidity x100

40020  HCHO Raw ppb
40021  HCHO Corrected ppb
40022  HCHO Alarm Threshold ppb

40030  DI bitmask DI1..DI8
40031  Relay bitmask R1..R8

40040  Alarm state
40041  Fault state
40042  Ready state

40050  Calibration active
40051  Zero raw
40052  Span raw
40053  Span reference ppb
```

Solange der SFA40 noch nicht aktiv ist:

- HCHO-Register als `not available` / definierter ungültiger Wert behandeln
- nicht so tun, als wäre 0 ppb eine reale Messung
- Temperatur und Feuchte über ihre eigenen Register übertragen

Registeradressen an einer zentralen Stelle definieren und dokumentieren.

---

# 9. Ethernet / Host

Das Potential des Boards soll genutzt werden.

Ethernet / RJ45 soll als **Host-/Service-Schnittstelle** vorbereitet werden.

Ziel für die lokale Weboberfläche:

## Live-Anzeige

- Temperatur
- relative Feuchte
- später HCHO raw
- später HCHO corrected
- Alarm
- Störung
- Bereit
- TEST_MODE / HCHO_MODE
- DI1–DI8
- Relay 1–8
- RS485 Status
- Uptime
- letzter Sensorfehler

## Servicefunktionen

- Relaistest R1–R8
- Anzeige der DI-Zustände
- TEST_MODE ein/aus
- konfigurierbare Testgrenzen
- später ZERO
- später SPAN 300 ppb
- später Calibration Reset
- Diagnose / Status

Serviceaktionen dürfen normale Automatikfunktionen nicht unkontrolliert überschreiben.

Host-Ausfall darf die Sensor-/Alarmfunktion nicht blockieren.

Die Hauptsteuerung muss auch ohne Netzwerk weiterlaufen.

---

# 10. USB-C

USB-C bleibt für:

- Programmierung
- Firmware Update
- Serial Monitor
- Debugging / Service

Monitor:

```text
115200 Baud
```

Serielle Logs sollen strukturiert sein, z. B.:

```text
[SYS]
[SENSOR]
[DI]
[RELAY]
[ALARM]
[MODBUS]
[HOST]
[CAL]
[FAULT]
```

Keine unkontrollierte Log-Flut im normalen Betrieb.

---

# 11. Softwarearchitektur

`main.cpp` möglichst klein halten.

Empfohlene Trennung:

```text
BoardIO
    DI1-DI8
    Relay1-Relay8

SensorManager
    aktueller Temp/RH-Testsensor
    später SFA40

AlarmManager
    Alarm
    Fault
    Ready
    Hysterese

CalibrationManager
    Zero
    Span
    Korrektur
    NVS

ModbusRtuServer
    RS485
    Registermap

HostServer
    Ethernet
    Web UI / API

ConfigStore
    Preferences / NVS

Diagnostics
    Fehlercodes
    Status
    Logging
```

Keine blockierenden langen `delay()`-Abläufe in der Hauptlogik.

Bevorzugt:

- `millis()`-basierte Tasks
- klar definierte Update-Intervalle
- Sensorfehler dürfen Modbus/Host/Relaislogik nicht komplett einfrieren

---

# 12. Plattform / Build

Aktueller Entwicklungsweg:

- VS Code
- PlatformIO
- Arduino Framework
- ESP32-S3
- Serial 115200

Bisher verwendetes Environment:

```ini
[env:esp32-s3-devkitc-1]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
monitor_speed = 115200
```

USB-CDC wurde bereits verwendet:

```ini
build_flags =
    -DARDUINO_USB_MODE=1
    -DARDUINO_USB_CDC_ON_BOOT=1
```

Das reale Waveshare-Modul verwendet einen ESP32-S3-WROOM-1U-N16R8.

Bestehendes funktionierendes `platformio.ini` nicht unnötig ersetzen.

Nicht auf ESP-IDF wechseln, solange dies nicht ausdrücklich verlangt wird.

---

# 13. Wichtige Entwicklungsregel

Vor jeder größeren Änderung:

1. bestehenden Code lesen
2. bereits funktionierende Teile identifizieren
3. funktionierenden I²C-Test nicht zerstören
4. funktionierenden Relaistest nicht zerstören
5. Änderungen modular durchführen
6. kompilieren
7. seriellen Start testen
8. anschließend Schnittstellen einzeln testen

Nicht alles gleichzeitig neu schreiben.

---

# 14. Gewünschte nächste Entwicklungsphase

Der nächste Agent soll den bestehenden Stand analysieren und dann schrittweise folgende Basis herstellen:

1. funktionierenden Temp/RH-Sensor weiterverwenden
2. CO₂ vollständig ignorieren
3. `TEST_MODE` einführen
4. zentrale Alarm-/Fault-/Ready-Logik implementieren
5. alle 8 DI einlesen
6. ZERO auf DI1 vorbereiten
7. SPAN auf DI2 vorbereiten
8. alle 8 Relais integrieren
9. R1 Alarm, R2 Störung, R3 Bereit
10. RS485 Modbus RTU Slave integrieren
11. zentrale Modbus-Registermap anlegen
12. Ethernet Host/Webstatus integrieren
13. USB-C Serial/Service beibehalten
14. Architektur so vorbereiten, dass später der SFA40 nur noch als reale HCHO-Sensorquelle eingesetzt wird

---

# 15. Akzeptanzkriterien für den aktuellen Prototyp

Der aktuelle Teststand gilt als erfolgreich, wenn:

- Firmware sauber startet
- Temp/RH werden stabil gelesen
- CO₂ spielt nirgends eine Rolle
- DI1–DI8 werden korrekt erkannt
- Relay1–Relay8 können softwareseitig angesprochen werden
- Alarm-Test schaltet Relay 1
- Fault-Test schaltet Relay 2
- Ready schaltet Relay 3
- Modbus Master kann Statuswerte lesen
- DI-Bitmaske kann per Modbus gelesen werden
- Relay-Bitmaske kann per Modbus gelesen werden
- Ethernet Host zeigt Live-Zustände
- USB-C Serial Monitor funktioniert weiterhin
- Netzwerk- oder Modbusfehler stoppen die lokale Alarmfunktion nicht
- Code ist für den späteren SFA40 vorbereitet

---

# 16. Nicht tun

- CO₂ reparieren oder in die Prozesslogik zurückbringen
- 0 ppm CO₂ als gültigen Messwert ausgeben
- SFA40-Kalibrierung in den Sensor selbst schreiben
- GPIOs oder Anschlussbelegungen raten
- funktionierende Relais-/I²C-Funktionen ohne Not ersetzen
- Produktions-HCHO-Logik mit Test-Temperatur-/Feuchte-Logik vermischen
- Netzwerk als Voraussetzung für die lokale Alarmfunktion machen
- große blockierende Delay-Schleifen einbauen
- Relais direkt aus vielen verschiedenen Modulen schalten

---

# Arbeitsauftrag an den neuen Agent

Bitte analysiere zuerst das vorhandene Repository und berichte kurz:

1. Welche der oben genannten Funktionen existieren bereits?
2. Welche Pin-/Boarddefinitionen werden aktuell verwendet?
3. Welche Sensorbibliothek ist aktuell für Temperatur/Feuchte aktiv?
4. Wie werden die Relais aktuell angesteuert?
5. Gibt es bereits RS485-, Ethernet- oder Web-Code?
6. Welche Änderungen sind für die oben beschriebene Zielarchitektur notwendig?

Danach einen **schrittweisen Implementierungsplan** erstellen.

Erst nach dieser Bestandsaufnahme Code ändern.

Priorität:

```text
Stabilität
> korrekte Hardwarebelegung
> modulare Architektur
> Testbarkeit
> zusätzliche Features
```
