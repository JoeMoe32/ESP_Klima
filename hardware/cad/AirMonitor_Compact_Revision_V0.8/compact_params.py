"""Laminar AirMonitor HCHO - Compact V0.8 parameters (mm).

V0.8 keeps the confirmed electronics, micro-switch and calibration-station
geometry. Only the lid retention is revised again:
- rounded outer housing and 10 mm overlapping cap remain;
- the 8 mm captured slide function from the earlier V0.8 is retained;
- all four guide points stay in the outer edge zones at X=18 and X=190;
- the enclosure centre contains no lid guides, posts or latch parts;
- the former rectangular C-window is replaced by a blind internal keyhole
  track with a 45-degree diagonal cross-section;
- the lid exterior remains closed and visually flush;
- entry pockets are open only toward the inside and lower skirt edge;
- a hidden detent at the front/right guide provides the end snap;
- P01 prints on its floor and P02 on its visible top without slicer supports.

Global coordinates: origin = outer lower corner of P01 without flange,
X = long axis, Y = short axis, Z = upward.
"""

# ---------- Main enclosure P01 ----------
L, W, H = 208.0, 112.0, 55.0
WALL = FLOOR = 3.2
FLANGE = 10.0
BODY_CORNER_R = 6.0
SHOULDER_Z0 = 45.0
SHOULDER_H = H - SHOULDER_Z0
SHOULDER_INSET = 2.8
SHOULDER_CORNER_R = 3.2
NO_LID_COLUMNS = True
NO_CENTER_FIXINGS = True

OPEN_X0, OPEN_X1 = 36.6, 158.6
OPEN_Z, OPEN_TOP_Z = 12.0, SHOULDER_Z0
WALL_MOUNT_HOLES = [(37.0, -5.0), (37.0, W + 5.0),
                    (L - 37.0, -5.0), (L - 37.0, W + 5.0)]
WALL_MOUNT_D = 4.5

# Waveshare mounting retained from V0.7.
STANDOFFS = [(24.0, 25.0), (169.0, 25.0),
             (24.0, 87.0), (169.0, 87.0)]
STANDOFF_D, STANDOFF_PILOT_D = 9.0, 2.5
BOARD_BOTTOM_Z, BOARD_TOP_Z = 9.6, 27.6
CARRIER = (10.0, 185.0, 11.0, 101.0, 9.6, 27.6)
PCB_WAVESHARE = (20.6, 172.4, 11.0, 101.0, 9.6, 11.2)

# Edge-only, captured 45-degree slide guides.
# The user-visible motion remains the earlier 8 mm slide. The guide tongue is
# diagonal in Y/Z, and the matching track is blind from the outside. This keeps
# the lid captured while avoiding a horizontal C-channel roof.
SLIDE_TRAVEL = 8.0
SLIDE_OPEN_OFFSET_X = 8.0
SLIDE_CLOSE_DIRECTION = '-X'
SLIDE_USER_DIRECTION = 'left-to-right in operating view'
GUIDE_MODE = 'blind internal 45-degree captured keyhole tracks at outer edges'
NO_CENTER_FIXINGS = True
NO_VISIBLE_GUIDE_WINDOWS = True
NO_HORIZONTAL_SLOT_ROOFS = True
GUIDE_PRINT_ANGLE_DEG = 45.0

# Four edge locations. The front/right location also carries the hidden detent.
GUIDE_X_FRONT = (18.0, 190.0)
GUIDE_X_REAR = (18.0, 190.0)
GUIDE_X_ALL = (18.0, 190.0)
GUIDE_LUG_W = 6.0
GUIDE_ROOT_Z0 = 46.8
GUIDE_ROOT_Z1 = 49.8
GUIDE_PROJ = 0.90
GUIDE_RISE = 0.90

# Blind groove on the inside of the 2.6 mm skirt. The groove is a diagonal
# parallelogram, not a rectangular tunnel. The outside skin remains closed.
GUIDE_GROOVE_INNER_Y_FRONT = 2.75
GUIDE_GROOVE_OUTER_Y_FRONT = 1.60
GUIDE_GROOVE_RISE = 1.15
GUIDE_GROOVE_Z0 = 46.4
GUIDE_GROOVE_Z1 = 50.2
GUIDE_OUTER_SKIN = 1.60
GUIDE_ENTRY_OUTER_SKIN = 1.15
GUIDE_ENTRY_W = 7.60
GUIDE_ENTRY_BOTTOM_Z = 44.60
GUIDE_ENTRY_TOP_Z = 55.20
GUIDE_TRACK_END_EXTRA = 3.80

# Hidden end detent at the front/right guide. The enlarged lug flexes the front
# skirt by about 0.20 mm while sliding, then relaxes in the deeper final pocket.
SNAP_X = 190.0
SNAP_EXTRA_PROJ = 0.55
SNAP_DETENT_EXTRA_DEPTH = 0.40
SNAP_DETENT_W = 6.40
SNAP_INTERFERENCE = 0.20
SNAP_FINAL_CLEARANCE = 0.20
NO_TOP_LATCH_TONGUE = True

# ---------- Right end wall: ZERO / SPAN ----------
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

# ---------- Cap lid P02 ----------
LID_Z, LID_T = 55.0, 3.0
LID_OVERLAP = 10.0
LID_OUTSET = 0.0
LID_X0, LID_X1 = -LID_OUTSET, L + LID_OUTSET
LID_Y0, LID_Y1 = -LID_OUTSET, W + LID_OUTSET
LID_CORNER_R = 6.0
LID_SKIRT_W = 2.5
LID_LEFT_END_OPEN = True
LID_IN_X0, LID_IN_X1 = LID_X0 + LID_SKIRT_W, LID_X1 - LID_SKIRT_W
LID_IN_Y0, LID_IN_Y1 = LID_Y0 + LID_SKIRT_W, LID_Y1 - LID_SKIRT_W
LID_TOP_FACE_FLAT = True
LID_PRINT_TOP_FACE_DOWN = True

# Sensor/calibration group remains at the confirmed V0.7 position.
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
