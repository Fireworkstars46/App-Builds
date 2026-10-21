#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, hashlib, io, zipfile

BASE7 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': '3084760fde00b8d73dfde055843e2a52c38416556586301a88a953c54fd810a6',
    'app/build.gradle': '8a0f531bea2bc2a234a0b42250920dfb177d4aff58a263e0648958a8ce210c80',
    'README.md': 'c7304e1be0314387ca146e26b9cdd0bd05ea651d47d3f91e5b24532feccba5d5',
    'BUILD_INFO.md': 'a3431d932e47316afd0a672aacf9389a2c2a240c0803a95bec2e0ff5529f2a2a',
    'tools/static_audit.py': 'e066ab1a99b72927b77d25ee879852c4f9dd99867f4f9c1563e6e84c0bf56b39',
}

STAGE8 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': '0c2ce6daeb8a7cf0a1b5bdcf37fa160228b97a0051c3571ce19d88df29dbdd2e',
    'app/build.gradle': '7121fac1d053df10032211cf64f0a0c83bd1275fb39650bed15198411a47d2ae',
    'README.md': 'b22a13ffe5683412ced7823509e2c9cb042b825ab2d3d1832155e31d2c18252d',
    'BUILD_INFO.md': '6ff421712fa8d042fa498e92b27cff83af02de4e42d6edd4d560ef272d725b84',
    'tools/static_audit.py': '8b22e32a955bd7d7706a5c22ec0da84efd2d2abe893c671f1dbbd7dacc8908e9',
}

BUILD8 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'e63e0e7281456aa8e6e5304e264b445649567422491643946764e7182995d36f',
    'app/build.gradle': '7121fac1d053df10032211cf64f0a0c83bd1275fb39650bed15198411a47d2ae',
    'README.md': 'b22a13ffe5683412ced7823509e2c9cb042b825ab2d3d1832155e31d2c18252d',
    'BUILD_INFO.md': '6ff421712fa8d042fa498e92b27cff83af02de4e42d6edd4d560ef272d725b84',
    'gradle.properties': '19054d8ae377b73924f5570a2092f90741d86c973c1ea19e71b0791ae1085cee',
    'tools/static_audit.py': '312100d25519191a05c5a755a867dd2134710a1407062f74869dabf7a8889c48',
}

PATCH_ZIP_SHA256 = '4deb1686394d73ae6e3405094ffbf4b411db3db06d6c08e842a4837d9afd370c'
GRADLE_PROPERTIES_TEXT = '# AndroidX is required by AndroidX Media3 used by Build 8\'s experimental native player.\nandroid.useAndroidX=true\n'


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def verify(root: Path, expected: dict[str, str], label: str) -> None:
    failures = []
    for rel, wanted in expected.items():
        path = root / rel
        got = sha_file(path) if path.is_file() else 'missing'
        if got != wanted:
            failures.append(f'{rel}: expected {wanted}, got {got}')
    if failures:
        raise SystemExit(label + ' hash verification failed:\n' + '\n'.join(failures))


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'Build 8 AndroidX correction expected one {label} match, got {count}')
    return text.replace(old, new, 1)


