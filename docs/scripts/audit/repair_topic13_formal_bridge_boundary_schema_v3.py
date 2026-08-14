"""Add the remaining legacy no-numeric-alpha field alias."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_formal_bridge_boundary.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = '        "numeric_alpha_not_emitted": checks.get("numeric_alpha_not_emitted"),\n'
    new = (
        '        "numeric_alpha_not_emitted": checks.get("numeric_alpha_not_emitted")\n'
        '        or checks.get("no_numeric_alpha_emitted"),\n'
    )
    if old not in text:
        if 'checks.get("no_numeric_alpha_emitted")' in text:
            print("FORMAL_BRIDGE_NUMERIC_ALPHA_ALIAS_ALREADY_PRESENT")
            return 0
        raise SystemExit("formal bridge numeric alpha field not found")
    TARGET.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("ADDED_FORMAL_BRIDGE_NUMERIC_ALPHA_ALIAS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
