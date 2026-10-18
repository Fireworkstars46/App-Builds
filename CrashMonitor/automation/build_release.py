#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SCRIPT = Path(__file__).resolve()
REPO = SCRIPT.parents[2]
AUTOMATION = SCRIPT.parent


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def run(cmd: list[str], *, cwd: Path | None = None, stdout_path: Path | None = None,
        stderr_path: Path | None = None) -> subprocess.CompletedProcess:
    print("+", " ".join(cmd))
    stdout = subprocess.PIPE if stdout_path is None else open(stdout_path, "wb")
    stderr = subprocess.PIPE if stderr_path is None else open(stderr_path, "wb")
    try:
        cp = subprocess.run(cmd, cwd=str(cwd) if cwd else None, stdout=stdout, stderr=stderr, check=False)
    finally:
        if stdout_path is not None:
            stdout.close()
        if stderr_path is not None:
            stderr.close()
    if cp.returncode != 0:
        if stdout_path is None and cp.stdout:
            print(cp.stdout.decode(errors="replace"), file=sys.stderr)
        if stderr_path is None and cp.stderr:
            print(cp.stderr.decode(errors="replace"), file=sys.stderr)
        fail(f"command failed with exit code {cp.returncode}: {' '.join(cmd)}")
    return cp


def which_tool(name: str, fallbacks: list[str] | None = None) -> str:
    hit = shutil.which(name)
    if hit:
        return hit
    for candidate in fallbacks or []:
        if Path(candidate).exists():
            return candidate
    fail(f"required tool not found: {name}")
    raise AssertionError


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def first_version_line(tool: str, args: list[str] | None = None) -> str:
    try:
        cp = subprocess.run([tool] + (args or ["--version"]), stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, check=False)
        return (cp.stdout or "").splitlines()[0].strip()
    except Exception as exc:
        return f"unavailable: {exc!r}"


def set_output(name: str, value: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"{name}={value}\n")


def safe_extract(zip_path: Path, destination: Path) -> None:
    destination = destination.resolve()
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            target = (destination / info.filename).resolve()
            if destination != target and destination not in target.parents:
                fail(f"unsafe path in source ZIP: {info.filename}")
        zf.extractall(destination)
        bad = zf.testzip()
        if bad:
            fail(f"source ZIP CRC failure at {bad}")


