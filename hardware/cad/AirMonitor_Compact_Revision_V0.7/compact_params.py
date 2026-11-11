"""Laminar AirMonitor HCHO – Compact V0.7 parameters (mm).

Basis: V0.6 plus the corrections marked in AirMonitor_V06_Massskizzen_1zu1.pdf.
V0.7 changes:
- Waveshare standoffs moved to measured coordinates X=24/169, Y=25/87.
- Right lid bosses moved to the same 7 mm edge offset as the left bosses.
- Complete sensor/calibration group moved 20 mm toward the enclosure centre (+X).
- Sensor pod widened 8 mm to the right; sensor location remains referenced to the old left edge.
- DC5521 moved from the right end wall to the opposite (left) end wall, Z unchanged.
- P04 and P08 changed from flat seals to TPU 95A D-profile seals with rounded plan corners.
- Matching 0.6 mm locating grooves are cut into the lid on both sides.
- External markings updated: ZERO, SPAN, 24 V DC and V0.7.

Global coordinates: origin = outer lower corner of P01 without flange,
X = long axis, Y = short axis, Z = upward.
"""

# ---------- Main enclosure P01 ----------
L, W, H = 208.0, 112.0, 55.0
WALL = FLOOR = 2.8
FLANGE = 10.0
OPEN_X0, OPEN_X1, OPEN_Z = 36.6, 158.6, 12.0
WALL_MOUNT_HOLES = [(37.0, -5.0), (37.0, W + 5.0), (L - 37.0, -5.0), (L - 37.0, W + 5.0)]
WALL_MOUNT_D = 4.5

# V0.7: both right bosses mirror the left 7 mm edge offset.
LID_BOSSES = [(7.0, 7.0), (7.0, W - 7.0), (L - 7.0, 7.0), (L - 7.0, W - 7.0)]
LID_BOSS_D, LID_BOSS_PILOT_D = 9.0, 2.5

# V0.7: measured mounting coordinates from annotated 1:1 sketch.
STANDOFFS = [(24.0, 25.0), (169.0, 25.0), (24.0, 87.0), (169.0, 87.0)]
STANDOFF_D, STANDOFF_PILOT_D = 9.0, 2.5
BOARD_BOTTOM_Z, BOARD_TOP_Z = 9.6, 27.6
# Overall component envelope retained until Daniel verifies the physical board.
CARRIER = (10.0, 185.0, 11.0, 101.0, 9.6, 27.6)
# Measured board body 151.8 x 90; hole offsets derived from the new standoff coordinates.
PCB_WAVESHARE = (20.6, 172.4, 11.0, 101.0, 9.6, 11.2)

# ---------- Right end wall: ZERO / SPAN only ----------
BTN_HOLDER_Y = (18.0, 94.0)  # 76.0 mm pattern
BTN_HOLDER_Z = (35.0, 51.0)  # 16.0 mm pattern
BTN_HOLDER_D, BTN_HOLDER_PILOT_D, BTN_HOLDER_LEN = 5.0, 1.6, 6.0
BTN_PCB = (80.0, 20.0, 1.5)  # Y length, Z height, X thickness [measured]
ZERO = (36.0, 41.0, 3.0)
SPAN = (52.0, 41.0, 3.0)

# ---------- Left end wall: DC5521 ----------
# V0.7: opposite end wall, same height as V0.6.
DC5521 = (44.0, 27.5, 11.2)  # y, z, diameter
DC_WALL = 'left'

# Markings (debossed)
MARK_DEPTH = 0.35
MARK_FONT = 'DejaVu Sans'
MARK_FONT_SIZE = 3.8

# ---------- Lid P02 ----------
LID_Z, LID_T = 55.0, 3.0
LID_HOLE_D, LID_CBORE_D, LID_CBORE_DEPTH = 3.3, 6.2, 1.8

# V0.7 complete sensor group moved +20 mm in X.
SENSOR_DX = 20.0
POD_EXTRA_X = 8.0
VENTS = [(32.0, 23.0 + 8.0 * i, 33.0, 4.0) for i in range(9)]
HOOD_SCREWS = [(47.0, 10.0), (47.0, 104.0)]
HOOD_SCREW_PILOT_D = 1.8
HOOD_SCREW_BOSS_D, HOOD_SCREW_BOSS_Z0 = 6.0, 53.0

