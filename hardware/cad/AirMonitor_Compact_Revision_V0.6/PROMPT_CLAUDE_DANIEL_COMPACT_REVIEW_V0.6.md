# Claude-Prüfprompt – AirMonitor Compact V0.6

Daniel, öffne zuerst in Fusion 360:

`01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.6.step`

## Prüfbereich

Prüfe ausschliesslich die rechte Rückwand der Revision V0.6. Sensorzelle, Kalibrierhaube, Waveshare, Deckel und übrige Gehäusegeometrie dürfen nicht neu konstruiert oder verschoben werden.

V0.6 korrigiert den Fehler aus V0.5:

- Nicht ZERO und SPAN werden zur Wandmitte verschoben.
- Die komplette Microtaster-Platine samt vier Haltern wird zentriert.
- ZERO und SPAN behalten ihre realen Positionen auf der Platine.
- DC5521 sitzt unterhalb und mittig zwischen beiden Microtastern.

## Sollwerte

```text
Platine:            80,0 × 20,0 × 1,5 mm
Platinenbereich:    Y 16,0…96,0 / Z 33,0…53,0 mm
Platinenmitte:      Y 56,0 mm
Halter Y:           18,0 / 94,0 mm
Halter Z:           35,0 / 51,0 mm
Lochbild:           76,0 × 16,0 mm
ZERO:               Y 36,0 / Z 41,0 mm
SPAN:               Y 52,0 / Z 41,0 mm
ZERO–SPAN:          16,0 mm
DC5521:             Y 44,0 / Z 27,5 mm
DC5521-Loch:        Ø11,2 mm
```

## In Fusion 360 prüfen

1. Platinenkörper und Lochbild sind auf der 112,0-mm-Rückwand zentriert.
2. Alle vier Halter liegen vollständig frei zwischen den beiden senkrechten Deckelschraubsäulen.
3. Kein Halter befindet sich hinter oder innerhalb einer Säule.
4. Platinenabstand zu den Säulenprojektionen beträgt beidseitig 3,5 mm.
5. Halteraussenkante zu den Säulenprojektionen beträgt beidseitig 3,0 mm.
6. ZERO liegt 20,0 mm ab Platinenkante Y und 8,0 mm über Platinenunterkante.
7. SPAN liegt 36,0 mm ab Platinenkante Y und 8,0 mm über Platinenunterkante.
8. DC5521 liegt in Y exakt mittig zwischen ZERO und SPAN und unterhalb der Schalter.
9. Kontermutter, Lötfahnen und Kabelbogen der realen DC5521-Buchse kollidieren nicht mit Platine oder Haltern.
10. Platine kann bei geöffnetem Deckel montiert und demontiert werden.
11. Keine andere Geometrie wurde gegenüber dem V0.3-Grundaufbau verändert.

Vergleiche zusätzlich:

- `03_Renders_Drawings/Drawing_RearPanel_Inside_V0.6.svg`
- `03_Renders_Drawings/Drawing_RearPanel_Outside_V0.6.svg`
- `REAR_PANEL_COORDS_V0.6.csv`

## Ergebnisformat

Für jeden Punkt:

| Prüfpunkt | Soll | Ist | Delta | Bewertung | Änderung nötig |
|---|---:|---:|---:|---|---|

Schlussbewertung exakt als:

- `freigegeben`
- `freigegeben mit Änderung`
- `nicht freigegeben`

Bei jeder Abweichung einen Fusion-360-Screenshot mit sichtbarem Messwert und Bezugskanten beifügen. Vor einer Geometrieänderung Daniels Bestätigung abwarten.
