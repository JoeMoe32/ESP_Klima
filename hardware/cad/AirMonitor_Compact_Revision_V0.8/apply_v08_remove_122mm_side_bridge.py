from __future__ import annotations

from pathlib import Path
import re

R = Path(__file__).resolve().parent


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one literal match, got {count}")
    return text.replace(old, new, 1)


def sub_once(text: str, pattern: str, repl: str, label: str) -> str:
    new, count = re.subn(pattern, lambda _m: repl, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one regex match, got {count}")
    return new


# ---------------------------------------------------------------------------
# Parameters: the 122 mm longitudinal opening must reach the upper body edge.
# This removes the unprintable 122 mm horizontal bridge above the opening.
# ---------------------------------------------------------------------------
p = R / "compact_params.py"
s = p.read_text(encoding="utf-8")
s = s.replace(
    "- P01 prints on its floor and P02 on its visible top without slicer supports.\n",
    "- both 122 mm longitudinal openings run from Z=12 to the upper edge Z=55;\n"
    "  there is no horizontal wall bridge above either opening;\n"
    "- P01 prints on its floor and P02 on its visible top without slicer supports.\n",
)
s = replace_once(
    s,
    "OPEN_Z, OPEN_TOP_Z = 12.0, SHOULDER_Z0\n",
    "OPEN_Z, OPEN_TOP_Z = 12.0, H\nNO_SIDE_OPENING_BRIDGE = True\n",
    "compact opening height",
)
p.write_text(s, encoding="utf-8")


# ---------------------------------------------------------------------------
# Numeric checks: explicitly require an open-top 122 x 43 mm side opening.
# ---------------------------------------------------------------------------
p = R / "check_clearances.py"
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    "    check('opening ends at shoulder', close(C.OPEN_TOP_Z,C.SHOULDER_Z0))\n",
    "    check('side opening reaches top edge', close(C.OPEN_TOP_Z,C.H))\n"
    "    check('side opening has no upper bridge', C.NO_SIDE_OPENING_BRIDGE)\n"
    "    check('side opening is 122 x 43',\n"
    "          close(C.OPEN_X1-C.OPEN_X0,122.0) and close(C.OPEN_TOP_Z-C.OPEN_Z,43.0))\n",
    "clearance opening checks",
)
p.write_text(s, encoding="utf-8")


# ---------------------------------------------------------------------------
# CAD build: cut through the upper shoulder, prove zero bridge volume, export a
# cache-safe base filename, update coordinate data and the side-view SVG.
# ---------------------------------------------------------------------------
p = R / "build_v08.py"
s = p.read_text(encoding="utf-8")

opening_cut = '''for y in (-0.5, W-wall-0.5):
    b = b.cut(box(C.OPEN_X0, y, C.OPEN_Z,
                  C.OPEN_X1-C.OPEN_X0, wall+1.0,
                  C.OPEN_TOP_Z-C.OPEN_Z+0.2))
'''
opening_cut_new = opening_cut + '''
# Definitive printability correction: no 122 mm horizontal bridge may remain
# above either longitudinal opening. Probe the complete former bridge zone
# between shoulder start Z=45 and enclosure top Z=55 on both long walls.
side_bridge_volumes = []
for wall_name, probe_y in (("front", -0.20), ("rear", W-wall-0.20)):
    probe = b.intersect(box(
        C.OPEN_X0 + 0.20,
        probe_y,
        C.SHOULDER_Z0 + 0.05,
        C.OPEN_X1 - C.OPEN_X0 - 0.40,
        wall + 0.40,
        C.H - C.SHOULDER_Z0 - 0.10,
    ))
    volume = sum(v.Volume() for v in probe.vals()) if probe.vals() else 0.0
    side_bridge_volumes.append((wall_name, volume))
    if volume > 0.01:
        raise SystemExit(
            f"Abbruch: oberer 122-mm-Quertraeger an {wall_name} verbleibt "
            f"({volume:.3f} mm3)."
        )
'''
s = replace_once(s, opening_cut, opening_cut_new, "CAD opening cut")

