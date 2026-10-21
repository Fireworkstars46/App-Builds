#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, io, zipfile

BASE6 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'aea6a4445e6ecf4c380d1544dd5ffc130d0564b647695c97d8248a360c9e109e',
    'app/build.gradle': '223ba80917e67743f82bf54878cc2124d812307da40fb9127f0d7340067c2d18',
    'README.md': '85798fa58e349562f5cd2ecd649bc4a86e7942a39bdb527c4147a44220a44820',
    'BUILD_INFO.md': 'f55ee67039f396d08b2d7542d53158bff09226edcd462b890a5bd44e6aa0b835',
    'tools/static_audit.py': 'fed635f3962045bb0067eb0d031c012af51e296b9fd7fec957ad38b03cadb647',
}

BUILD7 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': '3084760fde00b8d73dfde055843e2a52c38416556586301a88a953c54fd810a6',
    'app/build.gradle': '8a0f531bea2bc2a234a0b42250920dfb177d4aff58a263e0648958a8ce210c80',
    'README.md': 'c7304e1be0314387ca146e26b9cdd0bd05ea651d47d3f91e5b24532feccba5d5',
    'BUILD_INFO.md': 'a3431d932e47316afd0a672aacf9389a2c2a240c0803a95bec2e0ff5529f2a2a',
    'tools/static_audit.py': 'e066ab1a99b72927b77d25ee879852c4f9dd99867f4f9c1563e6e84c0bf56b39',
}

PATCH_ZIP_SHA256 = '8b49048fe6c5a8d988738dc0e7dce688ae09db0cbc1586525394a7ce7351edfd'


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
    verify(root, BASE6, 'Build 6 baseline')

    patch_path = Path(__file__).resolve().parent / 'build7-changed-files.zip'
    if not patch_path.is_file():
        raise SystemExit('Build 7 patch ZIP is missing')
    payload = patch_path.read_bytes()
    if sha_bytes(payload) != PATCH_ZIP_SHA256:
        raise SystemExit('Build 7 patch ZIP SHA-256 mismatch')

    expected_paths = set(BUILD7)
    with zipfile.ZipFile(io.BytesIO(payload), 'r') as zf:
        names = set(zf.namelist())
        if names != expected_paths:
            raise SystemExit(f'Build 7 patch ZIP contains unexpected/missing entries: {sorted(names ^ expected_paths)}')
        for rel in sorted(expected_paths):
            data = zf.read(rel)
            if sha_bytes(data) != BUILD7[rel]:
                raise SystemExit(f'Build 7 payload entry hash mismatch: {rel}')
            out = (root / rel).resolve()
            if root not in out.parents:
                raise SystemExit(f'Unsafe Build 7 patch path: {rel}')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)

    verify(root, BUILD7, 'Build 7 result')
    print('Build 7 live-zoom/compact-cursor/Silk-fallback patch applied and verified.')


if __name__ == '__main__':
    main()
