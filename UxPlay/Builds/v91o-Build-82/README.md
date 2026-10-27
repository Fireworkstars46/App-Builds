# UxPlay Quality Launcher Full — v91o Build 82

Corrective Direct USB build based on the exact Build 81 source.

## Confirmed Build 81 regression
The once-per-build Direct USB phone-confirmation reminder used a blocking system MessageBox. On the user's Windows PC the backend could exit while that MessageBox remained open, and clicking OK did not reliably dismiss the stuck prompt.

## Build 82 correction
- Replaces that Direct USB confirmation MessageBox with a project-owned fixed dialog.
- OK explicitly sets DialogResult.OK and closes the dialog immediately.
- Cancel explicitly closes the dialog and restores/stops USB through the existing path.
- A 100 ms backend watcher auto-closes the prompt with DialogResult.Abort if the Direct USB backend exits.
- The backend Exited handler also closes any active phone-confirmation prompt as a second fail-safe.
- The prompt acknowledgement is saved only after a real OK result. Backend-exit/Cancel does not falsely acknowledge the Build.
- The once-per-Build persistence behavior from Build 81 remains.
- The persistent black Direct USB renderer from Build 81 remains.
- Known-good Build 80 Wi-Fi renderer/title-bar pin behavior is preserved.
- Direct USB backend exit diagnostics from Build 81 are preserved.

The launcher reminder does not control iOS prompts; iOS-owned Trust/Allow/passcode prompts remain controlled by iOS.

## Validation state
Static/source audit: 79/79 PASS.
ZIP integrity: PASS.
Windows compile, installer build, real iPhone/USB behavior, and the actual OK/auto-close regression are NOT TESTED here.
Build 82 is NOT DONE / PENDING until those checks run on Windows.
