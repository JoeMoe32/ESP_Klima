# Laminar AirMonitor HCHO – CAD-Spezifikation V0.3 Compact

**Status:** Korrekturrevision zu V0.2 nach digitaler Prüfung (`../AirMonitor_Compact_Revision_V0.2/PRUEFBERICHT_V0.2_DIGITAL.md`). Freigabe durch Jonathan erteilt am 09.11.2026, Prüfung in Fusion 360 durch Daniel ausstehend.  
**Einheit:** mm. **Koordinatensystem:** wie V0.2 (Ursprung äussere untere Ecke P01, X lang, Y kurz, Z hoch).  
**Grundlage:** Alles, was hier nicht steht, gilt unverändert aus `CAD_COMPACT_SPEC_V0.2.md`.  
**Führende Quelle:** `compact_params.py` (Masse) → `build_compact_revision.py` (Geometrie). `check_clearances.py` prüft die Abstände ohne CAD-Kern und läuft vor jedem Build.

## 1 Änderungen V0.2 → V0.3

| ID | Teil | Befund V0.2 | V0.2 | V0.3 | Kennz. |
|---|---|---|---|---|---|
| K01 | P02/P03 | Pod-Bossen kollidieren mit Zungen, Pod-Wand, P08 | Bossen (14/44, 14/100) Z 51,0…55,0; Zungen Z 52,0…54,0 | Bossen (16,0/42,0, 12,0/102,0) Ø7,0 Z 52,0…55,0; Zungen X 13,0…45,0, Y 9,5…16,0 / 98,0…104,5, Z 50,0…52,0 | [Entscheidung] |
| K02 | P07 | Haubenboden geschlossen | Platte vollflächig | Bodenöffnung X 10,5…45,5; Y 18,5…51,5 und 54,5…95,5 | [Entscheidung] |
| K03 | P07 | Anschlüsse enden 0,85 vor Kammer | Bohrung ab Z 82,0 | Bohrung ab Kammerdecke − 1,0 | [Entscheidung] |
| K04 | P07/P04 | Bypass IN → OUT | eine Kammer | Trennsteg Y 51,5…54,5 über Deckelsteg zwischen Schlitz 4 und 5; P04 mit Quersteg (zwei Fenster). Gasweg: IN → Schlitze 1–4 → Sensorzelle → Schlitze 5–9 → OUT | [Entscheidung] |
| K05 | P04/P07 | Verpressung 88 % | Haube Z 58,15 | Haube Z 58,9; P04 1,2 → 0,9 = 25 % | [Entscheidung] |
| K06 | P08 | Verpressung 0 % | 1,0 im Spalt 1,0 | 1,3 im Spalt 1,0 = 23 % | [Entscheidung] |
| K07 | P05 | Stopfen füllt nur Z 48,0…51,2 | 4,0 × 6,0 × 3,2 | 4,0 × 6,0 × 8,0, Z 46,0…54,0; Kabelschlitz + Verguss | [Entscheidung] |
| K08 | P01 | Tasterplatine 0,8 in Rückwand und in Deckelbosse hinten rechts | Halter Y 32,0/108,0; ZERO/SPAN Y 50,0/66,0 | Halter Y 30,0/106,0; ZERO/SPAN Y 48,0/64,0; Platine Y 28,0…108,0 [Annahme: symmetrisch zum Lochbild] | [abgeleitet] |
| K09 | P01/P02 | Deckelbossen links 0,9 in Waveshare-Träger; rechts Kollision Tasterplatine/DC5521 | (8/8), (8/104), (200/8), (200/104) | (7,0/7,0), (7,0/105,0), (190,0/8,0), (190,0/104,0); Oberkante bündig Z 55,0 | [Entscheidung] |
| K10 | P02 | Haube ohne Gegenstück | Durchgangsloch Ø2,2 | Bosse Ø6,0 Z 53,0…55,0, Pilot Ø1,8 blind (M2 selbstschneidend, Insert offen) | [Entscheidung] |
| K11 | P02 | Druckdatei falsch herum | Platte oben | Druck-STEP/STL um 180° gedreht, Platte auf dem Bett | [Entscheidung] |
| K12 | P07 | Hülle 41,0 statt 38,0 | Spez. 38,0 | Spez. auf 41,0 nachgeführt (Tüllen unverändert) | [abgeleitet] |

