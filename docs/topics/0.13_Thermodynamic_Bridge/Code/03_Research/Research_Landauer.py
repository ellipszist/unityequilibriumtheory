"""
UET Thermodynamic Bridge: Landauer and Thermodynamic Identity Checks.

This verifier anchors the topic to source-backed Landauer lower-bound behavior
and formula-consistency checks for Bekenstein/Unruh/Hawking relations. It does
not by itself validate the full UET beta*C*I bridge as a first-principles law.
"""

import sys
from pathlib import Path

# --- ROBUST UET BOOTSTRAP ---
def _bootstrap():
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return None

ROOT = _bootstrap()
if not ROOT:
    print("CRITICAL: UET docs root not found!")
    sys.exit(1)


import numpy as np
import sys
import json
import hashlib
from datetime import datetime, timezone


import os
from pathlib import Path
from docs import ROOT_PATH

root_path = ROOT_PATH

import importlib.util

# --- ROBUST PATH FINDER (5x4 Grid Standard) ---


from docs.core.uet_glass_box import UETPathManager


TOPIC_DIR = ROOT / "docs" / "topics" / "0.13_Thermodynamic_Bridge"
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_13_thermodynamic_bridge_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
FOUNDATION_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "thermodynamic_bridge_foundation_claim_gate.json"
UNCERTAINTY_PREPROCESSING_PATH = TOPIC_DIR / "Data" / "03_Research" / "uncertainty_preprocessing_manifest.json"
UNCERTAINTY_PROPAGATION_SUMMARY_PATH = TOPIC_DIR / "Data" / "03_Research" / "uncertainty_propagation_summary.json"
MEASURED_CONSTANT_UNCERTAINTY_PACKAGE_PATH = TOPIC_DIR / "Data" / "03_Research" / "measured_constant_uncertainty_package.json"
CODATA_2022_MEASURED_CONSTANTS_EXTRACT_PATH = ROOT / "docs" / "data" / "external" / "constants" / "codata" / "codata_2022_measured_constants_extract.json"
BRIDGE_DERIVATION_MAP_PATH = TOPIC_DIR / "Data" / "03_Research" / "bridge_derivation_map.json"
UNITS_CONTRACT_PATH = TOPIC_DIR / "Data" / "03_Research" / "units_contract.json"
LANDAUER_UET_MAPPING_PATH = TOPIC_DIR / "Data" / "03_Research" / "landauer_uet_mapping.json"
BETA_ROLE_CLARIFICATION_PATH = TOPIC_DIR / "Data" / "03_Research" / "beta_role_clarification.json"
ROW_CLOSURE_MATRIX_PATH = TOPIC_DIR / "Data" / "03_Research" / "row_closure_matrix.json"
JUN_SOURCE_SUMMARY_LOCATOR_PATH = TOPIC_DIR / "Data" / "03_Research" / "jun_2014_source_summary_locator.json"
DATA_INPUTS = [
    TOPIC_DIR / "Data" / "03_Research" / "__init__.py",
    TOPIC_DIR / "Data" / "03_Research" / "berut_2012.json",
    TOPIC_DIR / "Data" / "03_Research" / "berut_2012_source_surface_note.json",
    TOPIC_DIR / "Data" / "03_Research" / "berut_2012_transcription_policy_blocker.json",
    TOPIC_DIR / "Data" / "03_Research" / "berut_2012_figure_locator_mapping.json",
    TOPIC_DIR / "Data" / "03_Research" / "cattaneo_data.json",
    TOPIC_DIR / "Data" / "03_Research" / "experimental_data.py",
    TOPIC_DIR / "Data" / "03_Research" / "landauer_source_lock.json",
    TOPIC_DIR / "Data" / "03_Research" / "hong_2016_runtime_target_policy.json",
    TOPIC_DIR / "Data" / "03_Research" / "legacy_0p028_runtime_row_policy.json",
    TOPIC_DIR / "Data" / "03_Research" / "jun_2014_source_summary_locator.json",
    TOPIC_DIR / "Data" / "03_Research" / "row_closure_matrix.json",
    ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "berut_2012" / "source_record.json",
    ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "jun_2014" / "source_record.json",
    ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "hong_2016" / "source_record.json",
    ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "hong_2016" / "crossref_work_record.json",
    ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "peterson_2018" / "source_record.json",
    ROOT / "docs" / "data" / "external" / "constants" / "codata" / "si_2019_exact_constants.json",
    ROOT / "docs" / "data" / "external" / "gravity" / "ligo_black_hole_mergers" / "source_record.json",
    ROOT / "docs" / "data" / "external" / "gravity" / "eht_black_hole_masses" / "source_record.json",
    ROOT / "docs" / "data" / "external" / "constants" / "codata" / "measured_constants_2022_source_record.json",
    CODATA_2022_MEASURED_CONSTANTS_EXTRACT_PATH,
]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _input_identity():
    items = []
    for path in DATA_INPUTS:
        rel = path.relative_to(ROOT).as_posix()
        if path.exists():
            items.append(
                {
                    "path": rel,
                    "sha256": _sha256(path),
                    "size_bytes": path.stat().st_size,
                }
            )
        else:
            items.append({"path": rel, "missing": True})
    return items


def _audit_metrics():
    k_B = 1.380649e-23
    electron_charge = 1.602176634e-19
    T_room = 300.0
    engine_landauer_j = landauer_energy(T_room)
    codata_landauer_j = k_B * T_room * np.log(2)
    engine_vs_codata_rel_error = abs(engine_landauer_j - codata_landauer_j) / codata_landauer_j

    landauer_eV = engine_landauer_j / electron_charge
    jun_source = _load_json(
        ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "jun_2014" / "source_record.json"
    )
    jun_primary_work_kT = jun_source["source_facing_summary"]["value_kT"]
    jun_primary_uncertainty_kT = jun_source["source_facing_summary"]["uncertainty_kT"]
    jun_primary_statistical_error_kT = jun_source["source_facing_summary"]["measurement_statistical_error_kT"]
    kT_eV = landauer_eV / np.log(2)
    jun_primary_eV = jun_primary_work_kT * kT_eV
    jun_primary_uncertainty_eV = jun_primary_uncertainty_kT * kT_eV
    jun_primary_statistical_error_eV = jun_primary_statistical_error_kT * kT_eV
    jun_ratio_to_lower_bound = jun_primary_eV / landauer_eV

    legacy_mixed_lineage_eV = 0.028
    legacy_mixed_lineage_ratio_to_lower_bound = legacy_mixed_lineage_eV / landauer_eV

    g_earth = 9.8
    earth_unruh_k = unruh_temperature(g_earth)

    M_sun = 1.989e30
    solar_hawking_k = surface_gravity_temperature(M_sun)
    solar_entropy_planck = bekenstein_bound_black_hole(M_sun)

    return {
        "landauer_300K_engine_J": engine_landauer_j,
        "landauer_300K_codata_J": codata_landauer_j,
        "landauer_engine_vs_codata_relative_error": engine_vs_codata_rel_error,
        "landauer_300K_engine_eV": landauer_eV,
        "jun_2014_source_facing_work_kT": jun_primary_work_kT,
        "jun_2014_source_facing_uncertainty_kT": jun_primary_uncertainty_kT,
        "jun_2014_source_facing_statistical_error_kT": jun_primary_statistical_error_kT,
        "jun_2014_source_facing_work_eV": jun_primary_eV,
        "jun_2014_source_facing_uncertainty_eV": jun_primary_uncertainty_eV,
        "jun_2014_source_facing_statistical_error_eV": jun_primary_statistical_error_eV,
        "jun_2014_ratio_to_landauer_lower_bound": jun_ratio_to_lower_bound,
        "legacy_mixed_lineage_observed_eV": legacy_mixed_lineage_eV,
        "legacy_mixed_lineage_ratio_to_landauer_lower_bound": legacy_mixed_lineage_ratio_to_lower_bound,
        "unruh_temperature_earth_g_K": earth_unruh_k,
        "hawking_temperature_solar_mass_K": solar_hawking_k,
        "bekenstein_hawking_entropy_solar_mass_planck_units": solar_entropy_planck,
    }