POD_MOUNTS = [(36.0, 12.0), (62.0, 12.0), (36.0, 102.0), (62.0, 102.0)]
POD_BOSS_D, POD_BOSS_Z0 = 7.0, 52.0
POD_BOSS_PILOT_D, POD_BOSS_PILOT_TOP = 2.5, 56.0

# ---------- Sensor pod P03 ----------
# Old body 45.5 mm wide, moved +20 mm and widened +8 mm to the right.
POD = (26.0, 79.5, 16.0, 98.0, 40.0, 54.0)
POD_WALL = 3.0
# Sensor remains referenced to the old left edge; extra width is on connector/cable side.
SENSOR_BOSSES = [(36.3, 49.5), (36.3, 64.5)]
SENSOR_BOSS_D, SENSOR_HOLE_D, SENSOR_BOSS_TOP = 5.6, 3.0, 46.0
GRAVITY_SLOT = (75.5, 80.0, 83.0, 89.0, 46.0, 54.5)
TONGUE_X = (33.0, 65.0)
TONGUE_Z = (50.0, 52.0)
TONGUE_FRONT_Y = (9.5, 16.0)
TONGUE_BACK_Y = (98.0, 104.5)
TONGUE_HOLE_D = 3.0

# ---------- TPU D-profile seals and locating grooves ----------
TPU_MATERIAL = 'eSUN eTPU-95A'
GASKET_H = 2.0
GASKET_TOP_FILLET = 0.85
GROOVE_DEPTH = 0.6
GROOVE_CLEARANCE = 0.2
GASKET_CORNER_R = 4.0

# P08: pod-to-lid seal. Gap to groove ceiling = 1.6 -> 20% compression.
P08 = dict(x=(26.0, 79.5), y=(16.0, 98.0), z0=54.0, h=GASKET_H,
           web=3.0, corner_r=GASKET_CORNER_R)
# P04: hood-to-lid seal. Groove floor z=57.4; hood underside z=58.9 -> 25% compression.
P04 = dict(x=(26.0, 78.0), y=(16.0, 98.0), z0=LID_Z + LID_T - GROOVE_DEPTH,
           h=GASKET_H, web=3.0, corner_r=GASKET_CORNER_R,
           bar_y=(51.5, 54.5))

# ---------- Cable stop P05 ----------
P05 = (75.5, 79.5, 83.0, 89.0, 46.0, 54.0)

# ---------- Calibration hood P07 ----------
HOOD_Z0 = LID_Z + LID_T + 0.9
# Shifted +20 mm and widened +8 mm to the right.
HOOD_PLATE = (24.0, 80.0, 4.2, 109.8)  # 56.0 x 105.6
HOOD_PLATE_T = 3.0
HOOD_CENTER = (52.0, 57.0)
HOOD_OUT = ((48.0, 94.0), (36.0, 70.0), 22.0)
HOOD_IN = ((43.0, 89.0), (31.0, 65.0), 20.2)
HOOD_ROOF = (34.0, 22.0, 36.0, 70.0, 3.0)
HOOD_FLOOR_OPEN = (30.5, 73.5, 18.5, 95.5)
HOOD_DIVIDER_Y = (51.5, 54.5)
HOOD_PORTS = {'IN': (40.0, 30.0), 'OUT': (56.0, 86.0)}
HOOD_PORT_D = 2.0
HOOD_NOZZLE = [(8.0, 4.0), (7.0, 4.0), (6.0, 5.0)]

# ---------- Purchased-part reference dummies ----------
SEN_PCB = (32.8, 64.8, 46.0, 68.0, 46.0, 47.6)
SEN_TOP = (42.3, 55.3, 52.0, 62.0, 47.6, 50.0)
SEN_CON = (56.0, 64.0, 48.0, 56.0, 47.6, 54.4)
BTN_PCB_DUMMY = (L - WALL - BTN_HOLDER_LEN - BTN_PCB[2], L - WALL - BTN_HOLDER_LEN,
                 sum(BTN_HOLDER_Y) / 2 - BTN_PCB[0] / 2, sum(BTN_HOLDER_Y) / 2 + BTN_PCB[0] / 2,
                 sum(BTN_HOLDER_Z) / 2 - BTN_PCB[1] / 2, sum(BTN_HOLDER_Z) / 2 + BTN_PCB[1] / 2)
