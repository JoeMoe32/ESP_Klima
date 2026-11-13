from __future__ import annotations

from pathlib import Path
import re

R = Path(__file__).resolve().parent


def sub_once(text: str, pattern: str, repl: str, label: str) -> str:
    new, count = re.subn(pattern, repl, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one replacement, got {count}")
    return new


PARAMS = '''"""Laminar AirMonitor HCHO - Compact V0.7 corrected parameters (mm).

Current V0.7 state:
- sensor/calibration group keeps the proven V0.6 X position;
- complete group is centred on enclosure Y=56.0;
- sensor pod is 8.0 mm wider on the right/cable side;
- purchased EPDM 70 Shore A O-rings replace printed TPU seals;
- ZERO/SPAN PCB assembly is moved 15.0 mm downward as one rigid group;
- P02 is a short-travel sliding lid: place at +8 mm X, lower, slide 8 mm
  toward -X, and the front spring tongue snaps over a detent pin;
- the lid upper face has no protruding closure hardware and is the print-bed face.

Global coordinates: origin = outer lower corner of P01 without flange,
X = long axis, Y = short axis, Z = upward.
"""

# ---------- Main enclosure P01 ----------
L, W, H = 208.0, 112.0, 55.0
WALL = FLOOR = 2.8
FLANGE = 10.0
OPEN_X0, OPEN_X1, OPEN_Z = 36.6, 158.6, 12.0
WALL_MOUNT_HOLES = [(37.0, -5.0), (37.0, W + 5.0),
                    (L - 37.0, -5.0), (L - 37.0, W + 5.0)]
WALL_MOUNT_D = 4.5

# Existing corner supports remain, but no lid screws are used in V0.7.
LID_SUPPORTS = [(7.0, 7.0), (7.0, W - 7.0),
                (L - 7.0, 7.0), (L - 7.0, W - 7.0)]
LID_SUPPORT_D = 9.0

# Four mushroom studs retain the lid in blind keyhole tracks on its underside.
SLIDE_STUDS = [(75.0, 7.0), (75.0, W - 7.0),
               (170.0, 7.0), (170.0, W - 7.0)]
SLIDE_STUD_BASE_D = 8.0
SLIDE_TRAVEL = 8.0
SLIDE_OPEN_OFFSET_X = 8.0
SLIDE_CLOSE_DIRECTION = '-X'
SLIDE_STEM_D, SLIDE_STEM_H = 4.0, 0.65
SLIDE_HEAD_D, SLIDE_HEAD_H = 7.0, 0.75
SLIDE_HEAD_CLEAR_D = 7.6
SLIDE_STEM_CLEAR_W = 4.6
SLIDE_POCKET_DEPTH = 1.65
SLIDE_THROAT_DEPTH = 0.75

# Snap tongue is cut into the front edge of P02. It remains flush on top.
LATCH_TONGUE_X = (110.0, 132.0)   # free end at X=110, root at X=132
LATCH_TONGUE_Y = (0.0, 10.5)
LATCH_SLOT_W = 0.9
LATCH_TONGUE_SKIN = 1.20
LATCH_HOLE = (116.0, 2.2, 3.4)     # x, y, diameter through tongue
LATCH_PIN = (116.0, 2.2)           # x, y on top of front long wall
LATCH_PIN_SEGMENTS = [(3.0, 0.8), (2.2, 0.7), (1.2, 0.7)]  # d, h

# Waveshare mounting retained from approved correction.
STANDOFFS = [(24.0, 25.0), (169.0, 25.0),
             (24.0, 87.0), (169.0, 87.0)]
STANDOFF_D, STANDOFF_PILOT_D = 9.0, 2.5
BOARD_BOTTOM_Z, BOARD_TOP_Z = 9.6, 27.6
CARRIER = (10.0, 185.0, 11.0, 101.0, 9.6, 27.6)
PCB_WAVESHARE = (20.6, 172.4, 11.0, 101.0, 9.6, 11.2)

# ---------- Right end wall: ZERO / SPAN ----------
# Entire PCB, both switches, all four holders and both service holes moved -15 mm in Z.
BTN_ASSEMBLY_DZ = -15.0
BTN_HOLDER_Y = (18.0, 94.0)
BTN_HOLDER_Z = (20.0, 36.0)
BTN_HOLDER_D, BTN_HOLDER_PILOT_D, BTN_HOLDER_LEN = 5.0, 1.6, 6.0
BTN_PCB = (80.0, 20.0, 1.5)
ZERO = (36.0, 26.0, 3.0)
SPAN = (52.0, 26.0, 3.0)
BTN_MARK_Z = 32.5

# ---------- Left end wall: DC5521 ----------
DC5521 = (44.0, 27.5, 11.2)
DC_WALL = 'left'

# Markings (debossed)
MARK_DEPTH = 0.35
MARK_FONT = 'DejaVu Sans'
MARK_FONT_SIZE = 3.8

# ---------- Lid P02 ----------
LID_Z, LID_T = 55.0, 3.0
LID_TOP_FACE_FLAT = True
LID_PRINT_TOP_FACE_DOWN = True

# Sensor/calibration group remains at V0.6 X and is centred only in Y.
SENSOR_DX = 0.0
SENSOR_DY = -1.0
POD_EXTRA_X = 8.0
VENTS = [(12.0, 22.0 + 8.0 * i, 33.0, 4.0) for i in range(9)]
HOOD_SCREWS = [(27.0, 9.0), (27.0, 103.0)]
HOOD_SCREW_PILOT_D = 1.8
HOOD_SCREW_BOSS_D, HOOD_SCREW_BOSS_Z0 = 6.0, 53.0

POD_MOUNTS = [(16.0, 11.0), (42.0, 11.0),
              (16.0, 101.0), (42.0, 101.0)]
POD_BOSS_D, POD_BOSS_Z0 = 7.0, 52.0
POD_BOSS_PILOT_D, POD_BOSS_PILOT_TOP = 2.5, 56.0

# ---------- Sensor pod P03 ----------
POD = (6.0, 59.5, 15.0, 97.0, 40.0, 54.0)
POD_WALL = 3.0
POD_SEAL_RIM_TOP = 55.0
SENSOR_BOSSES = [(16.3, 48.5), (16.3, 63.5)]
SENSOR_BOSS_D, SENSOR_HOLE_D, SENSOR_BOSS_TOP = 5.6, 3.0, 46.0
GRAVITY_SLOT = (55.5, 60.0, 82.0, 88.0, 46.0, 54.0)
TONGUE_X = (13.0, 45.0)
TONGUE_Z = (50.0, 52.0)
TONGUE_FRONT_Y = (8.5, 15.0)
TONGUE_BACK_Y = (97.0, 103.5)
TONGUE_HOLE_D = 3.0

# ---------- Purchased EPDM O-rings and grooves ----------
ORING_MATERIAL = 'EPDM 70 Shore A'
ORING_SUPPLIER = 'REAflon Switzerland'
ORING_CORD = 1.50
ORING_GROOVE_W = 1.80
ORING_GROOVE_D = 1.10
ORING_COMPRESSION = (ORING_CORD - ORING_GROOVE_D) / ORING_CORD
ORING_CORNER_R = 8.0

P04A_RING = dict(name='P04A', id=45.0, cord=ORING_CORD,
                 cx=32.0, cy=33.5, cw=46.0, ch=34.0, r=8.0,
                 sku='H48761')
P04B_RING = dict(name='P04B', id=50.0, cord=ORING_CORD,
                 cx=32.0, cy=74.5, cw=45.8, ch=42.0, r=8.0,
                 sku='H96773')
P08_RING = dict(name='P08', id=77.0, cord=ORING_CORD,
                cx=32.75, cy=56.0, cw=51.2, ch=79.0, r=8.0,
                sku='H48789')

# ---------- Cable stop P05 ----------
P05 = (55.5, 59.5, 82.0, 88.0, 46.0, 54.0)

# ---------- Calibration hood P07 ----------
HOOD_Z0 = LID_Z + LID_T
HOOD_PLATE = (4.0, 60.0, 3.2, 108.8)
HOOD_PLATE_T = 3.0
HOOD_CENTER = (32.0, 56.0)
HOOD_OUT = ((48.0, 94.0), (36.0, 70.0), 22.0)
HOOD_IN = ((43.0, 89.0), (31.0, 65.0), 20.2)
HOOD_ROOF = (14.0, 21.0, 36.0, 70.0, 3.0)
HOOD_FLOOR_OPEN = (10.5, 53.5, 17.5, 94.5)
HOOD_DIVIDER_Y = (49.5, 54.5)
HOOD_PORTS = {'IN': (20.0, 29.0), 'OUT': (36.0, 85.0)}
HOOD_PORT_D = 2.0
HOOD_NOZZLE = [(8.0, 4.0), (7.0, 4.0), (6.0, 5.0)]

# ---------- Purchased-part reference dummies ----------
SEN_PCB = (12.8, 44.8, 45.0, 67.0, 46.0, 47.6)
SEN_TOP = (22.3, 35.3, 51.0, 61.0, 47.6, 50.0)
SEN_CON = (36.0, 44.0, 47.0, 55.0, 47.6, 54.4)
BTN_PCB_DUMMY = (L - WALL - BTN_HOLDER_LEN - BTN_PCB[2],
                 L - WALL - BTN_HOLDER_LEN,
                 sum(BTN_HOLDER_Y) / 2 - BTN_PCB[0] / 2,
                 sum(BTN_HOLDER_Y) / 2 + BTN_PCB[0] / 2,
                 sum(BTN_HOLDER_Z) / 2 - BTN_PCB[1] / 2,
                 sum(BTN_HOLDER_Z) / 2 + BTN_PCB[1] / 2)
'''

CHECKS = '''"""Numeric checks for AirMonitor Compact V0.7 sliding-lid revision."""
from __future__ import annotations

import math
import compact_params as C


def run() -> int:
    failures: list[str] = []
    passed = 0

    def check(name: str, condition: bool, detail: str = '') -> None:
        nonlocal passed
        if condition:
            passed += 1
        else:
            failures.append(f'{name}: {detail or "failed"}')

    def close(a: float, b: float, tol: float = 1e-6) -> bool:
        return abs(a - b) <= tol

    check('base length fits MK4', C.L <= 250.0, f'{C.L}')
    check('base total width fits MK4', C.W + 2 * C.FLANGE <= 210.0,
          f'{C.W + 2 * C.FLANGE}')
    check('base height fits MK4', C.H <= 220.0, f'{C.H}')
    check('wall positive', C.WALL > 0)
    check('floor positive', C.FLOOR > 0)
    check('long-wall opening ordered', C.OPEN_X0 < C.OPEN_X1)
    check('opening in base', 0 < C.OPEN_X0 < C.OPEN_X1 < C.L)
    check('opening height valid', 0 < C.OPEN_Z < C.H)

    px0, px1, py0, py1, pz0, pz1 = C.POD
    check('pod X left retained', close(px0, 6.0), f'{px0}')
    check('pod X widened right', close(px1, 59.5), f'{px1}')
    check('pod Y centred', close((py0 + py1) / 2, C.W / 2))
    hx0, hx1, hy0, hy1 = C.HOOD_PLATE
    check('hood X left retained', close(hx0, 4.0))
    check('hood X widened right', close(hx1, 60.0))
    check('hood Y centred', close((hy0 + hy1) / 2, C.W / 2))
    check('open-position pod remains inside X', px0 + C.SLIDE_OPEN_OFFSET_X >= C.WALL,
          f'{px0 + C.SLIDE_OPEN_OFFSET_X}')
    check('open-position hood remains inside X', hx0 + C.SLIDE_OPEN_OFFSET_X >= C.WALL,
          f'{hx0 + C.SLIDE_OPEN_OFFSET_X}')

    check('Waveshare X pattern', close(C.STANDOFFS[1][0] - C.STANDOFFS[0][0], 145.0))
    check('Waveshare Y pattern', close(C.STANDOFFS[2][1] - C.STANDOFFS[0][1], 62.0))
    check('ZERO-SPAN 16 mm', close(C.SPAN[0] - C.ZERO[0], 16.0))
    check('button assembly lowered 15 mm', close(C.BTN_ASSEMBLY_DZ, -15.0))
    check('ZERO/SPAN Z lowered', close(C.ZERO[1], 26.0) and close(C.SPAN[1], 26.0),
          f'{C.ZERO[1]}/{C.SPAN[1]}')
    check('holder Z lowered', C.BTN_HOLDER_Z == (20.0, 36.0), f'{C.BTN_HOLDER_Z}')
    pcb_z0 = sum(C.BTN_HOLDER_Z) / 2 - C.BTN_PCB[1] / 2
    pcb_z1 = sum(C.BTN_HOLDER_Z) / 2 + C.BTN_PCB[1] / 2
    check('button PCB inside wall height', C.FLOOR < pcb_z0 < pcb_z1 < C.H,
          f'{pcb_z0}..{pcb_z1}')
    check('DC bore valid', C.DC5521[2] > 0)

    check('lid top declared flat', C.LID_TOP_FACE_FLAT)
    check('lid print face is upper face', C.LID_PRINT_TOP_FACE_DOWN)
    check('slide travel 8 mm', close(C.SLIDE_TRAVEL, 8.0))
    check('slide closes toward -X', C.SLIDE_CLOSE_DIRECTION == '-X')
    check('head clears blind pocket', C.SLIDE_HEAD_CLEAR_D > C.SLIDE_HEAD_D)
    check('stem clears throat', C.SLIDE_STEM_CLEAR_W > C.SLIDE_STEM_D)
    check('stud height fits pocket', C.SLIDE_STEM_H + C.SLIDE_HEAD_H < C.SLIDE_POCKET_DEPTH)
    check('blind pocket leaves top skin', C.LID_T - C.SLIDE_POCKET_DEPTH >= 1.2,
          f'{C.LID_T - C.SLIDE_POCKET_DEPTH:.2f}')
    check('throat reaches stem', C.SLIDE_THROAT_DEPTH >= C.SLIDE_STEM_H)
    for i, (x, y) in enumerate(C.SLIDE_STUDS, 1):
        entry_x = x - C.SLIDE_TRAVEL
        r = C.SLIDE_HEAD_CLEAR_D / 2
        check(f'slide stud {i} entry inside lid X', entry_x - r >= 0 and x + r <= C.L,
              f'{entry_x-r:.2f}..{x+r:.2f}')
        check(f'slide stud {i} pocket inside lid Y', y - r >= 0 and y + r <= C.W,
              f'{y-r:.2f}..{y+r:.2f}')
    check('slide studs clear hood in X', min(x for x, _ in C.SLIDE_STUDS) - C.SLIDE_HEAD_CLEAR_D/2 > hx1,
          f'{min(x for x, _ in C.SLIDE_STUDS)} vs hood {hx1}')

    tx0, tx1 = C.LATCH_TONGUE_X
    ty0, ty1 = C.LATCH_TONGUE_Y
    hx, hy, hd = C.LATCH_HOLE
    pinx, piny = C.LATCH_PIN
    pin_h = sum(h for _, h in C.LATCH_PIN_SEGMENTS)
    tongue_under_z = C.LID_Z + C.LID_T - C.LATCH_TONGUE_SKIN
    interference = C.H + pin_h - tongue_under_z
    check('latch hole aligned with pin', close(hx, pinx) and close(hy, piny))
    check('latch tongue dimensions', tx0 < hx < tx1 and ty0 <= hy < ty1)
    check('latch tongue skin printable', 1.0 <= C.LATCH_TONGUE_SKIN <= 1.4)
    check('latch snap interference', 0.2 <= interference <= 0.6,
          f'{interference:.2f}')
    check('pin outside free edge in open position', pinx < tx0 + C.SLIDE_OPEN_OFFSET_X,
          f'pin {pinx}, free edge open {tx0 + C.SLIDE_OPEN_OFFSET_X}')
    check('latch pin based on front wall', 0 < piny < C.WALL + 0.5, f'{piny}')

    check('O-ring cord', close(C.ORING_CORD, 1.50))
    check('groove wider than cord', C.ORING_GROOVE_W > C.ORING_CORD)
    check('groove depth below cord', 0 < C.ORING_GROOVE_D < C.ORING_CORD)
    check('compression 20-30 percent', 0.20 <= C.ORING_COMPRESSION <= 0.30,
          f'{C.ORING_COMPRESSION:.3f}')
    check('hood material below groove', C.HOOD_PLATE_T - C.ORING_GROOVE_D >= 1.8)
    check('pod wall below groove', C.POD_WALL - C.ORING_GROOVE_D >= 1.8)
    check('lid remains un-grooved full thickness', close(C.LID_T, 3.0))
    check('hood contacts lid', close(C.HOOD_Z0, C.LID_Z + C.LID_T))
    check('pod rim contacts lid', close(C.POD_SEAL_RIM_TOP, C.LID_Z))

    def ring_metrics(ring: dict) -> tuple[float, float, float]:
        path = 2.0 * (ring['cw'] + ring['ch']) + (2.0 * math.pi - 8.0) * ring['r']
        free = math.pi * (ring['id'] + ring['cord'])
        return path, free, path / free - 1.0

    def channel_bounds(ring: dict, width: float) -> tuple[float, float, float, float]:
        return (ring['cx'] - ring['cw'] / 2 - width / 2,
                ring['cx'] + ring['cw'] / 2 + width / 2,
                ring['cy'] - ring['ch'] / 2 - width / 2,
                ring['cy'] + ring['ch'] / 2 + width / 2)

    for ring in (C.P04A_RING, C.P04B_RING, C.P08_RING):
        path, free, stretch = ring_metrics(ring)
        check(f"{ring['name']} path stretch", -0.005 <= stretch <= 0.03,
              f'{stretch*100:.2f}%')
        check(f"{ring['name']} radius", ring['r'] >= 3.0 * ring['cord'])

    for ring in (C.P04A_RING, C.P04B_RING):
        x0, x1, y0, y1 = channel_bounds(ring, C.ORING_GROOVE_W)
        check(f"{ring['name']} groove X in hood", hx0 <= x0 and x1 <= hx1)
        check(f"{ring['name']} groove Y in hood", hy0 <= y0 and y1 <= hy1)

    a = channel_bounds(C.P04A_RING, C.ORING_GROOVE_W)
    b = channel_bounds(C.P04B_RING, C.ORING_GROOVE_W)
    check('P04 groove separation', a[3] < b[2], f'{a[3]:.2f}/{b[2]:.2f}')
    check('divider width 5 mm', close(C.HOOD_DIVIDER_Y[1] - C.HOOD_DIVIDER_Y[0], 5.0))

    x0, x1, y0, y1 = channel_bounds(C.P08_RING, C.ORING_GROOVE_W)
    check('P08 groove X in pod', px0 <= x0 and x1 <= px1)
    check('P08 groove Y in pod', py0 <= y0 and y1 <= py1)

    fx0, fx1, fy0, fy1 = C.HOOD_FLOOR_OPEN
    d0, d1 = C.HOOD_DIVIDER_Y
    check('floor opening X in plate', hx0 < fx0 < fx1 < hx1)
    check('divider in opening range', fy0 < d0 < d1 < fy1)
    for name, (x, y) in C.HOOD_PORTS.items():
        check(f'{name} port in roof X', C.HOOD_ROOF[0] <= x <= C.HOOD_ROOF[0] + C.HOOD_ROOF[2])
        check(f'{name} port in roof Y', C.HOOD_ROOF[1] <= y <= C.HOOD_ROOF[1] + C.HOOD_ROOF[3])

    if failures:
        print(f'V0.7 checks: {passed} passed, {len(failures)} FAILED')
        for item in failures:
            print('FAIL', item)
        return 1
    print(f'V0.7 checks: {passed} passed, 0 failed')
    return 0


if __name__ == '__main__':
    raise SystemExit(run())
'''

SPEC = '''# Laminar AirMonitor HCHO - CAD-Konstruktionsspezifikation V0.7

## 1. Verbindlicher Stand

Diese Ausgabe bleibt V0.7. Sie enthaelt die zuletzt freigegebenen Korrekturen und zusaetzlich:

- komplette ZERO-/SPAN-Platinenbaugruppe 15,0 mm tiefer;
- Schiebedeckel mit 8,0 mm kurzem Verriegelungsweg;
- Deckel wird von oben aufgesetzt, in offener Lage um +8,0 mm in X versetzt und danach 8,0 mm nach links (-X) geschoben;
- am Ende rastet eine federnde Zunge am vorderen Deckelrand auf einem Raststift ein;
- die Oberseite des Deckels bleibt ohne vorstehende Verschlussbauteile und wird beim Drucken auf das Druckbett gelegt;
- alle bisherigen O-Ring-, Sensor-, Hauben-, Waveshare- und Anschlusskorrekturen bleiben erhalten.

## 2. Gehaeuse und Deckel

```text
Gehaeuse ohne Flansche = 208,0 x 112,0 x 55,0
Gesamtbreite mit Flanschen = 132,0
Wand/Boden = 2,8
Deckel = 208,0 x 112,0 x 3,0
```

### 2.1 Deckelauflagen

Die vier bisherigen Eckpositionen bleiben als reine Auflagen erhalten:

```text
(7/7), (7/105), (201/7), (201/105)
Auflage D9,0
keine Deckelschraube
```

### 2.2 Schiebeverriegelung

Vier Pilzbolzen stehen auf separaten Stuetzpfosten:

```text
Bolzen XY = (75/7), (75/105), (170/7), (170/105)
Stuetzpfosten D8,0
Schaft D4,0 x 0,65
Kopf D7,0 x 0,75
```

Die Deckelunterseite hat blinde zweistufige Schluessellochbahnen:

```text
Schiebeweg = 8,0
Einsetzposition = Deckel +8,0 mm in X
Schliessrichtung = -X
Kopfkanal = 7,6 breit
Schaftkanal = 4,6 breit
Gesamttiefe = 1,65
untere Hals-Tiefe = 0,75
verbleibende obere Haut = 1,35
```

Die Oberseite ist plan. Die Taschen und Fuehrungen liegen auf der Unterseite.

### 2.3 Rastung

```text
Federzunge X=110,0..132,0 / Y=0,0..10,5
freie Zungenkante bei X=110,0
Restdicke Zunge = 1,20
Rastloch = X116,0 / Y2,2 / D3,4
Raststift = X116,0 / Y2,2 / Gesamthoehe 2,2
```

Beim Schliessen wird der Deckel 8,0 mm nach links geschoben. Der Raststift hebt die Zunge etwa 0,4 mm an und springt danach in das Rastloch. Zum Oeffnen die Zunge am vorderen Rand leicht anheben und den Deckel 8,0 mm nach rechts schieben; danach nach oben abheben.

## 3. Microtaster

Die gesamte Baugruppe wurde ohne Drehung 15,0 mm nach unten verschoben:

```text
ZERO = Y36,0 / Z26,0 / D3,0
SPAN = Y52,0 / Z26,0 / D3,0
ZERO-SPAN = 16,0 Mitte-Mitte
Halter = Y18,0/94,0; Z20,0/36,0
Lochbild = 76,0 x 16,0
Platine = 80,0 x 20,0 x 1,5
```

ZERO, SPAN, Platine, beide Schalter, vier Halter und beide Serviceoeffnungen wurden gemeinsam verschoben.

## 4. Sensor- und Kalibriereinheit

```text
X-Verschiebung gegenueber V0.6 = 0,0
Y-Mittelpunkt = 56,0
P03 = X6,0..59,5 / Y15,0..97,0 / Z40,0..54,0
P03 rechts 8,0 mm breiter
P07 Grundplatte = X4,0..60,0 / Y3,2..108,8 / Z58,0..61,0
```

In offener Deckellage (+8 mm X) bleibt P03 innerhalb des Gehaeuses; der kurze Schiebeweg kollidiert nicht mit dem Waveshare-Board.

## 5. EPDM-O-Ringe

```text
Material = EPDM 70 Shore A
Schnurstaerke = 1,50
Nutbreite = 1,80
Nuttiefe = 1,10
Verpressung = 0,40 = 26,7 %
Innenradius = R8,0
```

| Pos. | Ring | SKU | Verwendung |
|---|---:|---|---|
| P04A | D45,00 x 1,50 | H48761 | untere Kalibrierkammer |
| P04B | D50,00 x 1,50 | H96773 | obere Kalibrierkammer |
| P08 | D77,00 x 1,50 | H48789 | Sensorpod gegen Deckel |

P04-Nuten liegen in P07, P08-Nut im erhoehten P03-Rand. Im Deckel befinden sich keine O-Ring-Nuten.

## 6. Drucken und Montage

P02 wird mit der sichtbaren Oberseite auf dem Druckbett gedruckt. Dadurch sind die sichtbare Flaeche und der gesamte Rand plan; die blinden Schluessellochbahnen, Pod-/Haubenaufnahmen und die duenne Rastzunge werden auf der Oberseite des Druckaufbaus erzeugt.

Montagefolge:

1. P03, Sensor, Kabel und P05 am Deckel montieren.
2. P07 und O-Ringe montieren.
3. Deckel um +8,0 mm nach rechts versetzt von oben aufsetzen.
4. Pilzkoepfe in die grossen Einsetztaschen absenken.
5. Deckel 8,0 mm nach links schieben, bis die Zunge einrastet.
6. Sitz, Rastung, Kabelfreiraum und Dichtflaechen kontrollieren.

## 7. Pruefung

Automatisch kontrolliert werden unter anderem:

- Microtaster-Verschiebung -15,0 mm;
- Schiebeweg und Einsetzposition;
- Kopf-/Schaftspiel in den blinden Bahnen;
- verbleibende Deckelhaut;
- Auslenkung der Rastzunge;
- P03/P07-Freiraum in offener Deckellage;
- O-Ring-Pfadlaengen, Nutmasse und Verpressung;
- Prusa-MK4-Bauraum und unerwartete Volumenueberschneidungen.

Physisch zu pruefen:

- Rastkraft und Entriegelung mit dem realen PETG/ASA-Druck;
- Verschleiss nach wiederholtem Oeffnen;
- Kabelreserve fuer 8,0 mm Schiebeweg;
- reale O-Ring-Passung, Epoxidschicht und Leckrate;
- Nullpunkt, Pruefgas-Stabilitaet und Rueckkehr zum Nullpunkt.
'''

README = '''# AirMonitor Compact Revision V0.7

Aktueller V0.7-Stand:

- Sensor-/Kalibriereinheit: V0.6-X-Lage, auf Y=56,0 zentriert
- Sensorpod rechts 8,0 mm breiter
- drei geschlossene EPDM-70-Kauf-O-Ringe
- ZERO-/SPAN-Baugruppe 15,0 mm tiefer
- P02 als kurzer Schiebedeckel mit 8,0 mm Weg und Rastzunge
- sichtbare Deckeloberseite plan; Drucklage mit Oberseite auf dem Druckbett

## Deckel bedienen

1. Zum Montieren Deckel +8 mm in X versetzt von oben aufsetzen.
2. Pilzkoepfe in die grossen Unterseitentaschen absenken.
3. Deckel 8 mm nach links schieben, bis die Zunge einrastet.
4. Zum Oeffnen die Zunge am vorderen Rand leicht anheben, Deckel 8 mm nach rechts schieben und abheben.

## Start

- Referenzbaugruppe: `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.7.step`
- Druckteile: `02_CAD_Print/`
- Massskizzen: `AirMonitor_V07_Massskizzen_1zu1.pdf`
- Spezifikation: `CAD_COMPACT_SPEC_V0.7.md`
- O-Ringe: `PURCHASED_O_RINGS.csv`
- Daniel/Claude: `PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.7.md`
'''

PROMPT = '''# Claude-/Daniel-Pruefprompt - AirMonitor Compact V0.7

Oeffne zuerst:

`01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.7.step`

## Verbindliche neue Punkte

1. ZERO und SPAN sowie Platine, vier Halter und beide Serviceoeffnungen sind gemeinsam 15,0 mm tiefer.
2. P02 ist kein Schraubdeckel mehr. Er wird von oben aufgesetzt und nur 8,0 mm verschoben.
3. Einsetzlage: Deckel +8,0 mm in X. Schliessen: 8,0 mm nach -X.
4. Vier Pilzkoepfe muessen in den blinden zweistufigen Schluessellochbahnen laufen.
5. Die sichtbare Oberseite des Deckels muss plan und ohne vorstehende Verschlussteile sein.
6. Am Ende muss die vordere Federzunge auf dem Raststift einrasten.
7. Zum Oeffnen muss die Zunge erreichbar sein, ohne P03, P07 oder die O-Ringe zu demontieren.

## Sollwerte

```text
ZERO/SPAN Z = 26,0
Halter Z = 20,0 / 36,0
Schiebeweg = 8,0
Bolzen XY = (75/7), (75/105), (170/7), (170/105)
Schaft = D4,0
Kopf = D7,0
Kopfkanal = 7,6
Schaftkanal = 4,6
Taschentiefe = 1,65
obere Resthaut = 1,35
Rastzunge = X110..132 / Y0..10,5 / Restdicke 1,20
Rastloch/-stift = X116 / Y2,2
```

## Pruefen

- Deckel in offener Lage +8 mm: P03/P07, Kabel und Board kollisionsfrei.
- Absenken ueber alle vier Pilzkoepfe gleichzeitig moeglich.
- Nach 8 mm Schieben kein vertikales Abheben ohne Entriegelung.
- Rastung deutlich, aber ohne Bruchgefahr; Wiederholbarkeit mindestens 20 Zyklen im Prototypentest.
- Deckeloberseite liegt in Druckorientierung vollstaendig plan auf dem Druckbett.
- Blindtaschen haben keine offene Oberseite.
- O-Ring-Nuten, Y-Zentrierung, DC5521, Waveshare und Markierungen unveraendert korrekt.

Ergebnis: `freigegeben`, `freigegeben mit Aenderung` oder `nicht freigegeben`. Abweichungen mit Soll/Ist/Delta und Screenshot dokumentieren.
'''

START = '''START HIER - AirMonitor Compact V0.7

1. Fusion 360:
   01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.7.step

2. Massskizzen:
   AirMonitor_V07_Massskizzen_1zu1.pdf

3. Neu pruefen:
   - Microtaster-Baugruppe 15 mm tiefer
   - Schiebedeckel: +8 mm aufsetzen, 8 mm nach links schliessen
   - vier blinde Schluessellochbahnen
   - Rastzunge und Raststift
   - sichtbare Deckeloberseite plan / Druckseite

4. Spezifikation:
   CAD_COMPACT_SPEC_V0.7.md

5. Claude:
   PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.7.md
'''


def patch_build() -> None:
    path = R / 'build_v07.py'
    text = path.read_text(encoding='utf-8')
    text = text.replace(
        'and uses purchased EPDM 70 Shore A O-rings instead of printed TPU seals.\n',
        'uses purchased EPDM 70 Shore A O-rings, lowers ZERO/SPAN by 15 mm,\n'
        'and adds a flat-top short-travel sliding lid with a snap tongue.\n')

    marker = "    return ring\n\n\ndef outside_text_right"
    helper = '''    return ring\n\n\ndef capsule_x(x0, x1, y, width, z0, h):\n    \"\"\"Capsule prism running in X, used for blind keyhole tracks.\"\"\"\n    if x1 < x0:\n        x0, x1 = x1, x0\n    r = width / 2\n    s = box(x0, y - r, z0, x1 - x0, width, h)\n    s = s.union(cz(x0, y, z0, width, h))\n    s = s.union(cz(x1, y, z0, width, h))\n    return s\n\n\ndef outside_text_right'''
    if marker not in text:
        raise RuntimeError('build_v07 helper insertion marker not found')
    text = text.replace(marker, helper, 1)

    text = sub_once(
        text,
        r"for x, y in C\.LID_BOSSES:.*?(?=for x, y in C\.STANDOFFS:)",
        '''for x, y in C.LID_SUPPORTS:\n    b = b.union(cz(x, y, floor, C.LID_SUPPORT_D, H - floor))\nfor x, y in C.SLIDE_STUDS:\n    b = b.union(cz(x, y, floor, C.SLIDE_STUD_BASE_D, H - floor))\n    b = b.union(cz(x, y, H, C.SLIDE_STEM_D, C.SLIDE_STEM_H))\n    b = b.union(cz(x, y, H + C.SLIDE_STEM_H, C.SLIDE_HEAD_D, C.SLIDE_HEAD_H))\n''',
        'replace lid supports')

    marker = '# DC5521 on left end wall.'
    latch_pin = '''# Snap detent pin on top of the front long wall.\npx, py = C.LATCH_PIN\npz = H\nfor d, hh in C.LATCH_PIN_SEGMENTS:\n    b = b.union(cz(px, py, pz, d, hh))\n    pz += hh\n\n'''
    if marker not in text:
        raise RuntimeError('DC marker not found')
    text = text.replace(marker, latch_pin + marker, 1)

    text = text.replace(
        "for text, y, z in (('ZERO', C.ZERO[0], 47.5), ('SPAN', C.SPAN[0], 47.5)):",
        "for text, y, z in (('ZERO', C.ZERO[0], C.BTN_MARK_Z), ('SPAN', C.SPAN[0], C.BTN_MARK_Z)):")

    new_lid = '''# ---------------- P02 sliding lid ----------------\nlz, lt = C.LID_Z, C.LID_T\nl = box(0, 0, lz, L, W, lt)\nfor x, y, lx, ly in C.VENTS:\n    l = l.cut(box(x, y, lz - 0.5, lx, ly, lt + 1.0))\nfor x, y in C.HOOD_SCREWS:\n    l = l.union(cz(x, y, C.HOOD_SCREW_BOSS_Z0,\n                   C.HOOD_SCREW_BOSS_D, lz - C.HOOD_SCREW_BOSS_Z0))\n    l = l.cut(cz(x, y, C.HOOD_SCREW_BOSS_Z0 + 0.5,\n                 C.HOOD_SCREW_PILOT_D,\n                 lz + lt - C.HOOD_SCREW_BOSS_Z0))\nfor x, y in C.POD_MOUNTS:\n    l = l.union(cz(x, y, C.POD_BOSS_Z0,\n                   C.POD_BOSS_D, lz - C.POD_BOSS_Z0))\n    l = l.cut(cz(x, y, C.POD_BOSS_Z0 - 0.1,\n                 C.POD_BOSS_PILOT_D,\n                 C.POD_BOSS_PILOT_TOP - C.POD_BOSS_Z0 + 0.1))\n\n# Four blind, two-level keyhole tracks. Top face remains closed and planar.\nfor x, y in C.SLIDE_STUDS:\n    entry_x = x - C.SLIDE_TRAVEL\n    head_z0 = lz + C.SLIDE_STEM_H - 0.05\n    head_depth = C.SLIDE_POCKET_DEPTH - (C.SLIDE_STEM_H - 0.05)\n    head_channel = capsule_x(entry_x, x, y, C.SLIDE_HEAD_CLEAR_D,\n                             head_z0, head_depth + 0.05)\n    throat = capsule_x(entry_x, x, y, C.SLIDE_STEM_CLEAR_W,\n                       lz - 0.1, C.SLIDE_THROAT_DEPTH + 0.2)\n    entry = cz(entry_x, y, lz - 0.1, C.SLIDE_HEAD_CLEAR_D,\n               C.SLIDE_POCKET_DEPTH + 0.2)\n    l = l.cut(head_channel.union(throat).union(entry))\n\n# Flush spring tongue at the front edge: top remains flat on the print bed.\ntx0, tx1 = C.LATCH_TONGUE_X\nty0, ty1 = C.LATCH_TONGUE_Y\nl = l.cut(box(tx0, ty0, lz - 0.1, tx1 - tx0, ty1 - ty0,\n              lt - C.LATCH_TONGUE_SKIN + 0.1))\nl = l.cut(box(tx0, ty1, lz - 0.2, tx1 - tx0, C.LATCH_SLOT_W, lt + 0.4))\nl = l.cut(box(tx0 - C.LATCH_SLOT_W, ty0, lz - 0.2,\n              C.LATCH_SLOT_W, ty1 - ty0 + C.LATCH_SLOT_W, lt + 0.4))\nlhx, lhy, lhd = C.LATCH_HOLE\nl = l.cut(cz(lhx, lhy, lz - 0.2, lhd, lt + 0.4))\n\n# Important: no lid-screw holes and no O-ring grooves in P02.\n\n# ---------------- P03 sensor pod ----------------'''
    text = sub_once(
        text,
        r"# ---------------- P02 lid ----------------.*?# ---------------- P03 sensor pod ----------------",
        new_lid,
        'replace P02 section')

    svg_marker = "print('Generated AirMonitor Compact V0.7 corrected O-ring package:', R)"
    slide_svg = '''slide_svg = f\'\'\'<svg xmlns="http://www.w3.org/2000/svg" width="1150" height="720" viewBox="-5 -8 220 132">\n{svg_style}\n<text class="t" x="0" y="-3">AirMonitor V0.7 - Schiebedeckel, Oberseite und verdeckte Unterseite [mm]</text>\n<rect class="wall" x="0" y="0" width="208" height="112"/>\n<text class="s" x="80" y="108">Oberseite plan; Druckseite</text>\n<g stroke="#24566f" fill="none" stroke-dasharray="2 1" stroke-width="0.5">\n  <path d="M67 7 H75"/><circle cx="67" cy="7" r="3.8"/><circle cx="75" cy="7" r="2.3"/>\n  <path d="M67 105 H75"/><circle cx="67" cy="105" r="3.8"/><circle cx="75" cy="105" r="2.3"/>\n  <path d="M162 7 H170"/><circle cx="162" cy="7" r="3.8"/><circle cx="170" cy="7" r="2.3"/>\n  <path d="M162 105 H170"/><circle cx="162" cy="105" r="3.8"/><circle cx="170" cy="105" r="2.3"/>\n  <rect x="110" y="0" width="22" height="10.5"/>\n  <circle cx="116" cy="2.2" r="1.7"/>\n</g>\n<line x1="145" y1="20" x2="137" y2="20" stroke="#b33" stroke-width="0.7"/>\n<text class="s" x="138" y="17">Schliessen: 8 mm nach -X, dann Rastung</text>\n<text class="s" x="82" y="12">blinde Schluessellochbahnen unten</text>\n<text class="s" x="108" y="15">Federzunge / Rastloch</text>\n</svg>\'\'\'\n(D / 'Drawing_Sliding_Lid_Flat_Top_V0.7.svg').write_text(slide_svg, encoding='utf-8')\n\n'''
    if svg_marker not in text:
        raise RuntimeError('build SVG marker not found')
    text = text.replace(svg_marker, slide_svg + svg_marker, 1)
    path.write_text(text, encoding='utf-8')


def patch_sketches() -> None:
    path = R / 'generate_mass_sketches_v07.py'
    text = path.read_text(encoding='utf-8')
    text = sub_once(
        text,
        r'"""Generate revised 1:1 engineering sketches for AirMonitor Compact V0\.7\..*?"""',
        '''"""Generate revised 1:1 engineering sketches for AirMonitor Compact V0.7.\n\nIncludes Y-centred sensor group, purchased EPDM O-rings, the complete\nZERO/SPAN assembly 15 mm lower, and the flat-top 8 mm sliding snap lid.\n"""''',
        'sketch docstring')

    page1 = '''def page1_base(c):\n    header(c, "P01 - Gehaeuseboden / Draufsicht innen",\n           "Eckauflagen bleiben; vier separate Pilzbolzen fuehren den 8-mm-Schiebedeckel")\n    ox, oy = 38 * mm, 39 * mm\n    c.rect(ox, oy - C.FLANGE * mm, C.L * mm, (C.W + 2 * C.FLANGE) * mm)\n    c.rect(ox, oy, C.L * mm, C.W * mm)\n    for x, y in C.WALL_MOUNT_HOLES:\n        c.circle(ox + x * mm, oy + y * mm, C.WALL_MOUNT_D / 2 * mm)\n    c.setStrokeColor(colors.black)\n    for x, y in C.LID_SUPPORTS:\n        c.circle(ox + x * mm, oy + y * mm, C.LID_SUPPORT_D / 2 * mm)\n    c.setStrokeColor(C_CENTER)\n    for x, y in C.SLIDE_STUDS:\n        c.circle(ox + x * mm, oy + y * mm, C.SLIDE_STUD_BASE_D / 2 * mm)\n        c.circle(ox + x * mm, oy + y * mm, C.SLIDE_HEAD_D / 2 * mm)\n    c.setStrokeColor(C_POD)\n    for x, y in C.STANDOFFS:\n        c.circle(ox + x * mm, oy + y * mm, C.STANDOFF_D / 2 * mm)\n        c.circle(ox + x * mm, oy + y * mm, C.STANDOFF_PILOT_D / 2 * mm)\n    c.setStrokeColor(colors.black)\n    dim_h(c, ox, ox + C.L * mm, oy - 17 * mm, "208")\n    dim_v(c, ox + C.L * mm + 9 * mm, oy - C.FLANGE * mm, oy + (C.W + C.FLANGE) * mm, "132")\n    label(c, 12 * mm, 27 * mm, "Waveshare: (24/25), (169/25), (24/87), (169/87); Raster 145 x 62.", 7)\n    label(c, 12 * mm, 22 * mm, "Schwarz: Eckauflagen D9 bei (7/7),(7/105),(201/7),(201/105); keine Deckelschrauben.", 7)\n    label(c, 12 * mm, 17 * mm, "Gruen: Schiebebolzen bei (75/7),(75/105),(170/7),(170/105); Kopf D7, Schaft D4.", 7)\n    footer(c, 1)\n'''
    text = sub_once(text, r'def page1_base\(c\):.*?(?=\ndef page2_walls)', page1, 'page1')

    page3 = '''def page3_endwalls(c):\n    header(c, "P01 - Stirnwaende",\n           "Rechts komplette ZERO-/SPAN-Baugruppe 15,0 mm tiefer; links DC5521")\n    ox, oy = 24 * mm, 61 * mm\n    label(c, ox, oy + 62 * mm, "Rechte Stirnwand / Aussenansicht", 8, True)\n    c.rect(ox, oy, C.W * mm, C.H * mm)\n    for text_label, (yy, zz, dd) in (("ZERO", C.ZERO), ("SPAN", C.SPAN)):\n        c.circle(ox + yy * mm, oy + zz * mm, dd / 2 * mm)\n        c.drawCentredString(ox + yy * mm, oy + (zz + 5) * mm, text_label)\n    c.saveState()\n    c.setDash(2, 2)\n    c.setStrokeColor(C_POD)\n    for yy in C.BTN_HOLDER_Y:\n        for zz in C.BTN_HOLDER_Z:\n            c.circle(ox + yy * mm, oy + zz * mm, 2.5 * mm)\n    c.restoreState()\n    dim_v(c, ox + C.W * mm + 7 * mm, oy, oy + C.ZERO[1] * mm, "26,0")\n\n    ox2 = 160 * mm\n    label(c, ox2, oy + 62 * mm, "Linke Stirnwand / Aussenansicht", 8, True)\n    c.rect(ox2, oy, C.W * mm, C.H * mm)\n    yy, zz, dd = C.DC5521\n    c.circle(ox2 + yy * mm, oy + zz * mm, dd / 2 * mm)\n    c.drawCentredString(ox2 + yy * mm, oy + (zz + 9) * mm, "24 V DC")\n    c.drawString(ox2 + 82 * mm, oy + 7 * mm, "V0.7")\n\n    label(c, 12 * mm, 29 * mm, "ZERO: Y=36 / Z=26 / D3. SPAN: Y=52 / Z=26 / D3. Abstand 16 Mitte-Mitte.", 7)\n    label(c, 12 * mm, 24 * mm, "Platine 80 x 20 x 1,5; Halter Y=18/94, Z=20/36; Lochbild 76 x 16.", 7)\n    label(c, 12 * mm, 19 * mm, "Platine, beide Schalter, vier Halter und beide Serviceoeffnungen gemeinsam -15,0 mm in Z.", 7, True)\n    footer(c, 3)\n'''
    text = sub_once(text, r'def page3_endwalls\(c\):.*?(?=\ndef page4_lid)', page3, 'page3')

    page4 = '''def page4_lid(c):\n    header(c, "P02 - Flacher Schiebedeckel / Draufsicht",\n           "Oberseite plan und Druckbettseite; verdeckte Schluessellochbahnen unten, 8 mm Schiebeweg")\n    ox, oy = 38 * mm, 47 * mm\n    c.rect(ox, oy, C.L * mm, C.W * mm)\n    c.setStrokeColor(C_POD)\n    for x, y, lx, ly in C.VENTS:\n        c.rect(ox + x * mm, oy + y * mm, lx * mm, ly * mm)\n    for x, y in C.POD_MOUNTS:\n        c.circle(ox + x * mm, oy + y * mm, 1.5 * mm)\n    c.setStrokeColor(C_HOOD)\n    for x, y in C.HOOD_SCREWS:\n        c.circle(ox + x * mm, oy + y * mm, 1.1 * mm)\n\n    c.saveState()\n    c.setDash(3, 2)\n    c.setLineWidth(0.55)\n    c.setStrokeColor(C_CENTER)\n    for x, y in C.SLIDE_STUDS:\n        entry = x - C.SLIDE_TRAVEL\n        c.line(ox + entry * mm, oy + y * mm, ox + x * mm, oy + y * mm)\n        c.circle(ox + entry * mm, oy + y * mm, C.SLIDE_HEAD_CLEAR_D / 2 * mm)\n        c.circle(ox + x * mm, oy + y * mm, C.SLIDE_STEM_CLEAR_W / 2 * mm)\n    tx0, tx1 = C.LATCH_TONGUE_X\n    ty0, ty1 = C.LATCH_TONGUE_Y\n    c.rect(ox + tx0 * mm, oy + ty0 * mm, (tx1 - tx0) * mm, (ty1 - ty0) * mm)\n    hx, hy, hd = C.LATCH_HOLE\n    c.circle(ox + hx * mm, oy + hy * mm, hd / 2 * mm)\n    c.restoreState()\n\n    c.saveState()\n    c.setStrokeColor(C_ORING)\n    c.setFillColor(C_ORING)\n    c.setLineWidth(0.8)\n    c.line(ox + 150 * mm, oy + 24 * mm, ox + 142 * mm, oy + 24 * mm)\n    c.line(ox + 142 * mm, oy + 24 * mm, ox + 145 * mm, oy + 26 * mm)\n    c.line(ox + 142 * mm, oy + 24 * mm, ox + 145 * mm, oy + 22 * mm)\n    c.restoreState()\n    label(c, ox + 151 * mm, oy + 21 * mm, "Schliessen: 8,0 mm nach -X", 7, True, C_ORING)\n    label(c, ox + 78 * mm, oy + 104 * mm, "sichtbare Oberseite plan / auf Druckbett", 7, True)\n    label(c, ox + 68 * mm, oy + 13 * mm, "gestrichelt = blinde Unterseitenbahnen", 6.5, False, C_CENTER)\n    label(c, ox + 105 * mm, oy + 15 * mm, "Federzunge + Rastloch", 6.5, False, C_CENTER)\n\n    label(c, 12 * mm, 29 * mm, "Aufsetzen: Deckel +8,0 mm in X versetzt absenken; alle vier Pilzkoepfe in die grossen Taschen.", 7)\n    label(c, 12 * mm, 24 * mm, "Danach 8,0 mm nach links schieben. Raststift X116/Y2,2 springt in D3,4-Rastloch.", 7)\n    label(c, 12 * mm, 19 * mm, "Kopfkanal 7,6; Schaftkanal 4,6; Taschentiefe 1,65; obere geschlossene Haut 1,35.", 7, True)\n    footer(c, 4)\n'''
    text = sub_once(text, r'def page4_lid\(c\):.*?(?=\ndef page5_pod)', page4, 'page4')

    page9 = '''def page9_assembly(c):\n    header(c, "V0.7 - Montage- und Verschlussschema",\n           "P03/P07 zuerst am flachen P02 montieren; danach Deckel kurz aufsetzen, schieben und einrasten")\n    cx = 82 * mm\n    y_p03 = 48 * mm\n    y_lid = 95 * mm\n    y_p07 = 122 * mm\n    width = 90 * mm\n\n    c.setFillColor(colors.HexColor("#EAF1F8")); c.setStrokeColor(C_POD)\n    c.rect(cx, y_p03, width, 24 * mm, stroke=1, fill=1)\n    label(c, cx + 3 * mm, y_p03 + 9 * mm, "P03 Sensorpod - P08-Nut", 8, True, C_POD)\n    c.setFillColor(colors.HexColor("#F6DAD8")); c.setStrokeColor(C_ORING)\n    c.rect(cx + 8 * mm, y_p03 + 21 * mm, width - 16 * mm, 3 * mm, stroke=1, fill=1)\n\n    c.setFillColor(colors.HexColor("#F2F2F2")); c.setStrokeColor(colors.black)\n    c.rect(cx - 8 * mm, y_lid, width + 16 * mm, 3 * mm, stroke=1, fill=1)\n    label(c, cx + 3 * mm, y_lid + 7 * mm, "P02 oben plan; Verriegelung unten", 8, True)\n\n    c.setFillColor(colors.HexColor("#F6DAD8")); c.setStrokeColor(C_ORING)\n    c.rect(cx + 9 * mm, y_p07 - 3 * mm, width / 2 - 14 * mm, 3 * mm, stroke=1, fill=1)\n    c.rect(cx + width / 2 + 5 * mm, y_p07 - 3 * mm, width / 2 - 14 * mm, 3 * mm, stroke=1, fill=1)\n    c.setFillColor(colors.HexColor("#F1E8F7")); c.setStrokeColor(C_HOOD)\n    c.rect(cx, y_p07, width, 25 * mm, stroke=1, fill=1)\n    label(c, cx + 3 * mm, y_p07 + 9 * mm, "P07 Kalibrierhaube - zwei P04-Nuten", 8, True, C_HOOD)\n\n    label(c, 18 * mm, 43 * mm, "Montagereihenfolge", 8, True)\n    steps = [\n        "P08, P03, Sensor, Gravity-Kabel und P05 am Deckel montieren.",\n        "P04A/P04B und P07 montieren; Dichtungen kontrollieren.",\n        "Deckel +8,0 mm nach rechts versetzt von oben auf P01 absenken.",\n        "Deckel 8,0 mm nach links schieben, bis die Federzunge einrastet.",\n        "Zum Oeffnen Zunge leicht anheben, 8,0 mm nach rechts schieben und Deckel abheben.",\n        "Danach Lecktest, Nullpunkt, Pruefgas und Nullpunktrueckkehr dokumentieren.",\n    ]\n    for i, text_line in enumerate(steps):\n        label(c, 22 * mm, (35 - 5.5 * i) * mm, f"{i+1}. {text_line}", 7)\n    footer(c, 9)\n'''
    text = sub_once(text, r'def page9_assembly\(c\):.*?(?=\ndef page10_summary)', page9, 'page9')

    page10 = '''def page10_summary(c):\n    header(c, "V0.7 - Freigabe- und Pruefliste",\n           "Aktueller Stand: EPDM-O-Ringe, Microtaster -15 mm und flacher Schiebedeckel mit Rastung")\n    label(c, 18 * mm, 160 * mm, "Umgesetzt", 8, True)\n    items = [\n        "Sensor-/Kalibriereinheit: V0.6-X-Lage, auf Y=56,0 zentriert.",\n        "P03 rechts 8,0 mm breiter; drei geschlossene EPDM-O-Ringe.",\n        "ZERO-/SPAN-Platine, Schalter, Halter und Serviceoeffnungen gemeinsam 15,0 mm tiefer.",\n        "P02 ohne Deckelschrauben; vier blinde zweistufige Schluessellochbahnen unten.",\n        "Deckel wird +8,0 mm versetzt aufgesetzt und 8,0 mm nach -X geschlossen.",\n        "Federzunge am vorderen Rand rastet auf Stift X116/Y2,2 ein.",\n        "Sichtbare Deckeloberseite ohne vorstehende Verschlussteile; diese Seite liegt beim Drucken unten.",\n        "O-Ring-Nuten bleiben in P03/P07; P02 bleibt ohne Dichtnut.",\n    ]\n    for i, text_line in enumerate(items):\n        label(c, 22 * mm, (151 - 8 * i) * mm, "- " + text_line, 7)\n\n    label(c, 18 * mm, 82 * mm, "Vor Montage pruefen", 8, True)\n    checks = [\n        "[ ] Alle vier Pilzkoepfe lassen sich in offener +8-mm-Lage gleichzeitig absenken.",\n        "[ ] Deckel schiebt ohne Klemmen 8 mm nach links und kann geschlossen nicht angehoben werden.",\n        "[ ] Rastung ist deutlich; Zunge laesst sich zum Oeffnen ohne Werkzeugbruch anheben.",\n        "[ ] Kabelreserve reicht fuer 8 mm Schiebeweg; P03/P07 kollidieren nicht.",\n        "[ ] Deckeloberseite liegt in Druckorientierung plan auf dem Druckbett.",\n        "[ ] O-Ringe, Nuten, Lecktest, Nullpunkt und Pruefgas-Stabilitaet sind dokumentiert.",\n    ]\n    for i, text_line in enumerate(checks):\n        label(c, 22 * mm, (73 - 8 * i) * mm, text_line, 7)\n    footer(c, 10, "CAD-Stand: V0.7 - Schiebedeckel / EPDM-O-Ringe")\n'''
    text = sub_once(text, r'def page10_summary\(c\):.*?(?=\ndef main)', page10, 'page10')
    path.write_text(text, encoding='utf-8')


def main() -> None:
    (R / 'compact_params.py').write_text(PARAMS, encoding='utf-8')
    (R / 'check_clearances.py').write_text(CHECKS, encoding='utf-8')
    patch_build()
    patch_sketches()
    (R / 'CAD_COMPACT_SPEC_V0.7.md').write_text(SPEC, encoding='utf-8')
    (R / 'README.md').write_text(README, encoding='utf-8')
    (R / 'PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.7.md').write_text(PROMPT, encoding='utf-8')
    (R / 'START_HIER_DANIEL_CLAUDE.txt').write_text(START, encoding='utf-8')
    print('Applied V0.7 micro-switch and sliding-lid patch')


if __name__ == '__main__':
    main()
