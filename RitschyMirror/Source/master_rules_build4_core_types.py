import os
from pathlib import Path

root = Path(os.environ.get('RITSCHY_SOURCE', '/mnt/data/ritschy_build4_proto'))

def read(name): return (root/name).read_text(encoding='utf-8')
def write(name, text): (root/name).write_text(text, encoding='utf-8')
def repl(name, old, new, count=1):
    p=root/name; s=p.read_text(encoding='utf-8')
    if s.count(old) < count:
        raise RuntimeError(f'{name}: anchor not found enough times: {old[:120]!r}')
    s=s.replace(old,new,count)
    p.write_text(s,encoding='utf-8')
    print('patched', name)

# Build number only; version remains 1.3.2.
repl('AppInfo.cs', 'public const int BuildNumber = 3;', 'public const int BuildNumber = 4;')

write('SettingsPersistence.cs', r'''using System.Text;

namespace RitschyMirror;

/// <summary>
/// Project-local settings persistence. Writes a complete replacement beside the
/// destination and renames it into place, then reads it back byte-for-text to
/// prove the committed value is the value requested. No shared temp directory.
/// </summary>
internal static class SettingsPersistence
{
    public static void WriteTextAtomicVerified(string path, string text)
    {
        string full = Path.GetFullPath(path);
        string? dir = Path.GetDirectoryName(full);
        if (string.IsNullOrWhiteSpace(dir))
            throw new IOException("Settings path has no parent directory.");
        Directory.CreateDirectory(dir);
        string temp = full + ".write-" + Guid.NewGuid().ToString("N") + ".tmp";
        try
        {
            var utf8 = new UTF8Encoding(encoderShouldEmitUTF8Identifier: false);
            using (var fs = new FileStream(temp, FileMode.CreateNew, FileAccess.Write,
                                           FileShare.None, 4096, FileOptions.WriteThrough))
            using (var writer = new StreamWriter(fs, utf8))
            {
                writer.Write(text);
                writer.Flush();
                fs.Flush(flushToDisk: true);
            }
            File.Move(temp, full, overwrite: true);
            string verify = File.ReadAllText(full, Encoding.UTF8);
            if (!string.Equals(verify, text, StringComparison.Ordinal))
                throw new IOException("Settings verification failed after write.");
        }
        finally
        {
            try { if (File.Exists(temp)) File.Delete(temp); } catch { }
        }
    }
}
''')

write('SettingsActions.cs', r'''using System.Text.Json.Nodes;

namespace RitschyMirror;

/// <summary>
/// Shared production state setters used by duplicate Settings/tray/preview
/// controls. Each setter persists through the normal config class and verifies
/// by reloading the committed file.
/// </summary>
internal static class SettingsActions
{
    private static void VerifyApp(string path, Func<AppSettings, bool> ok, string name)
    {
        if (!ok(AppSettings.Load(path)))
            throw new IOException(name + " was not persisted.");
    }

    public static void SetNotifications(AppSettings app, string path, bool value)
    {
        bool old = app.NotificationsEnabled;
        app.NotificationsEnabled = value;
        try
        {
            app.Save(path);
            VerifyApp(path, a => a.NotificationsEnabled == value, "notifications_enabled");
        }
        catch
        {
            app.NotificationsEnabled = old;
            throw;
        }
    }

    public static void SetMainSettingsMinimizeToTray(AppSettings app, string path, bool value)
    {
        bool old = app.MinimizeSettingsToTray;
        app.MinimizeSettingsToTray = value;
        try
        {
            app.Save(path);
            VerifyApp(path, a => a.MinimizeSettingsToTray == value, "minimize_settings_to_tray");
        }
        catch
        {
            app.MinimizeSettingsToTray = old;
            throw;
        }
    }

    public static void SetDebugLogging(string path, bool value)
    {
        MirrorConfig.MergePatch(path, new JsonObject { ["debug_logging"] = value });
        if (MirrorConfig.Load(path).DebugLogging != value)
            throw new IOException("debug_logging was not persisted.");
    }

    public static void SetHidePreviewTaskbarButton(string path, bool value)
    {
        MirrorConfig.MergePatch(path, new JsonObject { ["hide_preview_taskbar_button"] = value });
        if (MirrorConfig.Load(path).HidePreviewTaskbarButton != value)
            throw new IOException("hide_preview_taskbar_button was not persisted.");
    }

    public static void SetMinimizePreviewToTray(string path, bool value)
    {
        MirrorConfig.MergePatch(path, new JsonObject { ["minimize_preview_to_tray"] = value });
        if (MirrorConfig.Load(path).MinimizePreviewToTray != value)
            throw new IOException("minimize_preview_to_tray was not persisted.");
    }

    public static void ResetPreviewWindowLayout(string path)
    {
        MirrorConfig.MergePatch(path, new JsonObject
        {
            ["preview_x"] = int.MinValue,
            ["preview_y"] = int.MinValue,
            ["preview_width"] = 0,
            ["preview_height"] = 0,
            ["preview_maximized"] = false,
        });
        var cfg = MirrorConfig.Load(path);
        if (cfg.PreviewX != int.MinValue || cfg.PreviewY != int.MinValue ||
            cfg.PreviewWidth != 0 || cfg.PreviewHeight != 0 || cfg.PreviewMaximized)
            throw new IOException("Preview window layout reset was not persisted.");
    }
}
''')

