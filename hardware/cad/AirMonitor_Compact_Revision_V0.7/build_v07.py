"""Build Laminar AirMonitor HCHO Compact V0.7 (CadQuery).

Generates global STEP, print-oriented STEP/STL, SVG review drawings and CSV data.
V0.7 implements the corrections from the annotated V0.6 1:1 drawings and
changes P04/P08 to rounded TPU 95A D-profile seals in locating grooves.
"""
from pathlib import Path
import csv
import shutil
import sys

import cadquery as cq
from cadquery import exporters

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import compact_params as C  # noqa: E402
import check_clearances  # noqa: E402

if check_clearances.run() != 0:
    raise SystemExit('Abbruch: V0.7 Mass-/Freiraumprüfung fehlgeschlagen.')

G = R / '01_CAD_Global'
P = R / '02_CAD_Print'
D = R / '03_Renders_Drawings'
for pth in (G, P, D):
    pth.mkdir(parents=True, exist_ok=True)
    for child in pth.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
REV = 'V0.7'


def box(x, y, z, l, w, h):
    return cq.Workplane('XY').box(l, w, h, centered=(False, False, False)).translate((x, y, z))


def bb(x0, x1, y0, y1, z0, z1):
    return box(x0, y0, z0, x1 - x0, y1 - y0, z1 - z0)


def cz(x, y, z, d, h):
    return cq.Workplane('XY', origin=(x, y, z)).circle(d / 2).extrude(h)


def cx(x, y, z, d, h):
    return cq.Workplane('YZ', origin=(x, 0, 0)).center(y, z).circle(d / 2).extrude(h)


def step(shape, path):
    exporters.export(shape, str(path), exportType='STEP')


def stl(shape, path):
    exporters.export(shape, str(path), exportType='STL', tolerance=.08, angularTolerance=.15)


def origin(shape):
    b = shape.val().BoundingBox()
    return shape.translate((-b.xmin, -b.ymin, -b.zmin))


def rounded_prism(x0, x1, y0, y1, r, z0, h):
    """Axis-aligned rounded rectangle prism."""
    r = max(0.0, min(r, (x1 - x0) / 2, (y1 - y0) / 2))
    if r <= 1e-9:
        return bb(x0, x1, y0, y1, z0, z0 + h)
    s = box(x0 + r, y0, z0, (x1 - x0) - 2 * r, y1 - y0, h)
    s = s.union(box(x0, y0 + r, z0, x1 - x0, (y1 - y0) - 2 * r, h))
    for x in (x0 + r, x1 - r):
        for y in (y0 + r, y1 - r):
            s = s.union(cz(x, y, z0, 2 * r, h))
    return s


def rounded_ring(x0, x1, y0, y1, web, corner_r, z0, h):
    outer = rounded_prism(x0, x1, y0, y1, corner_r, z0, h)
    ir = max(0.5, corner_r - web)
    inner = rounded_prism(x0 + web, x1 - web, y0 + web, y1 - web,
                          ir, z0 - 0.1, h + 0.2)
    return outer.cut(inner)


def d_profile_ring(cfg, add_bar=False):
    """Flat underside + rounded upper edges, printable without support."""
    x0, x1 = cfg['x']
    y0, y1 = cfg['y']
    z0 = cfg['z0']
    h = cfg['h']
    web = cfg['web']
    ring = rounded_ring(x0, x1, y0, y1, web, cfg['corner_r'], z0, h)
    # Round the upper inside and outside edges to approximate a D-shaped seal.
    try:
        ring = ring.edges('>Z').fillet(C.GASKET_TOP_FILLET)
    except Exception as exc:
        print('WARN gasket ring top fillet skipped:', exc)
    if add_bar:
        by0, by1 = cfg['bar_y']
        bar = bb(x0 + web, x1 - web, by0, by1, z0, z0 + h)
        try:
            bar = bar.edges('>Z').fillet(C.GASKET_TOP_FILLET)
        except Exception as exc:
            print('WARN gasket bar top fillet skipped:', exc)
        ring = ring.union(bar)
    return ring


