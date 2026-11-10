# Laminar AirMonitor HCHO – CAD Compact Specification V0.6

## Zweck der Revision

V0.6 korrigiert ausschliesslich die Anordnung an der rechten Rückwand.

Die vorherige V0.5 hatte ZERO und SPAN optisch zur Wandmitte verschoben. Das war nicht das gewünschte Prinzip. In V0.6 wird stattdessen die **komplette Platinenhalterung** zentriert. ZERO und SPAN bleiben an ihren gemessenen Positionen auf der Platine. Die DC5521-Buchse liegt darunter, mittig zwischen beiden Microtastern.

## Unverändert

- Gehäuse 208,0 × 112,0 × 55,0 mm
- Waveshare-Position und Standoffs
- Sensorzelle P03 und SEN0661-Anordnung
- Kalibrierhaube P07 und Dichtungen
- Deckel, Lüftungsschlitze und Klemmenöffnungen
- Microtaster-Platine 80,0 × 20,0 × 1,5 mm
- Lochbild 76,0 × 16,0 mm
- vier Halter, Halterdurchmesser und Befestigungsprinzip
- ZERO–SPAN-Mittenabstand 16,0 mm
- Serviceöffnungen Ø3,0 mm
- DC5521-Loch Ø11,2 mm und Z-Höhe 27,5 mm

## V0.6 – rechte Rückwand

### Platine und Halterung

Die Platine wird geometrisch auf der 112,0-mm-Rückwand zentriert:

| Merkmal | Koordinaten / Mass |
|---|---:|
| Platinen-Aussenbereich | Y = 16,0…96,0 / Z = 33,0…53,0 mm |
| Platinenmitte | Y = 56,0 mm |
| Halter Y | 18,0 / 94,0 mm |
| Halter Z | 35,0 / 51,0 mm |
| Halter-Lochbild | 76,0 × 16,0 mm |
| Abstand Platinenkante zur Säulenprojektion | je 3,5 mm |
| Abstand Halteraussenkante zur Säulenprojektion | je 3,0 mm |

Damit liegt keine Platinenhalterung mehr hinter einer der senkrechten Deckelschraubsäulen.

### ZERO und SPAN

ZERO und SPAN werden nicht unabhängig zentriert. Sie behalten ihre gemessenen Offsets auf der Platine:

| Merkmal | Wert |
|---|---:|
| ZERO-Mitte | Y = 36,0 / Z = 41,0 mm |
| SPAN-Mitte | Y = 52,0 / Z = 41,0 mm |
| ZERO ab Platinenkante Y | 20,0 mm |
| SPAN ab Platinenkante Y | 36,0 mm |
| ZERO/SPAN Abstand | 16,0 mm |
| Höhe ab Platinenunterkante | 8,0 mm |

### DC5521

Die DC5521-Buchse sitzt direkt unter dem Schalterpaar:

| Merkmal | Wert |
|---|---:|
| Mittelpunkt | Y = 44,0 / Z = 27,5 mm |
| Lochdurchmesser | Ø11,2 mm |
| Y-Lage | exakt mittig zwischen ZERO und SPAN |
| Abstand Lochkante DC zu Ø3-Serviceöffnungen | 6,4 mm |

## Prüfung und Unsicherheit

Der CAD-Check verwendet für die DC5521-Kontermutter die Annahme Ø16,0 mm und 3,0 mm Dicke. Der errechnete 3D-Abstand zur Platine ist ausreichend. Nicht vollständig durch Messwerte abgesichert sind jedoch Länge und Richtung der Lötfahnen sowie der reale Kabelbogen. Daniel muss diese Punkte am vorhandenen Bauteil oder in Fusion 360 prüfen.

## Freigabepunkte für Daniel

1. Platinenkörper und 76,0-mm-Lochbild liegen mittig zwischen den Säulen.
2. Alle vier Halter sind sichtbar, zugänglich und nicht von Säulen verdeckt.
3. ZERO und SPAN stimmen mit den realen Tastern auf der Platine überein.
4. DC5521 liegt unterhalb und mittig zwischen ZERO und SPAN.
5. Kontermutter, Lötfahnen und Kabel kollidieren nicht mit Platine oder Haltern.
6. Keine andere Geometrie wurde gegenüber dem V0.3-Grundaufbau verändert.
