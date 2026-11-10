"""Dimension and clearance checks for AirMonitor Compact V0.4."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compact_params as C  # noqa: E402


def run():
    rows = []
    bad = 0

    def chk(name, value, limit, ge=True, unit='mm'):
        nonlocal bad
        ok = value >= limit - 1e-9 if ge else value <= limit + 1e-9
        if not ok:
            bad += 1
        rows.append(f"{'OK ' if ok else 'NOK'} {name}: {value:.2f} {unit} ({'≥' if ge else '≤'} {limit:.2f})")

    px0, px1, py0, py1, pz0, pz1 = C.POD
    inner = (px0 + C.POD_WALL, px1 - C.POD_WALL,
             py0 + C.POD_WALL, py1 - C.POD_WALL)
    pcb = C.SEN_PCB
    con = C.SEN_CON
    top = C.SEN_TOP
    slot = C.GRAVITY_SLOT
    carrier = C.CARRIER

    chk('P03 left margin', px0, C.WALL + 5.0)
    chk('P03 right margin', C.L - px1, 20.0)
    chk('P03 front margin', py0, 10.0)
    chk('P03 rear margin', C.W - py1, 10.0)
    chk('Waveshare top to P03 bottom', pz0 - carrier[5], 10.0)
    chk('P03 top to lid underside', C.LID_Z - pz1, 1.0)

    chk('PCB left clearance in pod', pcb[0] - inner[0], 5.0)
    chk('PCB right clearance in pod', inner[1] - pcb[1], 5.0)
    chk('PCB front clearance in pod', pcb[2] - inner[2], 5.0)
    chk('PCB rear clearance in pod', inner[3] - pcb[3], 5.0)
    chk('Sensor top to lid underside', C.LID_Z - top[5], 5.0)

    chk('Connector top equals PCB underside', abs(con[5] - pcb[4]), 0.05, ge=False)
    chk('Connector below PCB', pcb[4] - con[4], 4.0)
    chk('Connector X within PCB', min(con[0] - pcb[0], pcb[1] - con[1]), 0.5)
    chk('Connector Y within PCB', min(con[2] - pcb[2], pcb[3] - con[3]), 0.5)

    chk('Slot left around connector', con[0] - slot[0], 0.4)
    chk('Slot right around connector', slot[1] - con[1], 0.4)
    chk('Slot front around connector', con[2] - slot[2], 0.4)
    chk('Slot rear around connector', slot[3] - con[3], 0.4)
    chk('Slot below connector', con[4] - slot[4], 0.5)
    chk('Slot above PCB underside', slot[5] - pcb[4], 0.4)

    for i, (x, y, lx, ly) in enumerate(C.VENTS, 1):
        chk(f'Vent {i} left in pod inner', x - inner[0], 1.0)
        chk(f'Vent {i} right in pod inner', inner[1] - (x + lx), 1.0)
        chk(f'Vent {i} front in pod inner', y - inner[2], 1.0)
        chk(f'Vent {i} rear in pod inner', inner[3] - (y + ly), 1.0)
        fo = C.HOOD_FLOOR_OPEN
        chk(f'Vent {i} in hood opening X-left', x - fo[0], 0.5)
        chk(f'Vent {i} in hood opening X-right', fo[1] - (x + lx), 0.5)
        chk(f'Vent {i} in hood opening Y-front', y - fo[2], 0.5)
        chk(f'Vent {i} in hood opening Y-rear', fo[3] - (y + ly), 0.5)

    gap8 = C.LID_Z - pz1
    comp8 = (C.P08['t'] - gap8) / C.P08['t'] * 100
    chk('P08 compression min', comp8, 15.0, unit='%')
    chk('P08 compression max', comp8, 35.0, ge=False, unit='%')
    gap4 = C.HOOD_Z0 - (C.LID_Z + C.LID_T)
    comp4 = (C.P04['t'] - gap4) / C.P04['t'] * 100
    chk('P04 compression min', comp4, 15.0, unit='%')
    chk('P04 compression max', comp4, 35.0, ge=False, unit='%')

    _, top_w, _ = C.HOOD_IN
    cx, cy = C.HOOD_CENTER
    tx0, tx1 = cx - top_w[0] / 2, cx + top_w[0] / 2
    ty0, ty1 = cy - top_w[1] / 2, cy + top_w[1] / 2
    for name, (x, y) in C.HOOD_PORTS.items():
        chk(f'{name} port inside top cavity X-left', x - tx0, 2.0)
        chk(f'{name} port inside top cavity X-right', tx1 - x, 2.0)
        chk(f'{name} port inside top cavity Y-front', y - ty0, 2.0)
        chk(f'{name} port inside top cavity Y-rear', ty1 - y, 2.0)
    chk('IN on lower divider side', C.HOOD_DIVIDER_Y[0] - C.HOOD_PORTS['IN'][1], 3.0)
    chk('OUT on upper divider side', C.HOOD_PORTS['OUT'][1] - C.HOOD_DIVIDER_Y[1], 3.0)
    chk('Divider leaves right flow gap', (C.HOOD_CENTER[0] + C.HOOD_IN[0][0] / 2) - C.HOOD_DIVIDER_X[1], 4.0)

    chk('Base X fits Prusa MK4', C.L, 250.0, ge=False)
    chk('Base Y incl. flanges fits Prusa MK4', C.W + 2 * C.FLANGE, 210.0, ge=False)
    max_z = C.HOOD_Z0 + C.HOOD_PLATE_T + C.HOOD_OUT[2] + C.HOOD_ROOF[4] + sum(h for _, h in C.HOOD_NOZZLE)
    chk('Max Z incl. compact hood', max_z, 220.0, ge=False)

    print('\n'.join(rows))
    print(f'\n{len(rows)} checks, {bad} NOK')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(run())
