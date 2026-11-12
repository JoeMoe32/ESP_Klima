"""Generate 1:1 mass sketches for AirMonitor Compact V0.7 corrected O-ring revision."""
from pathlib import Path
import math

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors

import compact_params as C

R = Path(__file__).resolve().parent
OUT = R / 'AirMonitor_V07_Massskizzen_1zu1.pdf'
PAGE = landscape(A4)
PW, PH = PAGE


def header(c, title, subtitle=''):
    c.setFont('Helvetica-Bold', 12)
    c.drawString(12*mm, PH-12*mm, 'LAMINAR | AirMonitor HCHO | V0.7')
    c.setFont('Helvetica-Bold', 10)
    c.drawString(12*mm, PH-20*mm, title)
    if subtitle:
        c.setFont('Helvetica', 7.5)
        c.drawString(12*mm, PH-26*mm, subtitle)
    c.line(12*mm, PH-29*mm, PW-12*mm, PH-29*mm)


def footer(c, page_no, note=''):
    c.setFont('Helvetica', 6.5)
    c.drawString(12*mm, 8*mm, 'A4 quer | Massstab 1:1 | Masse in mm | Druck: 100 % / Tatsaechliche Groesse')
    if note:
        c.drawCentredString(PW/2, 8*mm, note)
    c.drawRightString(PW-12*mm, 8*mm, str(page_no))
    # 50 mm control bar
    x0 = PW-72*mm; y0 = 16*mm
    c.line(x0, y0, x0+50*mm, y0)
    c.line(x0, y0-2*mm, x0, y0+2*mm)
    c.line(x0+50*mm, y0-2*mm, x0+50*mm, y0+2*mm)
    c.setFont('Helvetica', 6)
    c.drawCentredString(x0+25*mm, y0+2.5*mm, 'Kontrolle: 50 mm')


def dim_h(c, x0, x1, y, text, off=3):
    c.line(x0, y, x1, y)
    c.line(x0, y-off*mm, x0, y+off*mm)
    c.line(x1, y-off*mm, x1, y+off*mm)
    c.setFont('Helvetica', 6.5)
    c.drawCentredString((x0+x1)/2, y+2*mm, text)


def dim_v(c, x, y0, y1, text, off=3):
    c.line(x, y0, x, y1)
    c.line(x-off*mm, y0, x+off*mm, y0)
    c.line(x-off*mm, y1, x+off*mm, y1)
    c.saveState(); c.translate(x+2.5*mm, (y0+y1)/2); c.rotate(90)
    c.setFont('Helvetica', 6.5); c.drawCentredString(0, 0, text); c.restoreState()


def page1_base(c):
    header(c, 'P01 - Gehaeuseboden / Draufsicht innen',
           'Aussen 208 x 132 x 55 inkl. Flansche; Gehaeuse ohne Flansche 208 x 112')
    ox, oy = 38*mm, 39*mm
    c.rect(ox, oy-C.FLANGE*mm, C.L*mm, (C.W+2*C.FLANGE)*mm)
    c.rect(ox, oy, C.L*mm, C.W*mm)
    for x, y in C.WALL_MOUNT_HOLES:
        c.circle(ox+x*mm, oy+y*mm, C.WALL_MOUNT_D/2*mm)
    for x, y in C.LID_BOSSES:
        c.circle(ox+x*mm, oy+y*mm, C.LID_BOSS_D/2*mm)
        c.circle(ox+x*mm, oy+y*mm, C.LID_BOSS_PILOT_D/2*mm)
    c.setStrokeColor(colors.darkblue)
    for x, y in C.STANDOFFS:
        c.circle(ox+x*mm, oy+y*mm, C.STANDOFF_D/2*mm)
        c.circle(ox+x*mm, oy+y*mm, C.STANDOFF_PILOT_D/2*mm)
    c.setStrokeColor(colors.black)
    dim_h(c, ox, ox+C.L*mm, oy-17*mm, '208')
    dim_v(c, ox+C.L*mm+9*mm, oy-C.FLANGE*mm, oy+(C.W+C.FLANGE)*mm, '132')
    c.setFont('Helvetica', 7)
    c.drawString(12*mm, 22*mm, 'Waveshare-Pilotloecher: XY (24/25), (169/25), (24/87), (169/87); Raster 145 x 62.')
    c.drawString(12*mm, 18*mm, 'Deckelbossen: XY (7/7), (7/105), (201/7), (201/105). Boden/Waende 2,8.')
    footer(c, 1)


