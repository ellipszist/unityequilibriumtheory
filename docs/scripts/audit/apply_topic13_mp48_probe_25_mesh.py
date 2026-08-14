from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
path = ROOT / "docs/scripts/audit/probe_topic13_mp48_finer_mesh.py"
text = path.read_text(encoding="utf-8")
old = "    for shape in ((20, 20, 8),):\n"
new = "    for shape in ((25, 25, 10),):\n"
assert text.count(old) == 1
path.write_text(text.replace(old, new), encoding="utf-8")
print(path)
