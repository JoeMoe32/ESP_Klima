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
# Parameters: the opening must cut through BOTH the outer lower wall and the
# recessed upper shoulder wall. The previous check only covered the outer wall,
# which left a hidden 122 mm strip at the inner shoulder depth.
# ---------------------------------------------------------------------------
p = R / "compact_params.py"
s = p.read_text(encoding="utf-8")
if "SIDE_OPEN_FRONT_Y0" not in s:
    s = replace_once(
        s,
        "NO_SIDE_OPENING_BRIDGE = True\n",
        "NO_SIDE_OPENING_BRIDGE = True\n"
        "# Complete cut ranges through lower wall plus recessed shoulder wall.\n"
        "SIDE_OPEN_FRONT_Y0 = -0.50\n"
        "SIDE_OPEN_FRONT_Y1 = SHOULDER_INSET + WALL + 0.50\n"
        "SIDE_OPEN_REAR_Y0 = W - SHOULDER_INSET - WALL - 0.50\n"
        "SIDE_OPEN_REAR_Y1 = W + 0.50\n"
        "SIDE_OPEN_CUT_THROUGH_SHOULDER = True\n",
        "side-opening Y ranges",
    )
    s = s.replace(
        "  there is no horizontal wall bridge above either opening;\n",
        "  neither the outer wall nor the recessed inner shoulder leaves a horizontal bridge;\n",
    )
p.write_text(s, encoding="utf-8")


# ---------------------------------------------------------------------------
# Numeric checks: require the cut to reach beyond both shoulder-wall bounds.
# ---------------------------------------------------------------------------
p = R / "check_clearances.py"
s = p.read_text(encoding="utf-8")
if "full side cut reaches front shoulder inner edge" not in s:
    anchor = (
        "    check('side opening is 122 x 43',\n"
        "          close(C.OPEN_X1-C.OPEN_X0,122.0) and close(C.OPEN_TOP_Z-C.OPEN_Z,43.0))\n"
    )
    addition = anchor + (
        "    check('full shoulder-cut flag', C.SIDE_OPEN_CUT_THROUGH_SHOULDER)\n"
        "    check('full side cut reaches front shoulder inner edge',\n"
        "          C.SIDE_OPEN_FRONT_Y1 >= C.SHOULDER_INSET + C.WALL)\n"
        "    check('full side cut reaches rear shoulder inner edge',\n"
        "          C.SIDE_OPEN_REAR_Y0 <= C.W - C.SHOULDER_INSET - C.WALL)\n"
        "    check('front cut begins outside body', C.SIDE_OPEN_FRONT_Y0 < 0.0)\n"
        "    check('rear cut ends outside body', C.SIDE_OPEN_REAR_Y1 > C.W)\n"
    )
    s = replace_once(s, anchor, addition, "complete side-cut checks")
p.write_text(s, encoding="utf-8")


# ---------------------------------------------------------------------------
# CAD build: replace the incomplete wall-only cut and wall-only probe with a
# full-depth cut through the recessed shoulder. Export a cache-safe filename.
# ---------------------------------------------------------------------------
p = R / "build_v08.py"
s = p.read_text(encoding="utf-8")

new_opening_block = '''side_open_cut_ranges = [
    ("front", C.SIDE_OPEN_FRONT_Y0, C.SIDE_OPEN_FRONT_Y1),
    ("rear", C.SIDE_OPEN_REAR_Y0, C.SIDE_OPEN_REAR_Y1),
]
for wall_name, y0, y1 in side_open_cut_ranges:
    b = b.cut(box(
        C.OPEN_X0,
        y0,
        C.OPEN_Z,
        C.OPEN_X1 - C.OPEN_X0,
        y1 - y0,
        C.OPEN_TOP_Z - C.OPEN_Z + 0.20,
    ))

# Definitive printability correction: probe the complete combined wall depth,
# including the recessed shoulder ring. This catches the exact hidden strip
# that remained around Y=SHOULDER_INSET+WALL/2 in the previous STL.
side_bridge_volumes = []
for wall_name, y0, y1 in side_open_cut_ranges:
    probe_y0 = y0 + 0.10
    probe_y1 = y1 - 0.10
    probe = b.intersect(box(
        C.OPEN_X0 + 0.20,
        probe_y0,
        C.SHOULDER_Z0 + 0.05,
        C.OPEN_X1 - C.OPEN_X0 - 0.40,
        probe_y1 - probe_y0,
        C.H - C.SHOULDER_Z0 - 0.10,
    ))
    volume = sum(v.Volume() for v in probe.vals()) if probe.vals() else 0.0
    side_bridge_volumes.append((wall_name, y0, y1, volume))
    if volume > 0.01:
        raise SystemExit(
            f"Abbruch: innerer Schulter-Quertraeger an {wall_name} verbleibt "
            f"({volume:.3f} mm3, Y={y0:.2f}..{y1:.2f})."
        )

'''
pattern = (
    r"for y in \(-0\.5, W-wall-0\.5\):.*?"
    r"(?=\nfor x, y in C\.STANDOFFS:)"
)
s = sub_once(s, pattern, new_opening_block.rstrip(), "replace incomplete side-opening cut")

