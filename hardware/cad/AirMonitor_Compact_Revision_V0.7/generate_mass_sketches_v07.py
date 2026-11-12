"""Generate revised 1:1 engineering sketches for AirMonitor Compact V0.7.

This drawing set reflects the corrected V0.7 state:
- sensor/calibration unit retains the proven V0.6 X position;
- complete unit is centred on Y=56.0 mm;
- P03 is 8.0 mm wider on the cable side;
- purchased EPDM 70 Shore A O-rings replace printed TPU seals;
- grooves are located in P03 and P07, not in the 3.0 mm lid.
"""
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors

import compact_params as C

OUT = Path(__file__).resolve().parent / "AirMonitor_V07_Massskizzen_1zu1.pdf"
PAGE = landscape(A4)
PW, PH = PAGE

# Drawing colours
C_POD = colors.HexColor("#1F5AA6")
C_HOOD = colors.HexColor("#7A3FA0")
C_ORING = colors.HexColor("#D22F27")
C_CENTER = colors.HexColor("#278C73")
C_DIM = colors.HexColor("#333333")
C_LIGHT = colors.HexColor("#DCE6F1")


def fmt(value, digits=1):
    return f"{value:.{digits}f}".replace(".", ",")


def header(c, title, subtitle=""):
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.35)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(12 * mm, PH - 12 * mm, "LAMINAR | AirMonitor HCHO | V0.7")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(12 * mm, PH - 20 * mm, title)
    if subtitle:
        c.setFont("Helvetica", 7.5)
        c.drawString(12 * mm, PH - 26 * mm, subtitle)
    c.line(12 * mm, PH - 29 * mm, PW - 12 * mm, PH - 29 * mm)


def footer(c, page_no, note=""):
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    c.setFont("Helvetica", 6.5)
    c.drawString(12 * mm, 8 * mm, "A4 quer | Massstab 1:1 | Masse in mm | Druck: 100 % / Tatsaechliche Groesse")
    if note:
        c.drawCentredString(PW / 2, 8 * mm, note)
    c.drawRightString(PW - 12 * mm, 8 * mm, str(page_no))
    x0 = PW - 72 * mm
    y0 = 16 * mm
    c.line(x0, y0, x0 + 50 * mm, y0)
    c.line(x0, y0 - 2 * mm, x0, y0 + 2 * mm)
    c.line(x0 + 50 * mm, y0 - 2 * mm, x0 + 50 * mm, y0 + 2 * mm)
    c.setFont("Helvetica", 6)
    c.drawCentredString(x0 + 25 * mm, y0 + 2.5 * mm, "Kontrolle: 50 mm")


def dim_h(c, x0, x1, y, text, ext=3.0):
    c.saveState()
    c.setStrokeColor(C_DIM)
    c.setFillColor(C_DIM)
    c.setLineWidth(0.25)
    c.line(x0, y, x1, y)
    c.line(x0, y - ext * mm, x0, y + ext * mm)
    c.line(x1, y - ext * mm, x1, y + ext * mm)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString((x0 + x1) / 2, y + 2 * mm, text)
    c.restoreState()


def dim_v(c, x, y0, y1, text, ext=3.0):
    c.saveState()
    c.setStrokeColor(C_DIM)
    c.setFillColor(C_DIM)
    c.setLineWidth(0.25)
    c.line(x, y0, x, y1)
    c.line(x - ext * mm, y0, x + ext * mm, y0)
    c.line(x - ext * mm, y1, x + ext * mm, y1)
    c.translate(x + 2.5 * mm, (y0 + y1) / 2)
    c.rotate(90)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(0, 0, text)
    c.restoreState()


def label(c, x, y, text, size=6.5, bold=False, color=colors.black):
    c.saveState()
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawString(x, y, text)
    c.restoreState()


