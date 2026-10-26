#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, hashlib, io, zipfile

BASE8 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'e63e0e7281456aa8e6e5304e264b445649567422491643946764e7182995d36f',
    'app/build.gradle': '7121fac1d053df10032211cf64f0a0c83bd1275fb39650bed15198411a47d2ae',
    'BUILD_INFO.md': '6ff421712fa8d042fa498e92b27cff83af02de4e42d6edd4d560ef272d725b84',
    'README.md': 'b22a13ffe5683412ced7823509e2c9cb042b825ab2d3d1832155e31d2c18252d',
    'tools/static_audit.py': '312100d25519191a05c5a755a867dd2134710a1407062f74869dabf7a8889c48',
}

BUILD9 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'c2b60181021f21d25d80f92fbf7da1b30febb38f86294fc5550b93ef6e674de4',
    'app/build.gradle': '8f7082922fe1264e7ed25659e957eaa453a43847ea732a1b3f2928e53cfbc135',
    'BUILD_INFO.md': 'aa019ab7b7b3df03ce855eacc10308142402de2a4bce96f4dd8b710fa1d5c116',
    'README.md': '7229a72cf329158d5b7515ea6a73766039ce1dcbf6cee1bc18c9e671c275123f',
    'tools/static_audit.py': '0cd430ff7eee9b9fec6d9c1959d3bc8fbba11d3283ce5697c9708aa30fdcab25',
}

PATCH_ZIP_SHA256 = '8e9932cb16801f52751a281a881d9f24aaf2756a8b6dd14c6a4891fe940546f9'


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
    verify(root, BASE8, 'Build 8 baseline')

    parts_dir = Path(__file__).resolve().parent / 'patch_parts'
    parts = sorted(parts_dir.glob('part*.b64'))
    expected_names = [f'part{i:02d}.b64' for i in range(4)]
    if [p.name for p in parts] != expected_names:
        raise SystemExit('Build 9 patch payload must contain exactly part00.b64 through part03.b64')
    encoded = ''.join(p.read_text(encoding='ascii') for p in parts)
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f'Build 9 patch base64 decode failed: {exc}')
    if sha_bytes(payload) != PATCH_ZIP_SHA256:
        raise SystemExit('Build 9 patch ZIP SHA-256 mismatch')

    expected_paths = set(BUILD9)
    with zipfile.ZipFile(io.BytesIO(payload), 'r') as zf:
        names = set(zf.namelist())
        if names != expected_paths:
            raise SystemExit(f'Build 9 patch ZIP contains unexpected/missing entries: {sorted(names ^ expected_paths)}')
        for rel in sorted(expected_paths):
            data = zf.read(rel)
            if sha_bytes(data) != BUILD9[rel]:
                raise SystemExit(f'Build 9 payload entry hash mismatch: {rel}')
            out = (root / rel).resolve()
            if root not in out.parents:
                raise SystemExit(f'Unsafe Build 9 patch path: {rel}')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)

    verify(root, BUILD9, 'Build 9 result')
    print('Build 9 privacy-safe Debug Mode patch applied and verified.')


if __name__ == '__main__':
    main()
