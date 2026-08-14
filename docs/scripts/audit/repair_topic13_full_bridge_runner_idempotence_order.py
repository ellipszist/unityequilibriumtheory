"""Run the Topic 13 idempotence repair before compatibility repairs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/run_topic13_full_bridge_wave.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    command = '    "docs/scripts/audit/repair_topic13_full_gate_remaining_compatibility_idempotence.py",\n'
    if command in text:
        print("FULL_BRIDGE_RUNNER_IDEMPOTENCE_ORDER_ALREADY_PRESENT")
        return 0
    needle = "COMMANDS = [\n"
    if text.count(needle) != 1:
        raise SystemExit(f"runner command list: expected one match, found {text.count(needle)}")
    TARGET.write_text(text.replace(needle, needle + command, 1), encoding="utf-8")
    print("ADDED_FULL_BRIDGE_RUNNER_IDEMPOTENCE_ORDER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
