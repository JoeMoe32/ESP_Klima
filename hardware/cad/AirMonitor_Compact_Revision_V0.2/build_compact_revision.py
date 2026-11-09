from pathlib import Path
import csv
import cadquery as cq
from cadquery import exporters

R=Path(__file__).resolve().parent
G=R/'01_CAD_Global'; P=R/'02_CAD_Print'; D=R/'03_Renders_Drawings'
for x in (G,P,D): x.mkdir(parents=True,exist_ok=True)
L,W,H=208.,112.,55.; wall=floor=2.8; lid_z=55.; lid_t=3.
open_x0,open_x1,open_z=36.6,158.6,12.

def box(x,y,z,l,w,h): return cq.Workplane('XY').box(l,w,h,centered=(False,False,False)).translate((x,y,z))
def cz(x,y,z,d,h): return cq.Workplane('XY',origin=(x,y,z)).circle(d/2).extrude(h)
def cx(x,y,z,d,h): return cq.Workplane('YZ',origin=(x,0,0)).center(y,z).circle(d/2).extrude(h)
def step(s,p): exporters.export(s,str(p),exportType='STEP')
def stl(s,p): exporters.export(s,str(p),exportType='STL',tolerance=.08,angularTolerance=.15)
def origin(s):
 b=s.val().BoundingBox(); return s.translate((-b.xmin,-b.ymin,-b.zmin))

# P01 base: 208 x 112 x 55, mounting flanges give Y=-10..122.
b=box(0,0,0,L,W,floor)
for q in (box(0,0,0,wall,W,H),box(L-wall,0,0,wall,W,H),box(0,0,0,L,wall,H),box(0,W-wall,0,L,wall,H)): b=b.union(q)
b=b.union(box(0,-10,0,L,10,floor)).union(box(0,W,0,L,10,floor))
for x in (37,L-37):
 for y in (-5,W+5): b=b.cut(cz(x,y,-.2,4.5,floor+.5))
for y in (-.5,W-wall-.5): b=b.cut(box(open_x0,y,open_z,open_x1-open_x0,wall+1,44))
for x,y in ((8,8),(L-8,8),(8,W-8),(L-8,W-8)):
 b=b.union(cz(x,y,floor,9,H-floor-1)).cut(cz(x,y,floor-.2,2.5,H-floor+.5))
for x in (20,175):
 for y in (21,91): b=b.union(cz(x,y,floor,9,9.6-floor)).cut(cz(x,y,floor-.2,2.5,9.6-floor+.5))
b=b.cut(cx(L-wall-.2,15,27.5,11.2,wall+.5)).cut(cx(L-wall-.2,50,28,3,wall+.5)).cut(cx(L-wall-.2,66,28,3,wall+.5))
for y in (32,108):
 for z in (22,38): b=b.union(cx(L-wall-6,y,z,5,6)).cut(cx(L-wall-6.2,y,z,1.6,6.5))

# P02 lid with vents and blind sensor-pod bosses.
l=box(0,0,lid_z,L,W,lid_t)
for i in range(9): l=l.cut(box(12,23+8*i,lid_z-.5,33,4,lid_t+1))
for y in (10,104): l=l.cut(cz(27,y,lid_z-.5,2.2,lid_t+1))
for x,y in ((8,8),(L-8,8),(8,W-8),(L-8,W-8)):
 l=l.cut(cz(x,y,lid_z-.5,3.3,lid_t+1)).cut(cz(x,y,lid_z+1.5,6.2,1.8))
mount=((14,14),(44,14),(14,100),(44,100))
for x,y in mount: l=l.union(cz(x,y,51,7,4)).cut(cz(x,y,51,2.5,3.5))

# P03 sealed sensor pod above left side of Waveshare.
p=box(6,16,40,45.5,82,14).cut(box(9,19,43,39.5,76,12))
p=p.union(box(8,12,52,42,4,2)).union(box(8,98,52,42,4,2))
for x,y in mount: p=p.cut(cz(x,y,51.5,3,3))
for y in (49.5,64.5): p=p.union(cz(16.3,y,43,5.6,3)).cut(cz(16.3,y,42.5,3,4))
p=p.cut(box(47.5,83,46,4.5,6,8.5))

# P04/P05/P08 seals and cable stop.
g8=box(6,16,54,45.5,82,1).cut(box(9,19,53.8,39.5,76,1.4))
stop=box(47.5,83,48,4,6,3.2)
g4=box(6,16,57.95,44,82,1.2).cut(box(8,18,57.7,40,78,1.7))

