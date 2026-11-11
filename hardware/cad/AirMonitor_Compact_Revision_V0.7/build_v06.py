"""Build AirMonitor Compact V0.6.

V0.6 keeps the proven V0.3 enclosure and changes only the right rear wall:
- center the complete 80 x 20 mm ZERO/SPAN PCB holder between the columns;
- keep ZERO/SPAN at their measured positions on the PCB;
- move DC5521 below and midway between ZERO/SPAN.
"""
from pathlib import Path
import csv
import runpy

R = Path(__file__).resolve().parent
G = R / '01_CAD_Global'
D = R / '03_Renders_Drawings'

# Remove copied/generated revision-specific files before rebuilding.
for name in (
    'AirMonitor_Compact_Assembly_V0.3.step',
    'AirMonitor_Compact_Reference_With_Dummies_V0.3.step',
    'AirMonitor_Compact_Assembly_V0.5.step',
    'AirMonitor_Compact_Reference_With_Dummies_V0.5.step',
    'AirMonitor_Compact_Assembly_V0.6.step',
    'AirMonitor_Compact_Reference_With_Dummies_V0.6.step',
):
    p = G / name
    if p.exists():
        p.unlink()

for name in ('Drawing_RearPanel_Inside_V0.5.svg', 'Drawing_RearPanel_Outside_V0.5.svg'):
    p = D / name
    if p.exists():
        p.unlink()

runpy.run_path(str(R / 'build_compact_revision.py'), run_name='__main__')

# Rename the two revision-specific STEP assemblies.
renames = {
    'AirMonitor_Compact_Assembly_V0.3.step': 'AirMonitor_Compact_Assembly_V0.6.step',
    'AirMonitor_Compact_Reference_With_Dummies_V0.3.step':
        'AirMonitor_Compact_Reference_With_Dummies_V0.6.step',
}
for old, new in renames.items():
    src = G / old
    if not src.exists():
        raise FileNotFoundError(src)
    src.replace(G / new)

# Correct revision text in inherited SVG drawings.
for path in (D / 'Drawing_Compact_Top_View.svg', D / 'Drawing_Compact_Side_View.svg'):
    if path.exists():
        text = path.read_text(encoding='utf-8').replace('V0.3', 'V0.6').replace('V0.5', 'V0.6')
        path.write_text(text, encoding='utf-8')

