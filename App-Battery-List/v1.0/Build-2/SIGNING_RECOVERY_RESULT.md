# Signing Recovery Result — App Battery List v1.0 Build 2

Result: **PASS**

The permanent Android signing identity has passed the durable-backup and real-recovery gate.

## Safe verification evidence
- Package ID: `com.fireworkstars46.appbatterylist`
- Key alias: `appbatterylist-release`
- Expected permanent certificate SHA-256: `BB:7F:D5:23:C7:67:32:70:28:07:5F:F7:8B:1D:50:D2:B5:5B:79:57:1A:3E:46:51:C2:BF:23:F2:BB:4F:43:93`
- Signing backup ZIP SHA-256: `4854981262de190f390428f77bc28d591d829bbbc2df453de65fe8bba3148509`
- Durable recovery copy #1: private GitHub recovery repository.
- Durable recovery copy #2: user-controlled Dropbox signing-backup storage.
- Real recovery test: private GitHub Actions run `41659723022`, job `125999413354` — PASS.

The recovery test opened a recovered backup copy and verified the package identity, key alias, and exact certificate fingerprint. Private signing keys and passwords are not stored in this public report.

This metadata-only verification does not change application code or artifact behavior and therefore does not create a new Build.
