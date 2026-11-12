"""Numeric checks for AirMonitor Compact V0.7 sliding-lid revision."""
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
