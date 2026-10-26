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

BUILD13 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': '2ace504d804fb354263c83e576c78910f2360e3f83ee25dd090260302190e055',
    'app/build.gradle': '03997107cdec224b322613b7efc98a93abe7972a12f898895fc437e89e5b7d27',
    'BUILD_INFO.md': '5df4ee811a42c92b83e0ca55d24098c6d43fd2d30b23275bd70f6c9836b17b74',
    'README.md': '1c99c15d377cd9d26cf5527f3169b07b4fb23087cd1323a6667b823e6c3c1d0e',
    'tools/static_audit.py': 'b12c3fb75f2579993154435a066c41abe5f23886d4a7907f0e3107cda3489a6c',
}

PATCH_ZIP_SHA256 = '8d9d2b49d6748724a612cefa0a1390ab8b807bb04a1452195d1e366b15cf99d3'
PATCH_PARTS = [
    'part00.b64',
    'part01a.b64',
    'part01b.b64',
    'part02.b64',
    'part03.b64',
    'part04.b64',
]


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
    parts = [parts_dir / name for name in PATCH_PARTS]
    missing = [p.name for p in parts if not p.is_file()]
    if missing:
        raise SystemExit('Build 13 patch payload missing parts: ' + ', '.join(missing))
    encoded = ''.join(p.read_text(encoding='ascii') for p in parts)
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f'Build 13 patch base64 decode failed: {exc}')
    if sha_bytes(payload) != PATCH_ZIP_SHA256:
        raise SystemExit('Build 13 patch ZIP SHA-256 mismatch')

    expected_paths = set(BUILD13)
    with zipfile.ZipFile(io.BytesIO(payload), 'r') as zf:
        names = set(zf.namelist())
        if names != expected_paths:
            raise SystemExit(f'Build 13 patch ZIP contains unexpected/missing entries: {sorted(names ^ expected_paths)}')
        for rel in sorted(expected_paths):
            data = zf.read(rel)
            if sha_bytes(data) != BUILD13[rel]:
                raise SystemExit(f'Build 13 payload entry hash mismatch: {rel}')
            out = (root / rel).resolve()
            if root not in out.parents:
                raise SystemExit(f'Unsafe Build 13 patch path: {rel}')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)

    verify(root, BUILD13, 'Build 13 result')
    print('Build 13 stability rollback/crash-stage patch applied and verified.')


if __name__ == '__main__':
    main()
