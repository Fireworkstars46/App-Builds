import os
from pathlib import Path
root=Path(os.environ.get('RITSCHY_SOURCE','/mnt/data/ritschy_build4_final'))

def repl(name, old, new, count=1):
    p=root/name; s=p.read_text(encoding='utf-8')
    if s.count(old) < count:
        raise RuntimeError(f'{name}: missing anchor {old[:100]!r}')
    s=s.replace(old,new,count)
    p.write_text(s,encoding='utf-8')
    print('patched',name)

def write(name,text):
    (root/name).write_text(text,encoding='utf-8'); print('created',name)

write('MainSettingsCloseBehavior.cs', r'''using System.Windows.Forms;

namespace RitschyMirror;

internal enum MainSettingsCloseAction { None, HideToTray, ExitApp }

internal static class MainSettingsCloseBehavior
{
    public static MainSettingsCloseAction Resolve(CloseReason reason, bool appExitRequested, bool closeToTray)
    {
        if (reason != CloseReason.UserClosing || appExitRequested) return MainSettingsCloseAction.None;
        return closeToTray ? MainSettingsCloseAction.HideToTray : MainSettingsCloseAction.ExitApp;
    }
}
''')

# Use the close-decision production helper inside TrayContext; actions remain the same.
repl('TrayContext.cs',
'''        _settings.FormClosing += (_, e) =>
        {
            if (e.CloseReason == CloseReason.UserClosing && !_appExitRequested)
            {
                e.Cancel = true;
                if (_app.CloseSettingsToTray)
                    _settings?.HideMainSettingsToTray("Main Settings X setting");
                else
                    RequestFullAppExit("Main Settings X");
            }
        };''',
'''        _settings.FormClosing += (_, e) =>
        {
            switch (MainSettingsCloseBehavior.Resolve(e.CloseReason, _appExitRequested, _app.CloseSettingsToTray))
            {
                case MainSettingsCloseAction.HideToTray:
                    e.Cancel = true;
                    _settings?.HideMainSettingsToTray("Main Settings X setting");
                    break;
                case MainSettingsCloseAction.ExitApp:
                    e.Cancel = true;
                    RequestFullAppExit("Main Settings X");
                    break;
            }
        };''')

# Let the Safe Self-Test use an isolated startup registry value while production
# keeps the established RitschyMirror value name.
repl('SettingsForm.cs',
'''    private readonly AppSettings _app;
    private MirrorConfig _cfg;''',
'''    private readonly AppSettings _app;
    private readonly string _loginRunValue;
    private MirrorConfig _cfg;''')
repl('SettingsForm.cs',
'''    public SettingsForm(MirrorEngine engine, string appSettingsPath, AppSettings app)
    {
        _engine = engine; _appSettingsPath = appSettingsPath; _app = app;
        _cfg = MirrorConfig.Load(engine.ConfigPath);''',
'''    public SettingsForm(MirrorEngine engine, string appSettingsPath, AppSettings app, string? loginRunValueOverride = null)
    {
        _engine = engine; _appSettingsPath = appSettingsPath; _app = app;
        _loginRunValue = string.IsNullOrWhiteSpace(loginRunValueOverride) ? RunValue : loginRunValueOverride;
        _cfg = MirrorConfig.Load(engine.ConfigPath);''')
repl('SettingsForm.cs',
'''    private static bool IsLoginAutostart()
    {
        try { return LoginAutostart.IsEnabled(RunValue); }
        catch { return false; }
    }

    private void SetLoginAutostart(bool on)
    {
        try { LoginAutostart.SetEnabled(RunValue, on, Application.ExecutablePath); }''',
'''    private bool IsLoginAutostart()
    {
        try { return LoginAutostart.IsEnabled(_loginRunValue); }
        catch { return false; }
    }

    private void SetLoginAutostart(bool on)
    {
        try { LoginAutostart.SetEnabled(_loginRunValue, on, Application.ExecutablePath); }''')

# Self-test uses the isolated registry value through the real UI checkbox.
diag=(root/'DiagnosticsManager.cs').read_text(encoding='utf-8')
diag=diag.replace(
'''            using (var form = new SettingsForm(engine, appPath, app))''',
'''            string uiRunValue = "RitschyMirror.SafeSelfTest.UI." + Guid.NewGuid().ToString("N");
            try { LoginAutostart.SetEnabled(uiRunValue, false, Application.ExecutablePath); } catch { }
            using (var form = new SettingsForm(engine, appPath, app, uiRunValue))''',1)

# Test shared close decision and combine it with actual hide/restore + actual child exit tests.
anchor='''            // Tray gesture arbitration is production code. Pump WinForms messages so the same Timer path runs.'''
insert='''            if (MainSettingsCloseBehavior.Resolve(CloseReason.UserClosing, false, false) == MainSettingsCloseAction.ExitApp &&
                MainSettingsCloseBehavior.Resolve(CloseReason.UserClosing, false, true) == MainSettingsCloseAction.HideToTray &&
                MainSettingsCloseBehavior.Resolve(CloseReason.UserClosing, true, true) == MainSettingsCloseAction.None &&
                MainSettingsCloseBehavior.Resolve(CloseReason.ApplicationExitCall, false, true) == MainSettingsCloseAction.None)
                Pass("main Settings X/Exit close-decision production path keeps close-to-tray and full exit distinct");
            else Fail("main Settings X/Exit close-decision production path keeps close-to-tray and full exit distinct");

''' + anchor
if anchor not in diag: raise RuntimeError('close-decision selftest anchor missing')
diag=diag.replace(anchor,insert,1)