def apply_androidx_correction(root: Path) -> None:
    (root / 'gradle.properties').write_text(GRADLE_PROPERTIES_TEXT, encoding='utf-8', newline='\n')
    audit_path = root / 'tools' / 'static_audit.py'
    text = audit_path.read_text(encoding='utf-8')
    text = replace_once(text,
        "README = ROOT / 'README.md'\nREPORT = ROOT / 'build' / 'reports' / 'STATIC-AUDIT-v0.1-Build8.txt'",
        "README = ROOT / 'README.md'\nGRADLE_PROPERTIES = ROOT / 'gradle.properties'\nREPORT = ROOT / 'build' / 'reports' / 'STATIC-AUDIT-v0.1-Build8.txt'",
        'GRADLE_PROPERTIES declaration')
    text = replace_once(text,
        "for path in [APP_GRADLE, MANIFEST, MAIN, BUILD_INFO, README]:",
        "for path in [APP_GRADLE, MANIFEST, MAIN, BUILD_INFO, README, GRADLE_PROPERTIES]:",
        'required-file list')
    text = replace_once(text,
        "    gradle = manifest_text = main = build_info = readme = ''",
        "    gradle = manifest_text = main = build_info = readme = gradle_properties = ''",
        'failure defaults')
    text = replace_once(text,
        "    readme = README.read_text(encoding='utf-8')\n\n# Identity / build / dependency invariants.",
        "    readme = README.read_text(encoding='utf-8')\n    gradle_properties = GRADLE_PROPERTIES.read_text(encoding='utf-8')\n\n# Identity / build / dependency invariants.",
        'gradle.properties read')
    text = replace_once(text,
        "add('Media3 version pinned to 1.8.1', 'def media3_version = \"1.8.1\"' in gradle, 'last compatible line before minSdk 23 migration')\nfor dep in ['media3-exoplayer', 'media3-exoplayer-dash', 'media3-exoplayer-hls', 'media3-ui']:",
        "add('Media3 version pinned to 1.8.1', 'def media3_version = \"1.8.1\"' in gradle, 'last compatible line before minSdk 23 migration')\nadd('AndroidX mode enabled for Media3', 'android.useAndroidX=true' in gradle_properties, 'required by AndroidX Media3 dependencies')\nfor dep in ['media3-exoplayer', 'media3-exoplayer-dash', 'media3-exoplayer-hls', 'media3-ui']:",
        'AndroidX audit check')
    audit_path.write_text(text, encoding='utf-8', newline='\n')


def apply_media3_opt_in(root: Path) -> None:
    main_path = root / 'app' / 'src' / 'main' / 'java' / 'com' / 'fireworkstars46' / 'disneynowfiretv' / 'MainActivity.java'
    text = main_path.read_text(encoding='utf-8')
    text = replace_once(text,
        'import androidx.media3.common.Player;\n',
        'import androidx.media3.common.Player;\nimport androidx.media3.common.util.UnstableApi;\n',
        'Media3 UnstableApi import')
    text = replace_once(text,
        'public final class MainActivity extends Activity {',
        '@UnstableApi\npublic final class MainActivity extends Activity {',
        'Media3 UnstableApi class annotation')
    main_path.write_text(text, encoding='utf-8', newline='\n')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    args = parser.parse_args()
    root = Path(args.source).resolve()
    verify(root, BASE7, 'Build 7 baseline')

    parts_dir = Path(__file__).resolve().parent / 'patch_parts'
    parts = sorted(parts_dir.glob('part*.b64'))
    expected_names = [f'part{i:02d}.b64' for i in range(6)]
    if [p.name for p in parts] != expected_names:
        raise SystemExit('Build 8 patch payload must contain exactly part00.b64 through part05.b64')
    encoded = ''.join(p.read_text(encoding='ascii') for p in parts)
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f'Build 8 patch base64 decode failed: {exc}')
    if sha_bytes(payload) != PATCH_ZIP_SHA256:
        raise SystemExit('Build 8 patch ZIP SHA-256 mismatch')

    expected_paths = set(STAGE8)
    with zipfile.ZipFile(io.BytesIO(payload), 'r') as zf:
        names = set(zf.namelist())
        if names != expected_paths:
            raise SystemExit(f'Build 8 patch ZIP contains unexpected/missing entries: {sorted(names ^ expected_paths)}')
        for rel in sorted(expected_paths):
            data = zf.read(rel)
            if sha_bytes(data) != STAGE8[rel]:
                raise SystemExit(f'Build 8 payload entry hash mismatch: {rel}')
            out = (root / rel).resolve()
            if root not in out.parents:
                raise SystemExit(f'Unsafe Build 8 patch path: {rel}')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)

    verify(root, STAGE8, 'Build 8 staged result')
    apply_androidx_correction(root)
    apply_media3_opt_in(root)
    verify(root, BUILD8, 'Build 8 result')
    print('Build 8 hybrid-TV-shell/native-navigation/whole-page-zoom/Media3 patch applied and verified.')


if __name__ == '__main__':
    main()
