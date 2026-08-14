"""Make Topic 13 source readiness distinguish normalized comparison from raw C_src."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SYNC = ROOT / "docs/scripts/audit/sync_topic13_ding_source_mapping_gate.py"
FULL_GATE = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
PACKAGE = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/matter_space_second_sound_source_package.json"
REVIEW = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/matter_space_thermal_source_review.json"

NEW_BLOCKER = "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing"
OLD_BLOCKER = "ttg_numeric_source_package_is_provisional"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


def replace_all_line(text: str, old_line: str, new_lines: str, label: str) -> str:
    if new_lines in text:
        return text
    count = text.count(old_line)
    if count == 0:
        raise SystemExit(f"{label}: no match")
    return text.replace(old_line, new_lines)


def update_json(path: Path, updater) -> None:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    updater(value)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def repair_sync() -> None:
    text = SYNC.read_text(encoding="utf-8-sig")
    text = replace_once(
        text,
        '    source_ready = bool(audit.get("source_route_ready_for_full_closure"))\n',
        '    normalized_source_ready = bool(\n'
        '        audit.get("checks", {}).get("permitted_figure_numeric_route_ready")\n'
        '    )\n'
        '    raw_author_source_ready = bool(\n'
        '        audit.get("checks", {}).get("raw_author_numeric_source_present")\n'
        '    )\n'
        '    source_ready = raw_author_source_ready\n',
        "Ding readiness split",
    )
    text = replace_once(
        text,
        '        "ttg_numeric_source_package_is_provisional",\n',
        '        "ttg_numeric_source_package_is_provisional",\n        "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing",\n',
        "compatibility blocker insertion",
    )
    text = replace_once(
        text,
        '        "FIGURE_DERIVED_PERMITTED_WITH_CLOSED_MAPPING"\n        if source_ready\n        else "PROVISIONAL_NUMERIC_SOURCE_INTAKE"\n',
        '        "FIGURE_DERIVED_PERMITTED_WITH_CLOSED_MAPPING"\n        if normalized_source_ready\n        else "RAW_AUTHOR_NUMERIC_SOURCE_OPEN"\n',
        "source status projection",
    )
    text = replace_once(
        text,
        '    source["figure_derived_numeric_route_ready"] = source_ready\n',
        '    source["figure_derived_numeric_route_ready"] = normalized_source_ready\n',
        "normalized route field",
    )
    text = replace_once(
        text,
        '    source["provisional_source_present"] = True\n',
        '    source["provisional_source_present"] = not raw_author_source_ready\n'
        '    source["normalized_comparison_route_ready"] = normalized_source_ready\n',
        "provisional source field",
    )
    text = replace_once(
        text,
        '        provisional_blocker = "ttg_numeric_source_package_is_provisional"\n',
        f'        provisional_blocker = "{NEW_BLOCKER}"\n',
        "active source blocker",
    )
    text = replace_once(
        text,
        '            "Acquire a permitted raw-author or independently reproduced numeric TTG package with "\n',
        '            "Acquire Ding raw-author or accepted independently reproduced PBTE C_src(T) rows with "\n',
        "source next action",
    )
    text = replace_once(
        text,
        '                "source_route_ready_for_full_closure": source_ready,\n',
        '                "source_route_ready_for_full_closure": source_ready,\n'
        '                "normalized_comparison_route_ready": normalized_source_ready,\n'
        '                "raw_author_numeric_source_present": raw_author_source_ready,\n',
        "source evidence summary",
    )
    text = replace_once(
        text,
        '        "source_route_ready_for_full_closure": source_ready,\n',
        '        "source_route_ready_for_full_closure": source_ready,\n'
        '        "normalized_comparison_route_ready": normalized_source_ready,\n'
        '        "raw_author_numeric_source_present": raw_author_source_ready,\n',
        "source print summary",
    )
    SYNC.write_text(text, encoding="utf-8")


def repair_full_gate() -> None:
    text = FULL_GATE.read_text(encoding="utf-8-sig")
    text = replace_once(
        text,
        '            "controlling_blocker": "ttg_numeric_source_package_is_provisional" if not source_ready else None,\n',
        f'            "normalized_comparison_route_ready": bool(ding_source_mapping.get("checks", {{}}).get("permitted_figure_numeric_route_ready", False)),\n'
        f'            "raw_author_C_src_route_ready": bool(ding_source_mapping.get("checks", {{}}).get("raw_author_numeric_source_present", False)),\n'
        f'            "controlling_blocker": "{NEW_BLOCKER}" if not source_ready else None,\n',
        "full source blocker projection",
    )
    text = replace_all_line(
        text,
        f'            "ttg_numeric_source_package_is_provisional",\n',
        f'            "ttg_numeric_source_package_is_provisional",\n            "{NEW_BLOCKER}",\n',
        "full compatibility blocker",
    )
    old_set_line = '                "original_conserved_c_gradient_baseline_blocked",\n'
    new_set_line = old_set_line + f'                "{OLD_BLOCKER}",\n'
    text = replace_once(text, old_set_line, new_set_line, "legacy source blocker filter")
    FULL_GATE.write_text(text, encoding="utf-8")


def repair_source_records() -> None:
    def package_update(value: dict) -> None:
        value["status"] = "FIGURE_DERIVED_NORMALIZED_COMPARISON_READY_RAW_AUTHOR_C_SRC_OPEN"
        value["claim_boundary"] = (
            "Ding 2022 is a permitted CC BY figure-derived normalized-shape source with closed printed-legend mapping; "
            "the raw-author PBTE C_src(T) route remains open and no alpha_Phi_K calibration is emitted."
        )
        for row in value.get("sources", []):
            if row.get("source_id") == "ding_2022_fig1d_digitized":
                row["status"] = "FIGURE_DERIVED_NUMERIC_PACKAGE_WITH_CLOSED_MAPPING"
                row["benchmark_role"] = "permitted training/comparison source for normalized shape only; no fitting in current wave"

    def review_update(value: dict) -> None:
        value["status"] = "FIGURE_DERIVED_NORMALIZED_COMPARISON_READY_RAW_AUTHOR_C_SRC_OPEN"
        value["claim_boundary"] = (
            "Ding 2022 Figure 1d is ready for permitted normalized comparison with closed mapping; "
            "raw-author PBTE C_src(T), base Phi-to-energy mapping, and alpha_Phi_K remain open."
        )
        for row in value.get("sources", []):
            if row.get("source_id") == "ding_2022_fig1d_digitized":
                row["status"] = "FIGURE_DERIVED_NUMERIC_PACKAGE_WITH_CLOSED_MAPPING"
                row["benchmark_role"] = "permitted training/comparison source for normalized shape only; no fitting in current wave"

    update_json(PACKAGE, package_update)
    update_json(REVIEW, review_update)


def main() -> int:
    repair_sync()
    repair_full_gate()
    repair_source_records()
    print("REPAIRED_TOPIC13_SOURCE_STATE_MACHINE_V2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
