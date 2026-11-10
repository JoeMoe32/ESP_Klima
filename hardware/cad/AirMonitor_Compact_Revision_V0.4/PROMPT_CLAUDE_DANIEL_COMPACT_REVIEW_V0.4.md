# Claude-Prüfauftrag – Laminar AirMonitor HCHO Compact V0.4

Prüfe mit Daniel in Fusion 360 die Revision V0.4. Die gewünschte Anordnung ist verbindlich:

- Sensorhalter mittig links über dem Waveshare-Board
- SEN0661-Platine mittig im Halter
- Gravity-Stecker unterhalb der Platine
- Kabelabgang nach unten
- kompakte Kalibrierhaube mit zwei Anschlüssen links

## Führende Dateien

1. `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.4.step`
2. `01_CAD_Global/AirMonitor_Compact_Assembly_V0.4.step`
3. `01_CAD_Global/P03_CenterLeft_SensorHolder_Global.step`
4. `01_CAD_Global/P07_Compact_Calibration_Hood.step`
5. `CAD_COMPACT_SPEC_V0.4.md`
6. `DIMENSIONS.csv`

## Prüfreihenfolge

1. SEN0661-Dummy gegen reales Bauteil vergleichen.
2. Platinenmittelpunkt und Lochbild kontrollieren.
3. Steckerposition unterhalb der Platine kontrollieren.
4. Durchlass, Kabelbogen und Abdichtung prüfen.
5. Kollisionen zum Waveshare und zum Deckel prüfen.
6. Lüftungsschlitze im Normalbetrieb prüfen.
7. Haube, Dichtung, Schrauben und U-Gasweg prüfen.
8. Druckbarkeit aller Einzelteile prüfen.

## Rückmeldung

Für jeden Prüfpunkt:

| ID | Merkmal | Soll | Ist | Delta | Status | notwendige Änderung |
|---|---|---:|---:|---:|---|---|

Jeden Wert als `[gemessen]`, `[Datenblatt]`, `[Entscheidung]`, `[abgeleitet]` oder `[Annahme]` kennzeichnen. Keine Masse erfinden. Maximal drei Rückfragen gleichzeitig.

## Klare Freigabe

Am Ende exakt eine Einstufung ausgeben:

- `freigegeben`
- `freigegeben mit Änderungen`
- `nicht freigegeben`
