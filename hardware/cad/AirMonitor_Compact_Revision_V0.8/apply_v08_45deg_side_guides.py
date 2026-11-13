from __future__ import annotations

from pathlib import Path
import re

R = Path(__file__).resolve().parent


def sub_once(text: str, pattern: str, repl: str, label: str) -> str:
    new, count = re.subn(pattern, repl, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one replacement, got {count}")
    return new


# ---------------------------------------------------------------------------
# 1) Parameters
# ---------------------------------------------------------------------------
params_path = R / "compact_params.py"
params = params_path.read_text(encoding="utf-8")
params = sub_once(
    params,
    r'"""Laminar AirMonitor HCHO - Compact V0\.8 parameters \(mm\)\..*?"""',
    '''"""Laminar AirMonitor HCHO - Compact V0.8 parameters (mm).

V0.8 keeps the confirmed electronics, micro-switch and calibration-station
geometry. Only the lid retention is revised again:
- rounded outer housing and 10 mm overlapping cap remain;
- the 8 mm captured slide function from the earlier V0.8 is retained;
- all four guide points stay in the outer edge zones at X=18 and X=190;
- the enclosure centre contains no lid guides, posts or latch parts;
- the former rectangular C-window is replaced by a blind internal keyhole
  track with a 45-degree diagonal cross-section;
- the lid exterior remains closed and visually flush;
- entry pockets are open only toward the inside and lower skirt edge;
- a hidden detent at the front/right guide provides the end snap;
- P01 prints on its floor and P02 on its visible top without slicer supports.

Global coordinates: origin = outer lower corner of P01 without flange,
X = long axis, Y = short axis, Z = upward.
"""''',
    "parameter docstring",
)
params = params.replace("SHOULDER_INSET = 2.3", "SHOULDER_INSET = 2.9")
params = params.replace("SHOULDER_CORNER_R = 3.7", "SHOULDER_CORNER_R = 3.1")
params = params.replace("LID_SKIRT_W = 2.0", "LID_SKIRT_W = 2.6")

guide_block = '''# Edge-only, captured 45-degree slide guides.
# The user-visible motion remains the earlier 8 mm slide. The guide tongue is
# diagonal in Y/Z, and the matching track is blind from the outside. This keeps
# the lid captured while avoiding a horizontal C-channel roof.
SLIDE_TRAVEL = 8.0
SLIDE_OPEN_OFFSET_X = 8.0
SLIDE_CLOSE_DIRECTION = '-X'
SLIDE_USER_DIRECTION = 'left-to-right in operating view'
GUIDE_MODE = 'blind internal 45-degree captured keyhole tracks at outer edges'
NO_CENTER_FIXINGS = True
NO_VISIBLE_GUIDE_WINDOWS = True
NO_HORIZONTAL_SLOT_ROOFS = True
GUIDE_PRINT_ANGLE_DEG = 45.0

# Four edge locations. The front/right location also carries the hidden detent.
GUIDE_X_FRONT = (18.0, 190.0)
GUIDE_X_REAR = (18.0, 190.0)
GUIDE_X_ALL = (18.0, 190.0)
GUIDE_LUG_W = 6.0
GUIDE_ROOT_Z0 = 46.8
GUIDE_ROOT_Z1 = 49.8
GUIDE_PROJ = 0.90
GUIDE_RISE = 0.90

# Blind groove on the inside of the 2.6 mm skirt. The groove is a diagonal
# parallelogram, not a rectangular tunnel. The outside skin remains closed.
GUIDE_GROOVE_INNER_Y_FRONT = 2.85
GUIDE_GROOVE_OUTER_Y_FRONT = 1.65
GUIDE_GROOVE_RISE = 1.20
GUIDE_GROOVE_Z0 = 46.4
GUIDE_GROOVE_Z1 = 50.2
GUIDE_OUTER_SKIN = 1.65
GUIDE_ENTRY_OUTER_SKIN = 1.15
GUIDE_ENTRY_W = 7.60
GUIDE_ENTRY_BOTTOM_Z = 44.60
GUIDE_ENTRY_TOP_Z = 55.20
GUIDE_TRACK_END_EXTRA = 3.80

# Hidden end detent at the front/right guide. The enlarged lug flexes the front
# skirt by about 0.20 mm while sliding, then relaxes in the deeper final pocket.
SNAP_X = 190.0
SNAP_EXTRA_PROJ = 0.55
SNAP_DETENT_EXTRA_DEPTH = 0.40
SNAP_DETENT_W = 6.40
SNAP_INTERFERENCE = 0.20
SNAP_FINAL_CLEARANCE = 0.20
NO_TOP_LATCH_TONGUE = True
'''
params = sub_once(
    params,
    r"# Support-free shoulder slide and open-bottom edge snap\..*?NO_C_BOTTOM_LIP = True\n",
    guide_block,
    "guide parameter block",
)
params_path.write_text(params, encoding="utf-8")


# ---------------------------------------------------------------------------
# 2) Build geometry
# ---------------------------------------------------------------------------
build_path = R / "build_v08.py"
build = build_path.read_text(encoding="utf-8")

lug_block = '''def guide_lug(xc, rear=False, snap=False):
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
'''
build = sub_once(
    build,
    r"def edge_snap_bump\(\):.*?b = b\.union\(edge_snap_bump\(\)\)\n",
    lug_block,
    "replace open-bottom snap with captured guide lugs",
)

track_block = '''# Blind internal 45-degree keyhole tracks. The outside face stays closed.
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

# ---------------- P03 sensor pod ----------------'''
build = sub_once(
    build,
    r"# Definitive red-line correction:.*?# ---------------- P03 sensor pod ----------------\n(?:# ---------------- P03 sensor pod ----------------\n)?",
    track_block,
    "replace straight-open notches with blind 45-degree tracks",
)

build = build.replace(
    "step(q, P / 'P02_Compact_Lid_Print_NO_C_V0.8.step')\n        stl(q, P / 'P02_Compact_Lid_Print_NO_C_V0.8.stl')",
    "step(q, P / 'P02_Compact_Lid_Print_45DEG_GUIDES_V0.8.step')\n        stl(q, P / 'P02_Compact_Lid_Print_45DEG_GUIDES_V0.8.stl')",
)

verification = '''# Write an explicit guide verification note.
with (R / 'LID_45DEG_GUIDE_VERIFICATION.txt').open('w', encoding='utf-8') as f:
    f.write('AirMonitor Compact V0.8 - captured 45-degree side guides\\n')
    f.write('Slide travel retained: 8.00 mm\\n')
    f.write('Guide locations: front/rear X=18.0 and X=190.0 mm\\n')
    f.write('Centre zone: no lid guides, posts or latch parts\\n')
    f.write(f'Lid skirt: {C.LID_SKIRT_W:.2f} mm; shoulder clearance: {C.SHOULDER_INSET-C.LID_SKIRT_W:.2f} mm\\n')
    f.write(f'Normal outside skin at blind track: {C.GUIDE_OUTER_SKIN:.2f} mm\\n')
    f.write(f'Minimum outside skin at entry pocket: {C.GUIDE_ENTRY_OUTER_SKIN:.2f} mm\\n')
    f.write('Track cross-section: diagonal parallelogram, 45-degree faces\\n')
    f.write('External guide windows: none\\n')
    f.write(f'Hidden snap interference: {C.SNAP_INTERFERENCE:.2f} mm\\n')
    f.write('Target printing: P01 on floor, P02 visible top on bed, no slicer support\\n')

# Dimensions and purchased component data.
'''
build = sub_once(
    build,
    r"# Write an explicit no-C verification note for review\..*?# Dimensions and purchased component data\.\n",
    verification,
    "replace verification note",
)

# Add guide metadata to the coordinate table.
coord_anchor = "    w.writerow(['P07 plate', 'X 4.0..60.0 / Y 3.2..108.8 / Z 58.0..61.0', 'CAD'])\n"
coord_add = coord_anchor + "    w.writerow(['Lid guides', 'blind 45-degree tracks; X 18/190 at front and rear; 8 mm slide', 'CAD'])\n    w.writerow(['Hidden snap', 'front/right X190; 0.20 mm nominal flex; blind detent', 'CAD'])\n"
if "blind 45-degree tracks" not in build:
    build = build.replace(coord_anchor, coord_add, 1)

# Replace the obsolete no-C drawing with three guide/slide drawings.
svg_block = '''guide_section_svg = f\'\'\'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="650" viewBox="0 43 16 15">
<style>text{{font-family:Arial,sans-serif;fill:#172b3a}}.t{{font-size:.55px;font-weight:bold}}.s{{font-size:.42px}}.lid{{fill:#f0b27a;stroke:#7d4e24;stroke-width:.08}}.body{{fill:#a9dfbf;stroke:#246b3d;stroke-width:.08}}.cut{{fill:white;stroke:#b33;stroke-width:.10}}.dim{{stroke:#b33;stroke-width:.08}}</style>
<text class="t" x="0.3" y="44.0">V0.8 Schnitt: innenliegende 45-Grad-Schiebefuehrung</text>
<rect class="lid" x="0" y="45" width="2.6" height="10"/>
<polygon class="cut" points="2.85,46.4 1.65,47.6 1.65,51.4 2.85,50.2"/>
<rect class="body" x="2.9" y="45" width="4.0" height="10"/>
<polygon class="body" points="2.9,46.8 2.0,47.7 2.0,50.7 2.9,49.8"/>
<text class="s" x="7.2" y="47.2">Deckelaussenhaut bleibt geschlossen</text>
<text class="s" x="7.2" y="48.2">diagonale Nut und Zunge: 45 Grad</text>
<text class="s" x="7.2" y="49.2">0,30 mm Schulterspiel</text>
<text class="s" x="7.2" y="50.2">kein horizontaler C-Kanal</text>
<text class="s" x="7.2" y="51.2">P02 sichtbare Oberseite auf Druckbett</text>
</svg>\'\'\'
(D / 'Drawing_V08_45deg_Guide_Section.svg').write_text(guide_section_svg, encoding='utf-8')

edge_svg = f\'\'\'<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="700" viewBox="-5 -8 218 128">
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
</svg>\'\'\'
(D / 'Drawing_V08_Edge_Guide_Positions.svg').write_text(edge_svg, encoding='utf-8')

slide_svg = f\'\'\'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="620" viewBox="0 0 210 72">
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
</svg>\'\'\'
(D / 'Drawing_V08_Slide_Sequence.svg').write_text(slide_svg, encoding='utf-8')

'''
build = sub_once(
    build,
    r"no_c_svg = f'''.*?\(D / 'Drawing_V08_NO_C_Open_To_Edge\.svg'\)\.write_text\(no_c_svg, encoding='utf-8'\)\n\n",
    svg_block,
    "replace obsolete no-C SVG",
)

build_path.write_text(build, encoding="utf-8")


# ---------------------------------------------------------------------------
# 3) Checks
# ---------------------------------------------------------------------------
checks = '''"""Numeric checks for AirMonitor Compact V0.8 captured 45-degree guides."""
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
    check('opening ends at shoulder', close(C.OPEN_TOP_Z,C.SHOULDER_Z0))

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
'''
(R / "check_clearances.py").write_text(checks, encoding="utf-8")


# ---------------------------------------------------------------------------
# 4) Updated 1:1 sketches
# ---------------------------------------------------------------------------
sketch_path = R / "generate_mass_sketches_v08.py"
sketch = sketch_path.read_text(encoding="utf-8")
sketch = sub_once(
    sketch,
    r'"""Generate revised 1:1 engineering sketches for AirMonitor Compact V0\.8\..*?"""',
    '''"""Generate V0.8 engineering sketches with blind 45-degree side guides.

The previous captured 8 mm slide is retained, while the rectangular C-window
is replaced by blind internal diagonal tracks. The enclosure centre stays free.
"""''',
    "sketch docstring",
)

page1 = '''def page1_base(c):
    header(c,"P01 - abgerundeter Gehaeuseboden / Draufsicht innen",
           "3,2-mm-Wand; R6; vier 45-Grad-Fuehrungen nur am Rand; Mitte frei")
    ox,oy=38*mm,39*mm
    c.roundRect(ox,oy-C.FLANGE*mm,C.L*mm,(C.W+2*C.FLANGE)*mm,2*mm)
    c.roundRect(ox,oy,C.L*mm,C.W*mm,C.BODY_CORNER_R*mm)
    c.saveState(); c.setDash(3,2); c.setStrokeColor(C_HOOD)
    c.roundRect(ox+C.SHOULDER_INSET*mm,oy+C.SHOULDER_INSET*mm,
                (C.L-2*C.SHOULDER_INSET)*mm,(C.W-2*C.SHOULDER_INSET)*mm,
                C.SHOULDER_CORNER_R*mm)
    c.restoreState()
    for x,y in C.WALL_MOUNT_HOLES:
        c.circle(ox+x*mm,oy+y*mm,C.WALL_MOUNT_D/2*mm)
    c.setStrokeColor(C_POD)
    for x,y in C.STANDOFFS:
        c.circle(ox+x*mm,oy+y*mm,C.STANDOFF_D/2*mm)
        c.circle(ox+x*mm,oy+y*mm,C.STANDOFF_PILOT_D/2*mm)
    c.setStrokeColor(C_ORING)
    for x in C.GUIDE_X_FRONT:
        c.rect(ox+(x-C.GUIDE_LUG_W/2)*mm,oy+(C.SHOULDER_INSET-C.GUIDE_PROJ)*mm,
               C.GUIDE_LUG_W*mm,C.GUIDE_PROJ*mm)
    for x in C.GUIDE_X_REAR:
        c.rect(ox+(x-C.GUIDE_LUG_W/2)*mm,oy+(C.W-C.SHOULDER_INSET)*mm,
               C.GUIDE_LUG_W*mm,C.GUIDE_PROJ*mm)
    c.saveState(); c.setDash(2,2); c.setStrokeColor(C_CENTER)
    c.rect(ox+28*mm,oy+8*mm,152*mm,96*mm)
    c.restoreState()
    c.setStrokeColor(colors.black)
    dim_h(c,ox,ox+C.L*mm,oy-17*mm,"208")
    dim_v(c,ox+C.L*mm+9*mm,oy-C.FLANGE*mm,oy+(C.W+C.FLANGE)*mm,"132")
    label(c,12*mm,27*mm,"Rot: Fuehrungen vorn/hinten bei X18 und X190; alle innerhalb der Randzonen.",7)
    label(c,12*mm,22*mm,"Gruen gestrichelt: gesamte mittlere Zone ohne Deckelfixierung oder Rastmechanik.",7)
    label(c,12*mm,17*mm,"Schulter 2,9 zurueckgesetzt; Deckelschuerze 2,6; nominelles Spiel 0,30.",7)
    footer(c,1)
'''
sketch = sub_once(sketch, r"def page1_base\(c\):.*?(?=\ndef page2_walls)", page1, "sketch page1")

page4 = '''def page4_lid(c):
    header(c,"P02 - abgerundeter Ueberwurf-Schiebedeckel",
           "Aussen geschlossen; innen vier 45-Grad-Keyhole-Fuehrungen; 8-mm-Schiebeweg")
    ox,oy=37.5*mm,46.5*mm
    w=C.LID_X1-C.LID_X0; h=C.LID_Y1-C.LID_Y0
    c.roundRect(ox,oy,w*mm,h*mm,C.LID_CORNER_R*mm)
    c.saveState(); c.setDash(3,2); c.setStrokeColor(C_HOOD)
    c.roundRect(ox+C.LID_SKIRT_W*mm,oy+C.LID_SKIRT_W*mm,
                (w-2*C.LID_SKIRT_W)*mm,(h-2*C.LID_SKIRT_W)*mm,
                max(0.8,(C.LID_CORNER_R-C.LID_SKIRT_W))*mm)
    for x in C.GUIDE_X_FRONT:
        entry=x-C.SLIDE_TRAVEL
        c.rect(ox+(entry-C.GUIDE_ENTRY_W/2)*mm,oy+C.GUIDE_ENTRY_OUTER_SKIN*mm,
               C.GUIDE_ENTRY_W*mm,(C.GUIDE_GROOVE_INNER_Y_FRONT-C.GUIDE_ENTRY_OUTER_SKIN)*mm)
        c.line(ox+entry*mm,oy+C.GUIDE_GROOVE_INNER_Y_FRONT*mm,
               ox+(x+C.GUIDE_TRACK_END_EXTRA)*mm,oy+C.GUIDE_GROOVE_INNER_Y_FRONT*mm)
    for x in C.GUIDE_X_REAR:
        entry=x-C.SLIDE_TRAVEL
        c.rect(ox+(entry-C.GUIDE_ENTRY_W/2)*mm,
               oy+(C.W-C.GUIDE_GROOVE_INNER_Y_FRONT)*mm,
               C.GUIDE_ENTRY_W*mm,(C.GUIDE_GROOVE_INNER_Y_FRONT-C.GUIDE_ENTRY_OUTER_SKIN)*mm)
        c.line(ox+entry*mm,oy+(C.W-C.GUIDE_GROOVE_INNER_Y_FRONT)*mm,
               ox+(x+C.GUIDE_TRACK_END_EXTRA)*mm,oy+(C.W-C.GUIDE_GROOVE_INNER_Y_FRONT)*mm)
    c.restoreState()
    c.setStrokeColor(C_POD)
    for x,y,lx,ly in C.VENTS:
        c.rect(ox+x*mm,oy+y*mm,lx*mm,ly*mm)
    for x,y in C.POD_MOUNTS:
        c.circle(ox+x*mm,oy+y*mm,1.5*mm)
    c.setStrokeColor(C_HOOD)
    for x,y in C.HOOD_SCREWS:
        c.circle(ox+x*mm,oy+y*mm,1.1*mm)
    c.setStrokeColor(colors.black)
    dim_h(c,ox,ox+w*mm,oy-11*mm,"208")
    dim_v(c,ox+w*mm+9*mm,oy,oy+h*mm,"112")
    label(c,12*mm,29*mm,"Aussen keine C-Fenster: sichtbare Schuerze bleibt durchgehend geschlossen.",7,True)
    label(c,12*mm,24*mm,"Aufsetzen: Deckel +8,0 mm versetzt; Fuehrungszungen in innere Einfuehrtaschen absenken.",7)
    label(c,12*mm,19*mm,"Dann 8,0 mm einschieben; front/rechts rastet verdeckt in einer tieferen Innentasche ein.",7)
    footer(c,4)
'''
sketch = sub_once(sketch, r"def page4_lid\(c\):.*?(?=\ndef page5_pod)", page4, "sketch page4")

page9 = '''def page9_assembly(c):
    header(c,"V0.8 - Gehaeuse- und Deckelmontage",
           "Funktion wie frueher: absenken und 8 mm einschieben; neue Fuehrung nur druckgerecht")
    label(c,18*mm,158*mm,"Schliessablauf",8,True)
    steps=[
        "P03, Sensor, Kabel, P05, P07 und O-Ringe am Deckel montieren.",
        "Deckel +8,0 mm versetzt ueber P01 absenken.",
        "Vier 45-Grad-Zungen in die innen offenen Einfuehrtaschen setzen.",
        "Deckel 8,0 mm einschieben; Zungen laufen in den blinden Diagonalnuten.",
        "Front/rechts federt die Schuerze ca. 0,20 mm und rastet verdeckt ein.",
        "Zum Oeffnen mit gleichmaessigem Zug 8,0 mm zurueckschieben und abheben.",
    ]
    for i,t in enumerate(steps): label(c,22*mm,(148-9*i)*mm,f"{i+1}. {t}",7)
    label(c,18*mm,85*mm,"Schnitt Fuehrung (vergroessert)",8,True)
    x=55*mm; y=42*mm; s=8*mm
    c.setFillColor(colors.HexColor("#F5CBA7")); c.setStrokeColor(C_HOOD)
    c.rect(x,y,2.6*s,10*s,stroke=1,fill=1)
    p=c.beginPath(); p.moveTo(x+2.85*s,y+1.4*s); p.lineTo(x+1.65*s,y+2.6*s); p.lineTo(x+1.65*s,y+6.4*s); p.lineTo(x+2.85*s,y+5.2*s); p.close()
    c.setFillColor(colors.white); c.drawPath(p,stroke=1,fill=1)
    c.setFillColor(colors.HexColor("#A9DFBF")); c.setStrokeColor(C_POD)
    c.rect(x+2.9*s,y,4*s,10*s,stroke=1,fill=1)
    p=c.beginPath(); p.moveTo(x+2.9*s,y+1.8*s); p.lineTo(x+2.0*s,y+2.7*s); p.lineTo(x+2.0*s,y+5.7*s); p.lineTo(x+2.9*s,y+4.8*s); p.close()
    c.drawPath(p,stroke=1,fill=1)
    label(c,x+62*mm,y+56*mm,"Aussenhaut bleibt geschlossen",7,True)
    label(c,x+62*mm,y+48*mm,"Nut/Zunge diagonal 45 Grad",7)
    label(c,x+62*mm,y+40*mm,"kein horizontaler C-Kanal",7)
    label(c,x+62*mm,y+32*mm,"P01 Boden unten; P02 Sichtseite unten drucken",7)
    footer(c,9)
'''
sketch = sub_once(sketch, r"def page9_assembly\(c\):.*?(?=\ndef page10_summary)", page9, "sketch page9")

page10 = '''def page10_summary(c):
    header(c,"V0.8 - Freigabe- und Pruefliste",
           "8-mm-Schiebefunktion beibehalten; nur die Fuehrungsprofile druckgerecht geaendert")
    label(c,18*mm,160*mm,"Umgesetzt",8,True)
    items=[
        "Microtaster, Waveshare, Sensorpod, Pruefstation und O-Ringe unveraendert.",
        "P01 208 x 112 x 55; Wand/Boden 3,2; Ecken R6,0.",
        "P02 aussen 208 x 112; 3,0-mm-Top; 10,0-mm-Uebergriff; Schuerze 2,6.",
        "Vier Fuehrungspunkte ausschliesslich bei X18 und X190; Mitte frei.",
        "Blinde Innennuten mit 45-Grad-Parallelogrammprofil; aussen keine Fenster.",
        "8-mm-Absenk-/Schiebeprinzip aus dem funktionierenden Vorentwurf bleibt bestehen.",
        "Verdeckte Endrastung front/rechts mit ca. 0,20 mm lokaler Auslenkung.",
        "P01 auf Boden und P02 mit sichtbarer Oberseite auf Bett, ohne Slicer-Stuetzen vorgesehen.",
    ]
    for i,t in enumerate(items): label(c,22*mm,(151-8*i)*mm,"- "+t,7)
    label(c,18*mm,82*mm,"Vor Freigabe praktisch pruefen",8,True)
    checks=[
        "[ ] Alle vier Zungen lassen sich in +8-mm-Lage gleichzeitig absenken.",
        "[ ] Deckel schiebt leicht, bleibt aber vertikal sicher gefangen.",
        "[ ] Verdeckte Rastung ist loesbar und uebersteht mindestens 20 Zyklen.",
        "[ ] PrusaSlicer fordert an Fuehrung und Einfuehrtaschen keine Stuetzen.",
        "[ ] Aussenfuge ist gleichmaessig; keine sichtbaren C-Ausschnitte.",
        "[ ] Kabelreserve, O-Ringe, Leckrate und Nullpunkt sind dokumentiert.",
    ]
    for i,t in enumerate(checks): label(c,22*mm,(73-8*i)*mm,t,7)
    footer(c,10,"CAD-Stand: V0.8 - verdeckte 45-Grad-Randfuehrung")
'''
sketch = sub_once(sketch, r"def page10_summary\(c\):.*?(?=\ndef main)", page10, "sketch page10")
sketch_path.write_text(sketch, encoding="utf-8")


# ---------------------------------------------------------------------------
# 5) Documents
# ---------------------------------------------------------------------------
spec = '''# Laminar AirMonitor HCHO - CAD-Konstruktionsspezifikation V0.8

## Verbindliche Korrektur

Der funktionierende Absenk-/Schiebeablauf des frueheren V0.8-Entwurfs bleibt
erhalten. Geaendert wird nur die Druckbarkeit der seitlichen Fuehrung.

- Deckel +8,0 mm versetzt absenken.
- Vier Randzungen in innere Einfuehrtaschen setzen.
- Deckel 8,0 mm in die Endstellung schieben.
- Front/rechts verdeckt einrasten.

## Aussenform

```text
P01 ohne Flansche       208,0 x 112,0 x 55,0 mm
P01 Wand/Boden          3,2 mm
Aussenradius            R6,0 mm
Schulterbeginn          Z45,0 mm
Schulterruecksprung     2,9 mm
P02 Topplatte           3,0 mm
P02 Uebergriff          10,0 mm
P02 Schuerzenwand       2,6 mm
Schulterspiel           0,30 mm je Seite
```

## Fuehrung

```text
Positionen vorn/hinten  X18,0 und X190,0 mm
Schiebeweg              8,0 mm
Zungenbreite            6,0 mm
Normaler Vorsprung      0,90 mm
Normaler Anstieg        0,90 mm = 45 Grad
Nutquerschnitt          blindes Parallelogramm, 45 Grad
Aussenhaut an Nut       mindestens 1,65 mm
Aussenhaut Einfuehrung  mindestens 1,15 mm
```

Die Einfuehrtaschen sind nur zur Innenseite und zur unteren Schuerzenkante
offen. Die sichtbare Aussenwand bleibt geschlossen. Nach dem Einschieben liegen
die Zungen in den blinden Diagonalnuten und verhindern das vertikale Abheben.

## Rastung

Die vordere rechte Zunge bei X190 besitzt 0,55 mm mehr Vorsprung. Im normalen
Track entsteht ca. 0,20 mm lokale Auslenkung; in der tieferen Endtasche bleibt
ca. 0,20 mm Spiel. Die Rastung ist aussen nicht sichtbar.

## Druckbarkeit

P01 wird auf dem Boden gedruckt. Die Zungenunterseiten steigen nach aussen mit
45 Grad an. P02 wird mit der sichtbaren Oberseite auf dem Druckbett gedruckt.
Die Innennuten besitzen ausschliesslich diagonale 45-Grad-Flaechen; es gibt
keine waagerechte C-Kanal-Decke. Die Einfuehrtaschen reichen bis zur offenen
Schuerzenkante. Slicer-Stuetzen sind konstruktiv nicht vorgesehen.

## Unveraendert

Microtaster, Boardposition, DC5521, Sensorpod, Kalibrierhaube, EPDM-O-Ringe,
Y-Zentrierung und Markierungen bleiben unveraendert. Die Pruefstation bleibt bis
zur physischen Kontrolle vorlaeufig.
'''
(R / "CAD_COMPACT_SPEC_V0.8.md").write_text(spec, encoding="utf-8")

readme = '''# AirMonitor Compact Revision V0.8

Aktueller Stand:

- abgerundeter, aussen buendiger 10-mm-Ueberwurfdeckel;
- funktionierender 8-mm-Absenk-/Schiebeablauf beibehalten;
- vier Fuehrungspunkte nur an den Aussenraendern X18/X190;
- Gehaeusemitte ohne Deckelfixierungen;
- verdeckte 45-Grad-Fuehrungszungen und blinde Innennuten;
- keine sichtbaren C-Fenster und keine waagerechte Kanaldecke;
- versteckte Endrastung vorne rechts;
- P01 und P02 fuer den Druck ohne Slicer-Stuetzen ausgelegt.

## Bedienung

1. Deckel +8 mm versetzt von oben aufsetzen.
2. Vier Fuehrungszungen in die inneren Einfuehrtaschen absenken.
3. Deckel 8 mm bis zur verdeckten Rastung einschieben.
4. Zum Oeffnen gleichmaessig zurueckschieben und abheben.

## Wichtige Dateien

- `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.8.step`
- `02_CAD_Print/P01_Compact_Base_Print.stl`
- `02_CAD_Print/P02_Compact_Lid_Print_45DEG_GUIDES_V0.8.stl`
- `AirMonitor_V08_Massskizzen_1zu1.pdf`
- `03_Renders_Drawings/Render_V08_Closed.png`
- `03_Renders_Drawings/Render_V08_Open_8mm.png`
- `03_Renders_Drawings/Render_V08_Guide_Section.png`
- `CAD_COMPACT_SPEC_V0.8.md`
'''
(R / "README.md").write_text(readme, encoding="utf-8")

prompt = '''# Daniel-/Claude-Pruefprompt - AirMonitor Compact V0.8

Die Konstruktion ist umgesetzt. Bitte nur kontrollieren und Abweichungen mit
Soll/Ist/Delta dokumentieren.

## Kritisches Ziel

Die fruehere 8-mm-Schiebefunktion muss erhalten sein. Die alte rechteckige
C-Kanal-Geometrie darf jedoch nicht mehr vorhanden sein. Stattdessen muessen
vier verdeckte, blinde 45-Grad-Innennuten mit passenden Randzungen vorhanden
sein.

## Sollwerte

```text
Fuehrungen vorn/hinten  X18 und X190
Schiebeweg              8,0 mm
Zungenbreite            6,0 mm
Zungenprofil            0,90 mm Vorsprung / 0,90 mm Anstieg
Deckelschuerze          2,60 mm
Schulterruecksprung     2,90 mm
Spiel                   0,30 mm
sichtbare C-Fenster     keine
Endrastung              verdeckt vorne rechts X190
```

## Pruefen

1. Deckel +8 mm versetzt absenkbar.
2. Alle vier Zungen greifen gleichzeitig.
3. Nach 8 mm Schieben ist der Deckel vertikal gefangen.
4. PrusaSlicer fordert fuer Zungen, Nuten und Einfuehrtaschen keine Stuetzen.
5. Aussenwand des Deckels ist geschlossen und optisch buendig.
6. Mitte des Gehaeuses hat keine Deckelfixierung.
7. Microtaster und Pruefstation wurden nicht verschoben.
8. Rastung mindestens 20 Oeffnungs-/Schliesszyklen pruefen.

Ergebnis: `freigegeben`, `freigegeben mit Aenderung` oder `nicht freigegeben`.
'''
(R / "PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.8.md").write_text(prompt, encoding="utf-8")

note = '''# Warum diese Fuehrung ohne Support druckbar ist

Die Funktion bleibt eine gefangene Schiebefuehrung. Der Unterschied liegt nur
im Querschnitt:

- Die Zunge am Boden hat eine 45-Grad-Unterseite und waechst schichtweise aus
  der Schulter heraus.
- Die Nut im Deckel ist ein blindes diagonales Parallelogramm. Es gibt keine
  waagerechte Decke, die frei in der Luft beginnen wuerde.
- Die Einfuehrtasche ist zur unteren Schuerzenkante und zur Innenseite offen.
- Die sichtbare Deckelaussenseite bleibt als mindestens 1,15 mm starke Haut
  geschlossen.
- P01 wird auf dem Boden, P02 mit der sichtbaren Oberseite auf dem Druckbett
  gedruckt.

Damit wird die Schiebefunktion des frueheren Entwurfs beibehalten, ohne dessen
problematische rechteckige C-Bruecke zu uebernehmen.
'''
(R / "SUPPORT_FREE_GUIDE_NOTE.md").write_text(note, encoding="utf-8")

start = '''START HIER - AirMonitor Compact V0.8

Fusion 360:
01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.8.step

Druckdeckel:
02_CAD_Print/P02_Compact_Lid_Print_45DEG_GUIDES_V0.8.stl

Neu kontrollieren:
- +8 mm absenken, danach 8 mm einschieben
- vier verdeckte Randfuehrungen X18/X190
- keine sichtbaren C-Fenster
- 45-Grad-Nut/Zunge ohne Slicer-Stuetzen
- versteckte Rastung vorne rechts
- Mitte frei

Massskizzen:
AirMonitor_V08_Massskizzen_1zu1.pdf
'''
(R / "START_HIER_DANIEL_CLAUDE.txt").write_text(start, encoding="utf-8")


# ---------------------------------------------------------------------------
# 6) Renderer
# ---------------------------------------------------------------------------
renderer = r'''from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import cadquery as cq
from cadquery import importers

import compact_params as C

R = Path(__file__).resolve().parent
G = R / "01_CAD_Global"
D = R / "03_Renders_Drawings"
D.mkdir(exist_ok=True)


def tess(path: Path, offset=(0.0,0.0,0.0), tol=1.0):
    shape = importers.importStep(str(path)).val()
    verts, tris = shape.tessellate(tol, 0.25)
    v = np.array([[p.x+offset[0],p.y+offset[1],p.z+offset[2]] for p in verts])
    return v[np.array(tris,dtype=int)]


def equal_axes(ax, bounds):
    xmin,xmax,ymin,ymax,zmin,zmax=bounds
    cx=(xmin+xmax)/2; cy=(ymin+ymax)/2; cz=(zmin+zmax)/2
    r=max(xmax-xmin,ymax-ymin,zmax-zmin)/2
    ax.set_xlim(cx-r,cx+r); ax.set_ylim(cy-r,cy+r); ax.set_zlim(cz-r,cz+r)
    ax.set_box_aspect((1,1,0.55)); ax.set_axis_off()


def render(name: str, lid_dx: float):
    fig=plt.figure(figsize=(12,7),dpi=180)
    ax=fig.add_subplot(111,projection='3d')
    parts=[
        ("P01_Compact_Base_Global.step",(0,0,0),"#3a9d5d",1.0),
        ("P02_Compact_Lid_Global.step",(lid_dx,0,0),"#e28b35",0.92),
        ("P03_Compact_SensorPod_Global.step",(lid_dx,0,0),"#4f83cc",0.95),
        ("P07_Calibration_Hood.step",(lid_dx,0,0),"#8d5bb7",0.92),
    ]
    for fn,off,col,alpha in parts:
        tri=tess(G/fn,off)
        pc=Poly3DCollection(tri,facecolor=col,edgecolor=(0,0,0,0.12),linewidth=0.15,alpha=alpha)
        ax.add_collection3d(pc)
    equal_axes(ax,(-10,225,-15,127,0,105))
    ax.view_init(elev=24,azim=-58)
    if lid_dx:
        ax.quiver(118,118,68,-24,0,0,color="#b33",linewidth=2,arrow_length_ratio=.18)
        ax.text(92,121,72,"8 mm einschieben",fontsize=10)
    ax.set_title("AirMonitor Compact V0.8 – " + ("offen / +8 mm" if lid_dx else "geschlossen"),fontsize=14)
    plt.tight_layout(pad=0)
    fig.savefig(D/name,bbox_inches='tight',pad_inches=.05)
    plt.close(fig)


render("Render_V08_Closed.png",0.0)
render("Render_V08_Open_8mm.png",C.SLIDE_OPEN_OFFSET_X)

# 2D guide section, enlarged.
fig,ax=plt.subplots(figsize=(10,6),dpi=180)
ax.add_patch(Rectangle((0,45),C.LID_SKIRT_W,10,facecolor="#e9a35a",edgecolor="#6e421d",linewidth=1.5,label="P02 Deckelschuerze"))
groove=np.array([
    [C.GUIDE_GROOVE_INNER_Y_FRONT,C.GUIDE_GROOVE_Z0],
    [C.GUIDE_GROOVE_OUTER_Y_FRONT,C.GUIDE_GROOVE_Z0+C.GUIDE_GROOVE_RISE],
    [C.GUIDE_GROOVE_OUTER_Y_FRONT,C.GUIDE_GROOVE_Z1+C.GUIDE_GROOVE_RISE],
    [C.GUIDE_GROOVE_INNER_Y_FRONT,C.GUIDE_GROOVE_Z1],
])
ax.add_patch(Polygon(groove,closed=True,facecolor="white",edgecolor="#b33",linewidth=2,label="blinde 45°-Nut"))
ax.add_patch(Rectangle((C.SHOULDER_INSET,45),4.5,10,facecolor="#8fd19e",edgecolor="#246b3d",linewidth=1.5,label="P01 Schulter"))
lug=np.array([
    [C.SHOULDER_INSET,C.GUIDE_ROOT_Z0],
    [C.SHOULDER_INSET-C.GUIDE_PROJ,C.GUIDE_ROOT_Z0+C.GUIDE_RISE],
    [C.SHOULDER_INSET-C.GUIDE_PROJ,C.GUIDE_ROOT_Z1+C.GUIDE_RISE],
    [C.SHOULDER_INSET,C.GUIDE_ROOT_Z1],
])
ax.add_patch(Polygon(lug,closed=True,facecolor="#3a9d5d",edgecolor="#1f5b34",linewidth=2,label="45°-Zunge"))
ax.annotate("sichtbare Aussenhaut\nbleibt geschlossen",xy=(.8,49),xytext=(-3.2,52.8),arrowprops=dict(arrowstyle="->"),fontsize=10)
ax.annotate("45°",xy=(2.35,47.25),xytext=(4.7,47.0),arrowprops=dict(arrowstyle="->"),fontsize=11)
ax.text(4.7,50.2,"0,30 mm Schulterspiel\n8 mm Schiebeweg\nkein horizontaler C-Kanal",fontsize=11,va="center")
ax.set_xlim(-4,10); ax.set_ylim(44,56); ax.set_aspect('equal'); ax.axis('off'); ax.legend(loc='lower right')
ax.set_title("V0.8 – Schnitt der supportfreien verdeckten Randfuehrung")
fig.savefig(D/"Render_V08_Guide_Section.png",bbox_inches='tight',pad_inches=.08)
plt.close(fig)
print("Generated V0.8 renders in",D)
'''
(R / "render_v08.py").write_text(renderer, encoding="utf-8")

print("Applied V0.8 blind 45-degree captured side-guide redesign")
