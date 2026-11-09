# Laminar AirMonitor HCHO – CAD-Konstruktionsspezifikation V0.2 Compact

**Status:** Kompaktrevision zur Prüfung durch Daniel in Fusion 360  
**Einheit:** mm  
**Koordinatensystem:** Ursprung an der äusseren unteren Ecke des Unterteils, X lange Seite, Y kurze Seite, Z nach oben.

## 1 Ziel der Revision

Die separate Sensorbox links neben dem Waveshare entfällt. Der SEN0661 wird in einer geschlossenen Sensorzelle **oben links über dem Waveshare-Board** angeordnet. Die Gehäusehöhe bleibt unverändert. Dadurch reduziert sich die Gehäuselänge von 263,0 auf **208,0 mm**.

Normalbetrieb:
- Kalibrierhaube entfernt.
- Neun Lüftungsschlitze offen.
- Umgebungsluft gelangt direkt in die geschlossene Sensorzelle.

Kalibrierbetrieb:
- Kalibrierhaube montiert.
- TPU-Dichtung unter der Haube.
- Prüfgasweg `IN → Sensorzelle → SEN0661 → OUT`.
- Die Sensorzelle ist nach unten gegen den Elektronikraum geschlossen; nur der Kabeldurchlass bleibt und wird mit Stopfen/Verguss abgedichtet.

## 2 Hauptänderungen gegenüber V0.1

| ID | Änderung | V0.1 | V0.2 Compact |
|---|---|---:|---:|
| A01 | Gehäuselänge | 263,0 | 208,0 |
| A02 | Gehäusehöhe Unterteil | 55,0 | 55,0 unverändert |
| A03 | Deckelhöhe | Z 55,0…58,0 | Z 55,0…58,0 unverändert |
| A04 | Sensorposition | links neben Elektronik | oben links über Waveshare |
| A05 | separate Sensorbox | vorhanden | entfernt |
| A06 | Waveshare-Träger | X 65,0…240,0 | X 10,0…185,0 |
| A07 | Sensorpod | Boden bis Deckel | nur Z 40,0…54,0 |
| A08 | Kalibrierhaube | vorhanden | abnehmbar; Hüllmass 48,0 × 105,6 × 38,0 |
| A09 | rechte Stirnwand | alte Buchsen-/Tasterlage | DC5521 und ZERO/SPAN integriert |

## 3 Teileumfang

| ID | Teil | Aussenmass / Hülle | Material | Druckausrichtung | Status |
|---|---|---|---|---|---|
| P01 | Kompaktes Unterteil | 208,0 × 132,0 × 55,0 inkl. Flansche | PETG/ASA | Boden flach | prüfen |
| P02 | Kompakter Deckel | 208,0 × 112,0 × 7,0 inkl. Unterseitenbossen; Deckelplatte 3,0 | PETG/ASA | flach; Slicer prüfen | prüfen |
| P03 | Kompakter Sensorpod | 45,5 × 90,0 × 14,0 inkl. Befestigungslaschen | PETG/ASA | Boden flach | prüfen |
| P04 | Haubendichtung | 44,0 × 82,0 × 1,2 | TPU 95A | flach | prüfen |
| P05 | Kabelstopfen | 4,0 × 6,0 × 3,2 | TPU/Silikon | flach | prüfen |
| P07 | Kalibrierhaube | Hülle 48,0 × 105,6 × 38,0 | PETG/ASA | Flansch flach | prüfen |
| P08 | Sensorpod-Deckeldichtung | 45,5 × 82,0 × 1,0 | TPU 95A | flach | neu |

## 4 Komponentenanordnung

### Waveshare

```text
carrier_x_min = 10.0
carrier_x_max = 185.0
carrier_y_min = 11.0
carrier_y_max = 101.0
board_bottom_z = 9.6
board_max_top_z = 27.6
mount_centers = [(20,21),(175,21),(20,91),(175,91)]
mount_spacing = 155.0 x 70.0
```

Daniel muss die reale Platine beziehungsweise den schwarzen Waveshare-Träger einsetzen und die Lochlage bestätigen.

### SEN0661

```text
sensor_pod_bbox = X 6.0..51.5; Y 12.0..102.0; Z 40.0..54.0
sensor_pcb_bbox = X 12.8..44.8; Y 46.0..68.0; Z 46.0..47.6
sensor_hole_centers = [(16.3,49.5),(16.3,64.5)]
sensor_hole_spacing = 15.0
sensor_hole_diameter = 3.0
sensor_measured_total_height = 8.4
sensor_highest_point = Z 54.4
lid_inner_surface = Z 55.0
remaining_clearance = 0.6
```

Der Abstand von 0,6 mm ist kritisch und muss mit dem realen SEN0661 inklusive Gravity-Stecker geprüft werden.

## 5 Unterteil P01

