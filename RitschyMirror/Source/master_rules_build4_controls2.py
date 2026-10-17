import os
from pathlib import Path
root=Path(os.environ.get('RITSCHY_SOURCE','/mnt/data/ritschy_build4_final2'))
p=root/'DiagnosticsManager.cs'
diag=p.read_text(encoding='utf-8')
anchor='''                // Verify restart-required controls explicitly communicate that fact while
                // their values persist immediately for the next restart.
                // Production Reset button path, not just SettingsActions directly.'''
insert='''                // Every safely testable combo box uses its actual SelectedIndexChanged production path.
                int comboOrdinal = 0;
                foreach (var combo in FindControls<ComboBox>(form))
                {
                    comboOrdinal++;
                    string id = "Settings ComboBox #" + comboOrdinal;
                    if (combo.Items.Count < 1)
                    {
                        Skip(id, "no selectable items are available in this CI desktop environment");
                        continue;
                    }
                    int beforeIndex = combo.SelectedIndex;
                    int nextIndex = combo.Items.Count > 1
                        ? (beforeIndex == 0 ? 1 : 0)
                        : (beforeIndex < 0 ? 0 : beforeIndex);
                    if (nextIndex == beforeIndex)
                    {
                        Skip(id, "only one already-selected value is available; no alternate state exists to exercise");
                        continue;
                    }
                    string beforeAppText = File.Exists(appPath) ? File.ReadAllText(appPath) : "";
                    string beforeMirrorText = File.Exists(mirrorPath) ? File.ReadAllText(mirrorPath) : "";
                    try
                    {
                        combo.SelectedIndex = nextIndex;
                        PumpFor(20);
                        bool changed = (File.Exists(appPath) ? File.ReadAllText(appPath) : "") != beforeAppText ||
                                       (File.Exists(mirrorPath) ? File.ReadAllText(mirrorPath) : "") != beforeMirrorText;
                        if (changed) Pass(id + " production selection path persisted state");
                        else Fail(id + " production selection path persisted state", "no project settings change detected");
                    }
                    catch (Exception ex) { Fail(id + " production selection path persisted state", SanitizeText(ex.Message)); }
                    finally { try { combo.SelectedIndex = beforeIndex; PumpFor(20); } catch { } }
                }

                int numericOrdinal = 0;
                foreach (var number in FindControls<NumericUpDown>(form))
                {
                    numericOrdinal++;
                    string id = "Settings NumericUpDown #" + numericOrdinal;
                    decimal before = number.Value;
                    decimal step = number.Increment > 0 ? number.Increment : 1;
                    decimal next = before + step <= number.Maximum ? before + step : before - step >= number.Minimum ? before - step : before;
                    if (next == before)
                    {
                        Skip(id, "numeric control has no alternate value inside its configured range");
                        continue;
                    }
                    string beforeAppText = File.Exists(appPath) ? File.ReadAllText(appPath) : "";
                    string beforeMirrorText = File.Exists(mirrorPath) ? File.ReadAllText(mirrorPath) : "";
                    try
                    {
                        number.Value = next;
                        PumpFor(20);
                        bool changed = (File.Exists(appPath) ? File.ReadAllText(appPath) : "") != beforeAppText ||
                                       (File.Exists(mirrorPath) ? File.ReadAllText(mirrorPath) : "") != beforeMirrorText;
                        if (changed) Pass(id + " production value-change path persisted state");
                        else Fail(id + " production value-change path persisted state", "no project settings change detected");
                    }
                    catch (Exception ex) { Fail(id + " production value-change path persisted state", SanitizeText(ex.Message)); }
                    finally { try { number.Value = before; PumpFor(20); } catch { } }
                }

                int textOrdinal = 0;
                foreach (var textBox in FindControls<TextBox>(form))
                {
                    textOrdinal++;
                    string id = "Settings TextBox #" + textOrdinal;
                    if (textBox.ReadOnly || !textBox.Enabled)
                    {
                        Skip(id, "control is read-only/disabled by design");
                        continue;
                    }
                    string before = textBox.Text;
                    string next = string.Equals(before, "localhost", StringComparison.OrdinalIgnoreCase) ? "+" : "localhost";
                    string beforeAppText = File.Exists(appPath) ? File.ReadAllText(appPath) : "";
                    string beforeMirrorText = File.Exists(mirrorPath) ? File.ReadAllText(mirrorPath) : "";
                    try
                    {
                        textBox.Text = next;
                        PumpFor(20);
                        bool changed = (File.Exists(appPath) ? File.ReadAllText(appPath) : "") != beforeAppText ||
                                       (File.Exists(mirrorPath) ? File.ReadAllText(mirrorPath) : "") != beforeMirrorText;
                        if (changed) Pass(id + " production text-change path persisted state");
                        else Fail(id + " production text-change path persisted state", "no project settings change detected");
                    }
                    catch (Exception ex) { Fail(id + " production text-change path persisted state", SanitizeText(ex.Message)); }
                    finally { try { textBox.Text = before; PumpFor(20); } catch { } }
                }

                // The two refresh buttons are safe read-only enumerations of currently available
                // displays/windows. Exercise the actual Click handlers; no external process is launched.
                var refreshButtons = FindControls<Button>(form).Where(b => b.Text == "↻").ToList();
                int refreshOk = 0;
                foreach (var refreshButton in refreshButtons)
                {
                    try { refreshButton.PerformClick(); PumpFor(20); refreshOk++; }
                    catch (Exception ex) { Fail("Settings refresh button production path", SanitizeText(ex.Message)); }
                }
                if (refreshButtons.Count == 2 && refreshOk == 2) Pass("both Settings display/window Refresh buttons execute production handlers safely");
                else Fail("both Settings display/window Refresh buttons execute production handlers safely",
                          $"found={refreshButtons.Count}, completed={refreshOk}");

                // Verify restart-required controls explicitly communicate that fact while
                // their values persist immediately for the next restart.
                // Production Reset button path, not just SettingsActions directly.'''
if anchor not in diag:
    raise RuntimeError('controls2 anchor not found')
diag=diag.replace(anchor,insert,1)
p.write_text(diag,encoding='utf-8')
print('Build 4 exhaustive safe Settings-control regression patch applied')
