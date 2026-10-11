"""Fix Build 3 diagnostics Explorer launch argument construction.

The tray patch source is Python-generated C#. Backslash-escaped quote literals in
that generator were consumed by Python, producing invalid C# around explorer.exe
arguments. Use ProcessStartInfo.ArgumentList instead so paths are passed as single
arguments without manual quoting. No behavior or permissions change.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])
p = root / "TrayContext.cs"
s = p.read_text(encoding="utf-8")

replacements = {
    'Process.Start(new ProcessStartInfo("explorer.exe", $""{dir}"") { UseShellExecute = true });': '''var psi = new ProcessStartInfo("explorer.exe") { UseShellExecute = true };
            psi.ArgumentList.Add(dir);
            Process.Start(psi);''',
    'Process.Start(new ProcessStartInfo("explorer.exe", $"/select,"{zip}"") { UseShellExecute = true });': '''var psi = new ProcessStartInfo("explorer.exe") { UseShellExecute = true };
            psi.ArgumentList.Add("/select," + zip);
            Process.Start(psi);''',
}

for old, new in replacements.items():
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"TrayContext.cs: expected one malformed Explorer launch, found {count}: {old!r}")
    s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")
print("Fixed Build 3 Explorer diagnostics launch syntax using ProcessStartInfo.ArgumentList")