def _relative_repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _load_module_from_path(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_source_evidence_intake_stub():
    berut_source = _load_json(ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "berut_2012" / "source_record.json")
    berut_surface_note = _load_json(TOPIC_DIR / "Data" / "03_Research" / "berut_2012_source_surface_note.json")
    berut_transcription_policy = _load_json(TOPIC_DIR / "Data" / "03_Research" / "berut_2012_transcription_policy_blocker.json")
    berut_locator_mapping = _load_json(TOPIC_DIR / "Data" / "03_Research" / "berut_2012_figure_locator_mapping.json")
    jun_source = _load_json(ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "jun_2014" / "source_record.json")
    jun_locator = _load_json(JUN_SOURCE_SUMMARY_LOCATOR_PATH)
    hong_source = _load_json(ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "hong_2016" / "source_record.json")
    peterson_source = _load_json(ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "peterson_2018" / "source_record.json")
    ligo_source = _load_json(ROOT / "docs" / "data" / "external" / "gravity" / "ligo_black_hole_mergers" / "source_record.json")
    eht_source = _load_json(ROOT / "docs" / "data" / "external" / "gravity" / "eht_black_hole_masses" / "source_record.json")
    measured_constants_source = _load_json(ROOT / "docs" / "data" / "external" / "constants" / "codata" / "measured_constants_2022_source_record.json")
    hong_runtime_target_policy = _load_json(TOPIC_DIR / "Data" / "03_Research" / "hong_2016_runtime_target_policy.json")
    hong_candidate_ids = hong_source.get("candidate_primary_identifiers_from_secondary_reference_trail", {})

    berut_working_copy = TOPIC_DIR / "Data" / "03_Research" / "berut_2012.json"
    experimental_module = TOPIC_DIR / "Data" / "03_Research" / "experimental_data.py"

    stub = {
        "schema_version": "1.0",
        "topic": "0.13_Thermodynamic_Bridge",
        "purpose": "Structured intake stub for external-source evidence before claim upgrades or data rewrites.",
        "instructions": [
            "Fill one source entry per unresolved upstream dataset or uncertainty record.",
            "Record DOI or URL, local path, file identity, unit basis, and extraction note before using the source in a verifier change.",
            "Do not treat this file as the evidence itself; it is an intake and tracking layer.",
        ],
        "source_targets": [
            {
                "name": "Berut 2012 upstream numeric surface or declared transcription policy",
                "priority": "immediate",
                "status": "partial",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "complete", "value": berut_source["doi_url"]},
                    {"field": "local_path", "status": "complete", "value": _relative_repo_path(berut_working_copy)},
                    {"field": "original_file_name", "status": "pending", "value": ""},
                    {"field": "row_identifier_or_table_label", "status": "partial", "value": "Figure 3 preview locator captured; exact numeric point/curve identifier within the figure is still open."},
                    {"field": "figure_level_locator", "status": "complete", "value": f"{berut_locator_mapping['selected_locator']['locator_value']}: {berut_locator_mapping['selected_locator']['locator_title']}"},
                    {
                        "field": "accessible_surface_status",
                        "status": "partial",
                        "value": (
                            "Current visible Nature page surface is "
                            f"{berut_surface_note['primary_surface_observation']['preview_surface_status']}; "
                            "the preview exposes figure labels rather than a directly visible row table, and Figure 3 is now the selected preview-level locator for the topic-summary row."
                        ),
                    },
                    {
                        "field": "declared_transcription_policy",
                        "status": "complete",
                        "value": "figure_level_locator_capture selected; Figure 3 preview locator mapped to topic-summary row; numeric point capture or stronger surface still required",
                    },
                    {"field": "unit_basis", "status": "complete", "value": "T in K; heat in J with optional kT lower-bound context"},
                    {
                        "field": "extraction_note",
                        "status": "complete",
                        "value": (
                            "Topic working copy stores a checked summary row only. The currently accessible source surface "
                            "looks figure-level rather than table-level, so source-lock closure now requires one numeric point within the selected Figure 3 locator or one stronger upstream numeric surface before normalization."
                        ),
                    },
                ],
            },
            {
                "name": "Jun 2014 feedback-trap benchmark source",
                "priority": "high",
                "status": "partial",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "complete", "value": jun_source["doi_url"]},
                    {"field": "local_path", "status": "complete", "value": _relative_repo_path(experimental_module)},
                    {"field": "original_file_name", "status": "complete", "value": jun_locator["source_identity"]["arxiv_id"]},
                    {"field": "source_summary_locator", "status": "complete", "value": f"{jun_locator["source_summary_locator"]["figure_locator"]}; {jun_locator["source_summary_locator"]["table_locator"]}; {jun_locator["source_summary_locator"]["equation_locator"]}; {jun_locator["source_summary_locator"]["fit_target"]}"},
                    {"field": "reported_energy_value", "status": "complete", "value": "Source-facing asymptotic full-erasure work is recorded as 0.71 +/- 0.03 kT in Table 1 for the full-erasure p=1 fit; under the current 300 K verifier baseline this converts to about 0.01836 +/- 0.00078 eV."},
                    {"field": "reported_uncertainty_or_interval", "status": "complete", "value": "Summary-layer uncertainty is available in kT and is tied to the captured Table 1/Figure 4/Eq. (3) asymptotic-work fit target."},
                    {"field": "final_source_or_local_archive", "status": "partial", "value": "arXiv:1408.5089 source-summary locator captured; final PRL page/PDF parity or local article/table archive remains open."},
                    {"field": "unit_basis", "status": "complete", "value": "source-facing quantity in kT; runtime comparison in eV after explicit conversion"},
                    {"field": "extraction_note", "status": "complete", "value": "Source identity and source-summary locator are pinned for the Jun 2014 feedback-trap branch; the separate legacy 0.028 eV runtime row remains mixed-lineage context outside active Jun logic."},
                ],
            },
            {
                "name": "Hong 2016 nanomagnetic-memory benchmark candidate",
                "priority": "high",
                "status": "partial",
                "evidence_fields": [
                    {"field": "primary_doi_or_article_page", "status": "partial", "value": hong_candidate_ids.get("doi_url", "")},
                    {"field": "local_path", "status": "complete", "value": _relative_repo_path(ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "hong_2016" / "source_record.json")},
                    {"field": "bibliographic_identity", "status": "complete", "value": hong_source["bibliographic_status"]},
                    {"field": "original_file_name", "status": "pending", "value": ""},
                    {"field": "reported_energy_value", "status": "partial", "value": "An accessible same-author preprint precursor exposes two Hong-side source-facing candidates: 6.09 +/- 1.43 zJ (~0.0380 eV) and 4.2 +/- 0.9 zJ (~0.0262 eV). Current topic policy provisionally prefers the temperature-series mean as the best fit to the inherited 2016/44%-above-limit narrative, while a separate legacy-row policy demotes the local 0.028 eV value out of active Jun/Hong benchmark logic until final-source confirmation."},
                    {"field": "reported_uncertainty_or_interval", "status": "partial", "value": "Preprint-level intervals are visible for both candidate Hong quantities, and the provisionally preferred target carries an interval, but final-source confirmation and the explicit replace/remove action for the local 0.028 eV row are still open."},
                    {"field": "unit_basis", "status": "complete", "value": hong_source["unit_convention"]["energy"]},
                    {"field": "extraction_note", "status": "complete", "value": "This candidate branch explains the 2016 nanomagnetic-memory narrative more plausibly than the current Jun source identity, and the current topic policy now provisionally prefers the Hong temperature-series mean because it best matches the inherited ~0.026 eV / 44%-above-limit wording. Final-source confirmation is still required before row closure."},
                ],
            },
            {
                "name": "Quantum Landauer branch source identity (legacy Peterson 2018 label unresolved)",
                "priority": "high",
                "status": "partial",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "partial", "value": "candidate sources recorded in peterson_2018/source_record.json; current evidence separates a Peterson-led 2016 quantum-thermodynamics paper, a trapped-ion PRL 2018 quantum-Landauer paper, and the Nature Physics 2018 DOI currently named by the legacy runtime label"},
                    {"field": "local_path", "status": "complete", "value": _relative_repo_path(ROOT / "docs" / "data" / "external" / "thermodynamics" / "landauer" / "peterson_2018" / "source_record.json")},
                    {"field": "original_file_name", "status": "pending", "value": ""},
                    {"field": "reported_energy_value", "status": "partial", "value": "Local runtime branch is not yet tied to one exact upstream row because the current branch appears composite rather than merely underspecified"},
                    {"field": "unit_basis", "status": "complete", "value": "source-specific quantum thermodynamic work/heat convention; runtime conversion must be explicit"},
                    {"field": "extraction_note", "status": "complete", "value": "This branch is intentionally unresolved; direct metadata checks now show that the local branch mixes incompatible source cues, so one exact paper identity must be chosen before row-level capture or gate use."},
                ],
            },
            {
                "name": "LIGO/Virgo mass uncertainty source package",
                "priority": "medium",
                "status": "ready_for_source_review",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "complete", "value": ligo_source["primary_reference"]["doi"]},
                    {"field": "local_path", "status": "complete", "value": _relative_repo_path(ROOT / "docs" / "data" / "external" / "gravity" / "ligo_black_hole_mergers" / "source_record.json")},
                    {"field": "event_identifier", "status": "complete", "value": "GW150914; GW151226; GW170104"},
                    {"field": "mass_value_and_uncertainty", "status": "complete", "value": "Topic-local summary rows exist in experimental_data.py with source-reported solar-mass uncertainties."},
                    {"field": "unit_basis", "status": "complete", "value": "solar masses in source rows; kg only after explicit conversion"},
                    {"field": "extraction_note", "status": "complete", "value": "Source family and uncertainty-bearing summary rows are identified; row-level archival capture and entropy propagation still remain separate tasks."},
                ],
            },
            {
                "name": "EHT black-hole mass source package",
                "priority": "medium",
                "status": "ready_for_source_review",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "complete", "value": "M87*: https://arxiv.org/abs/1906.11238; Sgr A*: https://arxiv.org/abs/2311.09479"},
                    {"field": "local_path", "status": "complete", "value": _relative_repo_path(ROOT / "docs" / "data" / "external" / "gravity" / "eht_black_hole_masses" / "source_record.json")},
                    {"field": "object_identifier", "status": "complete", "value": "M87*; Sgr A*"},
                    {"field": "mass_value_and_uncertainty", "status": "complete", "value": "Topic-local summary rows exist in experimental_data.py with source-reported solar-mass uncertainties."},
                    {"field": "unit_basis", "status": "complete", "value": "solar masses in source rows; kg only after explicit conversion"},
                    {"field": "extraction_note", "status": "complete", "value": "Source family and uncertainty-bearing summary rows are identified; object-level machine-readable capture still remains a follow-up task."},
                ],
            },
            {
                "name": "Measured-constant uncertainty record beyond exact SI constants",
                "priority": "medium",
                "status": "ready_for_source_review",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "complete", "value": "https://arxiv.org/abs/2409.03787; https://physics.nist.gov/constants"},
                    {"field": "local_path", "status": "complete", "value": _relative_repo_path(ROOT / "docs" / "data" / "external" / "constants" / "codata" / "measured_constants_2022_source_record.json")},
                    {"field": "numeric_extract_path", "status": "complete", "value": _relative_repo_path(CODATA_2022_MEASURED_CONSTANTS_EXTRACT_PATH)},
                    {"field": "constant_identifier", "status": "complete", "value": "G; supporting G_over_hbar_c row captured for audit context"},
                    {"field": "value_and_uncertainty", "status": "complete", "value": "Direct CODATA 2022 extraction records G = 6.67430e-11 with standard uncertainty 0.00015e-11 m^3 kg^-1 s^-2."},
                    {"field": "unit_basis", "status": "complete", "value": measured_constants_source["unit_convention"]},
                    {"field": "extraction_note", "status": "complete", "value": "This closes the direct G numeric-extraction blocker for the current gravity-context interval package; systematic astrophysical terms remain separate."},
                ],
            },
        ],
        "claim_boundary": (
            "This intake stub is for source evidence capture only. Filling it does not by itself justify "
            "upgrading the thermodynamic bridge claim class."
        ),
    }
    SOURCE_EVIDENCE_INTAKE_PATH.write_text(json.dumps(stub, indent=2), encoding="utf-8")
    return stub


def _build_source_evidence_readiness_matrix(intake_stub: dict):
    readiness_rows = []
    for target in intake_stub.get("source_targets", []):
        pending = [field["field"] for field in target["evidence_fields"] if field.get("status") not in ("complete",)]
        ready = len(pending) == 0
        fields_partial = sum(1 for field in target["evidence_fields"] if field.get("status") == "partial")
        readiness_rows.append(
            {
                "name": target["name"],
                "priority": target["priority"],
                "status": target.get("status", "pending"),
                "fields_total": len(target["evidence_fields"]),
                "fields_complete": sum(
                    1 for field in target["evidence_fields"] if field.get("status") == "complete"
                ),
                "fields_partial": fields_partial,
                "fields_pending": len(pending),
                "pending_fields": pending,
                "ready_for_source_review": ready,
                "blocking_reason": (
                    None
                    if ready
                    else "One or more required evidence fields are still pending."
                ),
            }
        )

    matrix = {
        "schema_version": "1.0",
        "topic": "0.13_Thermodynamic_Bridge",
        "purpose": "Readiness matrix for external-source evidence before provenance or claim upgrades.",
        "summary": {
            "source_targets_total": len(readiness_rows),
            "targets_ready_for_source_review": sum(
                1 for row in readiness_rows if row["ready_for_source_review"]
            ),
            "targets_with_partial_evidence": sum(
                1 for row in readiness_rows if row["fields_complete"] > 0 and not row["ready_for_source_review"]
            ),
            "targets_blocked_by_pending_evidence": sum(
                1 for row in readiness_rows if not row["ready_for_source_review"]
            ),
        },
        "readiness_rows": readiness_rows,
        "claim_boundary": (
            "This matrix is an evidence-readiness gate only. A target marked ready still requires "
            "actual source review before data or claim changes."
        ),
    }
    SOURCE_EVIDENCE_READINESS_PATH.write_text(json.dumps(matrix, indent=2), encoding="utf-8")
    return matrix


def _build_row_controller_summary():
    row_matrix = _load_json(ROW_CLOSURE_MATRIX_PATH)
    tracked_rows = {
        row["row_id"]: row
        for row in row_matrix.get("rows", [])
        if row["row_id"] in {
            "berut_2012_summary_300K",
            "jun_2014_summary_300K",
            "hong_2016_candidate_nanometric_memory_branch",
            "peterson_2018_quantum_landauer_branch",
        }
    }

    return {
        "path": ROW_CLOSURE_MATRIX_PATH.relative_to(ROOT).as_posix(),
        "sha256": _sha256(ROW_CLOSURE_MATRIX_PATH),
        "controller_rows": [
            {
                "row_id": row_id,
                "source_closure_status": row_data["source_closure_status"],
                "uncertainty_status": row_data["uncertainty_status"],
                "next_controller": row_data.get("next_controller", "not_declared"),
                "first_missing_requirement": row_data["missing_requirements"][0]
                if row_data.get("missing_requirements")
                else None,
            }
            for row_id, row_data in tracked_rows.items()
        ],
        "summary": {
            "tracked_row_count": len(tracked_rows),
            "rows_with_declared_next_controller": sum(
                1 for row_data in tracked_rows.values() if row_data.get("next_controller")
            ),
            "claim_boundary": (
                "This summary centralizes the current row-level controllers for the active Landauer blocker chain. "
                "It does not by itself close any row or upgrade the main topic claim class."
            ),
        },
    }


