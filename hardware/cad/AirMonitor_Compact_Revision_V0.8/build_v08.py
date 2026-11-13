"""Build Laminar AirMonitor HCHO Compact V0.8 corrected O-ring revision.

Generates global STEP, print-oriented STEP/STL, SVG review drawings and CSV data.
The sensor/calibration group retains the proven V0.6 X position, is centred in Y,
uses purchased EPDM 70 Shore A O-rings, lowers ZERO/SPAN by 15 mm,
and adds an edge-guided, visually flush short-travel sliding lid.
"""
from __future__ import annotations

from pathlib import Path
import csv
import math
import shutil
import sys

import cadquery as cq
from cadquery import exporters

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import compact_params as C  # noqa: E402
import check_clearances  # noqa: E402

if check_clearances.run() != 0:
    raise SystemExit('Abbruch: V0.8 Mass-/Freiraumprüfung fehlgeschlagen.')

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
REV = 'V0.8'


def box(x: float, y: float, z: float, l: float, w: float, h: float):
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
    inner_r = max(0.1, corner_r - web)
    inner = rounded_prism(x0 + web, x1 - web, y0 + web, y1 - web,
                          inner_r, z0 - 0.1, h + 0.2)
    return outer.cut(inner)


def channel_from_centerline(cfg: dict, width: float, z0: float, depth: float):
    """Rounded rectangular channel with dimensions referenced to its centreline."""
    cx0, cy0 = cfg['cx'], cfg['cy']
    cw, ch, r = cfg['cw'], cfg['ch'], cfg['r']
    outer = rounded_prism(cx0 - (cw + width) / 2,
                          cx0 + (cw + width) / 2,
                          cy0 - (ch + width) / 2,
                          cy0 + (ch + width) / 2,
                          r + width / 2, z0, depth)
    inner = rounded_prism(cx0 - (cw - width) / 2,
                          cx0 + (cw - width) / 2,
                          cy0 - (ch - width) / 2,
                          cy0 + (ch - width) / 2,
                          max(0.1, r - width / 2), z0 - 0.1, depth + 0.2)
    return outer.cut(inner)


def installed_ring(cfg: dict, z0: float, height: float):
    """Compressed installed O-ring reference, approximated as a rounded band."""
    ring = channel_from_centerline(cfg, cfg['cord'], z0, height)
    try:
        ring = ring.edges('>Z').fillet(min(cfg['cord'] * 0.35, height * 0.35))
    except Exception as exc:
        print('WARN O-ring reference fillet skipped:', cfg['name'], exc)
    return ring


def capsule_x(x0, x1, y, width, z0, h):
    """Capsule prism running in X, used for blind keyhole tracks."""
    if x1 < x0:
        x0, x1 = x1, x0
    r = width / 2
    s = box(x0, y - r, z0, x1 - x0, width, h)
    s = s.union(cz(x0, y, z0, width, h))
    s = s.union(cz(x1, y, z0, width, h))
    return s


def outside_text_right(text, y, z, size=None):
    plane = cq.Plane(origin=(C.L, 0, 0), xDir=(0, 1, 0), normal=(1, 0, 0))
    return cq.Workplane(plane).center(y, z).text(
        text, size or C.MARK_FONT_SIZE, -C.MARK_DEPTH,
        font=C.MARK_FONT, halign='center', valign='center')


def outside_text_left(text, y, z, size=None):
    plane = cq.Plane(origin=(0, C.W, 0), xDir=(0, -1, 0), normal=(-1, 0, 0))
    return cq.Workplane(plane).center(C.W - y, z).text(
        text, size or C.MARK_FONT_SIZE, -C.MARK_DEPTH,
        font=C.MARK_FONT, halign='center', valign='center')


def top_text(text, x, y, z, size=3.2):
    return cq.Workplane('XY', origin=(0, 0, z)).center(x, y).text(
        text, size, -C.MARK_DEPTH, font=C.MARK_FONT,
        halign='center', valign='center')


L, W, H, wall, floor = C.L, C.W, C.H, C.WALL, C.FLOOR

# ---------------- P01 rounded enclosure base ----------------
L, W, H, wall, floor = C.L, C.W, C.H, C.WALL, C.FLOOR

lower_outer = rounded_prism(0, L, 0, W, C.BODY_CORNER_R,
                            0, C.SHOULDER_Z0)
