# Modbus RTU und TCP

## Ethernet / Modbus TCP

Direktverbindung: ESP **192.168.77.2**, Laptop **192.168.77.1**, beide /24,
kein Gateway. TCP-Port **502**, Unit-ID **1**; alternativ wird 255 akzeptiert.
Bis zu zwei TCP-Clients gleichzeitig. FC03/FC04 lesen das gleiche Registerabbild
wie RS485; TCP erhält alle 200 ms eine konsistente Kopie aus der Hauptsteuerung.
Schreibfunktionen sind nicht implementiert. Keine Baudrate/Parität bei TCP.

MBAP-Header mit Transaction-ID, Protocol-ID 0 und Längenfeld; keine RTU-CRC auf TCP.
Geteilte und zusammen empfangene Telegramme werden anhand der MBAP-Länge getrennt.
Ungültige MBAP-Header schließen die betreffende Verbindung. Unvollständige Telegramme
laufen nach 3 s ab, vollständig untätige Clients nach 60 s. Andere Unit-IDs erhalten
keine Antwort. Ist das lokale Registerabbild älter als 2 s, antwortet der Server
mit Exception 04 statt mit alten Werten.

Die TCP-Zähler sind getrennt vom RTU-Zähler: USB `status` und JSON-Felder
`tcpRequests`/`tcpRejected` auf `/api/status`. Register 40059 bleibt der RTU-Zähler.

Beispiel im Modbus-Client: FC03, Startadresse **9**, Anzahl **2**. Ergebnis
`[2050, 4200]` bedeutet 20,50 °C und 42,00 %. Programme mit 4xxxx-Anzeige verwenden
dafür 40010/40011; die Adresse auf dem Draht ist nullbasiert.

Wiederholbarer Test mit Python ohne Zusatzpakete:

```text
python tools/test_modbus_tcp.py 192.168.77.2
```

Primärquelle für TCP-Framing und Port:
https://www.modbus.org/file/secure/messagingimplementationguide.pdf

## RS485 / Modbus RTU

Slave 1, 9600 Baud, 8N1; UART TX17/RX18, automatische Richtungsumschaltung der Boardhardware.
Unterstuetzt: FC03 (Holding Registers lesen), FC04 (gleiche Werte als Input Registers).
Schreibfunktionen sind absichtlich gesperrt. Konfiguration und Relaistest ueber Service.
Broadcasts (Adresse 0) werden nicht beantwortet. Adressen 0..63 koennen gelesen werden;
reservierte Register enthalten 0xFFFF. Andere Adressen ergeben Exception 02.

Die erste Spalte ist die uebliche 4xxxx-Anzeige. Auf dem Draht wird der **Offset** gesendet.

| Anzeige | Offset | Bedeutung |
|---|---:|---|
|40001|0|Statusbits: 0 Ready, 1 Alarm, 2 Fault, 3 Service, 4 Kalibrieranforderung, 5 Testmodus|
|40002|1|Betriebsart: 0 TEST_MODE, 1 HCHO_MODE|
|40003|2|Fehlerbits: 0 Sensor, 1 veraltet, 2 Relaistreiber, 3 HCHO fehlt, 4 NVS|
|40010|9|Temperatur x100, int16; ungueltig 0x8000|
|40011|10|Feuchte x100, uint16; ungueltig 0xFFFF|
|40020|19|HCHO roh ppb, int16; ungueltig 0x8000|
|40021|20|HCHO korrigiert ppb, int16; ungueltig 0x8000|
|40022|21|HCHO Alarmgrenze ppb, uint16|
|40030|29|DI-Bitmaske: Bit0=DI1 bis Bit7=DI8; 1=aktiv|
|40031|30|Zuletzt bestaetigtes Relaisregister; 1=EIN. Bei Treiberfehler nicht als bestaetigten aktuellen Kontaktzustand werten.|
|40040|39|Alarm 0/1|
|40041|40|Fault 0/1|
|40042|41|Ready 0/1|
|40050|49|Kalibrierung aktiv 0/1|
|40051|50|Zero-Rohreferenz ppb, int16; ungueltig 0x8000|
|40052|51|Span-Rohreferenz ppb, int16; ungueltig 0x8000|
|40053|52|Span-Referenz 300 ppb|
|40054|53|Temperatur/Feuchte aktuell gueltig 0/1|
|40055|54|HCHO aktuell gueltig 0/1|
|40056|55|Uptime Sekunden, High Word|
|40057|56|Uptime Sekunden, Low Word|
|40058|57|Letzter Sensorfehler|
|40059|58|Beantwortete Modbus-Anfragen inkl. Exceptions, untere 16 Bit|
|40060|59|Relaistreiber erreichbar 0/1|

Sensorfehlercodes: 100+Wire-Schreibfehler, 200+empfangene Bytezahl bei zu kurzer
Antwort, 300+Wortindex bei CRC-Fehler. Fehlende neue Werte nach 15 s sind veraltet.
HCHO wird im aktuellen Testbetrieb immer als ungueltig veroeffentlicht.

Normgrundlage: https://www.modbus.org/specs.php
Der echte Mastertest ueber COM9 am 24.10.2026 bestand zehn Pruefungen, siehe
PRUEFPROTOKOLL.md und modbus-test.json. DI- und Relaismasken wurden gelesen;
einzeln betaetigte Eingaenge und mechanische Kontakte sind noch zu pruefen.
