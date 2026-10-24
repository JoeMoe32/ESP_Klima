# Prüfprotokoll – 24.10.2026

## Anpassung der Servicezeit

Servicezeit auf Benutzerwunsch von 5 auf **15 Minuten (900.000 ms)** verlängert.
USB-Meldung, Webhinweis und Anleitung angepasst. Build und Upload erfolgreich;
anschließend USB-Selbsttest PASS, Ready=1/Fault=0 und HTTP 200 mit dem neuen
15-Minuten-Hinweis bestätigt. Service wurde zur Prüfung nicht geöffnet.

## Ethernet und Modbus TCP – aktueller Stand

Direkte Verbindung Laptop ↔ Waveshare über Ethernet erfolgreich eingerichtet:

- USB-LAN „Ethernet 3“: **192.168.77.1/24**, DHCP aus, kein Gateway.
- ESP: **192.168.77.2/24**, feste Konfiguration in NVS, kein Gateway.
- Modbus TCP: **Port 502**, Unit-ID 1 oder 255, FC03/FC04.
- HTTP: **http://192.168.77.2/** und `/api/status` erreichbar.
- Letzter Build und Upload: **SUCCESS**, RAM 20.712 Byte, Flash 388.393 Byte.
- Nach Firmware-Neustart ohne erneutes Senden eines Netzbefehls wieder unter
  192.168.77.2 erreichbar: gespeicherte Netzkonfiguration wird geladen.
- Erweiterter Logik-Selbsttest einschließlich TCP-Header und IP-Validierung: PASS.

**19/19 reale Ethernet-Prüfungen bestanden**, ausgeführt mit
`tools/test_modbus_tcp.py`. Ergebnisse in [tcp-test.json](tcp-test.json):

| Prüfung | Ergebnis |
|---|---|
| FC03, alle 64 Register | PASS |
| HCHO als ungültig gekennzeichnet | PASS |
| FC04, DI- und Relaismaske | PASS |
| Auf mehrere TCP-Sendungen verteiltes Telegramm | PASS |
| Zwei Telegramme in einer TCP-Sendung, Transaction-IDs korrekt | PASS |
| Falsche Registeradresse → Exception 02 | PASS |
| Anzahl 0 → Exception 03 | PASS |
| Nicht unterstützte Funktion → Exception 01 | PASS |
| Anzahl >125 → Exception 03 | PASS |
| Unit-ID 255 | PASS |
| Zwei gleichzeitige TCP-Clients | PASS |
| Vollständige HTTP-Seite bei aktiven Modbus-Verbindungen | PASS |
| HTTP-Live-JSON mit Messwerten und HCHO=null | PASS |
| Webservice ohne Schlüssel → HTTP 403 | PASS |
| Falsche Protocol-ID → Verbindung geschlossen | PASS |
| Zu kurzes MBAP-Längenfeld → Verbindung geschlossen | PASS |
| Zu großes MBAP-Längenfeld → Verbindung geschlossen | PASS |
| Unvollständiges Telegramm → Verbindung nach 3 s geschlossen | PASS |
| Lesen nach Fehlerprüfungen weiterhin möglich | PASS |

Letzter TCP-Messpunkt: **23,14 °C / 37,14 %**, DI=0x00, Relais=0x05,
Alarm=1, Fault=0, Ready=1. Der Temperatur-Testalarm ist bei >23 °C erwartungsgemäß
aktiv. Parallel zu vorherigen TCP-Prüfungen wurden erneut **10/10 RTU-Prüfungen**
auf COM9 bestanden (20,08 °C / 43,44 %, Ready=1, Fault=0).

Beim HTTP-Hardwaretest wurde eine nach 2 KB abgeschnittene Antwort erkannt und
behoben: größere Antworten werden jetzt in 512-Byte-Blöcken gesendet. Die abschließende
Prüfung hat den gesamten HTTP-Inhalt gelesen. Wiederholtes Starten der Ethernet-Server
verwendet vorhandene Listener weiter, statt zusätzliche W5500-Sockets zu belegen.

## Frühere Basisprüfung vor der TCP-Erweiterung

- Build mit PlatformIO espressif32 7.1.3, Arduino, DFRobot_SCD4X 1.0.1,
  Ethernet 2.0.2: **SUCCESS**. Statische RAM-Belegung 20.704 Byte, Firmware
  384.145 Byte. Dynamischer Heap/Task-Stack ist in dieser RAM-Zahl nicht enthalten.
- Upload an COM6: **SUCCESS**, esptool hat Flash-Hashes verifiziert und neu gestartet.
- USB-Befehl `selftest`: **PASS**. Enthält Hysterese, Alarmquittierung,
  Sensoralterung, millis-Überlauf, Kalibrierformel und Modbus-Protokollfehler.
  Diese Prüfung verändert keine realen Ausgänge oder Kalibrierwerte.
- Die damalige Firmware lief bei der Statusabfrage seit 615 Sekunden ohne Neustart:
  TEST_MODE, service=0, alarm=0, fault=0, ready=1, faults=0x0000,
  DI=0x00, Relaisregister=0x04.
- Temperatur/Feuchte über 20 Sekunden wiederholt plausibel gelesen:
  21,51–21,53 °C und 42,32–42,75 %, Sensorfehler=0.