# P07 removable calibration hood. Normal operation uses no hood.
h=box(4,4.2,58.15,48,105.6,3)
for y in (10,104): h=h.cut(cz(27,y,57.9,2.2,3.5))
out=(cq.Workplane('XY',origin=(0,0,61.15)).center(28,57).rect(40,94).workplane(offset=22).rect(28,70).loft())
inn=(cq.Workplane('XY',origin=(0,0,60.95)).center(28,57).rect(35,89).workplane(offset=20.2).rect(23,65).loft())
h=h.union(out).cut(inn).union(box(14,22,83.15,28,70,3))
for x,y in ((20,30),(36,86)):
 h=h.cut(cz(x,y,82,2,20)); z=86.15
 for d,hh in ((8,4),(7,4),(6,5)): h=h.union(cz(x,y,z,d,hh)); z+=hh
 h=h.cut(cz(x,y,82,2,20))

parts={'P01_Compact_Base_Global':b,'P02_Compact_Lid_Global':l,'P03_Compact_SensorPod_Global':p,'P04_Hood_Gasket_TPU':g4,'P05_Cable_Stop_Global':stop,'P07_Calibration_Hood_Unchanged':h,'P08_Pod_Lid_Gasket_Global':g8}
for n,s in parts.items(): step(s,G/(n+'.step'))
print_names={'P01_Compact_Base_Global':'P01_Compact_Base_Print','P02_Compact_Lid_Global':'P02_Compact_Lid_Print','P03_Compact_SensorPod_Global':'P03_Compact_SensorPod_Print','P04_Hood_Gasket_TPU':'P04_Hood_Gasket_TPU_Print','P05_Cable_Stop_Global':'P05_Cable_Stop_Print','P07_Calibration_Hood_Unchanged':'P07_Calibration_Hood_Print','P08_Pod_Lid_Gasket_Global':'P08_Pod_Lid_Gasket_Print'}
for n,s in parts.items():
 q=origin(s); step(q,P/(print_names[n]+'.step')); stl(q,P/(print_names[n]+'.stl'))
sh=[s.val() for s in parts.values()]
step(cq.Workplane(obj=cq.Compound.makeCompound(sh)),G/'AirMonitor_Compact_Assembly_V0.2.step')
carrier=box(10,11,9.6,175,90,18); pcb=box(21.6,11,9.6,151.8,90,1.6); sen=box(12.8,46,46,32,22,1.6); top=box(22.3,52,47.6,13,10,2.4); con=box(36,48,47.6,8,8,6.8)
step(cq.Workplane(obj=cq.Compound.makeCompound(sh+[carrier.val(),pcb.val(),sen.val(),top.val(),con.val()])),G/'AirMonitor_Compact_Reference_With_Dummies_V0.2.step')
with (R/'DIMENSIONS.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['part','x_len','y_len','z_len','x_min','x_max','y_min','y_max','z_min','z_max','volume_mm3'])
 for n,s in parts.items():
  q=s.val(); bb=q.BoundingBox(); w.writerow([n,*[f'{v:.3f}' for v in (bb.xlen,bb.ylen,bb.zlen,bb.xmin,bb.xmax,bb.ymin,bb.ymax,bb.zmin,bb.zmax,q.Volume())]])
top_svg='<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="-10 -20 228 152"><style>text{font-family:Arial;font-size:5px}.a{fill:none;stroke:#12385b;stroke-width:.8}.b{fill:#cfe1ef;stroke:#12385b}.c{fill:#f0c774;stroke:#12385b}</style><rect class="a" x="0" y="0" width="208" height="112"/><rect class="b" x="10" y="11" width="175" height="90"/><rect class="c" x="6" y="16" width="45.5" height="82"/><text x="3" y="-5">Laminar AirMonitor HCHO – Top view V0.2 [mm]</text><text x="70" y="58">Waveshare</text><text x="8" y="44">SEN0661 pod</text></svg>'
side_svg='<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="-10 -8 228 115"><style>text{font-family:Arial;font-size:5px}.a{fill:none;stroke:#12385b;stroke-width:.8}.b{fill:#cfe1ef;stroke:#12385b}.c{fill:#f0c774;stroke:#12385b}.d{fill:none;stroke:#a43;stroke-dasharray:3 2}</style><rect class="a" x="0" y="0" width="208" height="55"/><rect class="b" x="10" y="9.6" width="175" height="18"/><rect class="c" x="6" y="40" width="45.5" height="14"/><rect class="d" x="4" y="58.15" width="48" height="38"/><text x="3" y="-3">Laminar AirMonitor HCHO – Side view V0.2 [mm]</text><text x="60" y="22">Waveshare</text><text x="8" y="48">sensor pod</text></svg>'
(D/'Drawing_Compact_Top_View.svg').write_text(top_svg,encoding='utf-8'); (D/'Drawing_Compact_Side_View.svg').write_text(side_svg,encoding='utf-8')
print('Generated',R)
