#!/usr/bin/env python3
import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

REQUIRED_CONFIG_KEYS = {
    'APP_NAME', 'PACKAGE_ID', 'VERSION_NAME', 'VERSION_CODE', 'BUILD_NUMBER',
    'TAG_NAME', 'RELEASE_TITLE', 'ARTIFACT_FILENAME', 'APK_RELATIVE_PATH',
    'ANDROID_PLATFORM_PACKAGE', 'BUILD_TOOLS_VERSION', 'SDK_CHANNEL'
}


def fail(message: str) -> None:
    print(f'FAIL: {message}', file=sys.stderr)
    raise SystemExit(1)


def parse_env(path: Path) -> dict[str, str]:
    if not path.is_file():
        fail(f'missing release config: {path}')
    out: dict[str, str] = {}
    for lineno, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            fail(f'invalid config line {lineno}: expected KEY=VALUE')
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        if not re.fullmatch(r'[A-Z0-9_]+', key):
            fail(f'invalid config key on line {lineno}: {key}')
        out[key] = value
    missing = sorted(REQUIRED_CONFIG_KEYS - out.keys())
    if missing:
        fail('missing required config keys: ' + ', '.join(missing))
    return out


def normalize_fingerprint(text: str) -> str:
    compact = re.sub(r'[^0-9A-Fa-f]', '', text)
    if len(compact) != 64:
        fail('signer SHA-256 must contain exactly 64 hexadecimal digits')
    compact = compact.upper()
    return ':'.join(compact[i:i+2] for i in range(0, 64, 2))


def read_expected_signer(project_dir: Path) -> str:
    path = project_dir / 'signing' / 'EXPECTED_SIGNER_SHA256.txt'
    if not path.is_file():
        fail(f'missing expected signer metadata: {path}')
    text = path.read_text(encoding='utf-8').strip()
    if not text or 'PENDING' in text.upper() or 'SET_' in text.upper():
        fail('expected signer SHA-256 is still pending')
    return normalize_fingerprint(text)


def verify_recovery_gate(project_dir: Path, expected: str) -> None:
    path = project_dir / 'signing' / 'BACKUP_RECOVERY_STATUS.txt'
    if not path.is_file():
        fail(f'missing backup recovery status: {path}')
    lines = [x.strip() for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
    if not lines or lines[0].upper() != 'PASS':
        fail('durable backup + real recovery-test gate is not PASS')
    fields = {}
    for line in lines[1:]:
        if '=' in line:
            k, v = line.split('=', 1)
            fields[k.strip()] = v.strip()
    recovered = fields.get('VerifiedFingerprint')
    if not recovered:
        fail('BACKUP_RECOVERY_STATUS.txt lacks VerifiedFingerprint=... evidence')
    if normalize_fingerprint(recovered) != expected:
        fail('recovered-backup fingerprint does not match expected permanent signer')


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        fail(f'command failed ({proc.returncode}): {" ".join(cmd)}\n{proc.stdout}')
    return proc.stdout


def verify_apk(apk: Path, config: dict[str, str], expected_signer: str, aapt: str, apksigner: str) -> None:
    if not apk.is_file():
        fail(f'APK not found: {apk}')

    badging = run([aapt, 'dump', 'badging', str(apk)])
    first = next((line for line in badging.splitlines() if line.startswith('package:')), '')
    if not first:
        fail('aapt did not return package metadata')

    def attr(name: str) -> str:
        m = re.search(rf"{re.escape(name)}='([^']*)'", first)
        return m.group(1) if m else ''

    actual_package = attr('name')
    actual_version_code = attr('versionCode')
    actual_version_name = attr('versionName')
    if actual_package != config['PACKAGE_ID']:
        fail(f'package mismatch: expected {config["PACKAGE_ID"]}, got {actual_package}')
    if actual_version_code != str(config['VERSION_CODE']):
        fail(f'versionCode mismatch: expected {config["VERSION_CODE"]}, got {actual_version_code}')
    if actual_version_name != config['VERSION_NAME']:
        fail(f'versionName mismatch: expected {config["VERSION_NAME"]}, got {actual_version_name}')

    signer = run([apksigner, 'verify', '--print-certs', str(apk)])
    m = re.search(r'Signer #1 certificate SHA-256 digest:\s*([0-9A-Fa-f:]+)', signer)
    if not m:
        fail('apksigner did not return signer SHA-256 digest')
    actual_signer = normalize_fingerprint(m.group(1))
    if actual_signer != expected_signer:
        fail(f'signer mismatch: expected {expected_signer}, got {actual_signer}')

    digest = hashlib.sha256(apk.read_bytes()).hexdigest()
    print('PASS: release identity verified')
    print(f'Package={actual_package}')
    print(f'VersionName={actual_version_name}')
    print(f'VersionCode={actual_version_code}')
    print(f'SignerSHA256={actual_signer}')
    print(f'APK_SHA256={digest}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Fail-closed Android release identity verification.')
    parser.add_argument('--project-dir', required=True)
    parser.add_argument('--apk')
    parser.add_argument('--aapt')
    parser.add_argument('--apksigner')
    parser.add_argument('--metadata-only', action='store_true')
    args = parser.parse_args()

    project = Path(args.project_dir).resolve()
    config = parse_env(project / 'release' / 'RELEASE_CONFIG.env')
    expected = read_expected_signer(project)
    verify_recovery_gate(project, expected)

    if args.metadata_only:
        print('PASS: release metadata and recovery gate are valid')
        return

    if not args.apk or not args.aapt or not args.apksigner:
        fail('--apk, --aapt, and --apksigner are required unless --metadata-only is used')
    verify_apk(Path(args.apk).resolve(), config, expected, args.aapt, args.apksigner)


if __name__ == '__main__':
    main()
