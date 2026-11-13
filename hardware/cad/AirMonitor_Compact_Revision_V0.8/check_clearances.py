"""Numeric checks for AirMonitor Compact V0.8 open-bottom snap revision."""
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
    check('no C bottom lip flag', C.NO_C_BOTTOM_LIP)
    check('two open-edge notches', C.OPEN_EDGE_NOTCH_X == (18.0, 190.0))
    check('notches reach below skirt edge',
          C.OPEN_EDGE_NOTCH_Z0 < C.LID_Z - C.LID_OVERLAP)
    check('notch width printable', C.OPEN_EDGE_NOTCH_W >= 7.0)
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
    check('slide close direction retained', C.SLIDE_CLOSE_DIRECTION == '-X')
    check('operating-view direction documented', 'left-to-right' in C.SLIDE_USER_DIRECTION)
    check('continuous shoulder guide', 'shoulder' in C.GUIDE_MODE)
    check('no C channels', C.NO_C_CHANNELS and C.NO_CLOSED_SIDE_CHANNELS)
    check('no horizontal slot roofs', C.NO_HORIZONTAL_SLOT_ROOFS)
    check('former guide arrays empty', len(C.SIDE_LUG_X_FRONT) == 0 and len(C.SIDE_LUG_X_REAR) == 0)
    check('top latch removed', C.NO_TOP_LATCH_TONGUE)

    check('snap at right edge zone', C.EDGE_SNAP_X >= C.L-25.0, f'X={C.EDGE_SNAP_X}')
    check('snap ramp 45 degrees', close(C.EDGE_SNAP_RAMP, C.EDGE_SNAP_PROJ))
    check('notch wider than bump', C.EDGE_SNAP_NOTCH_W > C.EDGE_SNAP_WIDTH)
    check('notch open at skirt bottom', close(C.EDGE_SNAP_NOTCH_Z0, C.LID_Z-C.LID_OVERLAP))
    check('notch covers bump vertically', C.EDGE_SNAP_NOTCH_Z0 <= C.EDGE_SNAP_Z0 and C.EDGE_SNAP_NOTCH_Z1 >= C.EDGE_SNAP_Z1)
    check('notch is straight vertical cut', C.NO_HORIZONTAL_SLOT_ROOFS)
    front_clearance = C.SHOULDER_INSET - C.LID_IN_Y0
    snap_interference = C.EDGE_SNAP_PROJ - front_clearance
    check('snap flex 0.3..0.6 mm', 0.30 <= snap_interference <= 0.60, f'{snap_interference:.3f}')
    check('snap notch inside lid', C.EDGE_SNAP_X-C.EDGE_SNAP_NOTCH_W/2 >= C.LID_X0 and C.EDGE_SNAP_X+C.EDGE_SNAP_NOTCH_W/2 <= C.LID_X1)

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
