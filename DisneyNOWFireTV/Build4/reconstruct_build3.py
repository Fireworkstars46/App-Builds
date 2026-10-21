#!/usr/bin/env python3
from pathlib import Path
import argparse


def replace_exact(root: Path, path: str, old: str, new: str, count: int = 1) -> None:
    p = root / path
    text = p.read_text(encoding="utf-8")
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{path}: expected {count} occurrence(s), found {actual}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    args = ap.parse_args()
    root = Path(args.source).resolve()

    replace_exact(root, "app/build.gradle", "versionCode 2", "versionCode 3")
    replace_exact(root, "app/build.gradle", "buildConfigField 'int', 'APP_BUILD', '2'", "buildConfigField 'int', 'APP_BUILD', '3'")

    main_path = "app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java"
    replace_exact(root, main_path,
        "BuildConfig.APP_BUILD == 2 && BuildConfig.VERSION_CODE == 2",
        "BuildConfig.APP_BUILD == 3 && BuildConfig.VERSION_CODE == 3")
    replace_exact(root, main_path, "SafeSelfTest-v0.1-Build2.txt", "SafeSelfTest-v0.1-Build3.txt")
    replace_exact(root, main_path,
        "Build 2 fixes the reported Fire TV zoom, missing-cursor, and laggy D-pad navigation issues. It remains NOT DONE until this corrected build is tested on the actual Fire TV Stick.",
        "Build 3 preserves the Build 2 Fire TV cursor, zoom, and performance corrections and establishes the permanent release-signing identity for future in-place updates. It remains NOT DONE until this signed build is tested on the actual Fire TV Stick.")

    build_info = root / "BUILD_INFO.md"
    bi = build_info.read_text(encoding="utf-8")
    required = [
        "- Build: 2",
        "- Android versionCode: 2",
        "- Release state: NOT DONE pending real Fire TV runtime verification of the Build 2 cursor, zoom, smoothness, provider authentication, and protected playback.",
    ]
    for item in required:
        if item not in bi:
            raise SystemExit(f"BUILD_INFO.md pattern not found: {item!r}")
    bi = bi.replace("- Build: 2", "- Build: 3", 1)
    bi = bi.replace("- Android versionCode: 2", "- Android versionCode: 3", 1)
    bi = bi.replace(
        "- Release state: NOT DONE pending real Fire TV runtime verification of the Build 2 cursor, zoom, smoothness, provider authentication, and protected playback.",
        "- Release state: NOT DONE pending real Fire TV runtime verification of the Build 2 cursor/zoom/smoothness corrections plus Build 3 permanent-signing installation/update baseline.", 1)
    bi += "\nBuild 3 preserves all Build 2 functional behavior and exists because the first two compatibility-test APKs were incorrectly CI debug-signed. Build 3 establishes the permanent private release-signing identity. Build 1 must be uninstalled once because its temporary signing key was not preserved; Build 2 was never installed on the target Fire TV. Future builds must use the exact Build 3 release keystore so they can update in place.\n"
    build_info.write_text(bi, encoding="utf-8")

    readme = root / "README.md"
    rm = readme.read_text(encoding="utf-8")
    title = "# Source — DisneyNOW Fire TV Web Wrapper v0.1 Build 2"
    marker = "This is an Android/Fire TV WebView wrapper intended to use the normal DisneyNOW website on a Fire TV Stick.\n"
    old_sign = "Build 1 and Build 2 compatibility-test APKs use CI debug signing. A GitHub-hosted runner can generate a different debug signing key between builds, so Android may require Build 1 to be uninstalled before Build 2 installs. A stable private release-signing key must be established before a final update-compatible DONE release."
    for item in (title, marker, old_sign):
        if item not in rm:
            raise SystemExit(f"README pattern not found: {item!r}")
    rm = rm.replace(title, "# Source — DisneyNOW Fire TV Web Wrapper v0.1 Build 3", 1)
    insert = marker + "\n## Build 3 signing correction\n\nBuild 3 preserves the Build 2 cursor, 75% zoom, and performance corrections unchanged. Its artifact correction is establishing the permanent private release-signing identity required for future in-place updates. Build 1 used an unrecoverable CI debug key and must be uninstalled once. Build 2 was not installed on the target Fire TV.\n"
    rm = rm.replace(marker, insert, 1)
    rm = rm.replace(old_sign,
        "Build 1 and Build 2 compatibility-test APKs used CI debug signing. Build 3 establishes the permanent private release-signing identity. The Build 3 keystore is intentionally not committed to the public repository. Every later APK for this package must be signed with that same key.", 1)
    readme.write_text(rm, encoding="utf-8")

    audit = root / "tools/static_audit.py"
    a = audit.read_text(encoding="utf-8")
    replacements = [
        ("STATIC-AUDIT-v0.1-Build2.txt", "STATIC-AUDIT-v0.1-Build3.txt"),
        ('EXPECTED_BUILD = "2"', 'EXPECTED_BUILD = "3"'),
        ('EXPECTED_VERSION_CODE = "2"', 'EXPECTED_VERSION_CODE = "3"'),
        (r"versionCode\s+2\b", r"versionCode\s+3\b"),
        ("buildConfigField 'int', 'APP_BUILD', '2'", "buildConfigField 'int', 'APP_BUILD', '3'"),
        ("BuildConfig.APP_BUILD == 2", "BuildConfig.APP_BUILD == 3"),
        ('"Build: 2" in build_info', '"Build: 3" in build_info'),
        ("Build 2 self-test report filename", "Build 3 self-test report filename"),
        ("SafeSelfTest-v0.1-Build2.txt", "SafeSelfTest-v0.1-Build3.txt"),
        ("Version: 0.1 Build 2", "Version: 0.1 Build 3"),
    ]
    for old, new in replacements:
        if old not in a:
            raise SystemExit(f"static audit pattern not found: {old!r}")
        a = a.replace(old, new, 1)
    audit.write_text(a, encoding="utf-8")

    print("Build 3 source metadata patch reconstructed successfully.")


if __name__ == "__main__":
    main()
