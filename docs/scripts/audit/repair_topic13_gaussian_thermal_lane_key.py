"""Register the Topic 13 Gaussian finite-temperature lane with the full gate."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    marker = "'T13_UET_O2_CONDENSATE_FLUCTUATION_SPECTRUM': 'uet_o2_condensate_fluctuation_spectrum'"
    entry = ", 'T13_UET_O2_CONDENSATE_GAUSSIAN_FINITE_T_LANE': 'uet_o2_condensate_gaussian_finite_t_lane'"
    if "T13_UET_O2_CONDENSATE_GAUSSIAN_FINITE_T_LANE" in text:
        print("GAUSSIAN_THERMAL_LANE_KEY_ALREADY_PRESENT")
        return 0
    if marker not in text:
        raise SystemExit("full gate O(2) fluctuation lane anchor not found")
    TARGET.write_text(text.replace(marker, marker + entry, 1), encoding="utf-8")
    print("ADDED_TOPIC13_GAUSSIAN_THERMAL_LANE_KEY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
