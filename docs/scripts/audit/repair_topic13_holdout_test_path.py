from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TEST = ROOT / "docs/core/test/test_topic13_xie_2026_holdout_access_audit.py"


def main() -> int:
    text = TEST.read_text(encoding="utf-8-sig")
    old = 'ROOT = Path(__file__).resolve().parents[2]\n'
    new = 'ROOT = Path(__file__).resolve().parents[1]\n'
    if text.count(old) != 1:
        raise RuntimeError("unexpected holdout test root declaration")
    TEST.write_text(text.replace(old, new), encoding="utf-8")
    print("repaired Topic 13 holdout test path")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
