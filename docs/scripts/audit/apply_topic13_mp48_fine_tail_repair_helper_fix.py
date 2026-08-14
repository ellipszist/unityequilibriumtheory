from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
path = ROOT / "docs/scripts/audit/apply_topic13_mp48_fine_tail.py"
text = path.read_text(encoding="utf-8")
text = text.replace(
    'assert text.count(old) == 1\ntext = text.replace(old, new)\nAUDIT.write_text',
    'assert text.count(old) == 2\ntext = text.replace(old, new, 1)\nAUDIT.write_text',
)
path.write_text(text, encoding="utf-8")
print(path)
