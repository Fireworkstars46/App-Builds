"""Fix the taskbar shortcut instantly undoing itself and add clear tray feedback.

The existing keyboard/menu toggle called MirrorConfig.MergePatch to persist
hide_preview_taskbar_button, but the property was never added to MergePatch's
LiveKeys or StructKeys whitelist. MergePatch silently DROPPED that value.
The 1s tray timer then re-read the unchanged config and reapplied the old
visibility preference, causing the taskbar button to appear briefly and
disappear again. The tray menu text was also fixed and only its small check
mark could change.

Add the key to the LIVE whitelist, display explicit "Hide"/"Show" menu text
from the persisted preference, and log shortcut actions plus persist failures.
Neither window's visibility nor physical HDMI output is changed.
"""
import os
from pathlib import Path

root=Path(os.environ["RITSCHY_SOURCE"])
def patch(path,old,new):
    p=root/path
    s=p.read_text(encoding="utf-8")
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f"{path}: expected one anchor, got {n}: {old[:150]!r}")
    p.write_text(s.replace(old,new,1),encoding="utf-8")
    print("Patched",path)

patch("MirrorConfig.cs",
'''        "preview_x", "preview_y", "preview_width", "preview_height", "preview_maximized", "preview_open_on",''',
'''        "preview_x", "preview_y", "preview_width", "preview_height", "preview_maximized", "preview_open_on",
        "hide_preview_taskbar_button",''')

patch("TrayContext.cs",
'''            MirrorConfig.MergePatch(_engine.ConfigPath, new System.Text.Json.Nodes.JsonObject
            {
                ["hide_preview_taskbar_button"] = hideButton,
            });
            // Apply promptly; RefreshUi also reapplies on any new HWND.
            Win32Window.RequestPreviewTaskbarButton(!hideButton);
            _lastTaskbarHidden = null;
            _taskbarHeartbeat = 0;
            _taskbarToggleItem.Checked = hideButton;''',
'''            MirrorConfig.MergePatch(_engine.ConfigPath, new System.Text.Json.Nodes.JsonObject
            {
                ["hide_preview_taskbar_button"] = hideButton,
            });
            // MergePatch has a whitelist: verify the exact saved value before
            // manipulating Windows so a failed save never flashes then reverts.
            bool saved = MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;
            if (saved != hideButton)
            {
                _engine.Log("[TASKBAR] Could not persist taskbar button preference; leaving it unchanged.");
                return;
            }
            bool sent = Win32Window.RequestPreviewTaskbarButton(!hideButton);
            _lastTaskbarHidden = null;
            _taskbarHeartbeat = 0;
            _taskbarToggleItem.Checked = hideButton;
            _taskbarToggleItem.Text = hideButton
                ? "Show preview taskbar button (keep video visible)    Ctrl+Alt+T"
                : "Hide preview taskbar button (keep video visible)    Ctrl+Alt+T";
            _engine.Log($"[TASKBAR] User toggled: hidden={hideButton}, saved={saved}, preview_command_sent={sent}.");''')

patch("TrayContext.cs",
'''        _taskbarToggleItem.Checked =
            MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;

        // Independently of 'Hide preview to tray':''',
'''        bool taskbarIsHidden = MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;
        _taskbarToggleItem.Checked = taskbarIsHidden;
        _taskbarToggleItem.Text = taskbarIsHidden
            ? "Show preview taskbar button (keep video visible)    Ctrl+Alt+T"
            : "Hide preview taskbar button (keep video visible)    Ctrl+Alt+T";

        // Independently of 'Hide preview to tray':''')

print("Taskbar hotkey preference now survives config reload; menu label reflects actual saved state")
