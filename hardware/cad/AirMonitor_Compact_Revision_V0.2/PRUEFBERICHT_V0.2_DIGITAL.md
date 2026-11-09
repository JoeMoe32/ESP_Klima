# Prüfbericht AirMonitor Compact V0.2 – digitaler Teil

**Datum:** 09.11.2026  
**Geprüft von:** Claude (für Jonathan), Grundlage `PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW.md`  
**Methode:** STEP-Dateien textuell ausgewertet (Schema, Einheit, Körper), STL-Druckdateien mit Punktsonden (Material/Luft) in globalen Koordinaten geprüft, Geometrie aus `build_compact_revision.py` nachgerechnet. Kein CAD-Kern, keine Fusion-360-Screenshots.  
**Nicht geprüft (bleibt bei Daniel):** reales Waveshare und SEN0661 gegen Dummys, Gravity-Kabelbiegung, Klemmen-/Schraubendreherzugang, PrusaSlicer-Supportanalyse, Screenshots je Abweichung.

Kennzeichnung: `[abgeleitet]` = aus Modell/Skript berechnet bzw. per Sonde bestätigt, `[Annahme]` = nicht aus den Daten belegbar.

**Geometrie unverändert. Änderungen erst nach Jonathans Bestätigung (Revision V0.3).**

---

## 1 Dateiinventar

