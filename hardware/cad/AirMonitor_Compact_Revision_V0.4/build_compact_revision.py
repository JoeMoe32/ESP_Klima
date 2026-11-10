"""Laminar AirMonitor HCHO – Compact CAD revision V0.4.

CadQuery source for the confirmed arrangement:
- SEN0661 holder center-left above the Waveshare board
- SEN0661 PCB centered in the holder
- Gravity connector underneath the PCB
- cable routed downward
- compact calibration hood with two ports on the left
"""
from pathlib import Path
import csv
import sys

import cadquery as cq
from cadquery import exporters

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import compact_params as C  # noqa: E402
import check_clearances  # noqa: E402

if check_clearances.run() != 0:
    raise SystemExit('Aborted: V0.4 clearance check failed.')

G = R / '01_CAD_Global'
P = R / '02_CAD_Print'
D = R / '03_Renders_Drawings'
for directory in (G, P, D):
    directory.mkdir(parents=True, exist_ok=True)
REV = 'V0.4'


def box(x, y, z, lx, ly, lz):
    return cq.Workplane('XY').box(lx, ly, lz, centered=(False, False, False)).translate((x, y, z))


def bb(x0, x1, y0, y1, z0, z1):
    return box(x0, y0, z0, x1 - x0, y1 - y0, z1 - z0)


def cz(x, y, z, d, h):
    return cq.Workplane('XY', origin=(x, y, z)).circle(d / 2).extrude(h)


def cx(x, y, z, d, h):
    return cq.Workplane('YZ', origin=(x, 0, 0)).center(y, z).circle(d / 2).extrude(h)


def export_step(shape, path):
    exporters.export(shape, str(path), exportType='STEP')


def export_stl(shape, path):
    exporters.export(shape, str(path), exportType='STL', tolerance=.08, angularTolerance=.15)


def to_origin(shape):
    b = shape.val().BoundingBox()
    return shape.translate((-b.xmin, -b.ymin, -b.zmin))


L, W, H = C.L, C.W, C.H
wall, floor = C.WALL, C.FLOOR

# P01 – base enclosure
base = box(0, 0, 0, L, W, floor)
for wall_shape in (
    box(0, 0, 0, wall, W, H),
    box(L - wall, 0, 0, wall, W, H),
    box(0, 0, 0, L, wall, H),
    box(0, W - wall, 0, L, wall, H),
):
    base = base.union(wall_shape)
base = base.union(box(0, -C.FLANGE, 0, L, C.FLANGE, floor))
base = base.union(box(0, W, 0, L, C.FLANGE, floor))
for x, y in C.WALL_MOUNT_HOLES:
    base = base.cut(cz(x, y, -.2, C.WALL_MOUNT_D, floor + .5))
for y in (-.5, W - wall - .5):
    base = base.cut(box(C.OPEN_X0, y, C.OPEN_Z, C.OPEN_X1 - C.OPEN_X0, wall + 1, H - C.OPEN_Z + 1))
for x, y in C.LID_BOSSES:
    base = base.union(cz(x, y, floor, C.LID_BOSS_D, H - floor))
    base = base.cut(cz(x, y, floor - .2, C.LID_BOSS_PILOT_D, H - floor + .5))
for x, y in C.STANDOFFS:
    base = base.union(cz(x, y, floor, C.STANDOFF_D, C.BOARD_BOTTOM_Z - floor))
    base = base.cut(cz(x, y, floor - .2, C.STANDOFF_PILOT_D, C.BOARD_BOTTOM_Z - floor + .5))
jack_y, jack_z, jack_d = C.DC5521
base = base.cut(cx(L - wall - .2, jack_y, jack_z, jack_d, wall + .5))
for y, z, d in (C.ZERO, C.SPAN):
    base = base.cut(cx(L - wall - .2, y, z, d, wall + .5))
