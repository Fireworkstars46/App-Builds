"""Optional Minimize-to-Tray switch in BOTH the video preview's on-screen
right-click menu and the app's main Settings, synchronized with tray controls.

ON (default, consistent with previous releases): Windows titlebar "-" hides
the whole preview HWND to the existing tray icon; extended HDMI output no
longer displays the preview until restored. OFF: "-" does an ordinary Windows
minimize, without implicitly hiding the HWND. Both modes leave the other
"hide taskbar button but KEEP video visible" feature separate/unchanged.

Right-click directly INSIDE the child video surface to see the preview menu.
Only the real preview parent owns menus/config; no secondary tray/video windows
or capture/render loop changes are involved.
"""
import os
from pathlib import Path
root=Path(os.environ["RITSCHY_SOURCE"])
def patch(path, old, new):
    file=root/path
    s=file.read_text(encoding="utf-8")
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f"{path}: expected one anchor, found {n}: {old[:155]!r}")
    file.write_text(s.replace(old,new,1),encoding="utf-8")
    print("Patched", path)

# Shared single-key patch API must accept changes made from every surface.
patch("MirrorConfig.cs",
'''    public bool HidePreviewTaskbarButton { get; set; } = true;''',
'''    public bool HidePreviewTaskbarButton { get; set; } = true;
    // Independent of hiding ONLY the preview's taskbar button: toggles
    // whether pressing the real Windows minimize button hides the WHOLE
    // preview to the existing tray icon or does a normal Windows minimize.
    [JsonPropertyName("minimize_preview_to_tray")]
    public bool MinimizePreviewToTray { get; set; } = true;''')

patch("MirrorConfig.cs",
'''        "hide_preview_taskbar_button",''',
'''        "hide_preview_taskbar_button", "minimize_preview_to_tray",''')

# Use the correct full-name of the parent preview and the same config file
# already used by the tray and main Settings window.
patch("Win32Window.cs",
'''    private const uint WmPreviewTaskbarButton = 0x8052; // WM_APP + 0x52''',
'''    private const uint WmPreviewTaskbarButton = 0x8052; // WM_APP + 0x52

    private const uint MfString = 0x0000, MfChecked = 0x0008;
    private const uint TpmReturnCmd = 0x0100, TpmRightButton = 0x0002;
    private const uint ToggleMinimizeTrayMenuId = 0x5201;
    private static string PreviewConfigPath =>
        Path.Combine(AppContext.BaseDirectory, "mirror_config.json");

    // Native UI-thread message handlers can notify the existing tray host,
    // which marshals back to its own WinForms UI thread before updating the
    // main Settings checkbox and tray menu.
    public static event Action? PreviewMinimizeSettingChanged;

    private void ShowPreviewOverlayMenu()
    {
        if (Hwnd == IntPtr.Zero || !GetCursorPos(out POINT pt)) return;
        var popup = CreatePopupMenu();
        if (popup == IntPtr.Zero) return;
        try
        {
            bool enabled = MirrorConfig.Load(PreviewConfigPath).MinimizePreviewToTray;
            string label = enabled
                ? "Minimize to tray: ON (click to turn OFF)"
                : "Minimize to tray: OFF (click to turn ON)";
            if (!AppendMenu(popup, MfString | (enabled ? MfChecked : 0u),
                            ToggleMinimizeTrayMenuId, label))
                return;
            SetForegroundWindow(Hwnd);
            uint selection = TrackPopupMenu(popup, TpmReturnCmd | TpmRightButton,
                                            pt.X, pt.Y, 0, Hwnd, IntPtr.Zero);
            // Standard Windows menu-dismissal convention.
            PostMessage(Hwnd, 0 /*WM_NULL*/, IntPtr.Zero, IntPtr.Zero);
            if (selection != ToggleMinimizeTrayMenuId) return;
            bool next = !MirrorConfig.Load(PreviewConfigPath).MinimizePreviewToTray;
            MirrorConfig.MergePatch(PreviewConfigPath,
                new System.Text.Json.Nodes.JsonObject
                {
                    ["minimize_preview_to_tray"] = next,
                });
            if (MirrorConfig.Load(PreviewConfigPath).MinimizePreviewToTray == next)
                PreviewMinimizeSettingChanged?.Invoke();
        }
        catch (Exception)
        {
            // A menu action must never terminate the native preview's
            // message pump or corrupt video playback if config I/O fails.
        }
        finally { DestroyMenu(popup); }
    }''')

