# AirMonitor Compact Revision V0.7

V0.7 implements the corrections from the annotated V0.6 1:1 drawings and introduces rounded eTPU-95A D-profile seals with locating grooves.

## Main changes

- Waveshare standoffs: X=24/169, Y=25/87
- Right lid bosses: 7 mm from right edge
- Sensor/calibration group: +20 mm toward enclosure centre
- Sensor pod: +8 mm width to the right, nominal 53.5 mm
- DC5521: moved to the opposite/left end wall
- P04/P08: 3.0 x 2.0 mm D-profile TPU seals
- Lid grooves: 3.4 x 0.6 mm
- Markings updated: ZERO, SPAN, 24 V DC, V0.7, IN, OUT

## Start here

1. Open `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.7.step` in Fusion 360.
2. Read `CAD_COMPACT_SPEC_V0.7.md`.
3. Review `AirMonitor_V07_Massskizzen_1zu1.pdf` at 100% print scale.
4. Check the two TPU parts separately in `02_CAD_Print/`.
5. Use `PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.7.md` for Daniel's review with Claude.

## Important

This is a prototype and not a print release. The real board, DC5521 nut, SEN0661, Gravity cable and calibration seal must be physically test-fitted. FDM TPU is not automatically gas-tight; perform a leak test.