holder_x = L - wall - C.BTN_HOLDER_LEN
for y in C.BTN_HOLDER_Y:
    for z in C.BTN_HOLDER_Z:
        base = base.union(cx(holder_x, y, z, C.BTN_HOLDER_D, C.BTN_HOLDER_LEN))
        base = base.cut(cx(holder_x - .2, y, z, C.BTN_HOLDER_PILOT_D, C.BTN_HOLDER_LEN + .5))

# P02 – main lid
lid = box(0, 0, C.LID_Z, L, W, C.LID_T)
for x, y, lx, ly in C.VENTS:
    lid = lid.cut(box(x, y, C.LID_Z - .5, lx, ly, C.LID_T + 1))
for x, y in C.LID_BOSSES:
    lid = lid.cut(cz(x, y, C.LID_Z - .5, C.LID_HOLE_D, C.LID_T + 1))
    lid = lid.cut(cz(x, y, C.LID_Z + C.LID_T - C.LID_CBORE_DEPTH,
                     C.LID_CBORE_D, C.LID_CBORE_DEPTH + .3))
for x, y in C.POD_MOUNTS:
    lid = lid.union(cz(x, y, C.POD_BOSS_Z0, C.POD_BOSS_D, C.LID_Z - C.POD_BOSS_Z0))
    lid = lid.cut(cz(x, y, C.POD_BOSS_Z0 - .1, C.POD_BOSS_PILOT_D,
                     C.POD_BOSS_PILOT_TOP - C.POD_BOSS_Z0 + .1))
for x, y in C.HOOD_SCREWS:
    lid = lid.cut(cz(x, y, C.LID_Z - .5, 2.2, C.LID_T + 1.0))

# P03 – compact sensor holder, center-left, connector underneath PCB
px0, px1, py0, py1, pz0, pz1 = C.POD
t = C.POD_WALL
pod = bb(px0, px1, py0, py1, pz0, pz1)
pod = pod.cut(bb(px0 + t, px1 - t, py0 + t, py1 - t, pz0 + t, pz1 + 1))
for ty in (C.TONGUE_FRONT_Y, C.TONGUE_BACK_Y):
    pod = pod.union(bb(*C.TONGUE_X, *ty, *C.TONGUE_Z))
for x, y in C.POD_MOUNTS:
    pod = pod.cut(cz(x, y, C.TONGUE_Z[0] - .5, C.TONGUE_HOLE_D,
                     C.TONGUE_Z[1] - C.TONGUE_Z[0] + 1.0))
for x, y in C.HOOD_SCREWS:
    pod = pod.union(cz(x, y, pz0 + t, C.HOOD_SCREW_BOSS_D, pz1 - (pz0 + t)))
    pod = pod.cut(cz(x, y, pz0 + t - .2, C.HOOD_SCREW_PILOT_D,
                     pz1 - (pz0 + t) + .5))
for x, y in C.SENSOR_BOSSES:
    pod = pod.union(cz(x, y, pz0 + t, C.SENSOR_BOSS_D,
                       C.SENSOR_BOSS_TOP - (pz0 + t)))
    pod = pod.cut(cz(x, y, pz0 + t - .2, C.SENSOR_HOLE_D,
                     C.SENSOR_BOSS_TOP - (pz0 + t) + .5))
pod = pod.cut(bb(*C.GRAVITY_SLOT))
pod = pod.cut(bb(*C.CABLE_CHANNEL))

