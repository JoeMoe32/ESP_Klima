# Daniel-/Claude-Pruefprompt - AirMonitor Compact V0.8

Die Konstruktion ist umgesetzt. Bitte nur kontrollieren und Abweichungen mit
Soll/Ist/Delta dokumentieren.

## Kritisches Ziel

Die fruehere 8-mm-Schiebefunktion muss erhalten sein. Die alte rechteckige
C-Kanal-Geometrie darf jedoch nicht mehr vorhanden sein. Stattdessen muessen
vier verdeckte, blinde 45-Grad-Innennuten mit passenden Randzungen vorhanden
sein.

## Sollwerte

```text
Fuehrungen vorn/hinten  X18 und X190
Schiebeweg              8,0 mm
Zungenbreite            6,0 mm
Zungenprofil            0,90 mm Vorsprung / 0,90 mm Anstieg
Deckelschuerze          2,50 mm
Schulterruecksprung     2,80 mm
Spiel                   0,30 mm
sichtbare C-Fenster     keine
Endrastung              verdeckt vorne rechts X190
```

## Pruefen

1. Deckel +8 mm versetzt absenkbar.
2. Alle vier Zungen greifen gleichzeitig.
3. Nach 8 mm Schieben ist der Deckel vertikal gefangen.
4. PrusaSlicer fordert fuer Zungen, Nuten und Einfuehrtaschen keine Stuetzen.
5. Aussenwand des Deckels ist geschlossen und optisch buendig.
6. Mitte des Gehaeuses hat keine Deckelfixierung.
7. Microtaster und Pruefstation wurden nicht verschoben.
8. Rastung mindestens 20 Oeffnungs-/Schliesszyklen pruefen.

Ergebnis: `freigegeben`, `freigegeben mit Aenderung` oder `nicht freigegeben`.
