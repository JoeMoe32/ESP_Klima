from __future__ import annotations

from pathlib import Path

R = Path(__file__).resolve().parent


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return text.replace(old, new, 1)


def patch_params() -> None:
    p = R / "compact_params.py"
    text = p.read_text(encoding="utf-8")
    text = text.replace(
        "- four wall-integrated, 45-degree printable slide lugs and through-slots;\n"
        "- 8.0 mm slide travel and the existing end snap;\n"
        "- no additional lid columns in the enclosure centre;\n"
        "- support-free target orientation: base on its floor, lid on its visible top.\n",
        "- all lid guides moved to the outer edge zones; the enclosure centre stays free;\n"
        "- three wall-integrated 45-degree guide lugs plus one edge snap;\n"
        "- visually flush outer contour with matching body/lid radius;\n"
        "- 8.0 mm short slide in the operating view from left to right;\n"
        "- support-free target orientation: base on its floor, lid on its visible top.\n",
    )
    text = text.replace("SHOULDER_INSET = 2.0\nSHOULDER_CORNER_R = 4.0\nNO_LID_COLUMNS = True\n",
                        "SHOULDER_INSET = 2.3\nSHOULDER_CORNER_R = 3.7\nNO_LID_COLUMNS = True\nNO_CENTER_FIXINGS = True\n")
    text = replace_once(
        text,
        "# Wall-integrated slide lugs. Lower face rises 1.2 over 1.2 = 45 degrees.\n"
        "SLIDE_TRAVEL = 8.0\n"
        "SLIDE_OPEN_OFFSET_X = 8.0\n"
        "SLIDE_CLOSE_DIRECTION = '-X'\n"
        "SIDE_LUG_X = (80.0, 172.0)\n"
        "SIDE_LUG_WIDTH = 6.0\n"
        "SIDE_LUG_PROJ = 1.2\n"
        "SIDE_LUG_Z0 = 47.0\n"
        "SIDE_LUG_Z1 = 50.0\n"
        "SIDE_LUG_RAMP = 1.2\n",
        "# Edge-only slide retention. There is no lid fixing in the central zone.\n"
        "# Global -X appears left-to-right in the defined operating/front view.\n"
        "SLIDE_TRAVEL = 8.0\n"
        "SLIDE_OPEN_OFFSET_X = 8.0\n"
        "SLIDE_CLOSE_DIRECTION = '-X'\n"
        "SLIDE_USER_DIRECTION = 'left-to-right in operating view'\n"
        "SIDE_LUG_X_FRONT = (18.0,)\n"
        "SIDE_LUG_X_REAR = (18.0, 190.0)\n"
        "SIDE_LUG_X = tuple(sorted(set(SIDE_LUG_X_FRONT + SIDE_LUG_X_REAR)))\n"
        "SIDE_LUG_WIDTH = 6.0\n"
        "SIDE_LUG_PROJ = 1.2\n"
        "SIDE_LUG_Z0 = 47.0\n"
        "SIDE_LUG_Z1 = 50.0\n"
        "SIDE_LUG_RAMP = 1.2\n",
        "edge lug parameters",
    )
    text = replace_once(
        text,
        "# Snap tongue remains wall-based; no free-standing central pin/column.\n"
        "LATCH_TONGUE_X = (110.0, 132.0)\n"
        "LATCH_TONGUE_Y = (0.0, 10.5)\n"
        "LATCH_SLOT_W = 0.9\n"
        "LATCH_TONGUE_SKIN = 1.20\n"
        "LATCH_HOLE = (116.0, 2.2, 3.4)\n"
        "LATCH_PIN = (116.0, 2.2)\n"
        "LATCH_PIN_SEGMENTS = [(3.0, 0.8), (2.2, 0.7), (1.2, 0.7)]\n"
        "LATCH_SKIRT_NOTCH_X = (108.0, 134.0)\n",
        "# End snap moved to the front/right edge zone; centre remains completely free.\n"
        "LATCH_TONGUE_X = (177.0, 200.0)\n"
        "LATCH_TONGUE_Y = (0.0, 10.5)\n"
        "LATCH_SLOT_W = 0.9\n"
        "LATCH_TONGUE_SKIN = 1.20\n"
        "LATCH_HOLE = (184.0, 2.2, 3.4)\n"
        "LATCH_PIN = (184.0, 2.2)\n"
        "LATCH_PIN_SEGMENTS = [(3.0, 0.8), (2.2, 0.7), (1.2, 0.7)]\n"
        "LATCH_SKIRT_NOTCH_X = (175.0, 202.0)\n",
        "edge latch parameters",
    )
    text = text.replace("LID_OUTSET = 0.5\n", "LID_OUTSET = 0.0\n")
    text = text.replace("LID_CORNER_R = 6.5\nLID_SKIRT_W = 2.2\n",
                        "LID_CORNER_R = 6.0\nLID_SKIRT_W = 2.0\nLID_LEFT_END_OPEN = True\n")
    p.write_text(text, encoding="utf-8")