def groove(cfg, z0, depth, add_bar=False):
    """Square-bottom locating groove with rounded plan corners."""
    c = C.GROOVE_CLEARANCE
    x0, x1 = cfg['x']
    y0, y1 = cfg['y']
    web = cfg['web']
    # Increase channel width by c on both sides.
    g = rounded_ring(x0 - c, x1 + c, y0 - c, y1 + c,
                     web + 2 * c, cfg['corner_r'] + c, z0, depth)
    if add_bar:
        by0, by1 = cfg['bar_y']
        g = g.union(bb(x0 + web - c, x1 - web + c,
                       by0 - c, by1 + c, z0, z0 + depth))
    return g


def outside_text_right(text, y, z, size=None):
    plane = cq.Plane(origin=(C.L, 0, 0), xDir=(0, 1, 0), normal=(1, 0, 0))
    return cq.Workplane(plane).center(y, z).text(
        text, size or C.MARK_FONT_SIZE, -C.MARK_DEPTH,
        font=C.MARK_FONT, halign='center', valign='center')


def outside_text_left(text, y, z, size=None):
    # Origin at Y=W and local +X toward global -Y makes text readable from -X.
    plane = cq.Plane(origin=(0, C.W, 0), xDir=(0, -1, 0), normal=(-1, 0, 0))
    return cq.Workplane(plane).center(C.W - y, z).text(
        text, size or C.MARK_FONT_SIZE, -C.MARK_DEPTH,
        font=C.MARK_FONT, halign='center', valign='center')


L, W, H, wall, floor = C.L, C.W, C.H, C.WALL, C.FLOOR

# ---------------- P01 enclosure base ----------------
b = box(0, 0, 0, L, W, floor)
for q in (box(0, 0, 0, wall, W, H), box(L - wall, 0, 0, wall, W, H),
          box(0, 0, 0, L, wall, H), box(0, W - wall, 0, L, wall, H)):
    b = b.union(q)
b = b.union(box(0, -C.FLANGE, 0, L, C.FLANGE, floor))
b = b.union(box(0, W, 0, L, C.FLANGE, floor))
for x, y in C.WALL_MOUNT_HOLES:
    b = b.cut(cz(x, y, -0.2, C.WALL_MOUNT_D, floor + 0.5))
for y in (-0.5, W - wall - 0.5):
    b = b.cut(box(C.OPEN_X0, y, C.OPEN_Z,
                  C.OPEN_X1 - C.OPEN_X0, wall + 1.0, H - C.OPEN_Z + 1.0))
for x, y in C.LID_BOSSES:
    b = b.union(cz(x, y, floor, C.LID_BOSS_D, H - floor))
    b = b.cut(cz(x, y, floor - 0.2, C.LID_BOSS_PILOT_D, H - floor + 0.5))
for x, y in C.STANDOFFS:
    b = b.union(cz(x, y, floor, C.STANDOFF_D, C.BOARD_BOTTOM_Z - floor))
    b = b.cut(cz(x, y, floor - 0.2, C.STANDOFF_PILOT_D,
                 C.BOARD_BOTTOM_Z - floor + 0.5))

# DC5521 on opposite/left end wall.
dy, dz, dd = C.DC5521
b = b.cut(cx(-0.2, dy, dz, dd, wall + 0.5))

# ZERO/SPAN and PCB holders remain on right end wall.
for y, z, d in (C.ZERO, C.SPAN):
    b = b.cut(cx(L - wall - 0.2, y, z, d, wall + 0.5))
hx = L - wall - C.BTN_HOLDER_LEN
for y in C.BTN_HOLDER_Y:
    for z in C.BTN_HOLDER_Z:
        b = b.union(cx(hx, y, z, C.BTN_HOLDER_D, C.BTN_HOLDER_LEN))
        b = b.cut(cx(hx - 0.2, y, z, C.BTN_HOLDER_PILOT_D,
                     C.BTN_HOLDER_LEN + 0.5))