# Right rear wall, viewed from inside the enclosure.
# Drawing X = W - global Y; drawing Y = H - global Z.
inside_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700" viewBox="-5 -6 122 68">
<style>
text{font-family:Arial,sans-serif;font-size:3.0px;fill:#172b3a}
.title{font-size:4px;font-weight:bold}
.wall{fill:#f4f5f6;stroke:#172b3a;stroke-width:.6}
.pcb{fill:#d7e6ef;stroke:#172b3a;stroke-width:.55}
.column{fill:#c6c9cc;stroke:#59636a;stroke-width:.4}
.holder{fill:#9cc7dc;stroke:#24566f;stroke-width:.4}
.hole{fill:white;stroke:#172b3a;stroke-width:.45}
.dc{fill:#fff3c4;stroke:#172b3a;stroke-width:.55}
.axis{stroke:#8c8c8c;stroke-width:.22;stroke-dasharray:1 1}
.dim{stroke:#425866;stroke-width:.25;marker-start:url(#a);marker-end:url(#a)}
</style>
<defs><marker id="a" markerWidth="4" markerHeight="4" refX="2" refY="2" orient="auto"><path d="M4,0 L0,2 L4,4" fill="none" stroke="#425866" stroke-width=".5"/></marker></defs>
<text class="title" x="0" y="-2">AirMonitor Compact V0.6 – rechte Rückwand, Innenansicht [mm]</text>
<rect class="wall" x="0" y="0" width="112" height="55"/>
<!-- projected vertical lid columns: centres X 8 / 104, radius 4.5 -->
<rect class="column" x="3.5" y="0" width="9" height="55" rx="4.5"/>
<rect class="column" x="99.5" y="0" width="9" height="55" rx="4.5"/>
<text x="3" y="58">Deckelsäule</text><text x="96" y="58">Deckelsäule</text>
<!-- centered PCB: global Y 16..96, Z 33..53 -> inside X 16..96, drawing Y 2..22 -->
<rect class="pcb" x="16" y="2" width="80" height="20"/>
<text x="19" y="7">Microtaster-Platine 80,0 × 20,0 × 1,5</text>
<line class="axis" x1="56" y1="0" x2="56" y2="55"/>
<text x="57" y="53">Wandmitte</text>
<!-- holders: global Y 18/94, Z 35/51 -> inside X 94/18, drawing Y 20/4 -->
<circle class="holder" cx="18" cy="4" r="2.5"/>
<circle class="holder" cx="94" cy="4" r="2.5"/>
<circle class="holder" cx="18" cy="20" r="2.5"/>
<circle class="holder" cx="94" cy="20" r="2.5"/>
<text x="15" y="26">Halterung mittig; 76,0 × 16,0</text>
<!-- switches retain measured offsets on PCB -->
<circle class="hole" cx="76" cy="14" r="1.5"/>
<circle class="hole" cx="60" cy="14" r="1.5"/>
<text x="73" y="11">ZERO</text><text x="56" y="11">SPAN</text>
<!-- DC5521 below, midway between switches: global Y 44, Z 27.5 -> inside X 68, drawing Y 27.5 -->
<circle class="dc" cx="68" cy="27.5" r="5.6"/>
<text x="61" y="36">DC5521 Ø11,2</text>
<line class="axis" x1="68" y1="12" x2="68" y2="34"/>
<text x="70" y="31">unter Schalterpaar</text>
<!-- key projected gaps -->
<line class="dim" x1="12.5" y1="45" x2="16" y2="45"/>
<text x="12.2" y="43.5">3,5</text>
<line class="dim" x1="96" y1="45" x2="99.5" y2="45"/>
<text x="96.2" y="43.5">3,5</text>
<text x="1" y="62">ZERO/SPAN bleiben auf der Platine. Zentriert wird die Platinenhalterung; DC5521 sitzt darunter.</text>
</svg>'''

# Exterior view is mirrored horizontally relative to the inside view.
outside_svg = inside_svg.replace('Innenansicht', 'Aussenansicht')
outside_svg = outside_svg.replace('Drawing X = W - global Y', 'Drawing X = global Y') if 'Drawing X = W - global Y' in outside_svg else outside_svg
# Mirror all drawn geometry, but keep text readable by wrapping the geometry group would complicate the static SVG.
# Generate a dedicated simple exterior drawing instead.
outside_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="650" viewBox="-5 -6 122 66">
<style>text{font-family:Arial,sans-serif;font-size:3.1px;fill:#172b3a}.title{font-size:4px;font-weight:bold}.wall{fill:#f4f5f6;stroke:#172b3a;stroke-width:.6}.pcb{fill:none;stroke:#31708f;stroke-width:.4;stroke-dasharray:1.2 .8}.hole{fill:white;stroke:#172b3a;stroke-width:.45}.dc{fill:#fff3c4;stroke:#172b3a;stroke-width:.55}.axis{stroke:#8c8c8c;stroke-width:.22;stroke-dasharray:1 1}</style>
<text class="title" x="0" y="-2">AirMonitor Compact V0.6 – rechte Rückwand, Aussenansicht [mm]</text>
<rect class="wall" x="0" y="0" width="112" height="55"/>
<!-- PCB projection: global Y 16..96, Z 33..53 -->
<rect class="pcb" x="16" y="2" width="80" height="20"/>
<text x="18" y="7">Platinenprojektion – innen montiert</text>
<!-- global Y coordinates directly in exterior view -->
<circle class="hole" cx="36" cy="14" r="1.5"/><text x="32" y="11">ZERO</text>
<circle class="hole" cx="52" cy="14" r="1.5"/><text x="49" y="11">SPAN</text>
<circle class="dc" cx="44" cy="27.5" r="5.6"/><text x="37" y="36">DC5521 Ø11,2</text>
<line class="axis" x1="44" y1="12" x2="44" y2="34"/>
<text x="1" y="60">Die Buchse liegt von aussen direkt unter und mittig zwischen ZERO und SPAN.</text>
</svg>'''

D.mkdir(parents=True, exist_ok=True)
(D / 'Drawing_RearPanel_Inside_V0.6.svg').write_text(inside_svg, encoding='utf-8')
(D / 'Drawing_RearPanel_Outside_V0.6.svg').write_text(outside_svg, encoding='utf-8')

# Machine-readable rear-panel coordinates.
with (R / 'REAR_PANEL_COORDS_V0.6.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['feature', 'global_y_mm', 'global_z_mm', 'size_or_note'])
    w.writerow(['PCB outer', '16.0..96.0', '33.0..53.0', '80.0 x 20.0 x 1.5'])
    w.writerow(['Holder Y/Z', '18.0 / 94.0', '35.0 / 51.0', 'pattern 76.0 x 16.0'])
    w.writerow(['ZERO', '36.0', '41.0', 'service hole dia 3.0'])
    w.writerow(['SPAN', '52.0', '41.0', 'service hole dia 3.0'])
    w.writerow(['DC5521', '44.0', '27.5', 'bore dia 11.2'])

print('Generated AirMonitor Compact V0.6', R)
