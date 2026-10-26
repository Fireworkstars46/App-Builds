#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, hashlib, io, zipfile

BASE9 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'c2b60181021f21d25d80f92fbf7da1b30febb38f86294fc5550b93ef6e674de4',
    'app/build.gradle': '8f7082922fe1264e7ed25659e957eaa453a43847ea732a1b3f2928e53cfbc135',
    'BUILD_INFO.md': 'aa019ab7b7b3df03ce855eacc10308142402de2a4bce96f4dd8b710fa1d5c116',
    'README.md': '7229a72cf329158d5b7515ea6a73766039ce1dcbf6cee1bc18c9e671c275123f',
    'tools/static_audit.py': '0cd430ff7eee9b9fec6d9c1959d3bc8fbba11d3283ce5697c9708aa30fdcab25',
}

BUILD10 = {
    'app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java': 'fa6a93ebaa12304da596b9f772cc8804679cc85b8f00d9331b4bd5edd53c7878',
    'app/build.gradle': 'd10998ac372a6a8faf88be8fbb9e7b37c065580a70fc4c641e6f424077b56e21',
    'BUILD_INFO.md': 'f07555a3d179842b1900879adfe1be971ac698a9b623dba58c8e80a1012b679a',
    'README.md': '1a9d5e58f141b095381b6dc206edf10a91438ed11927a5ddac6c62f29efa22d7',
    'tools/static_audit.py': 'c7e692fcfa11684b072aec3cb4be29dcdbc9fb2d34bbc180b48b396933e04223',
}

PATCH_ZIP_SHA256 = 'b6da23e817f6afcb3192cf6e9ab427991e816cbd0c3f9b9797482cf357c36334'


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
    verify(root, BASE9, 'Build 9 baseline')

    parts_dir = Path(__file__).resolve().parent / 'patch_parts'
    parts = sorted(parts_dir.glob('part*.b64'))
    expected_names = [f'part{i:02d}.b64' for i in range(5)]
    if [p.name for p in parts] != expected_names:
        raise SystemExit('Build 10 patch payload must contain exactly part00.b64 through part04.b64')
    encoded = ''.join(p.read_text(encoding='ascii') for p in parts)
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f'Build 10 patch base64 decode failed: {exc}')
    if sha_bytes(payload) != PATCH_ZIP_SHA256:
        raise SystemExit('Build 10 patch ZIP SHA-256 mismatch')

    expected_paths = set(BUILD10)
    with zipfile.ZipFile(io.BytesIO(payload), 'r') as zf:
        names = set(zf.namelist())
        if names != expected_paths:
            raise SystemExit(f'Build 10 patch ZIP contains unexpected/missing entries: {sorted(names ^ expected_paths)}')
        for rel in sorted(expected_paths):
            data = zf.read(rel)
            if sha_bytes(data) != BUILD10[rel]:
                raise SystemExit(f'Build 10 payload entry hash mismatch: {rel}')
            out = (root / rel).resolve()
            if root not in out.parents:
                raise SystemExit(f'Unsafe Build 10 patch path: {rel}')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)

    verify(root, BUILD10, 'Build 10 result')
    print('Build 10 native handoff diagnostics patch applied and verified.')


if __name__ == '__main__':
    main()