# Updated physical markings.
for text, y, z in (('ZERO', C.ZERO[0], 47.5), ('SPAN', C.SPAN[0], 47.5)):
    try:
        b = b.cut(outside_text_right(text, y, z))
    except Exception as exc:
        print('WARN right-wall marking skipped:', text, exc)
try:
    b = b.cut(outside_text_left('24 V DC', C.DC5521[0], 38.0, 4.0))
    b = b.cut(outside_text_left('V0.7', 91.0, 8.0, 3.0))
except Exception as exc:
    print('WARN left-wall marking skipped:', exc)

# ---------------- P02 lid ----------------
lz, lt = C.LID_Z, C.LID_T
l = box(0, 0, lz, L, W, lt)
for x, y, lx, ly in C.VENTS:
    l = l.cut(box(x, y, lz - 0.5, lx, ly, lt + 1.0))
for x, y in C.LID_BOSSES:
    l = l.cut(cz(x, y, lz - 0.5, C.LID_HOLE_D, lt + 1.0))
    l = l.cut(cz(x, y, lz + lt - C.LID_CBORE_DEPTH,
                 C.LID_CBORE_D, C.LID_CBORE_DEPTH + 0.3))
for x, y in C.HOOD_SCREWS:
    l = l.union(cz(x, y, C.HOOD_SCREW_BOSS_Z0,
                   C.HOOD_SCREW_BOSS_D, lz - C.HOOD_SCREW_BOSS_Z0))
    l = l.cut(cz(x, y, C.HOOD_SCREW_BOSS_Z0 + 0.5,
                 C.HOOD_SCREW_PILOT_D,
                 lz + lt - C.HOOD_SCREW_BOSS_Z0))
for x, y in C.POD_MOUNTS:
    l = l.union(cz(x, y, C.POD_BOSS_Z0,
                   C.POD_BOSS_D, lz - C.POD_BOSS_Z0))
    l = l.cut(cz(x, y, C.POD_BOSS_Z0 - 0.1,
                 C.POD_BOSS_PILOT_D,
                 C.POD_BOSS_PILOT_TOP - C.POD_BOSS_Z0 + 0.1))

# Locating grooves: P08 underside and P04 topside.
groove8 = groove(C.P08, lz, C.GROOVE_DEPTH, add_bar=False)
groove4 = groove(C.P04, lz + lt - C.GROOVE_DEPTH, C.GROOVE_DEPTH, add_bar=True)
l = l.cut(groove8).cut(groove4)

# ---------------- P03 sensor pod ----------------
px0, px1, py0, py1, pz0, pz1 = C.POD
t = C.POD_WALL
p = bb(px0, px1, py0, py1, pz0, pz1)
p = p.cut(bb(px0 + t, px1 - t, py0 + t, py1 - t,
             pz0 + t, pz1 + 1.0))
for ty in (C.TONGUE_FRONT_Y, C.TONGUE_BACK_Y):
    p = p.union(bb(*C.TONGUE_X, *ty, *C.TONGUE_Z))
for x, y in C.POD_MOUNTS:
    p = p.cut(cz(x, y, C.TONGUE_Z[0] - 0.5, C.TONGUE_HOLE_D,
                 C.TONGUE_Z[1] - C.TONGUE_Z[0] + 1.0))
for x, y in C.SENSOR_BOSSES:
    p = p.union(cz(x, y, pz0 + t, C.SENSOR_BOSS_D,
                   C.SENSOR_BOSS_TOP - pz0 - t))
    p = p.cut(cz(x, y, pz0 + t - 0.5, C.SENSOR_HOLE_D,
                 C.SENSOR_BOSS_TOP - pz0 - t + 1.0))
p = p.cut(bb(*C.GRAVITY_SLOT))

# ---------------- P04 / P08 TPU seals and P05 cable stop ----------------
g4 = d_profile_ring(C.P04, add_bar=True)
g8 = d_profile_ring(C.P08, add_bar=False)
stop = bb(*C.P05)

