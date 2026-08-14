"""Add the conservative-action Kubo identifiability lane to the full gate."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
ANCHOR = (
    "'T13_UET_O2_GAUSSIAN_OFFSHELL_BACKGROUND_BOUNDARY': "
    "'uet_o2_gaussian_offshell_background_boundary',"
)
INSERT = (
    "'T13_TRANSPORT_COEFFICIENT_IDENTIFIABILITY_NO_GO': "
    "'transport_coefficient_identifiability_no_go', "
)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    if "T13_TRANSPORT_COEFFICIENT_IDENTIFIABILITY_NO_GO" not in text:
        if ANCHOR not in text:
            raise SystemExit("full gate lane map anchor not found")
        text = text.replace(ANCHOR, ANCHOR + INSERT, 1)
        TARGET.write_text(text, encoding="utf-8")
    print("PASS_REPAIRED_TOPIC13_TRANSPORT_IDENTIFIABILITY_LANE_KEY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
