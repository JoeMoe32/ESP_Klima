"""Generate 1:1 A4 landscape dimensional sketches for AirMonitor V0.7."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import black, HexColor

import compact_params as C

OUT = Path(__file__).resolve().parent / 'AirMonitor_V07_Massskizzen_1zu1.pdf'
PW, PH = landscape(A4)
BLUE = HexColor('#0b5d8b')
GRAY = HexColor('#666666')


def xpt(v):
    return v * mm


def txt(c, x, y, s, size=8, color=black, bold=False, align='left'):
    c.setFillColor(color)
    c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
    if align == 'center':
        c.drawCentredString(xpt(x), xpt(y), s)
    elif align == 'right':
        c.drawRightString(xpt(x), xpt(y), s)
    else:
        c.drawString(xpt(x), xpt(y), s)


def line(c, x1, y1, x2, y2, width=0.25, color=black, dash=None):
    c.setStrokeColor(color)
    c.setLineWidth(xpt(width))
    c.setDash(*(dash or []))
    c.line(xpt(x1), xpt(y1), xpt(x2), xpt(y2))
    c.setDash()


def rect(c, x, y, w, h, width=0.25, color=black, fill=None, radius=0):
    c.setStrokeColor(color)
    c.setLineWidth(xpt(width))
    if fill:
        c.setFillColor(fill)
        mode = 1
    else:
        mode = 0
    if radius:
        c.roundRect(xpt(x), xpt(y), xpt(w), xpt(h), xpt(radius), stroke=1, fill=mode)
    else:
        c.rect(xpt(x), xpt(y), xpt(w), xpt(h), stroke=1, fill=mode)


def circle(c, x, y, d, width=0.25, color=black, fill=None):
    c.setStrokeColor(color)
    c.setLineWidth(xpt(width))
    if fill:
        c.setFillColor(fill)
        mode = 1
    else:
        mode = 0
    c.circle(xpt(x), xpt(y), xpt(d / 2), stroke=1, fill=mode)


def cross(c, x, y, size=2.0, color=GRAY):
    line(c, x - size, y, x + size, y, 0.18, color)
    line(c, x, y - size, x, y + size, 0.18, color)


def dim_h(c, x1, x2, y, label, ext=2.5):
    line(c, x1, y, x2, y, 0.18, GRAY)
    line(c, x1, y - ext, x1, y + ext, 0.18, GRAY)
    line(c, x2, y - ext, x2, y + ext, 0.18, GRAY)
    line(c, x1 - 1.2, y - 1.2, x1 + 1.2, y + 1.2, 0.18, GRAY)
    line(c, x2 - 1.2, y - 1.2, x2 + 1.2, y + 1.2, 0.18, GRAY)
    txt(c, (x1 + x2) / 2, y + 2.0, label, 7, GRAY, align='center')


def dim_v(c, x, y1, y2, label, ext=2.5):
    line(c, x, y1, x, y2, 0.18, GRAY)
    line(c, x - ext, y1, x + ext, y1, 0.18, GRAY)
    line(c, x - ext, y2, x + ext, y2, 0.18, GRAY)
    line(c, x - 1.2, y1 - 1.2, x + 1.2, y1 + 1.2, 0.18, GRAY)
    line(c, x - 1.2, y2 - 1.2, x + 1.2, y2 + 1.2, 0.18, GRAY)
    c.saveState()
    c.translate(xpt(x + 2.0), xpt((y1 + y2) / 2))
    c.rotate(90)
    c.setFillColor(GRAY)
    c.setFont('Helvetica', 7)
    c.drawCentredString(0, 0, label)
    c.restoreState()


def header(c, subtitle, page_no, note=''):
    txt(c, 12, 197, 'LAMINAR | AirMonitor HCHO | V0.7', 14, bold=True)
    txt(c, 12, 187, subtitle, 10, bold=True)
    if note:
        txt(c, 12, 179, note, 7.5)
    line(c, 12, 174, 285, 174, 0.35)
    txt(c, 285, 8, str(page_no), 7, align='right')
    line(c, 12, 15, 285, 15, 0.3)
    txt(c, 12, 9, 'A4 quer | Massstab 1:1 | Masse in mm | Druck: 100 % / Tatsaechliche Groesse', 7)
    dim_h(c, 235, 285, 23, 'Kontrolle: 50 mm')


def finish(c):
    c.showPage()


c = canvas.Canvas(str(OUT), pagesize=(PW, PH))

# 1 P01 top view interior
header(c, 'P01 - Gehaeuseboden / Draufsicht innen', 1,
       'Aussen 208 x 132 x 55 inkl. Befestigungsflansche; Gehaeuse ohne Flansche 208 x 112')
ox, oy = 38, 32
rect(c, ox, oy, 208, 132)
rect(c, ox, oy + 10, 208, 112)
# wall mount holes, global y shifted +10 for flange drawing
for x, y in C.WALL_MOUNT_HOLES:
    circle(c, ox + x, oy + y + 10, C.WALL_MOUNT_D)
    cross(c, ox + x, oy + y + 10, 1.8)
# lid bosses
for x, y in C.LID_BOSSES:
    circle(c, ox + x, oy + y + 10, C.LID_BOSS_D)
    circle(c, ox + x, oy + y + 10, C.LID_BOSS_PILOT_D)
# board standoffs
for x, y in C.STANDOFFS:
    circle(c, ox + x, oy + y + 10, C.STANDOFF_D)
    circle(c, ox + x, oy + y + 10, C.STANDOFF_PILOT_D)
# dimensions and labels
dim_h(c, ox, ox + 208, oy - 4, '208')
dim_v(c, ox + 216, oy, oy + 132, '132')
dim_h(c, ox, ox + 24, oy + 76, '24')
dim_h(c, ox, ox + 169, oy + 83, '169')
dim_h(c, ox + 169, ox + 208, oy + 76, '39')
dim_v(c, ox + 182, oy + 10, oy + 35, '25')
dim_v(c, ox + 182, oy + 97, oy + 122, '25')
txt(c, 12, 26, 'Deckelbossen rechts: X=201,0 (7,0 mm vom Rand).', 7.5)
txt(c, 12, 21, 'Board-Pilotloecher: XY (24/25), (169/25), (24/87), (169/87); Raster 145 x 62.', 7.5)
finish(c)

# 2 long wall
header(c, 'P01 - Laengswand / Seitenansicht', 2,
       'Beide Laengswaende unveraendert; rechteckiger Ausschnitt')
ox, oy = 38, 75
rect(c, ox, oy, 208, 55)
# cutout represented by white box over top
c.setFillColorRGB(1, 1, 1)
c.rect(xpt(ox + C.OPEN_X0), xpt(oy + C.OPEN_Z), xpt(C.OPEN_X1 - C.OPEN_X0), xpt(H := 55 - C.OPEN_Z), stroke=0, fill=1)
line(c, ox + C.OPEN_X0, oy + C.OPEN_Z, ox + C.OPEN_X0, oy + 55)
line(c, ox + C.OPEN_X1, oy + C.OPEN_Z, ox + C.OPEN_X1, oy + 55)
line(c, ox + C.OPEN_X0, oy + C.OPEN_Z, ox + C.OPEN_X1, oy + C.OPEN_Z)
dim_h(c, ox, ox + 208, oy - 10, '208')
dim_v(c, ox + 216, oy, oy + 55, '55')
dim_h(c, ox, ox + C.OPEN_X0, oy - 2, '36,6')
dim_h(c, ox + C.OPEN_X0, ox + C.OPEN_X1, oy + 62, '122')
dim_v(c, ox + C.OPEN_X1 + 8, oy, oy + C.OPEN_Z, '12')
txt(c, 12, 26, 'Ausschnitt: 122 breit x 43 hoch; Beginn X=36,6; Ende X=158,6; Unterkante Z=12.', 7.5)
finish(c)

# 3 right end wall
header(c, 'P01 - Rechte Stirnwand / Aussenansicht', 3,
       'ZERO / SPAN und angepasste Markierungen; DC5521 auf Gegenseite')
ox, oy = 60, 75
rect(c, ox, oy, 112, 55)
for name, item in [('ZERO', C.ZERO), ('SPAN', C.SPAN)]:
    y, z, d = item
    circle(c, ox + y, oy + z, d)
    txt(c, ox + y, oy + z + 7, name, 7, bold=True, align='center')
# PCB projection dashed
c.setDash(3, 2)
rect(c, ox + 16, oy + 33, 80, 20, 0.2, BLUE)
c.setDash()
txt(c, ox + 56, oy + 38, 'Microtaster-Platine 80 x 20', 6.5, BLUE, align='center')
dim_h(c, ox + C.ZERO[0], ox + C.SPAN[0], oy + 63, '16')
dim_h(c, ox, ox + 112, oy - 8, '112')
dim_v(c, ox + 120, oy, oy + 55, '55')
txt(c, 190, 118, 'Lochmitten ab links / unten:', 8, bold=True)
txt(c, 190, 110, 'ZERO: Y=36 / Z=41 / D3', 7.5)
txt(c, 190, 103, 'SPAN: Y=52 / Z=41 / D3', 7.5)
txt(c, 190, 96, 'Innenhalter: Y=18 / 94; Z=35 / 51', 7.5)
txt(c, 190, 89, 'Halter-Lochbild: 76 x 16; Laenge 6', 7.5)
txt(c, 12, 26, 'Aussenmarkierungen ZERO und SPAN sind in die Wand 0,35 mm vertieft.', 7.5)
finish(c)

# 4 left end wall
header(c, 'P01 - Linke Stirnwand / Aussenansicht', 4,
       'DC5521 auf der gegenueberliegenden Stirnwand; Hoehe unveraendert')
ox, oy = 60, 75
rect(c, ox, oy, 112, 55)
y, z, d = C.DC5521
circle(c, ox + y, oy + z, d)
txt(c, ox + y, oy + z + 11, '24 V DC', 8, bold=True, align='center')
txt(c, ox + 91, oy + 7, 'V0.7', 6.5, align='center')
dim_h(c, ox, ox + y, oy + 18, '44')
dim_v(c, ox + y + 16, oy, oy + z, '27,5')
dim_h(c, ox, ox + 112, oy - 8, '112')
dim_v(c, ox + 120, oy, oy + 55, '55')
txt(c, 190, 112, 'DC5521: Y=44 / Z=27,5 / D11,2', 8)
txt(c, 190, 102, 'Markierung: 24 V DC', 8)
txt(c, 190, 92, 'Montage weiterhin mit Mutter gekontert.', 8)
finish(c)

# 5 lid top
header(c, 'P02 - Deckel / Draufsicht aussen', 5,
       'Sensor-/Kalibriergruppe 20 mm Richtung Mitte; Dichtungsnut P04 oben')
ox, oy = 38, 45
rect(c, ox, oy, 208, 112)
for x, y in C.LID_BOSSES:
    circle(c, ox + x, oy + y, C.LID_HOLE_D)
    circle(c, ox + x, oy + y, C.LID_CBORE_D)
for x, y, lx, ly in C.VENTS:
    rect(c, ox + x, oy + y, lx, ly)
for x, y in C.POD_MOUNTS:
    circle(c, ox + x, oy + y, C.POD_BOSS_D, 0.18, BLUE)
for x, y in C.HOOD_SCREWS:
    circle(c, ox + x, oy + y, C.HOOD_SCREW_BOSS_D, 0.18, BLUE)
# groove outline top
p4 = C.P04
rect(c, ox + p4['x'][0], oy + p4['y'][0], p4['x'][1]-p4['x'][0], p4['y'][1]-p4['y'][0], 0.25, BLUE, radius=4)
line(c, ox + p4['x'][0] + p4['web'], oy + p4['bar_y'][0], ox + p4['x'][1] - p4['web'], oy + p4['bar_y'][0], 0.25, BLUE)
line(c, ox + p4['x'][0] + p4['web'], oy + p4['bar_y'][1], ox + p4['x'][1] - p4['web'], oy + p4['bar_y'][1], 0.25, BLUE)
dim_h(c, ox, ox + 208, oy - 8, '208')
dim_v(c, ox + 216, oy, oy + 112, '112')
dim_h(c, ox + 12, ox + 32, oy + 60, 'V0.6 -> V0.7: +20')
txt(c, 12, 29, 'Rechte Deckelschrauben jetzt ebenfalls 7 mm vom Rand: XY (201/7), (201/105).', 7.5)
txt(c, 12, 24, 'Lueftungsschlitze starten bei X=32 statt X=12. P04-Nut: 0,6 tief.', 7.5)
finish(c)

# 6 sensor pod
header(c, 'P03 - Sensorpod / Draufsicht innen und Seitenansicht', 6,
       '8 mm nach rechts verbreitert; neue Nennbreite 53,5 mm')
ox, oy = 58, 52
# top view body and tabs
rect(c, ox, oy + 6.5, 53.5, 82)
rect(c, ox + 7, oy, 32, 6.5)
rect(c, ox + 7, oy + 88.5, 32, 6.5)
rect(c, ox + 3, oy + 9.5, 47.5, 76, 0.2, GRAY)
for x, y in ((10, 40), (10, 55)):
    circle(c, ox + x, oy + 6.5 + y, 3)
    circle(c, ox + x, oy + 6.5 + y, 5.6, 0.18, BLUE)
# slot at right wall
rect(c, ox + 49.5, oy + 6.5 + 67, 4.0, 6.0, 0.25, BLUE)
dim_h(c, ox, ox + 53.5, oy - 8, '53,5')
dim_v(c, ox - 10, oy + 6.5, oy + 88.5, '82')
dim_v(c, ox + 63, oy, oy + 95, '95')
# side view
sx, sy = 145, 92
rect(c, sx, sy, 95, 14)
dim_h(c, sx, sx + 95, sy - 8, '95')
dim_v(c, sx + 105, sy, sy + 14, '14')
txt(c, 145, 125, 'Verbreiterung erfolgt nur nach rechts.', 8, bold=True)
txt(c, 145, 117, 'Sensorbohrungen bleiben relativ zur linken Kante.', 7.5)
txt(c, 145, 109, 'Kabelschlitz wandert mit der neuen rechten Wand.', 7.5)
finish(c)

# 7 P04 gasket
header(c, 'P04 - Haubendichtung TPU95A / D-Profil und Nut', 7,
       'eSUN eTPU-95A; flache Unterseite, gerundete Oberseite, abgerundete Ecken')
ox, oy = 55, 55
w = C.P04['x'][1] - C.P04['x'][0]
h = C.P04['y'][1] - C.P04['y'][0]
rect(c, ox, oy, w, h, radius=4)
rect(c, ox + 3, oy + 3, w - 6, h - 6, radius=1)
rect(c, ox + 3, oy + (C.P04['bar_y'][0] - C.P04['y'][0]), w - 6, 3)
dim_h(c, ox, ox + w, oy - 8, f'{w:.1f}'.replace('.', ','))
dim_v(c, ox - 10, oy, oy + h, '82')
# Section D profile + groove
sx, sy = 145, 98
rect(c, sx, sy, 70, 8, fill=HexColor('#d9dde1'))
rect(c, sx + 25, sy, 3.4, 0.6, fill=HexColor('#ffffff'))
# D profile schematic
c.setFillColor(HexColor('#88c6d9'))
c.roundRect(xpt(sx + 25.2), xpt(sy + 0.2), xpt(3.0), xpt(2.0), xpt(0.9), stroke=1, fill=1)
txt(c, 145, 125, 'Querschnitt:', 8, bold=True)
txt(c, 145, 118, 'Dichtung 3,0 breit x 2,0 hoch', 7.5)
txt(c, 145, 112, 'Nut 3,4 breit x 0,6 tief', 7.5)
txt(c, 145, 106, 'Soll-Verpressung P04: 25 %', 7.5)
txt(c, 12, 25, 'Dichtung wird flach ohne Support gedruckt; 100 % Fuellung empfohlen.', 7.5)
finish(c)

# 8 P05
header(c, 'P05 - Kabelstopfen / drei Ansichten', 8, 'Quader 4 x 6 x 8; unveraendert, nur mit Sensorpod verschoben')
ox, oy = 65, 95
rect(c, ox, oy, 4, 6)
dim_h(c, ox, ox + 4, oy - 8, '4')
dim_v(c, ox - 8, oy, oy + 6, '6')
rect(c, 120, 95, 4, 8)
dim_h(c, 120, 124, 87, '4')
dim_v(c, 112, 95, 103, '8')
rect(c, 175, 95, 6, 8)
dim_h(c, 175, 181, 87, '6')
dim_v(c, 167, 95, 103, '8')
txt(c, 64, 112, 'Draufsicht', 7.5)
txt(c, 117, 112, 'Vorderansicht', 7.5)
txt(c, 173, 112, 'Seitenansicht', 7.5)
finish(c)

# 9 hood
header(c, 'P07 - Kalibrierhaube / Draufsicht und Laengsansicht', 9,
       'Mit Sensorgruppe +20 mm verschoben und 8 mm nach rechts verbreitert')
ox, oy = 55, 43
rect(c, ox, oy, 56, 105.6)
rect(c, ox + 10, oy + 14, 48, 94)
for name, (x, y) in C.HOOD_PORTS.items():
    lx = x - C.HOOD_PLATE[0]
    ly = y - C.HOOD_PLATE[2]
    circle(c, ox + lx, oy + ly, 8)
    txt(c, ox + lx + 8, oy + ly, name, 7, bold=True)
dim_h(c, ox, ox + 56, oy - 8, '56')
dim_v(c, ox - 10, oy, oy + 105.6, '105,6')
# side view simplified
sx, sy = 145, 75
rect(c, sx, sy, 105.6, 3)
line(c, sx + 10, sy + 3, sx + 18, sy + 25)
line(c, sx + 95.6, sy + 3, sx + 87.6, sy + 25)
line(c, sx + 18, sy + 25, sx + 87.6, sy + 25)
# nozzles
for xx in (sx + 30, sx + 75):
    rect(c, xx, sy + 25, 8, 4)
    rect(c, xx + 0.5, sy + 29, 7, 4)
    rect(c, xx + 1, sy + 33, 6, 5)
dim_h(c, sx, sx + 105.6, sy - 8, '105,6')
dim_v(c, sx + 114, sy, sy + 41, '41')
txt(c, 145, 126, 'Markierungen IN / OUT auf dem Haubendach angepasst.', 7.5)
finish(c)

# 10 P08
header(c, 'P08 - Pod-Deckeldichtung TPU95A / D-Profil und Nut', 10,
       'Aussenkontur folgt dem verbreiterten Sensorpod; Nut auf Deckelunterseite')
ox, oy = 55, 55
w = C.P08['x'][1] - C.P08['x'][0]
h = C.P08['y'][1] - C.P08['y'][0]
rect(c, ox, oy, w, h, radius=4)
rect(c, ox + 3, oy + 3, w - 6, h - 6, radius=1)
dim_h(c, ox, ox + w, oy - 8, f'{w:.1f}'.replace('.', ','))
dim_v(c, ox - 10, oy, oy + h, '82')
# Section
sx, sy = 145, 98
rect(c, sx, sy, 70, 8, fill=HexColor('#d9dde1'))
rect(c, sx + 25, sy + 7.4, 3.4, 0.6, fill=HexColor('#ffffff'))
c.setFillColor(HexColor('#88c6d9'))
c.roundRect(xpt(sx + 25.2), xpt(sy + 6.0), xpt(3.0), xpt(2.0), xpt(0.9), stroke=1, fill=1)
txt(c, 145, 125, 'Querschnitt Deckelunterseite:', 8, bold=True)
txt(c, 145, 118, 'Dichtung 3,0 breit x 2,0 hoch', 7.5)
txt(c, 145, 112, 'Nut 3,4 breit x 0,6 tief', 7.5)
txt(c, 145, 106, 'Soll-Verpressung P08: 20 %', 7.5)
txt(c, 12, 25, 'Prototyp nach Montage auf Dichtheit pruefen; FDM-TPU ist nicht automatisch gasdicht.', 7.5)
finish(c)

c.save()
print(OUT)
