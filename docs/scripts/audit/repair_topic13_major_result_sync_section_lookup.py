"""Allow Topic 13 register sync to consume lanes from their owning section."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/sync_topic13_major_result_lanes.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    anchor = '    source_package = full["verification_status"]["source_package"]\n'
    addition = (
        '    source_package = full["verification_status"]["source_package"]\n\n'
        '    def projection_for_lane(lane_key: str) -> dict:\n'
        '        """Read a lane from the section that owns its evidence role."""\n\n'
        '        sections = full.get("verification_status", {})\n'
        '        for section_name in (\n'
        '            "source_package",\n'
        '            "eos_transport_kms_entropy",\n'
        '            "dimensional_observable_map",\n'
        '        ):\n'
        '            section = sections.get(section_name, {})\n'
        '            candidate = section.get(lane_key)\n'
        '            if isinstance(candidate, dict):\n'
        '                return candidate\n'
        '        return {}\n'
    )
    text = replace_once(text, anchor, addition, "section projection helper")
    text = replace_once(
        text,
        "        projection = source_package.get(lane_key)\n",
        "        projection = projection_for_lane(lane_key)\n",
        "new-record projection lookup",
    )
    text = replace_once(
        text,
        '            "closure_level": source_package[lane_key].get("closure_level"),\n            "status": source_package[lane_key].get("status"),\n            "full_core_unlock": False,\n            "audit": source_package[lane_key].get("audit"),\n',
        '            "closure_level": projection_for_lane(lane_key).get("closure_level"),\n            "status": projection_for_lane(lane_key).get("status"),\n            "full_core_unlock": False,\n            "audit": projection_for_lane(lane_key).get("audit"),\n',
        "dependency projection lookup",
    )
    TARGET.write_text(text, encoding="utf-8")
    print("updated Topic 13 register sync to read section-owned lane projections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
