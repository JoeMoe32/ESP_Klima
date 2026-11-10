# Laminar AirMonitor HCHO – CAD Compact Specification V0.5

## Revision purpose

V0.5 corrects the earlier misunderstanding: the sensor holder and calibration assembly are **not** redesigned. The complete geometry from V0.3 is retained. Only the complete ZERO/SPAN microtaster PCB assembly on the right rear wall is translated as one rigid unit.

## Unchanged components

- Main enclosure: 208.0 × 112.0 × 55.0 mm
- Waveshare board position and all standoffs
- Sensor pod P03 and SEN0661 arrangement
- Calibration hood P07 and all seals
- Relay and control openings
- DC5521 bore, position and fastening principle
- Microtaster PCB dimensions, hole pattern, holder geometry and switch spacing

## Right rear wall – fixed geometry

| Item | Value | Status |
|---|---:|---|
| Microtaster PCB | 80.0 × 20.0 × 1.5 mm | measured |
| PCB mounting pattern | 76.0 × 16.0 mm | measured |
| PCB mounting holes | 4 × Ø2.0 mm | measured |
| ZERO–SPAN centre spacing | 16.0 mm | measured |
| Service openings | 2 × Ø3.0 mm | unchanged |
| DC5521 bore | Ø11.2 mm | unchanged |
| DC5521 centre | Y=15.0 / Z=27.5 mm | unchanged |

## V0.5 rigid translation

Compared with V0.3, the following elements are moved together by exactly the same vector:

1. Microtaster PCB dummy/reference
2. ZERO microtaster and service opening
3. SPAN microtaster and service opening
4. All four PCB holders
5. All four PCB pilot holes

```text
translation_y = -4.0 mm
translation_z = +13.0 mm
rotation = 0.0°
```

### Resulting coordinates

| Feature | V0.5 coordinates |
|---|---|
| PCB outer area | Y=24.0…104.0 / Z=33.0…53.0 mm |
| ZERO centre | Y=44.0 / Z=41.0 mm |
| SPAN centre | Y=60.0 / Z=41.0 mm |
| Holder centres Y | 26.0 / 102.0 mm |
| Holder centres Z | 35.0 / 51.0 mm |

Viewed from inside the enclosure, the PCB is in the upper part of the right rear wall and the unchanged DC5521 socket is below it on the right, matching the approved sketch.

## Verification requirements

- PCB, ZERO, SPAN, four holders and both service openings must remain a rigid assembly.
- ZERO and SPAN must not be repositioned independently.
- Maintain 76.0 × 16.0 mm mounting pattern and 16.0 mm switch spacing.
- Confirm DC5521 nut, solder tabs and wiring do not collide with the lower-right PCB corner.
- Confirm at least 0.3 mm CAD clearance; target practical clearance ≥1.0 mm.
- Confirm the PCB can still be installed and removed with the lid open.
- No other geometry may be changed in this revision.