# Add a generic functional pass over every checkbox in the real Settings form. This
# verifies that each safely testable toggle actually changes its project-owned state,
# not merely that a callback exists. The startup checkbox uses uiRunValue.
anchor='''                // Production Reset button path, not just SettingsActions directly.'''
generic='''                var allChecks = FindControls<CheckBox>(form).ToList();
                foreach (var cb in allChecks)
                {
                    string label = string.IsNullOrWhiteSpace(cb.Text) ? "<unnamed checkbox>" : cb.Text;
                    bool beforeChecked = cb.Checked;
                    string beforeAppText = File.Exists(appPath) ? File.ReadAllText(appPath) : "";
                    string beforeMirrorText = File.Exists(mirrorPath) ? File.ReadAllText(mirrorPath) : "";
                    bool beforeRun = LoginAutostart.IsEnabled(uiRunValue);
                    try
                    {
                        cb.Checked = !beforeChecked;
                        PumpFor(20);
                        bool registryChanged = LoginAutostart.IsEnabled(uiRunValue) != beforeRun;
                        bool appChanged = (File.Exists(appPath) ? File.ReadAllText(appPath) : "") != beforeAppText;
                        bool mirrorChanged = (File.Exists(mirrorPath) ? File.ReadAllText(mirrorPath) : "") != beforeMirrorText;
                        if (registryChanged || appChanged || mirrorChanged)
                            Pass("Settings checkbox production action changed project-owned state: " + label);
                        else
                            Fail("Settings checkbox production action changed project-owned state: " + label, "no persisted/runtime state change detected");
                    }
                    catch (Exception ex)
                    {
                        Fail("Settings checkbox production action changed project-owned state: " + label, SanitizeText(ex.Message));
                    }
                    finally
                    {
                        try { cb.Checked = beforeChecked; PumpFor(20); } catch { }
                    }
                }

                // Verify restart-required controls explicitly communicate that fact while
                // their values persist immediately for the next restart.
''' + anchor
if anchor not in diag: raise RuntimeError('generic checkbox anchor missing')
diag=diag.replace(anchor,generic,1)

# Ensure startup checkbox UI path used the isolated value and cleanup later.
anchor='''            // Login-autostart production helper with an isolated value name, then clean it.'''
insert='''            try
            {
                if (!LoginAutostart.IsEnabled(uiRunValue))
                    Pass("Settings login-autostart checkbox restored isolated registry value to OFF after production UI exercise");
                else Fail("Settings login-autostart checkbox restored isolated registry value to OFF after production UI exercise");
            }
            finally { try { LoginAutostart.SetEnabled(uiRunValue, false, Application.ExecutablePath); } catch { } }

''' + anchor
if anchor not in diag: raise RuntimeError('ui registry cleanup anchor missing')
diag=diag.replace(anchor,insert,1)

# Add actual minimize/hide/restore production method check if follow-up has not already inserted it.
if 'main Settings hide-to-tray and restore production methods change actual window visibility/taskbar state' not in diag:
    anchor='''                var agentBox = FindCheck("Enable HTTP agent");'''
    insert='''                app.MinimizeSettingsToTray = true;
                app.Save(appPath);
                form.Show();
                form.HideMainSettingsToTray("Safe Self-Test");
                bool hiddenToTray = !form.Visible && !form.ShowInTaskbar;
                form.RestoreMainSettingsFromTray();
                bool restored = form.Visible && form.ShowInTaskbar && form.WindowState != FormWindowState.Minimized;
                form.Hide();
                if (hiddenToTray && restored) Pass("main Settings hide-to-tray and restore production methods change actual window visibility/taskbar state");
                else Fail("main Settings hide-to-tray and restore production methods change actual window visibility/taskbar state",
                          $"hidden={hiddenToTray}, restored={restored}");

''' + anchor
    if anchor not in diag: raise RuntimeError('hide restore anchor missing')
    diag=diag.replace(anchor,insert,1)

# Helper for generic UI enumeration.
anchor='''    private static T? FindControl<T>(Control root, Func<T, bool> predicate) where T : Control
    {'''
helper='''    private static IEnumerable<T> FindControls<T>(Control root) where T : Control
    {
        foreach (Control child in root.Controls)
        {
            if (child is T typed) yield return typed;
            foreach (var nested in FindControls<T>(child)) yield return nested;
        }
    }

''' + anchor
if anchor not in diag: raise RuntimeError('find helper anchor missing')
diag=diag.replace(anchor,helper,1)

(root/'DiagnosticsManager.cs').write_text(diag,encoding='utf-8')
print('patched DiagnosticsManager.cs')
print('Build 4 production-control regression patch applied')
