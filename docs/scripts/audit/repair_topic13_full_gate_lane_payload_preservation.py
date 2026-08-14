"""Preserve lane-specific payloads when the canonical Topic 13 gate is rebuilt."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    if "lane_record = {" in text:
        print("FULL_GATE_LANE_PAYLOAD_PRESERVATION_ALREADY_PRESENT")
        return 0

    text = replace_once(
        text,
        "            key = LANE_KEY_BY_ID[result_id]\n            discovered_lane_integrations[key] = {\n",
        "            key = LANE_KEY_BY_ID[result_id]\n"
        "            # Keep lane-specific diagnostics instead of reducing the record\n"
        "            # to a status-only summary.\n"
        "            lane_record = {\n"
        "                field: value\n"
        "                for field, value in candidate.items()\n"
        "                if field not in {\"schema_version\", \"artifact\", \"generated_at\", \"major_result\", \"evidence_artifacts\"}\n"
        "            }\n"
        "            lane_record.update({\n",
        "full-gate lane payload start",
    )
    text = replace_once(
        text,
        "                \"claim_boundary\": major.get(\"claim_boundary\", \"artifact-reported boundary\"),\n            }\n    previous_major = previous_gate.get(\"major_result\", {})\n",
        "                \"claim_boundary\": major.get(\"claim_boundary\", \"artifact-reported boundary\"),\n"
        "            })\n"
        "            discovered_lane_integrations[key] = lane_record\n"
        "    previous_major = previous_gate.get(\"major_result\", {})\n",
        "full-gate lane payload end",
    )
    TARGET.write_text(text, encoding="utf-8")
    print("ADDED_FULL_GATE_LANE_PAYLOAD_PRESERVATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
