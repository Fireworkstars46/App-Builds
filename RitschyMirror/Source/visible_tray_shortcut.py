"""Add one global keyboard shortcut to the *existing* tray-only projector mode.

Ctrl+Alt+T toggles only the projector's Windows taskbar entry, never hides
the projector video or Windows taskbar itself. The visible extended display
and existing tray notification icon are left running. The same one-click
action is available from the tray right-click menu. Never claim that an app
can force Windows' icon to be pinned out of the ^ overflow: that is the
user's notification-area preference.

Runs after visible_extended_preview_tray.py, against the exact pinned source.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    f=root/path
    s=f.read_text(encoding="utf-8")
    count=s.count(old)
    if count!=1:
        raise RuntimeError(f"{path}: expected unique anchor, found {count}: {old[:130]!r}")
    f.write_text(s.replace(old,new,1),encoding="utf-8")
    print("Patched",path)

patch("TrayContext.cs",
'''    private int _taskbarHeartbeat;''',
'''    private int _taskbarHeartbeat;

    // A single Windows-wide hotkey, on the tray's message-pumping UI
    // thread; only this process instance registers it (Program mutex).
    private const int TaskbarHotkeyId = 0x524D;
    private const int WmHotkey = 0x0312;
    private const uint ModAlt = 0x0001;
    private const uint ModControl = 0x0002;
    private const uint ModNoRepeat = 0x4000;
    private const uint KeyT = 0x54;
    private readonly TaskbarShortcutFilter _taskbarShortcut;
    private bool _taskbarHotkeyRegistered;
    private readonly ToolStripMenuItem _taskbarToggleItem;

    private sealed class TaskbarShortcutFilter : IMessageFilter
    {
        private readonly Action _toggle;
        public TaskbarShortcutFilter(Action toggle) => _toggle = toggle;
        public bool PreFilterMessage(ref Message m)
        {
            if (m.Msg != WmHotkey || m.WParam.ToInt32() != TaskbarHotkeyId)
                return false;
            _toggle();
            return true;
        }
    }

    [System.Runtime.InteropServices.DllImport("user32.dll", SetLastError = true)]
    private static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, uint vk);

    [System.Runtime.InteropServices.DllImport("user32.dll", SetLastError = true)]
    private static extern bool UnregisterHotKey(IntPtr hWnd, int id);''')

patch("TrayContext.cs",
'''        menu.Items.Add(_hidePreviewItem);
        menu.Items.Add(new ToolStripMenuItem("Settings",''',
'''        menu.Items.Add(_hidePreviewItem);
        _taskbarToggleItem = new ToolStripMenuItem(
            "Hide preview taskbar button (keep video visible)    Ctrl+Alt+T",
            null, (_, _) => TogglePreviewTaskbarButton());
        menu.Items.Add(_taskbarToggleItem);
        menu.Items.Add(new ToolStripMenuItem("Settings",''')

patch("TrayContext.cs",
'''        _tray.BalloonTipClicked += (_, _) => { if (_pendingUpdateUrl != null) OpenUrl(_pendingUpdateUrl); };

        // Single-Instance''',
'''        _tray.BalloonTipClicked += (_, _) => { if (_pendingUpdateUrl != null) OpenUrl(_pendingUpdateUrl); };

        _taskbarShortcut = new TaskbarShortcutFilter(TogglePreviewTaskbarButton);
        Application.AddMessageFilter(_taskbarShortcut);
        _taskbarHotkeyRegistered = RegisterHotKey(_marshal.Handle, TaskbarHotkeyId,
                                                   ModControl | ModAlt | ModNoRepeat, KeyT);
        if (!_taskbarHotkeyRegistered)
            _engine.Log("Ctrl+Alt+T unavailable (another application may already use it); tray menu remains available.");

        // Single-Instance''')

patch("TrayContext.cs",
'''    private void RefreshUi()
    {
        bool running = _engine.IsRunning;''',
'''    /// <summary>
    /// Toggle taskbar BUTTON only; do not minimize, hide, or stop the
    /// mirrored video on the extended HDMI display. Persist the preference
    /// via MergePatch so the settings form and hot-reload keys are preserved.
    /// A second press restores the preview's taskbar button.
    /// </summary>
    private void TogglePreviewTaskbarButton()
    {
        try
        {
            var config = MirrorConfig.Load(_engine.ConfigPath);
            bool hideButton = !config.HidePreviewTaskbarButton;
            MirrorConfig.MergePatch(_engine.ConfigPath, new System.Text.Json.Nodes.JsonObject
            {
                ["hide_preview_taskbar_button"] = hideButton,
            });
            // Apply promptly; RefreshUi also reapplies on any new HWND.
            Win32Window.RequestPreviewTaskbarButton(!hideButton);
            _lastTaskbarHidden = null;
            _taskbarHeartbeat = 0;
            _taskbarToggleItem.Checked = hideButton;
        }
        catch (Exception ex)
        {
            _engine.Log("Could not toggle preview taskbar button: " + ex.Message);
        }
    }

    private void RefreshUi()
    {
        bool running = _engine.IsRunning;''')

patch("TrayContext.cs",
'''        _toggleItem.Text = running ? "Stop mirror" : "Start mirror";

        // Independently of 'Hide preview to tray':''',
'''        _toggleItem.Text = running ? "Stop mirror" : "Start mirror";
        _taskbarToggleItem.Checked =
            MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;

        // Independently of 'Hide preview to tray':''')

patch("TrayContext.cs",
'''    private void Quit()
    {
        _uiTimer.Stop();''',
'''    private void Quit()
    {
        _uiTimer.Stop();
        if (_taskbarHotkeyRegistered)
        {
            UnregisterHotKey(_marshal.Handle, TaskbarHotkeyId);
            _taskbarHotkeyRegistered = false;
        }
        Application.RemoveMessageFilter(_taskbarShortcut);''')

patch("SettingsForm.cs",
'''        Note("The preview can stay visible on Extended display without a Windows taskbar button.");''',
'''        Note("The preview can stay visible on Extended display without a Windows taskbar button.");
        Note("Shortcut: Ctrl+Alt+T toggles ONLY its taskbar button; the HDMI video stays visible.");''')

print("Ctrl+Alt+T and the existing tray menu toggle only the preview taskbar button; live HDMI video and tray icon remain visible")