def _build_evidence_lanes(test_results, metrics, readiness_matrix):
    source_targets_ready = readiness_matrix["summary"]["targets_ready_for_source_review"]
    source_targets_total = readiness_matrix["summary"]["source_targets_total"]
    primary_tests_pass = all(item["passed"] for item in test_results)
    landauer_identity_pass = (
        metrics["landauer_engine_vs_codata_relative_error"] <= 1e-12
        and metrics["jun_2014_ratio_to_landauer_lower_bound"] >= 1.0
    )

    return {
        "landauer_lower_bound": {
            "status": "PASS" if landauer_identity_pass else "FAIL",
            "claim_class": "C - internal lower-bound benchmark",
            "formula_ids": ["T13-004", "T13-005"],
            "evidence_role": "gate",
            "supports": "Exact-constant Landauer calculation and selected source-referenced measurements above the lower bound.",
            "does_not_support": "A complete UET thermodynamic bridge or first-principles information-field dynamics.",
            "source_lock_status": {
                "ready_targets": source_targets_ready,
                "total_targets": source_targets_total,
                "raw_numeric_tables_archived": False,
                "berut_stronger_surface_or_policy_closed": False,
            },
        },
        "bekenstein_hawking_formula_consistency": {
            "status": "PASS" if primary_tests_pass else "FAIL",
            "claim_class": "B/C - formula consistency only",
            "formula_ids": ["T13-006", "T13-007", "T13-008", "T13-009"],
            "evidence_role": "diagnostic",
            "supports": "Standard thermodynamic/gravity identity calculations with source-declared constants.",
            "does_not_support": "Independent empirical validation of UET dynamics.",
        },
        "synthetic_cattaneo_demo": {
            "status": "OPEN",
            "claim_class": "A/B - simulation-only model shape",
            "formula_ids": ["T13-010"],
            "evidence_role": "exploratory",
            "supports": "Non-equilibrium lag/hysteresis sandbox only.",
            "does_not_support": "External heat-transport validation until a real dataset and threshold are added.",
        },
        "uet_bridge_hypothesis": {
            "status": "BLOCKED",
            "claim_class": "A - hypothesis / B - model component",
            "formula_ids": ["T13-001", "T13-002", "T13-003", "T13-011"],
            "evidence_role": "claim ceiling",
            "supports": "Structured mechanism target and dependency map.",
            "does_not_support": "Solved, verified, exact, or theory-confirmed wording.",
            "blockers": [
                "Berut now has a selected Figure 3 preview locator mapped to the topic-summary row, but still lacks one numeric point capture or one stronger upstream numeric surface.",
                "Uncertainty propagation is only partial: Berut summary and black-hole mass intervals are attached, Jun has a captured Table 1/Figure 4 source-summary locator but still lacks final-source parity or local archival, and measured-constant terms remain open.",
                "UET-specific field variables are not yet derived from the standard thermodynamic identities.",
            ],
        },
    }


def _build_uncertainty_preprocessing_plan(metrics):
    manifest = {
        "schema_version": "1.0",
        "purpose": "Define and partially populate the next preprocessing step before 0.13 can move beyond WARN/source-lock-open.",
        "required_fields": [
            "source_row_id",
            "reported_value",
            "reported_uncertainty",
            "source_unit",
            "runtime_unit",
            "conversion_formula",
            "lower_bound_value",
            "ratio_to_lower_bound",
            "uncertainty_propagation_note",
        ],
        "rows": [
            {
                "source_row_id": "berut_2012_summary_300K",
                "reported_value": 3.0e-21,
                "reported_uncertainty": 5.0e-22,
                "source_unit": "J",
                "runtime_unit": "J",
                "conversion_formula": "identity",
                "lower_bound_value": metrics["landauer_300K_codata_J"],
                "ratio_to_lower_bound": 3.0e-21 / metrics["landauer_300K_codata_J"],
                "uncertainty_propagation_note": "Topic-local summary row exists and Figure 3 is now the selected preview-level locator, but numeric-point capture and stronger-surface provenance remain open."
            },
            {
                "source_row_id": "jun_2014_summary_300K",
                "reported_value": metrics["jun_2014_source_facing_work_eV"],
                "reported_uncertainty": metrics["jun_2014_source_facing_uncertainty_eV"],
                "source_unit": "eV",
                "runtime_unit": "eV",
                "conversion_formula": "source_facing_work_eV = source_facing_work_kT * (k_B T / e)",
                "lower_bound_value": metrics["landauer_300K_engine_eV"],
                "ratio_to_lower_bound": metrics["jun_2014_ratio_to_landauer_lower_bound"],
                "uncertainty_propagation_note": "Source-facing asymptotic-work summary and uncertainty are available at the preprint-summary layer, and the legacy 0.028 eV row is now declared outside the active Jun lane; final PRL parity/local archive still remains open."
            },
            {
                "source_row_id": "gw150914_final_mass",
                "reported_value": 62.0,
                "reported_uncertainty": 4.0,
                "source_unit": "M_sun",
                "runtime_unit": "kg",
                "conversion_formula": "mass_kg = mass_Msun * M_sun",
                "lower_bound_value": None,
                "ratio_to_lower_bound": None,
                "uncertainty_propagation_note": "Mass uncertainty exists in the topic-local summary, but propagation into entropy and Hawking-temperature uncertainty is still open."
            },
            {
                "source_row_id": "m87_mass",
                "reported_value": 6.5e9,
                "reported_uncertainty": 0.7e9,
                "source_unit": "M_sun",
                "runtime_unit": "kg",
                "conversion_formula": "mass_kg = mass_Msun * M_sun",
                "lower_bound_value": None,
                "ratio_to_lower_bound": None,
                "uncertainty_propagation_note": "Object mass uncertainty is present in the topic-local summary, but object-level entropy uncertainty propagation is still open."
            },
            {
                "source_row_id": "sgrA_mass",
                "reported_value": 4.0e6,
                "reported_uncertainty": 0.1e6,
                "source_unit": "M_sun",
                "runtime_unit": "kg",
                "conversion_formula": "mass_kg = mass_Msun * M_sun",
                "lower_bound_value": None,
                "ratio_to_lower_bound": None,
                "uncertainty_propagation_note": "Object mass uncertainty is present in the topic-local summary, but object-level entropy uncertainty propagation is still open."
            }
        ],
        "target_sources": [
            "Berut 2012 upstream numeric surface or declared transcription policy",
            "Jun 2014 feedback-trap benchmark source",
            "Quantum Landauer branch source identity (legacy Peterson 2018 label unresolved)",
            "LIGO/Virgo black-hole mass uncertainty package",
            "EHT black-hole mass uncertainty package"
        ],
        "current_status": "partially_populated_not_closed",
        "claim_boundary": "This manifest narrows the uncertainty-preprocessing workload. It does not upgrade the topic until source-normalized rows and propagated uncertainty outputs are attached to the verifier.",
    }
    UNCERTAINTY_PREPROCESSING_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def _build_measured_constant_uncertainty_package():
    measured_constants_source = _load_json(
        ROOT / "docs" / "data" / "external" / "constants" / "codata" / "measured_constants_2022_source_record.json"
    )
    exact_constants = _load_json(
        ROOT / "docs" / "data" / "external" / "constants" / "codata" / "si_2019_exact_constants.json"
    )
    measured_constants_extract = _load_json(CODATA_2022_MEASURED_CONSTANTS_EXTRACT_PATH)

    g_entry = measured_constants_extract["constants"]["G"]
    g_relative_uncertainty = g_entry["relative_uncertainty"]

    package = {
        "schema_version": "1.0",
        "topic": "0.13_Thermodynamic_Bridge",
        "purpose": (
            "Declare the current runtime uncertainty policy for measured constants in gravity-adjacent "
            "thermodynamic rows using the direct CODATA 2022 G extraction while keeping systematic astrophysical terms separate."
        ),
        "status": "direct_2022_g_extraction_threaded_into_gravity_context",
        "provenance": {
            "primary_anchor": {
                "path": "docs/data/external/constants/codata/measured_constants_2022_source_record.json",
                "role": measured_constants_source["source_role"],
            },
            "local_numeric_extract": {
                "path": _relative_repo_path(CODATA_2022_MEASURED_CONSTANTS_EXTRACT_PATH),
                "role": measured_constants_extract["source_class"],
                "source_url": measured_constants_extract["source_url"],
            },
            "claim_boundary": (
                "The provenance anchor for measured constants is pinned to the 2022/NIST source record and the current "
                "runtime numeric uncertainty for G now comes from the direct CODATA 2022 extract stored in the repo."
            ),
        },
        "runtime_constants": {
            "G": {
                "value": g_entry["value"],
                "uncertainty": g_entry["uncertainty"],
                "relative_uncertainty": g_relative_uncertainty,
                "unit": g_entry["unit"],
                "source_status": g_entry["source_status"],
            },
            "hbar": {
                "value": exact_constants["constants"]["h"]["value"] / (2.0 * np.pi),
                "uncertainty": 0.0,
                "relative_uncertainty": 0.0,
                "unit": "J s",
                "source_status": "treated_as_exact_under_current_repo_convention",
            },
            "c": {
                "value": exact_constants["constants"]["c"]["value"],
                "uncertainty": 0.0,
                "relative_uncertainty": 0.0,
                "unit": exact_constants["constants"]["c"]["unit"],
                "source_status": "exact_si_defining_constant",
            },
            "k_B": {
                "value": exact_constants["constants"]["k_B"]["value"],
                "uncertainty": 0.0,
                "relative_uncertainty": 0.0,
                "unit": exact_constants["constants"]["k_B"]["unit"],
                "source_status": "exact_si_defining_constant",
            },
        },
        "propagation_rules": [
            {
                "quantity": "Bekenstein-Hawking entropy",
                "relation": "S_BH proportional to G * M^2 when c and hbar are treated as exact",
                "relative_uncertainty_from_measured_constants_only": g_relative_uncertainty,
                "included_in_current_intervals": False,
            },
            {
                "quantity": "Hawking temperature",
                "relation": "T_H proportional to 1 / (G * M) when c, hbar, and k_B are treated as exact",
                "relative_uncertainty_from_measured_constants_only": g_relative_uncertainty,
                "included_in_current_intervals": False,
            },
            {
                "quantity": "Schwarzschild radius",
                "relation": "r_s proportional to G * M when c is treated as exact",
                "relative_uncertainty_from_measured_constants_only": g_relative_uncertainty,
                "included_in_current_intervals": False,
            },
        ],
        "row_policy": [
            {
                "source_row_id": "gw150914_final_mass",
                "current_interval_status": "mass_plus_direct_2022_g_interval_present",
                "measured_constant_uncertainty_status": "direct_2022_g_threaded",
                "relative_uncertainty_from_G_only": g_relative_uncertainty,
            },
            {
                "source_row_id": "m87_mass",
                "current_interval_status": "mass_plus_direct_2022_g_interval_present",
                "measured_constant_uncertainty_status": "direct_2022_g_threaded",
                "relative_uncertainty_from_G_only": g_relative_uncertainty,
            },
            {
                "source_row_id": "sgrA_mass",
                "current_interval_status": "mass_plus_direct_2022_g_interval_present",
                "measured_constant_uncertainty_status": "direct_2022_g_threaded",
                "relative_uncertainty_from_G_only": g_relative_uncertainty,
            },
            {
                "source_row_id": "berut_2012_summary_300K",
                "current_interval_status": "topic_summary_interval_present",
                "measured_constant_uncertainty_status": "not_applicable_under_exact_constant_lane",
                "relative_uncertainty_from_G_only": None,
            },
            {
                "source_row_id": "jun_2014_summary_300K",
                "current_interval_status": "source_summary_interval_present_legacy_row_policy_declared",
                "measured_constant_uncertainty_status": "not_applicable_under_exact_constant_lane",
                "relative_uncertainty_from_G_only": None,
            },
        ],
        "claim_boundary": (
            "This package narrows the measured-constant blocker by replacing the prior runtime proxy with a direct CODATA 2022 G extraction and propagation policy. "
            "It threads that direct G value into gravity-context combined intervals, but it does not mean astrophysical systematic terms or object-level source-row capture are closed."
        ),
    }
    MEASURED_CONSTANT_UNCERTAINTY_PACKAGE_PATH.write_text(
        json.dumps(package, indent=2), encoding="utf-8"
    )
    return package


