from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh

import compact_params as C

R = Path(__file__).resolve().parent
P = R / "02_CAD_Print"
D = R / "03_Renders_Drawings"
D.mkdir(parents=True, exist_ok=True)
STL = P / "P01_Compact_Base_Print_FULL_OPEN_SIDE_V0.8.stl"

if not STL.exists():
    raise SystemExit(f"Missing STL: {STL}")

mesh = trimesh.load_mesh(STL)
if not isinstance(mesh, trimesh.Trimesh):
    raise SystemExit("P01 STL did not load as one Trimesh")
if not mesh.is_watertight:
    raise SystemExit("P01 STL is not watertight")

# P01 print export is translated so the -10 mm front flange starts at Y=0.
y_shift = C.FLANGE
sample_planes = {
    "front inner shoulder depth": y_shift + C.SHOULDER_INSET + C.WALL / 2,
    "rear inner shoulder depth": y_shift + C.W - C.SHOULDER_INSET - C.WALL / 2,
}


def segment_enters_forbidden_zone(a: np.ndarray, b: np.ndarray) -> bool:
    # Dense linear sampling is sufficient for STL section polylines. Margins
    # exclude the intended vertical edges at X=36.6 and X=158.6.
    t = np.linspace(0.0, 1.0, 101)
    p = a[None, :] + (b - a)[None, :] * t[:, None]
    return bool(np.any(
        (p[:, 0] > C.OPEN_X0 + 0.25)
        & (p[:, 0] < C.OPEN_X1 - 0.25)
        & (p[:, 2] > C.SHOULDER_Z0 + 0.05)
    ))

sections: dict[str, list[np.ndarray]] = {}
failures: list[str] = []
for name, y in sample_planes.items():
    section = mesh.section(
        plane_origin=[0.0, y, 0.0],
        plane_normal=[0.0, 1.0, 0.0],
    )
    if section is None:
        failures.append(f"{name}: no section returned at Y={y:.2f}")
        continue
    curves = [np.asarray(c) for c in section.discrete]
    sections[name] = curves
    for curve in curves:
        for a, b in zip(curve[:-1], curve[1:]):
            if segment_enters_forbidden_zone(a, b):
                failures.append(
                    f"{name}: bridge segment remains at Y={y:.2f}; "
                    f"A=({a[0]:.2f},{a[2]:.2f}) B=({b[0]:.2f},{b[2]:.2f})"
                )
                break

if failures:
    raise SystemExit("\n".join(["FULL-OPEN STL CHECK FAILED:", *failures]))

fig, axes = plt.subplots(2, 1, figsize=(13, 7), dpi=180, sharex=True, sharey=True)
for ax, (name, y) in zip(axes, sample_planes.items()):
    for curve in sections[name]:
        ax.plot(curve[:, 0], curve[:, 2], linewidth=1.3)
    ax.axvspan(C.OPEN_X0, C.OPEN_X1, alpha=0.08)
    ax.axhspan(C.SHOULDER_Z0, C.H, alpha=0.08)
    ax.set_title(f"{name} – STL section Y={y:.2f} mm")
    ax.set_xlim(0, C.L)
    ax.set_ylim(0, C.H + 3)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linewidth=0.3)
    ax.set_ylabel("Z [mm]")
axes[-1].set_xlabel("X [mm]")
fig.suptitle(
    "AirMonitor V0.8: 122-mm opening fully open through outer wall and inner shoulder",
    fontsize=12,
)
fig.tight_layout()
fig.savefig(D / "Render_V08_Base_Full_Open_CrossSection.png", bbox_inches="tight")
plt.close(fig)

verification = R / "FULL_OPEN_SIDE_STL_VERIFICATION.txt"
verification.write_text(
    "\n".join([
        "AirMonitor Compact V0.8 - exact STL cross-section verification",
        f"STL: {STL.name}",
        f"Git-style mesh size: {STL.stat().st_size} bytes",
        f"Watertight: {mesh.is_watertight}",
        f"Front inner-shoulder sample Y: {sample_planes['front inner shoulder depth']:.2f} mm",
        f"Rear inner-shoulder sample Y: {sample_planes['rear inner shoulder depth']:.2f} mm",
        "Forbidden bridge zone: X 36.85..158.35 / Z above 45.05 mm",
        "Result: no section segment enters the forbidden zone",
        "Outer wall and recessed inner shoulder are both open to the top",
        "Render: 03_Renders_Drawings/Render_V08_Base_Full_Open_CrossSection.png",
    ]) + "\n",
    encoding="utf-8",
)
print(verification.read_text(encoding="utf-8"))
