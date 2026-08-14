"""Add the normal thermodynamic-consistency result to the full-gate map."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
RESULT_ID = "T13_UET_O2_NORMAL_THERMODYNAMIC_CONSISTENCY"
LANE_KEY = "uet_o2_normal_thermodynamic_consistency"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    if RESULT_ID in text:
        print("NORMAL_THERMODYNAMIC_CONSISTENCY_LANE_KEY_ALREADY_PRESENT")
        return 0
    needle = "'T13_UET_O2_ONE_LOOP_THERMAL_UV_BOUNDARY': 'uet_o2_one_loop_uv_boundary'"
    if text.count(needle) != 1:
        raise SystemExit("full-gate lane map anchor is not unique")
    replacement = needle + f", '{RESULT_ID}': '{LANE_KEY}'"
    TARGET.write_text(text.replace(needle, replacement, 1), encoding="utf-8")
    print("ADDED_NORMAL_THERMODYNAMIC_CONSISTENCY_LANE_KEY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
