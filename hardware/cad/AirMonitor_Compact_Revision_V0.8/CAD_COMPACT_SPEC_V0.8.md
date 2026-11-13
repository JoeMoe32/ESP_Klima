# Laminar AirMonitor HCHO - CAD-Konstruktionsspezifikation V0.8

## Aktuelle Korrektur: supportfreie Kerbe

Die bisherige C-foermige Seitenfuehrung wird nicht verwendet. Ein geschlossener
horizontaler Kanal wuerde in der gewaehlten Druckorientierung eine Bruecke bzw.
Stuetzstruktur erfordern.

Der Deckel wird jetzt durch die durchgehende, 10 mm hohe Gehaeuseschulter
gefuehrt. Die Gehaeusemitte bleibt frei. Am vorderen rechten Rand befindet sich
nur eine kleine 45-Grad-Rastnase. Im Deckel liegt dazu eine einfache rechteckige
Kerbe, die **senkrecht gerade bis zur unteren Schuerzenkante offen ist**.

```text
Schiebeweg                 8,0 mm
Bedienansicht              links nach rechts
Rastnase X                 190,0 mm
Rastnasenbreite            6,0 mm
Rastnasenvorsprung         0,80 mm
Rastnase Z                 47,0..50,0 mm
Unterseite Rastnase        45 Grad
Kerbenbreite               7,40 mm
Kerbe Z                    45,0..50,6 mm
lokale Auslenkung Schuerze ca. 0,50 mm
```

## Druckbarkeit

- P01 steht auf seinem Boden.
- P02 liegt mit der sichtbaren flachen Oberseite auf dem Druckbett.
- Die Kerbe ist in dieser Drucklage nach oben offen.
- Es gibt keinen C-Kanal, keine geschlossene Nutdecke und keine horizontale
  Fanglippe, die frei in der Luft begonnen werden muesste.
- Die Rastnase am P01 besitzt eine 45-Grad-Unterseite.
- Slicer-Stuetzen sind fuer Deckelfuehrung und Rastung nicht vorgesehen.

## Unveraendert

Microtaster, Waveshare-Position, DC5521, Sensorpod, Pruefstation,
EPDM-O-Ringe, Y-Zentrierung und die 10-mm-Deckelueberdeckung bleiben erhalten.
Die Pruefstation bleibt bis zur physischen Kontrolle vorlaeufig.

## Physische Pruefung

- Deckelspiel und Verzug;
- lokale Federwirkung der 2,0-mm-Schuerze;
- Rastkraft und Loesbarkeit an der offenen Kerbe;
- mindestens 20 Oeffnungs-/Schliesszyklen;
- keine Weissbruchbildung oder Risse;
- Kabelreserve, O-Ring-Sitz und Gasdichtheit.

## Verbindliche No-C-Korrektur

An den beiden sichtbaren Randpositionen X=18,0 und X=190,0 gibt es keinen
C-foermigen Ausschnitt mehr. Die 8,0-mm-Aussparungen laufen vom Kerbendach
senkrecht bis ueber die physische Unterkante der 10-mm-Deckelschuerze. Ein
unterer horizontaler Ruecksteg ist geometrisch ausgeschlossen und wird im
CAD-Kernel mit einem Volumenpruefkoerper kontrolliert.