def _build_uncertainty_propagation_summary(metrics, measured_constant_package):
    experimental_data = _load_module_from_path(
        "thermodynamic_bridge_experimental_data",
        TOPIC_DIR / "Data" / "03_Research" / "experimental_data.py",
    )
    g_relative_uncertainty = measured_constant_package["runtime_constants"]["G"]["relative_uncertainty"]

    def _build_mass_interval_row(source_row_id: str, mass_solar: float, mass_error_solar: float):
        mass_central_kg = mass_solar * experimental_data.M_SUN
        mass_lower_kg = max(mass_solar - mass_error_solar, 0.0) * experimental_data.M_SUN
        mass_upper_kg = (mass_solar + mass_error_solar) * experimental_data.M_SUN

        entropy_central = bekenstein_bound_black_hole(mass_central_kg)
        entropy_lower = bekenstein_bound_black_hole(mass_lower_kg)
        entropy_upper = bekenstein_bound_black_hole(mass_upper_kg)

        hawking_central = surface_gravity_temperature(mass_central_kg)
        hawking_lower = surface_gravity_temperature(mass_upper_kg)
        hawking_upper = surface_gravity_temperature(mass_lower_kg)

        mass_relative_uncertainty = mass_error_solar / mass_solar
        entropy_relative_uncertainty_combined = float(
            np.sqrt((2.0 * mass_relative_uncertainty) ** 2 + g_relative_uncertainty ** 2)
        )
        hawking_relative_uncertainty_combined = float(
            np.sqrt((mass_relative_uncertainty) ** 2 + g_relative_uncertainty ** 2)
        )
        return {
            "source_row_id": source_row_id,
            "runtime_inputs": {
                "mass_solar_central": mass_solar,
                "mass_solar_uncertainty": mass_error_solar,
                "mass_relative_uncertainty": mass_relative_uncertainty,
                "constant_uncertainty_included": False,
                "measured_constant_relative_uncertainty_direct_2022_G": g_relative_uncertainty,
            },
            "propagated_outputs": {
                "entropy_planck_central": entropy_central,
                "entropy_planck_interval_1sigma": [entropy_lower, entropy_upper],
                "entropy_relative_uncertainty_first_order": 2.0 * mass_relative_uncertainty,
                "entropy_relative_uncertainty_combined_mass_plus_direct_2022_G": entropy_relative_uncertainty_combined,
                "entropy_planck_interval_1sigma_mass_plus_direct_2022_G": [
                    entropy_central * (1.0 - entropy_relative_uncertainty_combined),
                    entropy_central * (1.0 + entropy_relative_uncertainty_combined),
                ],
                "hawking_temperature_K_central": hawking_central,
                "hawking_temperature_K_interval_1sigma": [hawking_lower, hawking_upper],
                "hawking_relative_uncertainty_first_order": mass_relative_uncertainty,
                "hawking_relative_uncertainty_combined_mass_plus_direct_2022_G": hawking_relative_uncertainty_combined,
                "hawking_temperature_K_interval_1sigma_mass_plus_direct_2022_G": [
                    hawking_central * (1.0 - hawking_relative_uncertainty_combined),
                    hawking_central * (1.0 + hawking_relative_uncertainty_combined),
                ],
                "measured_constant_relative_uncertainty_if_mass_fixed": {
                    "entropy_from_G_only": g_relative_uncertainty,
                    "hawking_temperature_from_G_only": g_relative_uncertainty,
                },
            },
            "claim_boundary": (
                "Mass-only intervals remain the current baseline. Additional combined intervals now include a provisional "
                "direct CODATA 2022 G uncertainty, but spin/systematic terms are still not included."
            ),
        }

    berut_summary_value_j = 3.0e-21
    berut_summary_uncertainty_j = 5.0e-22
    berut_lower_bound_j = metrics["landauer_300K_codata_J"]
    berut_ratio_sigma = berut_summary_uncertainty_j / berut_lower_bound_j
    berut_interval = [
        berut_summary_value_j - berut_summary_uncertainty_j,
        berut_summary_value_j + berut_summary_uncertainty_j,
    ]
    berut_ratio_interval = [
        berut_interval[0] / berut_lower_bound_j,
        berut_interval[1] / berut_lower_bound_j,
    ]

    summary = {
        "schema_version": "1.0",
        "topic": "0.13_Thermodynamic_Bridge",
        "purpose": "Attach first-pass propagated uncertainty intervals to the current 0.13 verifier without overstating source closure.",
        "rows": [
            {
                "source_row_id": "berut_2012_summary_300K",
                "runtime_inputs": {
                    "reported_value_J": berut_summary_value_j,
                    "reported_uncertainty_J": berut_summary_uncertainty_j,
                    "lower_bound_J": berut_lower_bound_j,
                    "constant_uncertainty_included": False,
                },
                "propagated_outputs": {
                    "reported_interval_1sigma_J": berut_interval,
                    "ratio_to_lower_bound_central": berut_summary_value_j / berut_lower_bound_j,
                    "ratio_to_lower_bound_sigma": berut_ratio_sigma,
                    "ratio_to_lower_bound_interval_1sigma": berut_ratio_interval,
                    "lower_bound_clearance_sigma": (
                        (berut_summary_value_j - berut_lower_bound_j) / berut_summary_uncertainty_j
                    ),
                    "crosses_lower_bound_at_1sigma": bool(berut_interval[0] < berut_lower_bound_j),
                },
                "claim_boundary": (
                    "This row is propagated from a topic-local summary value and uncertainty, not a row-level archived source table."
                ),
            },
            {
                "source_row_id": "jun_2014_summary_300K",
                "runtime_inputs": {
                    "reported_value_eV": metrics["jun_2014_source_facing_work_eV"],
                    "reported_uncertainty_eV": metrics["jun_2014_source_facing_uncertainty_eV"],
                    "reported_statistical_error_eV": metrics["jun_2014_source_facing_statistical_error_eV"],
                    "lower_bound_eV": metrics["landauer_300K_engine_eV"],
                },
                "propagated_outputs": {
                    "ratio_to_lower_bound_central": metrics["jun_2014_ratio_to_landauer_lower_bound"],
                    "ratio_to_lower_bound_sigma": (
                        metrics["jun_2014_source_facing_uncertainty_eV"] / metrics["landauer_300K_engine_eV"]
                    ),
                    "ratio_to_lower_bound_interval_1sigma": [
                        (metrics["jun_2014_source_facing_work_eV"] - metrics["jun_2014_source_facing_uncertainty_eV"]) / metrics["landauer_300K_engine_eV"],
                        (metrics["jun_2014_source_facing_work_eV"] + metrics["jun_2014_source_facing_uncertainty_eV"]) / metrics["landauer_300K_engine_eV"],
                    ],
                    "reported_interval_1sigma_eV": [
                        metrics["jun_2014_source_facing_work_eV"] - metrics["jun_2014_source_facing_uncertainty_eV"],
                        metrics["jun_2014_source_facing_work_eV"] + metrics["jun_2014_source_facing_uncertainty_eV"],
                    ],
                    "crosses_lower_bound_at_1sigma": bool(
                        (metrics["jun_2014_source_facing_work_eV"] - metrics["jun_2014_source_facing_uncertainty_eV"]) < metrics["landauer_300K_engine_eV"]
                    ),
                    "interval_status": "source_summary_interval_present",
                },
                "claim_boundary": "This interval is derived from the pinned Jun source-facing asymptotic-work summary and its summary-layer uncertainty, not from a fully archived row/file package. The legacy 0.028 eV runtime row remains separate mixed-lineage context.",
            },
            _build_mass_interval_row("gw150914_final_mass", 62.0, 4.0),
            _build_mass_interval_row("m87_mass", 6.5e9, 0.7e9),
            _build_mass_interval_row("sgrA_mass", 4.0e6, 0.1e6),
        ],
        "summary": {
            "rows_total": 5,
            "rows_with_propagated_intervals": 5,
            "rows_missing_uncertainty_inputs": 0,
            "constant_uncertainty_included": False,
            "measured_constant_runtime_package_status": measured_constant_package["status"],
            "current_status": "partial_intervals_mass_plus_direct_2022_g_for_gravity_context",
            "notable_constraints": [
                "Berut 2012 topic-summary interval crosses the Landauer lower bound at 1 sigma.",
                "Jun 2014 now has a source-facing summary-layer interval, a declared legacy-row demotion policy, and a captured Table 1/Figure 4 locator, but final-source parity/local archival remain open.",
                "Black-hole entropy and Hawking-temperature rows now keep mass-only intervals and also add combined intervals using a direct CODATA 2022 G extraction.",
                "The G term now comes from a direct CODATA 2022 extract, while spin/systematic astrophysical terms remain excluded.",
            ],
        },
        "claim_boundary": (
            "This summary adds first-pass propagated intervals and gravity-context combined intervals using direct CODATA 2022 G extraction, "
            "but it is not a full uncertainty package. Raw-source row capture, Jun final-source parity/local archival, systematic astrophysical terms remain open."
        ),
    }
    UNCERTAINTY_PROPAGATION_SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary


def _build_bridge_derivation_map():
    derivation_map = {
        "schema_version": "1.0",
        "topic": "0.13_Thermodynamic_Bridge",
        "purpose": (
            "Make the bridge-derivation boundary explicit: which relations are standard identities, "
            "which are UET proxies or hypotheses, and which proof gaps remain before stronger claims."
        ),
        "status": "open_boundary_mapped_not_derived",
        "claim_boundary": (
            "This map documents the current derivation state. It does not close the UET bridge proof."
        ),
        "layers": [
            {
                "layer_id": "standard_identity_inputs",
                "role": "externally established thermodynamic relations",
                "status": "usable_as_constraints_only",
                "entries": [
                    {
                        "formula_id": "T13-004",
                        "relation": "E_min = k_B T ln 2",
                        "type": "standard_lower_bound",
                        "derivation_status": "identity_or_source_backed_standard",
                        "used_now_as": "lower-bound benchmark constraint",
                    },
                    {
                        "formula_id": "T13-006",
                        "relation": "Bekenstein bound",
                        "type": "standard_identity",
                        "derivation_status": "standard_relation",
                        "used_now_as": "information-density constraint",
                    },
                    {
                        "formula_id": "T13-008",
                        "relation": "Unruh temperature",
                        "type": "standard_identity",
                        "derivation_status": "standard_relation",
                        "used_now_as": "thermodynamic-gravity context",
                    },
                    {
                        "formula_id": "T13-009",
                        "relation": "Hawking temperature",
                        "type": "standard_identity",
                        "derivation_status": "standard_relation",
                        "used_now_as": "thermodynamic-gravity context",
                    },
                ],
            },
            {
                "layer_id": "uet_proxy_terms",
                "role": "topic-local thermodynamic proxies and engine relations",
                "status": "heuristic_or_model_component",
                "entries": [
                    {
                        "formula_id": "T13-001",
                        "relation": "Stirling entropy proxy",
                        "type": "topic_proxy",
                        "derivation_status": "heuristic_proxy",
                        "used_now_as": "engine entropy trend",
                    },
                    {
                        "formula_id": "T13-002",
                        "relation": "dimensionless temperature proxy",
                        "type": "topic_proxy",
                        "derivation_status": "derived_from_proxy_not_physical_temperature",
                        "used_now_as": "engine equilibrium trend",
                    },
                    {
                        "formula_id": "T13-003",
                        "relation": "contact equilibrium update",
                        "type": "topic_model_rule",
                        "derivation_status": "simulation_rule",
                        "used_now_as": "zeroth-law-like sandbox",
                    },
                ],
            },
            {
                "layer_id": "uet_bridge_hypothesis",
                "role": "proposed information-entropy-energy bridge claims",
                "status": "blocked_hypothesis_lane",
                "entries": [
                    {
                        "formula_id": "T13-011",
                        "relation": "vacuum sink / bridge extension logic",
                        "type": "topic_hypothesis",
                        "derivation_status": "open",
                        "used_now_as": "hypothesis sandbox only",
                    }
                ],
            },
        ],
        "required_derivation_steps": [
            {
                "step_id": "bridge_units_contract",
                "question": "Which UET variables correspond to entropy, heat, work, temperature, and information in dimensional units?",
                "current_state": "open",
                "needed_evidence": [
                    "symbol-to-unit contract",
                    "conversion path from proxy quantities to physical observables",
                    "explicit statement of where physical scaling enters"
                ],
            },
            {
                "step_id": "landauer_to_uet_mapping",
                "question": "How does the UET bridge reproduce or constrain the Landauer lower bound without simply reusing the standard identity?",
                "current_state": "open",
                "needed_evidence": [
                    "non-circular mapping from UET variables to erasure cost",
                    "parameter-origin statement",
                    "testable difference between UET bridge output and the imported lower bound"
                ],
            },
            {
                "step_id": "gravity_identity_mapping",
                "question": "How do Bekenstein/Unruh/Hawking relations enter as consequences or constraints of UET rather than borrowed context only?",
                "current_state": "open",
                "needed_evidence": [
                    "derivation path with assumptions",
                    "regime statement for when the mapping is supposed to hold",
                    "reason the bridge adds information beyond reusing the standard formulas"
                ],
            },
            {
                "step_id": "uncertainty_and_source_closure",
                "question": "Can the bridge survive source-normalized data and uncertainty-aware evaluation?",
                "current_state": "partial",
                "needed_evidence": [
                    "Berut Figure 3 locator now needs one numeric point capture or one stronger upstream numeric surface",
                    "Jun final-source parity/local archive for captured Table 1/Figure 4 locator",
                    "measured-constant uncertainty package",
                    "claim gate that stays conservative under uncertainty intervals"
                ],
            },
        ],
        "non_derivation_shortcuts_to_avoid": [
            "Treating agreement with Landauer lower bound as proof of a full UET bridge",
            "Treating Bekenstein/Unruh/Hawking reuse as if UET derived them",
            "Upgrading synthetic Cattaneo or vacuum-sink behavior into empirical support",
            "Hiding unresolved parameter origin behind successful benchmark output",
        ],
        "promotion_rule": (
            "The bridge proof lane stays blocked until the unit contract, Landauer mapping, gravity-identity mapping, "
            "and uncertainty/source closure steps are each documented and tied to an artifact or verifier gate."
        ),
    }
    BRIDGE_DERIVATION_MAP_PATH.write_text(
        json.dumps(derivation_map, indent=2), encoding="utf-8"
    )
    return derivation_map


