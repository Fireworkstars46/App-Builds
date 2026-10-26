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
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'cabdf3ac12c831dc15ad350be75f35387b8eb2195e2aa139077d26cbb0e896f1',
    'app/build.gradle': 'a07d3b4c3051412453615db5b353aa46d8ecc8180ef57064fc52e4100182ae3b',
    'BUILD_INFO.md': '60aa05b3553f9bd4243103b4a00f5ff599aba5a47f718c7d526f1226f03549f0',
    'README.md': 'adefbaf2c51099d6a07d6c411a2d7a4386772cdf06c8b1fe3e797d57851ae401',
    'tools/static_audit.py': 'a89c1ba6e70250dc3024bd573717a187897a121c12e8ab95891a653812631281',
}

PATCH_ZIP_SHA256 = '77273d6dd0eb6a6cc28a7e14c078b2141fcf4bf3856c24d093c5dda966125b98'
PART_ORDER = [
    'part00.b64',
    'part01.b64',
    'part02.b64',
    'part03a.b64',
    'part03b.b64',
    'part03c1.b64',
    'part03c2.b64',
    'part03c3.b64',
    'part03d.b64',
    'part04.b64',
]
EXPECTED_PARTS = {
    'part00.b64': (9697, '54bf02462776fc52d6f1f1d2ad1c637eec3761c6afeceae96447aa6ef436be79'),
    'part01.b64': (9697, 'df3f58c49cefae426d287e19dddd829cf2e0e55b468c8c7a9ee5121aee843f1e'),
    'part02.b64': (9697, '6ac29e516bc1d6f76599bdf03918c448bff3e97c6fc7196adf3703998c02a9eb'),
    'part03a.b64': (3000, '7ffe3f06fe273632707a44741eb86c06cc39681492d84fb8522c168692f474b2'),
    'part03b.b64': (3000, '6320dd7d95786a25666b1669df88941f6c3ae0eb384e6d6926cea677a19f6385'),
    'part03c1.b64': (1000, 'b0fbc17688dbb31485ebc2bf63c9c9956aa1c491f8bef8520ece82063e52e284'),
    'part03c2.b64': (1000, '70dc4179ade5d5feeb568504670bd394804b8e5c85a6d0ed783bde44637b8641'),
    'part03c3.b64': (1000, '4d4ce840a23984873cfd650e94ea520711f79318332d979e79af316786908bbd'),
    'part03d.b64': (697, 'feefd8a6dde8aede55642241efa930699b0e99efa3da5d44acdaece1be0b5a07'),
    'part04.b64': (9696, '98489f8f7767edb6653898347a462919c63e7c330873989db9d8ce875be6dea7'),
}


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
    parts = [parts_dir / name for name in PART_ORDER]
    missing = [p.name for p in parts if not p.is_file()]
    if missing:
        raise SystemExit('Build 12 patch payload is missing required parts: ' + ', '.join(missing))

    part_failures = []
    for p in parts:
        data = p.read_bytes()
        expected_len, expected_sha = EXPECTED_PARTS[p.name]
        got_sha = sha_bytes(data)
        print(f'Build 12 patch part {p.name}: bytes={len(data)} sha256={got_sha}')
        if len(data) != expected_len or got_sha != expected_sha:
            part_failures.append(f'{p.name}: expected bytes={expected_len} sha256={expected_sha}; got bytes={len(data)} sha256={got_sha}')
    if part_failures:
        raise SystemExit('Build 12 patch part verification failed:\n' + '\n'.join(part_failures))

    encoded = ''.join(p.read_text(encoding='ascii') for p in parts)
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f'Build 12 patch base64 decode failed: {exc}')
    payload_sha = sha_bytes(payload)
    print(f'Build 12 reconstructed patch ZIP: bytes={len(payload)} sha256={payload_sha}')
    if payload_sha != PATCH_ZIP_SHA256:
        raise SystemExit(f'Build 12 patch ZIP SHA-256 mismatch: expected {PATCH_ZIP_SHA256}, got {payload_sha}')

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
    print('Build 12 automatic-handoff regression fix and persistent crash-breadcrumb patch applied and verified.')


if __name__ == '__main__':
    main()
