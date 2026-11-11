# Laminar AirMonitor HCHO – CAD Compact Specification V0.7

## 1. Scope

V0.7 is based on V0.6 and implements the handwritten corrections in `AirMonitor_V06_Massskizzen_1zu1.pdf`. In addition, P04 and P08 are redesigned for eSUN eTPU-95A as rounded D-profile seals seated in locating grooves.

All dimensions are in mm. Global coordinates: origin at the outer lower corner of P01 without flange; X = long axis, Y = short axis, Z = upward.

## 2. Changes from V0.6

| ID | Change | V0.7 value |
|---|---|---:|
| C01 | Right lid bosses moved to the edge like the left side | X=201; Y=7/105 |
| C02 | Waveshare standoffs moved to annotated coordinates | X=24/169; Y=25/87 |
| C03 | Complete sensor/calibration group moved toward centre | +20 in X |
| C04 | Sensor pod widened to the right | 45.5 -> 53.5 nominal |
| C05 | DC5521 moved to opposite end wall | left wall; Y=44; Z=27.5; D11.2 |
| C06 | P04 and P08 changed to rounded TPU D-profile | 3.0 wide x 2.0 high |
| C07 | Matching locating grooves added to lid | 3.4 wide x 0.6 deep |
| C08 | Physical markings updated | ZERO, SPAN, 24 V DC, V0.7, IN, OUT |

### Interpretation of the page-5 annotation

The red `46.3` is treated as a measured actual size of the V0.6 test/print. The explicit instruction `8 mm wider to the right` controls the CAD nominal change, therefore V0.7 uses 53.5 mm nominal width (45.5 + 8.0). Daniel must compare this with the real component before release.

## 3. P01 enclosure base

### 3.1 Lid bosses

```text
(7,7), (7,105), (201,7), (201,105)
Boss D9; pilot D2.5
```

### 3.2 Waveshare mounting

```text
Standoffs: (24,25), (169,25), (24,87), (169,87)
Pattern: 145 x 62
Standoff D9; pilot D2.5
Board support Z=9.6
Board body reference: 151.8 x 90 x 1.6
```

### 3.3 Right end wall

- ZERO: Y=36 / Z=41 / D3
- SPAN: Y=52 / Z=41 / D3
- PCB: 80 x 20 x 1.5
- Holder pattern: 76 x 16
- Engraved markings: `ZERO`, `SPAN`, depth 0.35
- No DC5521 bore on this wall.

### 3.4 Left end wall

- DC5521: Y=44 / Z=27.5 / D11.2
- Engraved marking: `24 V DC`, depth 0.35
- Engraved revision marking: `V0.7`

## 4. Sensor and calibration group

The complete group is shifted +20 in X.

### 4.1 P03 sensor pod

```text
Body: X=26.0..79.5 / Y=16.0..98.0 / Z=40.0..54.0
Nominal body width: 53.5
Body length: 82.0
Overall including tabs: 95.0
Wall/floor: 3.0
```

The extra 8.0 mm is added on the right/cable side. The sensor holes remain referenced to the former left edge. The cable slot moves with the new right wall.

### 4.2 P02 lid features

- Vent starts: X=32 instead of X=12
- Hood screws: X=47 / Y=10 and 104
- Pod mounts: X=36/62 / Y=12/102
- Right lid screw holes: X=201 / Y=7/105

### 4.3 P07 calibration hood

- Base plate: 56.0 x 105.6 x 3.0
- Overall height including ports: 41.0
- IN/OUT locations retained relative to the left plate edge
- Engraved `IN` and `OUT` markings on the roof

## 5. TPU seals and grooves

Material basis: **eSUN eTPU-95A, 1.75 mm**.

### 5.1 Seal cross-section

```text
Base width = 3.0
Overall height = 2.0
Flat underside
Rounded top edges, fillet R0.85
Rounded plan corners R4.0
```

The profile is D-shaped rather than a fully round O-ring so it can be printed flat without support.

### 5.2 Groove

```text
Groove width = 3.4
Groove depth = 0.6
Lateral clearance = 0.2 per side
```

The lid has a top groove for P04 and an underside groove for P08. Remaining lid material between both grooves is 1.8 mm.

### 5.3 Compression

| Seal | Free height | Installed height | Compression |
|---|---:|---:|---:|
| P04 hood/lid | 2.0 | 1.5 | 25% |
| P08 pod/lid | 2.0 | 1.6 | 20% |

### 5.4 Printing recommendation

- Print flat, no support
- 0.20 mm layer height
- 100% infill
- Low speed suitable for TPU 95A
- Dry filament before printing
- Test dimensions and airtightness before final assembly

FDM-printed TPU is not automatically gas-tight. The assembled calibration path must be leak-tested.

## 6. Verification status

Automated checks cover 58 dimensions/clearances and CAD-kernel part intersections. The generator stops on a failed check or unexpected intersection.

The following remain physical-test items:

1. Real Waveshare mounting-hole positions and connector clearances
2. DC5521 nut, solder tabs and cable bend on the left end wall
3. Fit of the 53.5 mm sensor pod around the real SEN0661 and Gravity cable
4. TPU groove fit, compression and removal without damage
5. Leak test under calibration flow
6. Readability of all engraved markings after printing

## 7. Deliverables

- Global STEP assembly and reference assembly with dummies
- Individual STEP files
- Print-oriented STEP and STL files
- `AirMonitor_V07_Massskizzen_1zu1.pdf`
- Review SVG drawings
- `DIMENSIONS.csv` and `V07_COORDINATES.csv`
- Claude/Daniel review prompt
