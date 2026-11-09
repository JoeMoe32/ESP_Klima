# Laminar AirMonitor HCHO – Compact Revision V0.2

Diese Revision ist eine reproduzierbare, parametrische CAD-Neukonstruktion:

- separate Sensorbox links entfernt,
- SEN0661-Sensorpod oben links über dem Waveshare angeordnet,
- Gehäusehöhe unverändert,
- Gesamtlänge auf 208,0 mm reduziert,
- abnehmbare Kalibrierhaube mit IN/OUT,
- rechte Stirnwand mit DC5521 und ZERO/SPAN integriert.

## Dateien

1. `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.2.step` zuerst in Fusion 360 öffnen.
2. `01_CAD_Global/AirMonitor_Compact_Assembly_V0.2.step` enthält die Baugruppe ohne Kaufteil-Dummys.
3. `02_CAD_Print/` enthält die einzelnen STEP- und STL-Dateien in Druckausrichtung.
4. `CAD_COMPACT_SPEC_V0.2.md` enthält die verbindlichen Masse und Prüfpunkte.
5. `PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW.md` ist der Prüfauftrag für Daniel und Claude.
6. `build_compact_revision.py` erzeugt die CAD-Dateien reproduzierbar neu.

## Status

Noch keine Serien- oder Druckfreigabe. Daniel prüft insbesondere:

- reale Lage des Waveshare-Trägers und Lochbild 155 × 70 mm,
- Zugänglichkeit aller Klemmen,
- Restabstand SEN0661 zum Deckel,
- Gravity-Kabelbogen,
- Dichtlinien P04/P08,
- konkrete Heat-Set-Insert-Bohrungen.

Die GitHub Action `.github/workflows/build-airmonitor-compact-cad.yml` erzeugt die STEP-/STL-Dateien automatisch und committed sie auf diesen Branch.
