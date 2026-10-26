#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, hashlib, io, zipfile

BASE10 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'fa6a93ebaa12304da596b9f772cc8804679cc85b8f00d9331b4bd5edd53c7878',
    'app/build.gradle': 'd10998ac372a6a8faf88be8fbb9e7b37c065580a70fc4c641e6f424077b56e21',
    'BUILD_INFO.md': 'f07555a3d179842b1900879adfe1be971ac698a9b623dba58c8e80a1012b679a',
    'README.md': '1a9d5e58f141b095381b6dc206edf10a91438ed11927a5ddac6c62f29efa22d7',
    'tools/static_audit.py': 'c7e692fcfa11684b072aec3cb4be29dcdbc9fb2d34bbc180b48b396933e04223',
}

BUILD11 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'c06d83dd5d6b5d138ecb4c0fb7b59b78da62f9443ecdeb520744450de3987fd0',
    'app/build.gradle': '908cf7838c7f0b7894f7b4cc77ebbf6e19c311ed1b29bf62739e4099c5108842',
    'BUILD_INFO.md': '7afdba92291caf379820639d53989ced24d1ad459a6606308aaa7d5de1f60697',
    'README.md': '7e981821f0e8e1bd876aa7f46824b958623c4bcd4fefe71e3accf7b10ec93574',
    'tools/static_audit.py': '36d4e2cb8ee1ba501b7fb485d0447a820618ad80b28f9dbfb44749131f80b08b',
}

PATCH_ZIP_SHA256 = '1e0d92d0d32398ea96083f48c7a82253187a1718d12a17f7c71b51b1e454e048'


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
    verify(root, BASE10, 'Build 10 baseline')

    parts_dir = Path(__file__).resolve().parent / 'patch_parts'
    parts = sorted(parts_dir.glob('part*.b64'))
    expected_names = [f'part{i:02d}.b64' for i in range(5)]
    if [p.name for p in parts] != expected_names:
        raise SystemExit('Build 11 patch payload must contain exactly part00.b64 through part04.b64')
    encoded = ''.join(p.read_text(encoding='ascii') for p in parts)
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f'Build 11 patch base64 decode failed: {exc}')
    if sha_bytes(payload) != PATCH_ZIP_SHA256:
        raise SystemExit('Build 11 patch ZIP SHA-256 mismatch')

    expected_paths = set(BUILD11)
    with zipfile.ZipFile(io.BytesIO(payload), 'r') as zf:
        names = set(zf.namelist())
        if names != expected_paths:
            raise SystemExit(f'Build 11 patch ZIP contains unexpected/missing entries: {sorted(names ^ expected_paths)}')
        for rel in sorted(expected_paths):
            data = zf.read(rel)
            if sha_bytes(data) != BUILD11[rel]:
                raise SystemExit(f'Build 11 payload entry hash mismatch: {rel}')
            out = (root / rel).resolve()
            if root not in out.parents:
                raise SystemExit(f'Unsafe Build 11 patch path: {rel}')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)

    verify(root, BUILD11, 'Build 11 result')
    print('Build 11 automatic native handoff/fallback patch applied and verified.')


if __name__ == '__main__':
    main()
