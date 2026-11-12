"""Numeric checks for AirMonitor Compact V0.7 corrected O-ring revision."""
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

    # Main geometry.
    check('base length fits MK4', C.L <= 250.0, f'{C.L}')
    check('base total width fits MK4', C.W + 2 * C.FLANGE <= 210.0,
          f'{C.W + 2 * C.FLANGE}')
    check('base height fits MK4', C.H <= 220.0, f'{C.H}')
    check('wall positive', C.WALL > 0)
    check('floor positive', C.FLOOR > 0)
    check('long-wall opening ordered', C.OPEN_X0 < C.OPEN_X1)
    check('long-wall opening in base', 0 < C.OPEN_X0 < C.OPEN_X1 < C.L)
    check('opening height valid', 0 < C.OPEN_Z < C.H)

    # Corrected positioning: X unchanged, Y centred.
    px0, px1, py0, py1, pz0, pz1 = C.POD
    check('pod X left retained', close(px0, 6.0), f'{px0}')
    check('pod X widened right', close(px1, 59.5), f'{px1}')
    check('pod Y centred', close((py0 + py1) / 2, C.W / 2),
          f'{(py0 + py1) / 2} vs {C.W / 2}')
    hx0, hx1, hy0, hy1 = C.HOOD_PLATE
    check('hood X left retained', close(hx0, 4.0), f'{hx0}')
    check('hood X widened right', close(hx1, 60.0), f'{hx1}')
    check('hood Y centred', close((hy0 + hy1) / 2, C.W / 2),
          f'{(hy0 + hy1) / 2}')
    check('hood centre Y', close(C.HOOD_CENTER[1], C.W / 2),
          f'{C.HOOD_CENTER[1]}')
    check('vents centred Y', close((C.VENTS[0][1] + C.VENTS[-1][1] + C.VENTS[-1][3]) / 2,
                                   C.W / 2),
          'vent pattern centre mismatch')
    check('hood screws symmetric Y', close(sum(y for _, y in C.HOOD_SCREWS) / 2, C.W / 2))

    # Board and wall hardware.
    check('Waveshare X pattern', close(C.STANDOFFS[1][0] - C.STANDOFFS[0][0], 145.0))
    check('Waveshare Y pattern', close(C.STANDOFFS[2][1] - C.STANDOFFS[0][1], 62.0))
    check('button holder X wall clearance', C.BTN_HOLDER_LEN > 0)
    check('ZERO-SPAN 16 mm', close(C.SPAN[0] - C.ZERO[0], 16.0))
    check('DC bore valid', C.DC5521[2] > 0)

    # Seal/groove fundamentals.
    check('O-ring cord', close(C.ORING_CORD, 1.50))
    check('groove wider than cord', C.ORING_GROOVE_W > C.ORING_CORD)
    check('groove depth below cord', 0 < C.ORING_GROOVE_D < C.ORING_CORD)
    check('compression 20-30 percent', 0.20 <= C.ORING_COMPRESSION <= 0.30,
          f'{C.ORING_COMPRESSION:.3f}')
    check('hood material below groove', C.HOOD_PLATE_T - C.ORING_GROOVE_D >= 1.8,
          f'{C.HOOD_PLATE_T - C.ORING_GROOVE_D:.2f}')
    check('pod wall below groove', C.POD_WALL - C.ORING_GROOVE_D >= 1.8,
          f'{C.POD_WALL - C.ORING_GROOVE_D:.2f}')
    check('lid remains un-grooved full thickness', close(C.LID_T, 3.0))
    check('hood contacts lid', close(C.HOOD_Z0, C.LID_Z + C.LID_T))
    check('pod seal rim contacts lid', close(C.POD_SEAL_RIM_TOP, C.LID_Z))

    def ring_metrics(ring: dict) -> tuple[float, float, float]:
        path = 2.0 * (ring['cw'] + ring['ch']) + (2.0 * math.pi - 8.0) * ring['r']
        free = math.pi * (ring['id'] + ring['cord'])
        stretch = path / free - 1.0
        return path, free, stretch

    for ring in (C.P04A_RING, C.P04B_RING, C.P08_RING):
        path, free, stretch = ring_metrics(ring)
        check(f"{ring['name']} path stretch", -0.005 <= stretch <= 0.03,
              f'path={path:.3f}, free={free:.3f}, stretch={stretch*100:.2f}%')
        check(f"{ring['name']} radius", ring['r'] >= 3.0 * ring['cord'],
              f"r={ring['r']}")
        check(f"{ring['name']} groove width", C.ORING_GROOVE_W >= ring['cord'] + 0.2)

    # P04 grooves fit the hood plate.
    def channel_bounds(ring: dict, width: float) -> tuple[float, float, float, float]:
        return (ring['cx'] - ring['cw'] / 2 - width / 2,
                ring['cx'] + ring['cw'] / 2 + width / 2,
                ring['cy'] - ring['ch'] / 2 - width / 2,
                ring['cy'] + ring['ch'] / 2 + width / 2)

    for ring in (C.P04A_RING, C.P04B_RING):
        x0, x1, y0, y1 = channel_bounds(ring, C.ORING_GROOVE_W)
        check(f"{ring['name']} groove X in hood", hx0 <= x0 and x1 <= hx1,
              f'{x0:.2f}..{x1:.2f} vs {hx0}..{hx1}')
        check(f"{ring['name']} groove Y in hood", hy0 <= y0 and y1 <= hy1,
              f'{y0:.2f}..{y1:.2f} vs {hy0}..{hy1}')

    a = channel_bounds(C.P04A_RING, C.ORING_GROOVE_W)
    b = channel_bounds(C.P04B_RING, C.ORING_GROOVE_W)
    check('P04 groove separation', a[3] < b[2], f'{a[3]:.2f} / {b[2]:.2f}')
    check('divider width 5 mm', close(C.HOOD_DIVIDER_Y[1] - C.HOOD_DIVIDER_Y[0], 5.0))

    # P08 groove fits the 3 mm pod sealing rim.
    x0, x1, y0, y1 = channel_bounds(C.P08_RING, C.ORING_GROOVE_W)
    check('P08 groove X in pod wall', px0 <= x0 and x1 <= px1,
          f'{x0:.2f}..{x1:.2f} vs {px0}..{px1}')
    check('P08 groove Y in pod wall', py0 <= y0 and y1 <= py1,
          f'{y0:.2f}..{y1:.2f} vs {py0}..{py1}')
    inner_x0 = C.P08_RING['cx'] - (C.P08_RING['cw'] - C.ORING_GROOVE_W) / 2
    inner_x1 = C.P08_RING['cx'] + (C.P08_RING['cw'] - C.ORING_GROOVE_W) / 2
    inner_y0 = C.P08_RING['cy'] - (C.P08_RING['ch'] - C.ORING_GROOVE_W) / 2
    inner_y1 = C.P08_RING['cy'] + (C.P08_RING['ch'] - C.ORING_GROOVE_W) / 2
    check('P08 groove avoids cavity X', inner_x0 <= px0 + C.POD_WALL + 0.2 and
          inner_x1 >= px1 - C.POD_WALL - 0.2,
          f'{inner_x0:.2f}/{inner_x1:.2f}')
    check('P08 groove avoids cavity Y', inner_y0 <= py0 + C.POD_WALL + 0.2 and
          inner_y1 >= py1 - C.POD_WALL - 0.2,
          f'{inner_y0:.2f}/{inner_y1:.2f}')

    # Openings and ports.
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
