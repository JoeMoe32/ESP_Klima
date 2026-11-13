"""Numeric checks for AirMonitor Compact V0.8 edge-guide revision."""
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
    check('wall increased', C.WALL >= 3.0)
    check('floor increased', C.FLOOR >= 3.0)
    check('matching outer footprint', close(C.LID_X0, 0.0) and close(C.LID_X1, C.L) and close(C.LID_Y0, 0.0) and close(C.LID_Y1, C.W))
    check('matching external radius', close(C.BODY_CORNER_R, C.LID_CORNER_R))
    check('rounded corners', C.BODY_CORNER_R >= 4.0)
    check('no lid columns', C.NO_LID_COLUMNS)
    check('no centre fixings', C.NO_CENTER_FIXINGS)
    check('shoulder height 10 mm', close(C.SHOULDER_H, 10.0))
    check('lid overlap 10 mm', close(C.LID_OVERLAP, 10.0))
    check('left insertion end open', C.LID_LEFT_END_OPEN)
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
    check('slide close direction retained for sensor clearance', C.SLIDE_CLOSE_DIRECTION == '-X')
    check('operating-view direction documented', 'left-to-right' in C.SLIDE_USER_DIRECTION)
    check('lug ramp 45 degrees', close(C.SIDE_LUG_RAMP, C.SIDE_LUG_PROJ))
    check('slot entry wider than lug', C.SLOT_ENTRY_W > C.SIDE_LUG_WIDTH)
    check('slot track covers lug height', C.SLOT_TRACK_Z0 < C.SIDE_LUG_Z0 and C.SLOT_TRACK_Z1 > C.SIDE_LUG_Z1)
    check('three guide lugs', len(C.SIDE_LUG_X_FRONT) + len(C.SIDE_LUG_X_REAR) == 3)
    all_lugs = tuple(C.SIDE_LUG_X_FRONT) + tuple(C.SIDE_LUG_X_REAR)
    for i, x in enumerate(all_lugs, 1):
        check(f'lug {i} in edge zone', x <= 25.0 or x >= C.L-25.0, f'X={x}')
        entry = x-C.SLIDE_TRAVEL
        check(f'lug {i} entry inside lid', entry-C.SLOT_ENTRY_W/2 >= C.LID_X0 and entry+C.SLOT_ENTRY_W/2 <= C.LID_X1)
    check('no lug in centre 25..183', all(not (25.0 < x < C.L-25.0) for x in all_lugs))

    tx0, tx1 = C.LATCH_TONGUE_X
    ty0, ty1 = C.LATCH_TONGUE_Y
    hx, hy, _ = C.LATCH_HOLE
    px, py = C.LATCH_PIN
    pin_h = sum(h for _, h in C.LATCH_PIN_SEGMENTS)
    tongue_under = C.LID_Z + C.LID_T - C.LATCH_TONGUE_SKIN
    interference = C.H + pin_h - tongue_under
    check('latch aligned', close(hx, px) and close(hy, py))
    check('latch at right edge zone', px >= C.L-30.0, f'X={px}')
    check('latch hole in tongue', tx0 < hx < tx1 and ty0 <= hy <= ty1)
    check('tongue printable skin', 1.0 <= C.LATCH_TONGUE_SKIN <= 1.4)
    check('snap interference', 0.2 <= interference <= 0.6, f'{interference:.2f}')
    check('pin outside tongue before close', px < tx0 + C.SLIDE_OPEN_OFFSET_X)

    check('ZERO-SPAN 16 mm', close(C.SPAN[0]-C.ZERO[0], 16.0))
    check('ZERO/SPAN height retained', close(C.ZERO[1],26.0) and close(C.SPAN[1],26.0))
    check('button holder pattern retained', C.BTN_HOLDER_Y == (18.0,94.0) and C.BTN_HOLDER_Z == (20.0,36.0))
    check('Waveshare X pattern', close(C.STANDOFFS[1][0]-C.STANDOFFS[0][0],145.0))
    check('Waveshare Y pattern', close(C.STANDOFFS[2][1]-C.STANDOFFS[0][1],62.0))

    px0, px1, py0, py1, *_ = C.POD
    check('P03 closed X retained', close(px0,6.0) and close(px1,59.5))
    check('P03 open service X inside base', px0+C.SLIDE_OPEN_OFFSET_X >= C.WALL and px1+C.SLIDE_OPEN_OFFSET_X <= C.L-C.WALL)
    check('P03 Y centred', close((py0+py1)/2, C.W/2))
    hx0,hx1,hy0,hy1=C.HOOD_PLATE
    check('P07 X retained', close(hx0,4.0) and close(hx1,60.0))
    check('P07 Y centred', close((hy0+hy1)/2, C.W/2))

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
