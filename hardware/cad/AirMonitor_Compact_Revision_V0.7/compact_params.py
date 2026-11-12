"""Laminar AirMonitor HCHO - Compact V0.7 corrected parameters (mm).

Current V0.7 state:
- sensor/calibration group keeps the proven V0.6 X position;
- complete group is centred on enclosure Y=56.0;
- sensor pod is 8.0 mm wider on the right/cable side;
- purchased EPDM 70 Shore A O-rings replace printed TPU seals;
- ZERO/SPAN PCB assembly is moved 15.0 mm downward as one rigid group;
- P02 is a short-travel sliding lid: place at +8 mm X, lower, slide 8 mm
  toward -X, and the front spring tongue snaps over a detent pin;
- the lid upper face has no protruding closure hardware and is the print-bed face.

Global coordinates: origin = outer lower corner of P01 without flange,
X = long axis, Y = short axis, Z = upward.
"""

# ---------- Main enclosure P01 ----------
L, W, H = 208.0, 112.0, 55.0
WALL = FLOOR = 2.8
FLANGE = 10.0
OPEN_X0, OPEN_X1, OPEN_Z = 36.6, 158.6, 12.0
WALL_MOUNT_HOLES = [(37.0, -5.0), (37.0, W + 5.0),
                    (L - 37.0, -5.0), (L - 37.0, W + 5.0)]
WALL_MOUNT_D = 4.5

# Existing corner supports remain, but no lid screws are used in V0.7.
LID_SUPPORTS = [(7.0, 7.0), (7.0, W - 7.0),
                (L - 7.0, 7.0), (L - 7.0, W - 7.0)]
LID_SUPPORT_D = 9.0

# Four mushroom studs retain the lid in blind keyhole tracks on its underside.
SLIDE_STUDS = [(75.0, 7.0), (75.0, W - 7.0),
               (170.0, 7.0), (170.0, W - 7.0)]
SLIDE_STUD_BASE_D = 8.0
SLIDE_TRAVEL = 8.0
SLIDE_OPEN_OFFSET_X = 8.0
SLIDE_CLOSE_DIRECTION = '-X'
SLIDE_STEM_D, SLIDE_STEM_H = 4.0, 0.65
SLIDE_HEAD_D, SLIDE_HEAD_H = 7.0, 0.75
SLIDE_HEAD_CLEAR_D = 7.6
SLIDE_STEM_CLEAR_W = 4.6
SLIDE_POCKET_DEPTH = 1.65
SLIDE_THROAT_DEPTH = 0.75

# Snap tongue is cut into the front edge of P02. It remains flush on top.
LATCH_TONGUE_X = (110.0, 132.0)   # free end at X=110, root at X=132
LATCH_TONGUE_Y = (0.0, 10.5)
LATCH_SLOT_W = 0.9
LATCH_TONGUE_SKIN = 1.20
LATCH_HOLE = (116.0, 2.2, 3.4)     # x, y, diameter through tongue
LATCH_PIN = (116.0, 2.2)           # x, y on top of front long wall
LATCH_PIN_SEGMENTS = [(3.0, 0.8), (2.2, 0.7), (1.2, 0.7)]  # d, h

# Waveshare mounting retained from approved correction.
STANDOFFS = [(24.0, 25.0), (169.0, 25.0),
             (24.0, 87.0), (169.0, 87.0)]
STANDOFF_D, STANDOFF_PILOT_D = 9.0, 2.5
BOARD_BOTTOM_Z, BOARD_TOP_Z = 9.6, 27.6
CARRIER = (10.0, 185.0, 11.0, 101.0, 9.6, 27.6)
PCB_WAVESHARE = (20.6, 172.4, 11.0, 101.0, 9.6, 11.2)

# ---------- Right end wall: ZERO / SPAN ----------
# Entire PCB, both switches, all four holders and both service holes moved -15 mm in Z.
BTN_ASSEMBLY_DZ = -15.0
BTN_HOLDER_Y = (18.0, 94.0)
BTN_HOLDER_Z = (20.0, 36.0)
BTN_HOLDER_D, BTN_HOLDER_PILOT_D, BTN_HOLDER_LEN = 5.0, 1.6, 6.0
BTN_PCB = (80.0, 20.0, 1.5)
ZERO = (36.0, 26.0, 3.0)
SPAN = (52.0, 26.0, 3.0)
BTN_MARK_Z = 32.5

# ---------- Left end wall: DC5521 ----------
DC5521 = (44.0, 27.5, 11.2)
DC_WALL = 'left'

# Markings (debossed)
MARK_DEPTH = 0.35
MARK_FONT = 'DejaVu Sans'
MARK_FONT_SIZE = 3.8

# ---------- Lid P02 ----------
LID_Z, LID_T = 55.0, 3.0
LID_TOP_FACE_FLAT = True
LID_PRINT_TOP_FACE_DOWN = True

