"""AirMonitor Compact V0.6 – zentrale Parameter (mm).

Basis ist die technisch geprüfte V0.3-Geometrie. V0.6 korrigiert nur die
rechte Rückwand:

- Nicht ZERO/SPAN werden auf der Wand zentriert, sondern die komplette
  80,0 × 20,0 mm Microtaster-Platine samt vier Haltern.
- ZERO und SPAN behalten ihre gemessenen Positionen auf der Platine.
- Die DC5521-Buchse sitzt unterhalb der beiden Microtaster, mittig zwischen
  ZERO und SPAN.
- Die Halter liegen dadurch frei zwischen den beiden senkrechten
  Deckelschraubsäulen und nicht mehr hinter einer Säule.

Sensorzelle, Kalibrierhaube, Waveshare, Deckel und alle übrigen Geometrien
bleiben unverändert.

Koordinaten global: Ursprung äussere untere Ecke P01, X lang, Y kurz, Z hoch.
"""

# ---------- Gehäuse P01 ----------
L, W, H = 208.0, 112.0, 55.0
WALL = FLOOR = 2.8
FLANGE = 10.0
OPEN_X0, OPEN_X1, OPEN_Z = 36.6, 158.6, 12.0
WALL_MOUNT_HOLES = [(37.0, -5.0), (37.0, W + 5.0), (L - 37.0, -5.0), (L - 37.0, W + 5.0)]
WALL_MOUNT_D = 4.5

# Deckelschraubbossen – unverändert aus V0.3
LID_BOSSES = [(7.0, 7.0), (7.0, W - 7.0), (190.0, 8.0), (190.0, W - 8.0)]
LID_BOSS_D, LID_BOSS_PILOT_D = 9.0, 2.5

# Waveshare – unverändert
STANDOFFS = [(20.0, 21.0), (175.0, 21.0), (20.0, 91.0), (175.0, 91.0)]
STANDOFF_D, STANDOFF_PILOT_D = 9.0, 2.5
BOARD_BOTTOM_Z, BOARD_TOP_Z = 9.6, 27.6
CARRIER = (10.0, 185.0, 11.0, 101.0, 9.6, 27.6)  # xmin,xmax,ymin,ymax,zmin,zmax

# ---------- Rechte Stirnwand ----------
# V0.6: Platinenhalterung geometrisch in der 112-mm-Wand zentriert.
# Platinen-Aussenbereich: Y = 16,0…96,0 / Z = 33,0…53,0.
# Lochbild bleibt 76,0 × 16,0; Halterabstand zu beiden Deckelsäulen ist symmetrisch.
BTN_HOLDER_Y = (18.0, 94.0)  # Lochbild 76,0
BTN_HOLDER_Z = (35.0, 51.0)  # Lochbild 16,0
BTN_HOLDER_D, BTN_HOLDER_PILOT_D, BTN_HOLDER_LEN = 5.0, 1.6, 6.0
BTN_PCB = (80.0, 20.0, 1.5)  # Länge Y, Höhe Z, Dicke X [gemessen]

# ZERO/SPAN bleiben auf der Platine bei 20,0 bzw. 36,0 mm ab deren Y-Min-Kante.
# Sie werden nicht als Paar auf der Gehäusewand zentriert.
ZERO = (36.0, 41.0, 3.0)
SPAN = (52.0, 41.0, 3.0)

# V0.6: DC5521 direkt unter den beiden Microtastern, mittig zwischen ZERO/SPAN.
# Z bleibt unverändert; nur Y wird auf den Schalter-Mittelpunkt gesetzt.
DC5521 = (44.0, 27.5, 11.2)  # y, z, d

