"""Generate revised 1:1 engineering sketches for AirMonitor Compact V0.8.

Includes Y-centred sensor group, purchased EPDM O-rings, the complete
ZERO/SPAN assembly 15 mm lower, and the edge-guided flush sliding lid.
"""
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors

import compact_params as C

OUT = Path(__file__).resolve().parent / "AirMonitor_V08_Massskizzen_1zu1.pdf"
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
    c.drawString(12 * mm, PH - 12 * mm, "LAMINAR | AirMonitor HCHO | V0.8")
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
    header(c,"P01 - abgerundeter Gehaeuseboden / Draufsicht innen",
           "3,2-mm-Wand; R6; Schulter fuehrt den Deckel; Mitte ohne Deckelfixierung")
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
    c.rect(ox+(C.EDGE_SNAP_X-C.EDGE_SNAP_WIDTH/2)*mm,
           oy+(C.SHOULDER_INSET-C.EDGE_SNAP_PROJ)*mm,
           C.EDGE_SNAP_WIDTH*mm,C.EDGE_SNAP_PROJ*mm)
    c.setStrokeColor(colors.black)
    dim_h(c,ox,ox+C.L*mm,oy-17*mm,"208")
    dim_v(c,ox+C.L*mm+9*mm,oy-C.FLANGE*mm,oy+(C.W+C.FLANGE)*mm,"132")
    label(c,12*mm,27*mm,"Violett: durchgehende Schulter je 2,3 zurueckgesetzt; Beginn Z45,0.",7)
    label(c,12*mm,22*mm,"Rot: nur eine kleine 45-Grad-Rastnase am rechten Rand; keine C-Fuehrung.",7)
    label(c,12*mm,17*mm,"Mitte frei; Deckel wird durch die Schulter gefuehrt. Waveshare-Bossen bleiben notwendig.",7)
    footer(c,1)

def page2_walls(c):
    header(c,"P01/P02 - Laengswand und 10-mm-Deckeluebergriff",
           "Deckelschuerze Z55..45; freie Bodenoeffnung endet bei Z45")
    ox,oy=38*mm,55*mm
    c.roundRect(ox,oy,C.L*mm,C.H*mm,C.BODY_CORNER_R*mm)
    c.rect(ox+C.OPEN_X0*mm,oy+C.OPEN_Z*mm,(C.OPEN_X1-C.OPEN_X0)*mm,(C.OPEN_TOP_Z-C.OPEN_Z)*mm)
    c.saveState(); c.setStrokeColor(C_HOOD); c.setLineWidth(0.8)
    c.line(ox-C.LID_OUTSET*mm,oy+(C.LID_Z-C.LID_OVERLAP)*mm,ox-C.LID_OUTSET*mm,oy+(C.LID_Z+C.LID_T)*mm)
    c.line(ox+(C.L+C.LID_OUTSET)*mm,oy+(C.LID_Z-C.LID_OVERLAP)*mm,ox+(C.L+C.LID_OUTSET)*mm,oy+(C.LID_Z+C.LID_T)*mm)
    c.line(ox-C.LID_OUTSET*mm,oy+(C.LID_Z+C.LID_T)*mm,ox+(C.L+C.LID_OUTSET)*mm,oy+(C.LID_Z+C.LID_T)*mm)
    c.restoreState()
    dim_h(c,ox,ox+C.L*mm,oy-12*mm,"208")
    dim_h(c,ox+C.OPEN_X0*mm,ox+C.OPEN_X1*mm,oy+C.OPEN_TOP_Z*mm+7*mm,"122")
    dim_v(c,ox+C.L*mm+8*mm,oy,oy+C.H*mm,"55")
    dim_v(c,ox+C.L*mm+18*mm,oy+C.SHOULDER_Z0*mm,oy+C.H*mm,"10")
    label(c,12*mm,27*mm,"Bodenoeffnung: X36,6..158,6 / Z12,0..45,0 = 122 x 33.",7)
    label(c,12*mm,22*mm,"Deckel: Topplatte 3,0; Schuerze 10,0; Oberseite ist Druckbettseite.",7)
    label(c,12*mm,17*mm,"Koerper/Deckel R6,0 und aussen buendig; Schulter R3,7.",7)
    footer(c,2)

