# 3d-models

Parametric 3D models for Prusa printers, written in Python with [build123d](https://build123d.readthedocs.io/) and designed together with Claude Code.

## Setup

```sh
uv sync
```

## Usage

Build a model (STEP + STL + preview renders in `out/<name>/`):

```sh
uv run scripts/build.py models/example_block
uv run scripts/build.py models/example_block --open   # also open in PrusaSlicer
```

Live 3D viewer while designing:

```sh
uv run python -m ocp_viewer                # starts the viewer, open the printed URL in a browser
uv run models/example_block/model.py       # sends the model to the viewer
```

Import the `.step` file into PrusaSlicer (smoother curves than STL). After rebuilding, use right-click → *Reload from disk*.

## New model

Create `models/<name>/model.py` with a `build()` function returning a build123d `Part` (see `models/example_block`). Shared printer tolerances live in `cadlib/printer.py`.
