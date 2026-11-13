# Laminar AirMonitor HCHO - CAD-Konstruktionsspezifikation V0.7

## 1. Verbindlicher Stand

Diese Ausgabe bleibt V0.7. Sie enthaelt die zuletzt freigegebenen Korrekturen und zusaetzlich:

- komplette ZERO-/SPAN-Platinenbaugruppe 15,0 mm tiefer;
- Schiebedeckel mit 8,0 mm kurzem Verriegelungsweg;
- Deckel wird von oben aufgesetzt, in offener Lage um +8,0 mm in X versetzt und danach 8,0 mm nach links (-X) geschoben;
- am Ende rastet eine federnde Zunge am vorderen Deckelrand auf einem Raststift ein;
- die Oberseite des Deckels bleibt ohne vorstehende Verschlussbauteile und wird beim Drucken auf das Druckbett gelegt;
- alle bisherigen O-Ring-, Sensor-, Hauben-, Waveshare- und Anschlusskorrekturen bleiben erhalten.

## 2. Gehaeuse und Deckel

```text
Gehaeuse ohne Flansche = 208,0 x 112,0 x 55,0
Gesamtbreite mit Flanschen = 132,0
Wand/Boden = 2,8
Deckel = 208,0 x 112,0 x 3,0
```

### 2.1 Deckelauflagen

Die vier bisherigen Eckpositionen bleiben als reine Auflagen erhalten:

```text
(7/7), (7/105), (201/7), (201/105)
Auflage D9,0
keine Deckelschraube
```

### 2.2 Schiebeverriegelung

Vier Pilzbolzen stehen auf separaten Stuetzpfosten:

```text
Bolzen XY = (75/7), (75/105), (170/7), (170/105)
Stuetzpfosten D8,0
Schaft D4,0 x 0,65
Kopf D7,0 x 0,75
```

Die Deckelunterseite hat blinde zweistufige Schluessellochbahnen:

```text
Schiebeweg = 8,0
Einsetzposition = Deckel +8,0 mm in X
Schliessrichtung = -X
Kopfkanal = 7,6 breit
Schaftkanal = 4,6 breit
Gesamttiefe = 1,65
untere Hals-Tiefe = 0,75
verbleibende obere Haut = 1,35
```

Die Oberseite ist plan. Die Taschen und Fuehrungen liegen auf der Unterseite.

### 2.3 Rastung

```text
Federzunge X=110,0..132,0 / Y=0,0..10,5
freie Zungenkante bei X=110,0
Restdicke Zunge = 1,20
Rastloch = X116,0 / Y2,2 / D3,4
Raststift = X116,0 / Y2,2 / Gesamthoehe 2,2
```

Beim Schliessen wird der Deckel 8,0 mm nach links geschoben. Der Raststift hebt die Zunge etwa 0,4 mm an und springt danach in das Rastloch. Zum Oeffnen die Zunge am vorderen Rand leicht anheben und den Deckel 8,0 mm nach rechts schieben; danach nach oben abheben.

## 3. Microtaster

Die gesamte Baugruppe wurde ohne Drehung 15,0 mm nach unten verschoben:

```text
ZERO = Y36,0 / Z26,0 / D3,0
SPAN = Y52,0 / Z26,0 / D3,0
ZERO-SPAN = 16,0 Mitte-Mitte
Halter = Y18,0/94,0; Z20,0/36,0
Lochbild = 76,0 x 16,0
Platine = 80,0 x 20,0 x 1,5
```

ZERO, SPAN, Platine, beide Schalter, vier Halter und beide Serviceoeffnungen wurden gemeinsam verschoben.

## 4. Sensor- und Kalibriereinheit

```text
X-Verschiebung gegenueber V0.6 = 0,0
Y-Mittelpunkt = 56,0
P03 = X6,0..59,5 / Y15,0..97,0 / Z40,0..54,0
P03 rechts 8,0 mm breiter
P07 Grundplatte = X4,0..60,0 / Y3,2..108,8 / Z58,0..61,0
```

In offener Deckellage (+8 mm X) bleibt P03 innerhalb des Gehaeuses; der kurze Schiebeweg kollidiert nicht mit dem Waveshare-Board.

## 5. EPDM-O-Ringe

```text
Material = EPDM 70 Shore A
Schnurstaerke = 1,50
Nutbreite = 1,80
Nuttiefe = 1,10
Verpressung = 0,40 = 26,7 %
Innenradius = R8,0
```

| Pos. | Ring | SKU | Verwendung |
|---|---:|---|---|
| P04A | D45,00 x 1,50 | H48761 | untere Kalibrierkammer |
| P04B | D50,00 x 1,50 | H96773 | obere Kalibrierkammer |
| P08 | D77,00 x 1,50 | H48789 | Sensorpod gegen Deckel |

P04-Nuten liegen in P07, P08-Nut im erhoehten P03-Rand. Im Deckel befinden sich keine O-Ring-Nuten.

## 6. Drucken und Montage

P02 wird mit der sichtbaren Oberseite auf dem Druckbett gedruckt. Dadurch sind die sichtbare Flaeche und der gesamte Rand plan; die blinden Schluessellochbahnen, Pod-/Haubenaufnahmen und die duenne Rastzunge werden auf der Oberseite des Druckaufbaus erzeugt.

Montagefolge:

1. P03, Sensor, Kabel und P05 am Deckel montieren.
2. P07 und O-Ringe montieren.
3. Deckel um +8,0 mm nach rechts versetzt von oben aufsetzen.
4. Pilzkoepfe in die grossen Einsetztaschen absenken.
5. Deckel 8,0 mm nach links schieben, bis die Zunge einrastet.
6. Sitz, Rastung, Kabelfreiraum und Dichtflaechen kontrollieren.

## 7. Pruefung

Automatisch kontrolliert werden unter anderem:

- Microtaster-Verschiebung -15,0 mm;
- Schiebeweg und Einsetzposition;
- Kopf-/Schaftspiel in den blinden Bahnen;
- verbleibende Deckelhaut;
- Auslenkung der Rastzunge;
- P03/P07-Freiraum in offener Deckellage;
- O-Ring-Pfadlaengen, Nutmasse und Verpressung;
- Prusa-MK4-Bauraum und unerwartete Volumenueberschneidungen.

Physisch zu pruefen:

- Rastkraft und Entriegelung mit dem realen PETG/ASA-Druck;
- Verschleiss nach wiederholtem Oeffnen;
- Kabelreserve fuer 8,0 mm Schiebeweg;
- reale O-Ring-Passung, Epoxidschicht und Leckrate;
- Nullpunkt, Pruefgas-Stabilitaet und Rueckkehr zum Nullpunkt.
