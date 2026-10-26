#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, zipfile

BASE11 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'c06d83dd5d6b5d138ecb4c0fb7b59b78da62f9443ecdeb520744450de3987fd0',
    'app/build.gradle': '908cf7838c7f0b7894f7b4cc77ebbf6e19c311ed1b29bf62739e4099c5108842',
    'BUILD_INFO.md': '7afdba92291caf379820639d53989ced24d1ad459a6606308aaa7d5de1f60697',
    'README.md': '7e981821f0e8e1bd876aa7f46824b958623c4bcd4fefe71e3accf7b10ec93574',
    'tools/static_audit.py': '36d4e2cb8ee1ba501b7fb485d0447a820618ad80b28f9dbfb44749131f80b08b',
}

BUILD12 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'cabdf3ac12c831dc15ad350be75f35387b8eb2195e2aa139077d26cbb0e896f1',
    'app/build.gradle': 'a07d3b4c3051412453615db5b353aa46d8ecc8180ef57064fc52e4100182ae3b',
    'BUILD_INFO.md': '60aa05b3553f9bd4243103b4a00f5ff599aba5a47f718c7d526f1226f03549f0',
    'README.md': 'adefbaf2c51099d6a07d6c411a2d7a4386772cdf06c8b1fe3e797d57851ae401',
    'tools/static_audit.py': 'a89c1ba6e70250dc3024bd573717a187897a121c12e8ab95891a653812631281',
}

PATCH_ZIP_SHA256 = '77273d6dd0eb6a6cc28a7e14c078b2141fcf4bf3856c24d093c5dda966125b98'


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

    patch = Path(__file__).resolve().parent / 'patch.zip'
    if not patch.is_file():
        raise SystemExit('Build 12 patch.zip is missing')
    if sha_file(patch) != PATCH_ZIP_SHA256:
        raise SystemExit('Build 12 patch ZIP SHA-256 mismatch')

    expected_paths = set(BUILD12)
    with zipfile.ZipFile(patch, 'r') as zf:
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
    print('Build 12 automatic-handoff regression fix and persistent crash-breadcrumb patch applied and verified.')


if __name__ == '__main__':
    main()
