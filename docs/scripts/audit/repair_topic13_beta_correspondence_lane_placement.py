"""Keep the beta-correspondence no-go under the bridge gate."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    marker = "    # Keep source-acquisition evidence in the source-package lane.\n"
    insertion = """    beta_correspondence_lane = merged_lane_integrations.get(
        "beta_action_normalized_correspondence_no_go"
    )
    if beta_correspondence_lane:
        artifact["verification_status"]["non_circular_bridge"][
            "beta_action_normalized_correspondence_no_go"
        ] = beta_correspondence_lane
        artifact["verification_status"]["eos_transport_kms_entropy"].pop(
            "beta_action_normalized_correspondence_no_go", None
        )
    # Keep source-acquisition evidence in the source-package lane.
"""
    if insertion.strip() in text:
        print("TOPIC13_BETA_CORRESPONDENCE_LANE_PLACEMENT_ALREADY_PRESENT")
        return 0
    if marker not in text:
        raise SystemExit("full gate source-package placement anchor not found")
    TARGET.write_text(text.replace(marker, insertion, 1), encoding="utf-8")
    print("PASS_REPAIRED_TOPIC13_BETA_CORRESPONDENCE_LANE_PLACEMENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
