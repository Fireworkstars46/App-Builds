v91o Build 105 - Fresh UsbDk Context Re-enumeration

Purpose:
Correct Build 103/104's post-0x52 UsbDk discovery so each probe uses a genuinely new libusb context instead of PyUSB's process-global cached context.

Functional change:
- direct UsbDk activation path finalizes/recreates the PyUSB libusb context for every bounded post-activation probe;
- 250 ms probe cadence / 20 second bound;
- requires active QuickTime 0x2A before handoff;
- does not force SET_CONFIGURATION(5) on the UsbDk reference path.

Preserved:
- Build 104 foreground-focus fix;
- Build 103 Apple-filter caution -> UsbDk-first policy;
- Build 102/95 explicit libusb0 troubleshooting path;
- Build 80 Wi-Fi/native-titlebar/pin behavior;
- stable AppId/per-user installer identity;
- Apple driver/filter stack unchanged;
- Valeria protocol packet behavior unchanged.

Status: NOT DONE / pending Windows compile and real iPhone test.
