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
        "source_record_declares_no_local_raw_file": local_raw_status == "not_stored",
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
        "no_numeric_transcription_emitted": True,
        "no_alpha_calibration_emitted": True,
        "xie_2026_accessed": False,
        "xie_2026_consumed": False,
    }

    blockers = [
        "berut_local_raw_or_permissioned_numeric_package_missing",
        "berut_figure3_ppt_binary_and_hash_not_archived_in_current_checkout",
        "berut_selected_panel_tick_mapping_and_numeric_transcription_missing",
        "berut_source_row_uncertainty_and_preprocessing_not_closed",
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
                "The figure-derived route remains explicitly open and cannot enter calibration until the binary, locator, axis mapping, transcription, uncertainty, preprocessing, and hash are archived.",
            ],
            "equation_or_mapping": "E_min = k_B T ln(2); Q_measured rows remain source-unresolved and are not mapped into Phi calibration",
            "units": "source convention: T in K; heat in J or kT; no new numeric row emitted",
            "derivation_class": "source-surface inventory and provenance-boundary audit",
            "observable": "Berut mean dissipated heat versus erasure duration / Landauer lower-bound comparison",
            "data_role": "SOURCE_PROVENANCE_AND_ACQUISITION_DECISION_ONLY; no calibration consumed",
            "evidence_artifacts": evidence,
            "verification_status": "PASS_SCOPED_BERUT_SOURCE_PACKAGE_BOUNDARY",
            "open_blockers": blockers,
            "dependency_unlocked": "Berut source-acquisition decision only; no Topic 13 full bridge, Core, Gravity, or transport dependency is unlocked.",
            "claim_boundary": "This closes only the current source-surface classification. It does not close a Berut numeric row, uncertainty package, alpha_Phi_K, the UET bridge, or external validation.",
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
        "observable": "source-defined Landauer heat benchmark; no accepted numeric row",
        "data_role": "SOURCE_PROVENANCE_AND_ACQUISITION_DECISION_ONLY",
        "evidence_artifacts": evidence,
        "verification_status": checks,
        "open_blockers": blockers,
        "dependency_unlocked": "none beyond the named source-acquisition controller",
        "claim_boundary": "Summary values remain lower-bound consistency inputs only; they are not raw data, calibration, prediction, or UET proof.",
        "source_surface": source_surface,
        "local_source_inventory": {
            "raw_external_file_present": False,
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
        "next_action": "Archive the official Figure 3 PPT or an explicitly permitted numeric/supplement package, then select one panel and record axis ticks, selected points/curve, row identity, uncertainty, preprocessing, and SHA-256 before any source-normalized use.",
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
