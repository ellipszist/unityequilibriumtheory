from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
path = ROOT / "docs/core/test/test_topic13_independent_csrc_acceptance.py"
text = path.read_text(encoding="utf-8")
text = text.replace("ROOT = Path(__file__).resolve().parents[2]", "ROOT = Path(__file__).resolve().parents[3]")
path.write_text(text, encoding="utf-8")
print("fixed Topic 13 acceptance test root")