export_anchor = '''    if n == 'P02_Compact_Lid_Global':
        step(q, P / 'P02_Compact_Lid_Print_45DEG_GUIDES_V0.8.step')
        stl(q, P / 'P02_Compact_Lid_Print_45DEG_GUIDES_V0.8.stl')
'''
export_new = '''    if n == 'P01_Compact_Base_Global':
        step(q, P / 'P01_Compact_Base_Print_OPEN_TOP_V0.8.step')
        stl(q, P / 'P01_Compact_Base_Print_OPEN_TOP_V0.8.stl')
    if n == 'P02_Compact_Lid_Global':
        step(q, P / 'P02_Compact_Lid_Print_45DEG_GUIDES_V0.8.step')
        stl(q, P / 'P02_Compact_Lid_Print_45DEG_GUIDES_V0.8.stl')
'''
s = replace_once(s, export_anchor, export_new, "cache-safe base export")

verify_anchor = '''    f.write('Target printing: P01 on floor, P02 visible top on bed, no slicer support\\n')

# Dimensions and purchased component data.
'''
verify_new = '''    f.write('Target printing: P01 on floor, P02 visible top on bed, no slicer support\\n')

with (R / 'SIDE_OPENING_VERIFICATION.txt').open('w', encoding='utf-8') as f:
    f.write('AirMonitor Compact V0.8 - longitudinal side-opening verification\\n')
    f.write(f'Opening X: {C.OPEN_X0:.1f}..{C.OPEN_X1:.1f} mm = {C.OPEN_X1-C.OPEN_X0:.1f} mm\\n')
    f.write(f'Opening Z: {C.OPEN_Z:.1f}..{C.OPEN_TOP_Z:.1f} mm = {C.OPEN_TOP_Z-C.OPEN_Z:.1f} mm\\n')
    f.write('Upper horizontal bridge: removed\\n')
    for wall_name, volume in side_bridge_volumes:
        f.write(f'Bridge volume {wall_name}: {volume:.3f} mm3\\n')
    f.write('Target printing: opening is open to the upper edge; no 122 mm bridge support required\\n')

# Dimensions and purchased component data.
'''
s = replace_once(s, verify_anchor, verify_new, "side-opening verification note")

coord_anchor = '''    w.writerow(['Hidden snap', 'front/right X190; 0.20 mm nominal flex; blind detent', 'CAD'])
'''
coord_new = coord_anchor + '''    w.writerow(['Long-wall openings', 'X 36.6..158.6 / Z 12.0..55.0 = 122 x 43; open to top edge; no upper bridge', 'CAD / support-free correction'])
'''
s = replace_once(s, coord_anchor, coord_new, "coordinate opening row")

side_svg_pattern = r"side_svg = f'''<svg.*?\(D / 'Drawing_V08_Overlap_Lid_Side\.svg'\)\.write_text\(side_svg, encoding='utf-8'\)"
side_svg_repl = '''side_svg = f\'\'\'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="620" viewBox="-5 -5 218 70">
{svg_style}
<text class="t" x="0" y="-1">AirMonitor V0.8 - Laengswand ohne 122-mm-Quertraeger [mm]</text>
<path class="wall" d="M0 55 H36.6 V12 H158.6 V55 H208 V0 H0 Z"/>
<path d="M-0.5 58 H208.5 V45 H206 V55 H158.6 V45 H36.6 V55 H2 V45 H-0.5 Z" fill="#F1E8F7" stroke="#7A3FA0" stroke-width="0.5"/>
<path d="M36.6 12 H158.6" fill="none" stroke="#172b3a" stroke-width="0.4"/>
<text class="s" x="162" y="50">P02: 10 mm Uebergriff</text>
<text class="s" x="69" y="31">P01-Oeffnung 122 x 43</text>
<text class="s" x="58" y="26">Z12 bis Oberkante Z55 - oben vollstaendig offen</text>
<text class="s" x="59" y="20">kein horizontaler Quertraeger / keine Stuetzstruktur</text>
<text class="s" x="70" y="62">Topplatte 3 mm; Deckel ist separates Bauteil</text>
</svg>\'\'\'
(D / 'Drawing_V08_Overlap_Lid_Side.svg').write_text(side_svg, encoding='utf-8')'''
s = sub_once(s, side_svg_pattern, side_svg_repl, "side SVG")
p.write_text(s, encoding="utf-8")


