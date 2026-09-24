"""Synchronize the preview taskbar setting between the tray and SettingsForm.

Before: SettingsForm cached MirrorConfig when opened. Ctrl+Alt+T/tray edits
mirror_config.json, but the still-open checkbox did not change. Worse, an
unrelated GUI edit called _cfg.Save() on the stale cached object and silently
reverted the tray preference. Conversely, changing the GUI checkbox saved
the file but did not update the tray menu until its next timer tick.

Now: one persisted value is shared by both views. A tray action immediately
updates the open form, the tray's existing UI tick also reconciles external
changes, and each GUI checkbox change uses a SINGLE-KEY MergePatch and posts
the native window taskbar update immediately. Any other GUI SaveCfg preserves
the latest persisted taskbar preference before writing the rest of the
existing render/geometry config. No duplicate tray icons or window changes.
"""
import os
from pathlib import Path

root=Path(os.environ["RITSCHY_SOURCE"])
def patch(path,old,new):
    p=root/path
    s=p.read_text(encoding="utf-8")
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f"{path}: expected exactly one anchor, found {n}: {old[:160]!r}")
    p.write_text(s.replace(old,new,1),encoding="utf-8")
    print("Patched",path)

patch("SettingsForm.cs",
'''    private bool _loading;

    private readonly Panel _panel;''',
'''    private bool _loading;
    private CheckBox _taskbarButtonCheck = null!;
    // CheckRow always calls SaveCfg after its callback. A dedicated flag
    // makes the taskbar checkbox save ONLY its own config key instead of
    // overwriting unrelated fields with this form's old cached _cfg.
    private bool _taskbarEditedInSettings;

    private readonly Panel _panel;''')

patch("SettingsForm.cs",
'''    private void SaveCfg()
    {
        if (_loading) return;
        try
        {
            var latest = MirrorConfig.Load(_engine.ConfigPath);
            _cfg.PreviewX = latest.PreviewX;
            _cfg.PreviewY = latest.PreviewY;
            _cfg.PreviewWidth = latest.PreviewWidth;
            _cfg.PreviewHeight = latest.PreviewHeight;
            _cfg.PreviewMaximized = latest.PreviewMaximized;
            _cfg.Save(_engine.ConfigPath);
        }
        catch { }
    }''',
'''    private void SaveCfg()
    {
        if (_loading) return;
        try
        {
            if (_taskbarEditedInSettings)
            {
                // A checkbox action saves only its own whitelisted key.
                bool hideButton = _cfg.HidePreviewTaskbarButton;
                MirrorConfig.MergePatch(_engine.ConfigPath,
                    new System.Text.Json.Nodes.JsonObject
                    {
                        ["hide_preview_taskbar_button"] = hideButton,
                    });
                if (MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton != hideButton)
                    throw new IOException("Taskbar button choice was not saved.");
                Win32Window.RequestPreviewTaskbarButton(!hideButton);
                _engine.Log($"[TASKBAR] Settings checkbox changed: hidden={hideButton}, saved=True.");
                return;
            }

            // A tray hotkey or menu action may have changed the SAME field
            // while this SettingsForm was open. Preserve its latest saved
            // preference whenever saving ANY other Settings control.
            var latest = MirrorConfig.Load(_engine.ConfigPath);
            _cfg.HidePreviewTaskbarButton = latest.HidePreviewTaskbarButton;
            _cfg.PreviewX = latest.PreviewX;
            _cfg.PreviewY = latest.PreviewY;
            _cfg.PreviewWidth = latest.PreviewWidth;
            _cfg.PreviewHeight = latest.PreviewHeight;
            _cfg.PreviewMaximized = latest.PreviewMaximized;
            _cfg.Save(_engine.ConfigPath);
            SyncTaskbarButtonFromConfig();
        }
        catch (Exception ex)
        {
            _engine.Log("[TASKBAR] Settings save failed: " + ex.Message);
            SyncTaskbarButtonFromConfig();
        }
        finally { _taskbarEditedInSettings = false; }
    }

    /// <summary>Called by the tray host and whenever the Settings window
    /// is activated. Never fires the CheckRow saving callback while syncing:
    /// the tray/file preference is already persisted.</summary>
    public void SyncTaskbarButtonFromConfig()
    {
        if (IsDisposed || _taskbarButtonCheck == null) return;
        bool saved = MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;
        if (_cfg.HidePreviewTaskbarButton == saved && _taskbarButtonCheck.Checked == saved)
            return;
        bool wasLoading = _loading;
        _loading = true;
        try
        {
            _cfg.HidePreviewTaskbarButton = saved;
            _taskbarButtonCheck.Checked = saved;
        }
        finally { _loading = wasLoading; }
    }''')

patch("SettingsForm.cs",
'''        CheckRow("Hide preview taskbar button (keep preview visible)",
                 _cfg.HidePreviewTaskbarButton,
                 v => _cfg.HidePreviewTaskbarButton = v);''',
'''        _taskbarButtonCheck = CheckRow("Hide preview taskbar button (keep preview visible)",
                 _cfg.HidePreviewTaskbarButton,
                 v =>
                 {
                     _cfg.HidePreviewTaskbarButton = v;
                     _taskbarEditedInSettings = true;
                 });''')

patch("TrayContext.cs",
'''            _engine.Log($"[TASKBAR] User toggled: hidden={hideButton}, saved={saved}, preview_command_sent={sent}.");''',
'''            _engine.Log($"[TASKBAR] User toggled: hidden={hideButton}, saved={saved}, preview_command_sent={sent}.");
            _settings?.SyncTaskbarButtonFromConfig();
            RefreshUi();''')

patch("TrayContext.cs",
'''        bool taskbarIsHidden = MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;
        _taskbarToggleItem.Checked = taskbarIsHidden;''',
'''        bool taskbarIsHidden = MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;
        _settings?.SyncTaskbarButtonFromConfig();
        _taskbarToggleItem.Checked = taskbarIsHidden;''')

patch("TrayContext.cs",
'''        if (_settings is { IsDisposed: false }) { _settings.Activate(); return; }''',
'''        if (_settings is { IsDisposed: false })
        {
            _settings.SyncTaskbarButtonFromConfig();
            _settings.Activate();
            return;
        }''')

patch("TrayContext.cs",
'''        menu.Items.Add(new ToolStripMenuItem("Exit", null, (_, _) => Quit()));

        _tray = new NotifyIcon''',
'''        menu.Items.Add(new ToolStripMenuItem("Exit", null, (_, _) => Quit()));
        // Sync menu text/checkmark at opening, not just once per second.
        menu.Opening += (_, _) => RefreshUi();

        _tray = new NotifyIcon''')

print("Main Settings checkbox, tray menu and Ctrl+Alt+T now share the same saved taskbar preference in both directions")
