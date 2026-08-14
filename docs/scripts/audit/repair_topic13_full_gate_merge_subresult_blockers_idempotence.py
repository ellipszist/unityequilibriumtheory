"""Make the historical subresult-blocker repair safe after integration."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/repair_topic13_full_gate_merge_subresult_blockers.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = '    if "        *source_level_blockers,\\n" not in text:\n'
    new = (
        '    if (\n'
        '        "        *source_level_blockers,\\n" not in text\n'
        '        and "source_level_blockers =" not in text\n'
        '    ):\n'
    )
    if old in text and new not in text:
        text = text.replace(old, new, 1)
        TARGET.write_text(text, encoding="utf-8")
        print({"changed": True})
        return 0
    if new in text:
        print({"changed": False, "reason": "already_repaired"})
        return 0
    raise SystemExit("stale merge repair conditional not found")


if __name__ == "__main__":
    raise SystemExit(main())