if "P01_Compact_Base_Print_FULL_OPEN_SIDE_V0.8" not in s:
    old = '''    if n == 'P01_Compact_Base_Global':
        step(q, P / 'P01_Compact_Base_Print_OPEN_TOP_V0.8.step')
        stl(q, P / 'P01_Compact_Base_Print_OPEN_TOP_V0.8.stl')
'''
    new = '''    if n == 'P01_Compact_Base_Global':
        step(q, P / 'P01_Compact_Base_Print_OPEN_TOP_V0.8.step')
        stl(q, P / 'P01_Compact_Base_Print_OPEN_TOP_V0.8.stl')
        step(q, P / 'P01_Compact_Base_Print_FULL_OPEN_SIDE_V0.8.step')
        stl(q, P / 'P01_Compact_Base_Print_FULL_OPEN_SIDE_V0.8.stl')
'''
    s = replace_once(s, old, new, "cache-safe full-open export")

verification_pattern = (
    r"with \(R / 'SIDE_OPENING_VERIFICATION\.txt'\)\.open\('w', encoding='utf-8'\) as f:.*?"
    r"(?=\n# Dimensions and purchased component data\.)"
)
verification_repl = '''with (R / 'SIDE_OPENING_VERIFICATION.txt').open('w', encoding='utf-8') as f:
    f.write('AirMonitor Compact V0.8 - longitudinal side-opening verification\\n')
    f.write(f'Opening X: {C.OPEN_X0:.1f}..{C.OPEN_X1:.1f} mm = {C.OPEN_X1-C.OPEN_X0:.1f} mm\\n')
    f.write(f'Opening Z: {C.OPEN_Z:.1f}..{C.OPEN_TOP_Z:.1f} mm = {C.OPEN_TOP_Z-C.OPEN_Z:.1f} mm\\n')
    f.write('Outer wall bridge: removed\\n')
    f.write('Recessed inner shoulder bridge: removed\\n')
    for wall_name, y0, y1, volume in side_bridge_volumes:
        f.write(f'Complete cut {wall_name} Y: {y0:.2f}..{y1:.2f} mm\\n')
        f.write(f'Full-depth bridge volume {wall_name}: {volume:.3f} mm3\\n')
    f.write('Target printing: both 122 mm openings are fully open through the entire wall/shoulder depth.\\n')
'''
s = sub_once(s, verification_pattern, verification_repl.rstrip(), "verification note")

s = s.replace(
    "'X 36.6..158.6 / Z 12.0..55.0 = 122 x 43; open to top edge; no upper bridge'",
    "'X 36.6..158.6 / Z 12.0..55.0 = 122 x 43; cut through outer wall and recessed shoulder; no bridge at any Y depth'",
)
p.write_text(s, encoding="utf-8")


# ---------------------------------------------------------------------------
# Mass sketch: clarify that the inner shoulder strip is also removed.
# ---------------------------------------------------------------------------
p = R / "generate_mass_sketches_v08.py"
s = p.read_text(encoding="utf-8")
s = s.replace(
    "Der bisherige 122-mm-Quertraeger oberhalb der Oeffnung ist vollstaendig entfernt.",
    "Aussenwand UND innere Schulterwand sind ueber 122 mm vollstaendig bis oben offen.",
)
s = s.replace(
    "P01-Oeffnung X36,6..158,6 / Z12..55: 122 x 43 und bis zur Oberkante offen",
    "P01-Oeffnung 122 x 43: durch Aussenwand und Schulterring bis Z55 offen",
)
p.write_text(s, encoding="utf-8")


# ---------------------------------------------------------------------------
# Documentation.
# ---------------------------------------------------------------------------
p = R / "README.md"
s = p.read_text(encoding="utf-8")
notice = '''
## Vollstaendig offene Laengsseiten

Die 122-mm-Oeffnungen schneiden jetzt nicht nur die aeussere 3,2-mm-Wand,
sondern auch die nach innen versetzte Schulterwand. Der zuvor im GitHub-STL
noch sichtbare innere Streifen bei etwa Y=14..15 mm der Druckdatei ist entfernt.
Zur cache-sicheren Kontrolle liegt zusaetzlich
`P01_Compact_Base_Print_FULL_OPEN_SIDE_V0.8.stl` vor.
'''
if "## Vollstaendig offene Laengsseiten" not in s:
    s = s.rstrip() + "\n" + notice
p.write_text(s, encoding="utf-8")

p = R / "CAD_COMPACT_SPEC_V0.8.md"
s = p.read_text(encoding="utf-8")
notice = '''
## Korrektur des inneren Schulter-Quertraegers

Die Laengsoeffnung X=36,6..158,6 und Z=12,0..55,0 wird ueber die komplette
kombinierte Wandtiefe geschnitten. Vorne reicht der CAD-Schnitt von
Y=-0,50 bis Y=6,50 mm, hinten von Y=105,50 bis Y=112,50 mm. Damit sind sowohl
die aeussere Gehaeusewand als auch die versetzte Schulterwand entfernt; es
bleibt kein 122-mm-Streifen fuer einen freien Brueckendruck stehen.
'''
if "## Korrektur des inneren Schulter-Quertraegers" not in s:
    s = s.rstrip() + "\n" + notice
p.write_text(s, encoding="utf-8")

print("Applied definitive V0.8 removal of outer and inner shoulder bridges")
