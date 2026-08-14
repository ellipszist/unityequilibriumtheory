"""Repair the Ding source sync fallback after the comparison/raw split."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/sync_topic13_ding_source_mapping_gate.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = '''    blocker = audit.get(
        "controlling_blocker",
        "ttg_numeric_source_package_is_provisional",
        "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing",
    )
'''
    new = '''    blocker = audit.get("controlling_blocker") or (
        "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing"
    )
'''
    if old in text:
        text = text.replace(old, new, 1)
    elif new not in text:
        raise SystemExit("source sync blocker fallback not found")
    TARGET.write_text(text, encoding="utf-8")
    print("REPAIRED_TOPIC13_SOURCE_SYNC_CONTROLLER_V4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