patch("Win32Window.cs",
'''    private static IntPtr StaticWndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)
    {
        Win32Window? self;
        lock (s_lock) s_windows.TryGetValue(hWnd, out self);
        return self != null
            ? self.InstanceWndProc(hWnd, msg, wParam, lParam)
            : DefWindowProc(hWnd, msg, wParam, lParam);
    }''',
'''    private static IntPtr StaticWndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)
    {
        Win32Window? self;
        lock (s_lock) s_windows.TryGetValue(hWnd, out self);
        if (self != null)
            return self.InstanceWndProc(hWnd, msg, wParam, lParam);

        // A normal native projector embeds exactly one child VIDEO HWND.
        // Intercept right-click UP there and show its parent preview's
        // toggle menu on the true owning UI thread. Do NOT turn a right
        // click in the picture into a minimize/hide operation.
        if (msg == 0x0205 /*WM_RBUTTONUP*/)
        {
            var parent = GetParent(hWnd);
            Win32Window? owner;
            lock (s_lock) s_windows.TryGetValue(parent, out owner);
            if (owner != null && owner._videoSurfaceHwnd == hWnd)
            {
                owner.ShowPreviewOverlayMenu();
                return IntPtr.Zero;
            }
        }
        return DefWindowProc(hWnd, msg, wParam, lParam);
    }''')

patch("Win32Window.cs",
'''                if (NativeMoveResize &&
                    (wParam.ToInt64() & 0xFFF0L) == 0xF020L /*SC_MINIMIZE*/)
                {
                    // In the normal framed preview, the real Windows
                    // minimize button now hides to the existing tray.
                    // Close still stops only the preview as before.
                    ShowWindow(hWnd, 0 /*SW_HIDE*/);
                    return IntPtr.Zero;
                }''',
'''                if (NativeMoveResize &&
                    (wParam.ToInt64() & 0xFFF0L) == 0xF020L /*SC_MINIMIZE*/ &&
                    MirrorConfig.Load(PreviewConfigPath).MinimizePreviewToTray)
                {
                    // ON: actual minimize button hides the WHOLE projector
                    // to the existing tray. OFF: fall through to normal
                    // DefWindowProc Windows minimize/restore behavior.
                    ShowWindow(hWnd, 0 /*SW_HIDE*/);
                    return IntPtr.Zero;
                }''')

patch("Win32Window.cs",
'''            return h != IntPtr.Zero && !IsWindowVisible(h);''',
'''            // Also allow the tray Show preview command to restore an
            // ordinary minimized window when minimize-to-tray is OFF,
            // even if its independent taskbar-button hiding is still ON.
            return h != IntPtr.Zero && (!IsWindowVisible(h) || IsIconic(h));''')

patch("Win32Window.cs",
'''    [DllImport("user32.dll")] private static extern bool IsWindowVisible(IntPtr hWnd);''',
'''    [DllImport("user32.dll")] private static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll")] private static extern bool IsIconic(IntPtr hWnd);
    [DllImport("user32.dll")] private static extern IntPtr GetParent(IntPtr hWnd);
    [DllImport("user32.dll")] private static extern IntPtr CreatePopupMenu();
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] private static extern bool AppendMenu(
        IntPtr hMenu, uint flags, uint idNewItem, string text);
    [DllImport("user32.dll", SetLastError = true)] private static extern uint TrackPopupMenu(
        IntPtr hMenu, uint flags, int x, int y, int reserved,
        IntPtr hwnd, IntPtr rect);
    [DllImport("user32.dll")] private static extern bool DestroyMenu(IntPtr hMenu);''')

