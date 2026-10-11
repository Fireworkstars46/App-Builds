from pathlib import Path
import os
root=Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new, count=1):
    p=root/path
    s=p.read_text(encoding="utf-8")
    n=s.count(old)
    if n!=count:
        raise RuntimeError(f"{path}: anchor count {n}, expected {count}: {old[:120]!r}")
    p.write_text(s.replace(old,new,count),encoding="utf-8")
    print("patched", path)

# Program: isolated command-line self-test + crash diagnostics.
patch('Program.cs',
'''    [STAThread]
    private static void Main()
    {
        // Single-Instance: läuft schon eine Kopie, bitten wir sie nur, die Einstellungen''',
'''    [STAThread]
    private static void Main()
    {
        var args = Environment.GetCommandLineArgs();
        bool safeSelfTest = Array.Exists(args, a => string.Equals(a, "--safe-self-test", StringComparison.OrdinalIgnoreCase));
        if (safeSelfTest)
        {
            // Safe Test Mode never starts the agent, renderer, tray icon or global hotkey.
            // It touches only a unique app-local Diagnostics/SelfTestTemp directory.
            try
            {
                bool ok = DiagnosticsManager.RunSafeSelfTest(AppContext.BaseDirectory, out _, out _);
                Environment.ExitCode = ok ? 0 : 2;
            }
            catch (Exception ex)
            {
                try { DiagnosticsManager.WriteCrashReport(AppContext.BaseDirectory, ex, "--safe-self-test"); } catch { }
                Environment.ExitCode = 3;
            }
            return;
        }

        Application.ThreadException += (_, e) =>
        {
            try { DiagnosticsManager.WriteCrashReport(AppContext.BaseDirectory, e.Exception, "WinForms UI thread"); } catch { }
        };
        AppDomain.CurrentDomain.UnhandledException += (_, e) =>
        {
            if (e.ExceptionObject is Exception ex)
                try { DiagnosticsManager.WriteCrashReport(AppContext.BaseDirectory, ex, "Unhandled AppDomain exception"); } catch { }
        };

        // Single-Instance: läuft schon eine Kopie, bitten wir sie nur, die Einstellungen''')
patch('Program.cs',
'''        Application.Run(new TrayContext(Environment.GetCommandLineArgs()));''',
'''        Application.Run(new TrayContext(args));''')
