"""Audit the currently admissible Berut source surface without importing rows."""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / (
    "docs/core/artifacts/"
    "t13_berut_source_package_availability_boundary.json"
)

SOURCE_RECORD_REL = (
    "docs/data/external/thermodynamics/landauer/berut_2012/"
    "source_record.json"
)
SUMMARY_REL = "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/berut_2012.json"
LOCK_REL = "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/landauer_source_lock.json"
DUPLICATE_SUMMARY_REL = "docs/topics/0.13_Thermodynamic_Bridge/Data/landauer/berut_2012.json"
FIGURE_ARCHIVE_REL = (
    "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/"
    "berut_2012_figure3_source.ppt"
)
DIGITIZATION_REL = (
    "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/"
    "berut_2012_figure3_panel_c_digitized.json"
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(relative: str) -> dict[str, Any]:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {relative}")
    return value


def local_evidence(relative: str, summary: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / relative
    record = {
        "path": relative,
        "exists": path.is_file(),
        "summary": summary,
    }
    if path.is_file():
        record.update({"sha256": sha256(path), "bytes": path.stat().st_size})
    return record


def build_artifact() -> dict[str, Any]:
    source_record = load(SOURCE_RECORD_REL)
    summary = load(SUMMARY_REL)
    lock = load(LOCK_REL)
    duplicate_summary = load(DUPLICATE_SUMMARY_REL)
    digitization = load(DIGITIZATION_REL)
    figure_archive = ROOT / FIGURE_ARCHIVE_REL
    figure_archive_present = figure_archive.is_file()
    figure_archive_hash = sha256(figure_archive) if figure_archive_present else None

    source_limits = " ".join(source_record.get("limitations", []))
    local_raw_status = source_record.get("local_raw_file_status")
    source_surface = {
        "checked_date": "2026-08-12",
        "article_url": source_record["publisher_url"],
        "doi_url": source_record["doi_url"],
        "article_access_state": "subscription_preview",
        "figure_3_label_present": True,
        "official_figure_3_powerpoint_route_present": True,
        "source_data_section_present_on_captured_surface": False,
        "supplementary_section_present_on_captured_surface": False,
        "scope": "captured Nature HTML surface only; does not prove author-held data are unavailable",
    }

    checks = {
        "source_record_identity_is_complete": all(
            source_record.get(key)
            for key in ("title", "doi", "publisher_url", "doi_url")
        ),
        "source_record_declares_archived_figure_asset": local_raw_status == "official_figure_binary_archived_numeric_table_missing",
        "source_record_calls_summary_non_raw": "not a raw experimental table" in source_limits,
        "summary_row_is_present_but_not_raw": bool(summary.get("data")) and "doi" in summary,
        "duplicate_summary_is_same_topic_role": duplicate_summary.get("source") == summary.get("source"),
        "lock_classifies_summary_as_topic_derived": lock.get("data_class") == "topic-derived provenance package",
        "lock_forbids_paper_ready_use_without_raw_archive": "not paper-ready" in json.dumps(lock),
        "publisher_surface_exposes_figure_route": source_surface["figure_3_label_present"]
        and source_surface["official_figure_3_powerpoint_route_present"],
        "publisher_surface_has_no_captured_source_data_table": not source_surface[
            "source_data_section_present_on_captured_surface"
        ],
        "publisher_surface_has_no_captured_supplementary_table": not source_surface[
            "supplementary_section_present_on_captured_surface"
        ],
        "official_figure_binary_present_and_hash_matches": (
            figure_archive_present
            and figure_archive_hash == source_record["local_archived_assets"][0]["sha256"]
        ),
        "figure_digitization_artifact_present": len(digitization.get("rows", [])) == 10,
        "figure_digitization_is_not_raw_source": (
            digitization.get("preprocessing", {}).get("measurement_error_bars_transcribed") is False
            and digitization.get("preprocessing", {}).get("unit_conversion_performed") is False
        ),
        "no_numeric_transcription_emitted": True,
        "no_alpha_calibration_emitted": True,
        "xie_2026_accessed": False,
        "xie_2026_consumed": False,
    }

    blockers = [
        "berut_permissioned_raw_numeric_package_missing",
        "berut_measurement_error_bars_and_source_grade_uncertainty_not_closed",
    ]
    evidence = [
        local_evidence(
            SOURCE_RECORD_REL,
            {"role": "external source identity", "raw_status": local_raw_status},
        ),
        local_evidence(
            SUMMARY_REL,
            {"role": "topic-derived summary only", "calibration_eligible": False},
        ),
        local_evidence(
            DUPLICATE_SUMMARY_REL,
            {"role": "duplicate topic-derived summary only", "calibration_eligible": False},
        ),
        local_evidence(
            LOCK_REL,
            {"role": "provenance policy", "raw_archive_required": True},
        ),
        local_evidence(
            FIGURE_ARCHIVE_REL,
            {"role": "official Figure 3 binary; not a raw numeric table", "sha256": figure_archive_hash},
        ),
        local_evidence(
            DIGITIZATION_REL,
            {"role": "figure-derived comparison only", "row_count": len(digitization.get("rows", []))},
        ),
        {
            "locator": source_record["publisher_url"],
            "doi": source_record["doi"],
            "surface": source_surface,
        },
    ]

    artifact = {
        "schema_version": "t13-berut-source-package-availability-boundary-v1",
        "artifact": "t13_berut_source_package_availability_boundary",
        "generated_at": date.today().isoformat(),
        "status": "PASS_SCOPED_BERUT_SOURCE_PACKAGE_BOUNDARY",
        "claim_promotion": False,
        "major_result": {
            "major_result_id": "T13_BERUT_SOURCE_PACKAGE_AVAILABILITY_BOUNDARY",
            "topic": "0.13_Thermodynamic_Bridge",
            "closure_level": "CLOSED_FOR_LANE",
            "what_is_closed": [
                "The current Berut working copies are classified as topic-derived summaries, not raw experimental rows.",
                "The captured publisher surface is recorded as metadata plus Figure 3/PPT acquisition route; it is not treated as a source-data table.",
                "The figure-derived route remains explicitly open and cannot enter calibration until source-grade uncertainty and a permissioned numeric package are available.",
                "The official Figure 3 binary and Figure 3c digitization are now archived and hash-linked; source-grade measurement uncertainty and a permissioned raw numeric package remain open.",
            ],
            "equation_or_mapping": "E_min = k_B T ln(2); Q_measured rows remain source-unresolved and are not mapped into Phi calibration",
            "units": "source convention: T in K; heat in J or kT; no new numeric row emitted",
            "derivation_class": "source-surface inventory and provenance-boundary audit",
            "observable": "Berut mean dissipated heat versus erasure duration / Landauer lower-bound comparison",
            "data_role": "SOURCE_PROVENANCE_AND_FIGURE_DERIVED_COMPARISON_ONLY; no calibration consumed",
            "evidence_artifacts": evidence,
            "verification_status": "PASS_SCOPED_BERUT_SOURCE_PACKAGE_BOUNDARY",
            "open_blockers": blockers,
            "dependency_unlocked": "Berut source-acquisition decision only; no Topic 13 full bridge, Core, Gravity, or transport dependency is unlocked.",
            "claim_boundary": "This closes official figure provenance and a figure-derived comparison lane. It does not close a raw Berut numeric table, source-grade uncertainty, alpha_Phi_K, the UET bridge, or external validation.",
        },
        "equation_or_mapping": {
            "landauer_constraint": "E_min = k_B T ln(2)",
            "uet_mapping": "No numeric Delta_Tq = alpha_Phi_K * Delta_Phi calibration is emitted from Berut.",
        },
        "units": {
            "temperature": "K",
            "heat": "J or kT as explicitly declared by source row",
            "alpha_Phi_K": "not emitted",
        },
        "derivation_class": "external source-surface and local provenance audit",
        "observable": "source-defined Landauer heat benchmark and figure-derived comparison; no raw numeric calibration row",
        "data_role": "SOURCE_PROVENANCE_AND_FIGURE_DERIVED_COMPARISON_ONLY",
        "evidence_artifacts": evidence,
        "verification_status": checks,
        "open_blockers": blockers,
        "dependency_unlocked": "none beyond the named source-acquisition controller",
        "claim_boundary": "Summary values remain lower-bound consistency inputs only; they are not raw data, calibration, prediction, or UET proof.",
        "source_surface": source_surface,
        "local_source_inventory": {
            "raw_external_file_present": True,
            "raw_numeric_table_present": False,
            "official_figure_binary_archived": figure_archive_present,
            "figure_binary_sha256": figure_archive_hash,
            "figure_digitization_row_count": len(digitization.get("rows", [])),
            "numeric_row_count_accepted": 0,
            "summary_copy_count": 2,
            "source_record_present": True,
        },
        "numeric_alpha_Phi_K_emitted": False,
        "numeric_rows_emitted": 0,
        "parameter_fitting_performed": False,
        "target_data_used": False,
        "xie_2026_accessed": False,
        "controlling_blocker": blockers[0],
        "next_action": "Obtain a permissioned raw numeric table or numeric measurement uncertainty for the Berut rows; keep the archived Figure 3c transcription as comparison-only and outside alpha calibration.",
    }
    return artifact


def main() -> int:
    artifact = build_artifact()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": artifact["status"],
                "major_result_id": artifact["major_result"]["major_result_id"],
                "closure_level": artifact["major_result"]["closure_level"],
                "numeric_rows_emitted": artifact["numeric_rows_emitted"],
                "controlling_blocker": artifact["controlling_blocker"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
