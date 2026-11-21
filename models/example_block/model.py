"""Example: mounting block with two M3 through holes.

Rounded top edges, elephant's-foot chamfer on the bottom, flat base for printing.
"""

from build123d import Align, Axis, Box, Cylinder, Part, Pos, chamfer, fillet

from cadlib.printer import ELEPHANT_FOOT_CHAMFER, SCREW_CLEARANCE

# Parameters (mm)
LENGTH = 40.0
WIDTH = 20.0
HEIGHT = 10.0
TOP_FILLET = 2.0
HOLE_SPACING = 26.0
HOLE_DIAMETER = SCREW_CLEARANCE["M3"]

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)


def build() -> Part:
    block = Box(LENGTH, WIDTH, HEIGHT, align=BOTTOM)
    block = fillet(block.edges().group_by(Axis.Z)[-1], TOP_FILLET)
    block = chamfer(block.edges().group_by(Axis.Z)[0], ELEPHANT_FOOT_CHAMFER)

    for x in (-HOLE_SPACING / 2, HOLE_SPACING / 2):
        block -= Pos(x, 0, 0) * Cylinder(HOLE_DIAMETER / 2, HEIGHT, align=BOTTOM)

    return block


if __name__ == "__main__":
    from cadlib.viewer import preview

    preview(build())
