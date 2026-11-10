"""AirMonitor Compact V0.3 – zentrale Parameter (mm).

Wird von build_compact_revision.py (CadQuery) und check_clearances.py (ohne CAD-Kern)
gemeinsam genutzt. Koordinaten global: Ursprung äussere untere Ecke P01, X lang, Y kurz, Z hoch.
Änderungen gegenüber V0.2 sind mit "V0.3:" markiert.
"""

# ---------- Gehäuse P01 ----------
L, W, H = 208.0, 112.0, 55.0
WALL = FLOOR = 2.8
FLANGE = 10.0
OPEN_X0, OPEN_X1, OPEN_Z = 36.6, 158.6, 12.0
WALL_MOUNT_HOLES = [(37.0, -5.0), (37.0, W + 5.0), (L - 37.0, -5.0), (L - 37.0, W + 5.0)]
WALL_MOUNT_D = 4.5

# V0.3: Deckelschraubbossen links nach aussen (7,0), rechts nach X 190,0
#       (frei von Waveshare-Träger, Tasterplatine und DC5521); Oberkante bündig Z 55,0.
LID_BOSSES = [(7.0, 7.0), (7.0, W - 7.0), (190.0, 8.0), (190.0, W - 8.0)]
LID_BOSS_D, LID_BOSS_PILOT_D = 9.0, 2.5

# Waveshare (unverändert)
STANDOFFS = [(20.0, 21.0), (175.0, 21.0), (20.0, 91.0), (175.0, 91.0)]
STANDOFF_D, STANDOFF_PILOT_D = 9.0, 2.5
BOARD_BOTTOM_Z, BOARD_TOP_Z = 9.6, 27.6
CARRIER = (10.0, 185.0, 11.0, 101.0, 9.6, 27.6)  # xmin,xmax,ymin,ymax,zmin,zmax

# Rechte Stirnwand
DC5521 = (15.0, 27.5, 11.2)  # y, z, d (unverändert)
# V0.3: Tasterplatine 2,0 nach -Y (frei von Rückwand), ZERO/SPAN mitgezogen
ZERO = (48.0, 28.0, 3.0)
SPAN = (64.0, 28.0, 3.0)
BTN_HOLDER_Y = (30.0, 106.0)  # Lochbild 76,0
BTN_HOLDER_Z = (22.0, 38.0)   # Lochbild 16,0
BTN_HOLDER_D, BTN_HOLDER_PILOT_D, BTN_HOLDER_LEN = 5.0, 1.6, 6.0
BTN_PCB = (80.0, 20.0, 1.5)   # Länge (Y), Höhe (Z), Dicke (X) [gemessen]

# ---------- Deckel P02 ----------
LID_Z, LID_T = 55.0, 3.0
LID_HOLE_D, LID_CBORE_D, LID_CBORE_DEPTH = 3.3, 6.2, 1.8
VENTS = [(12.0, 23.0 + 8.0 * i, 33.0, 4.0) for i in range(9)]  # x, y, lx, ly
# V0.3: Haube wird in Deckel geschraubt (Pilot + Bosse unten), statt Durchgangsloch ohne Gegenstück
HOOD_SCREWS = [(27.0, 10.0), (27.0, 104.0)]
HOOD_SCREW_PILOT_D = 1.8          # M2 selbstschneidend [Entscheidung, Insert offen]
HOOD_SCREW_BOSS_D, HOOD_SCREW_BOSS_Z0 = 6.0, 53.0

# V0.3: Pod-Befestigung ausserhalb von Pod-Wand und P08-Dichtlinie
POD_MOUNTS = [(16.0, 12.0), (42.0, 12.0), (16.0, 102.0), (42.0, 102.0)]
POD_BOSS_D, POD_BOSS_Z0 = 7.0, 52.0        # Bosse Z 52,0…55,0
POD_BOSS_PILOT_D, POD_BOSS_PILOT_TOP = 2.5, 56.0