def page2_walls(c):
    header(c, 'P01 - Laengswand / Seitenansicht',
           'Beide Laengswaende: Ausschnitt 122 breit x 43 hoch; Unterkante Z=12')
    ox, oy = 38*mm, 55*mm
    c.rect(ox, oy, C.L*mm, C.H*mm)
    c.rect(ox+C.OPEN_X0*mm, oy+C.OPEN_Z*mm,
           (C.OPEN_X1-C.OPEN_X0)*mm, (C.H-C.OPEN_Z)*mm)
    dim_h(c, ox, ox+C.L*mm, oy-12*mm, '208')
    dim_h(c, ox+C.OPEN_X0*mm, ox+C.OPEN_X1*mm, oy+C.H*mm+8*mm, '122')
    dim_v(c, ox+C.L*mm+8*mm, oy, oy+C.H*mm, '55')
    c.setFont('Helvetica', 7)
    c.drawString(12*mm, 25*mm, 'Beginn X=36,6; Ende X=158,6; Unterkante Z=12,0. Wand 2,8; Boden 2,8.')
    footer(c, 2)


def page3_endwalls(c):
    header(c, 'P01 - Stirnwaende',
           'Rechts ZERO/SPAN; links DC5521 und 24 V DC')
    # Right wall outside
    ox, oy = 25*mm, 60*mm
    c.setFont('Helvetica-Bold', 8); c.drawString(ox, oy+62*mm, 'Rechte Stirnwand / Aussenansicht')
    c.rect(ox, oy, C.W*mm, C.H*mm)
    for label, (y,z,d) in [('ZERO', C.ZERO), ('SPAN', C.SPAN)]:
        c.circle(ox+y*mm, oy+z*mm, d/2*mm)
        c.setFont('Helvetica', 6); c.drawCentredString(ox+y*mm, oy+(z+5)*mm, label)
    # Left wall outside
    ox2 = 160*mm
    c.setFont('Helvetica-Bold', 8); c.drawString(ox2, oy+62*mm, 'Linke Stirnwand / Aussenansicht')
    c.rect(ox2, oy, C.W*mm, C.H*mm)
    y,z,d = C.DC5521
    c.circle(ox2+y*mm, oy+z*mm, d/2*mm)
    c.setFont('Helvetica', 6.5); c.drawCentredString(ox2+y*mm, oy+(z+9)*mm, '24 V DC')
    c.drawString(ox2+82*mm, oy+7*mm, 'V0.7')
    c.setFont('Helvetica', 7)
    c.drawString(12*mm, 28*mm, 'ZERO: Y=36 / Z=41 / D3. SPAN: Y=52 / Z=41 / D3. Halter-Lochbild 76 x 16.')
    c.drawString(12*mm, 23*mm, 'DC5521 links: Y=44 / Z=27,5 / D11,2. Innenansicht jeweils horizontal gespiegelt.')
    footer(c, 3)


def page4_lid(c):
    header(c, 'P02 - Deckel / Draufsicht aussen',
           'X-Position der Sensorgruppe unveraendert; komplette Gruppe auf Y=56,0 zentriert')
    scale=1.0
    ox, oy = 38*mm, 48*mm
    c.rect(ox, oy, C.L*mm, C.W*mm)
    for x,y in C.LID_BOSSES:
        c.circle(ox+x*mm, oy+y*mm, C.LID_HOLE_D/2*mm)
    c.setStrokeColor(colors.darkblue)
    for x,y,lx,ly in C.VENTS:
        c.rect(ox+x*mm, oy+y*mm, lx*mm, ly*mm)
    for x,y in C.HOOD_SCREWS:
        c.circle(ox+x*mm, oy+y*mm, 1.1*mm)
    for x,y in C.POD_MOUNTS:
        c.circle(ox+x*mm, oy+y*mm, 1.5*mm)
    c.line(ox, oy+56*mm, ox+C.L*mm, oy+56*mm)
    c.setStrokeColor(colors.black)
    c.setFont('Helvetica', 7)
    c.drawString(12*mm, 26*mm, 'Lueftungsschlitze: X=12,0; Y=22,0 + 8,0*n. Haubenschrauben: (27/9), (27/103).')
    c.drawString(12*mm, 21*mm, 'Pod-Montage: (16/11),(42/11),(16/101),(42/101). Deckel bleibt 3,0 mm voll - keine O-Ring-Nuten im Deckel.')
    footer(c, 4)