# P08, P04 and P05 seals
g = C.P08
pod_gasket = bb(*g['x'], *g['y'], g['z0'], g['z0'] + g['t'])
pod_gasket = pod_gasket.cut(
    bb(g['x'][0] + g['web'], g['x'][1] - g['web'],
       g['y'][0] + g['web'], g['y'][1] - g['web'],
       g['z0'] - .2, g['z0'] + g['t'] + .2)
)
cable_stop = bb(*C.P05_OUTER).cut(bb(*C.P05_CABLE_SLOT))
hg = C.P04
hood_gasket = bb(*hg['x'], *hg['y'], hg['z0'], hg['z0'] + hg['t'])
wx0, wx1 = hg['x'][0] + hg['web'], hg['x'][1] - hg['web']
for wy0, wy1 in ((hg['y'][0] + hg['web'], hg['bar_y'][0]),
                 (hg['bar_y'][1], hg['y'][1] - hg['web'])):
    hood_gasket = hood_gasket.cut(bb(wx0, wx1, wy0, wy1, hg['z0'] - .2, hg['z0'] + hg['t'] + .2))

# P07 – compact calibration hood, two ports on left
hz0 = C.HOOD_Z0
plate_top = hz0 + C.HOOD_PLATE_T
hx0, hx1, hy0, hy1 = C.HOOD_PLATE
hood = bb(hx0, hx1, hy0, hy1, hz0, plate_top)
fo = C.HOOD_FLOOR_OPEN
hood = hood.cut(bb(fo[0], fo[1], fo[2], fo[3], hz0 - .2, plate_top + .2))
for x, y in C.HOOD_SCREWS:
    hood = hood.cut(cz(x, y, hz0 - .3, 2.2, C.HOOD_PLATE_T + .6))
(ob, ot, oh), (ib, it, ih) = C.HOOD_OUT, C.HOOD_IN
cxh, cyh = C.HOOD_CENTER
outer = (cq.Workplane('XY', origin=(0, 0, plate_top))
         .center(cxh, cyh).rect(*ob)
         .workplane(offset=oh).rect(*ot).loft())
inner = (cq.Workplane('XY', origin=(0, 0, plate_top - .2))
         .center(cxh, cyh).rect(*ib)
         .workplane(offset=ih).rect(*it).loft())
rx, ry, rlx, rly, rt = C.HOOD_ROOF
hood = hood.union(outer).cut(inner).union(box(rx, ry, plate_top + oh, rlx, rly, rt))
dx0, dx1 = C.HOOD_DIVIDER_X
dy0, dy1 = C.HOOD_DIVIDER_Y
hood = hood.union(bb(dx0, dx1, dy0, dy1, plate_top - .1, plate_top + ih - .1))
inner_top = plate_top - .2 + ih
roof_top = plate_top + oh + rt
for x, y in C.HOOD_PORTS.values():
    hood = hood.cut(cz(x, y, inner_top - 1.0, C.HOOD_PORT_D, roof_top - inner_top + 5.0))
    z = roof_top
    for d, height in C.HOOD_NOZZLE:
        hood = hood.union(cz(x, y, z, d, height))
        z += height
    hood = hood.cut(cz(x, y, inner_top - 1.0, C.HOOD_PORT_D, z - inner_top + 1.0))

parts = {
    'P01_Compact_Base_Global': base,
    'P02_Compact_Lid_Global': lid,
    'P03_CenterLeft_SensorHolder_Global': pod,
    'P04_Compact_Hood_Gasket_TPU': hood_gasket,
    'P05_UnderPCB_Cable_Seal': cable_stop,
    'P07_Compact_Calibration_Hood': hood,
    'P08_Pod_Lid_Gasket_Global': pod_gasket,
}
print_names = {
    'P01_Compact_Base_Global': 'P01_Compact_Base_Print',
    'P02_Compact_Lid_Global': 'P02_Compact_Lid_Print',
    'P03_CenterLeft_SensorHolder_Global': 'P03_CenterLeft_SensorHolder_Print',
    'P04_Compact_Hood_Gasket_TPU': 'P04_Compact_Hood_Gasket_TPU_Print',
    'P05_UnderPCB_Cable_Seal': 'P05_UnderPCB_Cable_Seal_Print',
    'P07_Compact_Calibration_Hood': 'P07_Compact_Calibration_Hood_Print',
    'P08_Pod_Lid_Gasket_Global': 'P08_Pod_Lid_Gasket_Print',
}
flip = {'P02_Compact_Lid_Global'}
for name, shape in parts.items():
    export_step(shape, G / f'{name}.step')
