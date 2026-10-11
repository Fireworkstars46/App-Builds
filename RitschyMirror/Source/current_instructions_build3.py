"""Apply the Build 3 CURRENT Custom Instructions compatibility/reliability patch set.

Split into readable source patches so the build remains auditable and non-obfuscated.
Each part runs after all established Build 2 behavior patches and preserves the
existing application identity, paths, settings/data and renderer behavior.
"""
from pathlib import Path
import runpy

here = Path(__file__).resolve().parent
for name in (
    "build3_core_reliability.py",
    "build3_remove_mouse_hook.py",
    "build3_program_selftest.py",
    "build3_settings_ui.py",
    "build3_tray_behavior.py",
    "build3_fix_tray_compile.py",
    "build3_warning_cleanup.py",
):
    print("Applying", name)
    runpy.run_path(str(here / name), run_name="__main__")

print("Build 3 current-instructions patch set applied")