# ---------------- P07 calibration hood ----------------
z0 = C.HOOD_Z0
pt = z0 + C.HOOD_PLATE_T
hx0, hx1, hy0, hy1 = C.HOOD_PLATE
cxh, cyh = C.HOOD_CENTER
h = bb(hx0, hx1, hy0, hy1, z0, pt)
fo = C.HOOD_FLOOR_OPEN
dv = C.HOOD_DIVIDER_Y
for oy in ((fo[2], dv[0]), (dv[1], fo[3])):
    h = h.cut(bb(fo[0], fo[1], *oy, z0 - 0.2, pt + 0.1))
for x, y in C.HOOD_SCREWS:
    h = h.cut(cz(x, y, z0 - 0.3, 2.2, C.HOOD_PLATE_T + 0.6))
(ob, ot, oh), (ib, it, ih) = C.HOOD_OUT, C.HOOD_IN
out = (cq.Workplane('XY', origin=(0, 0, pt)).center(cxh, cyh)
       .rect(*ob).workplane(offset=oh).rect(*ot).loft())
inn = (cq.Workplane('XY', origin=(0, 0, pt - 0.2)).center(cxh, cyh)
       .rect(*ib).workplane(offset=ih).rect(*it).loft())
rx, ry, rl, rw, rt = C.HOOD_ROOF
h = h.union(out).cut(inn).union(box(rx, ry, pt + oh, rl, rw, rt))
div = bb(hx0, hx1, dv[0], dv[1], pt - 0.3, pt - 0.2 + ih + 0.1).intersect(inn)
h = h.union(div)
inner_top = pt - 0.2 + ih
for name, (x, y) in C.HOOD_PORTS.items():
    h = h.cut(cz(x, y, inner_top - 1.0, C.HOOD_PORT_D, 40.0))
    zz = pt + oh + rt
    for d, hh in C.HOOD_NOZZLE:
        h = h.union(cz(x, y, zz, d, hh))
        zz += hh
    h = h.cut(cz(x, y, inner_top - 1.0, C.HOOD_PORT_D, 40.0))
    # Deboss IN / OUT into roof close to each port.
    try:
        txt = (cq.Workplane('XY', origin=(0, 0, pt + oh + rt + 0.05))
               .center(x + (8.0 if name == 'IN' else -8.0), y)
               .text(name, 3.5, -0.35, font=C.MARK_FONT,
                     halign='center', valign='center'))
        h = h.cut(txt)
    except Exception as exc:
        print('WARN hood marking skipped:', name, exc)

parts = {
    'P01_Compact_Base_Global': b,
    'P02_Compact_Lid_Global': l,
    'P03_Compact_SensorPod_Global': p,
    'P04_Hood_Gasket_D_Profile_TPU95A': g4,
    'P05_Cable_Stop_Global': stop,
    'P07_Calibration_Hood': h,
    'P08_Pod_Lid_Gasket_D_Profile_TPU95A': g8,
}
print_names = {
    'P01_Compact_Base_Global': 'P01_Compact_Base_Print',
    'P02_Compact_Lid_Global': 'P02_Compact_Lid_Print',
    'P03_Compact_SensorPod_Global': 'P03_Compact_SensorPod_Print',
    'P04_Hood_Gasket_D_Profile_TPU95A': 'P04_Hood_Gasket_D_Profile_TPU95A_Print',
    'P05_Cable_Stop_Global': 'P05_Cable_Stop_Print',
    'P07_Calibration_Hood': 'P07_Calibration_Hood_Print',
    'P08_Pod_Lid_Gasket_D_Profile_TPU95A': 'P08_Pod_Lid_Gasket_D_Profile_TPU95A_Print',
}
flip = {'P02_Compact_Lid_Global'}

for name, shape in parts.items():
    step(shape, G / f'{name}.step')
