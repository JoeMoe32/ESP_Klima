"""Setzt die Druck-STLs wieder in Einbaulage zusammen -> Baugruppen-STL für 360°-Ansicht.

Ohne CAD-Kern. Aufruf: python tools_assembly_stl.py
Erzeugt in 03_Renders_Drawings/:
  AirMonitor_Compact_Assembly_V0.3.stl              alle Teile, Haube montiert (Kalibrierbetrieb)
  AirMonitor_Compact_Assembly_With_Dummies_V0.3.stl zusätzlich Waveshare, SEN0661, Tasterplatine als Quader
"""
import struct
import sys
from pathlib import Path

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import compact_params as C  # noqa: E402

P = R / '02_CAD_Print'
OUT = R / '03_Renders_Drawings'

# Druck-STL -> global: Verschiebung um Bounding-Box-Minimum (aus DIMENSIONS.csv); P02 ist zusätzlich gedreht.
def shift(dx, dy, dz):
    return lambda x, y, z: (x + dx, y + dy, z + dz)

PARTS = {
    'P01_Compact_Base_Print.stl': shift(0, -10, 0),
    'P02_Compact_Lid_Print.stl': lambda x, y, z: (x, C.W - y, C.LID_Z + C.LID_T - z),  # 180° um X zurück
    'P03_Compact_SensorPod_Print.stl': shift(6, 9.5, 40),
    'P04_Hood_Gasket_TPU_Print.stl': shift(6, 16, 58),
    'P05_Cable_Stop_Print.stl': shift(47.5, 83, 46),
    'P07_Calibration_Hood_Print.stl': shift(4, 4.2, C.HOOD_Z0),
    'P08_Pod_Lid_Gasket_Print.stl': shift(6, 16, 54),
}


def read_stl(f):
    b = f.read_bytes()
    n = struct.unpack('<I', b[80:84])[0]
    assert 84 + 50 * n == len(b), f'{f.name}: kein binäres STL'
    for i in range(n):
        v = struct.unpack('<12f', b[84 + 50 * i:84 + 50 * i + 48])
        yield v[3:6], v[6:9], v[9:12]


def box_tris(x0, x1, y0, y1, z0, z1):
    p = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    q = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    for a, b, c, d in q:
        yield p[a], p[b], p[c]
        yield p[a], p[c], p[d]


def normal(a, b, c):
    u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    l = sum(x * x for x in n) ** .5 or 1.0
    return tuple(x / l for x in n)


def write_stl(path, tris):
    with path.open('wb') as f:
        f.write(b'Laminar AirMonitor Compact V0.3 assembly'.ljust(80, b' '))
        f.write(struct.pack('<I', len(tris)))
        for a, b, c in tris:
            f.write(struct.pack('<12fH', *normal(a, b, c), *a, *b, *c, 0))


tris = []
for name, tf in PARTS.items():
    tris += [tuple(tf(*p) for p in t) for t in read_stl(P / name)]
OUT.mkdir(exist_ok=True)
write_stl(OUT / 'AirMonitor_Compact_Assembly_V0.3.stl', tris)

dummies = [C.CARRIER, (21.6, 173.4, 11.0, 101.0, 9.6, 11.2), C.SEN_PCB, C.SEN_TOP, C.SEN_CON, C.BTN_PCB_DUMMY]
tris_d = tris + [t for d in dummies for t in box_tris(*d)]
write_stl(OUT / 'AirMonitor_Compact_Assembly_With_Dummies_V0.3.stl', tris_d)

xs = [p[0] for t in tris for p in t]; ys = [p[1] for t in tris for p in t]; zs = [p[2] for t in tris for p in t]
print(f'{len(tris)} Dreiecke, Hülle X {min(xs):.1f}…{max(xs):.1f}, Y {min(ys):.1f}…{max(ys):.1f}, Z {min(zs):.1f}…{max(zs):.1f}')
print(f'mit Dummys: {len(tris_d)} Dreiecke')
