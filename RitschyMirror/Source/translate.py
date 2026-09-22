"""Translate UI text for an unofficial English RitschyMirror 1.3.2 build.
Upstream: https://github.com/RitschyRigz/ritschy-mirror
This script changes UI strings only; no rendering or capture logic is altered.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])
def edit(name, pairs):
    file = root / name
    text = file.read_text(encoding="utf-8")
    changed = 0
    for old, new in pairs:
        if old not in text:
            print(f"Optional UI text not present in {name}; skipping replacement")
            continue
        text = text.replace(old, new)
        changed += 1
    file.write_text(text, encoding="utf-8")
    print(f"Translated {name}: {changed} replacements")

edit('SettingsForm.cs', [
('RitschyMirror — Einstellungen', 'RitschyMirror — Settings'),
('Neustart (Struktur)', 'Restart (display)'),
('Schließen','Close'),
('↻ Auf Updates prüfen','↻ Check for updates'),
('Quelle / Ziel & Modus','Source / Target & Mode'),
('Quellen-Modus','Capture mode'),
('monitor = ganzer Bildschirm  ·  window = nur EIN Fenster / Vollbild-App','monitor = entire screen  ·  window = one app window'),
('(Fenster-Modus zeigt beim Raustaben NICHT deinen Desktop — sicherer.)','(Window mode does not show your desktop when switching apps.)'),
('Quell-Monitor  (Modus „monitor\\")','Source monitor (monitor mode)'),
('Fenster  (Modus „window\\")','Window (window mode)'),
('⚠ Gespeichertes Fenster \\"{WindowLabel()}\\" aktuell nicht offen (Auswahl bleibt gespeichert).','⚠ Saved window \\"{WindowLabel()}\\" is not open (selection is saved).'),
('Ziel-Monitor','Target monitor'),
('⚠ Gespeicherte Quelle \\"{LabelOf(_cfg.SourceKey, _cfg.SourceLabel)}\\" aktuell nicht verbunden.','⚠ Saved source \\"{LabelOf(_cfg.SourceKey, _cfg.SourceLabel)}\\" is disconnected.'),
('⚠ Gespeichertes Ziel \\"{LabelOf(_cfg.TargetKey, _cfg.TargetLabel)}\\" aktuell nicht verbunden.','⚠ Saved target \\"{LabelOf(_cfg.TargetKey, _cfg.TargetLabel)}\\" is disconnected.'),
('Layout-Modus','Layout mode'),
('Ausgabe-Modus','Output mode'),
('Bit-Tiefe','Bit depth'),
('Test-Fenster Breite','Test window width'),
('Test-Fenster Höhe','Test window height'),
('Struktur (Monitor/Modus/Bit depth/Fenster) wirkt erst nach Neustart.','Display/mode/bit depth/window changes require a restart.'),
('Bild / Tonemap','Image / Tone mapping'),
('Tonemap aktiv (HDR→SDR)','Enable tone mapping (HDR→SDR)'),
('Belichtung (Stops)','Exposure (stops)'),
('Sättigung','Saturation'),
('Kontrast','Contrast'),
('Weißpunkt (nits)','White point (nits)'),
('Quell-Spitze (nits)','Source peak (nits)'),
('Vertikal-Offset (px)','Vertical offset (px)'),
('Mauszeiger anzeigen','Show mouse cursor'),
('Schlafmodus / Monitor-Abschaltung verhindern (während Spiegelung)','Keep PC and display awake while mirroring'),
('Crop (nur Layout-Modus crop_region)','Crop (crop_region layout only)'),
('Crop Breite (0..1)','Crop width (0..1)'),
('Crop Höhe (0..1)','Crop height (0..1)'),
('Verbindung / Autostart','Connection / Startup'),
('HTTP-Agent aktiv (Cockpit-Fernsteuerung)','Enable HTTP agent (remote control)'),
('Spiegelung beim App-Start automatisch beginnen','Start mirroring when app opens'),
('App beim Windows-Login automatisch starten','Start app when signing in to Windows'),
('Agent-/Bind-/Port-Änderungen wirken nach App-Neustart.','Agent/bind/port changes require restarting the app.'),
('Header("Über")','Header("About")'),
('Updates prüfst du unten über „↻ Check for updates".','Use the button below to check for updates.'),
('"prüfe…"','"Checking…"'),
('Update-Prüfung fehlgeschlagen (offline?).','Could not check for updates (offline?).'),
('Update {r.LatestVersion} ist verfügbar (du hast v{AppInfo.Version}).\n\nJetzt zur Download-Seite?','Update {r.LatestVersion} is available (installed: v{AppInfo.Version}).\n\nOpen the download page now?'),
('Du hast die neueste Version (v{AppInfo.Version}).','You have the latest version (v{AppInfo.Version}).'),
('Login-Autostart setzen fehlgeschlagen: ','Could not set login startup: '),
])
edit('TrayContext.cs', [
('"Mirror starten"','"Start mirroring"'),
('"Einstellungen…"','"Settings…"'),
('"Log öffnen"','"Open log"'),
('"Beenden"','"Exit"'),
('Agent-Start fehlgeschlagen: ','Could not start agent: '),
('Autostart-Mirror übersprungen: ','Automatic mirroring skipped: '),
('RitschyMirror — Update verfügbar','RitschyMirror — Update available'),
('Version {r.LatestVersion} ist da. Klick zum Öffnen.','Version {r.LatestVersion} is available. Click to open.'),
('Log oeffnen fehlgeschlagen: ','Could not open log: '),
('"Mirror stoppen" : "Start mirroring"','"Stop mirroring" : "Start mirroring"'),
('"Agent aus"','"Agent off"'),
('(running ? "läuft" : "idle")','(running ? "running" : "idle")'),
])
edit('MirrorEngine.cs', [
('"Keine Displays gefunden"','"No displays found"'),
('"Keine Displays gefunden."','"No displays found."'),
('nicht verbunden"','is disconnected"'),
('ids, "Quell"','ids, "Source"'),
('ids, "Ziel"','ids, "Target"'),
('"Schritt: Fenster erstellen..."','"Step: Creating window..."'),
('"aktiv" : "AUS"','"on" : "OFF"'),
('"Quelle wechselte auf HDR → Tonemapping-Pfad aktiv."','"Source changed to HDR → tone mapping enabled."'),
('"Quelle wechselte auf SDR → 1:1-Durchreichung, kein Tonemapping."','"Source changed to SDR → direct output, no tone mapping."'),
('"WARN: Schlafmodus-Sperre fehlgeschlagen (SetThreadExecutionState)."','"WARNING: Could not prevent sleep (SetThreadExecutionState)."'),
('"Schlafmodus + Monitor-Abschaltung gesperrt (Mirroring laeuft)."','"Sleep and display shutdown prevented while mirroring."'),
])
edit('WindowEnum.cs', [
('"Keine aufnehmbaren Fenster gefunden"','"No capturable windows found"'),
('"Kein Fenster ausgewählt"','"No window selected"'),
("Fenster '{what}' nicht gefunden (läuft die Anwendung?)","Window '{what}' not found (is the app running?)"),
])
edit('WindowCapture.cs', [('"Aufnahme-Fenster wurde geschlossen"','"Capture window was closed"')])
edit('ControlAgent.cs', [('<p>dock.html fehlt.</p>','<p>dock.html is missing.</p>')])
edit('web/dock.html', [
('lang="de"','lang="en"'),
('>verbinde…<','>connecting…<'),
('Quelle / Ziel','Source / Target'),
('(Wechsel = Neustart)','(changes require restart)'),
('>Modus<','>Mode<'),
('monitor — ganzer Bildschirm','monitor — entire screen'),
('window — ein Fenster / Vollbild-App','window — one app window'),
('>Fenster<','>Window<'),
('Fensterliste aktualisieren','Refresh window list'),
('Quell-Mon.','Source screen'),
('Ziel-Mon.','Target screen'),
('Monitore aktualisieren','Refresh monitors'),
('„window" spiegelt nur das Fenster — beim Raustaben bleibt der Desktop unsichtbar.','Window mode mirrors just one window. Switching apps will not show your desktop.'),
('Layout &amp; Ausgabe','Layout &amp; Output'),
('(Ausgabe/Bit-Tiefe/Fenster = Neustart)','(output/bit depth/window require restart)'),
('>Ausgabe<','>Output<'),
('>Bit-Tiefe<','>Bit depth<'),
('>Fenster B×H<','>Window W×H<'),
('Bild / Tonemap','Image / Tone mapping'),
('Tonemap aktiv (HDR→SDR)','Enable tone mapping (HDR→SDR)'),
('>Sättigung<','>Saturation<'),
('>Kontrast<','>Contrast<'),
('>Belichtung<','>Exposure<'),
('>Weißpunkt<','>White point<'),
('>Quell-Spitze<','>Source peak<'),
('>Vert.-Offset<','>Vertical offset<'),
('Mauszeiger anzeigen','Show mouse cursor'),
('Schlafmodus / Monitor-Abschaltung verhindern','Keep PC and monitor awake'),
('>Breite<','>Width<'),
('>Höhe<','>Height<'),
('Agent nicht erreichbar','Agent unavailable'),
])
print("English UI translation complete")
