# AirMonitor Compact Revision V0.8

Aktueller V0.8-Stand:

- abgerundeter, aussen buendiger 10-mm-Ueberwurfdeckel
- Deckelfuehrung nur durch die umlaufende Gehaeuseschulter
- Gehaeusemitte ohne Deckelfixierung
- kein C-Kanal und keine geschlossene horizontale Fuehrungsnut
- eine 45-Grad-Rastnase am vorderen rechten Rand
- passende Deckelkerbe offen und senkrecht bis zur Unterkante
- Ziel: P01 und P02 ohne Slicer-Stuetzen drucken
- bestaetigte Microtasterposition und bestehende Pruefstation beibehalten

## Bedienung

Deckel in der Serviceposition um 8 mm versetzt aufsetzen und in der definierten
Bedienansicht von links nach rechts einschieben. Die Seitenwand federt ueber die
Rastnase und springt am Ende in die offene Kerbe. Zum Oeffnen die Schuerze an
der Kerbe leicht nach aussen ziehen und den Deckel zurueckschieben.

## Dateien

- Baugruppe: `01_CAD_Global/AirMonitor_Compact_Assembly_V0.8.step`
- Referenz: `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.8.step`
- Druckteile: `02_CAD_Print/`
- Massskizzen: `AirMonitor_V08_Massskizzen_1zu1.pdf`
- Spezifikation: `CAD_COMPACT_SPEC_V0.8.md`

## Korrektur der sichtbaren C-Ausschnitte

Die beiden bisherigen C-foermigen Seitenfenster sind entfernt. Bei X=18 mm
und X=190 mm laeuft die Aussparung jetzt senkrecht und ohne unteren Steg bis
zur unteren Deckelschuerzenkante. Die CAD-Erzeugung bricht ab, falls in diesem
Bereich noch Material verbleibt. Fuer eine cache-sichere Kontrolle liegt der
Deckel zusaetzlich als `P02_Compact_Lid_Print_NO_C_V0.8.stl` vor.
