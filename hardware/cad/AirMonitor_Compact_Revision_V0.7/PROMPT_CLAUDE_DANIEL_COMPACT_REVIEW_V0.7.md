# Claude review prompt – Laminar AirMonitor HCHO V0.7

Daniel, review the V0.7 CAD in Fusion 360. Begin with:

`01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.7.step`

Do not redesign parts before reporting the checks below.

## A. Verify the annotated corrections

1. Right lid bosses are at X=201 and Y=7/105, exactly 7 mm from the right edge.
2. Waveshare standoffs are at (24/25), (169/25), (24/87), (169/87), pattern 145 x 62.
3. Complete sensor/calibration group is shifted +20 mm in X.
4. P03 body is 53.5 mm wide and is widened only to the right.
5. Sensor holes retain their position relative to the old left edge.
6. DC5521 is removed from the right end wall and placed on the left end wall at Y=44 / Z=27.5 / D11.2.
7. ZERO/SPAN remain on the right end wall with the existing PCB holder principle.

## B. Verify TPU sealing design

1. P04 and P08 have a flat underside and rounded top (D-profile).
2. Free profile is 3.0 mm wide x 2.0 mm high.
3. Lid grooves are 3.4 mm wide x 0.6 mm deep.
4. P04 target compression is 25%; P08 target compression is 20%.
5. Top and underside grooves leave 1.8 mm lid material between them.
6. Rounded plan corners do not create thin or unsupported sections.
7. Both seals lie flat for support-free printing in eSUN eTPU-95A.

## C. Verify markings

- Right wall: ZERO and SPAN
- Left wall: 24 V DC and V0.7
- Hood roof: IN and OUT
- Engraving depth: 0.35 mm
- Text must remain legible with a 0.4 mm nozzle.

## D. Physical-risk checks

- Real Waveshare hole pattern and board envelope
- Screwdriver access to all terminals
- DC5521 nut, solder tabs and cable bend
- SEN0661 and Gravity cable fit in the 53.5 mm pod
- No cable pinch at the moved slot
- TPU seals remain captive in their grooves during assembly
- Hood and pod can be removed without tearing TPU
- Calibration path can be leak-tested

## Required response

Return one of:

- `freigegeben`
- `freigegeben mit Änderung`
- `nicht freigegeben`

For each deviation provide: component, Soll, Ist, Delta, collision/functional consequence, and a Fusion 360 screenshot with visible dimensions.

### Important interpretation

The annotation `46.3` is treated as a measured V0.6 actual size. The explicit `8 mm wider to the right` instruction defines the V0.7 CAD nominal width of 53.5 mm. Flag this if the real component suggests a different target.
