# Laminar AirMonitor HCHO - CAD-Konstruktionsspezifikation V0.8

## Verbindliche Korrektur

Der funktionierende Absenk-/Schiebeablauf des frueheren V0.8-Entwurfs bleibt
erhalten. Geaendert wird nur die Druckbarkeit der seitlichen Fuehrung.

- Deckel +8,0 mm versetzt absenken.
- Vier Randzungen in innere Einfuehrtaschen setzen.
- Deckel 8,0 mm in die Endstellung schieben.
- Front/rechts verdeckt einrasten.

## Aussenform

```text
P01 ohne Flansche       208,0 x 112,0 x 55,0 mm
P01 Wand/Boden          3,2 mm
Aussenradius            R6,0 mm
Schulterbeginn          Z45,0 mm
Schulterruecksprung     2,8 mm
P02 Topplatte           3,0 mm
P02 Uebergriff          10,0 mm
P02 Schuerzenwand       2,5 mm
Schulterspiel           0,30 mm je Seite
```

## Fuehrung

```text
Positionen vorn/hinten  X18,0 und X190,0 mm
Schiebeweg              8,0 mm
Zungenbreite            6,0 mm
Normaler Vorsprung      0,90 mm
Normaler Anstieg        0,90 mm = 45 Grad
Nutquerschnitt          blindes Parallelogramm, 45 Grad
Aussenhaut an Nut       mindestens 1,65 mm
Aussenhaut Einfuehrung  mindestens 1,15 mm
```

Die Einfuehrtaschen sind nur zur Innenseite und zur unteren Schuerzenkante
offen. Die sichtbare Aussenwand bleibt geschlossen. Nach dem Einschieben liegen
die Zungen in den blinden Diagonalnuten und verhindern das vertikale Abheben.

## Rastung

Die vordere rechte Zunge bei X190 besitzt 0,55 mm mehr Vorsprung. Im normalen
Track entsteht ca. 0,20 mm lokale Auslenkung; in der tieferen Endtasche bleibt
ca. 0,20 mm Spiel. Die Rastung ist aussen nicht sichtbar.

## Druckbarkeit

P01 wird auf dem Boden gedruckt. Die Zungenunterseiten steigen nach aussen mit
45 Grad an. P02 wird mit der sichtbaren Oberseite auf dem Druckbett gedruckt.
Die Innennuten besitzen ausschliesslich diagonale 45-Grad-Flaechen; es gibt
keine waagerechte C-Kanal-Decke. Die Einfuehrtaschen reichen bis zur offenen
Schuerzenkante. Slicer-Stuetzen sind konstruktiv nicht vorgesehen.

## Unveraendert

Microtaster, Boardposition, DC5521, Sensorpod, Kalibrierhaube, EPDM-O-Ringe,
Y-Zentrierung und Markierungen bleiben unveraendert. Die Pruefstation bleibt bis
zur physischen Kontrolle vorlaeufig.

## Laengswandoeffnungen - verbindliche Druckkorrektur

```text
X-Bereich je Oeffnung    36,6..158,6 mm = 122,0 mm
Z-Bereich je Oeffnung    12,0..55,0 mm = 43,0 mm
Oberer Quertraeger       entfaellt vollstaendig
```

Beide Laengswandoeffnungen von P01 laufen bis zur oberen Gehaeusekante. Damit
gibt es keine 122 mm lange waagerechte Bruecke mehr, die beim Druck Stuetzen
oder eine unzulaessige freie Ueberbrueckung erfordern wuerde. Der violette
10-mm-Uebergriff gehoert ausschliesslich zum separat gedruckten Deckel P02.

## Korrektur des inneren Schulter-Quertraegers

Die Laengsoeffnung X=36,6..158,6 und Z=12,0..55,0 wird ueber die komplette
kombinierte Wandtiefe geschnitten. Vorne reicht der CAD-Schnitt von
Y=-0,50 bis Y=6,50 mm, hinten von Y=105,50 bis Y=112,50 mm. Damit sind sowohl
die aeussere Gehaeusewand als auch die versetzte Schulterwand entfernt; es
bleibt kein 122-mm-Streifen fuer einen freien Brueckendruck stehen.