def patch_build() -> None:
    p = R / "build_v08.py"
    text = p.read_text(encoding="utf-8")
    text = text.replace(
        "and adds a flat-top short-travel sliding lid with a snap tongue.\n",
        "and adds an edge-guided, visually flush short-travel sliding lid.\n",
    )
    text = replace_once(
        text,
        "b = b.union(upper_outer.cut(upper_inner))\n\n"
        "b = b.union(rounded_prism(0, L, -C.FLANGE, 0, 2.0, 0, floor))\n",
        "b = b.union(upper_outer.cut(upper_inner))\n\n"
        "# Keep the insertion-side end wall full height. The lid has no left end\n"
        "# skirt, so it can be lowered in the +8 mm service position without\n"
        "# colliding with the shoulder. Intersecting with the rounded body\n"
        "# preserves the external R6 corner contour.\n"
        "left_end_wall = rounded_prism(0, L, 0, W, C.BODY_CORNER_R,\n"
        "                              C.SHOULDER_Z0, C.SHOULDER_H)\n"
        "left_end_wall = left_end_wall.intersect(\n"
        "    box(0, 0, C.SHOULDER_Z0, wall, W, C.SHOULDER_H))\n"
        "b = b.union(left_end_wall)\n\n"
        "b = b.union(rounded_prism(0, L, -C.FLANGE, 0, 2.0, 0, floor))\n",
        "left insertion wall",
    )
    text = replace_once(
        text,
        "for x in C.SIDE_LUG_X:\n"
        "    b = b.union(side_lug(x,False)).union(side_lug(x,True))\n",
        "for x in C.SIDE_LUG_X_FRONT:\n"
        "    b = b.union(side_lug(x, False))\n"
        "for x in C.SIDE_LUG_X_REAR:\n"
        "    b = b.union(side_lug(x, True))\n",
        "edge lug construction",
    )
    text = replace_once(
        text,
        "l = l.union(skirt_outer.cut(skirt_inner))\n\n"
        "for x,y,lx,ly in C.VENTS:\n",
        "skirt = skirt_outer.cut(skirt_inner)\n"
        "# Open the insertion-side end of the 10 mm skirt. Front/rear skirts\n"
        "# remain continuous and the opposite end closes flush in service.\n"
        "if C.LID_LEFT_END_OPEN:\n"
        "    skirt = skirt.cut(box(C.LID_X0 - 0.2, C.LID_Y0 - 0.2,\n"
        "                           lz - C.LID_OVERLAP - 0.2,\n"
        "                           C.LID_SKIRT_W + 0.6,\n"
        "                           C.LID_Y1 - C.LID_Y0 + 0.4,\n"
        "                           C.LID_OVERLAP + 0.4))\n"
        "l = l.union(skirt)\n\n"
        "for x,y,lx,ly in C.VENTS:\n",
        "open insertion skirt",
    )
    text = replace_once(
        text,
        "slot_y_front = C.LID_Y0-0.2\n"
        "slot_y_rear = C.LID_IN_Y1-0.2\n"
        "slot_depth = C.LID_SKIRT_W+0.5\n"
        "for x in C.SIDE_LUG_X:\n"
        "    entry = x-C.SLIDE_TRAVEL\n"
        "    entry_x0 = entry-C.SLOT_ENTRY_W/2\n"
        "    entry_h = C.SLOT_ENTRY_TOP_Z-(lz-C.LID_OVERLAP)+0.2\n"
        "    track_x1 = x+C.SLOT_TRACK_END_EXTRA\n"
        "    for yy in (slot_y_front,slot_y_rear):\n"
        "        l = l.cut(box(entry_x0,yy,lz-C.LID_OVERLAP-0.1,\n"
        "                      C.SLOT_ENTRY_W,slot_depth,entry_h))\n"
        "        l = l.cut(box(entry,yy,C.SLOT_TRACK_Z0,\n"
        "                      track_x1-entry,slot_depth,C.SLOT_TRACK_Z1-C.SLOT_TRACK_Z0))\n",
        "slot_y_front = C.LID_Y0 - 0.2\n"
        "slot_y_rear = C.LID_IN_Y1 - 0.2\n"
        "slot_depth = C.LID_SKIRT_W + 0.5\n\n"
        "def cut_edge_slot(shape, x, yy):\n"
        "    entry = x - C.SLIDE_TRAVEL\n"
        "    entry_x0 = entry - C.SLOT_ENTRY_W / 2\n"
        "    entry_h = C.SLOT_ENTRY_TOP_Z - (lz - C.LID_OVERLAP) + 0.2\n"
        "    track_x1 = x + C.SLOT_TRACK_END_EXTRA\n"
        "    shape = shape.cut(box(entry_x0, yy, lz - C.LID_OVERLAP - 0.1,\n"
        "                          C.SLOT_ENTRY_W, slot_depth, entry_h))\n"
        "    shape = shape.cut(box(entry, yy, C.SLOT_TRACK_Z0,\n"
        "                          track_x1 - entry, slot_depth,\n"
        "                          C.SLOT_TRACK_Z1 - C.SLOT_TRACK_Z0))\n"
        "    return shape\n\n"
        "for x in C.SIDE_LUG_X_FRONT:\n"
        "    l = cut_edge_slot(l, x, slot_y_front)\n"
        "for x in C.SIDE_LUG_X_REAR:\n"
        "    l = cut_edge_slot(l, x, slot_y_rear)\n",
        "edge slot construction",
    )
    # Replace the hard-coded cap review drawing with the edge-only layout.
    old_cap_start = "cap_svg = f'''<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1180\" height=\"760\" viewBox=\"-8 -10 225 135\">"
    cap_index = text.find(old_cap_start)
    side_index = text.find("side_svg = f'''<svg", cap_index)
    if cap_index < 0 or side_index < 0:
        raise RuntimeError("review drawing block not found")
    new_cap = '''cap_svg = f\'\'\'<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="760" viewBox="-8 -10 225 135">\n{svg_style}\n<text class="t" x="0" y="-5">AirMonitor V0.8 - randgefuehrter, buendiger Schiebedeckel [mm]</text>\n<rect class="wall" x="0" y="0" width="208" height="112" rx="6"/>\n<rect class="part" x="2.3" y="2.3" width="203.4" height="107.4" rx="3.7"/>\n<rect x="0" y="0" width="208" height="112" rx="6" fill="none" stroke="#7A3FA0" stroke-width="0.7"/>\n<g stroke="#b33" fill="none" stroke-width="0.8">\n  <path d="M10 2.3 H18"/><path d="M10 109.7 H18"/><path d="M182 109.7 H190"/>\n  <rect x="177" y="0" width="23" height="10.5"/>\n</g>\n<text class="s" x="60" y="106">Aussenkontur Deckel = Gehaeuse: 208 x 112, R6</text>\n<text class="s" x="60" y="101">Fuehrungen nur in Randzonen; gesamte Mitte frei</text>\n<text class="s" x="145" y="16">Rastung vorn rechts</text>\n<text class="s" x="8" y="8">Einsetzseite offen</text>\n<path d="M145 20 H137" stroke="#24566f" stroke-width="0.7"/>\n<text class="s" x="145" y="25">Schliessen in Bedienansicht: links nach rechts</text>\n</svg>\'\'\'\n(D / 'Drawing_V08_Rounded_Overlap_Lid.svg').write_text(cap_svg, encoding='utf-8')\n\n'''
    text = text[:cap_index] + new_cap + text[side_index:]
    text = text.replace("Deckeluebergriff", "buendiger Deckeluebergriff")
    text = text.replace("Deckel 209 x 113, R6,5", "Deckel 208 x 112, R6")
    text = text.replace("Schulter 204 x 108, R4; Spiel 0,30/Seite",
                        "Schulter 203,4 x 107,4, R3,7; Spiel 0,30/Seite")
    p.write_text(text, encoding="utf-8")


