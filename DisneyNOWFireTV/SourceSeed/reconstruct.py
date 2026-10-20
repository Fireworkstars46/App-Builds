#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, hashlib, io, shutil, zipfile
EXPECTED_SHA256 = "86655134de1a0930ea497801b688295bd85c830e6f0ba97cc1d9823ca3b4fa3d"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args=ap.parse_args()
    seed_dir=Path(__file__).resolve().parent
    encoded=''.join(p.read_text(encoding='ascii').strip() for p in sorted(seed_dir.glob('part*.txt')))
    raw=base64.b64decode(encoded)
    actual=hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED_SHA256:
        raise SystemExit(f"Seed integrity failure: expected {EXPECTED_SHA256}, got {actual}")
    output=Path(args.output).resolve()
    if output.exists(): shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for member in z.infolist():
            target=(output/member.filename).resolve()
            if output != target and output not in target.parents:
                raise SystemExit(f"Unsafe archive path: {member.filename}")
        z.extractall(output)
    print(f"Reconstructed source at {output}")
    print(f"Seed ZIP SHA-256: {actual}")

if __name__ == '__main__': main()
