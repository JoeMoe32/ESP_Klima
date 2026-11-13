# Laminar AirMonitor HCHO - CAD-Konstruktionsspezifikation V0.8

## 1. Verbindlicher Stand

V0.8 übernimmt die bestätigte Microtaster-Baugruppe sowie Waveshare,
Sensorpod, Prüfstation, DC5521, Markierungen und EPDM-O-Ringe. Die
Prüfstation bleibt bis zur physischen Kontrolle vorläufig.

Die Deckelführung wurde nach der Sichtprüfung nochmals korrigiert:

- keine Deckelfixierung und keine zusätzliche Stabilisierung in der Mitte;
- alle Führungs- und Rastelemente liegen in den äußeren Randzonen;
- Deckel und Gehäuse haben dieselbe Außenkontur und denselben Radius;
- Einsetzseite des Deckels ist offen, damit der 10-mm-Übergriff beim Absenken
  nicht mit dem Gehäuse kollidiert;
- in der definierten Bedienansicht gleitet der Deckel von links nach rechts in
  die bündige Endstellung.

## 2. Gehäuse

```text
Gehäuse ohne Flansche = 208,0 x 112,0 x 55,0
Wand/Boden = 3,2
Außenradius = R6,0
Schulterbeginn = Z45,0
Schulterhöhe = 10,0
Schulterrücksprung Front/Heck/Rechts = 2,3
Schulterradius = R3,7
```

Die Einsetzseite links bleibt im oberen Bereich außen bündig. Es gibt keine
Deckelsäulen oder freistehenden Verschlusspfosten im Innenraum. Die vier
Waveshare-Abstandshalter bleiben ausschließlich als Platinenbefestigung.

## 3. Bündiger Überwurf-Schiebedeckel

```text
Deckel außen = 208,0 x 112,0
Topplatte = 3,0
Übergriff Front/Heck/Rechts = 10,0
Deckelradius = R6,0
Schürzenwand = 2,0
nominelles Spiel zur Schulter = 0,30 je Seite
kurzer Schiebeweg = 8,0
```

Die linke Einsetzseite der Schürze ist offen. Dadurch kann der Deckel in der
Serviceposition abgesenkt werden. Danach läuft er auf drei wandintegrierten
Führungen in die Endstellung:

```text
vorn: X18
hinten: X18 und X190
Endrastung vorn rechts: X184
```

Damit liegen alle Deckelbefestigungen höchstens 25 mm von einer Stirnseite
entfernt. Die komplette mittlere Gehäusezone bleibt frei.

## 4. Druckgerechte Konstruktion

- P01 mit dem Boden auf dem Druckbett.
- P02 mit der sichtbaren ebenen Oberseite auf dem Druckbett.
- Führungsnasen besitzen 45°-Unterseiten.
- Einführungen sind am Schürzenrand offen.
- Keine Slicer-Stützen vorgesehen.
- Nur drei kurze, kontrollierte Brücken in den seitlichen Führungsbahnen.
- Außenkontur im geschlossenen Zustand ohne 0,5-mm-Überstand: Deckel und
  Gehäuse verschmelzen optisch zu einer gemeinsamen Kontur.

## 5. Beibehaltene Punkte

```text
ZERO = Y36,0 / Z26,0 / D3,0
SPAN = Y52,0 / Z26,0 / D3,0
Halter = Y18,0/94,0; Z20,0/36,0
Platine = 80,0 x 20,0 x 1,5
Sensor-/Prüfgruppe X unverändert; Y-Mitte = 56,0
```

## 6. Physische Prüfung

- Absenken in der offenen Serviceposition ohne Kollision;
- gleichzeitiger Eingriff der drei Randführungen;
- Deckelmitte vollständig frei und ohne zusätzliche Stützen;
- leichtes Gleiten, bündiger Außenübergang und sichere Endrastung;
- Druck ohne Support, Brückenqualität und Verzug;
- Kabelreserve, O-Ring-Sitz und Gasdichtheit der Prüfstation.