| Feature | Position / Mass | Status |
|---|---|---|
| Körper | X 0…208; Y 0…112; Z 0…55 | neu kompakt |
| Montageflansche | Y -10…0 und 112…122 | Gesamtbreite 132,0 |
| Wandstärke | 2,8 | festgelegt |
| Boden | 2,8 | festgelegt |
| Steuerungsöffnung | X 36,6…158,6; Z 12…55; Breite 122,0 | gemessen/abgeleitet |
| Relaisöffnung | X 36,6…158,6; Z 12…55; Breite 122,0 | Entscheidung |
| DC5521 | rechte Wand, Y 15,0; Z 27,5; Ø11,2 | aus T3 |
| ZERO | rechte Wand, Y 50,0; Z 28,0; Ø3,0 | aus T3 |
| SPAN | rechte Wand, Y 66,0; Z 28,0; Ø3,0 | aus T3 |
| Tasterplatine | 80,0 × 20,0 × 1,5; Lochbild 76,0 × 16,0 | gemessen |
| Waveshare-Standoffs | (20,21), (175,21), (20,91), (175,91); Ø9,0; Pilot Ø2,5 | prüfen |
| Deckelbossen | X 8 / 200; Y 8 / 104 | M3/Insert finalisieren |
| Wandmontagebohrungen | X 37 / 171; Y -5 / 117; Ø4,5 | prüfen |

## 6 Deckel P02

| Feature | Position / Mass |
|---|---|
| Deckelplatte | 208,0 × 112,0 × 3,0; Z 55…58 |
| Lüftungsschlitze | 9 Stück; X 12…45; je 33 × 4; Y-Start 23; Pitch 8 |
| Haubenlöcher | X 27; Y 10 / 104; Ø2,2 |
| Deckelschrauben | X 8 / 200; Y 8 / 104; Ø3,3 / Gegenbohrung Ø6,2 |
| Pod-Befestigungsbossen | (14,14), (44,14), (14,100), (44,100); Ø7,0 |
| Pilot für Pod-Befestigung | Ø2,5; blind von unten; endgültiges Insertmass offen |

## 7 Sensorpod P03

| Feature | Position / Mass |
|---|---|
| Aussenkörper | X 6…51,5; Y 16…98; Z 40…54 |
| Aussenhöhe | 14,0 |
| Wand/Boden | 3,0 / 3,0 |
| Innenraum | X 9…48,5; Y 19…95; Z 43…54 |
| Sensorbossen | Ø5,6; Oberkante Z 46,0 |
| Sensorbohrungen | 2 × Ø3,0; Abstand 15,0 |
| Gravity-Durchlass | X 47,5…52,0; Y 83…89; Z 46…54 |
| Montagezungen | Y 12…16 und 98…102; Z 52…54 |
| Montagelöcher | (14,14), (44,14), (14,100), (44,100); Ø3,0 |

## 8 Vertikale Kollisionsrechnung

```text
Waveshare höchste Stelle = Z 27.6 [gemessen + Lage]
Sensorpod Unterseite = Z 40.0
Freiraum Board → Pod = 12.4
Sensorplatine Unterseite = Z 46.0
SEN0661 höchster Punkt = Z 54.4
Deckelunterseite = Z 55.0
Freiraum Sensor → Deckel = 0.6
```

## 9 Druckbarkeit

- P01: 208,0 × 132,0 × 55,0; passt einteilig in Prusa MK4 250 × 210 × 220.
- P02: 208,0 × 112,0; passt einteilig.
- P03, P04, P05, P08: klein und flach druckbar.
- Eine Gehäuseteilung ist für diese Revision nicht erforderlich.
- Kalibrierhaube: Tüllen und Brücken im Slicer kontrollieren.

## 10 Kritische Prüfpunkte für Daniel

1. Reales Waveshare-Modul in P01 beziehungsweise im Referenz-STEP positionieren.
2. Raster 155,0 × 70,0 sowie X-Lage 10,0…185,0 bestätigen.
3. Öffnungen vorne/hinten mit allen Klemmen, RJ45, USB-C und SMA abgleichen.
4. Schraubendreherzugang zu allen Relaisklemmen prüfen.
5. SEN0661 inklusive Stecker in P03 einsetzen; 0,6-mm-Deckelabstand prüfen.
6. Wärmeabstand zwischen Waveshare und Sensorpod bewerten; 12,4 mm mechanischer Abstand ist vorhanden.
7. Sensorpod-Deckeldichtung P08 und Haubendichtung P04 auf geschlossene Dichtlinien prüfen.
8. Prüfgas-Bypass und Leckweg zum Elektronikraum ausschliessen.
9. Tasterhalter und DC5521-Kontermutter auf Kollision mit Board/Kabeln prüfen.
10. Heat-Set-Insert-Bohrungen nach konkretem Insert-Fabrikat finalisieren.

## 11 Dateien

- `01_CAD_Global/AirMonitor_Compact_Assembly_V0.2.step` – Baugruppe ohne Kaufteil-Dummys
- `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.2.step` – Referenz mit Waveshare- und SEN0661-Dummys
- P01…P08 jeweils als STEP; Druckdateien zusätzlich als STL
- `build_compact_revision.py` – führende parametrische Quelle
- `DIMENSIONS.csv` – automatisch erzeugter Massbericht

## 12 Änderungsprotokoll

```text
V0.1: separate Sensorbox links, Gesamtlänge 263,0 mm.
V0.2 Compact: Sensorpod über linkem Waveshare-Bereich; separate Sensorbox entfernt;
Gesamtlänge 208,0 mm; Höhe unverändert; Taster-/DC5521-Stirnwand integriert;
abnehmbare Kalibrierhaube für ZERO/SPAN.
```
