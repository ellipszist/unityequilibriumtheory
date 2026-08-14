"""Separate normalized figure-comparison readiness from raw-author C_src readiness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PROVENANCE = ROOT / "docs/scripts/audit/audit_thermal_source_provenance.py"
BRANCH = ROOT / "docs/scripts/audit/audit_thermal_wave1_branch_gate.py"
SYNC = ROOT / "docs/scripts/audit/sync_topic13_ding_source_mapping_gate.py"
FULL_GATE = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
PACKAGE = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/matter_space_second_sound_source_package.json"
REVIEW = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/matter_space_thermal_source_review.json"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


def update_json(path: Path, updater) -> None:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    updater(value)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def repair_provenance() -> None:
    text = PROVENANCE.read_text(encoding="utf-8-sig")
    text = replace_once(
        text,
        '    local_rows = [row for row in rows if row["local_numeric_present"]]\n',
        '    local_rows = [row for row in rows if row["local_numeric_present"]]\n'
        '    normalized_rows = [\n'
        '        row for row in rows\n'
        '        if row["local_numeric_present"]\n'
        '        and row["source_id"] == "ding_2022_fig1d_digitized"\n'
        '        and row["status"] == "FIGURE_DERIVED_NUMERIC_PACKAGE_WITH_CLOSED_MAPPING"\n'
        '    ]\n'
        '    raw_author_rows = [\n'
        '        row for row in rows\n'
        '        if row["local_numeric_present"]\n'
        '        and row["source_id"] != "ding_2022_fig1d_digitized"\n'
        '        and row["status"] == "SOURCE_LOCKED_NUMERIC"\n'
        '    ]\n',
        "source role lists",
    )
    text = replace_once(
        text,
        '    mapping["evidence_class"] = "SOURCE_BACKED_PROVISIONAL_NUMERIC_INTAKE_WITH_DIMENSIONAL_BLOCKER"\n',
        '    mapping["evidence_class"] = "SOURCE_BACKED_FIGURE_DERIVED_NORMALIZED_COMPARISON_WITH_DIMENSIONAL_BLOCKER"\n',
        "mapping evidence class",
    )
    text = replace_once(
        text,
        '    mapping["measurement_operator"]["raw_signal_status"] = "DING_2022_FIGURE_DIGITIZATION_LOCAL_PROVISIONAL; XIE_2026_HOLDOUT_METADATA_ONLY"\n',
        '    mapping["measurement_operator"]["raw_signal_status"] = "DING_2022_FIGURE_DIGITIZATION_LOCAL_NORMALIZED_COMPARISON; XIE_2026_HOLDOUT_METADATA_ONLY"\n',
        "measurement status",
    )
    text = replace_once(
        text,
        '    mapping["gates"]["source_package_provenance_complete"] = provenance_complete\n',
        '    mapping["gates"]["source_package_provenance_complete"] = provenance_complete\n'
        '    mapping["gates"]["normalized_comparison_route_ready"] = bool(normalized_rows) and not failures\n'
        '    mapping["gates"]["raw_author_numeric_route_ready"] = bool(raw_author_rows) and not failures\n',
        "mapping source gates",
    )
    text = replace_once(
        text,
        '    mapping["blockers"] = [\n        "Ding 2022 numeric intake is a provisional figure digitization, not an author-provided raw table",\n',
        '    mapping["blockers"] = [\n        "Ding 2022 raw-author PBTE C_src(T) is not captured; the permitted figure-derived normalized comparison route is separate and ready",\n',
        "mapping blockers",
    )
    text = replace_once(
        text,
        '    mapping["next_required_artifact"] = "independent alpha_Phi_K calibration/derivation with uncertainty plus a preregistered normalized comparison using only non-holdout rows"\n',
        '    mapping["next_required_artifact"] = "raw-author or accepted independent PBTE C_src(T) reproduction plus independent alpha_Phi_K calibration/derivation with uncertainty; normalized comparison is already source-ready and must use only non-holdout rows"\n',
        "mapping next artifact",
    )
    text = replace_once(
        text,
        '        "status": "PASS_WITH_PROVISIONAL_DIGITIZATION" if provenance_complete and not holdout_consumed else "BLOCKED",\n',
        '        "status": "PASS_WITH_FIGURE_DERIVED_NORMALIZED_COMPARISON" if bool(normalized_rows) and not failures and not holdout_consumed else "BLOCKED",\n',
        "provenance status",
    )
    text = replace_once(
        text,
        '        "metrics": {"source_count": len(rows), "local_numeric_count": len(local_rows), "holdout_count": len(holdout_rows), "holdout_consumed": holdout_consumed, "provenance_complete": provenance_complete},\n',
        '        "metrics": {"source_count": len(rows), "local_numeric_count": len(local_rows), "normalized_comparison_count": len(normalized_rows), "raw_author_numeric_count": len(raw_author_rows), "holdout_count": len(holdout_rows), "holdout_consumed": holdout_consumed, "provenance_complete": provenance_complete},\n',
        "provenance metrics",
    )
    text = replace_once(
        text,
        '        "controlling_blocker": "provisional figure intake is not raw author data and independent alpha_Phi_K remains open",\n',
        '        "controlling_blocker": "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing; independent alpha_Phi_K remains open",\n',
        "provenance blocker",
    )
    text = replace_once(
        text,
        '        "next_action": "replace or supplement the provisional figure intake with an authorized numeric source or keep the dimensional/external gate blocked; do not digitize Xie 2026",\n',
        '        "next_action": "keep the normalized figure-derived route in comparison-only role; obtain raw-author or accepted independent PBTE C_src(T) and an independent alpha_Phi_K anchor without reading Xie 2026",\n',
        "provenance next action",
    )
    PROVENANCE.write_text(text, encoding="utf-8")


def repair_branch() -> None:
    text = BRANCH.read_text(encoding="utf-8-sig")
    text = replace_once(
        text,
        '    provisional_source = any(row.get("status") == "PROVISIONAL_DIGITIZED_NUMERIC_PACKAGE" for row in source_rows)\n',
        '    normalized_source_ready = any(\n'
        '        row.get("source_id") == "ding_2022_fig1d_digitized"\n'
        '        and row.get("status") == "FIGURE_DERIVED_NUMERIC_PACKAGE_WITH_CLOSED_MAPPING"\n'
        '        for row in source_rows\n'
        '    )\n'
        '    raw_author_source_ready = any(\n'
        '        row.get("status") == "SOURCE_LOCKED_NUMERIC"\n'
        '        and row.get("source_id") != "ding_2022_fig1d_digitized"\n'
        '        for row in source_rows\n'
        '    )\n',
        "branch source readiness",
    )
    text = replace_once(
        text,
        '        "provisional_source_provenance_present": provisional_source,\n',
        '        "normalized_comparison_route_ready": normalized_source_ready,\n'
        '        "raw_author_numeric_route_ready": raw_author_source_ready,\n'
        '        "provisional_source_provenance_present": not raw_author_source_ready,\n',
        "branch source gates",
    )
    text = replace_once(
        text,
        '"selected_causal_reference_prearrival_leakage", "selected_causal_reference_compact_support", "locked_threshold_unchanged", "holdout_not_consumed", "numeric_fitting_disabled", "provisional_source_provenance_present"',
        '"selected_causal_reference_prearrival_leakage", "selected_causal_reference_compact_support", "locked_threshold_unchanged", "holdout_not_consumed", "numeric_fitting_disabled", "normalized_comparison_route_ready"',
        "branch status gate",
    )
    text = replace_once(
        text,
        '            "provisional_source_present": provisional_source,\n',
        '            "provisional_source_present": not raw_author_source_ready,\n'
        '            "normalized_comparison_route_ready": normalized_source_ready,\n'
        '            "raw_author_numeric_route_ready": raw_author_source_ready,\n',
        "branch source contract",
    )
    BRANCH.write_text(text, encoding="utf-8")


def repair_sync() -> None:
    text = SYNC.read_text(encoding="utf-8-sig")
    text = replace_once(
        text,
        '        "ttg_numeric_source_package_is_provisional",\n',
        '        "ttg_numeric_source_package_is_provisional",\n        "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing",\n',
        "sync compatibility blockers",
    )
    text = replace_once(
        text,
        '    source["provisional_source_present"] = True\n',
        '    source["provisional_source_present"] = not raw_author_numeric_source_present\n'
        '    source["normalized_comparison_route_ready"] = bool(audit.get("checks", {}).get("permitted_figure_numeric_route_ready"))\n',
        "sync source status",
    )
    text = replace_once(
        text,
        '        provisional_blocker = "ttg_numeric_source_package_is_provisional"\n',
        '        provisional_blocker = "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing"\n',
        "sync source blocker",
    )
    text = replace_once(
        text,
        '            "Acquire a permitted raw-author or independently reproduced numeric TTG package with "\n',
        '            "Acquire Ding raw-author or accepted independently reproduced PBTE C_src(T) rows with "\n',
        "sync source next action",
    )
    SYNC.write_text(text, encoding="utf-8")


def repair_review_and_package() -> None:
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


def repair_full_gate() -> None:
    text = FULL_GATE.read_text(encoding="utf-8-sig")
    text = replace_once(
        text,
        '            "controlling_blocker": "ttg_numeric_source_package_is_provisional" if not source_ready else None,\n',
        '            "normalized_comparison_route_ready": bool(ding_source_mapping.get("checks", {}).get("permitted_figure_numeric_route_ready", False)),\n'
        '            "raw_author_C_src_route_ready": bool(ding_source_mapping.get("checks", {}).get("raw_author_numeric_source_present", False)),\n'
        '            "controlling_blocker": "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing" if not source_ready else None,\n',
        "full gate source fields",
    )
    text = replace_once(
        text,
        '        "ttg_numeric_source_package_is_provisional",\n',
        '        "ttg_numeric_source_package_is_provisional",\n        "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing",\n',
        "full gate source blocker compatibility",
    )
    FULL_GATE.write_text(text, encoding="utf-8")


def main() -> int:
    repair_provenance()
    repair_branch()
    repair_sync()
    repair_review_and_package()
    repair_full_gate()
    print("REPAIRED_TOPIC13_NORMALIZED_SOURCE_STATE_MACHINE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
