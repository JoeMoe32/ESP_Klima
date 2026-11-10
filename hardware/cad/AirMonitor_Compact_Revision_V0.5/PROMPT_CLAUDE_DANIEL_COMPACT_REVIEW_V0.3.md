# Claude-Prüfauftrag für Daniel – AirMonitor Compact Revision V0.3

Du unterstützt Daniel bei der technischen Prüfung der parametrisch erzeugten Kompaktrevision in Fusion 360.

## Ziel

Prüfe die neue Geometrie, bei der der SEN0661 nicht mehr in einer separaten linken Box sitzt, sondern in einer geschlossenen Sensorzelle oben links über dem Waveshare-Board. Die Gehäusehöhe bleibt unverändert; die Länge wurde auf 208,0 mm reduziert.

V0.3 korrigiert die Befunde der digitalen Prüfung von V0.2 (K01–K12 in `CAD_COMPACT_SPEC_V0.3.md`). Prüfe zusätzlich gezielt:

- K01: Pod hängt an vier Zungen Z 50,0…52,0, verschraubt in Deckelbossen Z 52,0…55,0 – montierbar, Schraubenzugang von unten?
- K02–K04: Kalibrierhaube mit offenem Boden, Trennsteg und P04-Quersteg – Gasweg IN → Schlitze 1–4 → Sensorzelle → Schlitze 5–9 → OUT ohne Bypass?
- K05/K06: Dichtungsverpressung P04 25 %, P08 23 %.
- K07: Kabelstopfen füllt den Durchlass Z 46,0…54,0.
- K08/K09: Tasterplatine Y 28,0…108,0 und Deckelbossen (7,0/7,0), (7,0/105,0), (190,0/8,0), (190,0/104,0) gegen reale Bauteile.
- Offene Annahmen in Abschnitt 4 der Spezifikation.

## Führende Dateien

1. `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.3.step` – zuerst öffnen; enthält Referenzkörper für Waveshare und SEN0661.
2. `01_CAD_Global/AirMonitor_Compact_Assembly_V0.3.step` – Baugruppe ohne Dummys.
3. Einzelteile P01 bis P08 als STEP.
4. `CAD_COMPACT_SPEC_V0.3.md` – verbindliche Masse und Prüfpunkte.
5. `build_compact_revision.py` – parametrische Quelle und Reproduktionsweg.

## Regeln

- Nichts stillschweigend ändern.
- Alle Masse in mm mit einer Nachkommastelle.
- Werte kennzeichnen als `[gemessen]`, `[Datenblatt]`, `[Entscheidung]`, `[abgeleitet]` oder `[Annahme]`.
- Pro Abweichung Fusion-360-Screenshot mit sichtbarem Messwert und Bezugskanten.
- STEP ist führend; STL dient nur der Slicerprüfung.

## Prüfreihenfolge

### 1. Dateiinventar

| Datei | vorhanden | lesbar | Körperzahl | Einheit | Bemerkung |
|---|---|---|---:|---|---|

### 2. P01 Unterteil

Prüfe:
- Aussenhülle 208,0 × 132,0 × 55,0 inklusive Flanschen.
- Waveshare-Träger X 10,0…185,0; Standoff-Raster 155,0 × 70,0.
- reale Passung ohne Verspannung.
- Front- und Rücköffnung X 36,6…158,6, Z 12,0…55,0.
- Zugang zu SMA, RJ45, USB-C, DI, 24 V, RS485 und allen Relaisklemmen.
- rechte Stirnwand mit DC5521 Ø11,2, ZERO/SPAN Ø3,0 und Tasterplatinenhalter.

### 3. P03 Sensorpod über Board

Prüfe:
- Unterseite Z 40,0; Boardhöchstpunkt Z 27,6; Freiraum 12,4.
- Sensorlochbild 15,0, zwei Bohrungen Ø3,0.
- SEN0661-Unterseite Z 46,0; höchster Punkt Z 54,4.
- Deckelunterseite Z 55,0; Rest 0,6.
- Gravity-Kabel passt durch 4,0 × 6,0 und erreicht den I²C-Anschluss ohne scharfen Knick.
- Sensorzelle ist nach unten geschlossen und hat keinen offenen Leckweg zum Elektronikraum.

### 4. P02 Deckel und Dichtungen

Prüfe:
- 9 Lüftungsschlitze liegen vollständig über der Sensorzelle.
- Pod-Befestigung mit vier Blindbossen kollidiert nicht mit Haube oder Sensor.
- P08 dichtet Pod gegen Deckel.
- P04 dichtet Kalibrierhaube gegen Deckel.
- Normalbetrieb: Haube entfernt, Luftweg frei.
- Kalibrierbetrieb: IN → Sensor → OUT, kein Bypass.

### 5. P07 Haube

- Lochabstand, Tüllen und Planauflage prüfen.
- Schlauchzugang und Druckausrichtung bewerten.
- Prüfen, ob der Prüfgasstrom den Sensor tatsächlich durchströmt.

### 6. Druckprüfung

In PrusaSlicer prüfen:
- P01 208 × 132 × 55 einteilig.
- P02 208 × 112 einteilig.
- keine ausserhalb des Bauraums liegenden Brims/Skirts.
- Supportbedarf je Teil.
- Mindestwandstärken und problematische Brücken markieren.

## Ergebnisformat

| Teil | Soll | Ist | Delta | Bewertung | Änderung erforderlich |
|---|---:|---:|---:|---|---|

Schlussbewertung je Teil:
- `freigegeben`
- `freigegeben mit Änderungen`
- `nicht freigegeben`

Geometrie erst nach Jonathans Bestätigung ändern. Danach geänderte Einzelteile separat als STEP und STL exportieren und Revision V0.4 dokumentieren.