def page3_endwalls(c):
    header(c, "P01 - Stirnwaende",
           "Rechts komplette ZERO-/SPAN-Baugruppe 15,0 mm tiefer; links DC5521")
    ox, oy = 24 * mm, 61 * mm
    label(c, ox, oy + 62 * mm, "Rechte Stirnwand / Aussenansicht", 8, True)
    c.rect(ox, oy, C.W * mm, C.H * mm)
    for text_label, (yy, zz, dd) in (("ZERO", C.ZERO), ("SPAN", C.SPAN)):
        c.circle(ox + yy * mm, oy + zz * mm, dd / 2 * mm)
        c.drawCentredString(ox + yy * mm, oy + (zz + 5) * mm, text_label)
    c.saveState()
    c.setDash(2, 2)
    c.setStrokeColor(C_POD)
    for yy in C.BTN_HOLDER_Y:
        for zz in C.BTN_HOLDER_Z:
            c.circle(ox + yy * mm, oy + zz * mm, 2.5 * mm)
    c.restoreState()
    dim_v(c, ox + C.W * mm + 7 * mm, oy, oy + C.ZERO[1] * mm, "26,0")

    ox2 = 160 * mm
    label(c, ox2, oy + 62 * mm, "Linke Stirnwand / Aussenansicht", 8, True)
    c.rect(ox2, oy, C.W * mm, C.H * mm)
    yy, zz, dd = C.DC5521
    c.circle(ox2 + yy * mm, oy + zz * mm, dd / 2 * mm)
    c.drawCentredString(ox2 + yy * mm, oy + (zz + 9) * mm, "24 V DC")
    c.drawString(ox2 + 82 * mm, oy + 7 * mm, "V0.8")

    label(c, 12 * mm, 29 * mm, "ZERO: Y=36 / Z=26 / D3. SPAN: Y=52 / Z=26 / D3. Abstand 16 Mitte-Mitte.", 7)
    label(c, 12 * mm, 24 * mm, "Platine 80 x 20 x 1,5; Halter Y=18/94, Z=20/36; Lochbild 76 x 16.", 7)
    label(c, 12 * mm, 19 * mm, "Platine, beide Schalter, vier Halter und beide Serviceoeffnungen gemeinsam -15,0 mm in Z.", 7, True)
    footer(c, 3)

def page4_lid(c):
    header(c,"P02 - abgerundeter Ueberwurf-Schiebedeckel",
           "208 x 112; R6; 10-mm-Schuerze; Kerbe offen gerade bis zur Unterkante")
    ox,oy=37.5*mm,46.5*mm
    w=C.LID_X1-C.LID_X0; h=C.LID_Y1-C.LID_Y0
    c.roundRect(ox,oy,w*mm,h*mm,C.LID_CORNER_R*mm)
    c.saveState(); c.setDash(3,2); c.setStrokeColor(C_HOOD)
    c.roundRect(ox+C.LID_SKIRT_W*mm,oy+C.LID_SKIRT_W*mm,
                (w-2*C.LID_SKIRT_W)*mm,(h-2*C.LID_SKIRT_W)*mm,
                (C.LID_CORNER_R-C.LID_SKIRT_W)*mm)
    c.restoreState()
    c.setStrokeColor(C_POD)
    for x,y,lx,ly in C.VENTS:
        c.rect(ox+(x-C.LID_X0)*mm,oy+(y-C.LID_Y0)*mm,lx*mm,ly*mm)
    c.setStrokeColor(C_ORING)
    nx0=C.EDGE_SNAP_X-C.EDGE_SNAP_NOTCH_W/2
    c.line(ox+(nx0-C.LID_X0)*mm,oy,
           ox+(nx0-C.LID_X0)*mm,oy+8*mm)
    c.line(ox+(nx0+C.EDGE_SNAP_NOTCH_W-C.LID_X0)*mm,oy,
           ox+(nx0+C.EDGE_SNAP_NOTCH_W-C.LID_X0)*mm,oy+8*mm)
    c.line(ox+(nx0-C.LID_X0)*mm,oy+8*mm,
           ox+(nx0+C.EDGE_SNAP_NOTCH_W-C.LID_X0)*mm,oy+8*mm)
    dim_h(c,ox,ox+w*mm,oy-10*mm,"208,0")
    dim_v(c,ox+w*mm+8*mm,oy,oy+h*mm,"112,0")

    # Enlarged side section explaining the red-line correction.
    sx,sy=170*mm,25*mm
    c.setStrokeColor(colors.black)
    c.rect(sx,sy,38*mm,18*mm)
    c.setStrokeColor(C_ORING); c.setLineWidth(1.1)
    c.line(sx+10*mm,sy,sx+10*mm,sy+10*mm)
    c.line(sx+10*mm,sy+10*mm,sx+28*mm,sy+10*mm)
    label(c,sx,sy+22*mm,"Schnitt: offene Kerbe",7,True)
    label(c,sx,sy-5*mm,"Rot: senkrecht gerade bis Unterkante; kein C-Kanal.",6.5)

    label(c,12*mm,29*mm,"Aufsetzen: +8,0 mm in X; Schliessen in Bedienansicht von links nach rechts.",7)
    label(c,12*mm,24*mm,"Schulter fuehrt. Rechte Seitenwand federt ueber 45-Grad-Nase und rastet in Kerbe ein.",7)
    label(c,12*mm,19*mm,"Druck: Oberseite auf Bett; Kerbe ist in Drucklage nach oben offen, daher ohne Stuetze.",7,True)
    footer(c,4)

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
    label(c, 18 * mm, 47 * mm, "Bestellreferenz: PURCHASED_O_RINGS.csv im V0.8-Ordner", 7, True)
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
    header(c,"V0.8 - Gehaeuse- und Deckelmontage",
           "Pruefstation bleibt auf P02; P02 wird als 10-mm-Kappe auf die Schulter gesetzt")
    label(c,18*mm,158*mm,"Schliessablauf",8,True)
    steps=[
        "P03, Sensor, Kabel, P05, P07 und O-Ringe am Deckel montieren.",
        "Deckel +8,0 mm in X versetzt ueber die Schulter absenken.",
        "Alle vier Wandlaschen durch die offenen Einfuehrungen fuehren.",
        "Deckel 8,0 mm nach links schieben; Laschen halten die Kappe vertikal.",
        "Federzunge einrasten und umlaufenden 0,30-mm-Spalt kontrollieren.",
        "Zum Oeffnen Zunge loesen, 8,0 mm nach rechts schieben und abheben.",
    ]
    for i,t in enumerate(steps): label(c,22*mm,(148-9*i)*mm,f"{i+1}. {t}",7)
    label(c,18*mm,85*mm,"Schematischer Schnitt",8,True)
    x=52*mm; y=40*mm
    c.setFillColor(colors.HexColor("#EAF1F8")); c.setStrokeColor(C_POD)
    c.roundRect(x,y,150*mm,45*mm,6*mm,stroke=1,fill=1)
    c.setFillColor(colors.white)
    c.roundRect(x+3.2*mm,y+3.2*mm,143.6*mm,42*mm,3*mm,stroke=1,fill=1)
    c.setFillColor(colors.HexColor("#F1E8F7")); c.setStrokeColor(C_HOOD)
    c.roundRect(x-0.5*mm,y+35*mm,151*mm,13*mm,6.5*mm,stroke=1,fill=1)
    label(c,x+154*mm,y+40*mm,"P02: 3 mm Top + 10 mm Schuerze",7)
    label(c,x+154*mm,y+31*mm,"P01: Schulter ab Z45",7)
    label(c,x+154*mm,y+22*mm,"keine Deckelsaeulen",7,True)
    footer(c,9)

