# Laminar AirMonitor HCHO - CAD-Konstruktionsspezifikation V0.7

## 1. Geltungsbereich

Diese Ausgabe korrigiert den bereits erzeugten V0.7-Stand, ohne eine neue Versionsnummer einzufuehren.

Verbindlich sind folgende Punkte:

- Die X-Position der Sensor- und Kalibriereinheit bleibt wie in V0.6.
- Die komplette Einheit wird nur auf der Y-Achse zentriert.
- Der Sensorpod bleibt auf der rechten Kabelseite 8,0 mm breiter.
- Die gedruckten TPU-Dichtungen P04 und P08 entfallen.
- Stattdessen werden drei geschlossene Kauf-O-Ringe aus EPDM 70 Shore A verwendet.
- Die O-Ring-Nuten liegen in P07 und P03. Der Deckel P02 bleibt ueberall 3,0 mm dick.

Alle Masse sind in mm. Globales Koordinatensystem: Ursprung an der aeusseren unteren Ecke von P01 ohne Flansch; X = lange Seite, Y = kurze Seite, Z = nach oben.

## 2. Korrektur gegenueber dem vorherigen V0.7-Stand

| ID | Merkmal | Vorheriger V0.7-Stand | Korrigierter V0.7-Stand |
|---|---|---|---|
| K01 | Sensorgruppe X | irrtuemlich +20,0 | 0,0; V0.6-X-Lage bleibt |
| K02 | Sensorgruppe Y | Mittelpunkt 57,0 | Mittelpunkt 56,0 |
| K03 | P03 Breite | 53,5 | 53,5; 8,0 rechts zusaetzlich |
| K04 | Dichtungen | gedrucktes TPU-D-Profil | geschlossene EPDM-Kauf-O-Ringe |
| K05 | Nuten | beidseitig im 3,0-mm-Deckel | P04 in P07; P08 in P03 |
| K06 | P07 Trennsteg | 3,0 | 5,0 fuer getrennte O-Ring-Nuten |
| K07 | P03 Oberkante | Z=54,0 | erhoehter Dichtrand bis Z=55,0 |
| K08 | Kabelschlitz | bis in den Dichtrand | endet bei Z=54,0; Dichtrand bleibt geschlossen |

## 3. Hauptgeometrie

### 3.1 P01 Gehaeuseboden

```text
Gehaeuse ohne Flansche = 208,0 x 112,0 x 55,0
Gesamtbreite mit Flanschen = 132,0
Wandstaerke = 2,8
Bodenstaerke = 2,8
```

Deckelbossen:

```text
(7,0 / 7,0)
(7,0 / 105,0)
(201,0 / 7,0)
(201,0 / 105,0)
Boss D9,0; Pilot D2,5
```

Waveshare-Aufnahmen:

```text
(24,0 / 25,0)
(169,0 / 25,0)
(24,0 / 87,0)
(169,0 / 87,0)
Raster = 145,0 x 62,0
Auflage Z = 9,6
```

### 3.2 Rechte Stirnwand

```text
ZERO = Y36,0 / Z41,0 / D3,0
SPAN = Y52,0 / Z41,0 / D3,0
ZERO-SPAN = 16,0 Mitte-Mitte
Platinenhalter = Y18,0/94,0; Z35,0/51,0
Halter-Lochbild = 76,0 x 16,0
```

### 3.3 Linke Stirnwand

```text
DC5521 = Y44,0 / Z27,5 / D11,2
Markierung = 24 V DC
Revisionsmarkierung = V0.7
```

## 4. Sensor- und Kalibriereinheit

### 4.1 Lage

```text
X-Verschiebung gegenueber V0.6 = 0,0
Y-Mittelpunkt = 56,0
```

### 4.2 P03 Sensorpod

```text
Koerper = X6,0..59,5 / Y15,0..97,0 / Z40,0..54,0
Koerperbreite X = 53,5
Koerperlaenge Y = 82,0
Wand/Boden = 3,0
Erhoehter Dichtrand = Z54,0..55,0
```

Sensorbefestigung:

```text
2 x D3,0
X = 16,3
Y = 48,5 / 63,5
Abstand = 15,0
```

Kabeldurchlass:

```text
X55,5..60,0
Y82,0..88,0
Z46,0..54,0
```

Der Kabeldurchlass endet unterhalb des Dichtrandes. P05 fuellt den Durchlass; die P08-Dichtlinie bleibt oben geschlossen.

### 4.3 P02 Deckel

```text
Deckel = 208,0 x 112,0 x 3,0
Lueftungsschlitze = X12,0; Y22,0 + 8,0*n; 33,0 x 4,0
Haubenschrauben = (27,0/9,0), (27,0/103,0)
Pod-Aufnahmen = (16,0/11,0), (42,0/11,0), (16,0/101,0), (42,0/101,0)
```

Im Deckel befinden sich keine O-Ring-Nuten. Dadurch bleibt seine Reststaerke 3,0 mm.

### 4.4 P07 Kalibrierhaube

