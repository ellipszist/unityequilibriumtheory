"""Add the actual alias-repair idempotence step to the Topic 13 wave."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/run_topic13_full_bridge_wave.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    command = '    "docs/scripts/audit/repair_topic13_full_gate_alias_repair_idempotence.py",\n'
    if command in text:
        print("RUNNER_ALIAS_REPAIR_IDEMPOTENCE_ALREADY_PRESENT")
        return 0
    needle = '    "docs/scripts/audit/repair_topic13_full_gate_backward_compat_aliases.py",\n'
    if text.count(needle) != 1:
        raise SystemExit(f"runner alias repair anchor: expected one match, found {text.count(needle)}")
    TARGET.write_text(text.replace(needle, command + needle, 1), encoding="utf-8")
    print("ADDED_RUNNER_ALIAS_REPAIR_IDEMPOTENCE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
