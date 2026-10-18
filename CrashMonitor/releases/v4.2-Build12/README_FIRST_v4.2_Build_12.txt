Crash Monitor v4.2 Build 12
============================

Build 12 fixes the Build 11 Windows Safe Self-Test child crash (0xC0000005) that occurred before the persistent report could be created.
It preserves all established Crash Monitor behavior and Build 11's 39-check automated release test.

Install/update over the existing Crash Monitor installation using:
Crash_Monitor_v4.2_Build_12_Setup.exe

After installation, run "Run Safe Self-Test..." once and send the generated Build 12 report back for runtime validation.
Do not manually repeat the four environment-owned checks; they remain honestly NOT TESTED unless separately proven.