def deterministic_zip(source_dir: Path, output_zip: Path) -> None:
    excluded_suffixes = {".obj", ".lib", ".su"}
    excluded_names = {"compile.err"}
    files: list[Path] = []
    for p in source_dir.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(source_dir)
        if p.suffix.lower() in excluded_suffixes:
            continue
        if p.name in excluded_names:
            continue
        if p.name.endswith("-noicon.exe"):
            continue
        if re.fullmatch(r"Crash_Monitor_v.+_Build_\d+_Setup\.exe", p.name):
            continue
        files.append(rel)
    files.sort(key=lambda p: p.as_posix().lower())
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in files:
            data = (source_dir / rel).read_bytes()
            zi = zipfile.ZipInfo(rel.as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o100644 << 16
            zf.writestr(zi, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(output_zip, "r") as zf:
        bad = zf.testzip()
        if bad:
            fail(f"generated source ZIP CRC failure at {bad}")


def main() -> int:
    request_path = Path(sys.argv[1] if len(sys.argv) > 1 else AUTOMATION / "request.json")
    if not request_path.is_absolute():
        request_path = (REPO / request_path).resolve()
    request = json.loads(request_path.read_text(encoding="utf-8"))

    if not bool(request.get("enabled", False)):
        print("Crash Monitor release automation is disabled in request.json; nothing to build.")
        set_output("built", "false")
        return 0

    base_folder_name = str(request.get("base_release_folder", "")).strip()
    version = str(request.get("target_version", "")).strip()
    build = request.get("target_build")
    patch_rel = str(request.get("patch_file", "")).strip()
    expected_static = request.get("expected_static_pass")
    archive = bool(request.get("archive", True))

    if not re.fullmatch(r"\d+(?:\.\d+)+", version):
        fail("target_version must look like 4.2")
    if not isinstance(build, int) or build < 1:
        fail("target_build must be a positive integer")
    if not re.fullmatch(r"v\d+(?:\.\d+)+-Build\d+", base_folder_name):
        fail("base_release_folder must look like v4.2-Build12")
    base_build_match = re.search(r"Build(\d+)$", base_folder_name)
    if not base_build_match:
        fail("could not parse base build")
    base_build = int(base_build_match.group(1))
    if archive and build <= base_build:
        fail("archived target_build must be greater than the base build")

    base_release = REPO / "CrashMonitor" / "releases" / base_folder_name
    if not base_release.is_dir():
        fail(f"base release folder not found: {base_release.relative_to(REPO)}")
    source_zips = sorted(base_release.glob("Crash_Monitor_*_Source.zip"))
    if len(source_zips) != 1:
        fail(f"expected exactly one base source ZIP, found {len(source_zips)}")
    base_source_zip = source_zips[0]

    target_folder_name = f"v{version}-Build{build}"
    target_release = REPO / "CrashMonitor" / "releases" / target_folder_name
    if archive and target_release.exists():
        fail(f"refusing to reuse/overwrite existing release folder: {target_release.relative_to(REPO)}")

    patch_path: Path | None = None
    if patch_rel:
        patch_path = (REPO / patch_rel).resolve()
        if REPO not in patch_path.parents:
            fail("patch_file must stay inside this repository")
        if not patch_path.is_file():
            fail(f"patch_file not found: {patch_rel}")

    clang = which_tool("clang++", ["/usr/local/swift/usr/bin/clang++"])
    lld_link = which_tool("lld-link", ["/usr/local/swift/usr/bin/lld-link"])
    python = which_tool("python3")

    with tempfile.TemporaryDirectory(prefix="crashmonitor-release-") as tmp_s:
        tmp = Path(tmp_s)
        src = tmp / "source"
        src.mkdir()
        safe_extract(base_source_zip, src)

        if patch_path:
            run(["git", "apply", "--unsafe-paths", "--whitespace=nowarn", str(patch_path)], cwd=src)

        cpp_files = list(src.glob("crash_monitor_*_build*-source.cpp"))
        embed_files = list(src.glob("embed_resources_*_build*.py"))
        check_files = list(src.glob("release_checks_*_build*.py"))
        if len(cpp_files) != 1 or len(embed_files) != 1 or len(check_files) != 1:
            fail("patched source must contain exactly one main C++ file, one embed_resources script, and one release_checks script")
        cpp = cpp_files[0]
        embed = embed_files[0]
        checks = check_files[0]

        expected_build_token = f"Build {build}"
        cpp_text = cpp.read_text(encoding="utf-8", errors="replace")
        if expected_build_token not in cpp_text:
            fail(f"target source does not identify {expected_build_token}; patch likely did not update the build")

        required_defs = ["KERNEL32", "USER32", "GDI32", "SHELL32", "ADVAPI32", "COMDLG32", "OLE32"]
        for stem in required_defs:
            d = src / f"{stem}.def"
            if not d.is_file():
                fail(f"missing required import definition: {d.name}")
            run([lld_link, "/lib", f"/def:{d.name}", "/machine:x64", f"/out:{stem}.lib"], cwd=src)

        obj = src / f"cm_v{version.replace('.', '_')}_b{build}.obj"
        compile_err = src / "compile.err"
        run([
            clang, "-target", "x86_64-pc-windows-msvc", "-std=c++17", "-ffreestanding",
            "-fno-exceptions", "-fno-rtti", "-fno-stack-protector", "-fno-threadsafe-statics",
            "-mno-stack-arg-probe", "-Wall", "-Wextra", "-Wpedantic", "-c", cpp.name,
            "-o", obj.name,
        ], cwd=src, stderr_path=compile_err)
        if compile_err.read_bytes().strip():
            fail("compiler produced warnings/errors; refusing to create release")

        noicon = src / f"Crash_Monitor_v{version}_Build_{build}_Setup-noicon.exe"
        final_exe = src / f"Crash_Monitor_v{version}_Build_{build}_Setup.exe"
        run([
            lld_link, "/subsystem:windows", "/entry:wWinMainCRTStartup", "/nodefaultlib", obj.name,
            *[f"{stem}.lib" for stem in required_defs], "/timestamp:0", f"/out:{noicon.name}"
        ], cwd=src)
        run([python, embed.name], cwd=src)
        if not final_exe.is_file():
            fail(f"embed script did not produce expected installer: {final_exe.name}")

        static_output = tmp / f"CI_STATIC_CHECK_OUTPUT_v{version}_Build_{build}.txt"
        cp = subprocess.run([python, checks.name], cwd=src, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, check=False)
        static_output.write_text(cp.stdout or "", encoding="utf-8")
        print(cp.stdout or "")
        if cp.returncode != 0:
            fail("release_checks reported failure")
        m = re.search(r"TOTAL=(\d+)\s+PASS=(\d+)\s+FAIL=(\d+)", cp.stdout or "")
        if not m:
            fail("release_checks output did not include TOTAL/PASS/FAIL summary")
        total, passed, failed = map(int, m.groups())
        if failed != 0 or passed != total:
            fail(f"release_checks summary is not clean: TOTAL={total} PASS={passed} FAIL={failed}")
        if expected_static is not None and int(expected_static) != passed:
            fail(f"static PASS count changed: expected {expected_static}, got {passed}")

        out_dir = tmp / "release-output"
        out_dir.mkdir()
        staged_exe = out_dir / final_exe.name
        shutil.copy2(final_exe, staged_exe)
        source_zip_name = f"Crash_Monitor_v{version}_Build_{build}_Source.zip"
        staged_source_zip = out_dir / source_zip_name
        deterministic_zip(src, staged_source_zip)

        exe_hash = sha256(staged_exe)
        zip_hash = sha256(staged_source_zip)
        build_log = out_dir / f"CI_BUILD_LOG_v{version}_Build_{build}.txt"
        build_log.write_text(
            "\n".join([
                f"Crash Monitor v{version} Build {build} automated build",
                f"UTC: {datetime.now(timezone.utc).isoformat()}",
                f"Git commit: {os.environ.get('GITHUB_SHA', 'local')}",
                f"Base source ZIP: {base_source_zip.relative_to(REPO).as_posix()}",
                f"Patch: {patch_rel or '(none)'}",
                f"clang++: {first_version_line(clang)}",
                f"lld-link: {first_version_line(lld_link)}",
                f"Python: {first_version_line(python, ['--version'])}",
                f"Static checks: {passed} PASS / 0 FAIL",
                f"Installer bytes: {staged_exe.stat().st_size}",
                f"Installer SHA-256: {exe_hash}",
                f"Source ZIP bytes: {staged_source_zip.stat().st_size}",
                f"Source ZIP SHA-256: {zip_hash}",
                "Runtime Safe Self-Test: PENDING exact GitHub-built installer test on Windows",
                "DONE status: NOT CLAIMED by build automation",
                "",
            ]), encoding="utf-8")
        shutil.copy2(static_output, out_dir / static_output.name)
        shutil.copy2(request_path, out_dir / f"CI_REQUEST_v{version}_Build_{build}.json")
        if patch_path:
            shutil.copy2(patch_path, out_dir / patch_path.name)

        manifest = {
            "schema": 1,
            "project": "Crash Monitor",
            "version": version,
            "build": build,
            "base_release_folder": base_folder_name,
            "base_source_zip": base_source_zip.relative_to(REPO).as_posix(),
            "patch_file": patch_rel or None,
            "git_source_commit": os.environ.get("GITHUB_SHA"),
            "static_checks": {"pass": passed, "fail": 0},
            "runtime_safe_self_test": "PENDING",
            "artifacts": {
                staged_exe.name: {"bytes": staged_exe.stat().st_size, "sha256": exe_hash},
                staged_source_zip.name: {"bytes": staged_source_zip.stat().st_size, "sha256": zip_hash},
            },
            "release_status": "PENDING_WINDOWS_RUNTIME_AND_POST_COMMIT_RETRIEVAL_VERIFICATION",
        }
        manifest_name = f"CI_BUILD_MANIFEST_v{version}_Build_{build}.json"
        (out_dir / manifest_name).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (out_dir / "ARCHIVE_STATUS.md").write_text(
            f"# Crash Monitor v{version} Build {build} archive status\n\n"
            "Automated GitHub build completed successfully.\n\n"
            f"- Static/release checks: **{passed} PASS / 0 FAIL**\n"
            f"- Installer: `{staged_exe.name}` — {staged_exe.stat().st_size:,} bytes — SHA-256 `{exe_hash}`\n"
            f"- Source ZIP: `{staged_source_zip.name}` — {staged_source_zip.stat().st_size:,} bytes — SHA-256 `{zip_hash}`\n"
            "- Windows Safe Self-Test: **PENDING** on this exact GitHub-built installer\n"
            "- Post-commit retrieval/hash verification: **PENDING**\n"
            "- Overall release status: **NOT DONE** until required runtime evidence and retrieval verification are recorded\n\n"
            "This automation intentionally does not convert environment-owned checks to PASS and does not claim DONE.\n",
            encoding="utf-8")

        if archive:
            target_release.mkdir(parents=True, exist_ok=False)
            for p in out_dir.iterdir():
                shutil.copy2(p, target_release / p.name)
            release_dir_for_output = target_release.relative_to(REPO).as_posix()
        else:
            local_out = REPO / "CrashMonitor" / "automation" / ".verify-output" / target_folder_name
            if local_out.exists():
                shutil.rmtree(local_out)
            local_out.mkdir(parents=True)
            for p in out_dir.iterdir():
                shutil.copy2(p, local_out / p.name)
            release_dir_for_output = local_out.relative_to(REPO).as_posix()

        print(f"Prepared release output: {release_dir_for_output}")
        print(f"Installer SHA-256: {exe_hash}")
        print(f"Source ZIP SHA-256: {zip_hash}")
        set_output("built", "true")
        set_output("archive", "true" if archive else "false")
        set_output("release_dir", release_dir_for_output)
        set_output("target_folder", target_folder_name)
        set_output("installer_sha256", exe_hash)
        set_output("source_sha256", zip_hash)
        set_output("installer_name", staged_exe.name)
        set_output("source_name", staged_source_zip.name)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
