# AirMonitor Compact Revision V0.4

Diese Revision setzt die bestätigte Anordnung um:

- Sensorhalter **mittig links** über dem Waveshare-Board
- SEN0661-Platine mittig im Halter
- Gravity-Stecker **unterhalb der Platine**
- Kabelabgang nach unten
- kompakte Kalibrierhaube mit IN und OUT links

## Ordner

- `01_CAD_Global` – STEP im globalen Gehäusekoordinatensystem
- `02_CAD_Print` – einzelne STEP/STL in Druckausrichtung
- `03_Renders_Drawings` – Übersichtszeichnungen
- `compact_params.py` – zentrale Masse
- `check_clearances.py` – automatische Mass- und Kollisionsprüfung
- `build_compact_revision.py` – CAD-Erzeugung
- `CAD_COMPACT_SPEC_V0.4.md` – technische Spezifikation
- `PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.4.md` – Prüfauftrag

## Bauen

```bash
python check_clearances.py
python build_compact_revision.py
```

Führendes Format für Daniel ist STEP. STL dient nur der Druckprüfung.