def rounded_path(c, origin_x, origin_y, ring, base_x, base_y, color=C_ORING, dash=None, width=0.55):
    x = origin_x + (ring["cx"] - base_x - ring["cw"] / 2) * mm
    y = origin_y + (ring["cy"] - base_y - ring["ch"] / 2) * mm
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(width)
    if dash:
        c.setDash(*dash)
    c.roundRect(x, y, ring["cw"] * mm, ring["ch"] * mm, ring["r"] * mm, stroke=1, fill=0)
    c.restoreState()
    return x, y


def draw_groove_section(c, x, y, title, substrate_label):
    """Draw an enlarged explanatory groove/O-ring cross-section (not 1:1)."""
    scale = 18.0
    base_w = 14.0 * scale
    base_h = 3.0 * scale
    groove_w = C.ORING_GROOVE_W * scale
    groove_d = C.ORING_GROOVE_D * scale
    ring_d = C.ORING_CORD * scale

    c.saveState()
    c.setFillColor(colors.HexColor("#EEF2F5"))
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.45)
    c.rect(x, y, base_w, base_h, stroke=1, fill=1)
    gx = x + (base_w - groove_w) / 2
    c.setFillColor(colors.white)
    c.rect(gx, y + base_h - groove_d, groove_w, groove_d + 0.2, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#F6B7B3"))
    c.setStrokeColor(C_ORING)
    c.circle(x + base_w / 2, y + base_h - groove_d + ring_d / 2, ring_d / 2, stroke=1, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x, y + base_h + 8 * mm, title)
    c.setFont("Helvetica", 6.5)
    c.drawString(x, y - 5 * mm, substrate_label)
    c.drawString(x, y - 10 * mm, "O-Ring D1,50 | Nut 1,80 x 1,10 | Ueberstand 0,40")
    c.drawString(x, y - 15 * mm, "Axiale Verpressung: 0,40 / 1,50 = 26,7 %")
    dim_h(c, gx, gx + groove_w, y + base_h + 2 * mm, "1,80", 1.5)
    dim_v(c, gx - 4 * mm, y + base_h - groove_d, y + base_h, "1,10", 1.5)
    dim_v(c, x + base_w + 4 * mm, y + base_h - groove_d, y + base_h - groove_d + ring_d, "1,50", 1.5)
    c.restoreState()


def page1_base(c):
    header(c, "P01 - Gehaeuseboden / Draufsicht innen",
           "Aussen 208 x 132 x 55 inkl. Flansche; Gehaeuse ohne Flansche 208 x 112")
    ox, oy = 38 * mm, 39 * mm
    c.rect(ox, oy - C.FLANGE * mm, C.L * mm, (C.W + 2 * C.FLANGE) * mm)
    c.rect(ox, oy, C.L * mm, C.W * mm)
    for x, y in C.WALL_MOUNT_HOLES:
        c.circle(ox + x * mm, oy + y * mm, C.WALL_MOUNT_D / 2 * mm)
    for x, y in C.LID_BOSSES:
        c.circle(ox + x * mm, oy + y * mm, C.LID_BOSS_D / 2 * mm)
        c.circle(ox + x * mm, oy + y * mm, C.LID_BOSS_PILOT_D / 2 * mm)
    c.setStrokeColor(C_POD)
    for x, y in C.STANDOFFS:
        c.circle(ox + x * mm, oy + y * mm, C.STANDOFF_D / 2 * mm)
        c.circle(ox + x * mm, oy + y * mm, C.STANDOFF_PILOT_D / 2 * mm)
    c.setStrokeColor(colors.black)
    dim_h(c, ox, ox + C.L * mm, oy - 17 * mm, "208")
    dim_v(c, ox + C.L * mm + 9 * mm, oy - C.FLANGE * mm, oy + (C.W + C.FLANGE) * mm, "132")
    label(c, 12 * mm, 25 * mm, "Waveshare-Pilotloecher: (24/25), (169/25), (24/87), (169/87); Raster 145 x 62.", 7)
    label(c, 12 * mm, 20 * mm, "Deckelbossen: (7/7), (7/105), (201/7), (201/105). Boden und Waende 2,8.", 7)
    label(c, 12 * mm, 15 * mm, "Blau = Waveshare-Aufnahmen; Schwarz = Gehaeuse, Deckel- und Wandbefestigungen.", 7)
    footer(c, 1)


def page2_walls(c):
    header(c, "P01 - Laengswand / Seitenansicht",
           "Beide Laengswaende: Ausschnitt 122 breit x 43 hoch; Unterkante Z=12")
    ox, oy = 38 * mm, 55 * mm
    c.rect(ox, oy, C.L * mm, C.H * mm)
    c.rect(ox + C.OPEN_X0 * mm, oy + C.OPEN_Z * mm,
           (C.OPEN_X1 - C.OPEN_X0) * mm, (C.H - C.OPEN_Z) * mm)
    dim_h(c, ox, ox + C.L * mm, oy - 12 * mm, "208")
    dim_h(c, ox + C.OPEN_X0 * mm, ox + C.OPEN_X1 * mm, oy + C.H * mm + 8 * mm, "122")
    dim_v(c, ox + C.L * mm + 8 * mm, oy, oy + C.H * mm, "55")
    dim_v(c, ox + C.OPEN_X1 * mm - 8 * mm, oy, oy + C.OPEN_Z * mm, "12")
    label(c, 12 * mm, 25 * mm, "Beginn X=36,6; Ende X=158,6; Unterkante Z=12,0. Wand 2,8; Boden 2,8.", 7)
    footer(c, 2)


def page3_endwalls(c):
    header(c, "P01 - Stirnwaende",
           "Rechts ZERO/SPAN; links DC5521, 24 V DC und Revisionsmarkierung")
    ox, oy = 24 * mm, 61 * mm
    label(c, ox, oy + 62 * mm, "Rechte Stirnwand / Aussenansicht", 8, True)
    c.rect(ox, oy, C.W * mm, C.H * mm)
    for text, (yy, zz, dd) in (("ZERO", C.ZERO), ("SPAN", C.SPAN)):
        c.circle(ox + yy * mm, oy + zz * mm, dd / 2 * mm)
        c.drawCentredString(ox + yy * mm, oy + (zz + 5) * mm, text)
    c.saveState()
    c.setDash(2, 2)
    c.setStrokeColor(C_POD)
    for yy in C.BTN_HOLDER_Y:
        for zz in C.BTN_HOLDER_Z:
            c.circle(ox + yy * mm, oy + zz * mm, 2.5 * mm)
    c.restoreState()

    ox2 = 160 * mm
    label(c, ox2, oy + 62 * mm, "Linke Stirnwand / Aussenansicht", 8, True)
    c.rect(ox2, oy, C.W * mm, C.H * mm)
    yy, zz, dd = C.DC5521
    c.circle(ox2 + yy * mm, oy + zz * mm, dd / 2 * mm)
    c.drawCentredString(ox2 + yy * mm, oy + (zz + 9) * mm, "24 V DC")
    c.drawString(ox2 + 82 * mm, oy + 7 * mm, "V0.7")

    label(c, 12 * mm, 29 * mm, "ZERO: Y=36 / Z=41 / D3. SPAN: Y=52 / Z=41 / D3. Abstand 16 Mitte-Mitte.", 7)
    label(c, 12 * mm, 24 * mm, "Platine 80 x 20 x 1,5; Halter-Lochbild Y=18/94, Z=35/51 = 76 x 16.", 7)
    label(c, 12 * mm, 19 * mm, "DC5521 links: Y=44 / Z=27,5 / D11,2. Innenansicht jeweils horizontal gespiegelt.", 7)
    footer(c, 3)


def page4_lid(c):
    header(c, "P02 - Deckel / Draufsicht aussen",
           "X-Lage wie V0.6; Sensorpod und Kalibrierhaube nur auf Y=56,0 zentriert")
    ox, oy = 38 * mm, 47 * mm
    c.rect(ox, oy, C.L * mm, C.W * mm)
    for x, y in C.LID_BOSSES:
        c.circle(ox + x * mm, oy + y * mm, C.LID_HOLE_D / 2 * mm)
    c.setStrokeColor(C_POD)
    for x, y, lx, ly in C.VENTS:
        c.rect(ox + x * mm, oy + y * mm, lx * mm, ly * mm)
    for x, y in C.POD_MOUNTS:
        c.circle(ox + x * mm, oy + y * mm, 1.5 * mm)
    c.setStrokeColor(C_HOOD)
    for x, y in C.HOOD_SCREWS:
        c.circle(ox + x * mm, oy + y * mm, 1.1 * mm)

    c.saveState()
    c.setDash(3, 2)
    c.setLineWidth(0.55)
    c.setStrokeColor(C_POD)
    c.rect(ox + C.POD[0] * mm, oy + C.POD[2] * mm,
           (C.POD[1] - C.POD[0]) * mm, (C.POD[3] - C.POD[2]) * mm)
    c.setStrokeColor(C_HOOD)
    c.rect(ox + C.HOOD_PLATE[0] * mm, oy + C.HOOD_PLATE[2] * mm,
           (C.HOOD_PLATE[1] - C.HOOD_PLATE[0]) * mm,
           (C.HOOD_PLATE[3] - C.HOOD_PLATE[2]) * mm)
    c.restoreState()

    c.saveState()
    c.setStrokeColor(C_CENTER)
    c.setDash(5, 2)
    c.setLineWidth(0.7)
    c.line(ox, oy + 56 * mm, ox + 70 * mm, oy + 56 * mm)
    c.restoreState()
    label(c, ox + 71 * mm, oy + 54 * mm, "Y-Mittelachse 56,0", 6.5, False, C_CENTER)
    label(c, ox + 72 * mm, oy + 96 * mm, "P03 unten (blau gestrichelt)", 6.5, False, C_POD)
    label(c, ox + 72 * mm, oy + 89 * mm, "P07 oben (violett gestrichelt)", 6.5, False, C_HOOD)
    label(c, ox + 72 * mm, oy + 82 * mm, "Linke X-Kante bleibt bei X=6,0 / X=4,0", 6.5)

    label(c, 12 * mm, 28 * mm, "Lueftungsschlitze: X=12,0; Y=22,0 + 8,0*n; 33 x 4.", 7)
    label(c, 12 * mm, 23 * mm, "Haubenschrauben: (27/9), (27/103). Pod-Montage: (16/11),(42/11),(16/101),(42/101).", 7)
    label(c, 12 * mm, 18 * mm, "Deckel bleibt vollstaendig 3,0 mm dick; keine O-Ring-Nut in P02.", 7, True)
    footer(c, 4)


def page5_pod(c):
    header(c, "P03 - Sensorpod / Draufsicht innen und Schnitt",
           "V0.6-X-Lage beibehalten; rechts 8,0 mm breiter; P08-Nut im erhoehten Dichtrand")
    ox, oy = 35 * mm, 48 * mm
    w = C.POD[1] - C.POD[0]
    h = C.POD[3] - C.POD[2]
    c.rect(ox, oy, w * mm, h * mm)
    c.rect(ox + C.POD_WALL * mm, oy + C.POD_WALL * mm,
           (w - 2 * C.POD_WALL) * mm, (h - 2 * C.POD_WALL) * mm)
    tx0, tx1 = C.TONGUE_X
    for yy0, yy1 in (C.TONGUE_FRONT_Y, C.TONGUE_BACK_Y):
        c.rect(ox + (tx0 - C.POD[0]) * mm, oy + (yy0 - C.POD[2]) * mm,
               (tx1 - tx0) * mm, (yy1 - yy0) * mm)
        for xh in (16.0, 42.0):
            yh = 11.0 if yy1 <= C.POD[2] else 101.0
            c.circle(ox + (xh - C.POD[0]) * mm, oy + (yh - C.POD[2]) * mm,
                     C.TONGUE_HOLE_D / 2 * mm)
    for xh, yh in C.SENSOR_BOSSES:
        c.circle(ox + (xh - C.POD[0]) * mm, oy + (yh - C.POD[2]) * mm,
                 C.SENSOR_HOLE_D / 2 * mm)
    c.setFillColor(C_LIGHT)
    c.setStrokeColor(colors.black)
    slot_y = oy + (C.GRAVITY_SLOT[2] - C.POD[2]) * mm
    c.rect(ox + w * mm - 2 * mm, slot_y, 2 * mm,
           (C.GRAVITY_SLOT[3] - C.GRAVITY_SLOT[2]) * mm, stroke=1, fill=1)
    c.setFillColor(colors.black)
    rounded_path(c, ox, oy, C.P08_RING, C.POD[0], C.POD[2])

    dim_h(c, ox, ox + w * mm, oy - 10 * mm, fmt(w))
    dim_v(c, ox + w * mm + 10 * mm, oy, oy + h * mm, fmt(h))
    dim_h(c, ox + (C.TONGUE_X[0] - C.POD[0]) * mm,
          ox + (C.TONGUE_X[1] - C.POD[0]) * mm,
          oy + h * mm + 11 * mm, "32,0")
    label(c, ox, oy + h * mm + 17 * mm, "Gesamtlaenge inkl. Laschen: 95,0", 6.5)

    draw_groove_section(c, 132 * mm, 96 * mm, "Schnitt A-A: P03 / P08 / Deckel",
                        "P03 erhoehter Dichtrand Z=54,0..55,0")
    label(c, 132 * mm, 77 * mm, "P08 Kaufteil: EPDM 70 Shore A, D77,0 x 1,50", 7, True, C_ORING)
    label(c, 132 * mm, 70 * mm, "Nutpfad: 51,2 x 79,0, Innenradius R8,0", 7)
    label(c, 132 * mm, 63 * mm, "Sensorbohrungen D3, Abstand 15,0", 7)
    label(c, 132 * mm, 56 * mm, "Kabelschlitz endet bei Z=54,0; Dichtlinie bleibt geschlossen", 7)
    footer(c, 5)


def page6_hood(c):
    header(c, "P07 - Kalibrierhaube / Unterseite und Schnitt",
           "Zwei getrennte EPDM-O-Ringe - je ein geschlossener Ring pro Kammer")
    ox, oy = 35 * mm, 39 * mm
    w = C.HOOD_PLATE[1] - C.HOOD_PLATE[0]
    h = C.HOOD_PLATE[3] - C.HOOD_PLATE[2]
    c.rect(ox, oy, w * mm, h * mm)
    fx0, fx1, fy0, fy1 = C.HOOD_FLOOR_OPEN
    d0, d1 = C.HOOD_DIVIDER_Y
    c.rect(ox + (fx0 - C.HOOD_PLATE[0]) * mm,
           oy + (fy0 - C.HOOD_PLATE[2]) * mm,
           (fx1 - fx0) * mm, (d0 - fy0) * mm)
    c.rect(ox + (fx0 - C.HOOD_PLATE[0]) * mm,
           oy + (d1 - C.HOOD_PLATE[2]) * mm,
           (fx1 - fx0) * mm, (fy1 - d1) * mm)
    for xh, yh in C.HOOD_SCREWS:
        c.circle(ox + (xh - C.HOOD_PLATE[0]) * mm,
                 oy + (yh - C.HOOD_PLATE[2]) * mm, 1.1 * mm)
    rounded_path(c, ox, oy, C.P04A_RING, C.HOOD_PLATE[0], C.HOOD_PLATE[2])
    rounded_path(c, ox, oy, C.P04B_RING, C.HOOD_PLATE[0], C.HOOD_PLATE[2])
    label(c, ox + 15 * mm, oy + 25 * mm, "P04A / untere Kammer", 6.5, True, C_ORING)
    label(c, ox + 15 * mm, oy + 73 * mm, "P04B / obere Kammer", 6.5, True, C_ORING)
    dim_h(c, ox, ox + w * mm, oy - 10 * mm, fmt(w))
    dim_v(c, ox + w * mm + 10 * mm, oy, oy + h * mm, fmt(h))

    draw_groove_section(c, 132 * mm, 103 * mm, "Schnitt B-B: P07 / P04 / Deckel",
                        "Nut in Unterseite P07; Deckeloberseite bleibt eben")
    label(c, 132 * mm, 82 * mm, "P04A: D45,0 x 1,50 - SKU H48761", 7, True, C_ORING)
    label(c, 132 * mm, 75 * mm, "P04B: D50,0 x 1,50 - SKU H96773", 7, True, C_ORING)
    label(c, 132 * mm, 68 * mm, "Beide Nuten 1,80 x 1,10; Innenradius R8,0", 7)
    label(c, 132 * mm, 61 * mm, "Trennsteg 5,0; Kammern bleiben gegeneinander dicht", 7)
    label(c, 132 * mm, 54 * mm, "Grundplatte 56,0 x 105,6 x 3,0", 7)
    footer(c, 6)


def page7_orings(c):
    header(c, "Kaufteile - EPDM-O-Ringe und Nutdaten",
           "Lagernde Standardringe; keine geklebte Rundschnur im Gasweg")
    x0 = 18 * mm
    y = 158 * mm
    cols = [0, 30, 68, 103, 135, 169, 214]
    headers = ["Pos.", "Abmessung", "SKU", "Nut B x T", "Verpressung", "Verwendung", "Menge"]
    c.setFont("Helvetica-Bold", 7)
    for i, text in enumerate(headers):
        c.drawString(x0 + cols[i] * mm, y, text)
    c.line(x0, y - 2 * mm, PW - 18 * mm, y - 2 * mm)
    rows = [
        ("P04A", "D45,0 x 1,50", "H48761", "1,80 x 1,10", "26,7 %", "untere Kammer", "1 / 2 empf."),
        ("P04B", "D50,0 x 1,50", "H96773", "1,80 x 1,10", "26,7 %", "obere Kammer", "1 / 2 empf."),
        ("P08", "D77,0 x 1,50", "H48789", "1,80 x 1,10", "26,7 %", "Pod / Deckel", "1 / 2 empf."),
    ]
    c.setFont("Helvetica", 7)
    for row_index, row in enumerate(rows):
        yy = y - (9 + 9 * row_index) * mm
        for col_index, value in enumerate(row):
            c.drawString(x0 + cols[col_index] * mm, yy, value)
        c.line(x0, yy - 2 * mm, PW - 18 * mm, yy - 2 * mm)

    label(c, 18 * mm, 112 * mm, "Einbauhinweise", 8, True)
    notes = [
        "Material: EPDM 70 Shore A; geschlossene Kaufteile, nicht schneiden oder kleben.",
        "Ring vor Montage leicht in die abgerundete Rechteckform legen; nicht verdrehen.",
        "Rechnerische Dehnung aller drei Pfade < 0,2 %.",
        "Nuten beim Epoxidieren abkleben; Harz im Nutgrund reduziert die freie Hoehe.",
        "Schrauben gleichmaessig ueber Kreuz anziehen; Anzugsmoment nach Passversuch festlegen.",
        "Vor Installation: Sitz, Leckrate, Nullpunkt und Rueckkehr nach Pruefgas pruefen.",
    ]
    for i, text in enumerate(notes):
        label(c, 22 * mm, (102 - 8 * i) * mm, "- " + text, 7)
    label(c, 18 * mm, 47 * mm, "Bestellreferenz: PURCHASED_O_RINGS.csv im V0.7-Ordner", 7, True)
    label(c, 18 * mm, 40 * mm, "Erforderlich: je 1 Stueck. Wegen Termin und Montageversuch empfohlen: je 2 Stueck.", 7)
    footer(c, 7)


def page8_p05(c):
    header(c, "P05 - Kabelstopfen und Dichtlinienbezug",
           "Quader 4 x 6 x 8; P08-Dichtrand bleibt oberhalb des Schlitzes geschlossen")
    ox, oy = 35 * mm, 103 * mm
    c.rect(ox, oy, 4 * mm, 6 * mm)
    label(c, ox - 2 * mm, oy + 11 * mm, "Draufsicht 4 x 6", 7)
    c.rect(ox + 55 * mm, oy, 4 * mm, 8 * mm)
    label(c, ox + 45 * mm, oy + 13 * mm, "Vorderansicht 4 x 8", 7)
    c.rect(ox + 110 * mm, oy, 6 * mm, 8 * mm)
    label(c, ox + 100 * mm, oy + 13 * mm, "Seitenansicht 6 x 8", 7)

    sx, sy = 48 * mm, 49 * mm
    c.setFillColor(C_LIGHT)
    c.setStrokeColor(colors.black)
    c.rect(sx, sy, 55 * mm, 22 * mm, stroke=1, fill=1)
    c.setFillColor(colors.white)
    c.rect(sx + 45 * mm, sy, 4.5 * mm, 14 * mm, stroke=1, fill=1)
    c.setFillColor(colors.black)
    c.setStrokeColor(C_ORING)
    c.setLineWidth(1.0)
    c.line(sx + 3 * mm, sy + 19 * mm, sx + 52 * mm, sy + 19 * mm)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.35)
    label(c, sx, sy + 27 * mm, "Schematischer Schnitt P03 rechte Kabelseite", 8, True)
    label(c, sx + 58 * mm, sy + 18 * mm, "P08-Dichtlinie Z=54..55", 7, False, C_ORING)
    label(c, sx + 58 * mm, sy + 11 * mm, "Kabelschlitz Z=46..54", 7)
    label(c, sx + 58 * mm, sy + 4 * mm, "P05 schliesst den Schlitz", 7)
    footer(c, 8)


