"""Repair Topic 13 source-state drift with explicit comparison/raw sub-lanes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SYNC = ROOT / "docs/scripts/audit/sync_topic13_ding_source_mapping_gate.py"
FULL_GATE = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
PACKAGE = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/matter_space_second_sound_source_package.json"
REVIEW = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/matter_space_thermal_source_review.json"

OLD_BLOCKER = "ttg_numeric_source_package_is_provisional"
NEW_RAW_BLOCKER = "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing"


def replace_first(text: str, old: str, new: str) -> str:
    return text.replace(old, new, 1) if old in text else text


def update_json(path: Path, update) -> None:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    update(value)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def repair_sync() -> None:
    text = SYNC.read_text(encoding="utf-8-sig")
    text = replace_first(
        text,
        '    source_ready = bool(audit.get("source_route_ready_for_full_closure"))\n',
        '    normalized_source_ready = bool(audit.get("checks", {}).get("permitted_figure_numeric_route_ready"))\n'
        '    raw_author_source_ready = bool(audit.get("checks", {}).get("raw_author_numeric_source_present"))\n'
        '    source_ready = raw_author_source_ready\n',
    )
    text = replace_first(
        text,
        '        "ttg_numeric_source_package_is_provisional",\n',
        '        "ttg_numeric_source_package_is_provisional",\n'
        f'        "{NEW_RAW_BLOCKER}",\n',
    )
    text = replace_first(
        text,
        '        if source_ready\n        else "PROVISIONAL_NUMERIC_SOURCE_INTAKE"\n',
        '        if normalized_source_ready\n        else "RAW_AUTHOR_NUMERIC_SOURCE_OPEN"\n',
    )
    text = replace_first(
        text,
        '    source["figure_derived_numeric_route_ready"] = source_ready\n',
        '    source["figure_derived_numeric_route_ready"] = normalized_source_ready\n',
    )
    text = replace_first(
        text,
        '    source["provisional_source_present"] = True\n',
        '    source["provisional_source_present"] = not raw_author_source_ready\n'
        '    source["normalized_comparison_route_ready"] = normalized_source_ready\n',
    )
    text = replace_first(text, '    if source_ready:\n', '    if normalized_source_ready:\n')
    text = replace_first(
        text,
        '        provisional_blocker = "ttg_numeric_source_package_is_provisional"\n',
        f'        provisional_blocker = "{NEW_RAW_BLOCKER}"\n',
    )
    text = replace_first(
        text,
        '            "Acquire a permitted raw-author or independently reproduced numeric TTG package with "\n',
        '            "Acquire Ding raw-author or accepted independently reproduced PBTE C_src(T) rows with "\n',
    )
    text = replace_first(
        text,
        '        "source_route_ready_for_full_closure": source_ready,\n',
        '        "source_route_ready_for_full_closure": source_ready,\n'
        '        "normalized_comparison_route_ready": normalized_source_ready,\n'
        '        "raw_author_numeric_source_present": raw_author_source_ready,\n',
    )
    SYNC.write_text(text, encoding="utf-8")


def repair_full_gate() -> None:
    text = FULL_GATE.read_text(encoding="utf-8-sig")
    text = replace_first(
        text,
        '    source_ready = source_status == "SOURCE_LOCKED_NUMERIC"\n',
        '    normalized_source_ready = bool(\n'
        '        source_contract.get("normalized_comparison_route_ready")\n'
        '        or ding_source_mapping.get("checks", {}).get("permitted_figure_numeric_route_ready", False)\n'
        '    )\n'
        '    raw_author_source_ready = bool(\n'
        '        source_contract.get("raw_author_numeric_route_ready")\n'
        '        or ding_source_mapping.get("checks", {}).get("raw_author_numeric_source_present", False)\n'
        '    )\n'
        '    source_ready = normalized_source_ready\n',
    )
    text = replace_first(
        text,
        '            "source_ready_for_full_closure": source_ready,\n',
        '            "source_ready_for_full_closure": raw_author_source_ready,\n'
        '            "normalized_comparison_route_ready": normalized_source_ready,\n'
        '            "raw_author_C_src_route_ready": raw_author_source_ready,\n',
    )
    text = replace_first(
        text,
        '            "controlling_blocker": "ttg_numeric_source_package_is_provisional" if not source_ready else None,\n',
        f'            "raw_author_C_src_controlling_blocker": "{NEW_RAW_BLOCKER}" if not raw_author_source_ready else None,\n'
        '            "controlling_blocker": None if source_ready else "ttg_numeric_source_package_is_provisional",\n',
    )
    text = replace_first(
        text,
        '                "formal_conserved_C_no_go_or_explicit_regularization_missing",\n',
        '                "formal_conserved_C_no_go_or_explicit_regularization_missing",\n'
        f'                "{OLD_BLOCKER}",\n',
    )
    FULL_GATE.write_text(text, encoding="utf-8")


def repair_source_records() -> None:
    def update_package(value: dict) -> None:
        value["status"] = "FIGURE_DERIVED_NORMALIZED_COMPARISON_READY_RAW_AUTHOR_C_SRC_OPEN"
        value["claim_boundary"] = (
            "Ding 2022 is a permitted CC BY figure-derived normalized-shape source with closed printed-legend mapping; "
            "the raw-author PBTE C_src(T) route remains open and no alpha_Phi_K calibration is emitted."
        )
        for row in value.get("sources", []):
            if row.get("source_id") == "ding_2022_fig1d_digitized":
                row["status"] = "FIGURE_DERIVED_NUMERIC_PACKAGE_WITH_CLOSED_MAPPING"
                row["benchmark_role"] = "permitted training/comparison source for normalized shape only; no fitting in current wave"

    def update_review(value: dict) -> None:
        value["status"] = "FIGURE_DERIVED_NORMALIZED_COMPARISON_READY_RAW_AUTHOR_C_SRC_OPEN"
        value["claim_boundary"] = (
            "Ding 2022 Figure 1d is ready for permitted normalized comparison with closed mapping; "
            "raw-author PBTE C_src(T), base Phi-to-energy mapping, and alpha_Phi_K remain open."
        )
        for row in value.get("sources", []):
            if row.get("source_id") == "ding_2022_fig1d_digitized":
                row["status"] = "FIGURE_DERIVED_NUMERIC_PACKAGE_WITH_CLOSED_MAPPING"
                row["benchmark_role"] = "permitted training/comparison source for normalized shape only; no fitting in current wave"

    update_json(PACKAGE, update_package)
    update_json(REVIEW, update_review)


def main() -> int:
    repair_sync()
    repair_full_gate()
    repair_source_records()
    print("REPAIRED_TOPIC13_SOURCE_STATE_MACHINE_V3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
