#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, hashlib, os, subprocess, tempfile, zlib

COMPRESSED_SHA256 = "eeb1f46d061c5a1e6308803292c1ec353806fc93d22c89476eef88320352b0d2"
PATCH_SHA256 = "bb94b859fd960e79b37fef0d8a70db1072d387a3bb6adb0837a8609d1dc064fa"
PART_NAMES = ("part01.txt", "part02.txt", "part03.txt")

def main() -> None:
    ap = argparse.ArgumentParser(description="Apply DisneyNOW Fire TV v0.1 Build 2 corrective patch")
    ap.add_argument("--source", required=True)
    args = ap.parse_args()
    source = Path(args.source).resolve()
    build2 = Path(__file__).resolve().parent

    build_gradle = source / "app" / "build.gradle"
    main_java = source / "app" / "src" / "main" / "java" / "com" / "fireworkstars46" / "disneynowfiretv" / "MainActivity.java"
    if not build_gradle.is_file() or not main_java.is_file():
        raise SystemExit(f"Expected reconstructed source was not found at {source}")
    if "com.fireworkstars46.disneynowfiretv" not in build_gradle.read_text(encoding="utf-8"):
        raise SystemExit("Package identity mismatch; refusing to patch unrelated source")

    encoded = "".join((build2 / "PatchParts" / name).read_text(encoding="ascii").strip() for name in PART_NAMES)
    compressed = base64.b64decode(encoded, validate=True)
    compressed_sha = hashlib.sha256(compressed).hexdigest()
    if compressed_sha != COMPRESSED_SHA256:
        raise SystemExit(f"Build 2 compressed patch integrity failure: expected {COMPRESSED_SHA256}, got {compressed_sha}")
    patch_bytes = zlib.decompress(compressed)
    patch_sha = hashlib.sha256(patch_bytes).hexdigest()
    if patch_sha != PATCH_SHA256:
        raise SystemExit(f"Build 2 patch integrity failure: expected {PATCH_SHA256}, got {patch_sha}")

    fd, tmp_name = tempfile.mkstemp(prefix="disneynow-build2-", suffix=".patch")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(patch_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        result = subprocess.run(
            ["patch", "-p1", "--batch", "--forward", "-i", tmp_name],
            cwd=str(source), text=True, capture_output=True
        )
        if result.returncode != 0:
            raise SystemExit("Build 2 patch application failed:\n" + result.stdout + result.stderr)
    finally:
        try: os.unlink(tmp_name)
        except OSError: pass

    after_gradle = build_gradle.read_text(encoding="utf-8")
    after_main = main_java.read_text(encoding="utf-8")
    checks = [
        ("versionCode 2", "versionCode 2" in after_gradle),
        ("APP_BUILD 2", "APP_BUILD', '2" in after_gradle),
        ("cursor implementation", "private final class CursorView extends View" in after_main),
        ("page zoom implementation", "DEFAULT_PAGE_ZOOM = 75" in after_main),
        ("Build 2 self-test identity", "BuildConfig.APP_BUILD == 2" in after_main),
    ]
    failed = [name for name, ok in checks if not ok]
    if failed:
        raise SystemExit("Build 2 patch verification failed: " + ", ".join(failed))
    print(f"Applied DisneyNOW Fire TV v0.1 Build 2 corrective patch to {source}")
    print(f"Compressed patch SHA-256: {compressed_sha}")
    print(f"Decoded patch SHA-256: {patch_sha}")
    for name, _ in checks:
        print(f"PASS - {name}")

if __name__ == "__main__":
    main()
