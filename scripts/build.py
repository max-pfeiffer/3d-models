"""Build a model: export STEP + STL, render preview images and run print checks.

Usage:
    uv run scripts/build.py models/<name> [--open] [--part fit_test]

Each model directory contains a model.py with a `build()` function returning a Part.
Optional variants are `build_<part>()` functions, built with --part <part>.
Outputs go to out/<name>/:
    <name>.step       -> import into PrusaSlicer (true curves)
    <name>.stl        -> mesh fallback
    <name>_views.png  -> iso/front/right/top renders for review
"""

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from build123d import export_step, export_stl
from matplotlib.collections import PolyCollection

from cadlib.printer import BED_SIZE

ROOT = Path(__file__).resolve().parent.parent
PRUSA_SLICER = "/Applications/Original Prusa Drivers/PrusaSlicer.app"

# (title, direction towards the camera, screen-up hint, axis labels)
VIEWS = [
    ("iso", (1, -1.2, 0.9), (0, 0, 1), ("", "")),
    ("front (from -Y)", (0, -1, 0), (0, 0, 1), ("X mm", "Z mm")),
    ("right (from +X)", (1, 0, 0), (0, 0, 1), ("Y mm", "Z mm")),
    ("top (from +Z)", (0, 0, 1), (0, 1, 0), ("X mm", "Y mm")),
]


def load_model(model_dir: Path, part: str | None):
    spec = importlib.util.spec_from_file_location(f"models.{model_dir.name}", model_dir / "model.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, f"build_{part}" if part else "build")()


def render_views(mesh: trimesh.Trimesh, title: str, path: Path):
    # Orthographic projection with back-face culling and depth sorting (painter's algorithm).
    # matplotlib's own 3D axes sort faces poorly and show hidden faces, so we project ourselves.
    light = np.array([0.4, -0.6, 0.7])
    light /= np.linalg.norm(light)
    shade = 0.35 + 0.65 * np.clip(mesh.face_normals @ light, 0, 1)
    colors = np.outer(shade, [0.95, 0.5, 0.15])  # Prusa orange

    lo, hi = mesh.bounds
    center = (lo + hi) / 2
    half = np.linalg.norm(hi - lo) / 2 * 1.05
    triangles = mesh.triangles - center

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"{title}  ({hi[0] - lo[0]:.1f} x {hi[1] - lo[1]:.1f} x {hi[2] - lo[2]:.1f} mm)")
    for ax, (name, toward_camera, up_hint, (xlabel, ylabel)) in zip(axes.flat, VIEWS):
        d = np.array(toward_camera, dtype=float)
        d /= np.linalg.norm(d)
        right = np.cross(up_hint, d)
        right /= np.linalg.norm(right)
        up = np.cross(d, right)

        visible = mesh.face_normals @ d > 1e-6
        tris = triangles[visible]
        order = np.argsort((tris @ d).mean(axis=1))  # far to near
        projected = np.stack([tris @ right, tris @ up], axis=-1)[order]
        face_colors = colors[visible][order]

        ax.add_collection(PolyCollection(projected, facecolors=face_colors, edgecolors=face_colors, linewidths=0.3))
        ax.set_xlim(-half, half)
        ax.set_ylim(-half, half)
        ax.set_aspect("equal")
        ax.set_title(name)
        if xlabel:
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            # Ticks in world coordinates rather than centered ones.
            ax.xaxis.set_major_formatter(lambda v, _, o=center @ right: f"{v + o:.0f}")
            ax.yaxis.set_major_formatter(lambda v, _, o=center @ up: f"{v + o:.0f}")
            ax.grid(alpha=0.3)
        else:
            ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def check(part, mesh: trimesh.Trimesh) -> list[str]:
    problems = []
    bb = part.bounding_box()
    if not part.is_valid:
        problems.append("shape is not a valid solid")
    if not mesh.is_watertight:
        problems.append("mesh is not watertight")
    if abs(bb.min.Z) > 1e-3:
        problems.append(f"part does not sit on the bed: min Z = {bb.min.Z:.3f} (should be 0)")
    for axis, size, limit in zip("XYZ", (bb.size.X, bb.size.Y, bb.size.Z), BED_SIZE):
        if size > limit:
            problems.append(f"{axis} size {size:.1f} exceeds build volume {limit:.0f}")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("model_dir", type=Path)
    parser.add_argument("--open", action="store_true", help="open the STEP file in PrusaSlicer")
    parser.add_argument("--part", help="build variant: calls build_<PART>() instead of build()")
    args = parser.parse_args()

    model_dir = args.model_dir.resolve()
    out_dir = ROOT / "out" / model_dir.name
    name = f"{model_dir.name}_{args.part}" if args.part else model_dir.name
    out_dir.mkdir(parents=True, exist_ok=True)

    part = load_model(model_dir, args.part)

    step_path = out_dir / f"{name}.step"
    stl_path = out_dir / f"{name}.stl"
    png_path = out_dir / f"{name}_views.png"
    export_step(part, step_path)
    export_stl(part, stl_path, tolerance=0.01, angular_tolerance=0.1)

    mesh = trimesh.load_mesh(stl_path)
    render_views(mesh, name, png_path)

    bb = part.bounding_box()
    print(f"model:   {name}")
    print(f"size:    {bb.size.X:.2f} x {bb.size.Y:.2f} x {bb.size.Z:.2f} mm")
    print(f"volume:  {part.volume / 1000:.2f} cm3")
    print(f"step:    {step_path.relative_to(ROOT)}")
    print(f"stl:     {stl_path.relative_to(ROOT)}")
    print(f"renders: {png_path.relative_to(ROOT)}")

    problems = check(part, mesh)
    for p in problems:
        print(f"PROBLEM: {p}")
    if not problems:
        print("checks:  OK")

    if args.open:
        subprocess.run(["open", "-a", PRUSA_SLICER, str(step_path)], check=False)

    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
