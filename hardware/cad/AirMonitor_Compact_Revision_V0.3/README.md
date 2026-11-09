# Laminar AirMonitor HCHO – Compact Revision V0.3

Korrekturrevision zu V0.2 nach der digitalen Prüfung (`../AirMonitor_Compact_Revision_V0.2/PRUEFBERICHT_V0.2_DIGITAL.md`).
Die Grundgeometrie bleibt gleich (208,0 × 132,0 × 55,0, Sensorpod oben links über dem Waveshare). Die Änderungen K01–K12 stehen in `CAD_COMPACT_SPEC_V0.3.md`.

## Dateien

| Datei | Zweck |
|---|---|
| `compact_params.py` | alle Masse, führend |
| `check_clearances.py` | Abstands-/Luftwegprüfung ohne CAD-Kern (`python check_clearances.py`) |
| `build_compact_revision.py` | erzeugt STEP/STL mit CadQuery 2.5.2, prüft vorher die Abstände und danach die Schnittvolumen |
| `CAD_COMPACT_SPEC_V0.3.md` | Änderungen gegenüber V0.2, Abstände, offene Punkte |
| `PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.3.md` | Prüfauftrag für Daniel und Claude |

Die Ordner `01_CAD_Global/`, `02_CAD_Print/`, `03_Renders_Drawings/` und `DIMENSIONS.csv` erzeugt die GitHub Action
`.github/workflows/build-airmonitor-compact-cad-v03.yml` beim Push auf den Branch `cad/airmonitor-compact-v0.3`.
Lokal ist kein CadQuery installiert (Python 3.15); STEP/STL liegen deshalb erst nach dem Action-Lauf vor.

## Status

Noch keine Druckfreigabe. Abstände rechnerisch geprüft (0 NOK), Schnittvolumen-Prüfung mit CAD-Kern erst im Action-Lauf.
