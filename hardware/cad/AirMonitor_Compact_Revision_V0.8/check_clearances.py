"""Numeric checks for AirMonitor Compact V0.8 captured 45-degree guides."""
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
        return abs(a-b) <= tol

    check('base length fits MK4', C.L <= 250.0)
    check('base total width fits MK4', C.W + 2*C.FLANGE <= 210.0)
    check('base height fits MK4', C.H <= 220.0)
    check('lid footprint fits MK4', C.LID_X1-C.LID_X0 <= 250.0 and C.LID_Y1-C.LID_Y0 <= 210.0)
    check('wall at least 3.2', C.WALL >= 3.2)
    check('floor at least 3.2', C.FLOOR >= 3.2)
    check('rounded matching footprint', close(C.LID_X0,0.0) and close(C.LID_X1,C.L) and close(C.LID_Y0,0.0) and close(C.LID_Y1,C.W))
    check('matching radius', close(C.BODY_CORNER_R,C.LID_CORNER_R))
    check('no lid columns', C.NO_LID_COLUMNS)
    check('no centre fixings', C.NO_CENTER_FIXINGS)
    check('shoulder height 10', close(C.SHOULDER_H,10.0))
    check('overlap 10', close(C.LID_OVERLAP,10.0))
    check('left insertion side open', C.LID_LEFT_END_OPEN)
    check('side opening reaches top edge', close(C.OPEN_TOP_Z,C.H))
    check('side opening has no upper bridge', C.NO_SIDE_OPENING_BRIDGE)
    check('side opening is 122 x 43',
          close(C.OPEN_X1-C.OPEN_X0,122.0) and close(C.OPEN_TOP_Z-C.OPEN_Z,43.0))
    check('full shoulder-cut flag', C.SIDE_OPEN_CUT_THROUGH_SHOULDER)
    check('full side cut reaches front shoulder inner edge',
          C.SIDE_OPEN_FRONT_Y1 >= C.SHOULDER_INSET + C.WALL)
    check('full side cut reaches rear shoulder inner edge',
          C.SIDE_OPEN_REAR_Y0 <= C.W - C.SHOULDER_INSET - C.WALL)
    check('front cut begins outside body', C.SIDE_OPEN_FRONT_Y0 < 0.0)
    check('rear cut ends outside body', C.SIDE_OPEN_REAR_Y1 > C.W)

    clearance = C.SHOULDER_INSET-C.LID_SKIRT_W
    check('shoulder/skirt clearance 0.30', close(clearance,0.30), f'{clearance:.3f}')
    check('skirt thick enough', C.LID_SKIRT_W >= 2.5)
    check('visible top flat', C.LID_TOP_FACE_FLAT)
    check('visible top is bed face', C.LID_PRINT_TOP_FACE_DOWN)

    check('slide travel retained', close(C.SLIDE_TRAVEL,8.0))
    check('close direction retained', C.SLIDE_CLOSE_DIRECTION == '-X')
    check('user direction retained', 'left-to-right' in C.SLIDE_USER_DIRECTION)
    check('guide mode captured', 'captured' in C.GUIDE_MODE)
    check('four edge locations', C.GUIDE_X_FRONT == (18.0,190.0) and C.GUIDE_X_REAR == (18.0,190.0))
    for x in C.GUIDE_X_ALL:
        check(f'guide X{x:g} in edge zone', x <= 25.0 or x >= C.L-25.0)
    check('no visible windows', C.NO_VISIBLE_GUIDE_WINDOWS)
    check('no horizontal roofs', C.NO_HORIZONTAL_SLOT_ROOFS)
    check('guide angle 45', close(C.GUIDE_PRINT_ANGLE_DEG,45.0))
    check('lug lower face 45', close(C.GUIDE_PROJ,C.GUIDE_RISE))
    groove_dy = C.GUIDE_GROOVE_INNER_Y_FRONT-C.GUIDE_GROOVE_OUTER_Y_FRONT
    check('groove face 45', close(groove_dy,C.GUIDE_GROOVE_RISE), f'{groove_dy:.3f}/{C.GUIDE_GROOVE_RISE:.3f}')
    check('normal outside skin >=1.5', C.GUIDE_OUTER_SKIN >= 1.5)
    check('entry outside skin >=1.1', C.GUIDE_ENTRY_OUTER_SKIN >= 1.1)
    check('entry pocket reaches lower edge', C.GUIDE_ENTRY_BOTTOM_Z < C.LID_Z-C.LID_OVERLAP)
    check('entry pocket reaches inner top', C.GUIDE_ENTRY_TOP_Z >= C.LID_Z)
    check('entry wider than lug', C.GUIDE_ENTRY_W > C.GUIDE_LUG_W)
    check('track extends beyond closed lug', C.GUIDE_TRACK_END_EXTRA > C.GUIDE_LUG_W/2)

    normal_tip_front = C.SHOULDER_INSET-C.GUIDE_PROJ
    snap_tip_front = C.SHOULDER_INSET-C.GUIDE_PROJ-C.SNAP_EXTRA_PROJ
    normal_interference = C.GUIDE_GROOVE_OUTER_Y_FRONT-snap_tip_front
    detent_outer = C.GUIDE_GROOVE_OUTER_Y_FRONT-C.SNAP_DETENT_EXTRA_DEPTH
    detent_clearance = snap_tip_front-detent_outer
    check('normal guide clearance positive', normal_tip_front-C.GUIDE_GROOVE_OUTER_Y_FRONT >= 0.25)
    check('snap flex 0.15..0.30', 0.15 <= normal_interference <= 0.30, f'{normal_interference:.3f}')
    check('detent final clearance 0.10..0.30', 0.10 <= detent_clearance <= 0.30, f'{detent_clearance:.3f}')
    check('snap at right edge', C.SNAP_X >= C.L-25.0)
    check('snap hidden', C.NO_TOP_LATCH_TONGUE)

    check('ZERO-SPAN 16', close(C.SPAN[0]-C.ZERO[0],16.0))
    check('ZERO/SPAN height retained', close(C.ZERO[1],26.0) and close(C.SPAN[1],26.0))
    check('button holders retained', C.BTN_HOLDER_Y == (18.0,94.0) and C.BTN_HOLDER_Z == (20.0,36.0))
    check('Waveshare X pattern', close(C.STANDOFFS[1][0]-C.STANDOFFS[0][0],145.0))
    check('Waveshare Y pattern', close(C.STANDOFFS[2][1]-C.STANDOFFS[0][1],62.0))

    px0,px1,py0,py1,*_=C.POD
    check('P03 X retained', close(px0,6.0) and close(px1,59.5))
    check('P03 open X inside', px0+C.SLIDE_OPEN_OFFSET_X >= C.WALL and px1+C.SLIDE_OPEN_OFFSET_X <= C.L-C.WALL)
    check('P03 Y centred', close((py0+py1)/2,C.W/2))
    hx0,hx1,hy0,hy1=C.HOOD_PLATE
    check('P07 X retained', close(hx0,4.0) and close(hx1,60.0))
    check('P07 Y centred', close((hy0+hy1)/2,C.W/2))

    check('O-ring cord', close(C.ORING_CORD,1.50))
    check('groove wider than cord', C.ORING_GROOVE_W > C.ORING_CORD)
    check('compression 20-30 percent', 0.20 <= C.ORING_COMPRESSION <= 0.30)
    def stretch(r):
        path=2*(r['cw']+r['ch'])+(2*math.pi-8)*r['r']
        free=math.pi*(r['id']+r['cord'])
        return path/free-1
    for ring in (C.P04A_RING,C.P04B_RING,C.P08_RING):
        s=stretch(ring)
        check(f"{ring['name']} path stretch", -0.005 <= s <= 0.03, f'{s*100:.2f}%')
        check(f"{ring['name']} radius", ring['r'] >= 3*ring['cord'])

    if failures:
        print(f'V0.8 checks: {passed} passed, {len(failures)} FAILED')
        for item in failures:
            print('FAIL',item)
        return 1
    print(f'V0.8 checks: {passed} passed, 0 failed')
    return 0


if __name__ == '__main__':
    raise SystemExit(run())
