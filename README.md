# ESP_Klima – Waveshare Formaldehyd-Prototyp

PlatformIO-Projekt für **ESP32-S3-ETH-8DI-8RO**, Arduino Framework.
Der aktive Programmeinstieg ist **`src/main.cpp`**. Den Ordner mit `platformio.ini`
als Projekt öffnen. `legacy/ESP_Klima.ino` ist ausschließlich der gesicherte alte Stand.

Die [Bedienungsanleitung](docs/BEDIENUNGSANLEITUNG.md) beschreibt Anschluss,
Web-Service, Grenzwerte, Relaistest und Wiederherstellung der Geräteeinstellungen.

## Aktueller Stand

TEST_MODE liest alle fünf Sekunden Temperatur und Feuchte des vorhandenen SCD41.
CO₂ wird nicht als Messwert verwendet. Modbus RTU und USB wurden am angeschlossenen
Board geprüft. Ethernet bietet Modbus TCP auf Port 502 und HTTP auf Port 80;
den jeweils nachgewiesenen Teststand enthält das Prüfprotokoll.
Der SFA40-Treiber ist noch nicht integriert. HCHO_MODE meldet deshalb ausdrücklich
eine Störung; HCHO bleibt ungültig. Diese Firmware ist der Testprototyp aus AGENTS.md.

## Kompilieren, Upload und Monitor

PowerShell im Projektordner:

```powershell
& "$env:USERPROFILE\.platformio\penv\Scripts\platformio.exe" run
& "$env:USERPROFILE\.platformio\penv\Scripts\platformio.exe" run --target upload
& "$env:USERPROFILE\.platformio\penv\Scripts\platformio.exe" device monitor
```

ESP: COM6, USB-Monitor 115200 Baud. Monitor mit **Strg+C** vor dem Upload schließen.
USB-RS485-Master: derzeit COM9, **Slave 1 / 9600 Baud / 8N1**.
COM-Nummern können sich nach Umstecken ändern; `platformio.ini` entsprechend anpassen.
Die Flash-Konfiguration beträgt 16 MB. PSRAM ist vorhanden, wird derzeit nicht benötigt.

## Automatik und Relais

| Funktion | Verhalten |
|---|---|
| R1 Alarm | Temperatur oder Feuchte außerhalb der gespeicherten Grenzwerte |
| R2 Störung | Sensor ungültig/veraltet, Relaistreiber-/NVS-Fehler oder HCHO fehlt im HCHO_MODE |
| R3 Bereit | Kein Fehler und Service geschlossen; kann gleichzeitig mit Alarm aktiv sein |
| R4–R8 | In Automatik AUS; einzeln im Service schaltbar |

Alarm setzt bei Überschreitung bzw. Unterschreitung. In der Standardkonfiguration
liegen die Rückschaltgrenzen 0,3 °C bzw. 2 Prozentpunkte innerhalb des erlaubten Bereichs. Beispiel: oberer
Temperaturalarm bei >23 °C, Rücksetzung bei ≤22,7 °C. Fehlerhafte oder über 15 s alte
Werte führen zur Störung. Ohne Alarmspeicherung wird der Messwertalarm dabei gelöscht.
Die Relaismaske ist der zuletzt erfolgreich geschriebene Expanderzustand; das Board
liefert keine Rückmeldung über die tatsächlichen mechanischen Kontakte.

### Standardwerte und gespeicherte Geräteeinstellungen

| Einstellung | Standard im Code | Zuletzt am ESP ausgelesen, 24.10.2026 |
|---|---|---|
| Temperatur min / max | 15 / 23 °C | 15 / 23 °C |
| Feuchte min / max | 30 / 50 % rF | 25 / 40 % rF |
| Temperaturhysterese | 0,3 °C | 0,3 °C |
| Feuchtehysterese | 2 Prozentpunkte | 1,5 Prozentpunkte |
| Alarm speichern | AUS | EIN |

Gespeicherte NVS-Werte haben Vorrang vor den Standardwerten. Ein normales
Firmware-Update behält NVS bei; ein neues oder vollständig gelöschtes Board beginnt
mit den Standardwerten. Das Repository enthält die dokumentierten Einstellungen,
keinen NVS-Speicherabzug. Aktuelle Werte liefert `GET /api/status`.

