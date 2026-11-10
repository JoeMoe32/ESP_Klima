# Claude review prompt – AirMonitor Compact V0.5

Daniel, open the following file first in Fusion 360:

`01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.5.step`

## Scope

Review **only** the V0.5 change on the right rear wall. Do not redesign the sensor pod, calibration hood, Waveshare mounting, lid or other enclosure geometry.

The complete ZERO/SPAN PCB assembly was moved as one rigid group. The following elements must have exactly the same translation and no rotation:

- PCB 80.0 × 20.0 × 1.5 mm
- ZERO switch and Ø3.0 mm service opening
- SPAN switch and Ø3.0 mm service opening
- four PCB holders and their pilot holes

DC5521 remains unchanged.

## Target values

```text
PCB outer area: Y 24.0…104.0 / Z 33.0…53.0 mm
ZERO centre:    Y 44.0 / Z 41.0 mm
SPAN centre:    Y 60.0 / Z 41.0 mm
Holder Y:       26.0 / 102.0 mm
Holder Z:       35.0 / 51.0 mm
PCB pattern:    76.0 × 16.0 mm
ZERO–SPAN:      16.0 mm
DC5521 centre:  Y 15.0 / Z 27.5 mm, unchanged
DC5521 bore:    Ø11.2 mm, unchanged
```

## Check in Fusion 360

1. Confirm that PCB, ZERO, SPAN, service openings and all holders moved together.
2. Confirm no independent ZERO/SPAN offset was introduced.
3. Confirm the PCB remains parallel to the rear wall.
4. Confirm all four holes still form a 76.0 × 16.0 mm pattern.
5. Confirm DC5521, its bore and its centre did not move.
6. Model or inspect the DC5521 nut, solder tabs and cable bend; verify no collision with the PCB or lower-right holder.
7. Confirm practical assembly access and screwdriver access.
8. Compare the arrangement with `03_Renders_Drawings/Drawing_RearPanel_Inside_V0.5.svg`.

## Required result

Return one of:

- `freigegeben`
- `freigegeben mit Änderung`
- `nicht freigegeben`

For every deviation, provide Soll, Ist, Delta and a Fusion 360 screenshot with visible dimensions. Do not change geometry before Daniel approves the correction.
