v91o Build 106 - Topology-bound UsbDk Re-enumeration

Purpose:
Avoid an unnecessary serial-number device open during the fragile post-0x52 UsbDk re-enumeration window.

Build 105 real result:
- fresh context worked;
- no Apple device at the first transition probe;
- the exact iPhone then appeared with 5 configurations and QuickTime config 5 descriptor present;
- activeQT was still false;
- the next fresh probe had fallen back to the normal 4-configuration state.

Functional change:
- cache physical bus+port topology before activation;
- select same-topology post-activation candidate without reading serial_number;
- exact serial becomes fallback only when topology cache cannot resolve the target;
- preserve Build 105 fresh context / 250 ms / 20 second bounded polling;
- preserve active-QT requirement and no forced SET_CONFIGURATION(5).

Preserved:
- Build 104 foreground-focus fix;
- Build 103 Apple-filter caution -> UsbDk-first policy;
- Build 102/95 explicit libusb0 troubleshooting path;
- Build 80 Wi-Fi/native-titlebar/pin behavior;
- stable AppId/per-user installer identity;
- Apple driver/filter stack unchanged;
- Valeria protocol packet behavior unchanged.

Status: NOT DONE / pending Windows compile and real iPhone test.