def page5_pod(c):
    header(c, 'P03 - Sensorpod / Draufsicht innen',
           'V0.6-X-Lage beibehalten; rechts 8,0 mm breiter; Dichtnut im erhoehten Rand')
    ox, oy = 45*mm, 45*mm
    w=(C.POD[1]-C.POD[0]); h=(C.POD[3]-C.POD[2])
    c.rect(ox, oy, w*mm, h*mm)
    c.rect(ox+C.POD_WALL*mm, oy+C.POD_WALL*mm,
           (w-2*C.POD_WALL)*mm, (h-2*C.POD_WALL)*mm)
    # P08 groove centerline and channel envelope
    r=C.P08_RING
    gx=ox+(r['cx']-C.POD[0]-r['cw']/2)*mm
    gy=oy+(r['cy']-C.POD[2]-r['ch']/2)*mm
    c.setStrokeColor(colors.red)
    c.roundRect(gx, gy, r['cw']*mm, r['ch']*mm, r['r']*mm)
    c.setStrokeColor(colors.black)
    for x,y in C.SENSOR_BOSSES:
        c.circle(ox+(x-C.POD[0])*mm, oy+(y-C.POD[2])*mm, C.SENSOR_HOLE_D/2*mm)
    dim_h(c, ox, ox+w*mm, oy-10*mm, f'{w:.1f}')
    dim_v(c, ox+w*mm+10*mm, oy, oy+h*mm, f'{h:.1f}')
    c.setFont('Helvetica', 7)
    c.drawString(120*mm, 120*mm, 'P08 O-Ring: EPDM 70, D77,0 x 1,50')
    c.drawString(120*mm, 114*mm, 'Nut: 1,80 breit x 1,10 tief')
    c.drawString(120*mm, 108*mm, 'Rand Z=54,0..55,0; Deckelunterseite Z=55,0')
    c.drawString(120*mm, 102*mm, 'Verpressung: 0,40 mm = 26,7 %')
    c.drawString(12*mm, 22*mm, 'Sensorbohrungen D3, Abstand 15. Kabelschlitz 4,5 x 6,0 x 8,0; oberer Dichtrand bleibt geschlossen.')
    footer(c, 5)


def page6_hood(c):
    header(c, 'P07 - Kalibrierhaube / Unterseite',
           'Zwei getrennte EPDM-O-Ringe; einer pro Kammer')
    ox, oy = 42*mm, 38*mm
    w=C.HOOD_PLATE[1]-C.HOOD_PLATE[0]; h=C.HOOD_PLATE[3]-C.HOOD_PLATE[2]
    c.rect(ox, oy, w*mm, h*mm)
    fx0,fx1,fy0,fy1=C.HOOD_FLOOR_OPEN; d0,d1=C.HOOD_DIVIDER_Y
    # openings local to hood plate
    c.rect(ox+(fx0-C.HOOD_PLATE[0])*mm, oy+(fy0-C.HOOD_PLATE[2])*mm,
           (fx1-fx0)*mm, (d0-fy0)*mm)
    c.rect(ox+(fx0-C.HOOD_PLATE[0])*mm, oy+(d1-C.HOOD_PLATE[2])*mm,
           (fx1-fx0)*mm, (fy1-d1)*mm)
    c.setStrokeColor(colors.red)
    for ring in (C.P04A_RING,C.P04B_RING):
        x=ox+(ring['cx']-C.HOOD_PLATE[0]-ring['cw']/2)*mm
        y=oy+(ring['cy']-C.HOOD_PLATE[2]-ring['ch']/2)*mm
        c.roundRect(x,y,ring['cw']*mm,ring['ch']*mm,ring['r']*mm)
    c.setStrokeColor(colors.black)
    c.setFont('Helvetica', 7)
    c.drawString(125*mm, 135*mm, 'P04A unten: EPDM 70, D45,0 x 1,50')
    c.drawString(125*mm, 128*mm, 'P04B oben: EPDM 70, D50,0 x 1,50')
    c.drawString(125*mm, 121*mm, 'Beide Nuten: 1,80 breit x 1,10 tief')
    c.drawString(125*mm, 114*mm, 'Trennsteg: 5,0 mm')
    c.drawString(125*mm, 107*mm, 'Haubenunterseite liegt plan auf Deckel')
    c.drawString(12*mm, 22*mm, 'Grundplatte 56,0 x 105,6 x 3,0. O-Ring-Nuten liegen in P07, nicht im Deckel.')
    footer(c, 6)