Alle DI werden mit 30 ms Entprellzeit gelesen, logisch aktiv bei LOW am ESP-Eingang.
DI1/DI2 erzeugen nach fünf Sekunden Halten eine ZERO-/SPAN-Anforderung. Dafür sind
Service, HCHO_MODE und ein gültiger HCHO-Sensor erforderlich. Ein kurzer Druck
speichert nichts. DI3–DI8 werden angezeigt und über Modbus übertragen.

## USB-Service

Zeilen mit Enter abschließen. Dezimalzahlen mit **Punkt** eingeben.

| Befehl | Wirkung |
|---|---|
| `status` | System, Messwerte, Netzwerk und Modbus-Zähler |
| `selftest` | Reine Logik-/Protokollprüfung, ohne Relais oder NVS zu verändern |
| `registers` | Aktuelles Registerabbild |
| `help` | Befehlsübersicht |
| `ack` | Gespeicherten Alarm quittieren, wenn Ursache und Störung beseitigt sind |
| `service on` | Service für 15 Minuten öffnen; Schlüssel für Webservice ausgeben |
| `service off` | Service beenden und automatische Relaissteuerung wiederherstellen |
| `relay 1 on` / `relay 1 off` | Im Service Relais 1 schalten; Nummern 1–8 möglich |
| `limits 15 23 30 50` | Im Service Tmin, Tmax, RHmin, RHmax dauerhaft speichern |
| `hysteresis 0.3 2` | Im Service Temperatur-/Feuchtehysterese dauerhaft speichern |
| `latch on` / `latch off` | Im Service Alarmspeicherung konfigurieren |
| `mode test` / `mode hcho` | Im Service Betriebsart wechseln; Neustart beginnt im TEST_MODE |
| `cal zero` / `cal span` / `cal reset` | Kalibrieraktion vormerken; derzeit ohne HCHO-Sensor abgelehnt |
| `cal confirm` | Innerhalb 30 s bestätigen, bei weiterhin gültigem HCHO-Sensor |

**Service übernimmt alle acht Relais manuell und startet mit allen Relais AUS.**
Prozesszustände werden weiter berechnet, steuern die Ausgänge währenddessen aber
nicht. Nach 15 Minuten oder `service off` gilt wieder Automatik. Bei angeschlossenen
Verbrauchern diesen Wechsel vor dem Relaistest berücksichtigen.

## Ethernet und Weboberfläche

Für die direkte Verbindung zu diesem Laptop wird folgende Konfiguration verwendet:

| Teilnehmer | IPv4 | Netzmaske | Gateway |
|---|---|---|---|
| Laptop, USB-LAN „Ethernet 3“ | 192.168.77.1 | 255.255.255.0 | keines |
| Waveshare ESP | 192.168.77.2 | 255.255.255.0 | keines |

Browser: **http://192.168.77.2/**. Modbus-Client: TCP, **192.168.77.2:502**,
Unit-ID **1**, FC03 oder FC04. Register und Skalierung stehen in
[MODBUS.md](docs/MODBUS.md). Beispiel: Offset 9, zwei Register lesen → Temperatur
und Feuchte, jeweils durch 100 teilen. RS485 bleibt parallel verfügbar.

Die ESP-Netzkonfiguration wird ausschließlich über USB geändert und in NVS gespeichert:

```text
network static 192.168.77.2 255.255.255.0 0.0.0.0
network dhcp
```

Diese Befehle benötigen keinen Relais-Service und ändern keine Ausgangsanforderung.
Die Netzwerkverbindungen werden dabei neu aufgebaut. Die erste Zeile richtet den
Direktbetrieb ein; die zweite aktiviert DHCP für einen Routeranschluss. Nach einem
Neustart gilt die gespeicherte Auswahl. Werkseinstellung ohne gespeicherten Eintrag
ist DHCP. Eine empfangene IP erscheint bei `status` und im HOST-Log.

Das Skript `tools/ConfigureDirectEthernet.ps1` richtet ausschließlich den zuvor
identifizierten USB-LAN-Adapter dieses Laptops ein. Administratorrechte sind erforderlich.
`-Mode Dhcp` entfernt die Testadresse und stellt diesen Adapter wieder auf DHCP.
WLAN wird nicht geändert. Vor Verwendung an einem anderen Laptop muss die geprüfte
Adapter-ID im Skript angepasst werden. Es richtet keinen Internetzugang über den ESP ein.

