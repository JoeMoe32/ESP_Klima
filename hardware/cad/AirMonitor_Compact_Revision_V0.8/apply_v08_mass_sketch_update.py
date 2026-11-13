from __future__ import annotations

from pathlib import Path
import re

R = Path(__file__).resolve().parent
P = R / "generate_mass_sketches_v08.py"
MARKER = "SKETCH_UPDATE_45DEG_DETAIL_V08"


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    new, count = re.subn(pattern, lambda _m: replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one replacement, got {count}")
    return new


text = P.read_text(encoding="utf-8")
if MARKER in text:
    print("V0.8 mass-sketch update already applied")
    raise SystemExit(0)

text = text.replace(
    "from pathlib import Path\n",
    f"from pathlib import Path\n\n{MARKER} = True\n",
    1,
)

page4 = r'''def page4_lid(c):
    header(c, "P02 - abgerundeter Ueberwurf-Schiebedeckel / Draufsicht",
           "Aussen geschlossen; vier verdeckte 45-Grad-Randfuehrungen; 8-mm-Schiebeweg")
    ox, oy = 37.5 * mm, 46.5 * mm
    w = C.LID_X1 - C.LID_X0
    h = C.LID_Y1 - C.LID_Y0

    # Visible outside contour, 1:1.
    c.setStrokeColor(colors.black)
    c.roundRect(ox, oy, w * mm, h * mm, C.LID_CORNER_R * mm)
    c.setStrokeColor(C_POD)
    for x, y, lx, ly in C.VENTS:
        c.rect(ox + x * mm, oy + y * mm, lx * mm, ly * mm)
    for x, y in C.POD_MOUNTS:
        c.circle(ox + x * mm, oy + y * mm, 1.5 * mm)
    c.setStrokeColor(C_HOOD)
    for x, y in C.HOOD_SCREWS:
        c.circle(ox + x * mm, oy + y * mm, 1.1 * mm)

    # Hidden underside tracks in dashed lines. Entry pocket is 8 mm before
    # the final guide position; the external skirt stays closed.
    c.saveState()
    c.setDash(2.2, 1.6)
    c.setLineWidth(0.55)
    c.setStrokeColor(C_ORING)
    for rear in (False, True):
        cy = h - C.GUIDE_GROOVE_INNER_Y_FRONT if rear else C.GUIDE_GROOVE_INNER_Y_FRONT
        for x in C.GUIDE_X_ALL:
            entry = x - C.SLIDE_TRAVEL
            track_end = x + C.GUIDE_TRACK_END_EXTRA
            c.rect(
                ox + (entry - C.GUIDE_ENTRY_W / 2) * mm,
                oy + (cy - 1.35) * mm,
                C.GUIDE_ENTRY_W * mm,
                2.70 * mm,
            )
            c.line(ox + entry * mm, oy + cy * mm,
                   ox + track_end * mm, oy + cy * mm)
            c.rect(
                ox + (x - C.GUIDE_LUG_W / 2) * mm,
                oy + (cy - 0.70) * mm,
                C.GUIDE_LUG_W * mm,
                1.40 * mm,
            )
    c.restoreState()

    # Operating-view direction. CAD closes by -X; in the selected operating
    # view this is perceived as left-to-right.
    c.saveState()
    c.setStrokeColor(C_CENTER)
    c.setFillColor(C_CENTER)
    c.setLineWidth(0.8)
    ay = oy + 56 * mm
    c.line(ox + 78 * mm, ay, ox + 130 * mm, ay)
    c.line(ox + 130 * mm, ay, ox + 125 * mm, ay + 3 * mm)
    c.line(ox + 130 * mm, ay, ox + 125 * mm, ay - 3 * mm)
    c.restoreState()
    label(c, ox + 82 * mm, ay + 5 * mm,
          "Bedienansicht: von links nach rechts einschieben", 7, True, C_CENTER)

    dim_h(c, ox, ox + w * mm, oy - 11 * mm, "208")
    dim_v(c, ox + w * mm + 9 * mm, oy, oy + h * mm, "112")
    dim_h(c, ox + 10 * mm, ox + 18 * mm, oy + h * mm + 8 * mm, "8,0")
    dim_h(c, ox + 182 * mm, ox + 190 * mm, oy + h * mm + 8 * mm, "8,0")

    label(c, 12 * mm, 31 * mm,
          "Verdeckt: Einfuehrtaschen X10/X182; Fuehrpositionen X18/X190; je vorne und hinten.", 7)
    label(c, 12 * mm, 26 * mm,
          "Fuehrungsbreite in X 6,00; Einfuehrtasche 7,60; Aussenhaut bleibt geschlossen.", 7)
    label(c, 12 * mm, 21 * mm,
          "Deckel +8,0 mm versetzt absenken, dann 8,0 mm bis zur verdeckten Endrastung einschieben.", 7)
    label(c, 12 * mm, 16 * mm,
          "Aussenkontur 208 x 112, R6; Top 3,0; Uebergriff 10,0; Schuerze 2,50.", 7, True)
    footer(c, 4, "Gestrichelt = verdeckte Unterseitengeometrie")


def page5_pod(c):'''

text = replace_once(
    text,
    r"def page4_lid\(c\):.*?\ndef page5_pod\(c\):",
    page4,
    "page 4 replacement",
)

new_tail = r'''def page9_assembly(c):
    header(c, "V0.8 - Aufsetzen, Absenken und Einschieben",
           "Funktion bleibt gefangen: Einfuehrtaschen nur zum Aufsetzen, danach 45-Grad-Randfuehrung")

    steps = [
        "1  Deckel in +8-mm-Serviceposition ueber P01 ausrichten.",
        "2  Vier Zungen gleichzeitig in die inneren Einfuehrtaschen absenken.",
        "3  Deckel 8,0 mm von links nach rechts in die Betriebsstellung schieben.",
        "4  Front/rechts rastet verdeckt ein; die Aussenkontur bleibt geschlossen.",
    ]
    for i, line in enumerate(steps):
        label(c, 18 * mm, (159 - 8 * i) * mm, line, 7.2, i == 2)

    # Three schematic sequence views (not to scale).
    base_y = 58 * mm
    view_w = 70 * mm
    view_h = 55 * mm
    xs = [18 * mm, 112 * mm, 206 * mm]
    titles = ["A  +8 mm ausrichten", "B  Absenken", "C  8 mm einschieben / Rastung"]
    for x, title in zip(xs, titles):
        label(c, x, base_y + view_h + 8 * mm, title, 7.5, True)
        c.setStrokeColor(C_POD)
        c.setFillColor(colors.HexColor("#D5F5E3"))
        c.roundRect(x, base_y, view_w, 22 * mm, 3 * mm, stroke=1, fill=1)
        c.setStrokeColor(C_HOOD)
        c.setFillColor(colors.HexColor("#F5CBA7"))
        c.roundRect(x, base_y + 28 * mm, view_w, 12 * mm, 3 * mm, stroke=1, fill=1)

    # A: horizontal offset.
    c.saveState()
    c.setStrokeColor(C_CENTER)
    c.setFillColor(C_CENTER)
    c.line(xs[0] + 22 * mm, base_y + 46 * mm, xs[0] + 30 * mm, base_y + 46 * mm)
    c.line(xs[0] + 30 * mm, base_y + 46 * mm, xs[0] + 27 * mm, base_y + 48 * mm)
    c.line(xs[0] + 30 * mm, base_y + 46 * mm, xs[0] + 27 * mm, base_y + 44 * mm)
    c.restoreState()
    label(c, xs[0] + 34 * mm, base_y + 44 * mm, "+8,0 mm", 7, True, C_CENTER)

    # B: lowering arrows.
    for ax in (xs[1] + 18 * mm, xs[1] + 52 * mm):
        c.saveState()
        c.setStrokeColor(C_CENTER)
        c.line(ax, base_y + 52 * mm, ax, base_y + 42 * mm)
        c.line(ax, base_y + 42 * mm, ax - 2 * mm, base_y + 45 * mm)
        c.line(ax, base_y + 42 * mm, ax + 2 * mm, base_y + 45 * mm)
        c.restoreState()

    # C: closing arrow and hidden detent.
    c.saveState()
    c.setStrokeColor(C_CENTER)
    c.setFillColor(C_CENTER)
    c.line(xs[2] + 12 * mm, base_y + 46 * mm, xs[2] + 48 * mm, base_y + 46 * mm)
    c.line(xs[2] + 48 * mm, base_y + 46 * mm, xs[2] + 44 * mm, base_y + 49 * mm)
    c.line(xs[2] + 48 * mm, base_y + 46 * mm, xs[2] + 44 * mm, base_y + 43 * mm)
    c.restoreState()
    c.setStrokeColor(C_ORING)
    c.circle(xs[2] + 58 * mm, base_y + 24 * mm, 2.2 * mm, stroke=1, fill=0)
    label(c, xs[2] + 43 * mm, base_y + 16 * mm, "verdeckt", 6.5, True, C_ORING)

    label(c, 18 * mm, 43 * mm,
          "Wichtig: Nach dem Einschieben liegen die Zungen in blinden Diagonalnuten und halten den Deckel vertikal.", 7, True)
    label(c, 18 * mm, 36 * mm,
          "Die Einfuehrtaschen sind nur zur Innenseite und zur unteren Schuerzenkante offen; aussen keine C-Fenster.", 7)
    label(c, 18 * mm, 29 * mm,
          "Zum Oeffnen gleichmaessig gegen die Einschubrichtung 8,0 mm zurueckschieben und danach abheben.", 7)
    label(c, 18 * mm, 22 * mm,
          "Darstellung schematisch; verbindliche Masse siehe Seite 10 und CAD-Dateien.", 7)
    footer(c, 9, "Montagefolge - nicht massstaeblich")


def page10_print_detail(c):
    header(c, "V0.8 - Druckdetail der 45-Grad-Randfuehrung",
           "Vergroesserter Y/Z-Schnitt; keine waagerechte C-Decke; Aussenhaut bleibt geschlossen")

    # Enlarged normal guide section.
    sx = 18 * mm
    sy = 54 * mm
    scale = 18 * mm

    def draw_section(x, title, snap=False):
        label(c, x, sy + 104 * mm, title, 8, True)

        # Lid skirt: 0..2.5 mm in Y, Z45..55 mm.
        c.setFillColor(colors.HexColor("#F5CBA7"))
        c.setStrokeColor(C_HOOD)
        c.rect(x, sy, C.LID_SKIRT_W * scale, 10.0 * scale, stroke=1, fill=1)

        # Blind diagonal groove (white cut-out).
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

        # P01 shoulder and support-free diagonal tongue.
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

        # 45-degree indication.
        c.saveState()
        c.setStrokeColor(C_CENTER)
        c.setFillColor(C_CENTER)
        c.line(x + 4.6 * scale, sy + 2.0 * scale,
               x + 4.6 * scale + 0.9 * scale, sy + 2.9 * scale)
        c.restoreState()
        label(c, x + 5.7 * scale, sy + 2.8 * scale, "45 Grad", 7, True, C_CENTER)

        dim_h(c, x, x + C.LID_SKIRT_W * scale, sy - 6 * mm, "2,50", 1.5)
        dim_h(c, x, x + C.GUIDE_OUTER_SKIN * scale,
              sy + 10.0 * scale + 6 * mm, "Aussenhaut 1,60", 1.5)
        dim_h(c, x + tip * scale, x + C.SHOULDER_INSET * scale,
              sy + 1.0 * scale, fmt(proj, 2), 1.2)
        dim_v(c, x + 7.2 * scale, sy + z0 * scale,
              sy + (z0 + proj) * scale, fmt(proj, 2), 1.2)

    draw_section(sx, "Normalfuehrung X18 / X190", snap=False)
    draw_section(151 * mm, "Endrastung vorne rechts X190", snap=True)

    label(c, 18 * mm, 42 * mm, "Verbindliche Zusatzmasse", 8, True)
    details = [
        f"Fuehrungszunge: Breite X {fmt(C.GUIDE_LUG_W, 2)}; Projektion/Anstieg normal {fmt(C.GUIDE_PROJ, 2)} / {fmt(C.GUIDE_RISE, 2)}.",
        f"Blinde Innennut: Z {fmt(C.GUIDE_GROOVE_Z0, 2)}..{fmt(C.GUIDE_GROOVE_Z1, 2)}; diagonaler Anstieg {fmt(C.GUIDE_GROOVE_RISE, 2)}.",
        f"Einfuehrtasche: Breite X {fmt(C.GUIDE_ENTRY_W, 2)}; Z {fmt(C.GUIDE_ENTRY_BOTTOM_Z, 2)}..{fmt(C.GUIDE_ENTRY_TOP_Z, 2)}.",
        f"Geschlossene Aussenhaut: normal {fmt(C.GUIDE_OUTER_SKIN, 2)}; an Einfuehrtasche mindestens {fmt(C.GUIDE_ENTRY_OUTER_SKIN, 2)}.",
        f"Verdeckte Rastung: nominelle lokale Auslenkung {fmt(C.SNAP_INTERFERENCE, 2)}; Endtasche tiefer, keine sichtbare Rastzunge.",
        f"Schiebeweg {fmt(C.SLIDE_TRAVEL, 2)}; Fuehrungen nur X18/X190 vorne und hinten; Gehaeusemitte frei.",
    ]
    for i, line in enumerate(details):
        label(c, 22 * mm, (34 - 5.3 * i) * mm, "- " + line, 6.6)

    label(c, 151 * mm, 42 * mm, "Drucklage", 8, True)
    label(c, 155 * mm, 34 * mm, "P01: Boden auf Druckbett", 7)
    label(c, 155 * mm, 28 * mm, "P02: sichtbare Oberseite auf Druckbett", 7)
    label(c, 155 * mm, 22 * mm, "45-Grad-Flaechen bauen sich schichtweise auf", 7)
    label(c, 155 * mm, 16 * mm, "Supportfrei vorgesehen - Probedruck bleibt erforderlich", 7, True, C_ORING)
    footer(c, 10, "Vergroessert - Schnitt nicht 1:1")


def page11_summary(c):
    header(c, "V0.8 - Freigabe- und Pruefliste",
           "8-mm-Schiebefunktion beibehalten; nur die Fuehrungsprofile druckgerecht geaendert")
    label(c, 18 * mm, 160 * mm, "Umgesetzt", 8, True)
    items = [
        "Microtaster, Waveshare, Sensorpod, Pruefstation und O-Ringe unveraendert.",
        "P01 208 x 112 x 55; Wand/Boden 3,2; Ecken R6,0.",
        "P02 aussen 208 x 112; 3,0-mm-Top; 10,0-mm-Uebergriff; Schuerze 2,5.",
        "Vier Fuehrungspunkte ausschliesslich bei X18 und X190; Mitte frei.",
        "Blinde Innennuten mit 45-Grad-Parallelogrammprofil; aussen keine Fenster.",
        "8-mm-Absenk-/Schiebeprinzip aus dem funktionierenden Vorentwurf bleibt bestehen.",
        "Verdeckte Endrastung front/rechts mit ca. 0,20 mm lokaler Auslenkung.",
        "P01 auf Boden und P02 mit sichtbarer Oberseite auf Bett, ohne Slicer-Stuetzen vorgesehen.",
    ]
    for i, line in enumerate(items):
        label(c, 22 * mm, (151 - 8 * i) * mm, "- " + line, 7)

    label(c, 18 * mm, 82 * mm, "Vor Freigabe praktisch pruefen", 8, True)
    checks = [
        "[ ] Alle vier Zungen lassen sich in +8-mm-Lage gleichzeitig absenken.",
        "[ ] Deckel schiebt leicht, bleibt aber vertikal sicher gefangen.",
        "[ ] Verdeckte Rastung ist loesbar und uebersteht mindestens 20 Zyklen.",
        "[ ] PrusaSlicer fordert an Fuehrung und Einfuehrtaschen keine Stuetzen.",
        "[ ] Aussenfuge ist gleichmaessig; keine sichtbaren C-Ausschnitte.",
        "[ ] Kabelreserve, O-Ringe, Leckrate und Nullpunkt sind dokumentiert.",
    ]
    for i, line in enumerate(checks):
        label(c, 22 * mm, (73 - 8 * i) * mm, line, 7)
    footer(c, 11, "CAD-Stand: V0.8 - verdeckte 45-Grad-Randfuehrung")


def main():
    c = canvas.Canvas(str(OUT), pagesize=PAGE)
    c.setTitle("AirMonitor HCHO V0.8 - Massskizzen 1:1")
    c.setSubject("Aktualisierte V0.8-Skizzen mit verdeckter 45-Grad-Randfuehrung")
    pages = [
        page1_base,
        page2_walls,
        page3_endwalls,
        page4_lid,
        page5_pod,
        page6_hood,
        page7_orings,
        page8_p05,
        page9_assembly,
        page10_print_detail,
        page11_summary,
    ]
    for fn in pages:
        fn(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
'''

text = replace_once(
    text,
    r"def page9_assembly\(c\):.*\Z",
    new_tail,
    "pages 9-11 and main replacement",
)

P.write_text(text, encoding="utf-8")
print("Applied V0.8 mass-sketch update with dedicated guide/print detail")