lower_inner = rounded_prism(wall, L-wall, wall, W-wall,
                            max(0.8, C.BODY_CORNER_R-wall),
                            floor, C.SHOULDER_Z0-floor+0.2)
b = lower_outer.cut(lower_inner)

sx0, sx1 = C.SHOULDER_INSET, L-C.SHOULDER_INSET
sy0, sy1 = C.SHOULDER_INSET, W-C.SHOULDER_INSET
upper_outer = rounded_prism(sx0, sx1, sy0, sy1,
                            C.SHOULDER_CORNER_R,
                            C.SHOULDER_Z0, C.SHOULDER_H)
upper_inner = rounded_prism(sx0+wall, sx1-wall,
                            sy0+wall, sy1-wall,
                            max(0.8, C.SHOULDER_CORNER_R-wall),
                            C.SHOULDER_Z0-0.1, C.SHOULDER_H+0.2)
b = b.union(upper_outer.cut(upper_inner))

# Keep the insertion-side end wall full height. The lid has no left end
# skirt, so it can be lowered in the +8 mm service position without
# colliding with the shoulder. Intersecting with the rounded body
# preserves the external R6 corner contour.
left_end_wall = rounded_prism(0, L, 0, W, C.BODY_CORNER_R,
                              C.SHOULDER_Z0, C.SHOULDER_H)
left_end_wall = left_end_wall.intersect(
    box(0, 0, C.SHOULDER_Z0, wall, W, C.SHOULDER_H))
b = b.union(left_end_wall)

b = b.union(rounded_prism(0, L, -C.FLANGE, 0, 2.0, 0, floor))
b = b.union(rounded_prism(0, L, W, W+C.FLANGE, 2.0, 0, floor))
for x, y in C.WALL_MOUNT_HOLES:
    b = b.cut(cz(x, y, -0.2, C.WALL_MOUNT_D, floor+0.5))

for y in (-0.5, W-wall-0.5):
    b = b.cut(box(C.OPEN_X0, y, C.OPEN_Z,
                  C.OPEN_X1-C.OPEN_X0, wall+1.0,
                  C.OPEN_TOP_Z-C.OPEN_Z+0.2))

for x, y in C.STANDOFFS:
    b = b.union(cz(x, y, floor, C.STANDOFF_D,
                   C.BOARD_BOTTOM_Z-floor))
    b = b.cut(cz(x, y, floor-0.2, C.STANDOFF_PILOT_D,
                 C.BOARD_BOTTOM_Z-floor+0.5))

def guide_lug(xc, rear=False, snap=False):
    """Diagonal support-free tongue integrated into the recessed shoulder.

    Both lower and upper faces rise outward at 45 degrees. Opposing front/rear
    tongues form a captured slide after the lid has moved out of the entry
    pockets. No guide exists in the enclosure centre.
    """
    x0 = xc - C.GUIDE_LUG_W / 2
    proj = C.GUIDE_PROJ + (C.SNAP_EXTRA_PROJ if snap else 0.0)
    rise = proj
    root_y = sy1 if rear else sy0
    tip_y = root_y + proj if rear else root_y - proj
    points = [
        (root_y, C.GUIDE_ROOT_Z0),
        (tip_y, C.GUIDE_ROOT_Z0 + rise),
        (tip_y, C.GUIDE_ROOT_Z1 + rise),
        (root_y, C.GUIDE_ROOT_Z1),
    ]
    return (cq.Workplane('YZ', origin=(x0, 0, 0))
            .polyline(points).close().extrude(C.GUIDE_LUG_W))

for x in C.GUIDE_X_FRONT:
    b = b.union(guide_lug(x, rear=False, snap=abs(x-C.SNAP_X) < 1e-6))
for x in C.GUIDE_X_REAR:
    b = b.union(guide_lug(x, rear=True, snap=False))

dy, dz, dd = C.DC5521
b = b.cut(cx(-0.2,dy,dz,dd,wall+0.5))
for y, z, d in (C.ZERO,C.SPAN):
    b = b.cut(cx(L-wall-0.2,y,z,d,wall+0.5))
hx = L-wall-C.BTN_HOLDER_LEN
for y in C.BTN_HOLDER_Y:
    for z in C.BTN_HOLDER_Z:
        b = b.union(cx(hx,y,z,C.BTN_HOLDER_D,C.BTN_HOLDER_LEN))
        b = b.cut(cx(hx-0.2,y,z,C.BTN_HOLDER_PILOT_D,C.BTN_HOLDER_LEN+0.5))