for name, shape in parts.items():
    q = shape.rotate((0, 0, 0), (1, 0, 0), 180) if name in flip else shape
    q = origin(q)
    step(q, P / f'{print_names[name]}.step')
    stl(q, P / f'{print_names[name]}.stl')

# Assemblies.
shapes = [shape.val() for shape in parts.values()]
assembly = cq.Workplane(obj=cq.Compound.makeCompound(shapes))
step(assembly, G / f'AirMonitor_Compact_Assembly_{REV}.step')

cr = C.CARRIER
dummies = [
    bb(*cr),
    bb(*C.PCB_WAVESHARE),
    bb(*C.SEN_PCB), bb(*C.SEN_TOP), bb(*C.SEN_CON),
    bb(*C.BTN_PCB_DUMMY),
    # DC5521 / nut reference on left wall (assumed Ø16 x 3 inside + Ø11.2 body).
    cx(C.WALL, C.DC5521[0], C.DC5521[1], 16.0, 3.0),
]
ref = cq.Workplane(obj=cq.Compound.makeCompound(shapes + [d.val() for d in dummies]))
step(ref, G / f'AirMonitor_Compact_Reference_With_Dummies_{REV}.step')

# CAD-kernel intersection report. Gasket compression contacts are intentional.
allowed = {
    ('P02_Compact_Lid_Global', 'P04_Hood_Gasket_D_Profile_TPU95A'),
    ('P02_Compact_Lid_Global', 'P08_Pod_Lid_Gasket_D_Profile_TPU95A'),
    ('P04_Hood_Gasket_D_Profile_TPU95A', 'P07_Calibration_Hood'),
    ('P03_Compact_SensorPod_Global', 'P08_Pod_Lid_Gasket_D_Profile_TPU95A'),
    ('P03_Compact_SensorPod_Global', 'P05_Cable_Stop_Global'),
}
problems = []
names = list(parts)
for i, a in enumerate(names):
    for bn in names[i + 1:]:
        if (a, bn) in allowed:
            continue
        r = parts[a].intersect(parts[bn])
        v = r.val().Volume() if r.vals() else 0.0
        if v > 0.01:
            problems.append(f'{a} ∩ {bn}: {v:.2f} mm³')
print('Unexpected part intersections:', *(problems or ['none']), sep='\n  ')
if problems:
    raise SystemExit('Unexpected CAD intersections found.')

# Dimension table.
with (R / 'DIMENSIONS.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['part', 'x_len', 'y_len', 'z_len', 'x_min', 'x_max',
                'y_min', 'y_max', 'z_min', 'z_max', 'volume_mm3'])
    for name, shape in parts.items():
        q = shape.val()
        bx = q.BoundingBox()
        vals = (bx.xlen, bx.ylen, bx.zlen, bx.xmin, bx.xmax,
                bx.ymin, bx.ymax, bx.zmin, bx.zmax, q.Volume())
        w.writerow([name, *[f'{v:.3f}' for v in vals]])