```text
Grundplatte = X4,0..60,0 / Y3,2..108,8 / Z58,0..61,0
Grundplatte = 56,0 x 105,6 x 3,0
Haubenmittelpunkt = X32,0 / Y56,0
Trennsteg = Y49,5..54,5; Breite 5,0
```

Die Haubenunterseite liegt direkt auf der Deckeloberseite Z=58,0. Die beiden P04-Nuten sind in die Haubenunterseite eingelassen.

## 5. O-Ring-Konzept

### 5.1 Material und Nut

```text
Material = EPDM 70 Shore A
Schnurstaerke = 1,50
Nutbreite = 1,80
Nuttiefe = 1,10
Freie Hoehe = 1,50
Installierte Hoehe = 1,10
Verpressung = 0,40 = 26,7 %
Innenradius der Pfade = R8,0
```

### 5.2 Kaufteile

| Pos. | O-Ring | REAflon SKU | Verwendung | Lagerstatus bei Pruefung |
|---|---|---|---|---|
| P04A | D45,00 x 1,50 | H48761 | untere Kalibrierkammer | verfuegbar |
| P04B | D50,00 x 1,50 | H96773 | obere Kalibrierkammer | verfuegbar |
| P08 | D77,00 x 1,50 | H48789 | Sensorpod gegen Deckel | verfuegbar |

Bestelllinks:

- P04A: `https://reaflon.ch/products/o-ring-epdm-70-shore-schnurstarke-mm?variant=47875417440544`
- P04B: `https://reaflon.ch/products/o-ring-epdm-70-shore-schnurstarke-mm?variant=47875417604384`
- P08: `https://reaflon.ch/products/o-ring-epdm-70-shore-schnurstarke-mm?variant=47875418128672`

Der zuvor verlinkte Variantencode `47845525750048` ist D2,00 x 1,25 mm. Dieser Ring ist fuer die drei Flaechendichtungen zu klein und wird nicht verwendet.

### 5.3 Installierte Pfade

| Pos. | Mittelpunkt X/Y | Mittellinien-Aussenmass | Radius | rechnerische Dehnung |
|---|---|---|---|---|
| P04A | 32,0 / 33,5 | 46,0 x 34,0 | R8,0 | ca. +0,12 % |
| P04B | 32,0 / 74,5 | 45,8 x 42,0 | R8,0 | ca. +0,05 % |
| P08 | 32,75 / 56,0 | 51,2 x 79,0 | R8,0 | ca. +0,02 % |

Die Ringe werden in der Montage zu abgerundeten Rechtecken geformt. Die Pfadlaengen sind so ausgelegt, dass keine relevante Ueberdehnung entsteht.

## 6. Markierungen

```text
ZERO
SPAN
24 V DC
V0.7
IN
OUT
```

Markierungstiefe = 0,35.

## 7. Druck und Montage

| Teil | Materialvorschlag | Drucklage | Support |
|---|---|---|---|
| P01 | PETG/ASA gemaess Projektfreigabe | Boden auf Druckbett | nein |
| P02 | PETG/ASA | Aussenseite nach unten / vorhandene Druckausrichtung | nein |
| P03 | PETG/ASA | Boden auf Druckbett | nein |
| P05 | PETG/TPU nach Passversuch | flach | nein |
| P07 | PETG/ASA | Grundplatte auf Druckbett | nein |
| P04A/P04B/P08 | Kaufteile EPDM | nicht drucken | - |

Alle Teile passen in den Bauraum des Original Prusa MK4 von 250 x 210 x 220 mm.

## 8. Pruefung vor Installation

1. O-Ringe trocken und ohne Verdrehung einlegen.
2. Pruefen, dass alle Ringe vollstaendig in ihren Nuten liegen.
3. Haube gleichmaessig verschrauben; kein sichtbarer Spalt oder Verkanten.
4. P05 und Gravity-Kabel pruefen; P08-Dichtlinie darf nicht unterbrochen sein.
5. Nuten bei der Epoxidversiegelung abkleben.
6. Nach Montage Lecktest mit Nullgas/Frischluft durchfuehren.
7. Anschliessend Pruefgas aufgeben und Stabilitaet dokumentieren.
8. Rueckkehr zum Nullpunkt und moegliche Adsorption/Desorption dokumentieren.

## 9. Automatische CAD-Pruefung

Die parametrische Pruefung kontrolliert 56 Masse und Freiraeume, darunter:

- X-Lage unveraendert
- Y-Zentrierung
- O-Ring-Pfadlaengen
- Nutabmessungen und Verpressung
- Trennung der beiden P04-Nuten
- Restmaterial in P03 und P07
- Bauraum des Prusa MK4
- unerwartete Volumenueberschneidungen zwischen Druckteilen

## 10. Offene physische Pruefungen

- reale Passung der drei gelieferten O-Ringe
- Einfluss von Drucktoleranz und Epoxidschicht auf Nuttiefe
- Gasdichtheit bei Kalibrierfluss
- Nullpunktstabilitaet und Ausgasung
- Drehmoment der Haubenschrauben
- dauerhafte Formstabilitaet nach wiederholtem Oeffnen