write('StartupBehavior.cs', r'''namespace RitschyMirror;

internal readonly record struct StartupPlan(bool AutostartMirror, bool OpenSettings, bool HideSettingsToTray);

/// <summary>One production decision path for startup flags and saved state.</summary>
internal static class StartupBehavior
{
    public static StartupPlan Resolve(AppSettings app, string[]? args)
    {
        bool explicitSettings = args != null && Array.Exists(args,
            a => string.Equals(a, "--settings", StringComparison.OrdinalIgnoreCase));
        bool open = explicitSettings || app.OpenSettingsAtStartup;
        bool hide = !explicitSettings && app.OpenSettingsAtStartup && app.StartMinimizedToTray;
        return new StartupPlan(app.AutostartMirror, open, hide);
    }
}
''')

write('SingleInstanceCoordinator.cs', r'''using System.Threading;

namespace RitschyMirror;

/// <summary>
/// Creates the show-settings event BEFORE the mutex decision, so a relaunch
/// during very early startup cannot lose its request before TrayContext has
/// registered its callback.
/// </summary>
internal sealed class SingleInstanceCoordinator : IDisposable
{
    private readonly Mutex _mutex;
    public EventWaitHandle ShowSettingsEvent { get; }
    public bool IsPrimary { get; }

    public SingleInstanceCoordinator(string mutexName, string eventName)
    {
        ShowSettingsEvent = new EventWaitHandle(false, EventResetMode.AutoReset, eventName);
        _mutex = new Mutex(initiallyOwned: true, mutexName, out bool createdNew);
        IsPrimary = createdNew;
    }

    public void SignalShowSettings() => ShowSettingsEvent.Set();

    public void Dispose()
    {
        ShowSettingsEvent.Dispose();
        _mutex.Dispose();
    }
}
''')

write('TrayClickCoordinator.cs', r'''using System.Windows.Forms;

namespace RitschyMirror;

/// <summary>
/// Arbitrates NotifyIcon left-click vs double-click so Windows cannot run both
/// actions for the same physical gesture. Existing RitschyMirror behavior is
/// preserved: single click = Settings; first double-click = Settings; second
/// distinct double-click within the window = restore a running preview.
/// </summary>
internal sealed class TrayClickCoordinator : IDisposable
{
    private readonly System.Windows.Forms.Timer _singleTimer;
    private readonly Action _openSettings;
    private readonly Action _restorePreview;
    private readonly TimeSpan _secondDoubleWindow;
    private DateTime _lastDoubleUtc = DateTime.MinValue;
    private DateTime _ignoreMouseClickUntilUtc = DateTime.MinValue;

    public TrayClickCoordinator(Action openSettings, Action restorePreview,
                                int? singleClickDelayMs = null,
                                TimeSpan? secondDoubleWindow = null)
    {
        _openSettings = openSettings;
        _restorePreview = restorePreview;
        _secondDoubleWindow = secondDoubleWindow ?? TimeSpan.FromSeconds(10);
        int delay = singleClickDelayMs ?? Math.Max(200, SystemInformation.DoubleClickTime + 50);
        _singleTimer = new System.Windows.Forms.Timer { Interval = Math.Max(1, delay) };
        _singleTimer.Tick += (_, _) =>
        {
            _singleTimer.Stop();
            _openSettings();
        };
    }

    public void OnMouseClick(MouseButtons button)
    {
        if (button != MouseButtons.Left) return;
        if (DateTime.UtcNow < _ignoreMouseClickUntilUtc) return;
        _singleTimer.Stop();
        _singleTimer.Start();
    }

    public void OnDoubleClick()
    {
        _singleTimer.Stop();
        var now = DateTime.UtcNow;
        _ignoreMouseClickUntilUtc = now.AddMilliseconds(Math.Max(1, _singleTimer.Interval));
        bool secondDoubleClick = (now - _lastDoubleUtc) <= _secondDoubleWindow;
        _lastDoubleUtc = secondDoubleClick ? DateTime.MinValue : now;
        if (secondDoubleClick) _restorePreview();
        else _openSettings();
    }

    public void Dispose() => _singleTimer.Dispose();
}
''')

write('LoginAutostart.cs', r'''using Microsoft.Win32;

namespace RitschyMirror;

internal static class LoginAutostart
{
    private const string RunKey = @"Software\Microsoft\Windows\CurrentVersion\Run";

    public static bool IsEnabled(string valueName)
    {
        using var k = Registry.CurrentUser.OpenSubKey(RunKey);
        return k?.GetValue(valueName) != null;
    }

    public static void SetEnabled(string valueName, bool enabled, string executablePath)
    {
        using var k = Registry.CurrentUser.OpenSubKey(RunKey, writable: true)
                      ?? Registry.CurrentUser.CreateSubKey(RunKey);
        if (enabled) k!.SetValue(valueName, $"\"{executablePath}\"");
        else k!.DeleteValue(valueName, throwOnMissingValue: false);

        bool actual = IsEnabled(valueName);
        if (actual != enabled)
            throw new IOException("Login startup registry change did not persist.");
    }
}
''')

print('Build 4 MASTER_RULES core helper types patch applied')