def page10_summary(c):
    header(c,"V0.8 - Freigabe- und Pruefliste",
           "Abgerundete 10-mm-Kappe, dickere Waende und wandintegrierte Schiebefuehrung")
    label(c,18*mm,160*mm,"Umgesetzt",8,True)
    items=[
        "Microtaster und Pruefstation aus V0.7 unveraendert uebernommen.",
        "P01 Wand/Boden 3,2; Ecken R6,0; Schulter R4,0.",
        "P02 209 x 113 mit R6,5 und 10,0-mm-Uebergriff.",
        "Keine zusaetzlichen Deckelstuetzen oder Verschlusssaeulen in der Mitte.",
        "Vier wandintegrierte 45-Grad-Laschen und offene Einfuehrschlitze.",
        "8-mm-Schiebeweg mit Federzunge am Ende.",
        "P01/P02 ohne Slicer-Stuetzen vorgesehen.",
        "Seitliche freie Oeffnung 122 x 33 unterhalb des Uebergriffs.",
    ]
    for i,t in enumerate(items): label(c,22*mm,(151-8*i)*mm,"- "+t,7)
    label(c,18*mm,82*mm,"Vor Freigabe praktisch pruefen",8,True)
    checks=[
        "[ ] Deckel senkt sich in +8-mm-Lage ohne Verkanten ab.",
        "[ ] Vier Laschen greifen gleichzeitig; kein Klappern oder Klemmen.",
        "[ ] offene Seitenkerbe funktioniert mindestens 20 Zyklen ohne Riss.",
        "[ ] P03/P07 und Kabel haben in beiden Lagen Freiraum.",
        "[ ] Deckel ist plan; Schuerze und Ecken sind unverzogen.",
        "[ ] O-Ring-Sitz, Pruefstation, Leckrate und Nullpunkt sind dokumentiert.",
    ]
    for i,t in enumerate(checks): label(c,22*mm,(73-8*i)*mm,t,7)
    footer(c,10,"CAD-Stand: V0.8 - abgerundeter Ueberwurf-Schiebedeckel")

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