for text_label,y,z in (('ZERO',C.ZERO[0],C.BTN_MARK_Z),
                       ('SPAN',C.SPAN[0],C.BTN_MARK_Z)):
    try:
        b = b.cut(outside_text_right(text_label,y,z))
    except Exception as exc:
        print('WARN right-wall marking skipped:',text_label,exc)
try:
    b = b.cut(outside_text_left('24 V DC',C.DC5521[0],38.0,4.0))
    b = b.cut(outside_text_left('V0.8',91.0,8.0,3.0))
except Exception as exc:
    print('WARN left-wall marking skipped:',exc)

# ---------------- P02 rounded 10-mm overlap cap lid ----------------
lz, lt = C.LID_Z, C.LID_T
l = rounded_prism(C.LID_X0,C.LID_X1,C.LID_Y0,C.LID_Y1,
                  C.LID_CORNER_R,lz,lt)
skirt_outer = rounded_prism(C.LID_X0,C.LID_X1,C.LID_Y0,C.LID_Y1,
                            C.LID_CORNER_R,lz-C.LID_OVERLAP,C.LID_OVERLAP)
skirt_inner = rounded_prism(C.LID_IN_X0,C.LID_IN_X1,C.LID_IN_Y0,C.LID_IN_Y1,
                            max(0.8,C.LID_CORNER_R-C.LID_SKIRT_W),
                            lz-C.LID_OVERLAP-0.1,C.LID_OVERLAP+0.2)
skirt = skirt_outer.cut(skirt_inner)
# Open the insertion-side end of the 10 mm skirt. Front/rear skirts
# remain continuous and the opposite end closes flush in service.
if C.LID_LEFT_END_OPEN:
    skirt = skirt.cut(box(C.LID_X0 - 0.2, C.LID_Y0 - 0.2,
                           lz - C.LID_OVERLAP - 0.2,
                           C.WALL + 0.8,
                           C.LID_Y1 - C.LID_Y0 + 0.4,
                           C.LID_OVERLAP + 0.4))
l = l.union(skirt)

for x,y,lx,ly in C.VENTS:
    l = l.cut(box(x,y,lz-0.5,lx,ly,lt+1.0))
for x,y in C.HOOD_SCREWS:
    l = l.union(cz(x,y,C.HOOD_SCREW_BOSS_Z0,C.HOOD_SCREW_BOSS_D,lz-C.HOOD_SCREW_BOSS_Z0))
    l = l.cut(cz(x,y,C.HOOD_SCREW_BOSS_Z0+0.5,C.HOOD_SCREW_PILOT_D,lz+lt-C.HOOD_SCREW_BOSS_Z0))
for x,y in C.POD_MOUNTS:
    l = l.union(cz(x,y,C.POD_BOSS_Z0,C.POD_BOSS_D,lz-C.POD_BOSS_Z0))
    l = l.cut(cz(x,y,C.POD_BOSS_Z0-0.1,C.POD_BOSS_PILOT_D,C.POD_BOSS_PILOT_TOP-C.POD_BOSS_Z0+0.1))

# Blind internal 45-degree keyhole tracks. The outside face stays closed.
# In the selected print orientation the diagonal Y/Z faces are self-supporting;
# there is no horizontal slot roof and no slicer support is required.
def guide_track_prism(x0, x1, rear=False, detent=False):
    inner = (C.W - C.GUIDE_GROOVE_INNER_Y_FRONT
             if rear else C.GUIDE_GROOVE_INNER_Y_FRONT)
    outer_normal = (C.W - C.GUIDE_GROOVE_OUTER_Y_FRONT
                    if rear else C.GUIDE_GROOVE_OUTER_Y_FRONT)
    if detent:
        outer = (outer_normal + C.SNAP_DETENT_EXTRA_DEPTH
                 if rear else outer_normal - C.SNAP_DETENT_EXTRA_DEPTH)
    else:
        outer = outer_normal
    rise = abs(outer - inner)
    points = [
        (inner, C.GUIDE_GROOVE_Z0),
        (outer, C.GUIDE_GROOVE_Z0 + rise),
        (outer, C.GUIDE_GROOVE_Z1 + rise),
        (inner, C.GUIDE_GROOVE_Z1),
    ]
    return (cq.Workplane('YZ', origin=(x0, 0, 0))
            .polyline(points).close().extrude(x1 - x0))