def page7_orings(c):
    header(c, 'Kaufteile - EPDM-O-Ringe und Nutdaten',
           'Lagernde Standardringe; keine geklebte Rundschnur im Gasweg')
    x0=18*mm; y=155*mm
    cols=[0,35,75,115,155,195]
    headers=['Pos.','Abmessung','SKU','Nut B x T','Verpressung','Verwendung']
    c.setFont('Helvetica-Bold',7)
    for i,h in enumerate(headers): c.drawString(x0+cols[i]*mm,y,h)
    c.line(x0,y-2*mm,PW-18*mm,y-2*mm)
    rows=[
        ('P04A','D45,0 x 1,50','H48761','1,80 x 1,10','26,7 %','untere Kammer'),
        ('P04B','D50,0 x 1,50','H96773','1,80 x 1,10','26,7 %','obere Kammer'),
        ('P08','D77,0 x 1,50','H48789','1,80 x 1,10','26,7 %','Pod / Deckel'),
    ]
    c.setFont('Helvetica',7)
    for r,row in enumerate(rows):
        yy=y-(9+8*r)*mm
        for i,val in enumerate(row): c.drawString(x0+cols[i]*mm,yy,val)
    c.setFont('Helvetica-Bold',8); c.drawString(18*mm,105*mm,'Konstruktionshinweise')
    c.setFont('Helvetica',7)
    notes=[
        'Material: EPDM 70 Shore A, schwarz; Ring als geschlossenes Kaufteil.',
        'O-Ring-Pfade haben weniger als 0,2 % rechnerische Dehnung.',
        'Innenradien R8,0; damit deutlich groesser als 3 x Schnurstaerke.',
        'Nuten beim Epoxidieren abdecken; Harz im Nutgrund veraendert die Verpressung.',
        'Vor Installation: Sitz, Leckrate, Nullpunkt und Rueckkehr nach Pruefgas testen.',
    ]
    for i,n in enumerate(notes): c.drawString(22*mm,(96-7*i)*mm,u'• '+n)
    footer(c, 7)


def page8_p05(c):
    header(c, 'P05 - Kabelstopfen / drei Ansichten', 'Quader 4 x 6 x 8; keine Bohrungen')
    ox,oy=50*mm,85*mm
    c.rect(ox,oy,4*mm,6*mm); c.drawString(ox-5*mm,oy+10*mm,'Draufsicht 4 x 6')
    c.rect(ox+55*mm,oy,4*mm,8*mm); c.drawString(ox+45*mm,oy+12*mm,'Vorderansicht 4 x 8')
    c.rect(ox+110*mm,oy,6*mm,8*mm); c.drawString(ox+100*mm,oy+12*mm,'Seitenansicht 6 x 8')
    c.setFont('Helvetica',7)
    c.drawString(12*mm,30*mm,'Kabelschlitz endet bei Z=54,0. Der neue P08-Dichtrand Z=54,0..55,0 bleibt dadurch durchgehend.')
    footer(c, 8)


def page9_summary(c):
    header(c, 'V0.7 - Freigabe- und Pruefliste', 'Aenderungen gegenueber dem vorherigen V0.7-Stand')
    c.setFont('Helvetica-Bold',8); c.drawString(18*mm,160*mm,'Umgesetzt')
    items=[
        'X-Lage der Sensor-/Kalibriereinheit auf V0.6 zurueckgesetzt.',
        'Gesamte Einheit exakt auf Y=56,0 zentriert.',
        'Pod rechts 8,0 mm breiter beibehalten.',
        'Gedruckte TPU-Dichtungen P04/P08 entfallen.',
        'Drei geschlossene EPDM-70-O-Ringe als Kaufteile vorgesehen.',
        'P04-Nuten in P07; P08-Nut im erhoehten P03-Rand; Deckel bleibt vollstaendig 3,0 mm dick.',
        'ZERO, SPAN, 24 V DC, V0.7, IN und OUT bleiben markiert.',
    ]
    c.setFont('Helvetica',7)
    for i,t in enumerate(items): c.drawString(22*mm,(151-8*i)*mm,u'• '+t)
    c.setFont('Helvetica-Bold',8); c.drawString(18*mm,82*mm,'Vor Montage pruefen')
    checks=[
        'Alle drei O-Ringe liegen ohne Verdrehung und ohne Ausbeulung in den Nuten.',
        'Haube und Deckel schliessen plan; Schrauben gleichmaessig anziehen.',
        'Gravity-Kabel und Kabelstopfen sitzen, ohne den P08-Ring zu unterbrechen.',
        'Lecktest mit Nullgas/Frischluft und anschliessend Pruefgas durchfuehren.',
        'Nach dem Pruefgas Rueckkehr zum Nullpunkt und Totzeit dokumentieren.',
    ]
    c.setFont('Helvetica',7)
    for i,t in enumerate(checks): c.drawString(22*mm,(73-8*i)*mm,u'□ '+t)
    footer(c, 9, 'CAD-Stand: V0.7 korrigiert - EPDM-O-Ringe')


def main():
    c=canvas.Canvas(str(OUT),pagesize=PAGE)
    pages=[page1_base,page2_walls,page3_endwalls,page4_lid,page5_pod,
           page6_hood,page7_orings,page8_p05,page9_summary]
    for fn in pages:
        fn(c); c.showPage()
    c.save()
    print(OUT)


if __name__=='__main__': main()