# ---------------------------------------------------------------------------
# Mass sketches: page 2 must show a true U-shaped/open-top side wall, not a
# rectangular window with a 122 mm top strip. Also record the correction in the
# final checklist.
# ---------------------------------------------------------------------------
p = R / "generate_mass_sketches_v08.py"
s = p.read_text(encoding="utf-8")
page2_pattern = r"def page2_walls\(c\):.*?(?=\ndef page3_endwalls)"
page2_repl = '''def page2_walls(c):
    header(c, "P01/P02 - Laengswand ohne oberen Quertraeger",
           "P01-Oeffnung X36,6..158,6 / Z12..55: 122 x 43 und bis zur Oberkante offen")
    ox, oy = 38 * mm, 55 * mm

    # Draw the actual printable P01 wall contour as a U-shape. The 122 mm
    # centre opening is open all the way to Z=55; there is no line/material
    # above it. P02 is shown separately in violet.
    path = c.beginPath()
    path.moveTo(ox, oy)
    path.lineTo(ox + C.L * mm, oy)
    path.lineTo(ox + C.L * mm, oy + C.H * mm)
    path.lineTo(ox + C.OPEN_X1 * mm, oy + C.H * mm)
    path.lineTo(ox + C.OPEN_X1 * mm, oy + C.OPEN_Z * mm)
    path.lineTo(ox + C.OPEN_X0 * mm, oy + C.OPEN_Z * mm)
    path.lineTo(ox + C.OPEN_X0 * mm, oy + C.H * mm)
    path.lineTo(ox, oy + C.H * mm)
    path.close()
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.white)
    c.drawPath(path, stroke=1, fill=0)

    # Separate overlapping lid, not a bridge belonging to P01.
    c.saveState()
    c.setStrokeColor(C_HOOD)
    c.setLineWidth(0.8)
    c.line(ox - C.LID_OUTSET * mm,
           oy + (C.LID_Z + C.LID_T) * mm,
           ox + (C.L + C.LID_OUTSET) * mm,
           oy + (C.LID_Z + C.LID_T) * mm)
    c.line(ox - C.LID_OUTSET * mm,
           oy + (C.LID_Z - C.LID_OVERLAP) * mm,
           ox - C.LID_OUTSET * mm,
           oy + (C.LID_Z + C.LID_T) * mm)
    c.line(ox + (C.L + C.LID_OUTSET) * mm,
           oy + (C.LID_Z - C.LID_OVERLAP) * mm,
           ox + (C.L + C.LID_OUTSET) * mm,
           oy + (C.LID_Z + C.LID_T) * mm)
    c.restoreState()

    dim_h(c, ox, ox + C.L * mm, oy - 12 * mm, "208")
    # Put the width dimension below the opening so it cannot be confused with
    # a physical horizontal bridge.
    dim_h(c,
          ox + C.OPEN_X0 * mm,
          ox + C.OPEN_X1 * mm,
          oy + (C.OPEN_Z - 7) * mm,
          "122")
    dim_v(c, ox + C.L * mm + 8 * mm, oy, oy + C.H * mm, "55")
    dim_v(c,
          ox + C.OPEN_X1 * mm + 8 * mm,
          oy + C.OPEN_Z * mm,
          oy + C.OPEN_TOP_Z * mm,
          "43")
    dim_v(c,
          ox + C.L * mm + 18 * mm,
          oy + C.SHOULDER_Z0 * mm,
          oy + C.H * mm,
          "10")

    label(c, 12 * mm, 29 * mm,
          "P01-Oeffnung: X36,6..158,6 / Z12,0..55,0 = 122 x 43; bis Oberkante offen.", 7, True)
    label(c, 12 * mm, 24 * mm,
          "Der bisherige 122-mm-Quertraeger oberhalb der Oeffnung ist vollstaendig entfernt.", 7, True, C_ORING)
    label(c, 12 * mm, 19 * mm,
          "Violett: separater P02-Deckel mit 10-mm-Uebergriff; nicht Bestandteil der P01-Druckbruecke.", 7)
    footer(c, 2)
'''
s = sub_once(s, page2_pattern, page2_repl, "mass sketch page 2")

