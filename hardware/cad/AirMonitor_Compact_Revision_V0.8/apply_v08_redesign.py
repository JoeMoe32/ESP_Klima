from __future__ import annotations

from pathlib import Path
import re

R = Path(__file__).resolve().parent


def sub_once(text: str, pattern: str, repl: str, label: str) -> str:
    new, count = re.subn(pattern, repl, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one replacement, got {count}")
    return new


PARAMS = '''"""Laminar AirMonitor HCHO - Compact V0.8 parameters (mm).

V0.8 retains the confirmed V0.7 electronics, micro-switch and calibration
station geometry, but redesigns the outer enclosure and service lid:
- rounded external corners;
- slightly thicker 3.2 mm enclosure walls and floor;
- a continuous, recessed upper shoulder instead of lid-support columns;
- a cap lid that overlaps the enclosure by 10.0 mm;
- four wall-integrated, 45-degree printable slide lugs and through-slots;
- 8.0 mm slide travel and the existing end snap;
- no additional lid columns in the enclosure centre;
- support-free target orientation: base on its floor, lid on its visible top.

Global coordinates: origin = outer lower corner of P01 without flange,
X = long axis, Y = short axis, Z = upward.
"""

# ---------- Main enclosure P01 ----------
L, W, H = 208.0, 112.0, 55.0
WALL = FLOOR = 3.2
FLANGE = 10.0
BODY_CORNER_R = 6.0
SHOULDER_Z0 = 45.0
SHOULDER_H = H - SHOULDER_Z0
SHOULDER_INSET = 2.0
SHOULDER_CORNER_R = 4.0
NO_LID_COLUMNS = True

OPEN_X0, OPEN_X1 = 36.6, 158.6
OPEN_Z, OPEN_TOP_Z = 12.0, SHOULDER_Z0
WALL_MOUNT_HOLES = [(37.0, -5.0), (37.0, W + 5.0),
                    (L - 37.0, -5.0), (L - 37.0, W + 5.0)]
WALL_MOUNT_D = 4.5

# Waveshare mounting retained from V0.7.
STANDOFFS = [(24.0, 25.0), (169.0, 25.0),
             (24.0, 87.0), (169.0, 87.0)]
STANDOFF_D, STANDOFF_PILOT_D = 9.0, 2.5
BOARD_BOTTOM_Z, BOARD_TOP_Z = 9.6, 27.6
CARRIER = (10.0, 185.0, 11.0, 101.0, 9.6, 27.6)
PCB_WAVESHARE = (20.6, 172.4, 11.0, 101.0, 9.6, 11.2)

# Wall-integrated slide lugs. Lower face rises 1.2 mm over 1.2 mm = 45 degrees.
SLIDE_TRAVEL = 8.0
SLIDE_OPEN_OFFSET_X = 8.0
SLIDE_CLOSE_DIRECTION = '-X'
SIDE_LUG_X = (80.0, 172.0)
SIDE_LUG_WIDTH = 6.0
SIDE_LUG_PROJ = 1.2
SIDE_LUG_Z0 = 47.0
SIDE_LUG_Z1 = 50.0
SIDE_LUG_RAMP = 1.2

# Lid slot geometry, open at the skirt bottom in the insertion position.
SLOT_ENTRY_W = 7.6
SLOT_ENTRY_TOP_Z = 51.2
SLOT_TRACK_Z0 = 46.6
SLOT_TRACK_Z1 = 50.4
SLOT_TRACK_END_EXTRA = 3.8

# Snap tongue remains wall-based; no free-standing central pin/column.
LATCH_TONGUE_X = (110.0, 132.0)
LATCH_TONGUE_Y = (0.0, 10.5)
LATCH_SLOT_W = 0.9
LATCH_TONGUE_SKIN = 1.20
LATCH_HOLE = (116.0, 2.2, 3.4)
LATCH_PIN = (116.0, 2.2)
LATCH_PIN_SEGMENTS = [(3.0, 0.8), (2.2, 0.7), (1.2, 0.7)]
LATCH_SKIRT_NOTCH_X = (108.0, 134.0)

# ---------- Right end wall: ZERO / SPAN ----------
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

# ---------- Cap lid P02 ----------
LID_Z, LID_T = 55.0, 3.0
LID_OVERLAP = 10.0
LID_OUTSET = 0.5
LID_X0, LID_X1 = -LID_OUTSET, L + LID_OUTSET
LID_Y0, LID_Y1 = -LID_OUTSET, W + LID_OUTSET
LID_CORNER_R = 6.5
LID_SKIRT_W = 2.2
LID_IN_X0, LID_IN_X1 = LID_X0 + LID_SKIRT_W, LID_X1 - LID_SKIRT_W
LID_IN_Y0, LID_IN_Y1 = LID_Y0 + LID_SKIRT_W, LID_Y1 - LID_SKIRT_W
LID_TOP_FACE_FLAT = True
LID_PRINT_TOP_FACE_DOWN = True

# Sensor/calibration group remains at the confirmed V0.7 position.
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

CHECKS = '''"""Numeric checks for AirMonitor Compact V0.8."""
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

    # Printer envelope and main structure.
    check('base length fits MK4', C.L <= 250.0)
    check('base total width fits MK4', C.W + 2*C.FLANGE <= 210.0)
    check('base height fits MK4', C.H <= 220.0)
    check('lid footprint fits MK4', C.LID_X1-C.LID_X0 <= 250.0 and C.LID_Y1-C.LID_Y0 <= 210.0)
    check('lid print height fits MK4', C.LID_OVERLAP + C.LID_T <= 220.0)
    check('wall increased', C.WALL >= 3.0, f'{C.WALL}')
    check('floor increased', C.FLOOR >= 3.0, f'{C.FLOOR}')
    check('outer corners rounded', C.BODY_CORNER_R >= 4.0 and C.LID_CORNER_R >= 4.0)
    check('no lid columns', C.NO_LID_COLUMNS)
    check('shoulder height 10 mm', close(C.SHOULDER_H, 10.0))
    check('lid overlap 10 mm', close(C.LID_OVERLAP, 10.0))
    check('opening ordered', C.OPEN_X0 < C.OPEN_X1)
    check('opening ends below shoulder', close(C.OPEN_TOP_Z, C.SHOULDER_Z0))

    # Telescoping fit.
    sx0, sx1 = C.SHOULDER_INSET, C.L-C.SHOULDER_INSET
    sy0, sy1 = C.SHOULDER_INSET, C.W-C.SHOULDER_INSET
    clearances = (sx0-C.LID_IN_X0, C.LID_IN_X1-sx1,
                  sy0-C.LID_IN_Y0, C.LID_IN_Y1-sy1)
    for i, value in enumerate(clearances, 1):
        check(f'skirt clearance {i}', 0.20 <= value <= 0.45, f'{value:.3f}')
    check('shoulder wall overlap lower wall', C.WALL > C.SHOULDER_INSET,
          f'{C.WALL-C.SHOULDER_INSET:.2f}')
    check('lid upper face flat', C.LID_TOP_FACE_FLAT)
    check('lid top is print-bed face', C.LID_PRINT_TOP_FACE_DOWN)

    # Support-free slide details.
    check('slide travel 8 mm', close(C.SLIDE_TRAVEL, 8.0))
    check('slide closes toward -X', C.SLIDE_CLOSE_DIRECTION == '-X')
    check('lug ramp 45 degrees', close(C.SIDE_LUG_RAMP, C.SIDE_LUG_PROJ))
    check('slot entry wider than lug', C.SLOT_ENTRY_W > C.SIDE_LUG_WIDTH)
    check('slot track covers lug height', C.SLOT_TRACK_Z0 < C.SIDE_LUG_Z0 and C.SLOT_TRACK_Z1 > C.SIDE_LUG_Z1)
    check('entry open to skirt bottom', C.SLOT_ENTRY_TOP_Z > C.SIDE_LUG_Z1)
    check('lugs clear calibration group', min(C.SIDE_LUG_X)-C.SIDE_LUG_WIDTH/2 > C.HOOD_PLATE[1])

    # Snap tongue.
    tx0, tx1 = C.LATCH_TONGUE_X
    ty0, ty1 = C.LATCH_TONGUE_Y
    hx, hy, hd = C.LATCH_HOLE
    px, py = C.LATCH_PIN
    pin_h = sum(h for _, h in C.LATCH_PIN_SEGMENTS)
    tongue_under = C.LID_Z + C.LID_T - C.LATCH_TONGUE_SKIN
    interference = C.H + pin_h - tongue_under
    check('latch aligned', close(hx, px) and close(hy, py))
    check('latch hole in tongue', tx0 < hx < tx1 and ty0 <= hy <= ty1)
    check('tongue printable skin', 1.0 <= C.LATCH_TONGUE_SKIN <= 1.4)
    check('snap interference', 0.2 <= interference <= 0.6, f'{interference:.2f}')
    check('skirt notch covers tongue', C.LATCH_SKIRT_NOTCH_X[0] <= tx0 and C.LATCH_SKIRT_NOTCH_X[1] >= tx1)

    # Confirmed V0.7 geometry retained.
    check('ZERO-SPAN 16 mm', close(C.SPAN[0]-C.ZERO[0], 16.0))
    check('ZERO/SPAN height retained', close(C.ZERO[1], 26.0) and close(C.SPAN[1], 26.0))
    check('button holder pattern retained', C.BTN_HOLDER_Y == (18.0,94.0) and C.BTN_HOLDER_Z == (20.0,36.0))
    check('Waveshare X pattern', close(C.STANDOFFS[1][0]-C.STANDOFFS[0][0],145.0))
    check('Waveshare Y pattern', close(C.STANDOFFS[2][1]-C.STANDOFFS[0][1],62.0))

    # Sensor group closed and open positions inside the upper shoulder cavity.
    inner_x0 = C.SHOULDER_INSET + C.WALL
    inner_x1 = C.L - C.SHOULDER_INSET - C.WALL
    inner_y0 = C.SHOULDER_INSET + C.WALL
    inner_y1 = C.W - C.SHOULDER_INSET - C.WALL
    for name, geom in [('P03', C.POD), ('P07', (*C.HOOD_PLATE, 0, 0))]:
        gx0, gx1, gy0, gy1 = geom[:4]
        check(f'{name} closed inside shoulder X', inner_x0 <= gx0 and gx1 <= inner_x1,
              f'{gx0}..{gx1} vs {inner_x0}..{inner_x1}')
        check(f'{name} open inside shoulder X', inner_x0 <= gx0+C.SLIDE_OPEN_OFFSET_X and gx1+C.SLIDE_OPEN_OFFSET_X <= inner_x1)
        check(f'{name} inside shoulder Y', inner_y0 <= gy0 and gy1 <= inner_y1)

    # O-rings.
    check('O-ring cord', close(C.ORING_CORD,1.50))
    check('groove wider than cord', C.ORING_GROOVE_W > C.ORING_CORD)
    check('compression 20-30 percent', 0.20 <= C.ORING_COMPRESSION <= 0.30)
    def metrics(r):
        path = 2*(r['cw']+r['ch']) + (2*math.pi-8)*r['r']
        free = math.pi*(r['id']+r['cord'])
        return path/free-1
    for ring in (C.P04A_RING,C.P04B_RING,C.P08_RING):
        stretch = metrics(ring)
        check(f"{ring['name']} path stretch", -0.005 <= stretch <= 0.03, f'{stretch*100:.2f}%')
        check(f"{ring['name']} radius", ring['r'] >= 3*ring['cord'])

    if failures:
        print(f'V0.8 checks: {passed} passed, {len(failures)} FAILED')
        for item in failures:
            print('FAIL', item)
        return 1
    print(f'V0.8 checks: {passed} passed, 0 failed')
    return 0


if __name__ == '__main__':
    raise SystemExit(run())
'''

SPEC = '''# Laminar AirMonitor HCHO - CAD-Konstruktionsspezifikation V0.8

## 1. Freigegebene Basis

V0.8 baut auf dem zuletzt erzeugten V0.7-Stand auf. Unverändert übernommen werden:

- Microtaster-Platine, ZERO, SPAN und die vier Halter in der bestätigten tieferen Position;
- Waveshare-Aufnahmen und Anschlusspositionen;
- Sensorpod, Prüfstation/Kalibrierhaube und drei EPDM-O-Ringe;
- X-Lage der Sensorgruppe und Zentrierung auf Y=56,0;
- DC5521 sowie die Markierungen.

Die Prüfstation ist konstruktiv übernommen, bleibt aber bis zur physischen Kontrolle vorläufig.

## 2. V0.8 Gehäusekonzept

Der flache V0.7-Deckel wird durch einen abgerundeten Überwurfdeckel ersetzt. Er reicht im geschlossenen Zustand 10,0 mm über die Gehäusewände nach unten. Der Gehäuseboden erhält dafür eine um 2,0 mm zurückgesetzte obere Schulter.

```text
Gehäuse = 208,0 x 112,0 x 55,0 mm ohne Flansche
Wand/Boden = 3,2 mm
unterer Außenradius = R6,0
Schulterbeginn = Z45,0
Schulterhöhe = 10,0 mm
Schulterrücksprung = 2,0 mm je Seite
Schulterradius = R4,0
Deckeloberteil = 209,0 x 113,0 x 3,0 mm
Deckelübergriff = 10,0 mm
Deckelradius = R6,5
Deckel-Schürzenwand = 2,2 mm
umlaufendes nominelles Spiel = 0,30 mm je Seite
```

Es gibt keine zusätzlichen Deckelstützen oder Verschlusssäulen in der Gehäusemitte. Die vorhandenen Waveshare-Abstandshalter bleiben ausschließlich als Platinenbefestigung erhalten.

## 3. Schiebeführung ohne Stützmaterial

Vier Rast-/Führungslaschen sind direkt in die obere Gehäuseschulter integriert, je zwei an beiden Längsseiten.

```text
X = 80,0 / 172,0 mm
Laschenbreite = 6,0 mm
Ausladung = 1,2 mm
Z = 47,0..50,0 mm
Unterseite = 45°-Rampe
Schiebeweg = 8,0 mm
Schließrichtung = -X
```

Der Deckel hat durchgehende Seitenschlitze. In der um +8,0 mm versetzten Einsetzposition werden die Laschen durch die nach unten offenen Einführungen abgesenkt. Anschließend wird der Deckel 8,0 mm nach links geschoben. Die Laschen liegen dann im schmalen Führungsteil und verhindern das Abheben.

Die bekannte Federzunge am vorderen Rand bleibt erhalten und rastet am Ende auf dem wandintegrierten Stift ein. Unter der Zunge besitzt die Deckelschürze eine Bedienausnehmung.

## 4. Druckauslegung

- P01 wird auf dem Boden gedruckt.
- P02 wird mit der sichtbaren, ebenen Oberseite auf dem Druckbett gedruckt.
- Die Deckelschürze baut dabei nach oben auf.
- Führungsschlitze sind durchgehend und an der Einsetzseite offen.
- Die Gehäuselaschen haben eine 45°-Unterseite.
- Es sind keine Slicer-Stützen vorgesehen; kurze Brücken an den Führungsschlitzen sind konstruktiv begrenzt.
- Außenkanten sind abgerundet, scharfe Gehäuseecken entfallen.

## 5. Seitliche Öffnungen

Die bestehenden Längswandöffnungen bleiben 122,0 mm breit. Wegen des 10-mm-Deckelübergriffs endet die freie Bodenöffnung bei Z45,0.

```text
X = 36,6..158,6
Z = 12,0..45,0
freie Höhe = 33,0 mm
```

## 6. Beibehaltene Microtaster

```text
ZERO = Y36,0 / Z26,0 / D3,0
SPAN = Y52,0 / Z26,0 / D3,0
Halter = Y18,0/94,0; Z20,0/36,0
Platine = 80,0 x 20,0 x 1,5
```

## 7. Physische Prüfung

Vor Produktionsdruck und Installation sind zu prüfen:

1. Deckel lässt sich in der +8-mm-Position ohne Verkanten absenken.
2. Alle vier Wandlaschen greifen gleichzeitig in die Führungsschlitze.
3. Schiebeweg ist leichtgängig, aber ohne fühlbares Klappern.
4. Federzunge rastet sicher und lässt sich wieder lösen.
5. Keine Kollision von P03/P07, Kabel oder Waveshare beim 8-mm-Schieben.
6. Außenkanten, Schürzenwand und Ecken bleiben nach dem Druck formstabil.
7. O-Ring-Sitz, Prüfstation und Gasdichtheit werden praktisch kontrolliert.
'''

README = '''# AirMonitor Compact Revision V0.8

V0.8 ist die Gehäuse- und Deckelrevision auf Basis des bestätigten V0.7-Standes.

## Neu

- Deckel reicht 10 mm an den Außenwänden nach unten.
- Boden besitzt eine zurückgesetzte obere Schulter.
- Wand und Boden sind 3,2 mm dick.
- Außenkanten von Boden und Deckel sind abgerundet.
- Keine zusätzlichen Deckelstützen oder Verschlusssäulen in der Mitte.
- Vier wandintegrierte 45°-Laschen führen den Deckel über 8 mm.
- Deckel rastet am Ende mit der vorhandenen Federzunge ein.
- P01 und P02 sind für Druck ohne Slicer-Stützen ausgelegt.

## Beibehalten

Microtaster, Waveshare, DC5521, Sensorpod, Prüfstation und EPDM-O-Ringe entsprechen V0.7.

## Start

- Referenzbaugruppe: `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.8.step`
- Druckteile: `02_CAD_Print/`
- Maßskizzen: `AirMonitor_V08_Massskizzen_1zu1.pdf`
- Spezifikation: `CAD_COMPACT_SPEC_V0.8.md`
- Prüfprompt: `PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.8.md`
'''

PROMPT = '''# Claude-/Daniel-Prüfprompt - AirMonitor Compact V0.8

Öffne zuerst:

`01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.8.step`

## Unverändert übernehmen

Microtaster, Waveshare, Sensorpod, Prüfstation, O-Ringe, DC5521 und Markierungen entsprechen dem V0.7-Stand. Die Prüfstation ist noch praktisch zu prüfen, darf aber nicht ohne Befund umgestaltet werden.

## V0.8 prüfen

1. Deckel überlappt das Gehäuse exakt 10,0 mm.
2. Gehäuseschulter beginnt bei Z45,0 und ist je Seite 2,0 mm zurückgesetzt.
3. Deckel-/Schulterspiel liegt nominal bei 0,30 mm je Seite.
4. Boden und Wände sind 3,2 mm dick.
5. Gehäuseecken R6,0 und Deckelecken R6,5 sind sauber und ohne scharfe Kanten.
6. Es gibt keine zusätzlichen Deckelstützen oder Verschlusssäulen in der Mitte.
7. Vier Wandlaschen bei X80/X172 greifen in die Seitenschlitze.
8. Deckel wird +8 mm versetzt abgesenkt und 8 mm nach -X geschlossen.
9. 45°-Laschen, Seitenschlitze und Druckorientierungen benötigen keine Slicer-Stützen.
10. Federzunge rastet am Ende und bleibt von außen lösbar.
11. P03, P07, Kabel und Board bleiben in offener und geschlossener Lage kollisionsfrei.

## Physischer Prototypentest

- Passung mit PETG/ASA mindestens 20 Öffnungszyklen;
- Rastkraft und Verschleiß;
- Verzug der 209 x 113 mm großen Deckelfläche;
- Schürzenwand und abgerundete Ecken;
- Gasdichtheit und O-Ring-Kompression.

Ergebnis: `freigegeben`, `freigegeben mit Änderung` oder `nicht freigegeben`. Abweichungen mit Soll/Ist/Delta und Screenshot dokumentieren.
'''

START = '''START HIER - AirMonitor Compact V0.8

1. Fusion 360:
   01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.8.step

2. Maßskizzen:
   AirMonitor_V08_Massskizzen_1zu1.pdf

3. Neu prüfen:
   - 10 mm Deckelübergriff
   - abgerundete Außenkanten
   - 3,2 mm Wand/Boden
   - keine Deckelsäulen in der Mitte
   - vier Wandlaschen und 8 mm Schiebeweg
   - Rastzunge
   - Druck ohne Slicer-Stützen

4. Spezifikation:
   CAD_COMPACT_SPEC_V0.8.md

5. Claude:
   PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.8.md
'''


def make_build_v08() -> None:
    src = R / 'build_v07.py'
    text = src.read_text(encoding='utf-8')
    text = text.replace('V0.7', 'V0.8').replace('V07', 'V08')

    replacement = r'''# ---------------- P01 rounded enclosure base ----------------
L, W, H, wall, floor = C.L, C.W, C.H, C.WALL, C.FLOOR

# Lower rounded shell to Z45.
lower_outer = rounded_prism(0, L, 0, W, C.BODY_CORNER_R,
                            0, C.SHOULDER_Z0)
lower_inner = rounded_prism(wall, L-wall, wall, W-wall,
                            max(0.8, C.BODY_CORNER_R-wall),
                            floor, C.SHOULDER_Z0-floor+0.2)
b = lower_outer.cut(lower_inner)

# Recessed upper shoulder, continuous and free of lid columns.
sx0, sx1 = C.SHOULDER_INSET, L-C.SHOULDER_INSET
sy0, sy1 = C.SHOULDER_INSET, W-C.SHOULDER_INSET
upper_outer = rounded_prism(sx0, sx1, sy0, sy1,
                            C.SHOULDER_CORNER_R,
                            C.SHOULDER_Z0, C.SHOULDER_H)
upper_inner = rounded_prism(sx0+wall, sx1-wall,
                            sy0+wall, sy1-wall,
                            max(0.8, C.SHOULDER_CORNER_R-wall),
                            C.SHOULDER_Z0-0.1, C.SHOULDER_H+0.2)
b = b.union(upper_outer.cut(upper_inner))

# Rounded mounting flanges.
b = b.union(rounded_prism(0, L, -C.FLANGE, 0, 2.0, 0, floor))
b = b.union(rounded_prism(0, L, W, W+C.FLANGE, 2.0, 0, floor))
for x, y in C.WALL_MOUNT_HOLES:
    b = b.cut(cz(x, y, -0.2, C.WALL_MOUNT_D, floor+0.5))

# Long-wall openings end at the shoulder / lid-overlap line.
for y in (-0.5, W-wall-0.5):
    b = b.cut(box(C.OPEN_X0, y, C.OPEN_Z,
                  C.OPEN_X1-C.OPEN_X0, wall+1.0,
                  C.OPEN_TOP_Z-C.OPEN_Z+0.2))

# Waveshare standoffs are functional board mounts, not lid supports.
for x, y in C.STANDOFFS:
    b = b.union(cz(x, y, floor, C.STANDOFF_D,
                   C.BOARD_BOTTOM_Z-floor))
    b = b.cut(cz(x, y, floor-0.2, C.STANDOFF_PILOT_D,
                 C.BOARD_BOTTOM_Z-floor+0.5))

# Wall-integrated slide lugs with 45-degree printable lower ramps.
def side_lug(xc, rear=False):
    x0 = xc - C.SIDE_LUG_WIDTH/2
    if rear:
        points = [(sy1, C.SIDE_LUG_Z0),
                  (sy1+C.SIDE_LUG_PROJ, C.SIDE_LUG_Z0+C.SIDE_LUG_RAMP),
                  (sy1+C.SIDE_LUG_PROJ, C.SIDE_LUG_Z1),
                  (sy1, C.SIDE_LUG_Z1)]
    else:
        points = [(sy0, C.SIDE_LUG_Z0),
                  (sy0-C.SIDE_LUG_PROJ, C.SIDE_LUG_Z0+C.SIDE_LUG_RAMP),
                  (sy0-C.SIDE_LUG_PROJ, C.SIDE_LUG_Z1),
                  (sy0, C.SIDE_LUG_Z1)]
    return (cq.Workplane('YZ', origin=(x0,0,0))
            .polyline(points).close().extrude(C.SIDE_LUG_WIDTH))

for x in C.SIDE_LUG_X:
    b = b.union(side_lug(x, False)).union(side_lug(x, True))

# Wall-based snap pin.
px, py = C.LATCH_PIN
pz = H
for d, hh in C.LATCH_PIN_SEGMENTS:
    b = b.union(cz(px, py, pz, d, hh))
    pz += hh

# DC5521 on left end wall.
dy, dz, dd = C.DC5521
b = b.cut(cx(-0.2, dy, dz, dd, wall+0.5))

# ZERO/SPAN and PCB holders on right end wall.
for y, z, d in (C.ZERO, C.SPAN):
    b = b.cut(cx(L-wall-0.2, y, z, d, wall+0.5))
hx = L-wall-C.BTN_HOLDER_LEN
for y in C.BTN_HOLDER_Y:
    for z in C.BTN_HOLDER_Z:
        b = b.union(cx(hx, y, z, C.BTN_HOLDER_D,
                       C.BTN_HOLDER_LEN))
        b = b.cut(cx(hx-0.2, y, z, C.BTN_HOLDER_PILOT_D,
                     C.BTN_HOLDER_LEN+0.5))

# Physical markings.
for text_label, y, z in (('ZERO', C.ZERO[0], C.BTN_MARK_Z),
                         ('SPAN', C.SPAN[0], C.BTN_MARK_Z)):
    try:
        b = b.cut(outside_text_right(text_label, y, z))
    except Exception as exc:
        print('WARN right-wall marking skipped:', text_label, exc)
try:
    b = b.cut(outside_text_left('24 V DC', C.DC5521[0], 38.0, 4.0))
    b = b.cut(outside_text_left('V0.8', 91.0, 8.0, 3.0))
except Exception as exc:
    print('WARN left-wall marking skipped:', exc)

# ---------------- P02 rounded 10-mm overlap cap lid ----------------
lz, lt = C.LID_Z, C.LID_T
l = rounded_prism(C.LID_X0, C.LID_X1,
                  C.LID_Y0, C.LID_Y1,
                  C.LID_CORNER_R, lz, lt)
skirt_outer = rounded_prism(C.LID_X0, C.LID_X1,
                            C.LID_Y0, C.LID_Y1,
                            C.LID_CORNER_R,
                            lz-C.LID_OVERLAP, C.LID_OVERLAP)
skirt_inner = rounded_prism(C.LID_IN_X0, C.LID_IN_X1,
                            C.LID_IN_Y0, C.LID_IN_Y1,
                            max(0.8, C.LID_CORNER_R-C.LID_SKIRT_W),
                            lz-C.LID_OVERLAP-0.1,
                            C.LID_OVERLAP+0.2)
l = l.union(skirt_outer.cut(skirt_inner))

# Ventilation and the retained P03/P07 mounting geometry.
for x, y, lx, ly in C.VENTS:
    l = l.cut(box(x, y, lz-0.5, lx, ly, lt+1.0))
for x, y in C.HOOD_SCREWS:
    l = l.union(cz(x, y, C.HOOD_SCREW_BOSS_Z0,
                   C.HOOD_SCREW_BOSS_D, lz-C.HOOD_SCREW_BOSS_Z0))
    l = l.cut(cz(x, y, C.HOOD_SCREW_BOSS_Z0+0.5,
                 C.HOOD_SCREW_PILOT_D,
                 lz+lt-C.HOOD_SCREW_BOSS_Z0))
for x, y in C.POD_MOUNTS:
    l = l.union(cz(x, y, C.POD_BOSS_Z0,
                   C.POD_BOSS_D, lz-C.POD_BOSS_Z0))
    l = l.cut(cz(x, y, C.POD_BOSS_Z0-0.1,
                 C.POD_BOSS_PILOT_D,
                 C.POD_BOSS_PILOT_TOP-C.POD_BOSS_Z0+0.1))

# Through-slots on both long skirt walls. The wide entry is open at the
# lower skirt edge in the +8-mm insertion position.
slot_y_front = C.LID_Y0-0.2
slot_y_rear = C.LID_IN_Y1-0.2
slot_depth = C.LID_SKIRT_W+0.5
for x in C.SIDE_LUG_X:
    entry = x-C.SLIDE_TRAVEL
    entry_x0 = entry-C.SLOT_ENTRY_W/2
    entry_h = C.SLOT_ENTRY_TOP_Z-(lz-C.LID_OVERLAP)+0.2
    track_x1 = x+C.SLOT_TRACK_END_EXTRA
    for yy in (slot_y_front, slot_y_rear):
        l = l.cut(box(entry_x0, yy, lz-C.LID_OVERLAP-0.1,
                      C.SLOT_ENTRY_W, slot_depth, entry_h))
        l = l.cut(box(entry, yy, C.SLOT_TRACK_Z0,
                      track_x1-entry, slot_depth,
                      C.SLOT_TRACK_Z1-C.SLOT_TRACK_Z0))

# Flush spring tongue in the top plate and an access notch in the skirt.
tx0, tx1 = C.LATCH_TONGUE_X
ty0, ty1 = C.LATCH_TONGUE_Y
l = l.cut(box(tx0, ty0, lz-0.1,
              tx1-tx0, ty1-ty0,
              lt-C.LATCH_TONGUE_SKIN+0.1))
l = l.cut(box(tx0, ty1, lz-0.2,
              tx1-tx0, C.LATCH_SLOT_W, lt+0.4))
l = l.cut(box(tx0-C.LATCH_SLOT_W, ty0, lz-0.2,
              C.LATCH_SLOT_W, ty1-ty0+C.LATCH_SLOT_W, lt+0.4))
lhx, lhy, lhd = C.LATCH_HOLE
l = l.cut(cz(lhx, lhy, lz-0.2, lhd, lt+0.4))
nx0, nx1 = C.LATCH_SKIRT_NOTCH_X
l = l.cut(box(nx0, C.LID_Y0-0.2,
              lz-C.LID_OVERLAP-0.1,
              nx1-nx0, C.LID_SKIRT_W+0.5,
              C.LID_OVERLAP+0.2))

# ---------------- P03 sensor pod ----------------'''

    text = sub_once(
        text,
        r"# ---------------- P01 enclosure base ----------------.*?# ---------------- P03 sensor pod ----------------",
        replacement,
        'P01/P02 redesign')

    # Rename coordinate file and add a V0.8 enclosure drawing before the final print.
    text = text.replace("'V08_COORDINATES.csv'", "'V08_COORDINATES.csv'")
    marker = "print('Generated AirMonitor Compact V0.8 corrected O-ring package:', R)"
    drawing = r'''cap_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="760" viewBox="-8 -10 225 135">
{svg_style}
<text class="t" x="0" y="-5">AirMonitor V0.8 - abgerundeter 10-mm-Ueberwurfdeckel [mm]</text>
<rect class="wall" x="0" y="0" width="208" height="112" rx="6"/>
<rect class="part" x="2" y="2" width="204" height="108" rx="4"/>
<rect x="-0.5" y="-0.5" width="209" height="113" rx="6.5" fill="none" stroke="#7A3FA0" stroke-width="0.6"/>
<text class="s" x="70" y="108">Deckel aussen 209 x 113, R6,5</text>
<text class="s" x="70" y="103">Schulter 204 x 108, R4; Spiel 0,30/Seite</text>
<g stroke="#b33" fill="none" stroke-width="0.7">
  <path d="M72 2 H83"/><path d="M164 2 H175"/>
  <path d="M72 110 H83"/><path d="M164 110 H175"/>
</g>
<text class="s" x="72" y="8">4 Seitenschlitze / 8 mm Weg</text>
<text class="s" x="108" y="16">vorn: Rastzunge + Bediennotch</text>
</svg>'''
(D / 'Drawing_V08_Rounded_Overlap_Lid.svg').write_text(cap_svg, encoding='utf-8')

side_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="620" viewBox="-5 -5 218 70">
{svg_style}
<text class="t" x="0" y="-1">AirMonitor V0.8 - Seitenansicht Deckeluebergriff [mm]</text>
<path class="wall" d="M0 55 V0 H208 V55 H206 V45 H2 V55 Z"/>
<path d="M-0.5 58 H208.5 V45 H206 V55 H2 V45 H-0.5 Z" fill="#F1E8F7" stroke="#7A3FA0" stroke-width="0.5"/>
<rect x="36.6" y="12" width="122" height="33" fill="white" stroke="#172b3a" stroke-width="0.4"/>
<text class="s" x="162" y="50">10 mm Uebergriff</text>
<text class="s" x="70" y="30">freie Oeffnung 122 x 33</text>
<text class="s" x="70" y="62">Topplatte 3 mm; Oberseite Druckbettseite</text>
</svg>'''
(D / 'Drawing_V08_Overlap_Lid_Side.svg').write_text(side_svg, encoding='utf-8')

'''
    if marker not in text:
        # Current copied build may use a slightly different final string.
        marker = "print('Generated AirMonitor Compact V0.8 corrected O-ring package:', R)"
    text = text.replace(marker, drawing + marker, 1)
    (R / 'build_v08.py').write_text(text, encoding='utf-8')


def make_sketches_v08() -> None:
    src = R / 'generate_mass_sketches_v07.py'
    text = src.read_text(encoding='utf-8')
    text = text.replace('V0.7', 'V0.8').replace('V07', 'V08')

    page1 = r'''def page1_base(c):
    header(c, "P01 - abgerundeter Gehaeuseboden / Draufsicht innen",
           "3,2-mm-Wand; R6; obere Schulter gestrichelt; keine Deckelstuetzen in der Mitte")
    ox, oy = 38*mm, 39*mm
    c.roundRect(ox, oy-C.FLANGE*mm, C.L*mm, (C.W+2*C.FLANGE)*mm, 2*mm)
    c.roundRect(ox, oy, C.L*mm, C.W*mm, C.BODY_CORNER_R*mm)
    c.saveState(); c.setDash(3,2); c.setStrokeColor(C_HOOD)
    c.roundRect(ox+C.SHOULDER_INSET*mm, oy+C.SHOULDER_INSET*mm,
                (C.L-2*C.SHOULDER_INSET)*mm,
                (C.W-2*C.SHOULDER_INSET)*mm,
                C.SHOULDER_CORNER_R*mm)
    c.restoreState()
    for x,y in C.WALL_MOUNT_HOLES:
        c.circle(ox+x*mm,oy+y*mm,C.WALL_MOUNT_D/2*mm)
    c.setStrokeColor(C_POD)
    for x,y in C.STANDOFFS:
        c.circle(ox+x*mm,oy+y*mm,C.STANDOFF_D/2*mm)
        c.circle(ox+x*mm,oy+y*mm,C.STANDOFF_PILOT_D/2*mm)
    c.setStrokeColor(C_ORING)
    for x in C.SIDE_LUG_X:
        c.rect(ox+(x-C.SIDE_LUG_WIDTH/2)*mm,oy+(C.SHOULDER_INSET-C.SIDE_LUG_PROJ)*mm,
               C.SIDE_LUG_WIDTH*mm,C.SIDE_LUG_PROJ*mm)
        c.rect(ox+(x-C.SIDE_LUG_WIDTH/2)*mm,oy+(C.W-C.SHOULDER_INSET)*mm,
               C.SIDE_LUG_WIDTH*mm,C.SIDE_LUG_PROJ*mm)
    c.setStrokeColor(colors.black)
    dim_h(c,ox,ox+C.L*mm,oy-17*mm,"208")
    dim_v(c,ox+C.L*mm+9*mm,oy-C.FLANGE*mm,oy+(C.W+C.FLANGE)*mm,"132")
    label(c,12*mm,27*mm,"Violett gestrichelt: zurueckgesetzte Schulter X/Y je 2,0; Beginn Z45,0.",7)
    label(c,12*mm,22*mm,"Rot: vier wandintegrierte Fuehrungslaschen bei X80 / X172; keine freien Deckelsaeulen.",7)
    label(c,12*mm,17*mm,"Blau: notwendige Waveshare-Abstandshalter; Wand/Boden 3,2; Aussenradius R6,0.",7)
    footer(c,1)
'''
    text = sub_once(text, r'def page1_base\(c\):.*?(?=\ndef page2_walls)', page1, 'page1')

    page2 = r'''def page2_walls(c):
    header(c,"P01/P02 - Laengswand und 10-mm-Deckeluebergriff",
           "Deckelschuerze reicht von Z55 bis Z45; freie Bodenoeffnung endet bei Z45")
    ox,oy=38*mm,55*mm
    c.roundRect(ox,oy,C.L*mm,C.H*mm,C.BODY_CORNER_R*mm)
    c.rect(ox+C.OPEN_X0*mm,oy+C.OPEN_Z*mm,
           (C.OPEN_X1-C.OPEN_X0)*mm,
           (C.OPEN_TOP_Z-C.OPEN_Z)*mm)
    c.saveState(); c.setStrokeColor(C_HOOD); c.setLineWidth(0.8)
    c.line(ox-C.LID_OUTSET*mm,oy+(C.LID_Z-C.LID_OVERLAP)*mm,
           ox-C.LID_OUTSET*mm,oy+(C.LID_Z+C.LID_T)*mm)
    c.line(ox+(C.L+C.LID_OUTSET)*mm,oy+(C.LID_Z-C.LID_OVERLAP)*mm,
           ox+(C.L+C.LID_OUTSET)*mm,oy+(C.LID_Z+C.LID_T)*mm)
    c.line(ox-C.LID_OUTSET*mm,oy+(C.LID_Z+C.LID_T)*mm,
           ox+(C.L+C.LID_OUTSET)*mm,oy+(C.LID_Z+C.LID_T)*mm)
    c.restoreState()
    dim_h(c,ox,ox+C.L*mm,oy-12*mm,"208")
    dim_h(c,ox+C.OPEN_X0*mm,ox+C.OPEN_X1*mm,oy+C.OPEN_TOP_Z*mm+7*mm,"122")
    dim_v(c,ox+C.L*mm+8*mm,oy,oy+C.H*mm,"55")
    dim_v(c,ox+C.L*mm+18*mm,oy+C.SHOULDER_Z0*mm,oy+C.H*mm,"10 Uebergriff")
    label(c,12*mm,27*mm,"Bodenoeffnung: X36,6..158,6 / Z12,0..45,0 = 122 x 33.",7)
    label(c,12*mm,22*mm,"Deckel: Topplatte 3,0; Schuerze 10,0 nach unten; Oberseite ist Druckbettseite.",7)
    label(c,12*mm,17*mm,"Unterer Koerper R6,0; Schulter R4,0; Deckel R6,5.",7)
    footer(c,2)
'''
    text = sub_once(text, r'def page2_walls\(c\):.*?(?=\ndef page3_endwalls)', page2, 'page2')

    page4 = r'''def page4_lid(c):
    header(c,"P02 - abgerundeter Ueberwurf-Schiebedeckel",
           "209 x 113; R6,5; 10 mm Schuerze; vier Seitenschlitze und Rastzunge")
    ox,oy=37.5*mm,46.5*mm
    w=C.LID_X1-C.LID_X0; h=C.LID_Y1-C.LID_Y0
    c.roundRect(ox,oy,w*mm,h*mm,C.LID_CORNER_R*mm)
    c.saveState(); c.setDash(3,2); c.setStrokeColor(C_HOOD)
    c.roundRect(ox+C.LID_SKIRT_W*mm,oy+C.LID_SKIRT_W*mm,
                (w-2*C.LID_SKIRT_W)*mm,(h-2*C.LID_SKIRT_W)*mm,
                (C.LID_CORNER_R-C.LID_SKIRT_W)*mm)
    c.restoreState()
    c.setStrokeColor(C_POD)
    for x,y,lx,ly in C.VENTS:
        c.rect(ox+(x-C.LID_X0)*mm,oy+(y-C.LID_Y0)*mm,lx*mm,ly*mm)
    c.setStrokeColor(C_ORING)
    for x in C.SIDE_LUG_X:
        entry=x-C.SLIDE_TRAVEL
        for yy in (C.LID_Y0,C.LID_Y1):
            py=oy+(yy-C.LID_Y0)*mm
            c.line(ox+(entry-C.LID_X0)*mm,py,ox+(x+C.SLOT_TRACK_END_EXTRA-C.LID_X0)*mm,py)
    tx0,tx1=C.LATCH_TONGUE_X; ty0,ty1=C.LATCH_TONGUE_Y
    c.rect(ox+(tx0-C.LID_X0)*mm,oy+(ty0-C.LID_Y0)*mm,(tx1-tx0)*mm,(ty1-ty0)*mm)
    hx,hy,hd=C.LATCH_HOLE
    c.circle(ox+(hx-C.LID_X0)*mm,oy+(hy-C.LID_Y0)*mm,hd/2*mm)
    dim_h(c,ox,ox+w*mm,oy-10*mm,"209,0")
    dim_v(c,ox+w*mm+8*mm,oy,oy+h*mm,"113,0")
    label(c,12*mm,29*mm,"Geschlossen: Deckel 8,0 mm nach -X schieben; Laschen liegen im schmalen Schlitz.",7)
    label(c,12*mm,24*mm,"Oeffnen: Rastzunge loesen, 8,0 mm nach +X schieben und nach oben abheben.",7)
    label(c,12*mm,19*mm,"Druck: sichtbare Oberseite auf dem Bett; Schuerze nach oben; keine Slicer-Stuetzen vorgesehen.",7,True)
    footer(c,4)
'''
    text = sub_once(text, r'def page4_lid\(c\):.*?(?=\ndef page5_pod)', page4, 'page4')

    page9 = r'''def page9_assembly(c):
    header(c,"V0.8 - Gehaeuse- und Deckelmontage",
           "Pruefstation bleibt auf P02; P02 wird als 10-mm-Kappe auf die Schulter gesetzt")
    label(c,18*mm,158*mm,"Schliessablauf",8,True)
    steps=[
        "P03, Sensor, Kabel, P05, P07 und die drei O-Ringe am Deckel montieren.",
        "Deckel um +8,0 mm in X versetzt ueber die abgerundete Schulter absenken.",
        "Alle vier Wandlaschen durch die nach unten offenen Einfuehrungen fuehren.",
        "Deckel 8,0 mm nach links (-X) schieben; Laschen halten die Kappe vertikal.",
        "Federzunge einrasten lassen und umlaufenden 0,30-mm-Spalt kontrollieren.",
        "Zum Oeffnen Zunge loesen, 8,0 mm nach rechts schieben und Kappe abheben.",
    ]
    for i,t in enumerate(steps): label(c,22*mm,(148-9*i)*mm,f"{i+1}. {t}",7)
    label(c,18*mm,85*mm,"Konstruktionsschnitt",8,True)
    x=52*mm; y=40*mm
    c.setFillColor(colors.HexColor("#EAF1F8")); c.setStrokeColor(C_POD)
    c.roundRect(x,y,150*mm,45*mm,6*mm,stroke=1,fill=1)
    c.setFillColor(colors.white)
    c.roundRect(x+3.2*mm,y+3.2*mm,143.6*mm,42*mm,3*mm,stroke=1,fill=1)
    c.setFillColor(colors.HexColor("#F1E8F7")); c.setStrokeColor(C_HOOD)
    c.roundRect(x-0.5*mm,y+35*mm,151*mm,13*mm,6.5*mm,stroke=1,fill=1)
    label(c,x+154*mm,y+40*mm,"P02: 3 mm Top + 10 mm Schuerze",7)
    label(c,x+154*mm,y+31*mm,"P01: Schulter ab Z45",7)
    label(c,x+154*mm,y+22*mm,"keine Deckelsaeulen",7,True)
    footer(c,9)
'''
    text = sub_once(text, r'def page9_assembly\(c\):.*?(?=\ndef page10_summary)', page9, 'page9')

    page10 = r'''def page10_summary(c):
    header(c,"V0.8 - Freigabe- und Pruefliste",
           "Abgerundete 10-mm-Kappe, dickere Waende und wandintegrierte Schiebefuehrung")
    label(c,18*mm,160*mm,"Umgesetzt",8,True)
    items=[
        "Microtaster und Pruefstation aus V0.7 unveraendert uebernommen.",
        "P01 Wand/Boden 3,2 mm; untere Ecken R6,0; obere Schulter R4,0.",
        "P02 209 x 113 mit R6,5 und 10,0-mm-Uebergriff.",
        "Keine zusaetzlichen Deckelstuetzen oder Verschlusssaeulen in der Mitte.",
        "Vier wandintegrierte 45-Grad-Laschen und nach unten offene Einfuehrschlitze.",
        "8-mm-Schiebeweg mit Federzunge am Ende.",
        "Druckorientierung von P01/P02 ohne Slicer-Stuetzen vorgesehen.",
        "Seitliche freie Oeffnung jetzt 122 x 33 unterhalb des Uebergriffs.",
    ]
    for i,t in enumerate(items): label(c,22*mm,(151-8*i)*mm,"- "+t,7)
    label(c,18*mm,82*mm,"Vor Freigabe praktisch pruefen",8,True)
    checks=[
        "[ ] Deckel senkt sich in +8-mm-Lage ohne Verkanten ueber die Schulter.",
        "[ ] Vier Laschen greifen gleichzeitig; Deckel klappert nicht und klemmt nicht.",
        "[ ] Rastzunge funktioniert mindestens 20 Zyklen ohne Riss.",
        "[ ] P03/P07 und Kabel haben in offener und geschlossener Lage Freiraum.",
        "[ ] Deckel ist plan, Ecken sind sauber und die 10-mm-Schuerze ist unverzogen.",
        "[ ] O-Ring-Sitz, Pruefstation, Leckrate und Nullpunktrueckkehr sind dokumentiert.",
    ]
    for i,t in enumerate(checks): label(c,22*mm,(73-8*i)*mm,t,7)
    footer(c,10,"CAD-Stand: V0.8 - abgerundeter Ueberwurf-Schiebedeckel")
'''
    text = sub_once(text, r'def page10_summary\(c\):.*?(?=\ndef main)', page10, 'page10')
    (R / 'generate_mass_sketches_v08.py').write_text(text, encoding='utf-8')


def clean_old_files() -> None:
    for name in [
        'build_v07.py', 'generate_mass_sketches_v07.py',
        'apply_v07_slide_lid_patch.py',
        'AirMonitor_V07_Massskizzen_1zu1.pdf',
        'CAD_COMPACT_SPEC_V0.7.md',
        'PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.7.md',
        'V07_COORDINATES.csv',
    ]:
        p = R / name
        if p.exists():
            p.unlink()


def main() -> None:
    (R / 'compact_params.py').write_text(PARAMS, encoding='utf-8')
    (R / 'check_clearances.py').write_text(CHECKS, encoding='utf-8')
    make_build_v08()
    make_sketches_v08()
    (R / 'CAD_COMPACT_SPEC_V0.8.md').write_text(SPEC, encoding='utf-8')
    (R / 'README.md').write_text(README, encoding='utf-8')
    (R / 'PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.8.md').write_text(PROMPT, encoding='utf-8')
    (R / 'START_HIER_DANIEL_CLAUDE.txt').write_text(START, encoding='utf-8')
    clean_old_files()
    print('Applied AirMonitor Compact V0.8 rounded overlap-lid redesign')


if __name__ == '__main__':
    main()