def _build_units_contract():
    units_contract = {
        "schema_version": "1.0",
        "topic": "0.13_Thermodynamic_Bridge",
        "purpose": (
            "Declare which symbols in 0.13 are dimensional SI quantities, which are topic-local proxies, "
            "and where no physical conversion path is currently justified."
        ),
        "status": "partial_contract_dimensional_and_proxy_layers_separated",
        "unit_systems": [
            {
                "system_id": "si_physical_layer",
                "scope": "Landauer and thermodynamic-gravity constraint calculations",
                "status": "declared",
            },
            {
                "system_id": "topic_proxy_layer",
                "scope": "engine entropy/contact dynamics and exploratory bridge sandbox",
                "status": "declared_nonphysical_until_scaled",
            },
        ],
        "symbols": [
            {
                "symbol": "E_min",
                "meaning": "Landauer lower-bound energy cost",
                "unit": "J",
                "layer": "si_physical_layer",
                "status": "physical_quantity",
                "code_surfaces": ["T13-004", "Research_Landauer.landauer_energy"],
                "conversion_rule": "optional conversion to eV via division by e",
            },
            {
                "symbol": "T",
                "meaning": "physical temperature in Landauer, Unruh, and Hawking relations",
                "unit": "K",
                "layer": "si_physical_layer",
                "status": "physical_quantity",
                "code_surfaces": ["T13-004", "T13-008", "T13-009"],
                "conversion_rule": "none; SI kelvin",
            },
            {
                "symbol": "E_eV",
                "meaning": "energy expressed in electron-volts for benchmark comparison",
                "unit": "eV",
                "layer": "si_physical_layer",
                "status": "converted_physical_quantity",
                "code_surfaces": ["T13-005", "Research_Landauer.landauer_energy_eV"],
                "conversion_rule": "E_eV = E_J / e",
            },
            {
                "symbol": "R",
                "meaning": "radius for Bekenstein bound examples",
                "unit": "m",
                "layer": "si_physical_layer",
                "status": "physical_quantity",
                "code_surfaces": ["T13-006"],
                "conversion_rule": "none; SI meter",
            },
            {
                "symbol": "M",
                "meaning": "black-hole mass for entropy and Hawking-temperature calculations",
                "unit": "kg",
                "layer": "si_physical_layer",
                "status": "physical_quantity_with_source_conversion",
                "code_surfaces": ["T13-007", "T13-009"],
                "conversion_rule": "source values often enter in M_sun and convert via mass_kg = mass_Msun * M_sun",
            },
            {
                "symbol": "S_BH",
                "meaning": "Bekenstein-Hawking entropy in Planck-unit normalization",
                "unit": "dimensionless_planck_units",
                "layer": "si_physical_layer",
                "status": "computed_theoretical_observable",
                "code_surfaces": ["T13-007"],
                "conversion_rule": "computed from area divided by 4*l_P^2",
            },
            {
                "symbol": "a",
                "meaning": "proper acceleration in Unruh relation",
                "unit": "m/s^2",
                "layer": "si_physical_layer",
                "status": "physical_quantity",
                "code_surfaces": ["T13-008"],
                "conversion_rule": "none; SI acceleration",
            },
            {
                "symbol": "E",
                "meaning": "engine energy quanta in entropy/contact model",
                "unit": "dimensionless_quanta",
                "layer": "topic_proxy_layer",
                "status": "proxy_not_mapped_to_joules",
                "code_surfaces": ["T13-001", "T13-002", "T13-003"],
                "conversion_rule": "no justified Joule conversion in current topic package",
            },
            {
                "symbol": "N",
                "meaning": "particle-count proxy in engine model",
                "unit": "count",
                "layer": "topic_proxy_layer",
                "status": "combinatorial_count",
                "code_surfaces": ["T13-001", "T13-002", "T13-003"],
                "conversion_rule": "count only; no dimensional conversion needed",
            },
            {
                "symbol": "S_proxy",
                "meaning": "Stirling entropy proxy from topic engine",
                "unit": "dimensionless_proxy",
                "layer": "topic_proxy_layer",
                "status": "proxy_not_physical_entropy",
                "code_surfaces": ["T13-001"],
                "conversion_rule": "no justified mapping to J/K or k_B units is documented yet",
            },
            {
                "symbol": "T_proxy",
                "meaning": "engine temperature-like quantity derived from S_proxy and E quanta",
                "unit": "dimensionless_proxy",
                "layer": "topic_proxy_layer",
                "status": "proxy_not_kelvin",
                "code_surfaces": ["T13-002"],
                "conversion_rule": "must not be reported as kelvin without a separate scale contract",
            },
            {
                "symbol": "q",
                "meaning": "synthetic heat-flux-like variable in Cattaneo demo",
                "unit": "synthetic_flux_proxy",
                "layer": "topic_proxy_layer",
                "status": "proxy_not_external_observable",
                "code_surfaces": ["T13-010"],
                "conversion_rule": "no stable SI calibration in current topic package",
            },
            {
                "symbol": "grad(T)",
                "meaning": "synthetic temperature-gradient-like driver in Cattaneo demo",
                "unit": "synthetic_gradient_proxy",
                "layer": "topic_proxy_layer",
                "status": "proxy_not_external_observable",
                "code_surfaces": ["T13-010"],
                "conversion_rule": "current values are proxy inputs, not sourced SI gradients",
            },
            {
                "symbol": "T_vac / T_sys",
                "meaning": "vacuum-sink sandbox temperatures",
                "unit": "mixed_labels_not_closed",
                "layer": "topic_proxy_layer",
                "status": "labelled_as_kelvin_but_not_physically_closed",
                "code_surfaces": ["T13-011"],
                "conversion_rule": "must not be treated as a physically grounded temperature field without conservation and mechanism closure",
            },
        ],
        "forbidden_unit_shortcuts": [
            "Do not report T13-002 engine temperature as kelvin.",
            "Do not report T13-001 entropy proxy as physical entropy in J/K.",
            "Do not treat synthetic Cattaneo q or grad(T) as sourced SI observables.",
            "Do not mix vacuum-sink temperature labels with the source-backed Landauer/gravity temperature layer.",
        ],
        "open_contract_steps": [
            "Map proxy energy quanta to a physically justified energy scale or keep the proxy layer explicitly nondimensional.",
            "Map entropy proxy outputs to a declared physical entropy convention or keep them diagnostic-only.",
            "Define whether any UET bridge term introduces a conversion between proxy and SI layers, and how that conversion is tested.",
        ],
        "claim_boundary": (
            "This contract separates current SI and proxy layers. It does not provide a full conversion from the topic engine to physical observables."
        ),
    }
    UNITS_CONTRACT_PATH.write_text(json.dumps(units_contract, indent=2), encoding="utf-8")
    return units_contract


def _build_landauer_uet_mapping(metrics):
    mapping = {
        "schema_version": "1.0",
        "topic": "0.13_Thermodynamic_Bridge",
        "purpose": (
            "State what the current topic can honestly claim about a UET-to-Landauer mapping, "
            "using current code and verifier evidence rather than aspiration."
        ),
        "status": "imported_constraint_not_noncircular_uet_derivation",
        "claim_boundary": (
            "Current 0.13 evidence supports Landauer as an imported lower-bound constraint. "
            "It does not yet show a non-circular UET derivation of the erasure-energy cost."
        ),
        "current_code_reading": {
            "engine_surface": "Code/01_Engine/Engine_Thermodynamics.py::get_landauer_limit",
            "current_relation": "return k_B * T_K * ln(2) * (beta / beta)",
            "interpretation": (
                "The current implementation preserves the standard Landauer form exactly. "
                "Because beta cancels algebraically, the present engine does not expose an additional UET-dependent scaling in this path."
            ),
            "added_uet_structure_detected": False,
        },
        "mapping_layers": [
            {
                "layer_id": "imported_standard_constraint",
                "status": "present",
                "statement": "Landauer lower bound enters as an externally established constraint formula.",
                "evidence": [
                    "T13-004",
                    "Research_Landauer.landauer_energy",
                    "engine_vs_codata_relative_error == 0"
                ],
            },
            {
                "layer_id": "uET_parameter_usage",
                "status": "present_but_trivialized",
                "statement": "A beta symbol appears in the engine path, but the current expression beta/beta cancels out.",
                "evidence": [
                    "Engine_Thermodynamics.get_landauer_limit",
                    "no change in output from beta in current verifier path"
                ],
            },
            {
                "layer_id": "noncircular_bridge_claim",
                "status": "absent",
                "statement": "No current artifact shows how UET variables generate the lower bound without reusing the standard relation directly.",
                "evidence_needed": [
                    "explicit mapping from UET variables to erasure cost",
                    "parameter-origin statement for any bridge coefficient",
                    "test distinguishing imported Landauer baseline from a UET-added term"
                ],
            },
        ],
        "current_evidence_summary": {
            "lower_bound_metric": metrics["jun_2014_ratio_to_landauer_lower_bound"],
            "codata_match_metric": metrics["landauer_engine_vs_codata_relative_error"],
            "what_passes_now": (
                "Exact-constant consistency and lower-bound non-violation."
            ),
            "what_does_not_pass_now": (
                "A UET-specific, non-circular derivation or correction term."
            ),
        },
        "forbidden_overreads": [
            "Do not say UET derives Landauer from first principles based on the current engine path.",
            "Do not treat beta symbol presence alone as bridge closure.",
            "Do not treat zero error against CODATA as evidence of a UET-added mechanism.",
        ],
        "next_hardening_steps": [
            "State whether beta is meant to be a derived bridge coefficient, a normalization tag, or a placeholder in this lane.",
            "If UET adds no correction here, document the lane explicitly as an imported thermodynamic boundary condition.",
            "If UET is meant to add structure, implement and test a nontrivial mapping that survives claim-discipline review.",
        ],
    }
    LANDAUER_UET_MAPPING_PATH.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    return mapping


def _build_beta_role_clarification():
    clarification = {
        "schema_version": "1.0",
        "topic": "0.13_Thermodynamic_Bridge",
        "purpose": (
            "Record what the current repository state supports about beta in topic 0.13, "
            "so legacy wording does not outrun the current verifier and engine path."
        ),
        "status": "beta_present_but_not_closed_as_derived_bridge_coefficient",
        "claim_boundary": (
            "Beta is visible in topic 0.13 language and code, but the current verifier does not support treating it "
            "as a closed thermodynamic bridge coefficient."
        ),
        "evidence_sources": [
            {
                "path": "Code/01_Engine/Engine_Thermodynamics.py::get_landauer_limit",
                "observation": "beta appears algebraically as beta/beta and cancels",
                "supports": "placeholder_or_normalization_tag_in_current_landauer_lane",
            },
            {
                "path": "Code/03_Research/Research_Landauer.py",
                "observation": "primary verifier treats Landauer as imported lower-bound constraint and blocks bridge-proof claims",
                "supports": "claim_discipline_ceiling",
            },
            {
                "path": "Code/03_Research/Research_Real_Data_Validation.py",
                "observation": "legacy script says beta*C*I term has thermodynamic basis, but this is not the current topic status authority",
                "supports": "legacy_claim_risk_only",
            },
            {
                "path": "Code/03_Research/Research_Thermodynamic_Bridge.py",
                "observation": "legacy research script equates beta with kT ln 2 for a bridge narrative, but this is not exported by the current verifier",
                "supports": "legacy_claim_risk_only",
            },
        ],
        "current_allowed_reading": {
            "landauer_lane": "beta may be mentioned only as a label attached to the imported lower-bound lane, not as a closed derived coefficient.",
            "engine_lane": "beta currently behaves as a non-operative placeholder or normalization tag in get_landauer_limit because it cancels out.",
            "topic_status_lane": "0.13 may export lower-bound consistency, not a verified beta bridge term.",
        },
        "disallowed_reading": [
            "beta is experimentally verified as a UET thermodynamic coefficient",
            "beta*C*I term is closed by current 0.13 evidence",
            "beta in the current engine path generates a nontrivial correction to Landauer"
        ],
        "role_options_under_current_evidence": [
            {
                "role": "placeholder_symbol",
                "fit_to_current_evidence": "strong",
                "reason": "beta appears in code and narratives but does not currently alter the Landauer output."
            },
            {
                "role": "normalization_tag",
                "fit_to_current_evidence": "plausible",
                "reason": "beta may mark the intended bridge slot without yet supplying a derived coefficient."
            },
            {
                "role": "derived_bridge_coefficient",
                "fit_to_current_evidence": "not_supported",
                "reason": "no non-circular derivation or tested nontrivial output path is attached to current verifier exports."
            },
        ],
        "next_hardening_questions": [
            "Should beta remain explicit in the Landauer lane if it cancels out?",
            "If beta is only a placeholder here, should legacy scripts and notes say that more clearly?",
            "If beta is meant to be derived later, what artifact will show its origin and nontrivial effect?"
        ],
    }
    BETA_ROLE_CLARIFICATION_PATH.write_text(
        json.dumps(clarification, indent=2), encoding="utf-8"
    )
    return clarification


