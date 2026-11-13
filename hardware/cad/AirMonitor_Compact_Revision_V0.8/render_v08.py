from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import cadquery as cq
from cadquery import importers

import compact_params as C

R = Path(__file__).resolve().parent
G = R / "01_CAD_Global"
D = R / "03_Renders_Drawings"
D.mkdir(exist_ok=True)


def tess(path: Path, offset=(0.0,0.0,0.0), tol=1.0):
    shape = importers.importStep(str(path)).val()
    verts, tris = shape.tessellate(tol, 0.25)
    v = np.array([[p.x+offset[0],p.y+offset[1],p.z+offset[2]] for p in verts])
    return v[np.array(tris,dtype=int)]


def equal_axes(ax, bounds):
    xmin,xmax,ymin,ymax,zmin,zmax=bounds
    cx=(xmin+xmax)/2; cy=(ymin+ymax)/2; cz=(zmin+zmax)/2
    r=max(xmax-xmin,ymax-ymin,zmax-zmin)/2
    ax.set_xlim(cx-r,cx+r); ax.set_ylim(cy-r,cy+r); ax.set_zlim(cz-r,cz+r)
    ax.set_box_aspect((1,1,0.55)); ax.set_axis_off()


def render(name: str, lid_dx: float):
    fig=plt.figure(figsize=(12,7),dpi=180)
    ax=fig.add_subplot(111,projection='3d')
    parts=[
        ("P01_Compact_Base_Global.step",(0,0,0),"#3a9d5d",1.0),
        ("P02_Compact_Lid_Global.step",(lid_dx,0,0),"#e28b35",0.92),
        ("P03_Compact_SensorPod_Global.step",(lid_dx,0,0),"#4f83cc",0.95),
        ("P07_Calibration_Hood.step",(lid_dx,0,0),"#8d5bb7",0.92),
    ]
    for fn,off,col,alpha in parts:
        tri=tess(G/fn,off)
        pc=Poly3DCollection(tri,facecolor=col,edgecolor=(0,0,0,0.12),linewidth=0.15,alpha=alpha)
        ax.add_collection3d(pc)
    equal_axes(ax,(-10,225,-15,127,0,105))
    ax.view_init(elev=24,azim=-58)
    if lid_dx:
        ax.quiver(118,118,68,-24,0,0,color="#b33",linewidth=2,arrow_length_ratio=.18)
        ax.text(92,121,72,"8 mm einschieben",fontsize=10)
    ax.set_title("AirMonitor Compact V0.8 – " + ("offen / +8 mm" if lid_dx else "geschlossen"),fontsize=14)
    plt.tight_layout(pad=0)
    fig.savefig(D/name,bbox_inches='tight',pad_inches=.05)
    plt.close(fig)


render("Render_V08_Closed.png",0.0)
render("Render_V08_Open_8mm.png",C.SLIDE_OPEN_OFFSET_X)

# 2D guide section, enlarged.
fig,ax=plt.subplots(figsize=(10,6),dpi=180)
ax.add_patch(Rectangle((0,45),C.LID_SKIRT_W,10,facecolor="#e9a35a",edgecolor="#6e421d",linewidth=1.5,label="P02 Deckelschuerze"))
groove=np.array([
    [C.GUIDE_GROOVE_INNER_Y_FRONT,C.GUIDE_GROOVE_Z0],
    [C.GUIDE_GROOVE_OUTER_Y_FRONT,C.GUIDE_GROOVE_Z0+C.GUIDE_GROOVE_RISE],
    [C.GUIDE_GROOVE_OUTER_Y_FRONT,C.GUIDE_GROOVE_Z1+C.GUIDE_GROOVE_RISE],
    [C.GUIDE_GROOVE_INNER_Y_FRONT,C.GUIDE_GROOVE_Z1],
])
ax.add_patch(Polygon(groove,closed=True,facecolor="white",edgecolor="#b33",linewidth=2,label="blinde 45°-Nut"))
ax.add_patch(Rectangle((C.SHOULDER_INSET,45),4.5,10,facecolor="#8fd19e",edgecolor="#246b3d",linewidth=1.5,label="P01 Schulter"))
lug=np.array([
    [C.SHOULDER_INSET,C.GUIDE_ROOT_Z0],
    [C.SHOULDER_INSET-C.GUIDE_PROJ,C.GUIDE_ROOT_Z0+C.GUIDE_RISE],
    [C.SHOULDER_INSET-C.GUIDE_PROJ,C.GUIDE_ROOT_Z1+C.GUIDE_RISE],
    [C.SHOULDER_INSET,C.GUIDE_ROOT_Z1],
])
ax.add_patch(Polygon(lug,closed=True,facecolor="#3a9d5d",edgecolor="#1f5b34",linewidth=2,label="45°-Zunge"))
ax.annotate("sichtbare Aussenhaut\nbleibt geschlossen",xy=(.8,49),xytext=(-3.2,52.8),arrowprops=dict(arrowstyle="->"),fontsize=10)
ax.annotate("45°",xy=(2.35,47.25),xytext=(4.7,47.0),arrowprops=dict(arrowstyle="->"),fontsize=11)
ax.text(4.7,50.2,"0,30 mm Schulterspiel\n8 mm Schiebeweg\nkein horizontaler C-Kanal",fontsize=11,va="center")
ax.set_xlim(-4,10); ax.set_ylim(44,56); ax.set_aspect('equal'); ax.axis('off'); ax.legend(loc='lower right')
ax.set_title("V0.8 – Schnitt der supportfreien verdeckten Randfuehrung")
fig.savefig(D/"Render_V08_Guide_Section.png",bbox_inches='tight',pad_inches=.08)
plt.close(fig)
print("Generated V0.8 renders in",D)
