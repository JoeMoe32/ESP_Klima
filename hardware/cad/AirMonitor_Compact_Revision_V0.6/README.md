# AirMonitor Compact Revision V0.5

This revision is based on the verified V0.3 enclosure geometry.

## What changed

Only the complete ZERO/SPAN microtaster PCB assembly on the right rear wall was moved:

- PCB 80.0 × 20.0 × 1.5 mm
- ZERO and SPAN switches
- both Ø3.0 mm service openings
- all four PCB holders and pilot holes

The movement is rigid and common to all listed elements:

```text
ΔY = -4.0 mm
ΔZ = +13.0 mm
rotation = 0.0°
```

## What did not change

DC5521, sensor pod, calibration hood, Waveshare position, openings, lid and the remaining enclosure geometry are unchanged.

## Start here

1. Open `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.5.step` in Fusion 360.
2. Compare the inside view of the right rear wall with `03_Renders_Drawings/Drawing_RearPanel_Inside_V0.5.svg`.
3. Verify PCB mounting, ZERO/SPAN alignment, DC5521 nut clearance and cable access.
4. Read `CAD_COMPACT_SPEC_V0.5.md`.
5. Use `PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.5.md` for the review with Claude.

Generated STEP/STL files are produced automatically by GitHub Actions from `compact_params.py`, `build_compact_revision.py` and `build_v05.py`.
