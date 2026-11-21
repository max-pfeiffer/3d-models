"""Mount for a UGREEN 2.5G USB ethernet adapter under a DeskPi SBC Shell 10" 1U rack tray.

Open-top channel screwed to the 2.5" HDD holes of the tray; the tray closes the top.
M3 screws go from above through the tray into captive nuts in the mount's ears.
The adapter slides in from the back (cable first) until its strain relief hits the front stop,
then a flexible tongue in the floor snaps in behind the RJ45 face.

Coordinates (as installed and as printed): X across the rack, -Y front, +Y back, Z up towards
the tray. Z = 0 is the floor underside, the top of the part touches the tray.
"""

from build123d import (
    Align,
    Axis,
    Box,
    Cylinder,
    Part,
    Plane,
    Polygon,
    Pos,
    RegularPolygon,
    chamfer,
    extrude,
)

from cadlib.printer import (
    CLEARANCE_SLIDING,
    ELEPHANT_FOOT_CHAMFER,
    NUT_POCKET_CLEARANCE,
    NUT_SIZE,
    SCREW_CLEARANCE,
)

# Adapter (measured, see README.md)
ADAPTER_LENGTH = 63.5
ADAPTER_WIDTH = 26.5
ADAPTER_HEIGHT = 16.0
BOOT_LENGTH = 19.0  # strain relief, tapers from full body size to BOOT_TIP_DIAMETER
BOOT_TIP_DIAMETER = 8.0

# Tray: 2.5" drive bottom mounting pattern (SFF-8201)
HOLE_ACROSS = 61.72
HOLE_ALONG = 76.60
FREE_HEIGHT = 25.0
TRAY_THICKNESS = 1.5  # estimated sheet thickness

# Channel
FLOOR = 2.0
WALL = 2.4
CAVITY_WIDTH = ADAPTER_WIDTH + 2 * CLEARANCE_SLIDING
CAVITY_HEIGHT = ADAPTER_HEIGHT + 2 * CLEARANCE_SLIDING
OUTER_WIDTH = CAVITY_WIDTH + 2 * WALL
HEIGHT = FLOOR + CAVITY_HEIGHT

# Screw ears: M3 x 10 from above through the tray into a captive nut.
# The nut is inserted from below through a hex channel; the screw pulls it up against the channel ceiling.
SCREW_LENGTH = 10.0
SCREW_PROTRUSION = 1.0  # screw tip sticking out below the nut
EAR_RADIUS = 5.0
HOLE_DIAMETER = SCREW_CLEARANCE["M3"]
NUT_ACROSS_FLATS, NUT_THICKNESS = NUT_SIZE["M3"]
NUT_POCKET_FLATS = NUT_ACROSS_FLATS + NUT_POCKET_CLEARANCE
# Material between tray and nut, so that the screw fully engages the nut
EAR_TOP = SCREW_LENGTH - TRAY_THICKNESS - NUT_THICKNESS - SCREW_PROTRUSION

# Clip: tongue in the floor with a ramped catch behind the RJ45 face
TONGUE_WIDTH = 8.0
TONGUE_LENGTH = 20.0
TONGUE_GAP = 1.0
CATCH_HEIGHT = 1.2
CATCH_DEPTH = 1.6
CATCH_MARGIN = 0.8  # extra room between RJ45 face and catch, absorbs stop position error

# Front stop: U-slot for the cable; the tapering boot stops against its sides
SLOT_WIDTH = 20.0
SLOT_BOTTOM = 2.0  # above the floor
FRONT_WALL = 3.0
# Where along the (assumed linear) taper the boot is SLOT_WIDTH wide
STOP_OFFSET = BOOT_LENGTH * (ADAPTER_WIDTH - SLOT_WIDTH) / (ADAPTER_WIDTH - BOOT_TIP_DIAMETER)

# Derived positions along Y
BACK_Y = HOLE_ALONG / 2 + EAR_RADIUS
FRONT_Y = -BACK_Y
PORT_FACE_Y = BACK_Y - CATCH_DEPTH - CATCH_MARGIN
STOP_Y = PORT_FACE_Y - ADAPTER_LENGTH - STOP_OFFSET  # inner face of the front wall

