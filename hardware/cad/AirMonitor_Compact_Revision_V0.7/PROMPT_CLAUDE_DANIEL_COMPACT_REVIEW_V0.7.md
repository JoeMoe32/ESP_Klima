# Claude-Pruefprompt fuer Daniel - AirMonitor Compact V0.7

Oeffne zuerst:

`01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.7.step`

## Verbindliche Korrektur

Der fruehere V0.7-Stand verschob die Sensor-/Kalibriereinheit irrtuemlich in X. Das ist korrigiert:

```text
X-Verschiebung gegenueber V0.6 = 0,0 mm
Y-Mittelpunkt der Einheit = 56,0 mm
```

Bitte die X-Lage nicht erneut veraendern.

## O-Ringe

Drei geschlossene Kauf-O-Ringe aus EPDM 70 Shore A:

```text
P04A = D45,00 x 1,50 mm, SKU H48761
P04B = D50,00 x 1,50 mm, SKU H96773
P08  = D77,00 x 1,50 mm, SKU H48789
```

Gemeinsame Nutdaten:

```text
Nutbreite = 1,80 mm
Nuttiefe = 1,10 mm
Verpressung = 26,7 %
Pfadecken = R8,0
```

P04A/P04B liegen in der Unterseite von P07. P08 liegt im erhoehten Rand von P03. P02 hat keine O-Ring-Nut und bleibt 3,0 mm dick.

## Kontrollpunkte in Fusion 360

1. P03 links bei X=6,0 und P07 links bei X=4,0 bestaetigen.
2. Y-Mittelpunkt von P03, P07 und Lueftungsschlitzen = 56,0 bestaetigen.
3. P03 Koerper X=6,0..59,5 / Y=15,0..97,0 bestaetigen.
4. P03-Dichtrand Z=54,0..55,0 und geschlossene Dichtlinie ueber dem Kabelschlitz pruefen.
5. P04A- und P04B-Nuten auf P07-Unterseite pruefen; keine Ueberschneidung.
6. P08-Nut in P03 pruefen; mindestens 1,8 mm Material unter dem Nutgrund.
7. Deckelstaerke durchgehend 3,0 mm pruefen.
8. Schrauben, Haube, Deckel und Pod auf plane Anlage pruefen.
9. O-Ring-Referenzkoerper einblenden und Sitz kontrollieren.
10. STEP- und STL-Ausgaben mit `AirMonitor_V07_Massskizzen_1zu1.pdf` vergleichen.

## Ergebnisformat

Antworte mit einem der folgenden Ergebnisse:

- `freigegeben`
- `freigegeben mit Aenderung`
- `nicht freigegeben`

Bei jeder Abweichung angeben:

```text
Merkmal
Soll
Ist
Delta
Bewertung
Screenshot / Messung in Fusion 360
```