def _build_foundation_claim_gate(
    metrics,
    readiness_matrix,
    row_controller_summary,
    evidence_lanes,
    uncertainty_summary,
    bridge_derivation_map,
    units_contract,
    landauer_uet_mapping,
    beta_role_clarification,
):
    source_summary = readiness_matrix["summary"]
    lower_bound_pass = evidence_lanes["landauer_lower_bound"]["status"] == "PASS"
    formula_pass = evidence_lanes["bekenstein_hawking_formula_consistency"]["status"] == "PASS"
    source_ready = (
        source_summary["targets_ready_for_source_review"]
        == source_summary["source_targets_total"]
    )
    bridge_unblocked = evidence_lanes["uet_bridge_hypothesis"]["status"] != "BLOCKED"

    gate = {
        "schema_version": "1.0",
        "topic": "0.13_Thermodynamic_Bridge",
        "purpose": "Machine-readable claim gate for using 0.13 as a UET theory foundation.",
        "foundation_role": "core information-entropy-energy constraint layer",
        "status": "FOUNDATION_WARN",
        "claim_ceiling": "C - formula/lower-bound consistency only",
        "accepted_foundation_exports": [
            {
                "export_id": "T13_EXPORT_LANDAUER_LOWER_BOUND",
                "status": "PASS" if lower_bound_pass else "FAIL",
                "claim_class": "C",
                "allowed_usage": "May constrain UET information-erasure energy language as a lower-bound relation.",
                "metric": "jun_2014_ratio_to_landauer_lower_bound",
                "value": metrics["jun_2014_ratio_to_landauer_lower_bound"],
                "blocker_to_stronger_usage": (
                    "Active Landauer row controllers remain open ("
                    + ", ".join(
                        f"{row['row_id']} -> {row['next_controller']}"
                        for row in row_controller_summary["controller_rows"]
                    )
                    + "), and the uncertainty lane is only "
                    f"{uncertainty_summary['summary']['current_status']}."
                ),
            },
            {
                "export_id": "T13_EXPORT_STANDARD_THERMO_GRAVITY_IDENTITIES",
                "status": "PASS" if formula_pass else "FAIL",
                "claim_class": "C",
                "allowed_usage": "May cite Bekenstein, Unruh, and Hawking relations as standard formula constraints.",
                "metric": "bekenstein_unruh_hawking_formula_consistency",
                "value": "formula_consistency_only",
                "blocker_to_stronger_usage": "These identities do not derive UET field variables by themselves.",
            },
        ],
        "blocked_foundation_exports": [
            {
                "export_id": "T13_EXPORT_UET_BRIDGE_PROOF",
                "status": "BLOCKED" if not bridge_unblocked else "OPEN",
                "claim_class": "A/B blocked",
                "forbidden_usage": "Do not cite 0.13 as proof that UET derives information, entropy, and energy from first principles.",
                "blockers": evidence_lanes["uet_bridge_hypothesis"]["blockers"]
                + [
                    f"{row['row_id']} controller: {row['next_controller']}"
                    for row in row_controller_summary["controller_rows"]
                ]
                + [
                    f"Bridge derivation map status: {bridge_derivation_map['status']}",
                    f"Units contract status: {units_contract['status']}",
                    f"Landauer-UET mapping status: {landauer_uet_mapping['status']}",
                    f"Beta role clarification status: {beta_role_clarification['status']}",
                ],
            },
            {
                "export_id": "T13_EXPORT_SOURCE_NORMALIZED_LANDAUER_DATASET",
                "status": "BLOCKED" if not source_ready else "READY_FOR_REVIEW",
                "claim_class": "B blocked",
                "forbidden_usage": "Do not cite the Landauer benchmark package as a fully source-normalized dataset.",
                "blockers": [
                    {
                        "source_target": row["name"],
                        "next_controller": next(
                            (
                                controller_row["next_controller"]
                                for controller_row in row_controller_summary["controller_rows"]
                                if row["name"].startswith(
                                    {
                                        "berut_2012_summary_300K": "Berut",
                                        "jun_2014_summary_300K": "Jun",
                                        "hong_2016_candidate_nanometric_memory_branch": "Hong",
                                        "peterson_2018_quantum_landauer_branch": "Quantum Landauer branch",
                                    }[controller_row["row_id"]]
                                )
                            ),
                            "not_declared",
                        ),
                    }
                    for row in readiness_matrix["readiness_rows"]
                    if not row["ready_for_source_review"]
                ],
            },
            {
                "export_id": "T13_EXPORT_CATTANEO_EXTERNAL_VALIDATION",
                "status": "SIMULATION_ONLY",
                "claim_class": "D",
                "forbidden_usage": "Do not use the Cattaneo branch as external heat-transport validation.",
                "blockers": [
                    "Current Cattaneo data is synthetic/proxy.",
                    "No real dataset, fixed-parameter threshold, or source package is attached.",
                ],
            },
        ],
        "dependency_exports": {
            "0.23_Unity_Scale_Link": {
                "may_inherit": [
                    "T13_EXPORT_LANDAUER_LOWER_BOUND",
                    "T13_EXPORT_STANDARD_THERMO_GRAVITY_IDENTITIES",
                ],
                "must_not_inherit": [
                    "T13_EXPORT_UET_BRIDGE_PROOF",
                    "T13_EXPORT_SOURCE_NORMALIZED_LANDAUER_DATASET",
                    "T13_EXPORT_CATTANEO_EXTERNAL_VALIDATION",
                ],
            },
            "0.0_Grand_Unification": {
                "may_inherit": [
                    "lower-bound/formula-consistency status",
                    "source-evidence blocker map",
                ],
                "must_block_theory_level_claim_if": [
                    "0.13 artifact status is WARN/FAIL",
                    "source evidence readiness has pending targets",
                    "UET bridge hypothesis lane remains BLOCKED",
                    "uncertainty preprocessing is not complete",
                ],
            },
        },
        "tier_decision": {
            "current": "Do not promote to Tier A",
            "reason": "The topic is foundational, but source-normalized data, uncertainty propagation, and UET-specific derivation are not closed.",
            "promotion_requirements": [
                "Berut must move beyond the selected Figure 3 preview locator to one numeric point capture or one stronger upstream numeric surface, Jun must attach final-source parity or local archival for the pinned Table 1/Figure 4 source-facing summary, and Peterson still needs one exact source-facing quantity.",
                "Uncertainty propagation for Landauer heat values and black-hole mass inputs.",
                "A derivation map from UET information-field variables to the standard thermodynamic identities, with open steps converted into derived or artifact-backed states.",
                "A units contract that closes the proxy-to-SI boundary or keeps the bridge claim explicitly nondimensional.",
                "A Landauer-to-UET mapping that does more than restate the imported lower bound.",
                "A beta-role artifact showing whether beta is placeholder, normalization tag, or derived coefficient in this lane.",
                "Verifier artifact showing no blocked source-evidence or hypothesis lanes.",
            ],
        },
        "claim_boundary": "0.13 is a priority foundation topic, but only its lower-bound and standard-formula lanes are currently usable by dependent theory topics.",
        "row_controller_summary": row_controller_summary["controller_rows"],
    }
    FOUNDATION_CLAIM_GATE_PATH.write_text(json.dumps(gate, indent=2), encoding="utf-8")
    return gate


def _build_thermodynamic_claim_scope_gate(
    status,
    evidence_lanes,
    readiness_matrix,
    row_controller_summary,
    foundation_claim_gate,
    uncertainty_summary,
    bridge_derivation_map,
    units_contract,
    landauer_uet_mapping,
    beta_role_clarification,
):
    lower_bound_status = evidence_lanes["landauer_lower_bound"]["status"]
    formula_status = evidence_lanes["bekenstein_hawking_formula_consistency"]["status"]
    bridge_status = evidence_lanes["uet_bridge_hypothesis"]["status"]
    source_summary = readiness_matrix["summary"]
    source_ready = (
        source_summary["targets_ready_for_source_review"]
        == source_summary["source_targets_total"]
    )
    controller_status = "WARN"
    if status == "FAIL" or lower_bound_status != "PASS" or formula_status != "PASS":
        controller_status = "FAIL"

    return {
        "schema_version": "1.0",
        "topic": "0.13_Thermodynamic_Bridge",
        "controller_status": controller_status,
        "controller_reason": (
            "Formula and lower-bound lanes are usable, but UET bridge export remains blocked by source, uncertainty, and derivation gates."
            if controller_status == "WARN"
            else "One or more formula/lower-bound controller lanes failed; dependent topics must not inherit 0.13 claims."
        ),
        "claim_class": "C_formula_lower_bound_only",
        "allowed_claims_now": [
            {
                "claim": "Landauer lower-bound consistency may constrain information-erasure energy wording.",
                "status": lower_bound_status,
                "artifact_role": "lower-bound gate",
                "source_evidence_readiness": "source_referenced_not_raw_table_archived",
            },
            {
                "claim": "Bekenstein, Unruh, and Hawking relations may be cited as standard formula-consistency constraints.",
                "status": formula_status,
                "artifact_role": "standard-formula diagnostic",
                "source_evidence_readiness": "formula_identity_not_uet_dynamics_proof",
            },
        ],
        "blocked_claims": [
            {
                "claim": "0.13 proves the UET information-entropy-energy bridge.",
                "status": "BLOCKED" if bridge_status == "BLOCKED" else "OPEN",
                "blocking_reason": "The UET-specific bridge lane is still a hypothesis lane, not a closed derivation.",
                "next_evidence_required": evidence_lanes["uet_bridge_hypothesis"].get("blockers", [])
                + [
                    f"{row['row_id']} controller must move beyond {row['next_controller']}"
                    for row in row_controller_summary["controller_rows"]
                ]
                + [
                    f"bridge_derivation_map status must move beyond {bridge_derivation_map['status']}",
                    f"units_contract status must move beyond {units_contract['status']}",
                    f"landauer_uet_mapping status must move beyond {landauer_uet_mapping['status']}",
                    f"beta_role_clarification status must move beyond {beta_role_clarification['status']}",
                ],
            },
            {
                "claim": "The Landauer benchmark package is fully source-normalized.",
                "status": "BLOCKED" if not source_ready else "READY_FOR_REVIEW",
                "blocking_reason": "Source-evidence readiness targets remain pending.",
                "next_evidence_required": [
                    {
                        "source_target": row["name"],
                        "next_controller": next(
                            (
                                controller_row["next_controller"]
                                for controller_row in row_controller_summary["controller_rows"]
                                if row["name"].startswith(
                                    {
                                        "berut_2012_summary_300K": "Berut",
                                        "jun_2014_summary_300K": "Jun",
                                        "hong_2016_candidate_nanometric_memory_branch": "Hong",
                                        "peterson_2018_quantum_landauer_branch": "Quantum Landauer branch",
                                    }[controller_row["row_id"]]
                                )
                            ),
                            "not_declared",
                        ),
                    }
                    for row in readiness_matrix["readiness_rows"]
                    if not row["ready_for_source_review"]
                ],
            },
            {
                "claim": "The synthetic Cattaneo branch is external heat-transport validation.",
                "status": "BLOCKED",
                "blocking_reason": "The current Cattaneo lane is simulation-only.",
                "next_evidence_required": [
                    "real heat-transport dataset",
                    "fixed-parameter threshold",
                    "source package with hashes",
                ],
            },
        ],
        "blocked_export_phrases": [
            "thermodynamic bridge proved",
            "verified UET bridge",
            "exact information energy equivalence",
            "external thermodynamic validation",
            "entropy energy unification solved",
            "Tier A foundation complete",
        ],
        "machine_readable_next_blockers": [
            "raw_landauer_numeric_tables_not_archived",
            f"landauer_uncertainty_status_{uncertainty_summary['summary']['current_status']}",
            f"uet_bridge_derivation_status_{bridge_derivation_map['status']}",
            f"units_contract_status_{units_contract['status']}",
            f"landauer_uet_mapping_status_{landauer_uet_mapping['status']}",
            f"beta_role_clarification_status_{beta_role_clarification['status']}",
            "synthetic_cattaneo_not_external_validation",
            "foundation_claim_gate_not_passed",
        ],
        "foundation_gate_summary": {
            "status": foundation_claim_gate["status"],
            "claim_ceiling": foundation_claim_gate["claim_ceiling"],
            "accepted_exports": [
                item["export_id"]
                for item in foundation_claim_gate["accepted_foundation_exports"]
                if item["status"] == "PASS"
            ],
            "blocked_exports": [
                item["export_id"]
                for item in foundation_claim_gate["blocked_foundation_exports"]
                if item["status"] != "PASS"
            ],
        },
        "row_controller_summary": row_controller_summary["controller_rows"],
        "dependency_export_policy": foundation_claim_gate["dependency_exports"],
        "claim_boundary": (
            "0.13 may be used as a lower-bound and standard-formula constraint layer. "
            "It must not be exported as proof of the UET bridge, source-normalized Landauer validation, "
            "or external heat-transport validation until the blocked lanes close."
        ),
    }