## 2 Abstände (Ergebnis `check_clearances.py`, Mindestabstand 0,3)

| Paar | Abstand |
|---|---:|
| P01-Deckelbossen links ↔ Waveshare-Träger | 0,5 |
| P01-Deckelbossen rechts ↔ Waveshare-Träger | 1,3 |
| P01-Deckelbosse hinten rechts ↔ Tasterplatine | 3,2 |
| P01-Deckelbosse vorne rechts ↔ DC5521-Mutter [Annahme SW14] | 7,7 |
| P02-Pod-Bossen ↔ P03-Wand / P08 | 0,5 |
| P02-Pod-Bossen ↔ P01-Deckelbossen | ≥ 1,5 |
| P01-Deckelbossen ↔ P03-Zungen | ≥ 1,5 |
| Tasterplatine ↔ Rückwand innen | 1,2 |
| Haubenschraub-Bossen ↔ P03-Zungen (Z) | 1,0 |
| Waveshare ↔ Pod-Unterseite | 12,4 (unverändert) |
| SEN0661 ↔ Deckel | 0,6 (unverändert, kritisch) |

Die CAD-Kern-Prüfung (Schnittvolumen aller Teile untereinander und gegen die Dummys) läuft im Build in der GitHub Action; Ergebnis im Action-Log.

## 3 Neue Teilehüllen (Soll)

| ID | Teil | Hülle | Änderung |
|---|---|---|---|
| P01 | Unterteil | 208,0 × 132,0 × 55,0 | Bossen/Halter verlegt |
| P02 | Deckel | 208,0 × 112,0 × 6,0 (Z 52,0…58,0; Platte 3,0) | Bossen neu |
| P03 | Sensorpod | 45,5 × 95,0 × 14,0 (Y 9,5…104,5) | Zungen neu |
| P04 | Haubendichtung | 44,0 × 82,0 × 1,2 | zwei Fenster |
| P05 | Kabelstopfen | 4,0 × 6,0 × 8,0 | volle Höhe |
| P07 | Kalibrierhaube | 48,0 × 105,6 × 41,0 (Z 58,9…99,9) | Boden offen, Trennsteg, Anschlüsse offen |
| P08 | Pod-Deckeldichtung | 45,5 × 82,0 × 1,3 | dicker |

## 4 Offene Punkte für Daniel

1. Reale Tasterplatine: Lage der Taster zum Lochbild 76,0 × 16,0 messen. Die Annahme «symmetrisch» bestimmt Y der ZERO/SPAN-Bohrungen.
2. DC5521-Kontermutter real messen (Annahme SW14, 3,0 dick).
3. P03: Zungen kragen 6,5 aus (Z 50,0…52,0) → im Slicer Support oder 45°-Fase prüfen.
4. Trennsteg P07 + P04-Quersteg: Dichtlinie im Kalibrierbetrieb geschlossen?
5. Weiterhin alle Punkte aus V0.2 Abschnitt 10 (Waveshare real, Klemmenzugang, 0,6 mm Sensorabstand, Gravity-Kabel, Inserts).

## 5 Änderungsprotokoll

```text
V0.1: separate Sensorbox links, Gesamtlänge 263,0 mm.
V0.2 Compact: Sensorpod über linkem Waveshare-Bereich; Länge 208,0 mm.
V0.3 Compact: Korrekturen K01–K12 aus digitaler Prüfung V0.2 (Pod-Befestigung,
Kalibrierhaube mit Gasweg ohne Bypass, Dichtungsverpressung, Kabelstopfen,
Tasterplatine/Deckelbossen, Haubenbefestigung, Druckausrichtung Deckel).
```
