"""Register the bounded Ding Fig. 1d lane in the canonical full gate."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    needle = "'T13_DING_PBTE_AUTHOR_REQUEST_PACKAGE': 'ding_pbte_author_request_package', "
    addition = needle + "'T13_DING_FIG1D_NORMALIZED_SOURCE_LANE': 'ding_fig1d_normalized_source_lane', "
    if "T13_DING_FIG1D_NORMALIZED_SOURCE_LANE" in text:
        print("DING_FIG1D_LANE_KEY_ALREADY_PRESENT")
        return 0
    if text.count(needle) != 1:
        raise SystemExit(f"Ding mapping anchor count: {text.count(needle)}")
    TARGET.write_text(text.replace(needle, addition, 1), encoding="utf-8")
    print("ADDED_DING_FIG1D_LANE_KEY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
