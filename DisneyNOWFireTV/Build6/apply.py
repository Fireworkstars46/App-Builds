#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, hashlib, io, zipfile

BASE5 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': '4a11b7386f5a16bf4679d1c8bb81e1f33c742bab855ce9f0285ce45c7464e978',
    'app/build.gradle': '80b3508c6fd672b6ab6352a32ea59f049df5884e4b405503c7302a00f2ed24cc',
    'README.md': 'ccead2d7ebf678cfe14c3187152d2aab1e0636b81220816044572b7d1fac8b0f',
    'BUILD_INFO.md': '85b2af76e57f26d99c88b87fe130bfd2ef1be116737558390832e1b484183451',
    'tools/static_audit.py': '84ca43e5c0f15902e9b92be3a70d569edcd603106e7f54188e0bc7389fa48e18',
}

BUILD6 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'aea6a4445e6ecf4c380d1544dd5ffc130d0564b647695c97d8248a360c9e109e',
    'app/build.gradle': '223ba80917e67743f82bf54878cc2124d812307da40fb9127f0d7340067c2d18',
    'README.md': '85798fa58e349562f5cd2ecd649bc4a86e7942a39bdb527c4147a44220a44820',
    'BUILD_INFO.md': 'f55ee67039f396d08b2d7542d53158bff09226edcd462b890a5bd44e6aa0b835',
    'tools/static_audit.py': 'fed635f3962045bb0067eb0d031c012af51e296b9fd7fec957ad38b03cadb647',
}

PATCH_ZIP_SHA256 = '592c5309be5030895e1e714ca24f6ad211a1f457f120307295cf04edf2b77d97'


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
    verify(root, BASE5, 'Build 5 baseline')

    parts_dir = Path(__file__).resolve().parent / 'patch_parts'
    parts = sorted(parts_dir.glob('part*.b64'))
    if [p.name for p in parts] != [f'part{i:02d}.b64' for i in range(5)]:
        raise SystemExit('Build 6 patch payload must contain exactly part00.b64 through part04.b64')
    encoded = ''.join(p.read_text(encoding='ascii') for p in parts)
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f'Build 6 patch base64 decode failed: {exc}')
    if sha_bytes(payload) != PATCH_ZIP_SHA256:
        raise SystemExit('Build 6 patch ZIP SHA-256 mismatch')

    expected_paths = set(BUILD6)
    with zipfile.ZipFile(io.BytesIO(payload), 'r') as zf:
        names = set(zf.namelist())
        if names != expected_paths:
            raise SystemExit(f'Build 6 patch ZIP contains unexpected/missing entries: {sorted(names ^ expected_paths)}')
        for rel in sorted(expected_paths):
            data = zf.read(rel)
            if sha_bytes(data) != BUILD6[rel]:
                raise SystemExit(f'Build 6 payload entry hash mismatch: {rel}')
            out = (root / rel).resolve()
            if root not in out.parents:
                raise SystemExit(f'Unsafe Build 6 patch path: {rel}')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)

    verify(root, BUILD6, 'Build 6 result')
    print('Build 6 zoom/video/login compatibility patch applied and verified.')


if __name__ == '__main__':
    main()
