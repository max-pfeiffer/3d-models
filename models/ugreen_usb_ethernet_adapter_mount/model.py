"""Mount for a UGREEN 2.5G USB ethernet adapter under a DeskPi SBC Shell 10" 1U rack tray.

Channel screwed to the 2.5" HDD holes of the tray. Cross ribs on top (printed as bridges) keep the
aluminium adapter off the steel tray and leave an air gap above it. The adapter gets hot, so the
floor and side walls are vented: cool air enters through the floor, warm air leaves sideways
through the wall vents between the ribs.
M3 screws go from above through the tray into captive nuts in the mount's ears.
The adapter slides in from the back (cable first) until its strain relief hits the front stop,
then a flexible tongue in the floor snaps in behind the RJ45 face.

Coordinates (as installed and as printed): X across the rack, -Y front, +Y back, Z up towards
the tray. Z = 0 is the floor underside. Only the screw bosses touch the tray; everything else
stays TRAY_GAP below it.
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

# Ventilation
RIB_HEIGHT = 3.0  # spacer ribs between adapter and tray = air gap above the adapter
RIB_WIDTH = 3.0
RIB_PITCH = 12.0  # approximate, ribs are spread evenly from the front stop to the back end
WALL_BAND = 4.0  # solid wall above the floor; vents above it reach up to the tray
VENT_POST = 5.0  # wall post under each rib
FLOOR_VENT_WIDTH = 4.0
FLOOR_VENT_EDGE = 4.0  # floor kept solid along both walls

# Only the screw bosses touch the tray; the rest of the mount keeps this gap to it
TRAY_GAP = 2.0
BODY_HEIGHT = FLOOR + CAVITY_HEIGHT + RIB_HEIGHT  # channel, ribs, front stop, ear bars
HEIGHT = BODY_HEIGHT + TRAY_GAP  # screw bosses, up to the tray

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
    outer = Pos(0, y, 0) * Box(OUTER_WIDTH, length, BODY_HEIGHT, align=BOTTOM)
    cavity = Pos(0, y, FLOOR) * Box(CAVITY_WIDTH, length + 2, CAVITY_HEIGHT + RIB_HEIGHT + 1, align=BOTTOM)
    return outer - cavity


def _rib_positions() -> list[float]:
    first = STOP_Y + RIB_WIDTH / 2
    last = BACK_Y - RIB_WIDTH / 2
    count = round((last - first) / RIB_PITCH) + 1
    return [first + i * (last - first) / (count - 1) for i in range(count)]


def _gap_centers() -> list[float]:
    ribs = _rib_positions()
    return [(a + b) / 2 for a, b in zip(ribs, ribs[1:])]


def _rib(y: float) -> Part:
    return Pos(0, y, FLOOR + CAVITY_HEIGHT) * Box(OUTER_WIDTH, RIB_WIDTH, RIB_HEIGHT, align=BOTTOM)


def _wall_vents() -> Part:
    # Open-top notches between the ribs, so they print without bridges.
    # Skipped where an ear joins the wall.
    pitch = _rib_positions()[1] - _rib_positions()[0]
    width = pitch - VENT_POST
    vents = Part()
    for y in _gap_centers():
        if abs(y) + width / 2 > HOLE_ALONG / 2 - EAR_RADIUS:
            continue
        vents += Pos(0, y, FLOOR + WALL_BAND) * Box(OUTER_WIDTH + 2, width, HEIGHT, align=BOTTOM)
    return vents


def _floor_vents() -> Part:
    tongue_start = BACK_Y - TONGUE_LENGTH - TONGUE_GAP
    length = CAVITY_WIDTH - 2 * FLOOR_VENT_EDGE
    vents = Part()
    for y in _gap_centers():
        if y + FLOOR_VENT_WIDTH / 2 > tongue_start:
            continue
        vents += Pos(0, y, -1) * Box(length, FLOOR_VENT_WIDTH, FLOOR + 2, align=BOTTOM)
    return vents


def _ears(y: float) -> Part:
    # Straight bar from the wall to the hole, rounded only around the hole.
    # The bar stays TRAY_GAP below the tray; only the round boss around the hole reaches it.
    x_inner = OUTER_WIDTH / 2 - WALL / 2
    width = HOLE_ACROSS / 2 - x_inner
    ears = Part()
    for side in (-1, 1):
        hole_pos = Pos(side * HOLE_ACROSS / 2, y, 0)
        ear = Pos(side * (x_inner + width / 2), y, 0) * Box(width, 2 * EAR_RADIUS, BODY_HEIGHT, align=BOTTOM)
        ear += hole_pos * Cylinder(EAR_RADIUS, HEIGHT, align=BOTTOM)
        ear -= hole_pos * Cylinder(HOLE_DIAMETER / 2, HEIGHT, align=BOTTOM)
        nut_channel = extrude(RegularPolygon(NUT_POCKET_FLATS / 2, 6, major_radius=False), HEIGHT - EAR_TOP)
        ear -= hole_pos * nut_channel
        ears += ear
    return ears


def _front_stop() -> Part:
    wall = Pos(0, STOP_Y - FRONT_WALL / 2, 0) * Box(OUTER_WIDTH, FRONT_WALL, BODY_HEIGHT, align=BOTTOM)
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
    part = _channel(FRONT_Y, BACK_Y) - _wall_vents()
    part += _ears(-HOLE_ALONG / 2) + _ears(HOLE_ALONG / 2)
    part += _front_stop()
    for y in _rib_positions():
        part += _rib(y)
    part -= _tongue_slots() + _floor_vents()
    part += _catch()
    return chamfer(part.edges().group_by(Axis.Z)[0], ELEPHANT_FOOT_CHAMFER)


def build_fit_test() -> Part:
    """Channel cross-section, one rib bridge and the across hole spacing, to check the fit before the full print."""
    half = FIT_TEST_LENGTH / 2
    part = _channel(-half, half) + _rib(0) + _ears(0)
    return chamfer(part.edges().group_by(Axis.Z)[0], ELEPHANT_FOOT_CHAMFER)


if __name__ == "__main__":
    from cadlib.viewer import preview

    preview(build())