def write_checks() -> None:
    content = '''"""Numeric checks for AirMonitor Compact V0.8 edge-guide revision."""
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
'''
    (R / "check_clearances.py").write_text(content, encoding="utf-8")


def patch_sketches() -> None:
    p = R / "generate_mass_sketches_v08.py"
    text = p.read_text(encoding="utf-8")
    text = text.replace(
        "ZERO/SPAN assembly 15 mm lower, and the flat-top 8 mm sliding snap lid.\n",
        "ZERO/SPAN assembly 15 mm lower, and the edge-guided flush sliding lid.\n",
    )
    text = text.replace(
        "for x in C.SIDE_LUG_X:\n"
        "        c.rect(ox+(x-C.SIDE_LUG_WIDTH/2)*mm,oy+(C.SHOULDER_INSET-C.SIDE_LUG_PROJ)*mm,C.SIDE_LUG_WIDTH*mm,C.SIDE_LUG_PROJ*mm)\n"
        "        c.rect(ox+(x-C.SIDE_LUG_WIDTH/2)*mm,oy+(C.W-C.SHOULDER_INSET)*mm,C.SIDE_LUG_WIDTH*mm,C.SIDE_LUG_PROJ*mm)\n",
        "for x in C.SIDE_LUG_X_FRONT:\n"
        "        c.rect(ox+(x-C.SIDE_LUG_WIDTH/2)*mm,oy+(C.SHOULDER_INSET-C.SIDE_LUG_PROJ)*mm,C.SIDE_LUG_WIDTH*mm,C.SIDE_LUG_PROJ*mm)\n"
        "    for x in C.SIDE_LUG_X_REAR:\n"
        "        c.rect(ox+(x-C.SIDE_LUG_WIDTH/2)*mm,oy+(C.W-C.SHOULDER_INSET)*mm,C.SIDE_LUG_WIDTH*mm,C.SIDE_LUG_PROJ*mm)\n",
    )
    text = text.replace("Violett: Schulter je 2,0 zurueckgesetzt; Beginn Z45,0.",
                        "Violett: Schulter je 2,3 zurueckgesetzt; Beginn Z45,0.")
    text = text.replace("Rot: vier wandintegrierte Fuehrungslaschen; keine freien Deckelsaeulen.",
                        "Rot: drei Fuehrungslaschen nur an den Raendern; Mitte komplett frei.")
    text = text.replace("Koerper R6,0; Schulter R4,0; Deckel R6,5.",
                        "Koerper/Deckel R6,0 und aussen buendig; Schulter R3,7.")
    text = text.replace("209 x 113; R6,5; 10 mm Schuerze; vier Seitenschlitze und Rastzunge",
                        "208 x 112; R6; 10 mm Schuerze; Randfuehrungen und Rastung rechts")
    text = text.replace("vier Seitenschlitze", "drei randnahe Seitenschlitze")
    text = text.replace("Deckel 8 mm nach links schieben", "Deckel in der Bedienansicht 8 mm von links nach rechts schieben")
    p.write_text(text, encoding="utf-8")


