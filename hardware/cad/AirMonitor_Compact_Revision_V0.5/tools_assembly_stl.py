"""Setzt die Druck-STLs wieder in Einbaulage zusammen -> Baugruppen-STL für 360°-Ansicht.

Ohne CAD-Kern. Aufruf: python tools_assembly_stl.py
Erzeugt in 03_Renders_Drawings/:
  AirMonitor_Compact_Assembly_V0.5.stl              alle Teile, Haube montiert (Kalibrierbetrieb)
  AirMonitor_Compact_Assembly_With_Dummies_V0.5.stl zusätzlich Waveshare, SEN0661, Tasterplatine als Quader
  AirMonitor_Compact_Assembly_Parts_V0.5.3mf        alle Teile + Dummys GETRENNT, benannt und farbig
  AirMonitor_Compact_Assembly_Parts_V0.5.stl        dasselbe als ASCII-STL mit einem solid-Block pro Teil
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
        f.write(b'Laminar AirMonitor Compact V0.5 assembly'.ljust(80, b' '))
        f.write(struct.pack('<I', len(tris)))
        for a, b, c in tris:
            f.write(struct.pack('<12fH', *normal(a, b, c), *a, *b, *c, 0))


tris = []
for name, tf in PARTS.items():
    tris += [tuple(tf(*p) for p in t) for t in read_stl(P / name)]
OUT.mkdir(exist_ok=True)
write_stl(OUT / 'AirMonitor_Compact_Assembly_V0.5.stl', tris)

dummies = [C.CARRIER, (21.6, 173.4, 11.0, 101.0, 9.6, 11.2), C.SEN_PCB, C.SEN_TOP, C.SEN_CON, C.BTN_PCB_DUMMY]
tris_d = tris + [t for d in dummies for t in box_tris(*d)]
write_stl(OUT / 'AirMonitor_Compact_Assembly_With_Dummies_V0.5.stl', tris_d)

# ---- Getrennte Teile in einer Datei ----
# 3MF: jedes Teil ein eigenes, benanntes Objekt mit Farbe (Windows 3D-Viewer, 3D Builder, PrusaSlicer, Fusion).
# ASCII-STL: mehrere "solid"-Blöcke; je nach Programm als getrennte Körper geladen.
import zipfile  # noqa: E402

COLORS = {'P01': '#B8C4CC', 'P02': '#E8EEF2', 'P03': '#F0C774', 'P04': '#3A3A3A', 'P05': '#3A3A3A',
          'P07': '#7FB3D5', 'P08': '#3A3A3A', 'Dummy': '#2E8B57'}
named = []
for name, tf in PARTS.items():
    named.append((name.replace('_Print.stl', ''), [tuple(tf(*p) for p in t) for t in read_stl(P / name)]))
dummy_names = ['Dummy_Waveshare_Traeger', 'Dummy_Waveshare_PCB', 'Dummy_SEN0661_PCB', 'Dummy_SEN0661_Oberteil',
               'Dummy_SEN0661_Stecker', 'Dummy_Tasterplatine']
named += [(n, list(box_tris(*d))) for n, d in zip(dummy_names, dummies)]


def color_of(n):
    return COLORS['Dummy'] if n.startswith('Dummy') else COLORS[n[:3]]


with (OUT / 'AirMonitor_Compact_Assembly_Parts_V0.5.stl').open('w', encoding='ascii') as f:
    for n, ts in named:
        f.write(f'solid {n}\n')
        for a, b, c in ts:
            nx, ny, nz = normal(a, b, c)
            f.write(f' facet normal {nx:.6e} {ny:.6e} {nz:.6e}\n  outer loop\n')
            for p in (a, b, c):
                f.write(f'   vertex {p[0]:.4f} {p[1]:.4f} {p[2]:.4f}\n')
            f.write('  endloop\n endfacet\n')
        f.write(f'endsolid {n}\n')

objs, items = [], []
mats = ''.join(f'<base name="{n}" displaycolor="{color_of(n)}FF"/>' for n, _ in named)
for i, (n, ts) in enumerate(named):
    idx, verts, tri_xml = {}, [], []
    for t in ts:
        ids = []
        for p in t:
            k = (round(p[0], 4), round(p[1], 4), round(p[2], 4))
            if k not in idx:
                idx[k] = len(verts); verts.append(k)
            ids.append(idx[k])
        if len(set(ids)) == 3:
            tri_xml.append(f'<triangle v1="{ids[0]}" v2="{ids[1]}" v3="{ids[2]}"/>')
    vx = ''.join(f'<vertex x="{x}" y="{y}" z="{z}"/>' for x, y, z in verts)
    objs.append(f'<object id="{i + 2}" name="{n}" type="model" pid="1" pindex="{i}"><mesh><vertices>{vx}</vertices>'
                f'<triangles>{"".join(tri_xml)}</triangles></mesh></object>')
    items.append(f'<item objectid="{i + 2}"/>')
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="de-CH" '
         'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         '<metadata name="Title">Laminar AirMonitor Compact V0.5 – Baugruppe</metadata>'
         f'<resources><basematerials id="1">{mats}</basematerials>{"".join(objs)}</resources>'
         f'<build>{"".join(items)}</build></model>')
with zipfile.ZipFile(OUT / 'AirMonitor_Compact_Assembly_Parts_V0.5.3mf', 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
               '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
               '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
print(f'getrennt: {len(named)} Teile -> AirMonitor_Compact_Assembly_Parts_V0.5.3mf / .stl')

xs = [p[0] for t in tris for p in t]; ys = [p[1] for t in tris for p in t]; zs = [p[2] for t in tris for p in t]
print(f'{len(tris)} Dreiecke, Hülle X {min(xs):.1f}…{max(xs):.1f}, Y {min(ys):.1f}…{max(ys):.1f}, Z {min(zs):.1f}…{max(zs):.1f}')
print(f'mit Dummys: {len(tris_d)} Dreiecke')
