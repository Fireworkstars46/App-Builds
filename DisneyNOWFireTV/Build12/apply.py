#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, hashlib, io, zipfile

BASE11 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'c06d83dd5d6b5d138ecb4c0fb7b59b78da62f9443ecdeb520744450de3987fd0',
    'app/build.gradle': '908cf7838c7f0b7894f7b4cc77ebbf6e19c311ed1b29bf62739e4099c5108842',
    'BUILD_INFO.md': '7afdba92291caf379820639d53989ced24d1ad459a6606308aaa7d5de1f60697',
    'README.md': '7e981821f0e8e1bd876aa7f46824b958623c4bcd4fefe71e3accf7b10ec93574',
    'tools/static_audit.py': '36d4e2cb8ee1ba501b7fb485d0447a820618ad80b28f9dbfb44749131f80b08b',
}

BUILD12 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': '396a0f25411290b0518fd5ba946ed659d9044be165bd186d2220bd276e457f9e',
    'app/build.gradle': 'a07d3b4c3051412453615db5b353aa46d8ecc8180ef57064fc52e4100182ae3b',
    'BUILD_INFO.md': '04c7fc874ca249b1086c5536a1cceffa9bbac83367094c65f0f8dc62e20b4316',
    'README.md': '324a3932f1c7d54f344825b9a4e7bdc9fbd2e56b0e22dcad8d3e454852b68583',
    'tools/static_audit.py': 'a8aec826583dbe60a84c1090a9bf530b4b1ec81616f757a78457d8f446e6e395',
}

PATCH_ZIP_SHA256 = '58ed13643b5bbd3497bfaf0ae5c96afaa262834798c2fc8ec34343d847937317'


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    args = parser.parse_args()
    root = Path(args.source).resolve()
    verify(root, BASE11, 'Build 11 baseline')

    parts_dir = Path(__file__).resolve().parent / 'patch_parts'
    parts = sorted(parts_dir.glob('part*.b64'))
    expected_names = [f'part{i:02d}.b64' for i in range(5)]
    if [p.name for p in parts] != expected_names:
        raise SystemExit('Build 12 patch payload must contain exactly part00.b64 through part04.b64')
    encoded = ''.join(p.read_text(encoding='ascii') for p in parts)
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f'Build 12 patch base64 decode failed: {exc}')
    if sha_bytes(payload) != PATCH_ZIP_SHA256:
        raise SystemExit('Build 12 patch ZIP SHA-256 mismatch')

    expected_paths = set(BUILD12)
    with zipfile.ZipFile(io.BytesIO(payload), 'r') as zf:
        names = set(zf.namelist())
        if names != expected_paths:
            raise SystemExit(f'Build 12 patch ZIP contains unexpected/missing entries: {sorted(names ^ expected_paths)}')
        for rel in sorted(expected_paths):
            data = zf.read(rel)
            if sha_bytes(data) != BUILD12[rel]:
                raise SystemExit(f'Build 12 payload entry hash mismatch: {rel}')
            out = (root / rel).resolve()
            if root not in out.parents:
                raise SystemExit(f'Unsafe Build 12 patch path: {rel}')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)

    verify(root, BUILD12, 'Build 12 result')
    print('Build 12 stability rollback/crash-stage patch applied and verified.')


if __name__ == '__main__':
    main()