# Fit test: short slice of the channel with one pair of ears
FIT_TEST_LENGTH = 10.0

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

assert HEIGHT <= FREE_HEIGHT
assert EAR_TOP >= 3.0, "too little material between tray and nut"
assert NUT_POCKET_FLATS / 2 < EAR_RADIUS - 1.0, "nut channel breaks through the ear"


def _channel(y_min: float, y_max: float) -> Part:
    length = y_max - y_min
    y = (y_min + y_max) / 2
    outer = Pos(0, y, 0) * Box(OUTER_WIDTH, length, HEIGHT, align=BOTTOM)
    cavity = Pos(0, y, FLOOR) * Box(CAVITY_WIDTH, length + 2, CAVITY_HEIGHT + 1, align=BOTTOM)
    return outer - cavity


def _ears(y: float) -> Part:
    # Straight bar from the wall to the hole, rounded only around the hole
    x_inner = OUTER_WIDTH / 2 - WALL / 2
    width = HOLE_ACROSS / 2 - x_inner
    ears = Part()
    for side in (-1, 1):
        hole_pos = Pos(side * HOLE_ACROSS / 2, y, 0)
        ear = Pos(side * (x_inner + width / 2), y, 0) * Box(width, 2 * EAR_RADIUS, HEIGHT, align=BOTTOM)
        ear += hole_pos * Cylinder(EAR_RADIUS, HEIGHT, align=BOTTOM)
        ear -= hole_pos * Cylinder(HOLE_DIAMETER / 2, HEIGHT, align=BOTTOM)
        nut_channel = extrude(RegularPolygon(NUT_POCKET_FLATS / 2, 6, major_radius=False), HEIGHT - EAR_TOP)
        ear -= hole_pos * nut_channel
        ears += ear
    return ears


def _front_stop() -> Part:
    wall = Pos(0, STOP_Y - FRONT_WALL / 2, 0) * Box(OUTER_WIDTH, FRONT_WALL, HEIGHT, align=BOTTOM)
    slot = Pos(0, STOP_Y - FRONT_WALL / 2, FLOOR + SLOT_BOTTOM) * Box(
        SLOT_WIDTH, FRONT_WALL + 2, HEIGHT, align=BOTTOM
    )
    return wall - slot


def _tongue_slots() -> Part:
    slots = Part()
    for side in (-1, 1):
        x = side * (TONGUE_WIDTH + TONGUE_GAP) / 2
        slots += Pos(x, BACK_Y - TONGUE_LENGTH / 2 + 0.5, -1) * Box(
            TONGUE_GAP, TONGUE_LENGTH + 1, FLOOR + 2, align=BOTTOM
        )
    return slots


def _catch() -> Part:
    # Profile in the YZ plane: vertical face towards the adapter (-Y), ramp towards the back
    catch_y = PORT_FACE_Y + CATCH_MARGIN
    profile = Polygon(
        (catch_y, FLOOR - 0.1),
        (catch_y, FLOOR + CATCH_HEIGHT),
        (catch_y + 0.4, FLOOR + CATCH_HEIGHT),
        (BACK_Y, FLOOR - 0.1),
        align=None,
    )
    return extrude(Plane.YZ * profile, TONGUE_WIDTH / 2, both=True)


def build() -> Part:
    part = _channel(FRONT_Y, BACK_Y)
    part += _ears(-HOLE_ALONG / 2) + _ears(HOLE_ALONG / 2)
    part += _front_stop()
    part -= _tongue_slots()
    part += _catch()
    return chamfer(part.edges().group_by(Axis.Z)[0], ELEPHANT_FOOT_CHAMFER)


def build_fit_test() -> Part:
    """Channel cross-section and the across hole spacing, to check the fit before the full print."""
    half = FIT_TEST_LENGTH / 2
    part = _channel(-half, half) + _ears(0)
    return chamfer(part.edges().group_by(Axis.Z)[0], ELEPHANT_FOOT_CHAMFER)


if __name__ == "__main__":
    from cadlib.viewer import preview

    preview(build())