def write_docs() -> None:
    spec = '''# Laminar AirMonitor HCHO - CAD-Konstruktionsspezifikation V0.8

## 1. Verbindlicher Stand

V0.8 übernimmt die bestätigte Microtaster-Baugruppe sowie Waveshare,
Sensorpod, Prüfstation, DC5521, Markierungen und EPDM-O-Ringe. Die
Prüfstation bleibt bis zur physischen Kontrolle vorläufig.

Die Deckelführung wurde nach der Sichtprüfung nochmals korrigiert:

- keine Deckelfixierung und keine zusätzliche Stabilisierung in der Mitte;
- alle Führungs- und Rastelemente liegen in den äußeren Randzonen;
- Deckel und Gehäuse haben dieselbe Außenkontur und denselben Radius;
- Einsetzseite des Deckels ist offen, damit der 10-mm-Übergriff beim Absenken
  nicht mit dem Gehäuse kollidiert;
- in der definierten Bedienansicht gleitet der Deckel von links nach rechts in
  die bündige Endstellung.

## 2. Gehäuse

```text
Gehäuse ohne Flansche = 208,0 x 112,0 x 55,0
Wand/Boden = 3,2
Außenradius = R6,0
Schulterbeginn = Z45,0
Schulterhöhe = 10,0
Schulterrücksprung Front/Heck/Rechts = 2,3
Schulterradius = R3,7
```

Die Einsetzseite links bleibt im oberen Bereich außen bündig. Es gibt keine
Deckelsäulen oder freistehenden Verschlusspfosten im Innenraum. Die vier
Waveshare-Abstandshalter bleiben ausschließlich als Platinenbefestigung.

## 3. Bündiger Überwurf-Schiebedeckel

```text
Deckel außen = 208,0 x 112,0
Topplatte = 3,0
Übergriff Front/Heck/Rechts = 10,0
Deckelradius = R6,0
Schürzenwand = 2,0
nominelles Spiel zur Schulter = 0,30 je Seite
kurzer Schiebeweg = 8,0
```

Die linke Einsetzseite der Schürze ist offen. Dadurch kann der Deckel in der
Serviceposition abgesenkt werden. Danach läuft er auf drei wandintegrierten
Führungen in die Endstellung:

```text
vorn: X18
hinten: X18 und X190
Endrastung vorn rechts: X184
```

Damit liegen alle Deckelbefestigungen höchstens 25 mm von einer Stirnseite
entfernt. Die komplette mittlere Gehäusezone bleibt frei.

## 4. Druckgerechte Konstruktion

- P01 mit dem Boden auf dem Druckbett.
- P02 mit der sichtbaren ebenen Oberseite auf dem Druckbett.
- Führungsnasen besitzen 45°-Unterseiten.
- Einführungen sind am Schürzenrand offen.
- Keine Slicer-Stützen vorgesehen.
- Nur drei kurze, kontrollierte Brücken in den seitlichen Führungsbahnen.
- Außenkontur im geschlossenen Zustand ohne 0,5-mm-Überstand: Deckel und
  Gehäuse verschmelzen optisch zu einer gemeinsamen Kontur.

## 5. Beibehaltene Punkte

```text
ZERO = Y36,0 / Z26,0 / D3,0
SPAN = Y52,0 / Z26,0 / D3,0
Halter = Y18,0/94,0; Z20,0/36,0
Platine = 80,0 x 20,0 x 1,5
Sensor-/Prüfgruppe X unverändert; Y-Mitte = 56,0
```

## 6. Physische Prüfung

- Absenken in der offenen Serviceposition ohne Kollision;
- gleichzeitiger Eingriff der drei Randführungen;
- Deckelmitte vollständig frei und ohne zusätzliche Stützen;
- leichtes Gleiten, bündiger Außenübergang und sichere Endrastung;
- Druck ohne Support, Brückenqualität und Verzug;
- Kabelreserve, O-Ring-Sitz und Gasdichtheit der Prüfstation.
'''
    readme = '''# AirMonitor Compact Revision V0.8

Aktueller V0.8-Stand:

- außen bündiger, abgerundeter Überwurf-Schiebedeckel
- Deckel 10 mm nach unten übergreifend
- Einsetzseite offen, Endstellung optisch bündig
- Führungen ausschließlich an den äußeren Rändern
- keine Deckelfixierung oder Stabilisierung in der Gehäusemitte
- drei 45°-Führungen und eine Endrastung vorn rechts
- supportfreie Zielausrichtung für P01 und P02
- bestätigte Microtaster-Position und bestehende Prüfstation beibehalten

## Bedienung

Deckel in der Serviceposition absenken und in der definierten Bedienansicht
von links nach rechts bis zur Rastung einschieben. Zum Öffnen die Rastzunge
lösen, 8 mm zurückschieben und den Deckel abheben.

## Dateien

- Baugruppe: `01_CAD_Global/AirMonitor_Compact_Assembly_V0.8.step`
- Referenz: `01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.8.step`
- Druckteile: `02_CAD_Print/`
- Massskizzen: `AirMonitor_V08_Massskizzen_1zu1.pdf`
- Spezifikation: `CAD_COMPACT_SPEC_V0.8.md`
'''
    prompt = '''# Claude-/Daniel-Prüfprompt - AirMonitor Compact V0.8

Die Konstruktion wurde bereits erstellt. Bitte nur prüfen und Abweichungen
dokumentieren; keine selbstständige Neukonstruktion ohne Rückmeldung.

## Verbindliche Punkte

1. Deckel und unteres Gehäuse außen 208 x 112, beide R6 und bündig.
2. Deckelübergriff 10 mm; Einsetzseite links offen.
3. Keine Deckelführung, Rastung oder Stabilisierung in der mittleren Zone.
4. Randführungen: vorn X18; hinten X18 und X190.
5. Endrastung vorn rechts bei X184.
6. Führungsnasen mit 45°-Unterseite; Druck ohne Support vorgesehen.
7. In der Bedienansicht gleitet der Deckel von links nach rechts in die
   bündige Endstellung.
8. Microtaster, Waveshare, Sensorpod, Prüfstation und O-Ringe unverändert.

## Prüfen

- reale Einsetz- und Schieberichtung;
- Kollisionsfreiheit in offener und geschlossener Stellung;
- freie Gehäusemitte;
- Rastkraft, Spiel, Klappern und 20 Öffnungszyklen;
- Brücken im PrusaSlicer ohne Support;
- optisch bündige Außenkontur und gleichmäßige Fuge;
- Kabelreserve sowie Prüfstation/O-Ringe.

Ergebnis: `freigegeben`, `freigegeben mit Änderung` oder `nicht freigegeben`.
'''
    start = '''START HIER - AirMonitor Compact V0.8

1. Öffnen:
   01_CAD_Global/AirMonitor_Compact_Reference_With_Dummies_V0.8.step

2. Prüfen:
   - Deckel/Gehäuse außen bündig 208 x 112 / R6
   - Randführungen X18 / X190
   - Endrastung X184
   - Mitte ohne Deckelfixierungen
   - Einsetzseite offen
   - supportfreie Drucklage

3. Massskizzen:
   AirMonitor_V08_Massskizzen_1zu1.pdf

4. Spezifikation:
   CAD_COMPACT_SPEC_V0.8.md
'''
    (R / "CAD_COMPACT_SPEC_V0.8.md").write_text(spec, encoding="utf-8")
    (R / "README.md").write_text(readme, encoding="utf-8")
    (R / "PROMPT_CLAUDE_DANIEL_COMPACT_REVIEW_V0.8.md").write_text(prompt, encoding="utf-8")
    (R / "START_HIER_DANIEL_CLAUDE.txt").write_text(start, encoding="utf-8")


def main() -> None:
    patch_params()
    patch_build()
    write_checks()
    patch_sketches()
    write_docs()
    print("Applied V0.8 edge-only seamless-lid correction")


if __name__ == "__main__":
    main()
