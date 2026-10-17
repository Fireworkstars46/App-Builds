from pathlib import Path
base = Path(__file__).parent
parts = sorted(base.glob("master_rules_build4_selftest.part*.txt"), key=lambda p: int(p.stem.split("part")[-1]))
code = "".join(p.read_text(encoding="utf-8") for p in parts)
exec(compile(code, str(base / "master_rules_build4_selftest.combined.py"), "exec"))