def entry_pocket(xc, rear=False, snap=False):
    entry = xc - C.SLIDE_TRAVEL
    x0 = entry - C.GUIDE_ENTRY_W / 2
    if rear:
        y0 = C.W - C.GUIDE_GROOVE_INNER_Y_FRONT - 0.15
        y1 = C.W - C.GUIDE_ENTRY_OUTER_SKIN
    else:
        y0 = C.GUIDE_ENTRY_OUTER_SKIN
        y1 = C.GUIDE_GROOVE_INNER_Y_FRONT + 0.15
    return box(x0, min(y0, y1), C.GUIDE_ENTRY_BOTTOM_Z,
               C.GUIDE_ENTRY_W, abs(y1-y0),
               C.GUIDE_ENTRY_TOP_Z-C.GUIDE_ENTRY_BOTTOM_Z)


def cut_guide(shape, xc, rear=False, snap=False):
    entry = xc - C.SLIDE_TRAVEL
    track_end = xc + C.GUIDE_TRACK_END_EXTRA
    shape = shape.cut(entry_pocket(xc, rear, snap))
    shape = shape.cut(guide_track_prism(entry, track_end, rear, False))
    if snap:
        dx0 = xc - C.SNAP_DETENT_W / 2
        dx1 = xc + C.SNAP_DETENT_W / 2
        shape = shape.cut(guide_track_prism(dx0, dx1, rear, True))
    return shape

for x in C.GUIDE_X_FRONT:
    l = cut_guide(l, x, rear=False, snap=abs(x-C.SNAP_X) < 1e-6)
for x in C.GUIDE_X_REAR:
    l = cut_guide(l, x, rear=True, snap=False)

# Objective geometry checks: the external skirt skin must remain closed and
# the guide recesses must never reach the visible outer faces.
if C.GUIDE_ENTRY_OUTER_SKIN < 1.0 or C.GUIDE_OUTER_SKIN < 1.0:
    raise SystemExit('Abbruch: sichtbare Deckelhaut an der Führung ist zu dünn.')

# ---------------- P03 sensor pod ----------------
px0, px1, py0, py1, pz0, pz1 = C.POD
t = C.POD_WALLpx0, px1, py0, py1, pz0, pz1 = C.POD
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

# Raised sealing rim to contact lid underside at Z=55.0.
pod_rim = bb(px0, px1, py0, py1, pz1, C.POD_SEAL_RIM_TOP)
pod_rim = pod_rim.cut(bb(px0 + t, px1 - t, py0 + t, py1 - t,
                         pz1 - 0.1, C.POD_SEAL_RIM_TOP + 0.1))
p = p.union(pod_rim)
# P08 O-ring groove is in the pod rim, not in the lid.
p08_groove = channel_from_centerline(
    C.P08_RING, C.ORING_GROOVE_W,
    C.POD_SEAL_RIM_TOP - C.ORING_GROOVE_D,
    C.ORING_GROOVE_D + 0.1)
p = p.cut(p08_groove)

# ---------------- P05 cable stop ----------------
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

# P04A/P04B grooves are machined/printed into the hood underside.
for ring in (C.P04A_RING, C.P04B_RING):
    gr = channel_from_centerline(ring, C.ORING_GROOVE_W,
                                 z0 - 0.1, C.ORING_GROOVE_D + 0.1)
    h = h.cut(gr)

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
    h = h.cut(cz(x, y, inner_top - 1.0, C.HOOD_PORT_D, 40))
    zz = pt + oh + rt
    for d, hh in C.HOOD_NOZZLE:
        h = h.union(cz(x, y, zz, d, hh))
        zz += hh
    h = h.cut(cz(x, y, inner_top - 1.0, C.HOOD_PORT_D, 40))
    try:
        label_y = y - 7.0 if name == 'IN' else y + 7.0
        h = h.cut(top_text(name, x, label_y, pt + oh + rt + 0.05, 3.2))
    except Exception as exc:
        print('WARN hood marking skipped:', name, exc)

# ---------------- Purchased O-ring installed references ----------------
ring04a = installed_ring(C.P04A_RING, z0, C.ORING_GROOVE_D)
ring04b = installed_ring(C.P04B_RING, z0, C.ORING_GROOVE_D)
ring08 = installed_ring(C.P08_RING,
                        C.POD_SEAL_RIM_TOP - C.ORING_GROOVE_D,
                        C.ORING_GROOVE_D)

