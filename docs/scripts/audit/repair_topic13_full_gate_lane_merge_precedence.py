"""Make current lane artifacts win over stale preserved summaries."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = '''    artifact["verification_status"]["eos_transport_kms_entropy"].update(discovered_lane_integrations)
    artifact["verification_status"]["eos_transport_kms_entropy"].update(preserved_lane_integrations)
'''
    new = '''    artifact["verification_status"]["eos_transport_kms_entropy"].update(preserved_lane_integrations)
    # Current source artifacts must override stale records from an older gate.
    artifact["verification_status"]["eos_transport_kms_entropy"].update(discovered_lane_integrations)
'''
    if old not in text:
        if new in text:
            print("FULL_GATE_LANE_MERGE_PRECEDENCE_ALREADY_PRESENT")
            return 0
        raise SystemExit("full-gate merge block not found")
    TARGET.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("ADDED_FULL_GATE_LANE_MERGE_PRECEDENCE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
