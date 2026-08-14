"""Run causal evidence before composing the canonical Topic 13 full gate."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/run_topic13_full_bridge_wave.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = '''COMMANDS = [
    "docs/scripts/audit/audit_topic13_full_bridge_gate.py",
    "docs/scripts/audit/audit_conserved_c_finite_cone_no_go.py",
    "docs/scripts/audit/sync_topic13_no_go_gate.py",
    "docs/scripts/audit/audit_major_result_closure.py",
    "docs/scripts/audit/sync_major_result_wave1_contract.py",
]
'''
    new = '''COMMANDS = [
    # The full gate composes causal evidence, so create the no-go record first.
    "docs/scripts/audit/audit_conserved_c_finite_cone_no_go.py",
    "docs/scripts/audit/audit_topic13_full_bridge_gate.py",
    "docs/scripts/audit/sync_topic13_no_go_gate.py",
    "docs/scripts/audit/audit_major_result_closure.py",
    "docs/scripts/audit/sync_major_result_wave1_contract.py",
]
'''
    if old not in text:
        if new in text:
            print("TOPIC13_FULL_BRIDGE_RUNNER_ORDER_ALREADY_PRESENT")
            return 0
        raise SystemExit("Topic 13 full-bridge command list not found")
    TARGET.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("REORDERED_TOPIC13_FULL_BRIDGE_CAUSAL_EVIDENCE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