parts = {
    'P01_Compact_Base_Global': b,
    'P02_Compact_Lid_Global': l,
    'P03_Compact_SensorPod_Global': p,
    'P05_Cable_Stop_Global': stop,
    'P07_Calibration_Hood': h,
}
ring_refs = {
    'P04A_O_Ring_EPDM70_45x1p50_Installed_Reference': ring04a,
    'P04B_O_Ring_EPDM70_50x1p50_Installed_Reference': ring04b,
    'P08_O_Ring_EPDM70_77x1p50_Installed_Reference': ring08,
}

print_names = {
    'P01_Compact_Base_Global': 'P01_Compact_Base_Print',
    'P02_Compact_Lid_Global': 'P02_Compact_Lid_Print',
    'P03_Compact_SensorPod_Global': 'P03_Compact_SensorPod_Print',
    'P05_Cable_Stop_Global': 'P05_Cable_Stop_Print',
    'P07_Calibration_Hood': 'P07_Calibration_Hood_Print',
}
flip = {'P02_Compact_Lid_Global'}

for n, s in parts.items():
    step(s, G / (n + '.step'))
for n, s in ring_refs.items():
    step(s, G / (n + '.step'))
for n, s in parts.items():
    q = s.rotate((0, 0, 0), (1, 0, 0), 180) if n in flip else s
    q = origin(q)
    step(q, P / (print_names[n] + '.step'))
    stl(q, P / (print_names[n] + '.stl'))
    if n == 'P02_Compact_Lid_Global':
        step(q, P / 'P02_Compact_Lid_Print_45DEG_GUIDES_V0.8.step')
        stl(q, P / 'P02_Compact_Lid_Print_45DEG_GUIDES_V0.8.stl')

# Global assemblies.
shapes = [s.val() for s in parts.values()]
step(cq.Workplane(obj=cq.Compound.makeCompound(shapes)),
     G / f'AirMonitor_Compact_Assembly_{REV}.step')
cr = C.CARRIER
dummies = [
    bb(*cr),
    bb(*C.PCB_WAVESHARE),
    bb(*C.SEN_PCB),
    bb(*C.SEN_TOP),
    bb(*C.SEN_CON),
    bb(*C.BTN_PCB_DUMMY),
]
reference_shapes = shapes + [d.val() for d in dummies] + [s.val() for s in ring_refs.values()]
step(cq.Workplane(obj=cq.Compound.makeCompound(reference_shapes)),
     G / f'AirMonitor_Compact_Reference_With_Dummies_{REV}.step')

# CAD-kernel intersection check. Exact face contacts are allowed; positive volumes are not.
allowed = {
    ('P02_Compact_Lid_Global', 'P03_Compact_SensorPod_Global'),
    ('P02_Compact_Lid_Global', 'P07_Calibration_Hood'),
    ('P03_Compact_SensorPod_Global', 'P05_Cable_Stop_Global'),
}
problems = []
names = list(parts)
for i, a in enumerate(names):
    for bn in names[i + 1:]:
        if (a, bn) in allowed or (bn, a) in allowed:
            continue
        inter = parts[a].intersect(parts[bn])
        vol = sum(v.Volume() for v in inter.vals()) if inter.vals() else 0.0
        pair = {a, bn}
        if pair == {'P01_Compact_Base_Global', 'P02_Compact_Lid_Global'} and vol <= 1.0:
            print(f'Intentional hidden snap preload: {vol:.3f} mm³')
            continue
        if vol > 0.01:
            problems.append(f'{a} ∩ {bn}: {vol:.2f} mm³')
print('Unexpected part intersections:', *(problems or ['none']), sep='\n  ')
if problems:
    raise SystemExit('Abbruch: unerwartete Bauteilüberschneidung.')