def page9_assembly(c):
    header(c, "V0.7 - Dichtaufbau / Explosionsschema",
           "P07 und P03 tragen die Nuten; P02 bleibt als ebene 3,0-mm-Trennplatte erhalten")
    cx = 82 * mm
    y_p03 = 52 * mm
    y_lid = 101 * mm
    y_p07 = 127 * mm
    width = 90 * mm

    c.setFillColor(colors.HexColor("#EAF1F8"))
    c.setStrokeColor(C_POD)
    c.rect(cx, y_p03, width, 24 * mm, stroke=1, fill=1)
    label(c, cx + 3 * mm, y_p03 + 9 * mm, "P03 Sensorpod - P08-Nut im erhoehten Rand", 8, True, C_POD)
    c.setFillColor(colors.HexColor("#F6DAD8"))
    c.setStrokeColor(C_ORING)
    c.rect(cx + 8 * mm, y_p03 + 21 * mm, width - 16 * mm, 3 * mm, stroke=1, fill=1)
    label(c, cx + width + 4 * mm, y_p03 + 21 * mm, "P08", 7, True, C_ORING)

    c.setFillColor(colors.HexColor("#F2F2F2"))
    c.setStrokeColor(colors.black)
    c.rect(cx - 8 * mm, y_lid, width + 16 * mm, 3 * mm, stroke=1, fill=1)
    label(c, cx + 3 * mm, y_lid + 7 * mm, "P02 Deckel 3,0 - keine Nut", 8, True)

    c.setFillColor(colors.HexColor("#F6DAD8"))
    c.setStrokeColor(C_ORING)
    c.rect(cx + 9 * mm, y_p07 - 3 * mm, width / 2 - 14 * mm, 3 * mm, stroke=1, fill=1)
    c.rect(cx + width / 2 + 5 * mm, y_p07 - 3 * mm, width / 2 - 14 * mm, 3 * mm, stroke=1, fill=1)
    label(c, cx + width + 4 * mm, y_p07 - 2 * mm, "P04A/B", 7, True, C_ORING)
    c.setFillColor(colors.HexColor("#F1E8F7"))
    c.setStrokeColor(C_HOOD)
    c.rect(cx, y_p07, width, 25 * mm, stroke=1, fill=1)
    label(c, cx + 3 * mm, y_p07 + 9 * mm, "P07 Kalibrierhaube - zwei Nuten in Unterseite", 8, True, C_HOOD)

    c.setStrokeColor(C_DIM)
    c.setLineWidth(0.5)
    c.line(cx + width / 2, y_p03 + 26 * mm, cx + width / 2, y_lid - 2 * mm)
    c.line(cx + width / 2, y_lid + 5 * mm, cx + width / 2, y_p07 - 5 * mm)
    label(c, 18 * mm, 43 * mm, "Montagereihenfolge:", 8, True)
    steps = [
        "P08 in P03-Nut einlegen; Kabelstopfen und Kabel pruefen.",
        "P03 unter P02 montieren und gleichmaessig anziehen.",
        "P04A und P04B in P07-Nuten einlegen; beide Kammern getrennt halten.",
        "P07 auf P02 setzen und gleichmaessig verschrauben.",
        "Lecktest mit Frischluft/Nullgas, danach Pruefgas und Nullpunktrueckkehr dokumentieren.",
    ]
    for i, text in enumerate(steps):
        label(c, 22 * mm, (35 - 6 * i) * mm, f"{i+1}. {text}", 7)
    footer(c, 9)


