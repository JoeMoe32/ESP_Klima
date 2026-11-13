"""Numeric checks for AirMonitor Compact V0.8."""
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

    sx0, sx1 = C.SHOULDER_INSET, C.L-C.SHOULDER_INSET
    sy0, sy1 = C.SHOULDER_INSET, C.W-C.SHOULDER_INSET
    clearances = (sx0-C.LID_IN_X0, C.LID_IN_X1-sx1,
                  sy0-C.LID_IN_Y0, C.LID_IN_Y1-sy1)
    for i, value in enumerate(clearances, 1):
        check(f'skirt clearance {i}', 0.20 <= value <= 0.45, f'{value:.3f}')
    check('shoulder joins lower wall', C.WALL > C.SHOULDER_INSET)
    check('lid upper face flat', C.LID_TOP_FACE_FLAT)
    check('lid top is print-bed face', C.LID_PRINT_TOP_FACE_DOWN)

    check('slide travel 8 mm', close(C.SLIDE_TRAVEL, 8.0))
    check('slide closes toward -X', C.SLIDE_CLOSE_DIRECTION == '-X')
    check('lug ramp 45 degrees', close(C.SIDE_LUG_RAMP, C.SIDE_LUG_PROJ))
    check('slot entry wider than lug', C.SLOT_ENTRY_W > C.SIDE_LUG_WIDTH)
    check('slot track covers lug height', C.SLOT_TRACK_Z0 < C.SIDE_LUG_Z0 and C.SLOT_TRACK_Z1 > C.SIDE_LUG_Z1)
    check('entry open above lug', C.SLOT_ENTRY_TOP_Z > C.SIDE_LUG_Z1)
    check('lugs clear calibration group', min(C.SIDE_LUG_X)-C.SIDE_LUG_WIDTH/2 > C.HOOD_PLATE[1])

    tx0, tx1 = C.LATCH_TONGUE_X
    ty0, ty1 = C.LATCH_TONGUE_Y
    hx, hy, _ = C.LATCH_HOLE
    px, py = C.LATCH_PIN
    pin_h = sum(h for _, h in C.LATCH_PIN_SEGMENTS)
    tongue_under = C.LID_Z + C.LID_T - C.LATCH_TONGUE_SKIN
    interference = C.H + pin_h - tongue_under
    check('latch aligned', close(hx, px) and close(hy, py))
    check('latch hole in tongue', tx0 < hx < tx1 and ty0 <= hy <= ty1)
    check('tongue printable skin', 1.0 <= C.LATCH_TONGUE_SKIN <= 1.4)
    check('snap interference', 0.2 <= interference <= 0.6, f'{interference:.2f}')
    check('skirt notch covers tongue', C.LATCH_SKIRT_NOTCH_X[0] <= tx0 and C.LATCH_SKIRT_NOTCH_X[1] >= tx1)

    check('ZERO-SPAN 16 mm', close(C.SPAN[0]-C.ZERO[0], 16.0))
    check('ZERO/SPAN height retained', close(C.ZERO[1],26.0) and close(C.SPAN[1],26.0))
    check('button holder pattern retained', C.BTN_HOLDER_Y == (18.0,94.0) and C.BTN_HOLDER_Z == (20.0,36.0))
    check('Waveshare X pattern', close(C.STANDOFFS[1][0]-C.STANDOFFS[0][0],145.0))
    check('Waveshare Y pattern', close(C.STANDOFFS[2][1]-C.STANDOFFS[0][1],62.0))

    # Only P03 passes through the enclosure shoulder. P07 sits above P02 and
    # therefore must be checked against the lid footprint, not the shoulder cavity.
    inner_x0 = C.SHOULDER_INSET + C.WALL
    inner_x1 = C.L - C.SHOULDER_INSET - C.WALL
    inner_y0 = C.SHOULDER_INSET + C.WALL
    inner_y1 = C.W - C.SHOULDER_INSET - C.WALL
    gx0, gx1, gy0, gy1 = C.POD[:4]
    check('P03 closed inside shoulder X', inner_x0 <= gx0 and gx1 <= inner_x1,
          f'{gx0}..{gx1} vs {inner_x0}..{inner_x1}')
    check('P03 open inside shoulder X', inner_x0 <= gx0+C.SLIDE_OPEN_OFFSET_X and gx1+C.SLIDE_OPEN_OFFSET_X <= inner_x1)
    check('P03 inside shoulder Y', inner_y0 <= gy0 and gy1 <= inner_y1)

    hx0, hx1, hy0, hy1 = C.HOOD_PLATE
    check('P07 inside lid X', C.LID_X0 <= hx0 and hx1 <= C.LID_X1)
    check('P07 inside lid Y', C.LID_Y0 <= hy0 and hy1 <= C.LID_Y1)
    check('P07 stays fixed to moving lid', close(C.HOOD_Z0, C.LID_Z + C.LID_T))

    check('O-ring cord', close(C.ORING_CORD,1.50))
    check('groove wider than cord', C.ORING_GROOVE_W > C.ORING_CORD)
    check('compression 20-30 percent', 0.20 <= C.ORING_COMPRESSION <= 0.30)
    def stretch(r):
        path = 2*(r['cw']+r['ch']) + (2*math.pi-8)*r['r']
        free = math.pi*(r['id']+r['cord'])
        return path/free-1
    for ring in (C.P04A_RING,C.P04B_RING,C.P08_RING):
        s = stretch(ring)
        check(f"{ring['name']} path stretch", -0.005 <= s <= 0.03, f'{s*100:.2f}%')
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