# Write an explicit guide verification note.
with (R / 'LID_45DEG_GUIDE_VERIFICATION.txt').open('w', encoding='utf-8') as f:
    f.write('AirMonitor Compact V0.8 - captured 45-degree side guides\n')
    f.write('Slide travel retained: 8.00 mm\n')
    f.write('Guide locations: front/rear X=18.0 and X=190.0 mm\n')
    f.write('Centre zone: no lid guides, posts or latch parts\n')
    f.write(f'Lid skirt: {C.LID_SKIRT_W:.2f} mm; shoulder clearance: {C.SHOULDER_INSET-C.LID_SKIRT_W:.2f} mm\n')
    f.write(f'Normal outside skin at blind track: {C.GUIDE_OUTER_SKIN:.2f} mm\n')
    f.write(f'Minimum outside skin at entry pocket: {C.GUIDE_ENTRY_OUTER_SKIN:.2f} mm\n')
    f.write('Track cross-section: diagonal parallelogram, 45-degree faces\n')
    f.write('External guide windows: none\n')
    f.write(f'Hidden snap interference: {C.SNAP_INTERFERENCE:.2f} mm\n')
    f.write('Target printing: P01 on floor, P02 visible top on bed, no slicer support\n')

# Dimensions and purchased component data.
with (R / 'DIMENSIONS.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['part', 'x_len', 'y_len', 'z_len', 'x_min', 'x_max',
                'y_min', 'y_max', 'z_min', 'z_max', 'volume_mm3'])
    for n, s in {**parts, **ring_refs}.items():
        q = s.val(); bx = q.BoundingBox()
        w.writerow([n, *[f'{v:.3f}' for v in
                   (bx.xlen, bx.ylen, bx.zlen, bx.xmin, bx.xmax,
                    bx.ymin, bx.ymax, bx.zmin, bx.zmax, q.Volume())]])

