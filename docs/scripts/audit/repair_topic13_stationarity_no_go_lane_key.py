"""Add the thermal Gaussian stationarity no-go to Topic 13 discovery."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
RESULT_ID = "T13_UET_O2_GAUSSIAN_THERMAL_STATIONARITY_NO_GO"
LANE_KEY = "uet_o2_gaussian_thermal_stationarity_no_go"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    if RESULT_ID in text:
        print("TOPIC13_STATIONARITY_NO_GO_KEY_ALREADY_PRESENT")
        return 0
    anchors = (
        "'T13_UET_O2_THERMAL_STABILITY_BOUNDARY': "
        "'uet_o2_thermal_stability_boundary',",
        "'T13_UET_O2_GAUSSIAN_OFFSHELL_BACKGROUND_BOUNDARY': "
        "'uet_o2_gaussian_offshell_background_boundary',",
    )
    insertion = f"'{RESULT_ID}': '{LANE_KEY}', "
    for anchor in anchors:
        if anchor in text:
            TARGET.write_text(text.replace(anchor, anchor + insertion, 1), encoding="utf-8")
            print("PASS_REPAIRED_TOPIC13_STATIONARITY_NO_GO_KEY")
            return 0
    raise SystemExit("full gate lane map anchor not found")


if __name__ == "__main__":
    raise SystemExit(main())
