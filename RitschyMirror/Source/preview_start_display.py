"""Add a preview-location selector to the English RitschyMirror build.

Runs after persistent_resizable_preview.py. Only changes initial placement
for windowed output; does not switch or duplicate the Windows display mode.
"""
import os
from pathlib import Path
root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, before, after):
    target = root / path
    content = target.read_text(encoding="utf-8")
    count = content.count(before)
    if count != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {count}: {before[:120]!r}")
    target.write_text(content.replace(before, after, 1), encoding="utf-8")
    print(f"Updated {path}")

patch("MirrorConfig.cs",
'    [JsonPropertyName("preview_maximized")] public bool PreviewMaximized { get; set; } = false;',
'''    [JsonPropertyName("preview_maximized")] public bool PreviewMaximized { get; set; } = false;
    // "main" = Windows primary display; "extended" = selected Target monitor;
    // "remember" = last saved preview location, falling back to Target display.
    [JsonPropertyName("preview_open_on")] public string PreviewOpenOn { get; set; } = "remember";''')

patch("MirrorConfig.cs",
'        "preview_x", "preview_y", "preview_width", "preview_height", "preview_maximized",',
'        "preview_x", "preview_y", "preview_width", "preview_height", "preview_maximized", "preview_open_on",')

patch("SettingsForm.cs",
'''        Note("Preview remembers the size you drag it to and restores it after maximizing.");''',
'''        Note("Preview remembers the size you drag it to and restores it after maximizing.");
        ComboRow("Preview opens on", new[] { "Main display", "Extended display", "Remember last position" },
                 _cfg.PreviewOpenOn switch
                 {
                     "main" => "Main display",
                     "extended" => "Extended display",
                     _ => "Remember last position",
                 },
                 s => _cfg.PreviewOpenOn = s switch
                 {
                     "Main display" => "main",
                     "Extended display" => "extended",
                     _ => "remember",
                 });
        Note("Main = Windows primary screen; Extended = selected Target monitor.");''')

# Persisted width/height can be reused regardless of placement. A forced choice
# overrides only saved position (not normal size), and maximizing then restores
# on the selected display. "remember" retains old behavior.
patch("MirrorEngine.cs",
'''            if (cfg.PreviewWidth >= 320 && cfg.PreviewWidth <= 8192
                && cfg.PreviewHeight >= 240 && cfg.PreviewHeight <= 8192)
            {
                bool intersectsDisplay = displays.Any(d =>
                    cfg.PreviewX < d.R - 64 && cfg.PreviewX + cfg.PreviewWidth > d.L + 64
                    && cfg.PreviewY < d.B - 64 && cfg.PreviewY + cfg.PreviewHeight > d.T + 64);
                if (intersectsDisplay)
                {
                    x = cfg.PreviewX; y = cfg.PreviewY;
                    outW = cfg.PreviewWidth; outH = cfg.PreviewHeight;
                }
            }''',
'''            bool hasSavedSize = cfg.PreviewWidth >= 320 && cfg.PreviewWidth <= 8192
                && cfg.PreviewHeight >= 240 && cfg.PreviewHeight <= 8192;
            if (hasSavedSize)
            {
                outW = cfg.PreviewWidth; outH = cfg.PreviewHeight;
            }
            switch ((cfg.PreviewOpenOn ?? "remember").Trim().ToLowerInvariant())
            {
                case "main":
                {
                    var main = System.Windows.Forms.Screen.PrimaryScreen;
                    if (main != null)
                    {
                        x = main.WorkingArea.Left + 30;
                        y = main.WorkingArea.Top + 30;
                    }
                    break;
                }
                case "extended":
                    // Default position already uses the selected Target display.
                    break;
                default: // remember last saved position, falling back to target screen
                    if (hasSavedSize)
                    {
                        bool intersectsDisplay = displays.Any(d =>
                            cfg.PreviewX < d.R - 64 && cfg.PreviewX + cfg.PreviewWidth > d.L + 64
                            && cfg.PreviewY < d.B - 64 && cfg.PreviewY + cfg.PreviewHeight > d.T + 64);
                        if (intersectsDisplay)
                        {
                            x = cfg.PreviewX; y = cfg.PreviewY;
                        }
                    }
                    break;
            }''')
print("Configurable preview startup display patch applied")
