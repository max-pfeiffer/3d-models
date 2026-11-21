"""Printer limits and print tolerances shared by all models. All values in mm.

Tuned for Prusa FDM printers with a 0.4 mm nozzle. If fits come out too tight
or too loose, adjust here once instead of in every model.
"""

# Build volume (X, Y, Z). Prusa MK4/MK4S: 250 x 210 x 220.
# Core One: 250 x 220 x 270, MINI: 180 x 180 x 180, XL: 360 x 360 x 360.
BED_SIZE = (250.0, 210.0, 220.0)

NOZZLE = 0.4
LAYER_HEIGHT = 0.2
MIN_WALL = 1.2  # 3 perimeters at 0.4 mm
MAX_OVERHANG_DEG = 45.0  # from vertical; steeper needs supports

# Fits between two printed parts (gap added to the hole / subtracted from the pin, per side).
CLEARANCE_SLIDING = 0.2
CLEARANCE_PRESS = 0.1

# Small chamfer on bottom edges to counter elephant's foot from the first layer.
ELEPHANT_FOOT_CHAMFER = 0.5

# Through-hole diameters for metric screws (screw slides through freely).
SCREW_CLEARANCE = {
    "M2": 2.4,
    "M2.5": 2.9,
    "M3": 3.4,
    "M4": 4.5,
    "M5": 5.5,
}

# Hex nuts (ISO 4032): (across flats, thickness).
NUT_SIZE = {
    "M2": (4.0, 1.6),
    "M2.5": (5.0, 2.0),
    "M3": (5.5, 2.4),
    "M4": (7.0, 3.2),
    "M5": (8.0, 4.7),
}
# Added to the nut size for a captive nut pocket (total, not per side).
NUT_POCKET_CLEARANCE = 0.3
