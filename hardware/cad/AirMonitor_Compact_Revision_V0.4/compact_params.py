"""Laminar AirMonitor HCHO – Compact V0.4 parameters (mm).

Global coordinates:
- origin: outer lower corner of P01 base
- X: enclosure long axis
- Y: enclosure short axis
- Z: upward

V0.4 change:
- compact sensor holder moved to center-left above the Waveshare board
- SEN0661 PCB centered in the holder
- Gravity connector located underneath the PCB and routed downward
- calibration hood reduced to a compact rectangular part matching the reference photo
"""

# ---------- Main enclosure ----------
L, W, H = 208.0, 112.0, 55.0
WALL = FLOOR = 2.8
FLANGE = 10.0
OPEN_X0, OPEN_X1, OPEN_Z = 36.6, 158.6, 12.0
WALL_MOUNT_HOLES = [(37.0, -5.0), (37.0, W + 5.0), (L - 37.0, -5.0), (L - 37.0, W + 5.0)]
WALL_MOUNT_D = 4.5

# Cover mounting bosses
LID_BOSSES = [(7.0, 7.0), (7.0, W - 7.0), (190.0, 8.0), (190.0, W - 8.0)]
LID_BOSS_D, LID_BOSS_PILOT_D = 9.0, 2.5

# Waveshare reference geometry
STANDOFFS = [(20.0, 21.0), (175.0, 21.0), (20.0, 91.0), (175.0, 91.0)]
STANDOFF_D, STANDOFF_PILOT_D = 9.0, 2.5
BOARD_BOTTOM_Z, BOARD_TOP_Z = 9.6, 27.6
CARRIER = (10.0, 185.0, 11.0, 101.0, 9.6, 27.6)
PCB_WAVESHARE = (21.6, 173.4, 11.0, 101.0, 9.6, 11.2)

# Right end wall components
DC5521 = (15.0, 27.5, 11.2)  # y, z, diameter
ZERO = (48.0, 28.0, 3.0)
SPAN = (64.0, 28.0, 3.0)
BTN_HOLDER_Y = (30.0, 106.0)
BTN_HOLDER_Z = (22.0, 38.0)
BTN_HOLDER_D, BTN_HOLDER_PILOT_D, BTN_HOLDER_LEN = 5.0, 1.6, 6.0
BTN_PCB = (80.0, 20.0, 1.5)

# ---------- Main lid ----------
LID_Z, LID_T = 55.0, 3.0
LID_HOLE_D, LID_CBORE_D, LID_CBORE_DEPTH = 3.3, 6.2, 1.8

# Compact vent field directly above centered SEN0661
VENTS = [(56.0, y, 36.0, 2.5) for y in (40.0, 45.0, 50.0, 61.0, 66.0, 71.0)]

# ---------- Compact sensor holder P03 ----------
# centered-left above Waveshare, significantly smaller than V0.3
POD = (44.0, 104.0, 34.0, 78.0, 40.0, 54.0)  # x0,x1,y0,y1,z0,z1
POD_WALL = 2.5

# External mounting tabs for attaching pod to lid
POD_MOUNTS = [(52.0, 32.0), (96.0, 32.0), (52.0, 80.0), (96.0, 80.0)]
POD_BOSS_D, POD_BOSS_Z0 = 7.0, 52.0
POD_BOSS_PILOT_D, POD_BOSS_PILOT_TOP = 2.5, 56.0
TONGUE_FRONT_Y = (30.0, 34.0)
TONGUE_BACK_Y = (78.0, 82.0)
TONGUE_X = (48.0, 100.0)
TONGUE_Z = (50.0, 52.0)
TONGUE_HOLE_D = 3.0

# SEN0661 centered in pod; connector is below PCB
SEN_PCB = (58.0, 90.0, 45.0, 67.0, 45.0, 46.6)
SEN_TOP = (67.5, 80.5, 51.0, 61.0, 46.6, 49.0)
SEN_CON = (81.0, 89.0, 52.0, 60.0, 40.6, 45.0)
SENSOR_BOSSES = [(61.5, 48.5), (61.5, 63.5)]
SENSOR_BOSS_D, SENSOR_HOLE_D, SENSOR_BOSS_TOP = 5.6, 3.0, 45.0

# Through floor directly below Gravity connector; cable drops downward
GRAVITY_SLOT = (80.5, 89.5, 51.5, 60.5, 39.5, 45.5)
CABLE_CHANNEL = (82.0, 88.0, 54.0, 58.0, 38.5, 42.0)

# ---------- Pod-to-lid seal P08 ----------
P08 = dict(x=(44.0, 104.0), y=(34.0, 78.0), z0=54.0, t=1.3, web=2.5)

# Cable seal / potting insert placeholder P05
P05_OUTER = (80.5, 89.5, 51.5, 60.5, 38.5, 40.4)
P05_CABLE_SLOT = (82.2, 87.8, 55.2, 56.8, 38.0, 41.0)  # 5.6 x 1.6 for measured 5.0 x 1.1 bundle

# ---------- Compact calibration hood P07 ----------
# Similar visual arrangement to the supplied reference photo: compact rectangular hood, two ports on the left.
HOOD_Z0 = LID_Z + LID_T + 0.9
HOOD_PLATE = (42.0, 106.0, 32.0, 80.0)  # 64 x 48 flange
HOOD_PLATE_T = 3.0
HOOD_CENTER = (74.0, 56.0)
HOOD_OUT = ((58.0, 42.0), (50.0, 34.0), 16.0)
HOOD_IN = ((54.0, 38.0), (46.0, 30.0), 14.5)
HOOD_ROOF = (49.0, 37.0, 50.0, 38.0, 3.0)
HOOD_FLOOR_OPEN = (50.0, 98.0, 38.0, 74.0)

# Four compression screws around the compact hood; thread into local pod/lid bosses
HOOD_SCREWS = [(47.0, 36.0), (101.0, 36.0), (47.0, 76.0), (101.0, 76.0)]
HOOD_SCREW_PILOT_D = 1.8
HOOD_SCREW_BOSS_D, HOOD_SCREW_BOSS_Z0 = 6.0, 51.0

# Internal U-flow divider: IN lower half -> around right-hand gap -> OUT upper half
HOOD_DIVIDER_Y = (54.7, 57.3)
HOOD_DIVIDER_X = (48.0, 92.0)
HOOD_PORTS = {'IN': (54.0, 45.0), 'OUT': (54.0, 67.0)}
HOOD_PORT_D = 2.0
HOOD_NOZZLE = [(8.0, 4.0), (7.0, 4.0), (6.0, 5.0)]

# Hood gasket P04: outer ring plus crossbar under divider
P04 = dict(x=(44.0, 104.0), y=(34.0, 78.0), z0=58.0, t=1.2, web=2.0,
           bar_y=HOOD_DIVIDER_Y)

# ---------- Reference dummies ----------
BTN_PCB_DUMMY = (L - WALL - BTN_HOLDER_LEN - BTN_PCB[2], L - WALL - BTN_HOLDER_LEN,
                 sum(BTN_HOLDER_Y) / 2 - BTN_PCB[0] / 2, sum(BTN_HOLDER_Y) / 2 + BTN_PCB[0] / 2,
                 sum(BTN_HOLDER_Z) / 2 - BTN_PCB[1] / 2, sum(BTN_HOLDER_Z) / 2 + BTN_PCB[1] / 2)