- Frühere Zwischenversion: Temperaturalarm mit Relaismaske 0x05 beobachtet;
  Rückschaltung bei 22,55 °C auf 0x04 nach Unterschreiten der Hysterese.
- W5500 erkannt; link=0, online=0. Sensor und Ready liefen trotz fehlendem LAN weiter.
- Abschließende USB-Abfrage bei 977 s Uptime: weiterhin fault=0, ready=1,
  Logik-Selbsttest PASS; Modbus requests=6, rejected=3. Temperatur 21,83–21,86 °C,
  Feuchte 43,92–44,36 %. LAN war damals noch ohne Link. Das jeweils zuletzt
  gespeicherte USB-Leseprotokoll liegt in [serial-test.txt](serial-test.txt).

## RS485 über tatsächlichen USB-Adapter

Adapter COM9: CH343, USB VID:PID 1A86:55D3.
Master 9600 Baud, 8N1, Slave 1. Kommunikation über A/B/GND zum Waveshare.

| Prüfung | Ergebnis |
|---|---|
| FC03, alle 64 Register, Antwortlänge und CRC | PASS |
| HCHO-Rohwert und Korrekturwert jeweils 0x8000 | PASS |
| FC04, DI- und Relaismaske | PASS |
| Adresse außerhalb Registermap → Exception 02 | PASS |
| Anzahl 0 → Exception 03 | PASS |
| Nicht unterstütztes FC01 → Exception 01 | PASS |
| Broadcast wird ignoriert | PASS |
| Fremde Slaveadresse wird ignoriert | PASS |
| Falsche CRC wird ignoriert | PASS |
| Status erneut nach Fehlertelegrammen lesbar | PASS |

Über Modbus gelesen: Temperatur 21,51 °C, Feuchte 42,32 %, Status 0x0021,
DI 0x00, Relais 0x04, Alarm 0, Fault 0, Ready 1. Die Rohdaten und Einzelresultate
stehen, nach erneuter Prüfung aktualisiert, in [modbus-test.json](modbus-test.json). Kein Schreibauftrag an Ausgänge
wurde für diesen Test versendet.

## Service-Freigabe im Browser (24.10.2026)

- Firmware mit Senden-Schaltfläche und separater Schlüsselprüfung gebaut und
  auf COM6 übertragen: **SUCCESS**, Flash-Hashes verifiziert. RAM 20.712 Byte,
  Firmware 392.729 Byte.
- USB-Status nach Neustart: TEST_MODE, Sensor gültig, fault=0, faults=0x0000,
  W5500/link/online=1, IP 192.168.77.2. Service für 15 Minuten geöffnet;
  alle Relais zunächst AUS.
- Tatsächlicher Chrome-Browser an `http://192.168.77.2/`: falscher Schlüssel
  wird abgewiesen, Eingabe und Senden bleiben sichtbar, Serviceaktionen gesperrt.
- Gültiger Schlüssel mit **Senden** bestätigt: Eingabe und Senden ausgeblendet,
  gelbe **Service**-Anzeige sichtbar (90 × 42 px, RGB 246/204/69),
  Restzeit sichtbar und Serviceaktionen freigegeben. Schlüsselprüfung schaltet
  keine Relais. Keine Speicherung des Schlüssels im Browser-Speicher.
- Der frühere Browserfehler `command is not a function` wurde durch einen
  eindeutigen Namen für den Service-Befehlshandler behoben. Im Browser
  Relais 8 gewählt und **Ausschalten** gedrückt: Befehl angenommen und anschließend
  Status „Relaisanforderung angenommen“. R8 war bereits AUS; alle Relais blieben AUS.
- Vor erneuter Service-Aktivierung war nach Ablauf des vorherigen Zeitfensters
  „Service geschlossen“ sichtbar; Eingabe sichtbar, Service-Schaltflächen gesperrt.
- Nach dem Flash trat vorübergehend „Verbindung unterbrochen“ auf. Im
  abschließenden Test lief die Live-Anzeige und die API lieferte gültige Daten.
- Screenshot der bestätigten Freigabe: [service-freigegeben.jpg](service-freigegeben.jpg).

## Noch nicht physisch abgenommen

- DHCP an einem Router, physisches Abziehen/Wiederverbinden des LAN-Kabels.
  HTTP-Auslieferung, Status-API, Zugriffssperre und Service-Bedienung im Browser
  wurden bereits geprüft.
- DI1 bis DI8 einzeln an den Klemmen, inklusive DI1/DI2-Langdruck.
- Alle acht mechanischen Relaiskontakte, tatsächliche angeschlossene Lasten.
- Fehler durch realen Sensor-/I²C-Ausfall und Wiederanlauf; Verhalten bei
  Stromausfall und Wiederkehr; Langzeitbetrieb.
- NVS-Persistenz nach tatsächlicher Grenzwertänderung und Neustart.
- Echter SFA40, HCHO-Messung, Referenzgase und Kalibrierung. Aktuell ist HCHO
  bewusst ungültig; vorhandene Rechen- und Protokolltests ersetzen keinen Sensortest.

Für die vollständigen Akzeptanzkriterien in AGENTS.md sind diese Hardwareprüfungen
noch erforderlich. Keine Abnahme als einsatzbereites Formaldehyd-Warngerät.
