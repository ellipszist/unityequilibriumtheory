"""Repair the Berut test contract for explicit negative safety checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TEST = ROOT / "docs/core/test/test_topic13_berut_source_package_availability.py"


def main() -> int:
    text = TEST.read_text(encoding="utf-8-sig")
    old = '    assert all(artifact["verification_status"].values())\n'
    new = '''    checks = artifact["verification_status"]
    positive_checks = [
        value
        for key, value in checks.items()
        if key not in {"xie_2026_accessed", "xie_2026_consumed"}
    ]
    assert all(positive_checks)
    assert checks["xie_2026_accessed"] is False
    assert checks["xie_2026_consumed"] is False
'''
    if old in text:
        TEST.write_text(text.replace(old, new, 1), encoding="utf-8")
        print("PATCHED_BERUT_TEST_SAFETY_INVARIANTS")
    else:
        print("BERUT_TEST_SAFETY_INVARIANTS_ALREADY_PATCHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

