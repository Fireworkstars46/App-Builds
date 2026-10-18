# Crash Monitor v4.2 Build 10

Build 10 is a corrective build for the real Windows Build 9 Safe Self-Test failure at test 36/36.

## Fix

Build 9 removed the 1 MiB stack buffer and stopped the access-violation crash, but the production
archive splitter still failed when a single 1 MiB input read crossed a configured part boundary.
After closing a full part, leftover bytes from that same read attempted to write to the now-closed
handle.

Build 10 fixes that production path by reopening the next numbered part inside the inner write loop
before any leftover bytes are written. It also tracks completed parts explicitly, so exact-boundary
files produce the correct count without an extra empty part.

Safe Self-Test 36/36 now verifies the real production splitter with a forced 8 KiB source and 2 KiB
part limit, checks exactly four parts, validates every output byte in order, confirms no fifth part,
and checks the reassembly script is created.

All existing Crash Monitor identity, paths, settings, tray/taskbar behavior, WER behavior, dump types,
OBS PSS/VA-clone handling, ZIP verification, log limits, test progress, hang detection, and update
compatibility are preserved.

Runtime Windows verification of Build 10 is still required before DONE.
