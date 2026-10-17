import os
from pathlib import Path
root=Path(os.environ.get('RITSCHY_SOURCE','/mnt/data/ritschy_build4_final2'))
p=root/'DiagnosticsManager.cs'
diag=p.read_text(encoding='utf-8')
anchor='''                // Verify restart-required controls explicitly communicate that fact while
                // their values persist immediately for the next restart.
                // Production Reset button path, not just SettingsActions directly.'''
insert='''                // Button.PerformClick only executes a real WinForms Click path when the
                // control can be selected. Keep the real Settings form alive but invisible
                // while exercising safe production button handlers.
                form.ShowInTaskbar = false;
                form.Opacity = 0.0;
                form.Show();
                PumpFor(30);

                // Every safely testable combo box uses its actual SelectedIndexChanged production path.
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

                // NumericUpDown and other composite WinForms controls contain internal
                // TextBox-derived editor children. Those are implementation details, not
                // separate RitschyMirror settings. Exercise only TextBox controls the app
                // actually created as settings controls.
                int textOrdinal = 0;
                foreach (var textBox in FindControls<TextBox>(form).Where(tb => tb.GetType() == typeof(TextBox)))
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

                // Exercise the actual refresh-button Click handlers and prove they ran by
                // corrupting the adjacent combo's item list first. A successful production
                // refresh must remove the sentinel even if the environment has no windows.
                var refreshButtons = FindControls<Button>(form).Where(b => b.Text == "↻").ToList();
                int refreshOk = 0;
                foreach (var refreshButton in refreshButtons)
                {
                    try
                    {
                        var adjacent = FindControls<ComboBox>(form)
                            .OrderBy(c => Math.Abs(c.Top - refreshButton.Top) + Math.Abs(c.Left - refreshButton.Left))
                            .FirstOrDefault();
                        if (adjacent == null)
                        {
                            Fail("Settings refresh button production path", "adjacent ComboBox not found");
                            continue;
                        }
                        const string sentinel = "__RITSCHYMIRROR_SAFE_SELF_TEST_REFRESH__";
                        adjacent.Items.Clear();
                        adjacent.Items.Add(sentinel);
                        adjacent.SelectedIndex = 0;
                        refreshButton.PerformClick();
                        PumpFor(30);
                        bool handlerRan = !adjacent.Items.Contains(sentinel);
                        if (handlerRan) refreshOk++;
                        else Fail("Settings refresh button production path", "sentinel remained; Click handler did not repopulate control");
                    }
                    catch (Exception ex) { Fail("Settings refresh button production path", SanitizeText(ex.Message)); }
                }
                if (refreshButtons.Count == 2 && refreshOk == 2) Pass("both Settings display/window Refresh buttons execute production handlers and repopulate controls");
                else Fail("both Settings display/window Refresh buttons execute production handlers and repopulate controls",
                          $"found={refreshButtons.Count}, verified={refreshOk}");

                // Verify restart-required controls explicitly communicate that fact while
                // their values persist immediately for the next restart.
                // Production Reset button path, not just SettingsActions directly.'''
if anchor not in diag:
    raise RuntimeError('controls2 anchor not found')
diag=diag.replace(anchor,insert,1)
p.write_text(diag,encoding='utf-8')
print('Build 4 exhaustive safe Settings-control regression patch applied')
