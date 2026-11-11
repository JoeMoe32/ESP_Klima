"""Dimension and clearance checks for AirMonitor Compact V0.7.

Runs without the CAD kernel. Exit code 0 means all defined checks pass.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compact_params as C  # noqa: E402

MIN_GAP = 0.3


def rect_dist(px, py, x0, x1, y0, y1):
    dx = max(x0 - px, 0.0, px - x1)
    dy = max(y0 - py, 0.0, py - y1)
    return math.hypot(dx, dy)


def run():
    rows = []
    bad = 0

    def chk(name, value, limit, ge=True, unit='mm'):
        nonlocal bad
        ok = value >= limit - 1e-9 if ge else value <= limit + 1e-9
        bad += 0 if ok else 1
        rows.append(f"{'OK ' if ok else 'NOK'} {name}: {value:.3f} {unit} ({'≥' if ge else '≤'} {limit:.3f})")

    def eq(name, value, target, tol=1e-6, unit='mm'):
        nonlocal bad
        ok = abs(value - target) <= tol
        bad += 0 if ok else 1
        rows.append(f"{'OK ' if ok else 'NOK'} {name}: {value:.3f} {unit} (= {target:.3f} ± {tol:.3f})")

    # Annotated V0.6 drawing corrections.
    eq('right lid boss edge offset top', C.L - C.LID_BOSSES[2][0], 7.0)
    eq('right lid boss edge offset bottom', C.L - C.LID_BOSSES[3][0], 7.0)
    eq('board standoff left X', C.STANDOFFS[0][0], 24.0)
    eq('board standoff right X', C.STANDOFFS[1][0], 169.0)
    eq('board standoff bottom Y', C.STANDOFFS[0][1], 25.0)
    eq('board standoff top Y', C.STANDOFFS[2][1], 87.0)
    eq('board hole spacing X', C.STANDOFFS[1][0] - C.STANDOFFS[0][0], 145.0)
    eq('board hole spacing Y', C.STANDOFFS[2][1] - C.STANDOFFS[0][1], 62.0)

    # Board body relative to standoffs.
    p = C.PCB_WAVESHARE
    eq('board body length', p[1] - p[0], 151.8)
    eq('board body width', p[3] - p[2], 90.0)
    eq('left mounting offset', C.STANDOFFS[0][0] - p[0], 3.4)
    eq('right mounting offset', p[1] - C.STANDOFFS[1][0], 3.4)
    eq('front mounting offset', C.STANDOFFS[0][1] - p[2], 14.0)
    eq('rear mounting offset', p[3] - C.STANDOFFS[2][1], 14.0)

    # Sensor group shift and width.
    eq('pod left edge moved +20', C.POD[0], 26.0)
    eq('pod nominal width', C.POD[1] - C.POD[0], 53.5)
    eq('vent field moved +20', C.VENTS[0][0], 32.0)
    eq('hood screw moved +20', C.HOOD_SCREWS[0][0], 47.0)
    eq('pod mount moved +20', C.POD_MOUNTS[0][0], 36.0)
    chk('pod right edge inside enclosure', C.L - C.POD[1], 20.0)
    chk('pod front clearance', C.POD[2] - C.WALL, 10.0)
    chk('pod rear clearance', (C.W - C.WALL) - C.POD[3], 10.0)
    chk('Waveshare to pod vertical clearance', C.POD[4] - C.BOARD_TOP_Z, 10.0)
    chk('SEN0661 connector to lid clearance', C.LID_Z - C.SEN_CON[5], 0.5)

    # Slot remains in the new right wall.
    eq('slot reaches pod right wall', C.GRAVITY_SLOT[1] - C.POD[1], 0.5)
    eq('cable stop width', C.P05[1] - C.P05[0], 4.0)
    eq('cable stop height', C.P05[5] - C.P05[4], 8.0)

    # Button PCB remains centered between projected lid columns.
    pcb_y0 = sum(C.BTN_HOLDER_Y) / 2 - C.BTN_PCB[0] / 2
    pcb_y1 = sum(C.BTN_HOLDER_Y) / 2 + C.BTN_PCB[0] / 2
    eq('button PCB centered in 112 mm wall', (pcb_y0 + pcb_y1) / 2, C.W / 2)
    eq('button holder pattern Y', C.BTN_HOLDER_Y[1] - C.BTN_HOLDER_Y[0], 76.0)
    eq('button holder pattern Z', C.BTN_HOLDER_Z[1] - C.BTN_HOLDER_Z[0], 16.0)
    eq('ZERO-SPAN spacing', C.SPAN[0] - C.ZERO[0], 16.0)

    # Right-wall columns projected in Y: centres 7 and 105, radius 4.5.
    left_column_edge = C.LID_BOSSES[2][1] + C.LID_BOSS_D / 2
    right_column_edge = C.LID_BOSSES[3][1] - C.LID_BOSS_D / 2
    chk('PCB left edge to lower column', pcb_y0 - left_column_edge, 3.0)
    chk('PCB right edge to upper column', right_column_edge - pcb_y1, 3.0)

    # DC jack moved to opposite wall; height unchanged.
    if C.DC_WALL != 'left':
        rows.append('NOK DC5521 wall: expected left')
        bad += 1
    else:
        rows.append('OK  DC5521 wall: left/opposite end wall')
    eq('DC5521 height', C.DC5521[1], 27.5)
    chk('DC5521 edge clearance Y low', C.DC5521[0] - C.DC5521[2] / 2, 8.0)
    chk('DC5521 edge clearance Y high', C.W - (C.DC5521[0] + C.DC5521[2] / 2), 8.0)

    # Gasket and groove design.
    eq('TPU gasket height', C.GASKET_H, 2.0)
    eq('groove depth', C.GROOVE_DEPTH, 0.6)
    residual = C.LID_T - 2 * C.GROOVE_DEPTH
    chk('lid residual thickness between grooves', residual, 1.5)
    p08_gap = (C.LID_Z + C.GROOVE_DEPTH) - C.POD[5]
    p08_comp = (C.P08['h'] - p08_gap) / C.P08['h'] * 100
    chk('P08 compression min', p08_comp, 15.0, unit='%')
    chk('P08 compression max', p08_comp, 30.0, ge=False, unit='%')
    p04_floor = C.LID_Z + C.LID_T - C.GROOVE_DEPTH
    p04_gap = C.HOOD_Z0 - p04_floor
    p04_comp = (C.P04['h'] - p04_gap) / C.P04['h'] * 100
    chk('P04 compression min', p04_comp, 15.0, unit='%')
    chk('P04 compression max', p04_comp, 35.0, ge=False, unit='%')
    chk('P08 gasket width for TPU printing', C.P08['web'], 2.4)
    chk('P04 gasket width for TPU printing', C.P04['web'], 2.4)

    # Hood remains within lid and covers the enlarged pod.
    hp = C.HOOD_PLATE
    chk('hood left edge on lid', hp[0], 3.0)
    chk('hood right edge on lid', C.L - hp[1], 3.0)
    chk('hood plate covers pod left', C.POD[0] - hp[0], 1.5)
    chk('hood plate covers pod right', hp[1] - C.POD[1], 0.4)

    # Lid bosses vs carrier and sensor features.
    carrier = C.CARRIER
    for i, (x, y) in enumerate(C.LID_BOSSES, 1):
        gap = rect_dist(x, y, carrier[0], carrier[1], carrier[2], carrier[3]) - C.LID_BOSS_D / 2
        chk(f'lid boss {i} to carrier', gap, MIN_GAP)
    for i, (x, y) in enumerate(C.POD_MOUNTS, 1):
        on_front = C.TONGUE_X[0] + C.TONGUE_HOLE_D/2 <= x <= C.TONGUE_X[1] - C.TONGUE_HOLE_D/2
        on_y = ((C.TONGUE_FRONT_Y[0] + C.TONGUE_HOLE_D/2 <= y <= C.TONGUE_FRONT_Y[1] - C.TONGUE_HOLE_D/2) or
                (C.TONGUE_BACK_Y[0] + C.TONGUE_HOLE_D/2 <= y <= C.TONGUE_BACK_Y[1] - C.TONGUE_HOLE_D/2))
        if on_front and on_y:
            rows.append(f'OK  pod mount {i} lies in mounting tongue')
        else:
            rows.append(f'NOK pod mount {i} outside mounting tongue')
            bad += 1

    print('\n'.join(rows))
    print(f'\n{len(rows)} checks, {bad} NOK')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(run())
