"""Send shapes to the OCP CAD Viewer if it is running (`uv run python -m ocp_viewer`)."""


def preview(*shapes, **kwargs):
    try:
        from ocp_viewer import show

        show(*shapes, **kwargs)
    except Exception as exc:
        print(f"Viewer not reachable ({exc}). Start it with: uv run python -m ocp_viewer")
