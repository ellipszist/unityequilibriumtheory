"""Add the renormalized normal one-loop lane to the full-gate discovery map."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
RESULT_ID = "T13_UET_O2_RENORMALIZED_NORMAL_ONE_LOOP_LANE"
LANE_KEY = "uet_o2_renormalized_normal_one_loop_lane"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    if RESULT_ID in text:
        print("TOPIC13_RENORMALIZED_NORMAL_LANE_KEY_ALREADY_PRESENT")
        return 0
    anchors = (
        "'T13_UET_O2_NORMAL_RESPONSE_CURVATURE_LANE': "
        "'uet_o2_normal_response_curvature_lane',",
        "'T13_UET_O2_NORMAL_THERMODYNAMIC_CONSISTENCY': "
        "'uet_o2_normal_thermodynamic_consistency',",
    )
    insertion = f"'{RESULT_ID}': '{LANE_KEY}', "
    for anchor in anchors:
        if anchor in text:
            TARGET.write_text(text.replace(anchor, anchor + insertion, 1), encoding="utf-8")
            print("PASS_REPAIRED_TOPIC13_RENORMALIZED_NORMAL_LANE_KEY")
            return 0
    raise SystemExit("full gate lane map anchor not found")


if __name__ == "__main__":
    raise SystemExit(main())