with (R / 'PURCHASED_O_RINGS.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['position', 'material', 'inside_diameter_mm', 'cord_mm', 'supplier', 'sku', 'variant_id', 'product_url'])
    purchased = [
        (C.P04A_RING, '47875417440544'),
        (C.P04B_RING, '47875417604384'),
        (C.P08_RING, '47875418128672'),
    ]
    for r, variant in purchased:
        url = 'https://reaflon.ch/products/o-ring-epdm-70-shore-schnurstarke-mm?variant=' + variant
        w.writerow([r['name'], C.ORING_MATERIAL, f"{r['id']:.2f}", f"{r['cord']:.2f}",
                    C.ORING_SUPPLIER, r['sku'], variant, url])

with (R / 'V08_COORDINATES.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['feature', 'value', 'status'])
    w.writerow(['Sensor group X shift', '0.0 mm; V0.6 X position retained', 'approved correction'])
    w.writerow(['Sensor group Y centre', '56.0 mm', 'approved correction'])
    w.writerow(['P03 body', 'X 6.0..59.5 / Y 15.0..97.0 / Z 40.0..54.0', 'CAD'])
    w.writerow(['P03 sealing rim', 'Z 54.0..55.0', 'CAD'])
    w.writerow(['P07 plate', 'X 4.0..60.0 / Y 3.2..108.8 / Z 58.0..61.0', 'CAD'])
    w.writerow(['Lid guides', 'blind 45-degree tracks; X 18/190 at front and rear; 8 mm slide', 'CAD'])
    w.writerow(['Hidden snap', 'front/right X190; 0.20 mm nominal flex; blind detent', 'CAD'])
    for r in (C.P04A_RING, C.P04B_RING, C.P08_RING):
        path = 2 * (r['cw'] + r['ch']) + (2 * math.pi - 8) * r['r']
        free = math.pi * (r['id'] + r['cord'])
        w.writerow([r['name'],
                    f"EPDM70 Ø{r['id']:.2f}x{r['cord']:.2f}; centre ({r['cx']:.2f},{r['cy']:.2f}); "
                    f"path {r['cw']:.2f}x{r['ch']:.2f} R{r['r']:.2f}; stretch {(path/free-1)*100:.2f}%",
                    f"stocked SKU {r['sku']}"])

# Review SVGs.
svg_style = '''<style>text{font-family:Arial,sans-serif;fill:#172b3a}.t{font-size:4px;font-weight:bold}.s{font-size:3px}.wall{fill:#f5f5f5;stroke:#172b3a;stroke-width:.5}.part{fill:#d7e6ef;stroke:#24566f;stroke-width:.45}.groove{fill:none;stroke:#b33;stroke-width:1.2}.axis{stroke:#777;stroke-width:.2;stroke-dasharray:1 1}</style>'''

sensor_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="650" viewBox="-5 -8 218 130">
{svg_style}
<text class="t" x="0" y="-3">AirMonitor V0.8 – korrigierte Sensorgruppe, Draufsicht [mm]</text>
<rect class="wall" x="0" y="0" width="208" height="112"/>
<line class="axis" x1="0" y1="56" x2="208" y2="56"/>
<rect class="part" x="4" y="3.2" width="56" height="105.6"/>
<rect class="part" x="6" y="15" width="53.5" height="82"/>
<text class="s" x="65" y="48">X unverändert: links bei 4,0 / 6,0</text>
<text class="s" x="65" y="55">Y-Mitte der Baugruppe = 56,0</text>
<text class="s" x="65" y="62">Pod rechts +8,0 mm breiter</text>
<text class="s" x="65" y="69">P07 56,0 × 105,6; P03 53,5 × 82,0</text>
</svg>'''
(D / 'Drawing_Sensor_Group_X_Retained_Y_Centred_V0.8.svg').write_text(sensor_svg, encoding='utf-8')

or_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="760" viewBox="0 0 110 100">
{svg_style}
<text class="t" x="3" y="6">AirMonitor V0.8 – EPDM-O-Ringe und Nuten</text>
<rect class="part" x="4" y="10" width="56" height="85"/>
<rect class="groove" x="9" y="17" width="46" height="34" rx="8"/>
<rect class="groove" x="9.1" y="53.5" width="45.8" height="42" rx="8"/>
<text class="s" x="64" y="30">P04A: Ø45 × 1,50</text>
<text class="s" x="64" y="37">P04B: Ø50 × 1,50</text>
<text class="s" x="64" y="44">Nut 1,80 breit × 1,10 tief</text>
<text class="s" x="64" y="51">Verpressung 26,7 %</text>
<rect class="part" x="4" y="101" width="53.5" height="82"/>
<rect class="groove" x="5.15" y="102.5" width="51.2" height="79" rx="8"/>
<text class="s" x="64" y="135">P08: Ø77 × 1,50</text>
<text class="s" x="64" y="142">Nut im erhöhten Pod-Rand</text>
<text class="s" x="64" y="149">Deckel bleibt 3,0 mm voll</text>
</svg>'''
(D / 'Drawing_EPDM_O_Ring_Grooves_V0.8.svg').write_text(or_svg, encoding='utf-8')

cap_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="760" viewBox="-8 -10 225 135">
{svg_style}
<text class="t" x="0" y="-5">AirMonitor V0.8 - randgefuehrter, buendiger Schiebedeckel [mm]</text>
<rect class="wall" x="0" y="0" width="208" height="112" rx="6"/>
<rect class="part" x="2.3" y="2.3" width="203.4" height="107.4" rx="3.7"/>
<rect x="0" y="0" width="208" height="112" rx="6" fill="none" stroke="#7A3FA0" stroke-width="0.7"/>
<g stroke="#b33" fill="none" stroke-width="0.8">
  <path d="M10 2.3 H18"/><path d="M10 109.7 H18"/><path d="M182 109.7 H190"/>
  <rect x="177" y="0" width="23" height="10.5"/>
</g>
<text class="s" x="60" y="106">Aussenkontur Deckel = Gehaeuse: 208 x 112, R6</text>
<text class="s" x="60" y="101">Fuehrungen nur in Randzonen; gesamte Mitte frei</text>
<text class="s" x="145" y="16">Rastung vorn rechts</text>
<text class="s" x="8" y="8">Einsetzseite offen</text>
<path d="M145 20 H137" stroke="#24566f" stroke-width="0.7"/>
<text class="s" x="145" y="25">Schliessen in Bedienansicht: links nach rechts</text>
</svg>'''
(D / 'Drawing_V08_Rounded_Overlap_Lid.svg').write_text(cap_svg, encoding='utf-8')

side_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="620" viewBox="-5 -5 218 70">
{svg_style}
<text class="t" x="0" y="-1">AirMonitor V0.8 - Seitenansicht buendiger Deckeluebergriff [mm]</text>
<path class="wall" d="M0 55 V0 H208 V55 H206 V45 H2 V55 Z"/>
<path d="M-0.5 58 H208.5 V45 H206 V55 H2 V45 H-0.5 Z" fill="#F1E8F7" stroke="#7A3FA0" stroke-width="0.5"/>
<rect x="36.6" y="12" width="122" height="33" fill="white" stroke="#172b3a" stroke-width="0.4"/>
<text class="s" x="162" y="50">10 mm Uebergriff</text>
<text class="s" x="70" y="30">freie Oeffnung 122 x 33</text>
<text class="s" x="70" y="62">Topplatte 3 mm; Oberseite Druckbettseite</text>
</svg>'''
(D / 'Drawing_V08_Overlap_Lid_Side.svg').write_text(side_svg, encoding='utf-8')


guide_section_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="650" viewBox="0 43 16 15">
<style>text{{font-family:Arial,sans-serif;fill:#172b3a}}.t{{font-size:.55px;font-weight:bold}}.s{{font-size:.42px}}.lid{{fill:#f0b27a;stroke:#7d4e24;stroke-width:.08}}.body{{fill:#a9dfbf;stroke:#246b3d;stroke-width:.08}}.cut{{fill:white;stroke:#b33;stroke-width:.10}}.dim{{stroke:#b33;stroke-width:.08}}</style>
<text class="t" x="0.3" y="44.0">V0.8 Schnitt: innenliegende 45-Grad-Schiebefuehrung</text>
<rect class="lid" x="0" y="45" width="2.6" height="10"/>
<polygon class="cut" points="2.75,46.4 1.60,47.55 1.60,51.35 2.75,50.2"/>
<rect class="body" x="2.9" y="45" width="4.0" height="10"/>
<polygon class="body" points="2.9,46.8 2.0,47.7 2.0,50.7 2.9,49.8"/>
<text class="s" x="7.2" y="47.2">Deckelaussenhaut bleibt geschlossen</text>
<text class="s" x="7.2" y="48.2">diagonale Nut und Zunge: 45 Grad</text>
<text class="s" x="7.2" y="49.2">0,30 mm Schulterspiel</text>
<text class="s" x="7.2" y="50.2">kein horizontaler C-Kanal</text>
<text class="s" x="7.2" y="51.2">P02 sichtbare Oberseite auf Druckbett</text>
</svg>'''
(D / 'Drawing_V08_45deg_Guide_Section.svg').write_text(guide_section_svg, encoding='utf-8')

edge_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="700" viewBox="-5 -8 218 128">
{{svg_style}}
<text class="t" x="0" y="-3">AirMonitor V0.8 - vier verdeckte Randfuehrungen, Mitte frei [mm]</text>
<rect class="wall" x="0" y="0" width="208" height="112" rx="6"/>
<g fill="#d7e6ef" stroke="#24566f" stroke-width=".6">
  <rect x="15" y="1" width="6" height="3"/><rect x="187" y="1" width="6" height="3"/>
  <rect x="15" y="108" width="6" height="3"/><rect x="187" y="108" width="6" height="3"/>
</g>
<rect x="28" y="8" width="152" height="96" fill="none" stroke="#278c73" stroke-width=".5" stroke-dasharray="2 2"/>
<text class="s" x="72" y="56">gesamte mittlere Zone ohne Deckelfixierung</text>
<text class="s" x="6" y="9">X18</text><text class="s" x="184" y="9">X190 + versteckte Rastung</text>
<path d="M140 18 H132" stroke="#b33" stroke-width=".8"/><text class="s" x="142" y="19">Bedienansicht: links nach rechts</text>
</svg>'''
(D / 'Drawing_V08_Edge_Guide_Positions.svg').write_text(edge_svg, encoding='utf-8')

slide_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="620" viewBox="0 0 210 72">
{{svg_style}}
<text class="t" x="2" y="6">V0.8 Schiebeablauf - Funktion wie vorher, nur druckgerechte Innenprofile</text>
<rect class="wall" x="2" y="14" width="92" height="48" rx="5"/>
<rect x="10" y="20" width="92" height="48" rx="5" fill="none" stroke="#7A3FA0" stroke-width=".7"/>
<text class="s" x="25" y="38">1. +8 mm versetzt absenken</text>
<text class="s" x="25" y="44">Zungen in innere Einfuehrtaschen</text>
<rect class="wall" x="112" y="14" width="92" height="48" rx="5"/>
<rect x="112" y="14" width="92" height="48" rx="5" fill="none" stroke="#7A3FA0" stroke-width=".7"/>
<text class="s" x="132" y="38">2. 8 mm einschieben</text>
<text class="s" x="132" y="44">verdeckt gefuehrt und eingerastet</text>
<path d="M99 38 H109" stroke="#b33" stroke-width="1"/>
</svg>'''
(D / 'Drawing_V08_Slide_Sequence.svg').write_text(slide_svg, encoding='utf-8')

print('Generated AirMonitor Compact V0.8 corrected O-ring package:', R)