# SettingsForm must not write its old cached toggle value when changing
# unrelated controls (same bug class as the previous taskbar setting).
patch("SettingsForm.cs",
'''    private bool _taskbarEditedInSettings;

    private readonly Panel _panel;''',
'''    private bool _taskbarEditedInSettings;
    private CheckBox _minimizeToTrayCheck = null!;
    private bool _minimizeEditedInSettings;

    private readonly Panel _panel;''')

patch("SettingsForm.cs",
'''            if (_taskbarEditedInSettings)
            {
                // A checkbox action saves only its own whitelisted key.''',
'''            if (_minimizeEditedInSettings)
            {
                bool minimizeToTray = _cfg.MinimizePreviewToTray;
                MirrorConfig.MergePatch(_engine.ConfigPath,
                    new System.Text.Json.Nodes.JsonObject
                    {
                        ["minimize_preview_to_tray"] = minimizeToTray,
                    });
                if (MirrorConfig.Load(_engine.ConfigPath).MinimizePreviewToTray != minimizeToTray)
                    throw new IOException("Minimize-to-tray choice was not saved.");
                _engine.Log($"[TRAY] Main Settings minimize-to-tray changed: enabled={minimizeToTray}.");
                return;
            }
            if (_taskbarEditedInSettings)
            {
                // A checkbox action saves only its own whitelisted key.''')

patch("SettingsForm.cs",
'''            _cfg.HidePreviewTaskbarButton = latest.HidePreviewTaskbarButton;
            _cfg.PreviewX = latest.PreviewX;''',
'''            _cfg.HidePreviewTaskbarButton = latest.HidePreviewTaskbarButton;
            _cfg.MinimizePreviewToTray = latest.MinimizePreviewToTray;
            _cfg.PreviewX = latest.PreviewX;''')

patch("SettingsForm.cs",
'''            SyncTaskbarButtonFromConfig();
        }
        catch (Exception ex)
        {
            _engine.Log("[TASKBAR] Settings save failed: " + ex.Message);
            SyncTaskbarButtonFromConfig();
        }
        finally { _taskbarEditedInSettings = false; }
    }''',
'''            SyncTaskbarButtonFromConfig();
            SyncMinimizeToTrayFromConfig();
        }
        catch (Exception ex)
        {
            _engine.Log("[TASKBAR] Settings save failed: " + ex.Message);
            SyncTaskbarButtonFromConfig();
            SyncMinimizeToTrayFromConfig();
        }
        finally
        {
            _taskbarEditedInSettings = false;
            _minimizeEditedInSettings = false;
        }
    }''')

patch("SettingsForm.cs",
'''    public void SyncTaskbarButtonFromConfig()
    {''',
'''    public void SyncMinimizeToTrayFromConfig()
    {
        if (IsDisposed || _minimizeToTrayCheck == null) return;
        bool saved = MirrorConfig.Load(_engine.ConfigPath).MinimizePreviewToTray;
        if (_cfg.MinimizePreviewToTray == saved && _minimizeToTrayCheck.Checked == saved)
            return;
        bool wasLoading = _loading;
        _loading = true;
        try
        {
            _cfg.MinimizePreviewToTray = saved;
            _minimizeToTrayCheck.Checked = saved;
        }
        finally { _loading = wasLoading; }
    }

    public void SyncTaskbarButtonFromConfig()
    {''')

patch("SettingsForm.cs",
'''        Note("Shortcut: Ctrl+Alt+T toggles ONLY its taskbar button; the HDMI video stays visible.");''',
'''        Note("Shortcut: Ctrl+Alt+T toggles ONLY its taskbar button; the HDMI video stays visible.");
        _minimizeToTrayCheck = CheckRow("Minimize preview to tray when clicking —",
                 _cfg.MinimizePreviewToTray,
                 v =>
                 {
                     _cfg.MinimizePreviewToTray = v;
                     _minimizeEditedInSettings = true;
                 });
        Note("Right-click inside the video preview to switch Minimize to tray ON/OFF.");
        Note("ON hides video to tray when minimized; OFF uses normal Windows minimize.");''')

