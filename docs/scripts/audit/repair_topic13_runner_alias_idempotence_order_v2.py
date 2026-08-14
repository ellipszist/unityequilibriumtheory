"""Place the original alias-repair idempotence fix first in the Topic 13 wave."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/run_topic13_full_bridge_wave.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    command = '    "docs/scripts/audit/repair_topic13_runner_alias_idempotence_order_v2.py",\n'
    if command in text:
        print("RUNNER_ALIAS_IDEMPOTENCE_ORDER_V2_ALREADY_PRESENT")
        return 0
    needle = '    "docs/scripts/audit/repair_topic13_full_gate_remaining_compatibility_idempotence.py",\n'
    if text.count(needle) != 1:
        raise SystemExit(f"runner idempotence anchor: expected one match, found {text.count(needle)}")
    TARGET.write_text(text.replace(needle, command + needle, 1), encoding="utf-8")
    print("ADDED_RUNNER_ALIAS_IDEMPOTENCE_ORDER_V2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