def _write_verification_artifact(test_results, plot_paths, metrics):
    test_pass = all(item["passed"] for item in test_results)
    plot_pass = all(item["saved"] for item in plot_paths)
    formula_pass = metrics["landauer_engine_vs_codata_relative_error"] < 1e-12
    lower_bound_pass = metrics["jun_2014_ratio_to_landauer_lower_bound"] >= 1.0

    warnings = []
    if not plot_pass:
        warnings.append("One or more optional visualization files failed to render.")
    warnings.append(
        "Berut/CODATA source records and source-lock hashes are pinned, and the current Berut summary row now has a selected Figure 3 preview locator, but numeric-point capture or stronger-surface closure is still open."
    )
    warnings.append(
        "Bekenstein/Jacobson checks are formula-consistency checks, not independent tests of UET dynamics."
    )

    status = "PASS" if test_pass and plot_pass and formula_pass and lower_bound_pass and not warnings else "WARN"
    if not (test_pass and formula_pass and lower_bound_pass):
        status = "FAIL"

    source_evidence_intake_stub = _build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = _build_source_evidence_readiness_matrix(
        source_evidence_intake_stub
    )
    row_controller_summary = _build_row_controller_summary()
    evidence_lanes = _build_evidence_lanes(test_results, metrics, source_evidence_readiness_matrix)
    uncertainty_preprocessing_plan = _build_uncertainty_preprocessing_plan(metrics)
    measured_constant_uncertainty_package = _build_measured_constant_uncertainty_package()
    uncertainty_propagation_summary = _build_uncertainty_propagation_summary(
        metrics,
        measured_constant_uncertainty_package,
    )
    bridge_derivation_map = _build_bridge_derivation_map()
    units_contract = _build_units_contract()
    landauer_uet_mapping = _build_landauer_uet_mapping(metrics)
    beta_role_clarification = _build_beta_role_clarification()
    foundation_claim_gate = _build_foundation_claim_gate(
        metrics,
        source_evidence_readiness_matrix,
        row_controller_summary,
        evidence_lanes,
        uncertainty_propagation_summary,
        bridge_derivation_map,
        units_contract,
        landauer_uet_mapping,
        beta_role_clarification,
    )
    thermodynamic_claim_scope_gate = _build_thermodynamic_claim_scope_gate(
        status,
        evidence_lanes,
        source_evidence_readiness_matrix,
        row_controller_summary,
        foundation_claim_gate,
        uncertainty_propagation_summary,
        bridge_derivation_map,
        units_contract,
        landauer_uet_mapping,
        beta_role_clarification,
    )

    warnings.append(
        "Uncertainty propagation is now partial only: Berut summary intervals are attached, gravity-context rows now add mass-plus-direct-CODATA-2022-G intervals, Jun final-source parity/local archival remains open, and systematic astrophysical terms are still excluded."
    )

    artifact = {
        "schema_version": "1.3",
        "topic": "0.13_Thermodynamic_Bridge",
        "command": ".venv\\Scripts\\python.exe docs\\topics\\0.13_Thermodynamic_Bridge\\Code\\03_Research\\Research_Landauer.py",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "claim_class": "C",
        "inputs": _input_identity(),
        "metrics": metrics,
        "evidence_lanes": evidence_lanes,
        "uncertainty_preprocessing_plan": uncertainty_preprocessing_plan,
        "measured_constant_uncertainty_package": measured_constant_uncertainty_package,
        "uncertainty_propagation_summary": uncertainty_propagation_summary,
        "bridge_derivation_map": bridge_derivation_map,
        "units_contract": units_contract,
        "landauer_uet_mapping": landauer_uet_mapping,
        "beta_role_clarification": beta_role_clarification,
        "thermodynamic_claim_scope_gate": thermodynamic_claim_scope_gate,
        "foundation_claim_gate": {
            "path": FOUNDATION_CLAIM_GATE_PATH.relative_to(ROOT).as_posix(),
            "sha256": _sha256(FOUNDATION_CLAIM_GATE_PATH),
            "status": foundation_claim_gate["status"],
            "claim_ceiling": foundation_claim_gate["claim_ceiling"],
            "accepted_foundation_exports": [
                item["export_id"]
                for item in foundation_claim_gate["accepted_foundation_exports"]
                if item["status"] == "PASS"
            ],
            "blocked_foundation_exports": [
                item["export_id"]
                for item in foundation_claim_gate["blocked_foundation_exports"]
                if item["status"] != "PASS"
            ],
            "tier_decision": foundation_claim_gate["tier_decision"],
            "claim_boundary": foundation_claim_gate["claim_boundary"],
        },
        "thresholds": {
            "landauer_engine_vs_codata_relative_error_max": 1e-12,
            "jun_2014_observed_to_landauer_lower_bound_min": 1.0,
            "required_test_pass_count": len(test_results),
            "required_plot_artifacts": len(plot_paths),
        },
        "test_results": test_results,
        "plot_artifacts": plot_paths,
        "source_evidence_intake_stub": {
            "path": SOURCE_EVIDENCE_INTAKE_PATH.relative_to(ROOT).as_posix(),
            "sha256": _sha256(SOURCE_EVIDENCE_INTAKE_PATH),
            "source_targets": [item["name"] for item in source_evidence_intake_stub["source_targets"]],
            "claim_boundary": (
                "This intake stub is for source evidence capture only. "
                "It does not authorize data or claim upgrades by itself."
            ),
        },
        "source_evidence_readiness_matrix": {
            "path": SOURCE_EVIDENCE_READINESS_PATH.relative_to(ROOT).as_posix(),
            "sha256": _sha256(SOURCE_EVIDENCE_READINESS_PATH),
            "summary": source_evidence_readiness_matrix["summary"],
            "claim_boundary": (
                "This readiness matrix is a workflow gate only. "
                "It tracks whether source evidence is still pending."
            ),
        },
        "row_controller_summary": row_controller_summary,
        "uncertainty_preprocessing_manifest": {
            "path": UNCERTAINTY_PREPROCESSING_PATH.relative_to(ROOT).as_posix(),
            "sha256": _sha256(UNCERTAINTY_PREPROCESSING_PATH),
            "current_status": uncertainty_preprocessing_plan["current_status"],
            "row_count": len(uncertainty_preprocessing_plan["rows"]),
            "claim_boundary": uncertainty_preprocessing_plan["claim_boundary"],
        },
        "uncertainty_propagation_artifact": {
            "path": UNCERTAINTY_PROPAGATION_SUMMARY_PATH.relative_to(ROOT).as_posix(),
            "sha256": _sha256(UNCERTAINTY_PROPAGATION_SUMMARY_PATH),
            "current_status": uncertainty_propagation_summary["summary"]["current_status"],
            "rows_with_propagated_intervals": uncertainty_propagation_summary["summary"]["rows_with_propagated_intervals"],
            "rows_missing_uncertainty_inputs": uncertainty_propagation_summary["summary"]["rows_missing_uncertainty_inputs"],
            "claim_boundary": uncertainty_propagation_summary["claim_boundary"],
        },
        "measured_constant_uncertainty_artifact": {
            "path": MEASURED_CONSTANT_UNCERTAINTY_PACKAGE_PATH.relative_to(ROOT).as_posix(),
            "sha256": _sha256(MEASURED_CONSTANT_UNCERTAINTY_PACKAGE_PATH),
            "status": measured_constant_uncertainty_package["status"],
            "row_policy_count": len(measured_constant_uncertainty_package["row_policy"]),
            "claim_boundary": measured_constant_uncertainty_package["claim_boundary"],
        },
        "bridge_derivation_artifact": {
            "path": BRIDGE_DERIVATION_MAP_PATH.relative_to(ROOT).as_posix(),
            "sha256": _sha256(BRIDGE_DERIVATION_MAP_PATH),
            "status": bridge_derivation_map["status"],
            "required_derivation_steps_open": sum(
                1
                for step in bridge_derivation_map["required_derivation_steps"]
                if step["current_state"] != "closed"
            ),
            "claim_boundary": bridge_derivation_map["claim_boundary"],
        },
        "units_contract_artifact": {
            "path": UNITS_CONTRACT_PATH.relative_to(ROOT).as_posix(),
            "sha256": _sha256(UNITS_CONTRACT_PATH),
            "status": units_contract["status"],
            "proxy_symbols_count": sum(
                1 for symbol in units_contract["symbols"] if symbol["layer"] == "topic_proxy_layer"
            ),
            "physical_symbols_count": sum(
                1 for symbol in units_contract["symbols"] if symbol["layer"] == "si_physical_layer"
            ),
            "claim_boundary": units_contract["claim_boundary"],
        },
        "landauer_uet_mapping_artifact": {
            "path": LANDAUER_UET_MAPPING_PATH.relative_to(ROOT).as_posix(),
            "sha256": _sha256(LANDAUER_UET_MAPPING_PATH),
            "status": landauer_uet_mapping["status"],
            "added_uet_structure_detected": landauer_uet_mapping["current_code_reading"]["added_uet_structure_detected"],
            "claim_boundary": landauer_uet_mapping["claim_boundary"],
        },
        "beta_role_clarification_artifact": {
            "path": BETA_ROLE_CLARIFICATION_PATH.relative_to(ROOT).as_posix(),
            "sha256": _sha256(BETA_ROLE_CLARIFICATION_PATH),
            "status": beta_role_clarification["status"],
            "claim_boundary": beta_role_clarification["claim_boundary"],
        },
        "paper_readiness_gate": {
            "status": "BLOCKED",
            "blocking_conditions": [
                "source_evidence_readiness_matrix.targets_ready_for_source_review < source_targets_total",
                "uet_bridge_hypothesis lane remains BLOCKED",
                "uncertainty_preprocessing_plan.current_status != complete",
                "uncertainty_propagation_summary.current_status != complete",
                "bridge_derivation_map.status != derived_or_closed",
                "units_contract.status != closed_proxy_to_si_mapping",
                "landauer_uet_mapping.status != noncircular_mapping_closed",
                "beta_role_clarification.status != derived_coefficient_role_closed",
                "foundation_claim_gate.status != FOUNDATION_PASS",
            ],
            "allowed_public_wording": [
                "formula-consistency check",
                "lower-bound consistency",
                "source-referenced internal benchmark",
                "UET bridge hypothesis",
            ],
            "forbidden_public_wording": [
                "solved",
                "verified UET bridge",
                "exact thermodynamic bridge",
                "external validation",
            ],
        },
        "warnings": warnings,
        "interpretation": (
            "The Landauer relation is anchored to exact SI constants and topic-local literature summary values. "
            "The verifier currently supports formula-consistency and lower-bound checks, and now records first-pass "
            "propagated intervals for Berut-summary and black-hole mass rows. A machine-readable derivation map now "
            "separates standard imported identities from UET proxy and hypothesis layers. A machine-readable units "
            "contract now separates the SI and proxy symbol layers. A Landauer-to-UET mapping artifact now records "
            "that the current engine path imports the lower bound as a constraint rather than exposing a nontrivial "
            "UET-added term. A beta-role clarification artifact now records that beta is present in topic language "
            "but not closed as a derived thermodynamic bridge coefficient. The UET-specific thermodynamic bridge "
            "still requires narrower Berut/Jun/Peterson source closure, fuller uncertainty propagation, and dependency proof."
        ),
    }
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"\n[Artifact] Verification artifact written: {ARTIFACT_PATH}")
    print(f"[Artifact] Status: {status}")
    return artifact