# Add the same setting to the existing tray menu to make the state clear
# even when the preview or Settings UI is not currently visible.
patch("TrayContext.cs",
'''    private readonly ToolStripMenuItem _taskbarToggleItem;''',
'''    private readonly ToolStripMenuItem _taskbarToggleItem;
    private readonly ToolStripMenuItem _minimizeToTrayItem;''')

patch("TrayContext.cs",
'''        menu.Items.Add(_taskbarToggleItem);
        menu.Items.Add(new ToolStripMenuItem("Settings",''',
'''        menu.Items.Add(_taskbarToggleItem);
        _minimizeToTrayItem = new ToolStripMenuItem(
            "Minimize preview to tray: ON",
            null, (_, _) => ToggleMinimizeToTraySetting());
        menu.Items.Add(_minimizeToTrayItem);
        menu.Items.Add(new ToolStripMenuItem("Settings",''')

patch("TrayContext.cs",
'''        _taskbarToggleItem.Checked = taskbarIsHidden;''',
'''        _taskbarToggleItem.Checked = taskbarIsHidden;
        bool minimizeToTray = MirrorConfig.Load(_engine.ConfigPath).MinimizePreviewToTray;
        _minimizeToTrayItem.Checked = minimizeToTray;
        _minimizeToTrayItem.Text = minimizeToTray
            ? "Minimize preview to tray: ON (click for OFF)"
            : "Minimize preview to tray: OFF (click for ON)";
        _settings?.SyncMinimizeToTrayFromConfig();''')

patch("TrayContext.cs",
'''    private void RefreshUi()
    {
        bool running = _engine.IsRunning;''',
'''    private void ToggleMinimizeToTraySetting()
    {
        try
        {
            bool next = !MirrorConfig.Load(_engine.ConfigPath).MinimizePreviewToTray;
            MirrorConfig.MergePatch(_engine.ConfigPath,
                new System.Text.Json.Nodes.JsonObject
                {
                    ["minimize_preview_to_tray"] = next,
                });
            if (MirrorConfig.Load(_engine.ConfigPath).MinimizePreviewToTray != next)
            {
                _engine.Log("[TRAY] Minimize-to-tray toggle could not be saved.");
                return;
            }
            _engine.Log($"[TRAY] Tray menu minimize-to-tray: enabled={next}.");
            RefreshUi();
        }
        catch (Exception ex)
        {
            _engine.Log("[TRAY] Minimize-to-tray toggle failed: " + ex.Message);
        }
    }

    private void RefreshUi()
    {
        bool running = _engine.IsRunning;''')

patch("TrayContext.cs",
'''        _taskbarShortcut = new TaskbarShortcutFilter(TogglePreviewTaskbarButton);
        Application.AddMessageFilter(_taskbarShortcut);''',
'''        Win32Window.PreviewMinimizeSettingChanged += OnPreviewMinimizeSettingChanged;
        _taskbarShortcut = new TaskbarShortcutFilter(TogglePreviewTaskbarButton);
        Application.AddMessageFilter(_taskbarShortcut);''')

patch("TrayContext.cs",
'''    private void Quit()
    {
        _uiTimer.Stop();''',
'''    private void OnPreviewMinimizeSettingChanged()
    {
        // This event is raised by the native projector UI thread (not the
        // WinForms tray thread). Marshal before touching menus/checkboxes.
        try { _marshal.BeginInvoke((Action)RefreshUi); } catch { }
    }

    private void Quit()
    {
        _uiTimer.Stop();
        Win32Window.PreviewMinimizeSettingChanged -= OnPreviewMinimizeSettingChanged;''')

print("New native preview on-screen right-click switch + main Settings checkbox + tray control; independent normal/minimize-to-tray behavior with live bidirectional synchronization")
