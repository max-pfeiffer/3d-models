# 3d-models

Parametric 3D models written in Python with [build123d](https://build123d.readthedocs.io/), printed on Prusa FDM printers and sliced in PrusaSlicer.

## Layout

- `models/<name>/model.py` — one model per directory. Exposes `build() -> Part`. Parameters as UPPER_CASE constants at the top.
- `models/<name>/README.md` — what the part is for, real-world measurements it is based on, print settings (orientation, material, supports yes/no).
- `cadlib/printer.py` — bed size, nozzle, wall thickness, fit clearances, screw hole sizes. Import from here; never hard-code tolerances in a model.
- `cadlib/viewer.py` — `preview(part)` sends shapes to the OCP CAD Viewer.
- `scripts/build.py` — exports STEP/STL, renders previews, runs checks.
- `out/` — generated files, gitignored.

## Workflow

1. Build: `uv run scripts/build.py models/<name>` (add `--open` to open the STEP in PrusaSlicer). Variants such as fit tests are extra `build_<part>()` functions in `model.py`, built with `--part <part>`.
2. **Always** read `out/<name>/<name>_views.png` after a build and check the geometry visually (iso, front, right, top views).
3. Check the printed stats (size, volume) against the intended dimensions. A non-zero exit means a PROBLEM line was printed — fix it.
4. Build models incrementally: base shape first, then one feature at a time, building and checking the renders after each step.

The user views models live with `uv run python -m ocp_viewer` (browser viewer) and `uv run models/<name>/model.py`.

## Modeling conventions

- Units are millimetres. Z is up; the part's print orientation is its modeled orientation, with the bed at Z = 0.
- Use build123d algebra mode (`Box(...) - Cylinder(...)`, `Pos(...) * shape`), not builder mode.
- Every dimension is a named constant derived from measurements or from `cadlib.printer`. Derived values are computed, not retyped.
- Select edges/faces by geometry (`group_by(Axis.Z)`, `filter_by(...)`, `sort_by(...)`), not by index.
- Shared features used by more than one model (screw bosses, magnet pockets, heat-set insert holes) go into `cadlib/`.
- When the user gives real-world measurements, record them in the model's README.md.

## Design for FDM printing

- Flat face on the bed; no part of the model below Z = 0.
- Overhangs at most 45° from vertical. Avoid designs that need supports; split the part or reorient instead.
- Bottom edges: chamfer by `ELEPHANT_FOOT_CHAMFER`, don't fillet (fillets on the bottom overhang). Fillets are fine elsewhere.
- Horizontal holes larger than ~5 mm: use a teardrop or flat-topped shape so the top doesn't sag.
- Walls at least `MIN_WALL`; prefer multiples of the nozzle width.
- Mating parts: apply `CLEARANCE_SLIDING` / `CLEARANCE_PRESS`. Screw holes from `SCREW_CLEARANCE`.
- Bridges up to ~10 mm are fine without supports.
- Must fit within `BED_SIZE`.

## Git

Commit source only. Don't commit `out/`.