# ---------- Sensorpod P03 ----------
POD = (6.0, 51.5, 16.0, 98.0, 40.0, 54.0)  # Aussenkörper
POD_WALL = 3.0
SENSOR_BOSSES = [(16.3, 49.5), (16.3, 64.5)]
SENSOR_BOSS_D, SENSOR_HOLE_D, SENSOR_BOSS_TOP = 5.6, 3.0, 46.0
GRAVITY_SLOT = (47.5, 52.0, 83.0, 89.0, 46.0, 54.5)
# V0.3: Montagezungen tiefer (Z 50,0…52,0) und bis Y 9,5 / 104,5, X 13,0…45,0
TONGUE_X = (13.0, 45.0)
TONGUE_Z = (50.0, 52.0)
TONGUE_FRONT_Y = (9.5, 16.0)
TONGUE_BACK_Y = (98.0, 104.5)
TONGUE_HOLE_D = 3.0

# ---------- Dichtungen ----------
# V0.3: P08 1,3 dick im Spalt 1,0 -> 23 % Verpressung (frei modelliert, 0,3 Überdeckung mit Deckel)
P08 = dict(x=(6.0, 51.5), y=(16.0, 98.0), z0=54.0, t=1.3, web=3.0)
# V0.3: P04 mit Quersteg (zwei Fenster) unter dem Haubentrennsteg; Haube 0,9 über Deckel -> 25 %
P04 = dict(x=(6.0, 50.0), y=(16.0, 98.0), z0=58.0, t=1.2, web=2.0, bar_y=(51.5, 54.5))

# ---------- Kabelstopfen P05 ----------
# V0.3: volle Durchlasshöhe Z 46,0…54,0
P05 = (47.5, 51.5, 83.0, 89.0, 46.0, 54.0)

# ---------- Kalibrierhaube P07 ----------
HOOD_Z0 = LID_Z + LID_T + 0.9          # V0.3: 58,9 statt 58,15 (P04-Verpressung 25 %)
HOOD_PLATE = (4.0, 52.0, 4.2, 109.8)   # Flansch 48,0 × 105,6
HOOD_PLATE_T = 3.0
HOOD_CENTER = (28.0, 57.0)
HOOD_OUT = ((40.0, 94.0), (28.0, 70.0), 22.0)   # unten, oben, Höhe (ab Plattenoberkante)
HOOD_IN = ((35.0, 89.0), (23.0, 65.0), 20.2)    # ab Plattenoberkante - 0,2
HOOD_ROOF = (14.0, 22.0, 28.0, 70.0, 3.0)
# V0.3: Bodenöffnung über Schlitzfeld (innerhalb P04-Fenster), Trennsteg über Steg Y 51…55
HOOD_FLOOR_OPEN = (10.5, 45.5, 18.5, 95.5)
HOOD_DIVIDER_Y = (51.5, 54.5)
HOOD_PORTS = {'IN': (20.0, 30.0), 'OUT': (36.0, 86.0)}
HOOD_PORT_D = 2.0
HOOD_NOZZLE = [(8.0, 4.0), (7.0, 4.0), (6.0, 5.0)]

# ---------- Kaufteil-Dummys (Referenz) ----------
SEN_PCB = (12.8, 44.8, 46.0, 68.0, 46.0, 47.6)
SEN_TOP = (22.3, 35.3, 52.0, 62.0, 47.6, 50.0)
SEN_CON = (36.0, 44.0, 48.0, 56.0, 47.6, 54.4)
# V0.3: Tasterplatine als Dummy [Annahme: symmetrisch zum Lochbild]
BTN_PCB_DUMMY = (L - WALL - BTN_HOLDER_LEN - BTN_PCB[2], L - WALL - BTN_HOLDER_LEN,
                 sum(BTN_HOLDER_Y) / 2 - BTN_PCB[0] / 2, sum(BTN_HOLDER_Y) / 2 + BTN_PCB[0] / 2,
                 sum(BTN_HOLDER_Z) / 2 - BTN_PCB[1] / 2, sum(BTN_HOLDER_Z) / 2 + BTN_PCB[1] / 2)