Die Seite zeigt Messwerte, Betriebszustände, alle DI/Relais und Modbus-Zähler.
`GET /api/status` liefert dieselben Werte als JSON, ungültige Messwerte als `null`.
Für Änderungen zuerst per USB `service on` senden und den ausgegebenen Schlüssel
in der Webseite eintragen und **Senden** drücken. Erst nach Bestätigung durch den ESP
verschwinden Eingabefeld und Senden-Button; ein gelbes **Service**-Feld in Buttongröße
zeigt die Freigabe an. Dann sind die Serviceaktionen bedienbar. Die Restzeit steht
daneben. Bei falschem Schlüssel bleibt die Eingabe sichtbar. Nach Ablauf oder
`service off` erscheint sie wieder. Die Schlüsselprüfung schaltet keine Relais.
Webbefehle können den Service nicht öffnen oder verlängern.
Der Schlüssel gilt nur für die jeweilige Servicephase. Die lokale HTTP-Schnittstelle
hat kein TLS. Der Schlüssel wird nicht über die Status-API ausgegeben.

Ethernet läuft in einer eigenen FreeRTOS-Task. DHCP, fehlendes LAN und langsame
HTTP-Clients blockieren die lokale Sensor-/Relaislogik nicht.

## HCHO-Erweiterung und Kalibrierung

`SensorManager` liefert den zentralen `Sample`. Für den SFA40 sind noch der echte
Treiber, Fehlerbehandlung und die Hardwareprüfung zu ergänzen. Er muss `rawHcho`,
`hchoValid`, Gültigkeit und Messzeit liefern. Vor Alarm, Registerabbild und Webstatus
ist `correctHcho(rawHcho, calibration.data)` auf den HCHO-Wert anzuwenden.
Die vorbereitete HCHO-Alarmgrenze beträgt 300 ppb, die Rückschalthysterese 10 ppb.
Diese beiden Werte liegen in `Settings`; es gibt noch keinen USB-Befehl dafür.

Externe Zweipunktkorrektur:

```text
corrected_ppb = 300 × (raw_ppb − zeroRaw) / (spanRaw − zeroRaw)
```

ZERO speichert den Rohwert unter 0-ppb-Referenz und deaktiviert die bisherige
Korrektur. SPAN unter 300-ppb-Referenz aktiviert sie, wenn die Rohwertdifferenz
größer als 1 ppb ist. Die Vorgabe wird beim Anfordern erfasst; die Bestätigung
speichert genau diesen Vorschlag. Referenzgas und Stabilität müssen extern
sichergestellt werden. NVS speichert nur die ESP-Korrekturdaten. Die
Sensirion-Werkskalibrierung wird nicht beschrieben.

## Dateien und Nachweise

- [Bestandsaufnahme und Implementierungsplan](docs/IMPLEMENTIERUNGSPLAN.md)
- [Bedienungsanleitung und Geräteeinstellungen](docs/BEDIENUNGSANLEITUNG.md)
- [Modbus-Registermap](docs/MODBUS.md)
- [Prüfprotokoll und offene Hardwaretests](docs/PRUEFPROTOKOLL.md)
- [Maschinenlesbares Modbus-Prüfergebnis](docs/modbus-test.json)
- [Ethernet-/Modbus-TCP-Prüfergebnis: 19 Prüfungen](docs/tcp-test.json)
- `src/BoardIO.h`: einzige Schicht für TCA9554 und digitale Eingänge
- `src/Core.h`: Zustände, Einstellungen und Alarmberechnung
- `src/SensorManager.h`: nicht blockierender Sensorzustandsautomat
- `src/ConfigStore.h`, `CalibrationManager.h`: NVS und externe Kalibrierung
- `src/ModbusProtocol.h`, `ModbusRtuServer.h`, `ModbusTcpServer.h`, `RegisterMap.h`: gemeinsames Protokoll, RTU/TCP und Register
- `src/NetworkConfig.h`: validierte feste IP oder DHCP, Speicherung durch HostServer
- `src/HostServer.*`, `WebPage.h`: Netzwerk-Task, API und Oberfläche

Die ursprüngliche Aufgabenbeschreibung liegt in `AGENTS.md`.
Repository: [JoeMoe32/ESP_Klima](https://github.com/JoeMoe32/ESP_Klima).
