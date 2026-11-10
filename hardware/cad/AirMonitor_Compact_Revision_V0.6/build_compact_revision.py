"""AirMonitor Compact V0.3 – parametrische Quelle (CadQuery 2.5.2).

Alle Masse stehen in compact_params.py. Vor dem Build läuft check_clearances.py
(ohne CAD-Kern); bei einer Kollision bricht der Build ab.
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
    sys.exit('Abbruch: Kollisionsprüfung fehlgeschlagen (siehe oben).')

G = R / '01_CAD_Global'; P = R / '02_CAD_Print'; D = R / '03_Renders_Drawings'
for x in (G, P, D):
    x.mkdir(parents=True, exist_ok=True)
REV = 'V0.3'


def box(x, y, z, l, w, h):
    return cq.Workplane('XY').box(l, w, h, centered=(False, False, False)).translate((x, y, z))


def bb(x0, x1, y0, y1, z0, z1):
    return box(x0, y0, z0, x1 - x0, y1 - y0, z1 - z0)


def cz(x, y, z, d, h):
    return cq.Workplane('XY', origin=(x, y, z)).circle(d / 2).extrude(h)


def cx(x, y, z, d, h):
    return cq.Workplane('YZ', origin=(x, 0, 0)).center(y, z).circle(d / 2).extrude(h)


def step(s, p):
    exporters.export(s, str(p), exportType='STEP')


def stl(s, p):
    exporters.export(s, str(p), exportType='STL', tolerance=.08, angularTolerance=.15)


def origin(s):
    b = s.val().BoundingBox()
    return s.translate((-b.xmin, -b.ymin, -b.zmin))


L, W, H, wall, floor = C.L, C.W, C.H, C.WALL, C.FLOOR

# ---------------- P01 Unterteil ----------------
b = box(0, 0, 0, L, W, floor)
for q in (box(0, 0, 0, wall, W, H), box(L - wall, 0, 0, wall, W, H),
          box(0, 0, 0, L, wall, H), box(0, W - wall, 0, L, wall, H)):
    b = b.union(q)
b = b.union(box(0, -C.FLANGE, 0, L, C.FLANGE, floor)).union(box(0, W, 0, L, C.FLANGE, floor))
for x, y in C.WALL_MOUNT_HOLES:
    b = b.cut(cz(x, y, -.2, C.WALL_MOUNT_D, floor + .5))
for y in (-.5, W - wall - .5):
    b = b.cut(box(C.OPEN_X0, y, C.OPEN_Z, C.OPEN_X1 - C.OPEN_X0, wall + 1, H - C.OPEN_Z + 1))
for x, y in C.LID_BOSSES:  # V0.3: neue Lage, bündig bis Z 55,0
    b = b.union(cz(x, y, floor, C.LID_BOSS_D, H - floor)).cut(cz(x, y, floor - .2, C.LID_BOSS_PILOT_D, H - floor + .5))
for x, y in C.STANDOFFS:
    b = b.union(cz(x, y, floor, C.STANDOFF_D, C.BOARD_BOTTOM_Z - floor)).cut(
        cz(x, y, floor - .2, C.STANDOFF_PILOT_D, C.BOARD_BOTTOM_Z - floor + .5))
dy, dz, dd = C.DC5521
b = b.cut(cx(L - wall - .2, dy, dz, dd, wall + .5))
for y, z, d in (C.ZERO, C.SPAN):
    b = b.cut(cx(L - wall - .2, y, z, d, wall + .5))
hx = L - wall - C.BTN_HOLDER_LEN
for y in C.BTN_HOLDER_Y:
    for z in C.BTN_HOLDER_Z:
        b = b.union(cx(hx, y, z, C.BTN_HOLDER_D, C.BTN_HOLDER_LEN)).cut(
            cx(hx - .2, y, z, C.BTN_HOLDER_PILOT_D, C.BTN_HOLDER_LEN + .5))

# ---------------- P02 Deckel ----------------
lz, lt = C.LID_Z, C.LID_T
l = box(0, 0, lz, L, W, lt)
for x, y, lx, ly in C.VENTS:
    l = l.cut(box(x, y, lz - .5, lx, ly, lt + 1))
for x, y in C.LID_BOSSES:
    l = l.cut(cz(x, y, lz - .5, C.LID_HOLE_D, lt + 1)).cut(cz(x, y, lz + lt - C.LID_CBORE_DEPTH, C.LID_CBORE_D, C.LID_CBORE_DEPTH + .3))
for x, y in C.HOOD_SCREWS:  # V0.3: Haube schraubt in Deckel
    l = l.union(cz(x, y, C.HOOD_SCREW_BOSS_Z0, C.HOOD_SCREW_BOSS_D, lz - C.HOOD_SCREW_BOSS_Z0))
    l = l.cut(cz(x, y, C.HOOD_SCREW_BOSS_Z0 + .5, C.HOOD_SCREW_PILOT_D, lz + lt - C.HOOD_SCREW_BOSS_Z0))
for x, y in C.POD_MOUNTS:  # V0.3: Bossen Z 52,0…55,0 ausserhalb Pod-Wand und P08
    l = l.union(cz(x, y, C.POD_BOSS_Z0, C.POD_BOSS_D, lz - C.POD_BOSS_Z0))
    l = l.cut(cz(x, y, C.POD_BOSS_Z0 - .1, C.POD_BOSS_PILOT_D, C.POD_BOSS_PILOT_TOP - C.POD_BOSS_Z0 + .1))

# ---------------- P03 Sensorpod ----------------
px0, px1, py0, py1, pz0, pz1 = C.POD
t = C.POD_WALL
p = bb(px0, px1, py0, py1, pz0, pz1).cut(bb(px0 + t, px1 - t, py0 + t, py1 - t, pz0 + t, pz1 + 1))
for ty in (C.TONGUE_FRONT_Y, C.TONGUE_BACK_Y):  # V0.3: Zungen Z 50,0…52,0
    p = p.union(bb(*C.TONGUE_X, *ty, *C.TONGUE_Z))
for x, y in C.POD_MOUNTS:
    p = p.cut(cz(x, y, C.TONGUE_Z[0] - .5, C.TONGUE_HOLE_D, C.TONGUE_Z[1] - C.TONGUE_Z[0] + 1))
for x, y in C.SENSOR_BOSSES:
    p = p.union(cz(x, y, pz0 + t, C.SENSOR_BOSS_D, C.SENSOR_BOSS_TOP - pz0 - t)).cut(
        cz(x, y, pz0 + t - .5, C.SENSOR_HOLE_D, C.SENSOR_BOSS_TOP - pz0 - t + 1))
p = p.cut(bb(*C.GRAVITY_SLOT))

# ---------------- P08 / P04 / P05 ----------------
g = C.P08
g8 = bb(*g['x'], *g['y'], g['z0'], g['z0'] + g['t']).cut(
    bb(g['x'][0] + g['web'], g['x'][1] - g['web'], g['y'][0] + g['web'], g['y'][1] - g['web'], g['z0'] - .2, g['z0'] + g['t'] + .2))
g = C.P04
g4 = bb(*g['x'], *g['y'], g['z0'], g['z0'] + g['t'])
wx = (g['x'][0] + g['web'], g['x'][1] - g['web'])
for wy in ((g['y'][0] + g['web'], g['bar_y'][0]), (g['bar_y'][1], g['y'][1] - g['web'])):  # V0.3: zwei Fenster
    g4 = g4.cut(bb(*wx, *wy, g['z0'] - .2, g['z0'] + g['t'] + .2))
stop = bb(*C.P05)  # V0.3: volle Höhe

# ---------------- P07 Kalibrierhaube ----------------
z0 = C.HOOD_Z0
pt = z0 + C.HOOD_PLATE_T
hx0, hx1, hy0, hy1 = C.HOOD_PLATE
cxh, cyh = C.HOOD_CENTER
h = bb(hx0, hx1, hy0, hy1, z0, pt)
fo = C.HOOD_FLOOR_OPEN
dv = C.HOOD_DIVIDER_Y
for oy in ((fo[2], dv[0]), (dv[1], fo[3])):  # V0.3: Boden offen, Steg bleibt als Trennsteg-Fuss
    h = h.cut(bb(fo[0], fo[1], *oy, z0 - .2, pt + .1))
for x, y in C.HOOD_SCREWS:
    h = h.cut(cz(x, y, z0 - .3, 2.2, C.HOOD_PLATE_T + .6))
(ob, ot, oh), (ib, it, ih) = C.HOOD_OUT, C.HOOD_IN
out = cq.Workplane('XY', origin=(0, 0, pt)).center(cxh, cyh).rect(*ob).workplane(offset=oh).rect(*ot).loft()
inn = cq.Workplane('XY', origin=(0, 0, pt - .2)).center(cxh, cyh).rect(*ib).workplane(offset=ih).rect(*it).loft()
rx, ry, rl, rw, rt = C.HOOD_ROOF
h = h.union(out).cut(inn).union(box(rx, ry, pt + oh, rl, rw, rt))
div = bb(hx0, hx1, dv[0], dv[1], pt - .3, pt - .2 + ih + .1).intersect(inn)  # V0.3: Trennsteg IN | OUT
h = h.union(div)
inner_top = pt - .2 + ih
for x, y in C.HOOD_PORTS.values():
    h = h.cut(cz(x, y, inner_top - 1.0, C.HOOD_PORT_D, 40))  # V0.3: Bohrung bis in die Kammer
    zz = pt + oh + rt
    for d, hh in C.HOOD_NOZZLE:
        h = h.union(cz(x, y, zz, d, hh)); zz += hh
    h = h.cut(cz(x, y, inner_top - 1.0, C.HOOD_PORT_D, 40))

parts = {
    'P01_Compact_Base_Global': b, 'P02_Compact_Lid_Global': l, 'P03_Compact_SensorPod_Global': p,
    'P04_Hood_Gasket_TPU': g4, 'P05_Cable_Stop_Global': stop, 'P07_Calibration_Hood': h,
    'P08_Pod_Lid_Gasket_Global': g8,
}
print_names = {
    'P01_Compact_Base_Global': 'P01_Compact_Base_Print', 'P02_Compact_Lid_Global': 'P02_Compact_Lid_Print',
    'P03_Compact_SensorPod_Global': 'P03_Compact_SensorPod_Print', 'P04_Hood_Gasket_TPU': 'P04_Hood_Gasket_TPU_Print',
    'P05_Cable_Stop_Global': 'P05_Cable_Stop_Print', 'P07_Calibration_Hood': 'P07_Calibration_Hood_Print',
    'P08_Pod_Lid_Gasket_Global': 'P08_Pod_Lid_Gasket_Print',
}
flip = {'P02_Compact_Lid_Global'}  # V0.3: Deckelplatte nach unten drucken
for n, s in parts.items():
    step(s, G / (n + '.step'))
for n, s in parts.items():
    q = s.rotate((0, 0, 0), (1, 0, 0), 180) if n in flip else s
    q = origin(q)
    step(q, P / (print_names[n] + '.step')); stl(q, P / (print_names[n] + '.stl'))

sh = [s.val() for s in parts.values()]
step(cq.Workplane(obj=cq.Compound.makeCompound(sh)), G / f'AirMonitor_Compact_Assembly_{REV}.step')
cr = C.CARRIER
dummies = [bb(*cr), box(21.6, 11, 9.6, 151.8, 90, 1.6), bb(*C.SEN_PCB), bb(*C.SEN_TOP), bb(*C.SEN_CON), bb(*C.BTN_PCB_DUMMY)]
step(cq.Workplane(obj=cq.Compound.makeCompound(sh + [d.val() for d in dummies])),
     G / f'AirMonitor_Compact_Reference_With_Dummies_{REV}.step')

# Restvolumen-Prüfung mit CAD-Kern: Teile untereinander und gegen Dummys
pairs = [(a, bn) for i, a in enumerate(parts) for bn in list(parts)[i + 1:]]
allowed = {('P02_Compact_Lid_Global', 'P08_Pod_Lid_Gasket_Global'),   # Verpressung 0,3
           ('P02_Compact_Lid_Global', 'P04_Hood_Gasket_TPU'),          # Kontakt
           ('P04_Hood_Gasket_TPU', 'P07_Calibration_Hood'),            # Verpressung 0,3
           ('P03_Compact_SensorPod_Global', 'P05_Cable_Stop_Global')}  # Stopfen im Durchlass (Kontakt)
problems = []
for a, bn in pairs:
    if (a, bn) in allowed:
        continue
    v = parts[a].intersect(parts[bn]).val().Volume() if parts[a].intersect(parts[bn]).vals() else 0.0
    if v > 0.01:
        problems.append(f'{a} ∩ {bn}: {v:.2f} mm³')
for n, s in parts.items():
    for i, d in enumerate(dummies):
        r = s.intersect(d)
        v = r.val().Volume() if r.vals() else 0.0
        if v > 0.01:
            problems.append(f'{n} ∩ Dummy{i}: {v:.2f} mm³')
print('Überschneidungen:', *(problems or ['keine']), sep='\n  ')

with (R / 'DIMENSIONS.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['part', 'x_len', 'y_len', 'z_len', 'x_min', 'x_max', 'y_min', 'y_max', 'z_min', 'z_max', 'volume_mm3'])
    for n, s in parts.items():
        q = s.val(); bx = q.BoundingBox()
        w.writerow([n, *[f'{v:.3f}' for v in (bx.xlen, bx.ylen, bx.zlen, bx.xmin, bx.xmax, bx.ymin, bx.ymax, bx.zmin, bx.zmax, q.Volume())]])

top_svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="-10 -20 228 152"><style>text{font-family:Arial;font-size:5px}'
           '.a{fill:none;stroke:#12385b;stroke-width:.8}.b{fill:#cfe1ef;stroke:#12385b}.c{fill:#f0c774;stroke:#12385b}</style>'
           '<rect class="a" x="0" y="0" width="208" height="112"/><rect class="b" x="10" y="11" width="175" height="90"/>'
           '<rect class="c" x="6" y="16" width="45.5" height="82"/><text x="3" y="-5">Laminar AirMonitor HCHO – Top view V0.3 [mm]</text>'
           '<text x="70" y="58">Waveshare</text><text x="8" y="44">SEN0661 pod</text></svg>')
side_svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="-10 -8 228 115"><style>text{font-family:Arial;font-size:5px}'
            '.a{fill:none;stroke:#12385b;stroke-width:.8}.b{fill:#cfe1ef;stroke:#12385b}.c{fill:#f0c774;stroke:#12385b}.d{fill:none;stroke:#a43;stroke-dasharray:3 2}</style>'
            '<rect class="a" x="0" y="0" width="208" height="55"/><rect class="b" x="10" y="9.6" width="175" height="18"/>'
            f'<rect class="c" x="6" y="40" width="45.5" height="14"/><rect class="d" x="4" y="{z0}" width="48" height="41"/>'
            '<text x="3" y="-3">Laminar AirMonitor HCHO – Side view V0.3 [mm]</text><text x="60" y="22">Waveshare</text><text x="8" y="48">sensor pod</text></svg>')
(D / 'Drawing_Compact_Top_View.svg').write_text(top_svg, encoding='utf-8')
(D / 'Drawing_Compact_Side_View.svg').write_text(side_svg, encoding='utf-8')
print('Generated', R)
if problems:
    sys.exit('Überschneidungen gefunden – Dateien erzeugt, aber nicht freigabefähig.')
