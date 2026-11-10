# Laminar AirMonitor HCHO – CAD Compact Revision V0.4

## Status

Prüfstand für Daniel / Fusion 360. Keine Serienfreigabe.

## Änderung gegenüber V0.3

- Sensorhalter von der äusseren linken Zone in die **Mitte links über dem Waveshare-Board** verschoben.
- Sensorhalter auf **60,0 × 44,0 mm** kompakter ausgeführt.
- SEN0661-Platine im Halter zentriert.
- Gravity-Stecker liegt **unterhalb der Platine** und ragt durch eine Öffnung im Pod-Boden nach unten.
- Kabel wird nach unten in den Elektronikraum geführt; kein seitlicher Kabelabgang mehr.
- Kalibrierhaube auf **64,0 × 48,0 mm** verkleinert, mit zwei Anschlüssen links wie in der Referenzdarstellung.
- Interner U-förmiger Gasweg: IN → untere Kammer → rechter Umlenkspalt → obere Kammer → OUT.

## Koordinatensystem

- Ursprung: äussere untere Ecke des Unterteils
- X: lange Gehäuseseite
- Y: kurze Gehäuseseite
- Z: nach oben

## Hauptmasse

| Merkmal | Wert | Status |
|---|---:|---|
| Gehäusekörper | 208,0 × 112,0 × 55,0 mm | [Entscheidung] |
| Gesamtbreite mit Flanschen | 132,0 mm | [abgeleitet] |
| Sensorhalter P03 | 60,0 × 44,0 × 14,0 mm | [Annahme, zu prüfen] |
| P03 Position | X 44,0…104,0 / Y 34,0…78,0 / Z 40,0…54,0 | [Entscheidung] |
| SEN0661 PCB | 32,0 × 22,0 × 1,6 mm | [Datenblatt] |
| SEN0661 PCB Position | X 58,0…90,0 / Y 45,0…67,0 / Z 45,0…46,6 | [Annahme, zu prüfen] |
| Gravity-Stecker Dummy | 8,0 × 8,0 × 4,4 mm | [Annahme innerhalb Gesamtbauhöhe] |
| Gravity-Stecker Position | unter PCB, X 81,0…89,0 / Y 52,0…60,0 | [Entscheidung] |
| Freiraum Waveshare → Pod | 12,4 mm | [abgeleitet] |
| Freiraum Sensoroberkante → Deckel | 6,0 mm | [abgeleitet] |
| Kalibrierhauben-Flansch | 64,0 × 48,0 mm | [Annahme nach Referenzbild] |
| Max. Höhe mit Haube und Tüllen | 93,9 mm | [abgeleitet] |

## Sensorhalter P03

- geschlossene Messzelle mit 2,5 mm Wandstärke
- Befestigung über vier externe Zungen
- zwei Sensorbefestigungen, Lochabstand 15,0 mm, Ø3,0 mm
- Sensorplatine mittig im Halter
- Gravity-Stecker unter der Platine
- Durchlass um den Stecker: 9,0 × 9,0 mm
- flexibler P05-Dichteinsatz mit 5,6 × 1,6 mm Kabelschlitz; endgültig zusätzlich Epoxid/Verguss prüfen

## Normalbetrieb

- Kalibrierhaube entfernt
- sechs Lüftungsschlitze im Deckel offen
- Raumluft gelangt direkt zur Sensoroberseite
- Messzelle bleibt gegen Elektronikraum geschlossen; Kabeldurchlass wird abgedichtet

## Kalibrierbetrieb

- P07 montiert
- P04 TPU-Dichtung 25 % rechnerische Verpressung
- IN und OUT liegen links an der Haube
- interner Trennsteg erzwingt einen U-förmigen Gasweg mit 9,0 mm Umlenkspalt rechts

## Prüfpunkte für Daniel

1. Reale SEN0661-Platine in Fusion gegen die Dummys ausrichten.
2. Bestätigen, dass der Gravity-Stecker tatsächlich unter der Platine montiert ist und der 9,0 × 9,0-mm-Durchlass ausreicht.
3. Kabelbogen unterhalb des Steckers prüfen.
4. Zugang zu Sensorbefestigung und Kabel bei montiertem Waveshare prüfen.
5. Prüfen, ob die sechs Lüftungsschlitze ausreichend freie Messfläche bieten.
6. Haube, Dichtung und Schraubenpositionen auf Gasdichtheit prüfen.
7. Tüllenpositionen und Schlauchanschluss prüfen.
8. STEP-Dateien auf geschlossene Körper und korrekte Einheiten prüfen.
9. STL-Dateien im PrusaSlicer auf Supportfreiheit prüfen.

## Automatische Prüfung

`check_clearances.py` prüft 87 geometrische Bedingungen. Der lokale Erzeugungslauf V0.4 wurde mit **0 NOK** abgeschlossen.
