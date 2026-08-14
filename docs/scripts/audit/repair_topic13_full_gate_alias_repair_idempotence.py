"""Make the original Topic 13 alias repair safe to rerun."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/repair_topic13_full_gate_backward_compat_aliases.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = (
        '    updated = replace_once(text, alias_anchor, alias_block, "legacy lane aliases")\n'
        "    if updated != text:\n"
        "        changed = True\n"
        "        text = updated\n"
    )
    new = (
        '    if "legacy_lane_aliases = {" not in text:\n'
        '        updated = replace_once(text, alias_anchor, alias_block, "legacy lane aliases")\n'
        "        if updated != text:\n"
        "            changed = True\n"
        "            text = updated\n"
    )
    if old not in text:
        if 'if "legacy_lane_aliases = {" not in text:' in text:
            print("FULL_GATE_ALIAS_REPAIR_IDEMPOTENCE_ALREADY_PRESENT")
            return 0
        raise SystemExit("alias repair idempotence anchor not found")
    TARGET.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("ADDED_FULL_GATE_ALIAS_REPAIR_IDEMPOTENCE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
