from __future__ import annotations

from pathlib import Path
import re

R = Path(__file__).resolve().parent
P = R / "generate_mass_sketches_v08.py"
MARKER = "PAGE10_LAYOUT_FIX_V2"

text = P.read_text(encoding="utf-8")
if MARKER in text:
    print("V0.8 page-10 layout fix already applied")
    raise SystemExit(0)

text = text.replace(
    "SKETCH_UPDATE_45DEG_DETAIL_V08 = True\n",
    "SKETCH_UPDATE_45DEG_DETAIL_V08 = True\nPAGE10_LAYOUT_FIX_V2 = True\n",
    1,
)

page10 = r'''def page10_print_detail(c):
    header(c, "V0.8 - Druckdetail der 45-Grad-Randfuehrung",
           "Vergroesserter Y/Z-Schnitt; keine waagerechte C-Decke; Aussenhaut bleibt geschlossen")

    # Enlarged sections kept fully below the header and above the notes.
    sy = 48 * mm
    scale = 9.2 * mm

    def draw_section(x, title, snap=False):
        label(c, x, sy + 98 * mm, title, 8, True)

        # P02 skirt: physical Y=0..2.50 and Z=45..55 mm.
        c.setFillColor(colors.HexColor("#F5CBA7"))
        c.setStrokeColor(C_HOOD)
        c.rect(x, sy, C.LID_SKIRT_W * scale, 10.0 * scale, stroke=1, fill=1)

        # Blind diagonal groove.
        inner = C.GUIDE_GROOVE_INNER_Y_FRONT
        outer = C.GUIDE_GROOVE_OUTER_Y_FRONT
        if snap:
            outer -= C.SNAP_DETENT_EXTRA_DEPTH
        rise = abs(outer - inner)
        gz0 = C.GUIDE_GROOVE_Z0 - 45.0
        gz1 = C.GUIDE_GROOVE_Z1 - 45.0
        p = c.beginPath()
        p.moveTo(x + inner * scale, sy + gz0 * scale)
        p.lineTo(x + outer * scale, sy + (gz0 + rise) * scale)
        p.lineTo(x + outer * scale, sy + (gz1 + rise) * scale)
        p.lineTo(x + inner * scale, sy + gz1 * scale)
        p.close()
        c.setFillColor(colors.white)
        c.drawPath(p, stroke=1, fill=1)

        # P01 shoulder and diagonal guide tongue.
        wall_x = x + C.SHOULDER_INSET * scale
        c.setFillColor(colors.HexColor("#A9DFBF"))
        c.setStrokeColor(C_POD)
        c.rect(wall_x, sy, 3.8 * scale, 10.0 * scale, stroke=1, fill=1)
        proj = C.GUIDE_PROJ + (C.SNAP_EXTRA_PROJ if snap else 0.0)
        z0 = C.GUIDE_ROOT_Z0 - 45.0
        z1 = C.GUIDE_ROOT_Z1 - 45.0
        tip = C.SHOULDER_INSET - proj
        p = c.beginPath()
        p.moveTo(x + C.SHOULDER_INSET * scale, sy + z0 * scale)
        p.lineTo(x + tip * scale, sy + (z0 + proj) * scale)
        p.lineTo(x + tip * scale, sy + (z1 + proj) * scale)
        p.lineTo(x + C.SHOULDER_INSET * scale, sy + z1 * scale)
        p.close()
        c.drawPath(p, stroke=1, fill=1)

        # Angle note.
        c.saveState()
        c.setStrokeColor(C_CENTER)
        c.setFillColor(C_CENTER)
        c.line(x + 4.3 * scale, sy + 2.0 * scale,
               x + 5.2 * scale, sy + 2.9 * scale)
        c.restoreState()
        label(c, x + 5.4 * scale, sy + 2.7 * scale, "45 Grad", 7, True, C_CENTER)

        # Main dimensions.
        dim_h(c, x, x + C.LID_SKIRT_W * scale, sy - 5 * mm, "2,50", 1.2)
        dim_h(c, x, x + C.GUIDE_OUTER_SKIN * scale,
              sy + 10.0 * scale + 5 * mm, "Haut 1,60", 1.2)
        dim_h(c, x + tip * scale, x + C.SHOULDER_INSET * scale,
              sy + 1.0 * scale, fmt(proj, 2), 1.0)
        dim_v(c, x + 7.0 * scale, sy + z0 * scale,
              sy + (z0 + proj) * scale, fmt(proj, 2), 1.0)

    draw_section(24 * mm, "Normalfuehrung X18 / X190", snap=False)
    draw_section(151 * mm, "Endrastung vorne rechts X190", snap=True)

    # Compact notes in two columns; kept clear of footer/control scale.
    label(c, 18 * mm, 39 * mm, "Verbindliche Masse", 8, True)
    left_notes = [
        f"Zunge X-Breite {fmt(C.GUIDE_LUG_W, 2)}; normal proj./Anstieg {fmt(C.GUIDE_PROJ, 2)} / {fmt(C.GUIDE_RISE, 2)}.",
        f"Nut Z {fmt(C.GUIDE_GROOVE_Z0, 2)}..{fmt(C.GUIDE_GROOVE_Z1, 2)}; diagonal {fmt(C.GUIDE_GROOVE_RISE, 2)}.",
        f"Einfuehrtasche X-Breite {fmt(C.GUIDE_ENTRY_W, 2)}; Z {fmt(C.GUIDE_ENTRY_BOTTOM_Z, 2)}..{fmt(C.GUIDE_ENTRY_TOP_Z, 2)}.",
    ]
    for i, line in enumerate(left_notes):
        label(c, 22 * mm, (33 - 6 * i) * mm, "- " + line, 6.5)

    label(c, 151 * mm, 39 * mm, "Druck und Rastung", 8, True)
    right_notes = [
        f"Aussenhaut normal {fmt(C.GUIDE_OUTER_SKIN, 2)}, Einfuehrtasche min. {fmt(C.GUIDE_ENTRY_OUTER_SKIN, 2)}.",
        f"Rastung: lokale Auslenkung {fmt(C.SNAP_INTERFERENCE, 2)}; Schiebeweg {fmt(C.SLIDE_TRAVEL, 2)}.",
        "P01 Boden unten; P02 sichtbare Oberseite unten; keine Slicer-Stuetzen vorgesehen.",
    ]
    for i, line in enumerate(right_notes):
        label(c, 155 * mm, (33 - 6 * i) * mm, "- " + line, 6.5)

    label(c, 155 * mm, 15 * mm,
          "Supportfrei vorgesehen - Probedruck bleibt erforderlich", 7, True, C_ORING)
    footer(c, 10, "Vergroessert - Schnitt nicht 1:1")


def page11_summary(c):'''

new, count = re.subn(
    r"def page10_print_detail\(c\):.*?\ndef page11_summary\(c\):",
    lambda _m: page10,
    text,
    count=1,
    flags=re.S,
)
if count != 1:
    raise RuntimeError(f"page10 replacement expected once, got {count}")

P.write_text(new, encoding="utf-8")
print("Applied V0.8 page-10 layout fix")