# Machine-readable change table.
with (R / 'V07_COORDINATES.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['feature', 'value', 'note'])
    w.writerow(['LID_BOSSES', C.LID_BOSSES, 'right bosses now 7 mm from edge'])
    w.writerow(['STANDOFFS', C.STANDOFFS, 'annotated board mount coordinates'])
    w.writerow(['POD', C.POD, 'moved +20 X and widened +8 to right'])
    w.writerow(['DC5521', f'left wall; Y={C.DC5521[0]}; Z={C.DC5521[1]}; D={C.DC5521[2]}', 'opposite end wall'])
    w.writerow(['P04', C.P04, 'D-profile TPU95A, top groove'])
    w.writerow(['P08', C.P08, 'D-profile TPU95A, underside groove'])

# Review SVGs.
inside_right = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="680" viewBox="-5 -6 122 67">
<style>text{{font-family:Arial,sans-serif;font-size:3.1px;fill:#172b3a}}.t{{font-size:4px;font-weight:bold}}.wall{{fill:#f4f5f6;stroke:#172b3a;stroke-width:.6}}.pcb{{fill:#d7e6ef;stroke:#172b3a;stroke-width:.5}}.col{{fill:#c6c9cc;stroke:#59636a;stroke-width:.4}}.h{{fill:#9cc7dc;stroke:#24566f;stroke-width:.4}}.o{{fill:white;stroke:#172b3a;stroke-width:.45}}</style>
<text class="t" x="0" y="-2">AirMonitor V0.7 – rechte Stirnwand innen: ZERO / SPAN</text>
<rect class="wall" x="0" y="0" width="112" height="55"/>
<rect class="col" x="2.5" y="0" width="9" height="55" rx="4.5"/><rect class="col" x="100.5" y="0" width="9" height="55" rx="4.5"/>
<rect class="pcb" x="16" y="2" width="80" height="20"/>
<circle class="h" cx="18" cy="4" r="2.5"/><circle class="h" cx="94" cy="4" r="2.5"/><circle class="h" cx="18" cy="20" r="2.5"/><circle class="h" cx="94" cy="20" r="2.5"/>
<circle class="o" cx="76" cy="14" r="1.5"/><circle class="o" cx="60" cy="14" r="1.5"/>
<text x="70" y="11">ZERO</text><text x="56" y="11">SPAN</text>
<text x="15" y="27">80,0 × 20,0 × 1,5; Halter 76,0 × 16,0</text>
<text x="2" y="61">DC5521 ist nicht mehr auf dieser Wand.</text></svg>'''
(D / 'Drawing_Right_EndWall_Inside_V0.7.svg').write_text(inside_right, encoding='utf-8')

outside_left = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="650" viewBox="-5 -6 122 66">
<style>text{{font-family:Arial,sans-serif;font-size:3.2px;fill:#172b3a}}.t{{font-size:4px;font-weight:bold}}.wall{{fill:#f4f5f6;stroke:#172b3a;stroke-width:.6}}.dc{{fill:#fff3c4;stroke:#172b3a;stroke-width:.55}}</style>
<text class="t" x="0" y="-2">AirMonitor V0.7 – linke Stirnwand aussen: 24 V DC</text>
<rect class="wall" x="0" y="0" width="112" height="55"/>
<circle class="dc" cx="44" cy="27.5" r="5.6"/>
<text x="36" y="18">24 V DC</text><text x="36" y="37">DC5521 Ø11,2</text>
<text x="2" y="60">Lochmitte Y=44,0 / Z=27,5; Markierung V0.7 angepasst.</text></svg>'''
(D / 'Drawing_Left_EndWall_Outside_V0.7.svg').write_text(outside_left, encoding='utf-8')

seal_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="550" viewBox="0 0 110 55">
<style>text{{font-family:Arial,sans-serif;font-size:3px;fill:#172b3a}}.t{{font-size:4px;font-weight:bold}}.rigid{{fill:#d9dde1;stroke:#172b3a;stroke-width:.45}}.seal{{fill:#88c6d9;stroke:#172b3a;stroke-width:.45}}.dim{{stroke:#172b3a;stroke-width:.25}}</style>
<text class="t" x="2" y="5">V0.7 TPU95A D-Profil und Einbuchtung</text>
<rect class="rigid" x="8" y="31" width="70" height="8"/><rect x="28" y="31" width="14" height="2.4" fill="white" stroke="#172b3a" stroke-width=".3"/>
<path class="seal" d="M30 33.4 L40 33.4 L40 29.8 Q40 27.4 37.6 27.4 L32.4 27.4 Q30 27.4 30 29.8 Z"/>
<text x="47" y="29">Gasket height 2,0</text><text x="47" y="33">Groove depth 0,6</text><text x="47" y="37">Base width 3,0</text>
<text x="8" y="47">P08 compression 20 %; P04 compression 25 %; flat underside, rounded top.</text></svg>'''
(D / 'Drawing_TPU_D_Profile_Groove_V0.7.svg').write_text(seal_svg, encoding='utf-8')

print('Generated', R)