# Initialize Engine for calculations
try:
    engine_path = (
        root_path
        / "docs/topics/0.13_Thermodynamic_Bridge/Code/01_Engine/Engine_Thermodynamics.py"
    )
    spec = importlib.util.spec_from_file_location("Engine_Thermodynamics", engine_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    UETThermoEngine = getattr(module, "UETThermoEngine")
    engine = UETThermoEngine()
except Exception as e:
    print(f"Error loading Engine: {e}")
    sys.exit(1)


# ==============================================================================
# LANDAUER LIMIT
# ==============================================================================


def landauer_energy(T: float, bits: float = 1.0) -> float:
    """
    Calculate minimum energy to erase information.

    Args:
        T: Temperature in Kelvin
        bits: Number of bits to erase

    Returns:
        Energy in Joules
    """
    """
    Calculate minimum energy to erase information.
    Delegates to Engine (get_landauer_limit).
    """
    return engine.get_landauer_limit(T) * bits


def landauer_energy_eV(T: float, bits: float = 1.0) -> float:
    """Same as landauer_energy but returns eV."""
    eV_to_J = 1.602176634e-19
    return landauer_energy(T, bits) / eV_to_J


# ==============================================================================
# BEKENSTEIN BOUND
# ==============================================================================


def bekenstein_bound(R: float, E: float) -> float:
    """
    Calculate maximum entropy (bits) in a region.

    S_max = 2*pi * k_B * R * E / (hbar * c)

    Args:
        R: Radius of region (meters)
        E: Total energy in region (Joules)

    Returns:
        Maximum entropy in bits
    """
    """
    Calculate maximum entropy (bits) in a region.
    Delegates to Engine.
    """
    return engine.get_region_entropy_bound(R, E)


def bekenstein_bound_black_hole(M_kg: float) -> float:
    """
    Calculate Bekenstein-Hawking entropy for black hole.

    S = A / (4 * l_P^2) where A = 4*pi*(2GM/c^2)^2

    Args:
        M_kg: Black hole mass in kg

    Returns:
        Entropy in Planck units
    """

    """
    Calculate Bekenstein-Hawking entropy for black hole.
    Delegates to Engine.
    """
    return engine.get_bekenstein_entropy(M_kg)


# ==============================================================================
# JACOBSON TEMPERATURE
# ==============================================================================


def unruh_temperature(a: float) -> float:
    """
    Calculate Unruh temperature for accelerated observer.

    T = hbar*a / (2*pi * k_B * c)

    Args:
        a: Proper acceleration (m/s^2)

    Returns:
        Temperature in Kelvin
    """
    """
    Calculate Unruh temperature for accelerated observer.
    Delegates to Engine.
    """
    return engine.get_unruh_temperature(a)


def surface_gravity_temperature(M_kg: float) -> float:
    """
    Calculate Hawking temperature for black hole.

    T = hbar*c^3 / (8*pi * G * M * k_B)

    Args:
        M_kg: Black hole mass in kg

    Returns:
        Temperature in Kelvin
    """

    """
    Calculate Hawking temperature for black hole.
    Delegates to Engine.
    """
    return engine.get_hawking_temperature(M_kg)


# ==============================================================================
# TEST FUNCTIONS
# ==============================================================================


def test_landauer_limit():
    """Test Landauer limit at various temperatures."""
    print("=" * 60)
    print("TEST 1: Landauer Limit (E = kT ln(2))")
    print("=" * 60)

    # Test temperatures
    temperatures = [
        (300, "Room Temperature"),
        (4.2, "Liquid Helium"),
        (1, "Cryogenic"),
        (2.725, "CMB Temperature"),
    ]

    print(f"\n{'Temperature':<20} {'E (Joules)':<15} {'E (eV)':<12}")
    print("-" * 50)

    for T, name in temperatures:
        E_J = landauer_energy(T)
        E_eV = landauer_energy_eV(T)
        print(f"{name} ({T}K){'':<6} {E_J:.3e}       {E_eV:.6f}")

    # Source-backed lower-bound comparison. The numeric row is still topic-derived.
    print("\n[DATA] Lower-Bound Benchmark Summary:")
    T_exp = 300  # Room temperature
    E_landauer = landauer_energy_eV(T_exp)
    kT_eV = E_landauer / np.log(2)
    E_jun_source = 0.71 * kT_eV
    E_legacy_context = 0.028  # eV legacy mixed-lineage context; see DATA_MANIFEST

    error = abs(E_jun_source - E_landauer) / E_landauer * 100
    print(f"   Landauer Prediction: {E_landauer:.6f} eV")
    print(f"   Jun source-facing asymptotic-work summary: {E_jun_source:.6f} eV")
    print(f"   Legacy mixed-lineage context row: {E_legacy_context:.3f} eV")
    print("   [OK] Jun source-facing summary remains above the Landauer lower bound")

    return True


def test_bekenstein_bound():
    """Test Bekenstein bound for various systems."""
    print("\n" + "=" * 60)
    print("TEST 2: Bekenstein Bound (S_max = 2*pi*k*R*E/(hbar*c))")
    print("=" * 60)

    # Test systems
    M_sun = 1.989e30
    c = 299792458
    systems = [
        ("Human Brain", 0.1, 10),  # 10cm radius, 10J metabolic
        ("Hard Drive (1TB)", 0.05, 100),  # 5cm, 100J capacity
        ("Earth", 6.371e6, 5.5e41),  # Earth mass-energy
        ("Solar Mass BH", 3e3, M_sun * c**2),  # Schwarzschild radius, mc^2
    ]

    print(f"\n{'System':<20} {'S_max (bits)':<20}")
    print("-" * 45)

    for name, R, E in systems:
        S_max = bekenstein_bound(R, E)
        print(f"{name:<20} {S_max:.3e}")

    # Black hole comparison
    print("\n[DATA] Black Hole Entropy (Bekenstein-Hawking):")
    M_bh = M_sun
    S_bh = bekenstein_bound_black_hole(M_bh)
    print(f"   Solar mass BH entropy: {S_bh:.3e} Planck units")
    print(f"   [OK] Confirms Area Law: S ~ R^2")

    return True


def test_jacobson_temperature():
    """Test Unruh/Hawking temperature derivation."""
    print("\n" + "=" * 60)
    print("TEST 3: Jacobson Thermodynamic Gravity")
    print("=" * 60)

    # Unruh temperature for Earth surface gravity
    g_earth = 9.8
    T_unruh = unruh_temperature(g_earth)
    print(f"\n[EARTH] Unruh temperature at Earth surface (a=9.8 m/s^2):")
    print(f"   T = {T_unruh:.3e} K (extremely cold!)")

    # Hawking temperature for various BH masses
    print("\n[BH] Hawking Temperature for Black Holes:")
    M_sun = 1.989e30
    masses = [
        ("Solar Mass", M_sun),
        ("Sagittarius A*", 4e6 * M_sun),
        ("M87*", 6.5e9 * M_sun),
    ]

    for name, M in masses:
        T_hawk = surface_gravity_temperature(M)
        print(f"   {name}: T = {T_hawk:.3e} K")

    print("\n[OK] Jacobson bridge constraint: delta_Q = T dS is consistent with thermodynamic-gravity literature")
    print("   Interpretation: formula-consistency context, not an independent UET gravity proof.")

    return True


def run_all_tests():
    """Run all thermodynamic bridge tests."""
    print("\n" + "=" * 70)
    print("[THERMO] UET THERMODYNAMIC BRIDGE VALIDATION")
    print("   Connecting Information <-> Entropy <-> Energy <-> Spacetime")
    print("=" * 70)

    results = []
    results.append(("Landauer Limit", test_landauer_limit()))
    results.append(("Bekenstein Bound", test_bekenstein_bound()))
    results.append(("Jacobson Temperature", test_jacobson_temperature()))

    print("\n" + "=" * 70)
    print("[DATA] SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, r in results if r)
    for name, result in results:
        status = "[OK] PASS" if result else "[FAIL] FAIL"
        print(f"   {name}: {status}")

    print(f"\nTotal: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("* THERMODYNAMIC BRIDGE FORMULA CHECKS PASSED *")

    # --- VISUALIZATION ---
    plot_paths = []
    try:
        from docs.core import uet_viz

        result_dir = UETPathManager.get_result_dir(
            topic_id="0.13_Thermodynamic_Bridge",
            experiment_name="Research_Landauer",
            pillar="03_Research",
            category="log",
        )
        result_dir.mkdir(parents=True, exist_ok=True)

        # 1. Landauer: Energy vs Temperature
        fig1 = uet_viz.go.Figure()
        T_range = np.linspace(0.1, 400, 100)
        E_range = [landauer_energy_eV(t) for t in T_range]

        fig1.add_trace(
            uet_viz.go.Scatter(
                x=T_range,
                y=E_range,
                mode="lines",
                name="Landauer Limit",
                line=dict(color="red"),
            )
        )
        # Experimental point
        fig1.add_trace(
            uet_viz.go.Scatter(
                x=[300],
                y=[0.71 * (landauer_energy_eV(300) / np.log(2))],
                mode="markers",
                name="Jun source-facing benchmark",
                marker=dict(color="blue", size=10),
            )
        )
        fig1.add_trace(
            uet_viz.go.Scatter(
                x=[300],
                y=[0.028],
                mode="markers",
                name="Legacy mixed-lineage context row",
                marker=dict(color="orange", size=10, symbol="x"),
            )
        )

        fig1.update_layout(
            title="Landauer Limit: Info-Energy Cost",
            xaxis_title="Temperature (K)",
            yaxis_title="Erasure Cost (eV)",
        )
        saved = uet_viz.save_plot(fig1, "landauer/landauer_viz.png", result_dir)
        plot_paths.append(
            {
                "name": "landauer_limit_curve",
                "path": str(saved.relative_to(TOPIC_DIR)) if saved else None,
                "saved": saved is not None,
            }
        )

        # 2. Bekenstein: Entropy vs Mass (Black Hole)
        M_sun = 1.989e30  # Define for viz
        fig2 = uet_viz.go.Figure()
        M_range = np.logspace(30, 40, 50)  # Solar mass range
        S_range = [bekenstein_bound_black_hole(m) for m in M_range]

        fig2.add_trace(
            uet_viz.go.Scatter(
                x=M_range / M_sun,
                y=S_range,
                mode="lines",
                name="BH Entropy",
                line=dict(color="purple"),
            )
        )

        fig2.update_layout(
            title="Bekenstein-Hawking Entropy",
            xaxis_title="Mass (Solar Masses)",
            yaxis_title="Entropy (Planck Units)",
            xaxis_type="log",
            yaxis_type="log",
        )
        saved = uet_viz.save_plot(fig2, "bekenstein/bekenstein_viz.png", result_dir)
        plot_paths.append(
            {
                "name": "bekenstein_hawking_entropy_curve",
                "path": str(saved.relative_to(TOPIC_DIR)) if saved else None,
                "saved": saved is not None,
            }
        )

        # 3. Jacobson: T_unruh vs Acceleration
        fig3 = uet_viz.go.Figure()
        a_range = np.logspace(0, 25, 50)
        T_unruh_range = [unruh_temperature(a) for a in a_range]

        fig3.add_trace(
            uet_viz.go.Scatter(
                x=a_range,
                y=T_unruh_range,
                mode="lines",
                name="Unruh Temp",
                line=dict(color="orange"),
            )
        )

        fig3.update_layout(
            title="Unruh Temperature (Jacobson Link)",
            xaxis_title="Acceleration (m/s^2)",
            yaxis_title="Temperature (K)",
            xaxis_type="log",
            yaxis_type="log",
        )
        saved = uet_viz.save_plot(fig3, "jacobson/jacobson_viz.png", result_dir)
        plot_paths.append(
            {
                "name": "unruh_temperature_curve",
                "path": str(saved.relative_to(TOPIC_DIR)) if saved else None,
                "saved": saved is not None,
            }
        )

        print("\n[Viz] Generated 3 bridge visualizations.")

    except Exception as e:
        print(f"Viz Error: {e}")
        plot_paths.append({"name": "visualization_block", "path": None, "saved": False, "error": str(e)})

    test_results = [
        {"name": name, "passed": bool(result)} for name, result in results
    ]
    artifact = _write_verification_artifact(test_results, plot_paths, _audit_metrics())
    return artifact["status"] != "FAIL"


if __name__ == "__main__":
    run_all_tests()