def page10_summary(c):
    header(c, "V0.7 - Freigabe- und Pruefliste",
           "Skizzenstand nach Y-Zentrierung und Umstellung auf geschlossene EPDM-Kauf-O-Ringe")
    label(c, 18 * mm, 160 * mm, "Umgesetzt", 8, True)
    items = [
        "X-Lage der Sensor-/Kalibriereinheit entspricht wieder V0.6.",
        "Gesamte Einheit ist auf der Y-Achse bei Y=56,0 zentriert.",
        "P03 bleibt auf der rechten Kabelseite 8,0 mm breiter.",
        "Gedruckte TPU-Dichtungen P04/P08 sind durch drei geschlossene EPDM-Ringe ersetzt.",
        "P04-Nuten liegen in P07; P08-Nut liegt im erhoehten P03-Dichtrand.",
        "P02 bleibt vollstaendig 3,0 mm dick und ohne O-Ring-Nut.",
        "Markierungen ZERO, SPAN, 24 V DC, V0.7, IN und OUT bleiben erhalten.",
        "Massskizzen zeigen jetzt Nutquerschnitt, Kaufteile und Montagereihenfolge.",
    ]
    for i, text in enumerate(items):
        label(c, 22 * mm, (151 - 8 * i) * mm, "- " + text, 7)

    label(c, 18 * mm, 82 * mm, "Vor Montage pruefen", 8, True)
    checks = [
        "[ ] Drei O-Ringe stimmen mit D45 x 1,50 / D50 x 1,50 / D77 x 1,50 ueberein.",
        "[ ] Nuten sind sauber, frei von Epoxid und ohne Druckgrate.",
        "[ ] Ringe liegen ohne Verdrehung, Ausbeulung oder Quetschung in den Nuten.",
        "[ ] P03 und P07 schliessen plan gegen P02; Schrauben werden gleichmaessig angezogen.",
        "[ ] Gravity-Kabel und P05 unterbrechen die P08-Dichtlinie nicht.",
        "[ ] Lecktest, Nullpunkt, Pruefgas-Stabilitaet und Rueckkehr zum Nullpunkt sind dokumentiert.",
    ]
    for i, text in enumerate(checks):
        label(c, 22 * mm, (73 - 8 * i) * mm, text, 7)
    footer(c, 10, "CAD-Stand: V0.7 korrigiert - EPDM-O-Ringe")


def main():
    c = canvas.Canvas(str(OUT), pagesize=PAGE)
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
        page10_summary,
    ]
    for fn in pages:
        fn(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
