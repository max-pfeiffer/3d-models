# UGREEN USB Ethernet Adapter Mount

This model is for mounting a [UGREEN 2.5G USB LAN Adapter Ethernet Adapter USB to RJ45 Network Adapter](https://www.amazon.de/dp/B0CWV2Q6HJ)
under a [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell).

The mount uses the 4 mounting holes for 2.5HDD/SSD(M3). The mount screwed onto that [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell)
from underneath. So that screws need to be accessible from underneath. The [UGREEN 2.5G USB LAN Adapter Ethernet Adapter USB to RJ45 Network Adapter](https://www.amazon.de/dp/B0CWV2Q6HJ)
device sits in the middle of the mount. The [UGREEN 2.5G USB LAN Adapter Ethernet Adapter USB to RJ45 Network Adapter](https://www.amazon.de/dp/B0CWV2Q6HJ)
can be slided into the mount from the back direction of [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell).

The ethernet port of the adapter should face to the back of the [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell).
The holes of [DeskPi SBC Shell 10 inch 1U Rack](https://deskpi.com/products/deskpi-accessories-sbc-shell) are not threaded.
So the mount has to include nuts. The screws should be 10 mm long.  
The adapter should it slide in to an end stop and clip in place.
Nothing sits in front of RJ45 port.

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

## Design

- Channel 26.9 x 16.4 mm inside, total height 21.4 mm.
- Seven 3 mm tall cross ribs on top keep the aluminium adapter off the steel tray (no metal on metal)
  and leave a 3 mm air gap above the adapter. The ribs print as bridges (no supports).
- Ventilation, because the adapter gets hot: slots in the floor let cool air in from below, open notches
  in both side walls between the ribs let warm air out sideways from the gap above the adapter.
  The adapter only touches plastic: floor strips, the lower 4 mm of the side walls, wall posts and ribs.
- Four ears on the HDD hole pattern with captive M3 nuts. The nut is pushed in from below through a hex channel;
  the M3 x 10 screw goes from above through the tray and pulls the nut up against the channel ceiling.
  5.1 mm of plastic between tray and nut, assuming a 1.5 mm tray (`TRAY_THICKNESS` in `model.py`).
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

- 4x M3 x 10 mm screws
- 4x M3 hex nuts (ISO 4032, 5.5 mm across flats)

## Build

```sh
uv run scripts/build.py models/ugreen_usb_ethernet_adapter_mount                 # full mount
uv run scripts/build.py models/ugreen_usb_ethernet_adapter_mount --part fit_test # 10 mm fit test slice
```