# ---------- Deckel P02 ----------
LID_Z, LID_T = 55.0, 3.0
LID_HOLE_D, LID_CBORE_D, LID_CBORE_DEPTH = 3.3, 6.2, 1.8
VENTS = [(12.0, 23.0 + 8.0 * i, 33.0, 4.0) for i in range(9)]
HOOD_SCREWS = [(27.0, 10.0), (27.0, 104.0)]
HOOD_SCREW_PILOT_D = 1.8
HOOD_SCREW_BOSS_D, HOOD_SCREW_BOSS_Z0 = 6.0, 53.0

# Pod-Befestigung – unverändert aus V0.3
POD_MOUNTS = [(16.0, 12.0), (42.0, 12.0), (16.0, 102.0), (42.0, 102.0)]
POD_BOSS_D, POD_BOSS_Z0 = 7.0, 52.0
POD_BOSS_PILOT_D, POD_BOSS_PILOT_TOP = 2.5, 56.0

# ---------- Sensorpod P03 – vollständig unverändert aus V0.3 ----------
POD = (6.0, 51.5, 16.0, 98.0, 40.0, 54.0)
POD_WALL = 3.0
SENSOR_BOSSES = [(16.3, 49.5), (16.3, 64.5)]
SENSOR_BOSS_D, SENSOR_HOLE_D, SENSOR_BOSS_TOP = 5.6, 3.0, 46.0
GRAVITY_SLOT = (47.5, 52.0, 83.0, 89.0, 46.0, 54.5)
TONGUE_X = (13.0, 45.0)
TONGUE_Z = (50.0, 52.0)
TONGUE_FRONT_Y = (9.5, 16.0)
TONGUE_BACK_Y = (98.0, 104.5)
TONGUE_HOLE_D = 3.0

# ---------- Dichtungen – unverändert ----------
P08 = dict(x=(6.0, 51.5), y=(16.0, 98.0), z0=54.0, t=1.3, web=3.0)
P04 = dict(x=(6.0, 50.0), y=(16.0, 98.0), z0=58.0, t=1.2, web=2.0, bar_y=(51.5, 54.5))

# ---------- Kabelstopfen P05 – unverändert ----------
P05 = (47.5, 51.5, 83.0, 89.0, 46.0, 54.0)

# ---------- Kalibrierhaube P07 – vollständig unverändert aus V0.3 ----------
HOOD_Z0 = LID_Z + LID_T + 0.9
HOOD_PLATE = (4.0, 52.0, 4.2, 109.8)
HOOD_PLATE_T = 3.0
HOOD_CENTER = (28.0, 57.0)
HOOD_OUT = ((40.0, 94.0), (28.0, 70.0), 22.0)
HOOD_IN = ((35.0, 89.0), (23.0, 65.0), 20.2)
HOOD_ROOF = (14.0, 22.0, 28.0, 70.0, 3.0)
HOOD_FLOOR_OPEN = (10.5, 45.5, 18.5, 95.5)
HOOD_DIVIDER_Y = (51.5, 54.5)
HOOD_PORTS = {'IN': (20.0, 30.0), 'OUT': (36.0, 86.0)}
HOOD_PORT_D = 2.0
HOOD_NOZZLE = [(8.0, 4.0), (7.0, 4.0), (6.0, 5.0)]

# ---------- Kaufteil-Dummys ----------
SEN_PCB = (12.8, 44.8, 46.0, 68.0, 46.0, 47.6)
SEN_TOP = (22.3, 35.3, 52.0, 62.0, 47.6, 50.0)
SEN_CON = (36.0, 44.0, 48.0, 56.0, 47.6, 54.4)
BTN_PCB_DUMMY = (L - WALL - BTN_HOLDER_LEN - BTN_PCB[2], L - WALL - BTN_HOLDER_LEN,
                 sum(BTN_HOLDER_Y) / 2 - BTN_PCB[0] / 2, sum(BTN_HOLDER_Y) / 2 + BTN_PCB[0] / 2,
                 sum(BTN_HOLDER_Z) / 2 - BTN_PCB[1] / 2, sum(BTN_HOLDER_Z) / 2 + BTN_PCB[1] / 2)
