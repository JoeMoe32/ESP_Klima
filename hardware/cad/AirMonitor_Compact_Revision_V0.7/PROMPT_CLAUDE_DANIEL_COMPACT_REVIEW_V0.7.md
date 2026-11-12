# Claude-/Daniel-Pruefprompt - AirMonitor Compact V0.7

Oeffne zuerst:

`01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.7.step`

## Verbindliche neue Punkte

1. ZERO und SPAN sowie Platine, vier Halter und beide Serviceoeffnungen sind gemeinsam 15,0 mm tiefer.
2. P02 ist kein Schraubdeckel mehr. Er wird von oben aufgesetzt und nur 8,0 mm verschoben.
3. Einsetzlage: Deckel +8,0 mm in X. Schliessen: 8,0 mm nach -X.
4. Vier Pilzkoepfe muessen in den blinden zweistufigen Schluessellochbahnen laufen.
5. Die sichtbare Oberseite des Deckels muss plan und ohne vorstehende Verschlussteile sein.
6. Am Ende muss die vordere Federzunge auf dem Raststift einrasten.
7. Zum Oeffnen muss die Zunge erreichbar sein, ohne P03, P07 oder die O-Ringe zu demontieren.

## Sollwerte

```text
ZERO/SPAN Z = 26,0
Halter Z = 20,0 / 36,0
Schiebeweg = 8,0
Bolzen XY = (75/7), (75/105), (170/7), (170/105)
Schaft = D4,0
Kopf = D7,0
Kopfkanal = 7,6
Schaftkanal = 4,6
Taschentiefe = 1,65
obere Resthaut = 1,35
Rastzunge = X110..132 / Y0..10,5 / Restdicke 1,20
Rastloch/-stift = X116 / Y2,2
```

## Pruefen

- Deckel in offener Lage +8 mm: P03/P07, Kabel und Board kollisionsfrei.
- Absenken ueber alle vier Pilzkoepfe gleichzeitig moeglich.
- Nach 8 mm Schieben kein vertikales Abheben ohne Entriegelung.
- Rastung deutlich, aber ohne Bruchgefahr; Wiederholbarkeit mindestens 20 Zyklen im Prototypentest.
- Deckeloberseite liegt in Druckorientierung vollstaendig plan auf dem Druckbett.
- Blindtaschen haben keine offene Oberseite.
- O-Ring-Nuten, Y-Zentrierung, DC5521, Waveshare und Markierungen unveraendert korrekt.

Ergebnis: `freigegeben`, `freigegeben mit Aenderung` oder `nicht freigegeben`. Abweichungen mit Soll/Ist/Delta und Screenshot dokumentieren.
