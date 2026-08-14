"""Add the off-shell Gaussian background lane to the full Topic 13 gate."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
ANCHOR = (
    "'T13_UET_O2_CONDENSATE_GAUSSIAN_FINITE_T_LANE': "
    "'uet_o2_condensate_gaussian_finite_t_lane',"
)
INSERT = (
    "'T13_UET_O2_GAUSSIAN_OFFSHELL_BACKGROUND_BOUNDARY': "
    "'uet_o2_gaussian_offshell_background_boundary', "
)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    if "T13_UET_O2_GAUSSIAN_OFFSHELL_BACKGROUND_BOUNDARY" not in text:
        if ANCHOR not in text:
            raise SystemExit("full gate lane map anchor not found")
        text = text.replace(ANCHOR, ANCHOR + INSERT, 1)
        TARGET.write_text(text, encoding="utf-8")
    print("PASS_REPAIRED_TOPIC13_GAUSSIAN_OFFSHELL_LANE_KEY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
