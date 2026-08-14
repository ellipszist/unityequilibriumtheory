"""Add the formal Topic 13 bridge-boundary result to the canonical gate map."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    result_id = "T13_FORMAL_NONCIRCULAR_BRIDGE_BOUNDARY"
    if result_id in text:
        print("FORMAL_BRIDGE_LANE_KEY_MAPPING_ALREADY_PRESENT")
        return 0
    needle = "'T13_THERMAL_RESPONSE_BETA_CONTRACT': 'thermal_response_beta_contract',"
    replacement = needle + " 'T13_FORMAL_NONCIRCULAR_BRIDGE_BOUNDARY': 'formal_non_circular_bridge_boundary',"
    if text.count(needle) != 1:
        raise SystemExit(f"full-gate beta mapping count: {text.count(needle)}")
    TARGET.write_text(text.replace(needle, replacement, 1), encoding="utf-8")
    print("ADDED_FORMAL_BRIDGE_LANE_KEY_MAPPING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
