"""Add the normal-response-curvature lane to the Topic 13 full gate."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    result_id = "T13_UET_O2_NORMAL_RESPONSE_CURVATURE_LANE"
    if result_id in text:
        print("TOPIC13_NORMAL_RESPONSE_CURVATURE_LANE_KEY_ALREADY_PRESENT")
        return 0
    anchors = (
        "'T13_TRANSPORT_COEFFICIENT_IDENTIFIABILITY_NO_GO': "
        "'transport_coefficient_identifiability_no_go',",
        "'T13_UET_O2_GAUSSIAN_OFFSHELL_BACKGROUND_BOUNDARY': "
        "'uet_o2_gaussian_offshell_background_boundary',",
    )
    insert = (
        "'T13_UET_O2_NORMAL_RESPONSE_CURVATURE_LANE': "
        "'uet_o2_normal_response_curvature_lane', "
    )
    for anchor in anchors:
        if anchor in text:
            TARGET.write_text(text.replace(anchor, anchor + insert, 1), encoding="utf-8")
            print("PASS_REPAIRED_TOPIC13_NORMAL_RESPONSE_CURVATURE_LANE_KEY")
            return 0
    raise SystemExit("full gate lane map anchor not found")


if __name__ == "__main__":
    raise SystemExit(main())
