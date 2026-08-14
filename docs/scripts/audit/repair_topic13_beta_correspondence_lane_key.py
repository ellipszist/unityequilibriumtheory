"""Register the beta-correspondence no-go with the Topic 13 gate."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    result_id = "T13_BETA_ACTION_NORMALIZED_CORRESPONDENCE_NO_GO"
    if result_id in text:
        print("TOPIC13_BETA_CORRESPONDENCE_LANE_KEY_ALREADY_PRESENT")
        return 0
    anchor = "'T13_BETA_SYMBOL_SEPARATION_NONCIRCULARITY_NO_GO': 'beta_symbol_separation_non_circularity_no_go',"
    insert = " 'T13_BETA_ACTION_NORMALIZED_CORRESPONDENCE_NO_GO': 'beta_action_normalized_correspondence_no_go',"
    if anchor not in text:
        raise SystemExit("full gate beta lane anchor not found")
    TARGET.write_text(text.replace(anchor, anchor + insert, 1), encoding="utf-8")
    print("PASS_REPAIRED_TOPIC13_BETA_CORRESPONDENCE_LANE_KEY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