| Datei | vorhanden | lesbar | Körperzahl | Einheit | Bemerkung |
|---|---|---|---:|---|---|
| 01_CAD_Global/AirMonitor_Compact_Assembly_V0.2.step | ja | ja | 7 | mm | 6 × MANIFOLD_SOLID_BREP + P07 als BREP_WITH_VOIDS |
| 01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.2.step | ja | ja | 12 | mm | 7 Teile + 5 Dummys (Träger, PCB, Sensor, Sensor-Oberteil, Stecker) |
| 01_CAD_Global/P01_Compact_Base_Global.step | ja | ja | 1 | mm | AP214 |
| 01_CAD_Global/P02_Compact_Lid_Global.step | ja | ja | 1 | mm | AP214 |
| 01_CAD_Global/P03_Compact_SensorPod_Global.step | ja | ja | 1 | mm | AP214 |
| 01_CAD_Global/P04_Hood_Gasket_TPU.step | ja | ja | 1 | mm | AP214 |
| 01_CAD_Global/P05_Cable_Stop_Global.step | ja | ja | 1 | mm | AP214 |
| 01_CAD_Global/P07_Calibration_Hood_Unchanged.step | ja | ja | 1 | mm | **BREP_WITH_VOIDS: Körper mit eingeschlossenem Hohlraum** (siehe P07) |
| 01_CAD_Global/P08_Pod_Lid_Gasket_Global.step | ja | ja | 1 | mm | AP214 |
| 02_CAD_Print/*.step (7 Dateien) | ja | ja | je 1 | mm | P07 ebenfalls BREP_WITH_VOIDS |
| 02_CAD_Print/*.stl (7 Dateien) | ja | ja | – | mm | Hüllmasse = DIMENSIONS.csv |
| P06 | nein | – | – | – | in Spezifikation nicht aufgeführt, Nummer übersprungen |

## 2 Ergebnis Soll/Ist

### P01 Unterteil

| Teil | Soll | Ist | Delta | Bewertung | Änderung erforderlich |
|---|---:|---:|---:|---|---|
| P01 Aussenhülle | 208,0 × 132,0 × 55,0 | 208,0 × 132,0 × 55,0 [abgeleitet] | 0,0 | i. O. | nein |
| P01 Standoff-Raster | 155,0 × 70,0 | 155,0 × 70,0 [abgeleitet] | 0,0 | i. O. | nein |
| P01 Standoff-Oberkante | Z 9,6 | Z 9,6 [abgeleitet] | 0,0 | i. O. | nein |
| P01 Front-/Rücköffnung | X 36,6…158,6; Z 12,0…55,0 | X 36,6…158,6; Z 12,0…55,0, Wand offen [abgeleitet, Sonde] | 0,0 | i. O. | nein |
| P01 DC5521 / ZERO / SPAN | Ø11,2 Y 15,0 Z 27,5 / Ø3,0 Y 50,0 und 66,0, Z 28,0 | wie Soll [abgeleitet, Sonde] | 0,0 | i. O. | nein |
| P01 Tasterhalter-Lochbild | 76,0 × 16,0 | 76,0 × 16,0 (Y 32,0/108,0; Z 22,0/38,0) [abgeleitet] | 0,0 | i. O. | nein |
| **P01 Tasterplatine 80,0 × 20,0 vs. Rückwand** | Platine frei | Platine Y 30,0…110,0 [Annahme: symmetrisch zum Lochbild]; Rückwand innen Y 109,2 [abgeleitet] | **−0,8 Kollision** | n. i. O. | ja: Halter um ≥ 1,5 nach −Y verschieben, ZERO/SPAN-Bohrungen mitziehen |
| **P01 Deckelbossen (8,0/8,0) und (8,0/104,0) Ø9,0 vs. Waveshare-Träger** | frei | Bosse ragt 0,9 in Träger-Dummy-Ecke (10,0/11,0) bzw. (10,0/101,0), Z 9,6…27,6 [abgeleitet, Sonde] | **−0,9 Kollision** | n. i. O. (Dummy) | real prüfen; ggf. Bossen nach aussen/kleiner oder Träger-Lage anpassen |
| **P01 Deckelbossen vs. P03-Montagezungen** | frei | Überlappung X 8,0…10,1; Y 12,0…12,5 bzw. 99,5…102,0; Z 52,0…54,0 [abgeleitet, Sonde] | **−0,5 Kollision** | n. i. O. | ja, mit P03-Zungen lösen |
| P01 Deckelbossen-Oberkante | Deckelunterseite Z 55,0 | Z 54,0 [abgeleitet] | 1,0 Spalt | Hinweis | Insertmass finalisieren (Spalt bewusst?) |

### P03 Sensorpod

| Teil | Soll | Ist | Delta | Bewertung | Änderung erforderlich |
|---|---:|---:|---:|---|---|
| P03 Unterseite | Z 40,0 | Z 40,0 [abgeleitet] | 0,0 | i. O. | nein |
| P03 Freiraum Board → Pod | 12,4 | 12,4 (27,6 → 40,0) [abgeleitet] | 0,0 | i. O. | nein |
| P03 Sensorbossen-Oberkante | Z 46,0 | Z 46,0 [abgeleitet] | 0,0 | i. O. | nein |
| P03 Sensorbohrungen | 2 × Ø3,0, Abstand 15,0 | 2 × Ø3,0, Abstand 15,0; Boden darunter geschlossen [abgeleitet, Sonde] | 0,0 | i. O. | nein |
| P03 Restabstand Sensor → Deckel | 0,6 | 0,6 (54,4 → 55,0) [abgeleitet] | 0,0 | kritisch, real prüfen | nein (Daniel) |
| P03 Zelle nach unten geschlossen | kein Leckweg | Boden 3,0 geschlossen [abgeleitet] | – | i. O. | nein |
| **P03 Gravity-Durchlass** | 4,0 × 6,0 | Schlitz X 47,5…52,0; Y 83,0…89,0; Z 46,0…54,5, Querschnitt durch die Wand 6,0 × 8,0 [abgeleitet] | +2,0 Höhe | Hinweis | Mass mit P05 abstimmen |
| **P03 Montagezungen vs. P02-Bossen** | frei | Kollision, siehe P02 | – | n. i. O. | ja |

### P02 Deckel

| Teil | Soll | Ist | Delta | Bewertung | Änderung erforderlich |
|---|---:|---:|---:|---|---|
| P02 Hülle | 208,0 × 112,0 × 7,0 | 208,0 × 112,0 × 7,0 [abgeleitet] | 0,0 | i. O. | nein |
| P02 9 Schlitze über Sensorzelle | vollständig innerhalb | X 12,0…45,0; Y 23,0…91,0 liegt in Zelle X 9,0…48,5; Y 19,0…95,0, in P08- und P04-Innenkontur [abgeleitet] | ≥ 3,0 Rand | i. O. | nein |
| **P02 Pod-Bossen Ø7,0, Z 51,0…55,0** | kollisionsfrei | überlappen P03-Zungen (Z 52,0…54,0) vollflächig, P03-Wand (Y 16,0…17,5 bzw. 96,5…98,0, Z 51,0…54,0) und P08-Dichtung (Z 54,0…55,0) [abgeleitet, Sonde] | **bis −3,0 Kollision** | n. i. O. | ja: Pod ist so nicht montierbar |
| **P02 Drucklage Export** | Platte flach auf Bett | Druck-STL hat Platte oben (Z 4,0…7,0), Bossen unten (Z 0,0…4,0) [abgeleitet] | – | Hinweis | im Slicer 180° drehen oder gedreht exportieren |
| P02 Haubenlöcher Ø2,2 | Befestigung Haube | Durchgangsloch, darunter kein Gewinde/Insert/Mutter modelliert [abgeleitet] | – | Hinweis | Befestigung definieren |

### P04 / P08 Dichtungen

| Teil | Soll | Ist | Delta | Bewertung | Änderung erforderlich |
|---|---:|---:|---:|---|---|
| P08 Dichtlinie Pod ↔ Deckel | geschlossen | geschlossener Rahmen 45,5 × 82,0, Steg 3,0 [abgeleitet] | – | i. O. | nein |
| **P08 Verpressung** | definiert (typ. 20–30 % [Annahme]) | Dicke 1,0 im Spalt 1,0 (Z 54,0…55,0) → 0 % [abgeleitet] | 0 % | n. i. O. | Dicke/Nut festlegen |
| P04 Dichtlinie Haube ↔ Deckel | geschlossen | geschlossener Rahmen 44,0 × 82,0, Steg 2,0 [abgeleitet] | – | i. O. | nein |
| **P04 Verpressung** | definiert | Haubenplatte Z 58,15 auf Dichtung Z 57,95…59,15 → 1,05 von 1,2 Überdeckung (88 %) [abgeleitet] | +1,05 Überdeckung | n. i. O. | Haube auf ≈ Z 58,9…59,0 oder Dichtung in Nut |

### P05 Kabelstopfen

| Teil | Soll | Ist | Delta | Bewertung | Änderung erforderlich |
|---|---:|---:|---:|---|---|
| **P05 Abdichtung Durchlass** | Durchlass dicht | Stopfen 4,0 × 6,0 × 3,2 füllt nur Z 48,0…51,2 des Durchlasses Z 46,0…54,0; offen bleiben Z 46,0…48,0 und 51,2…54,0 [abgeleitet, Sonde] | **4,8 offen** | n. i. O. | Stopfen auf volle Höhe 8,0 oder Durchlass auf Kabelmass + Verguss |

### P07 Kalibrierhaube

| Teil | Soll | Ist | Delta | Bewertung | Änderung erforderlich |
|---|---:|---:|---:|---|---|
| P07 Hülle | 48,0 × 105,6 × 38,0 | 48,0 × 105,6 × 41,0 [abgeleitet] | **+3,0** | Abweichung | Spezifikation oder Tüllen anpassen |
| P07 Lochabstand | 94,0 (Y 10,0/104,0) | 94,0 [abgeleitet] | 0,0 | i. O. | nein |
| **P07 Haubenboden** | offen über den Schlitzen | Platte Z 58,15…60,95 durchgehend geschlossen, nur 2 Schraubenlöcher [abgeleitet, Sonde bei (28,0/57,0/59,5) und (28,0/25,0/59,5) = Material] | – | **n. i. O.** | Boden über Schlitzbereich öffnen |
| **P07 Anschlüsse IN/OUT** | mit Innenraum verbunden | Bohrungen Ø2,0 beginnen Z 82,0, Innenraumdecke Z 81,15 → 0,85 Haut [abgeleitet, Sonde] | 0,85 zu | **n. i. O.** | Bohrungen bis in Innenraum führen |
| **P07 Gasweg IN → Sensor → OUT** | kein Bypass | auch nach Öffnen: eine einzige Kammer über allen 9 Schlitzen, IN und OUT direkt verbunden → Bypass [abgeleitet] | – | **n. i. O.** | Trennsteg: IN auf Schlitze 1–4, OUT auf 6–9, Steg dichtet auf Deckel |

### Druckprüfung (Bauraum Prusa MK4 250 × 210 × 220)

| Teil | Hülle | passt | Bemerkung |
|---|---|---|---|
| P01 | 208,0 × 132,0 × 55,0 | ja | einteilig |
| P02 | 208,0 × 112,0 × 7,0 | ja | Lage drehen (s. o.) |
| P03 | 45,5 × 90,0 × 14,0 | ja | Zungen 4,0 auskragend in Z 52,0…54,0 → Support prüfen |
| P07 | 48,0 × 105,6 × 41,0 | ja | Dach-Innenbrücke 23,0 × 65,0 (nach Öffnen relevant) |
| P04, P05, P08 | klein | ja | flach |

Brims/Skirts, Supportbedarf und Wandstärken im Slicer: **nicht geprüft** (Daniel).

## 3 Schlussbewertung je Teil

| Teil | Bewertung | Hauptgrund |
|---|---|---|
| P01 Unterteil | freigegeben mit Änderungen | Tasterplatine 0,8 in Rückwand; Deckelbossen vs. Träger und Pod-Zungen |
| P02 Deckel | **nicht freigegeben** | Pod-Bossen kollidieren mit P03 und P08 |
| P03 Sensorpod | freigegeben mit Änderungen | Montagezungen neu lagern (mit P02/P01 abstimmen) |
| P04 Haubendichtung | freigegeben mit Änderungen | Verpressung definieren |
| P05 Kabelstopfen | **nicht freigegeben** | dichtet Durchlass nicht |
| P07 Kalibrierhaube | **nicht freigegeben** | Boden zu, Anschlüsse zu, Bypass |
| P08 Pod-Deckeldichtung | freigegeben mit Änderungen | Verpressung 0 %; Bossen-Kollision |

## 4 Vorschlag für V0.3 (nur nach Bestätigung durch Jonathan)

1. **Pod-Befestigung neu:** Zungen und Deckelbossen ausserhalb der P08-Dichtlinie und der Pod-Wand legen, z. B. Zungen Z 50,0…52,0 und Bossen Z 52,0…55,0. Neue Positionen müssen auch die P01-Deckelbossen Ø9,0 bei (8,0/8,0) und (8,0/104,0) freihalten (Mittenabstand > 8,0).
2. **P07:** Boden über dem Schlitzfeld öffnen, Bohrungen bis in den Innenraum führen, Trennsteg zwischen IN- und OUT-Kammer (Steg dichtet auf dem Deckel zwischen Schlitz 4 und 6).
3. **Dichtungen:** P08 und P04 mit definierter Verpressung (Nut oder Dicke).
4. **P05:** Stopfen auf volle Durchlasshöhe 8,0 oder Durchlass auf Kabelquerschnitt reduzieren und vergiessen.
5. **P01:** Tasterhalter um ≥ 1,5 nach −Y verschieben, ZERO/SPAN mitziehen. Deckelbossen vs. realer Waveshare-Träger prüfen.
6. **P02:** Druckdatei mit Platte nach unten exportieren. Haubenbefestigung (Insert/Mutter) festlegen.
7. **Spezifikation:** P07-Höhe 41,0 statt 38,0 nachführen oder Tüllen kürzen.
