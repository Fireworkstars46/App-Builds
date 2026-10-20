#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, os, tempfile, zipfile

PATCH_SHA256 = "2f39d0ccf95bd2fc8509d37edab4cd7e8044b987f6ff173f1119562a9d87023f"
EXPECTED_FILES = {
    "app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java",
    "app/build.gradle",
    "tools/static_audit.py",
    "BUILD_INFO.md",
    "README.md",
}

def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.replace(tmp, path)
    except Exception:
        try: os.unlink(tmp)
        except OSError: pass
        raise

def main() -> None:
    ap = argparse.ArgumentParser(description="Apply DisneyNOW Fire TV v0.1 Build 2 corrective source replacements")
    ap.add_argument("--source", required=True)
    args = ap.parse_args()
    source = Path(args.source).resolve()
    patch = Path(__file__).resolve().with_name("patch.zip")

    build_gradle = source / "app" / "build.gradle"
    main_java = source / "app" / "src" / "main" / "java" / "com" / "fireworkstars46" / "disneynowfiretv" / "MainActivity.java"
    if not build_gradle.is_file() or not main_java.is_file():
        raise SystemExit(f"Expected reconstructed source was not found at {source}")
    if "com.fireworkstars46.disneynowfiretv" not in build_gradle.read_text(encoding="utf-8"):
        raise SystemExit("Package identity mismatch; refusing to patch unrelated source")

    actual = hashlib.sha256(patch.read_bytes()).hexdigest()
    if actual != PATCH_SHA256:
        raise SystemExit(f"Build 2 patch integrity failure: expected {PATCH_SHA256}, got {actual}")

    with zipfile.ZipFile(patch) as archive:
        names = set(archive.namelist())
        if names != EXPECTED_FILES:
            raise SystemExit(f"Unexpected Build 2 patch contents: {sorted(names)}")
        for member in archive.infolist():
            target = (source / member.filename).resolve()
            if source != target and source not in target.parents:
                raise SystemExit(f"Unsafe patch path: {member.filename}")
            atomic_write(target, archive.read(member))

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
    print(f"Patch ZIP SHA-256: {actual}")
    for name, _ in checks: print(f"PASS - {name}")

if __name__ == "__main__": main()
