# Laminar AirMonitor HCHO - CAD-Konstruktionsspezifikation V0.8

## 1. Basis

V0.8 übernimmt Microtaster, Waveshare, Sensorpod, Prüfstation, EPDM-O-Ringe,
DC5521 und Markierungen aus V0.7. Die Microtasterposition ist bestätigt. Die
Prüfstation bleibt bis zur physischen Kontrolle vorläufig.

## 2. Neues Gehäuse

```text
Gehäuse ohne Flansche = 208,0 x 112,0 x 55,0
Wand/Boden = 3,2
unterer Außenradius = R6,0
Schulterbeginn = Z45,0
Schulterhöhe = 10,0
Schulterrücksprung = 2,0 je Seite
Schulterradius = R4,0
```

Es gibt keine zusätzlichen Deckelstützen oder Verschlusssäulen in der Mitte.
Die Waveshare-Abstandshalter bleiben nur für die Platinenmontage.

## 3. Überwurf-Schiebedeckel

```text
Deckel außen = 209,0 x 113,0
Topplatte = 3,0
Übergriff nach unten = 10,0
Deckelradius = R6,5
Schürzenwand = 2,2
nominelles Spiel = 0,30 je Seite
Schiebeweg = 8,0 nach -X
```

Vier 6,0 mm breite Laschen sind direkt in die obere Gehäuseschulter integriert.
Sie ragen 1,2 mm nach außen und besitzen eine 45°-Unterseite. Der Deckel hat
entsprechende, nach unten offene Einführungen und durchgehende Seitenschlitze.
Die Federzunge rastet am Ende am wandintegrierten Stift ein.

## 4. Druck

- P01 auf dem Boden drucken.
- P02 mit der sichtbaren ebenen Oberseite auf dem Druckbett drucken.
- Schürze und Innengeometrie bauen nach oben auf.
- Keine Slicer-Stützen vorgesehen; nur kurze kontrollierte Brücken an den Schlitzen.
- Außenkanten sind abgerundet.

## 5. Seitliche Öffnung

Der 10-mm-Deckelübergriff deckt den oberen Wandbereich. Die freie Öffnung ist:

```text
X = 36,6..158,6
Z = 12,0..45,0
122,0 x 33,0
```

## 6. Beibehaltene Microtaster

```text
ZERO = Y36,0 / Z26,0 / D3,0
SPAN = Y52,0 / Z26,0 / D3,0
Halter = Y18,0/94,0; Z20,0/36,0
Platine = 80,0 x 20,0 x 1,5
```

## 7. Physische Prüfung

- Absenken in +8-mm-Position ohne Verkanten;
- gleichzeitiger Eingriff aller vier Laschen;
- Schieben ohne Klemmen und ohne Klappern;
- sichere, lösbare Rastung;
- Kabelreserve und Kollisionsfreiheit von P03/P07;
- Verzug der 209 x 113 mm großen Deckelfläche;
- O-Ring-Sitz und Gasdichtheit der Prüfstation.
