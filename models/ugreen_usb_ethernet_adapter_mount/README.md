# UGREEN USB Ethernet Adapter Mount

This model is for mounting a [UGREEN 2.5G USB LAN Adapter Ethernet Adapter USB to RJ45 Network Adapter](https://www.amazon.de/dp/B0CWV2Q6HJ)
under a [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell).

The mount uses the 4 mounting holes for 2.5HDD/SSD(M3). The mount screwed onto that [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell)
from underneath. So that screws need to be accessible from underneath. The [UGREEN 2.5G USB LAN Adapter Ethernet Adapter USB to RJ45 Network Adapter](https://www.amazon.de/dp/B0CWV2Q6HJ)
device sits in the middle of the mount. The [UGREEN 2.5G USB LAN Adapter Ethernet Adapter USB to RJ45 Network Adapter](https://www.amazon.de/dp/B0CWV2Q6HJ)
can be slided into the mount from the back direction of [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell).

The ethernet port of the adapter should face to the back of the [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell).
The holes of [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell) are not threaded.
So the mount has to include nuts. The screws are M3 x 20 mm button head screws, the screw head sits above the tray.
The channels for inserting the nuts must be only as long as it needs to be to hold the nuts.
The adapter should it slide in to an end stop and clip in place.
Nothing sits in front of RJ45 port.
The mount must only touch the [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell)
at the mount points. There muste be a space of 2 mm between the mount and the [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell) anywhere else.

## Measurements

### UGREEN adapter (body, without cable)
- Length: 63.5 mm
- Width: 26.5 mm
- Height: 16 mm
- Corner radius (estimate): 3 mm
- Cable strain relief at the back:
  - length 19 mm
  - at the casing: width 26.5 mm, height 16 mm
  - at the cable: diameter 8 mm
- Cable diameter: 4 mm

### UGREEN adapter – operating temperature
UGREEN publishes no operating temperature for this adapter (not on the product listing, and the
[ServeTheHome review](https://servethehome.com/ugreen-usb-a-to-rj45-2-5gbe-adapter-review) gives none either).
- Chip: Realtek RTL8156BG ([ServeTheHome](https://servethehome.com/ugreen-usb-a-to-rj45-2-5gbe-adapter-review)),
  about 1–2 W power draw for 2.5GbE.
- Comparable adapter with the same chip, Cudy UE25A: operating temperature 0–40 °C ambient, storage −40–75 °C
  ([datasheet](https://cudy.com/cdn/shop/files/UE25A_1.0_Datasheet.pdf)). j5create JCE145 (2.5G USB-C): 0–40 °C
  ([specifications](https://en.j5create.com/pages/jce145-specifications)).
- So assume **0–40 °C ambient** air around the adapter. The casing itself runs warmer than the ambient air;
  its temperature under load has not been measured.

### DeskPi SBC Shell – 2.5" HDD mounting holes (M3)
Standard 2.5" drive bottom mounting pattern (SFF-8201), matches the caliper photos:
- Hole spacing across: 61.72 mm (center to center)
- Hole spacing along: 76.60 mm (center to center)
- Free height below the tray: 25 mm
- Material thinkness of DeskPi SBC Shell: 1.5 mm

## Design

- Channel 26.9 x 16.4 mm inside. Body (channel, ribs, front stop, ear bars) 21.4 mm tall, screw bosses 23.4 mm.
- Only the four round screw bosses touch the tray. Everything else keeps a 2 mm gap to it (`TRAY_GAP` in `model.py`).
- Seven 3 mm tall cross ribs on top hold the adapter down in the channel and leave a 3 mm air gap above it
  (plus the 2 mm gap to the tray above the ribs). The ribs print as bridges (no supports).
- Ventilation, because the adapter gets hot: slots in the floor let cool air in from below, open notches
  in both side walls between the ribs let warm air out sideways from the gap above the adapter.
  The adapter only touches plastic: floor strips, the lower 4 mm of the side walls, wall posts and ribs.
- Four ears on the HDD hole pattern. The M3 x 20 button head screw goes from above through the tray and the boss
  into a nut. The nut is pushed up from below into a hex recess at the bottom of the boss, only one nut deep
  (2.7 mm), which keeps it from turning. The screw pulls the nut up against the recess ceiling (prints as a short
  bridge). 15.1 mm of plastic between tray and nut, 1 mm of screw sticks out below the nut, assuming a 1.5 mm tray
  (`TRAY_THICKNESS` in `model.py`). Only the 1.65 mm screw head sits above the tray.
- The ears only reach as far down as the nut recess. From there the underside slopes down at 45° to the side wall,
  so the ears print without supports.
- Front stop: wall with a 20 mm U-slot for the cable. The strain relief stops against the slot sides.
  The stop position assumes a linear taper of the strain relief (`STOP_OFFSET` in `model.py`).
- Clip: 8 mm wide tongue in the floor at the back with a ramped catch behind the RJ45 face.
  To remove the adapter, push the tongue down from below and pull the adapter out to the back.

## Printing

- Orientation: as modeled (floor on the bed), no supports.
- Material: PETG (or ASA). Not PLA: it softens around 55 °C, too close to the adapter's operating temperature.
  PETG also flexes better for the clip tongue.
- 0.2 mm layers, 3 perimeters, 20 % infill.

## Hardware

- 4x M3 x 20 mm button head screws (ISO 7380)
- 4x M3 hex nuts (ISO 4032, 5.5 mm across flats)

## Build

```sh
uv run scripts/build.py models/ugreen_usb_ethernet_adapter_mount                 # full mount
uv run scripts/build.py models/ugreen_usb_ethernet_adapter_mount --part fit_test # 10 mm fit test slice
```