# Sensor/calibration group remains at V0.6 X and is centred only in Y.
SENSOR_DX = 0.0
SENSOR_DY = -1.0
POD_EXTRA_X = 8.0
VENTS = [(12.0, 22.0 + 8.0 * i, 33.0, 4.0) for i in range(9)]
HOOD_SCREWS = [(27.0, 9.0), (27.0, 103.0)]
HOOD_SCREW_PILOT_D = 1.8
HOOD_SCREW_BOSS_D, HOOD_SCREW_BOSS_Z0 = 6.0, 53.0

POD_MOUNTS = [(16.0, 11.0), (42.0, 11.0),
              (16.0, 101.0), (42.0, 101.0)]
POD_BOSS_D, POD_BOSS_Z0 = 7.0, 52.0
POD_BOSS_PILOT_D, POD_BOSS_PILOT_TOP = 2.5, 56.0

# ---------- Sensor pod P03 ----------
POD = (6.0, 59.5, 15.0, 97.0, 40.0, 54.0)
POD_WALL = 3.0
POD_SEAL_RIM_TOP = 55.0
SENSOR_BOSSES = [(16.3, 48.5), (16.3, 63.5)]
SENSOR_BOSS_D, SENSOR_HOLE_D, SENSOR_BOSS_TOP = 5.6, 3.0, 46.0
GRAVITY_SLOT = (55.5, 60.0, 82.0, 88.0, 46.0, 54.0)
TONGUE_X = (13.0, 45.0)
TONGUE_Z = (50.0, 52.0)
TONGUE_FRONT_Y = (8.5, 15.0)
TONGUE_BACK_Y = (97.0, 103.5)
TONGUE_HOLE_D = 3.0

# ---------- Purchased EPDM O-rings and grooves ----------
ORING_MATERIAL = 'EPDM 70 Shore A'
ORING_SUPPLIER = 'REAflon Switzerland'
ORING_CORD = 1.50
ORING_GROOVE_W = 1.80
ORING_GROOVE_D = 1.10
ORING_COMPRESSION = (ORING_CORD - ORING_GROOVE_D) / ORING_CORD
ORING_CORNER_R = 8.0

P04A_RING = dict(name='P04A', id=45.0, cord=ORING_CORD,
                 cx=32.0, cy=33.5, cw=46.0, ch=34.0, r=8.0,
                 sku='H48761')
P04B_RING = dict(name='P04B', id=50.0, cord=ORING_CORD,
                 cx=32.0, cy=74.5, cw=45.8, ch=42.0, r=8.0,
                 sku='H96773')
P08_RING = dict(name='P08', id=77.0, cord=ORING_CORD,
                cx=32.75, cy=56.0, cw=51.2, ch=79.0, r=8.0,
                sku='H48789')

# ---------- Cable stop P05 ----------
P05 = (55.5, 59.5, 82.0, 88.0, 46.0, 54.0)

# ---------- Calibration hood P07 ----------
HOOD_Z0 = LID_Z + LID_T
HOOD_PLATE = (4.0, 60.0, 3.2, 108.8)
HOOD_PLATE_T = 3.0
HOOD_CENTER = (32.0, 56.0)
HOOD_OUT = ((48.0, 94.0), (36.0, 70.0), 22.0)
HOOD_IN = ((43.0, 89.0), (31.0, 65.0), 20.2)
HOOD_ROOF = (14.0, 21.0, 36.0, 70.0, 3.0)
HOOD_FLOOR_OPEN = (10.5, 53.5, 17.5, 94.5)
HOOD_DIVIDER_Y = (49.5, 54.5)
HOOD_PORTS = {'IN': (20.0, 29.0), 'OUT': (36.0, 85.0)}
HOOD_PORT_D = 2.0
HOOD_NOZZLE = [(8.0, 4.0), (7.0, 4.0), (6.0, 5.0)]

# ---------- Purchased-part reference dummies ----------
SEN_PCB = (12.8, 44.8, 45.0, 67.0, 46.0, 47.6)
SEN_TOP = (22.3, 35.3, 51.0, 61.0, 47.6, 50.0)
SEN_CON = (36.0, 44.0, 47.0, 55.0, 47.6, 54.4)
BTN_PCB_DUMMY = (L - WALL - BTN_HOLDER_LEN - BTN_PCB[2],
                 L - WALL - BTN_HOLDER_LEN,
                 sum(BTN_HOLDER_Y) / 2 - BTN_PCB[0] / 2,
                 sum(BTN_HOLDER_Y) / 2 + BTN_PCB[0] / 2,
                 sum(BTN_HOLDER_Z) / 2 - BTN_PCB[1] / 2,
                 sum(BTN_HOLDER_Z) / 2 + BTN_PCB[1] / 2)
