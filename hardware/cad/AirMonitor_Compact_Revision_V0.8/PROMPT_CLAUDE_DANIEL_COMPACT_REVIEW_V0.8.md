# Daniel-/Claude-Pruefprompt - AirMonitor Compact V0.8

Die Konstruktion ist bereits umgesetzt. Bitte nur kontrollieren und Abweichungen
dokumentieren.

## Kritischer Punkt

Die Deckelfuehrung darf **kein C-Profil** enthalten. Die Rastkerbe im vorderen
Deckelrand muss vom Kerbendach senkrecht gerade bis zur unteren Schuerzenkante
offen sein. In der Drucklage mit der sichtbaren Oberseite auf dem Druckbett ist
diese Kerbe nach oben offen und benoetigt keine Stuetzstruktur.

## Soll

```text
Schulterfuehrung umlaufend
keine Deckelfixierung in Gehaeusemitte
keine geschlossenen horizontalen Seitenkanaele
Rastnase X190 / Breite 6,0 / Vorsprung 0,80
Rastnase Z47,0..50,0 / Unterseite 45 Grad
Kerbe Breite 7,40 / Z45,0..50,6 / bis Unterkante offen
Schiebeweg 8,0
```

Pruefen:

1. Kerbe ist wirklich unten offen und nicht C-foermig.
2. PrusaSlicer erzeugt fuer die Kerbe und Rastnase keine automatische Stuetze.
3. Deckel laesst sich ohne Bruch aufsetzen, einschieben und loesen.
4. Geschlossen ist die Aussenkontur optisch buendig.
5. Microtaster und Pruefstation wurden nicht verschoben.

Ergebnis: `freigegeben`, `freigegeben mit Aenderung` oder `nicht freigegeben`.