for name, shape in parts.items():
    print_shape = shape.rotate((0, 0, 0), (1, 0, 0), 180) if name in flip else shape
    print_shape = to_origin(print_shape)
    export_step(print_shape, P / f'{print_names[name]}.step')
    export_stl(print_shape, P / f'{print_names[name]}.stl')
assembly_shapes = [shape.val() for shape in parts.values()]
assembly = cq.Workplane(obj=cq.Compound.makeCompound(assembly_shapes))
export_step(assembly, G / f'AirMonitor_Compact_Assembly_{REV}.step')
dummies = [
    bb(*C.CARRIER), bb(*C.PCB_WAVESHARE), bb(*C.SEN_PCB), bb(*C.SEN_TOP),
    bb(*C.SEN_CON), bb(*C.BTN_PCB_DUMMY),
]
reference = cq.Workplane(obj=cq.Compound.makeCompound(assembly_shapes + [d.val() for d in dummies]))
export_step(reference, G / f'AirMonitor_Compact_Reference_With_Dummies_{REV}.step')

with (R / 'DIMENSIONS.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['part', 'x_len', 'y_len', 'z_len', 'x_min', 'x_max',
                     'y_min', 'y_max', 'z_min', 'z_max', 'volume_mm3'])
    for name, shape in parts.items():
        solid = shape.val(); b = solid.BoundingBox()
        writer.writerow([name, *[f'{value:.3f}' for value in (
            b.xlen, b.ylen, b.zlen, b.xmin, b.xmax, b.ymin, b.ymax,
            b.zmin, b.zmax, solid.Volume())]])

top_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="-10 -20 228 152"><style>text{font-family:Arial;font-size:5px}.a{fill:none;stroke:#12385b;stroke-width:.8}.b{fill:#cfe1ef;stroke:#12385b}.c{fill:#f0c774;stroke:#12385b}.d{fill:#ddd;stroke:#333}</style><rect class="a" x="0" y="0" width="208" height="112"/><rect class="b" x="10" y="11" width="175" height="90"/><rect class="c" x="44" y="34" width="60" height="44"/><rect class="d" x="58" y="45" width="32" height="22"/><rect class="a" x="81" y="52" width="8" height="8"/><text x="3" y="-5">Laminar AirMonitor HCHO – V0.4 top view [mm]</text><text x="68" y="58">SEN0661 PCB</text><text x="82" y="57">connector below</text><text x="118" y="58">Waveshare</text></svg>'''
side_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="-10 -8 228 115"><style>text{font-family:Arial;font-size:5px}.a{fill:none;stroke:#12385b;stroke-width:.8}.b{fill:#cfe1ef;stroke:#12385b}.c{fill:#f0c774;stroke:#12385b}.d{fill:#ddd;stroke:#333}.e{fill:#aaa;stroke:#333}</style><rect class="a" x="0" y="0" width="208" height="55"/><rect class="b" x="10" y="9.6" width="175" height="18"/><rect class="c" x="44" y="40" width="60" height="14"/><rect class="d" x="58" y="45" width="32" height="1.6"/><rect class="e" x="81" y="40.6" width="8" height="4.4"/><rect class="a" x="42" y="58.9" width="64" height="35"/><text x="3" y="-3">Laminar AirMonitor HCHO – V0.4 side view [mm]</text><text x="60" y="43">holder</text><text x="60" y="50">PCB</text><text x="82" y="43">connector below</text></svg>'''
(D / 'Drawing_V0.4_Top_View.svg').write_text(top_svg, encoding='utf-8')
(D / 'Drawing_V0.4_Side_View.svg').write_text(side_svg, encoding='utf-8')
print(f'Generated {REV} in {R}')