s = replace_once(
    s,
    '        "P01 208 x 112 x 55; Wand/Boden 3,2; Ecken R6,0.",\n',
    '        "P01 208 x 112 x 55; Wand/Boden 3,2; Ecken R6; beide Laengsoeffnungen 122 x 43 bis Z55 offen.",\n',
    "summary P01 item",
)
s = replace_once(
    s,
    '        "[ ] PrusaSlicer fordert an Fuehrung und Einfuehrtaschen keine Stuetzen.",\n',
    '        "[ ] P01 besitzt ueber den 122-mm-Oeffnungen keinen Quertraeger; PrusaSlicer fordert dort keine Stuetzen.",\n',
    "summary print check",
)
p.write_text(s, encoding="utf-8")


# Review rendering must include the corrected side-wall page 2.
p = R / "verify_v08_mass_sketches.py"
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    'REVIEW_PAGES = {\n    4: "MassSketch_V08_Page04_Lid.png",\n',
    'REVIEW_PAGES = {\n    2: "MassSketch_V08_Page02_OpenTopSide.png",\n    4: "MassSketch_V08_Page04_Lid.png",\n',
    "review page 2",
)
s = s.replace(
    '            "Dedicated guide print detail: page 10",\n',
    '            "Open-top longitudinal wall correction: page 2",\n'
    '            "Dedicated guide print detail: page 10",\n',
)
p.write_text(s, encoding="utf-8")


# ---------------------------------------------------------------------------
# Documentation.
# ---------------------------------------------------------------------------
p = R / "README.md"
s = p.read_text(encoding="utf-8")
needle = "- P01 und P02 fuer den Druck ohne Slicer-Stuetzen ausgelegt.\n"
replacement = (
    "- beide 122-mm-Laengsoeffnungen in P01 reichen von Z12 bis Z55; kein oberer Quertraeger;\n"
    "- P01 und P02 fuer den Druck ohne Slicer-Stuetzen ausgelegt.\n"
)
if "kein oberer Quertraeger" not in s:
    s = replace_once(s, needle, replacement, "README support-free bullet")
p.write_text(s, encoding="utf-8")

p = R / "CAD_COMPACT_SPEC_V0.8.md"
s = p.read_text(encoding="utf-8")
section = '''
## Laengswandoeffnungen - verbindliche Druckkorrektur

```text
X-Bereich je Oeffnung    36,6..158,6 mm = 122,0 mm
Z-Bereich je Oeffnung    12,0..55,0 mm = 43,0 mm
Oberer Quertraeger       entfaellt vollstaendig
```

Beide Laengswandoeffnungen von P01 laufen bis zur oberen Gehaeusekante. Damit
gibt es keine 122 mm lange waagerechte Bruecke mehr, die beim Druck Stuetzen
oder eine unzulaessige freie Ueberbrueckung erfordern wuerde. Der violette
10-mm-Uebergriff gehoert ausschliesslich zum separat gedruckten Deckel P02.
'''
if "Laengswandoeffnungen - verbindliche Druckkorrektur" not in s:
    s = s.rstrip() + "\n" + section
p.write_text(s, encoding="utf-8")

p = R / "SUPPORT_FREE_GUIDE_NOTE.md"
s = p.read_text(encoding="utf-8")
addition = '''
## P01-Laengswand

Der 122 mm breite Ausschnitt reicht von Z=12 bis zur oberen Gehaeusekante
Z=55. Oberhalb des Ausschnitts bleibt kein P01-Quertraeger stehen. Damit muss
P01 an dieser Stelle weder 122 mm frei ueberbruecken noch mit Stuetzmaterial
gedruckt werden. Der 10-mm-Uebergriff ist Teil des separat gedruckten Deckels.
'''
if "## P01-Laengswand" not in s:
    s = s.rstrip() + "\n" + addition
p.write_text(s, encoding="utf-8")

print("Applied V0.8 removal of the unprintable 122 mm side-wall bridge")
