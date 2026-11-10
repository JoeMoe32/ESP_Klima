"""Build AirMonitor Compact V0.5.

The solid geometry remains V0.3 except for the rigid translation of the complete
ZERO/SPAN PCB assembly defined in compact_params.py. This wrapper executes the
proven V0.3 CadQuery builder, renames revision-specific assemblies to V0.5 and
creates a dedicated inside-view drawing of the right rear wall.
"""
from pathlib import Path
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
):
    p = G / name
    if p.exists():
        p.unlink()

runpy.run_path(str(R / 'build_compact_revision.py'), run_name='__main__')

# Rename the two revision-specific STEP assemblies.
renames = {
    'AirMonitor_Compact_Assembly_V0.3.step': 'AirMonitor_Compact_Assembly_V0.5.step',
    'AirMonitor_Compact_Reference_With_Dummies_V0.3.step':
        'AirMonitor_Compact_Reference_With_Dummies_V0.5.step',
}
for old, new in renames.items():
    src = G / old
    if not src.exists():
        raise FileNotFoundError(src)
    src.replace(G / new)

# Correct revision text in inherited SVG drawings.
for path in (D / 'Drawing_Compact_Top_View.svg', D / 'Drawing_Compact_Side_View.svg'):
    if path.exists():
        path.write_text(path.read_text(encoding='utf-8').replace('V0.3', 'V0.5'), encoding='utf-8')

# Right rear wall, viewed from inside the enclosure.
# Horizontal drawing coordinate = W - global Y, so DC5521 is below-right.
rear_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="650" viewBox="-4 -4 120 63">
<style>
text{font-family:Arial,sans-serif;font-size:3.2px;fill:#172b3a}
.wall{fill:#f4f5f6;stroke:#172b3a;stroke-width:.6}
.pcb{fill:#d7e6ef;stroke:#172b3a;stroke-width:.5}
.hole{fill:white;stroke:#172b3a;stroke-width:.45}
.holder{fill:none;stroke:#31708f;stroke-width:.35;stroke-dasharray:1.2 0.8}
.dim{stroke:#555;stroke-width:.25}
</style>
<text x="0" y="-1">AirMonitor Compact V0.5 – rechte Rückwand, Innenansicht [mm]</text>
<rect class="wall" x="0" y="0" width="112" height="55"/>
<!-- PCB: global Y 24..104, Z 33..53 -> inside view X 8..88, drawing Y 2..22 -->
<rect class="pcb" x="8" y="2" width="80" height="20"/>
<text x="10" y="7">Microtaster-Platine 80,0 × 20,0 × 1,5</text>
<!-- Four holder axes, mirrored from global Y -->
<circle class="holder" cx="10" cy="4" r="2.5"/>
<circle class="holder" cx="86" cy="4" r="2.5"/>
<circle class="holder" cx="10" cy="20" r="2.5"/>
<circle class="holder" cx="86" cy="20" r="2.5"/>
<!-- ZERO/SPAN service openings, rigidly moved with PCB -->
<circle class="hole" cx="68" cy="14" r="1.5"/>
<circle class="hole" cx="52" cy="14" r="1.5"/>
<text x="65" y="18">ZERO</text>
<text x="48" y="18">SPAN</text>
<!-- DC5521 unchanged: global Y 15, Z 27.5 -> inside X 97, drawing Y 27.5 -->
<circle class="hole" cx="97" cy="27.5" r="5.6"/>
<text x="89" y="36">DC5521 Ø11,2</text>
<text x="2" y="59">Nur ZERO/SPAN-Platine, beide Schalter, vier Halter und zwei Ø3,0-Serviceöffnungen verschoben. DC5521 unverändert.</text>
</svg>'''
D.mkdir(parents=True, exist_ok=True)
(D / 'Drawing_RearPanel_Inside_V0.5.svg').write_text(rear_svg, encoding='utf-8')
print('Generated AirMonitor Compact V0.5', R)
