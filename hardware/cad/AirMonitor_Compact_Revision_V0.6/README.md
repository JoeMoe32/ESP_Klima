# AirMonitor Compact Revision V0.6

V0.6 korrigiert nur die rechte Rückwand des bewährten V0.3-Grundaufbaus.

## Geändert

- Die komplette 80,0 × 20,0-mm-Microtaster-Platine wird mit ihrem 76,0 × 16,0-mm-Lochbild auf der Rückwand zentriert.
- Alle vier Halter werden gemeinsam verschoben und liegen frei zwischen den beiden senkrechten Deckelschraubsäulen.
- ZERO und SPAN bleiben an ihren gemessenen Positionen auf der Platine; sie werden nicht separat zur Wandmitte verschoben.
- DC5521 wird unterhalb der Microtaster und mittig zwischen ZERO und SPAN angeordnet.

## Unverändert

Sensorzelle, Kalibrierhaube, Waveshare, Deckel, Klemmenöffnungen und übrige Gehäusegeometrie bleiben unverändert.

## Start

1. Öffne in Fusion 360:
   `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.6.step`
2. Vergleiche die Rückwand mit:
   - `03_Renders_Drawings/Drawing_RearPanel_Inside_V0.6.svg`
   - `03_Renders_Drawings/Drawing_RearPanel_Outside_V0.6.svg`
3. Lies `CAD_COMPACT_SPEC_V0.6.md`.
4. Verwende für Daniel und Claude:
   `PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.6.md`

## Wichtige Koordinaten

```text
PCB:     Y 16,0…96,0 / Z 33,0…53,0 mm
Halter:  Y 18,0 / 94,0; Z 35,0 / 51,0 mm
ZERO:    Y 36,0 / Z 41,0 mm
SPAN:    Y 52,0 / Z 41,0 mm
DC5521:  Y 44,0 / Z 27,5 mm; Ø11,2 mm
```

Die GitHub-Action erzeugt STEP- und STL-Dateien automatisch aus `compact_params.py`, `check_clearances.py`, `build_compact_revision.py` und `build_v06.py`.
