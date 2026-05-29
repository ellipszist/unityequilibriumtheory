"""
UET Rydberg Formula Validation
==============================
Topic 0.20 diagnostic verifier.

This verifier checks a standard Rydberg-series relation against the topic-local
NIST hydrogen spectrum working copy and CODATA R_H value. It supports an internal
hydrogen-spectrum benchmark only; it does not derive the Rydberg formula from UET
first principles or validate many-electron atomic physics.
"""

import json
import platform
import re
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

import numpy as np


def _bootstrap():
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return None


ROOT = _bootstrap()
if ROOT is None:
    print("CRITICAL: UET docs root not found")
    sys.exit(1)

TOPIC_DIR = ROOT / "docs" / "topics" / "0.20_Atomic_Physics"
SPECTRUM_PATH = TOPIC_DIR / "Data" / "03_Research" / "nist_hydrogen_spectrum.json"
CODATA_PATH = TOPIC_DIR / "Data" / "03_Research" / "codata_2018_atomic.json"
HYDROGEN_LIKE_ION_PATH = TOPIC_DIR / "Data" / "03_Research" / "hydrogen_like_ion_spectrum.json"
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_20_atomic_physics_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"
ATOMIC_FORMULA_BRIDGE_PATH = TOPIC_DIR / "Data" / "03_Research" / "atomic_formula_bridge_manifest.json"


def file_sha256(path):
    digest = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_transition(text):
    values = [int(token) for token in re.findall(r"\d+", text)]
    if len(values) != 2:
        raise ValueError(f"Cannot parse transition: {text}")
    return values[0], values[1]


def collect_lines(spectrum):
    rows = []
    for series_name in ("balmer_series", "lyman_series"):
        for line in spectrum[series_name]["lines"]:
            n_upper, n_lower = parse_transition(line["transition"])
            rows.append(
                {
                    "series": series_name.replace("_series", ""),
                    "name": line["name"],
                    "n_upper": n_upper,
                    "n_lower": n_lower,
                    "wavelength_vacuum_nm": line["wavelength_vacuum_nm"],
                }
            )
    return rows


def write_artifact(artifact):
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.20_Atomic_Physics",
        "purpose": "Source evidence intake before upgrading claims across hydrogen, level-energy, and many-electron atomic branches.",
        "source_targets": [
            {
                "name": "NIST hydrogen spectrum package",
                "priority": "immediate",
                "status_hint": "source_backed_working_copy",
                "evidence_entries": [
                    "working_copy_json_path",
                    "doi_or_url",
                    "transition_scope",
                    "unit_basis",
                    "hash_lock",
                    "benchmark_role",
                ],
            },
            {
                "name": "CODATA atomic constants package",
                "priority": "immediate",
                "status_hint": "source_backed_working_copy",
                "evidence_entries": [
                    "working_copy_json_path",
                    "doi",
                    "constant_scope",
                    "unit_basis",
                    "hash_lock",
                    "benchmark_role",
                ],
            },
            {
                "name": "Hydrogen level-energy package",
                "priority": "high",
                "status_hint": "secondary_lane_not_yet_primary_gated",
                "evidence_entries": [
                    "level_data_path",
                    "upstream_source_package",
                    "artifact_path",
                    "observable_scope",
                    "unit_basis",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Hydrogen-like ion package",
                "priority": "high",
                "status_hint": "source_referenced_one_electron_ion_rows",
                "evidence_entries": [
                    "ion_line_dataset",
                    "reduced_mass_convention",
                    "nuclear_mass_source",
                    "artifact_path",
                    "observable_scope",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Fine-structure and Lamb-shift package",
                "priority": "high",
                "status_hint": "blocked_precision_branch",
                "evidence_entries": [
                    "fine_structure_dataset",
                    "lamb_shift_dataset",
                    "comparison_artifact",
                    "observable_scope",
                    "unit_basis",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Helium and many-electron package",
                "priority": "medium",
                "status_hint": "blocked_theory_branch",
                "evidence_entries": [
                    "helium_dataset",
                    "many_electron_dataset",
                    "artifact_paths",
                    "observable_scope",
                    "cross_topic_dependency_map",
                    "upgrade_requirement",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself validate full atomic theory.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "NIST hydrogen spectrum package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 5,
            "fields_pending": 1,
            "pending_fields": ["transcription_precision_audit"],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "CODATA atomic constants package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Hydrogen level-energy package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 2,
            "fields_pending": 4,
            "pending_fields": [
                "upstream_source_package",
                "artifact_path",
                "observable_scope",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "Hydrogen level data exists, but there is no primary artifact for the level-energy lane yet.",
        },
        {
            "name": "Hydrogen-like ion package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 5,
            "fields_pending": 1,
            "pending_fields": [
                "direct_primary_ASD_row_for_Li_III",
            ],
            "ready_for_source_review": True,
            "blocking_reason": "Ready for provisional source review: He II is a direct NIST handbook row, while Li III is currently a secondary paper row citing NIST and still needs direct ASD capture.",
        },
        {
            "name": "Fine-structure and Lamb-shift package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "fine_structure_dataset",
                "lamb_shift_dataset",
                "comparison_artifact",
                "observable_scope",
                "unit_basis",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The current topic has no fine-structure or Lamb-shift artifact.",
        },
        {
            "name": "Helium and many-electron package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "helium_dataset",
                "many_electron_dataset",
                "artifact_paths",
                "cross_topic_dependency_map",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "Helium and many-electron lanes remain excluded from the current hydrogen-only benchmark.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.20_Atomic_Physics",
        "purpose": "Readiness matrix for source-evidence review across atomic benchmark and theory branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row has enough provenance structure for source review. It does not by itself upgrade atomic-theory claims.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.20_Atomic_Physics",
        "purpose": "Claim gate for separate atomic-physics branches inside the topic.",
        "summary": {
            "branches_total": 8,
            "accepted_now": 4,
            "blocked_for_strong_claims": 4,
        },
        "branches": [
            {
                "branch": "Hydrogen Rydberg benchmark branch",
                "status": "accepted_source_backed_benchmark_branch",
                "allowed_usage_now": "Accepted hydrogen-spectrum benchmark branch using the standard Rydberg relation with source-backed NIST/CODATA working copies.",
                "blocker_to_stronger_claim": "Need a first-principles derivation before promoting beyond a benchmark branch.",
            },
            {
                "branch": "Hydrogen constant-consistency branch",
                "status": "accepted_constant_checkpoint_branch",
                "allowed_usage_now": "Accepted atomic-constant consistency branch for `R_H` and related hydrogen residual checks.",
                "blocker_to_stronger_claim": "Constant consistency does not independently validate atomic theory or UET derivation.",
            },
            {
                "branch": "Bohr/de Broglie/Rydberg formula bridge branch",
                "status": "accepted_formula_bridge_manifest_branch",
                "allowed_usage_now": "Accepted as an explicit inheritance map from standard atomic theory into the UET topic, with no first-principles UET derivation claim.",
                "blocker_to_stronger_claim": "Need a UET-specific derivation artifact that derives alpha, R_H, and transition operators without treating inherited formulas as proof.",
            },
            {
                "branch": "Hydrogen level-energy branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Secondary lane only.",
                "blocker_to_stronger_claim": "Need a dedicated level-energy artifact with threshold policy.",
            },
            {
                "branch": "Hydrogen-like ion branch",
                "status": "accepted_provisional_source_referenced_benchmark_branch",
                "allowed_usage_now": "Selected He+ and Li2+ one-electron ion rows may be cited as a provisional reduced-mass hydrogenic benchmark when the artifact gate passes.",
                "blocker_to_stronger_claim": "Need direct primary ASD capture for Li III, source precision normalization, fine-structure component policy, and more ions before claiming general hydrogen-like ion validation.",
            },
            {
                "branch": "Fine-structure and Lamb-shift branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need source-backed precision datasets and dedicated residual artifacts.",
            },
            {
                "branch": "Helium and many-electron branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need dedicated helium and many-electron datasets plus artifacts.",
            },
            {
                "branch": "First-principles UET atomic theory claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need derivation and validation beyond the standard hydrogen Rydberg benchmark.",
            },
        ],
        "claim_boundary": "This gate keeps the topic at hydrogen benchmark status, not full atomic-theory closure.",
    }


def build_atomic_formula_bridge_manifest() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.20_Atomic_Physics",
        "purpose": "Formula dependency map showing how inherited standard atomic equations connect to UET foundation topics without upgrading them into first-principles derivations.",
        "dependency_chain": [
            {
                "step_id": "AT20-BRIDGE-01",
                "relation": "Delta E = h nu = h c / lambda",
                "source_role": "inherited standard photon-energy relation",
                "uet_role": "0.13 may motivate an information-energy accounting interpretation, but does not currently derive h or transition operators.",
                "status": "accepted_standard_relation",
                "claim_ceiling": "photon transition bookkeeping only",
            },
            {
                "step_id": "AT20-BRIDGE-02",
                "relation": "lambda_de_broglie = h / p",
                "source_role": "inherited de Broglie relation",
                "uet_role": "candidate standing-wave bridge for orbital quantization; not independently derived from UET in this artifact.",
                "status": "accepted_standard_relation",
                "claim_ceiling": "standard-theory inheritance",
            },
            {
                "step_id": "AT20-BRIDGE-03",
                "relation": "2 pi r = n lambda_de_broglie; m v r = n hbar",
                "source_role": "Bohr quantization condition",
                "uet_role": "candidate geometric resonance interpretation only.",
                "status": "accepted_standard_relation",
                "claim_ceiling": "Bohr-level explanatory bridge, not many-electron theory",
            },
            {
                "step_id": "AT20-BRIDGE-04",
                "relation": "E_n = - mu c^2 alpha^2 Z^2 / (2 n^2)",
                "source_role": "hydrogenic energy relation with reduced mass",
                "uet_role": "depends on 0.6 alpha/electroweak constants and 0.17 electron-mass context, but those topics do not yet derive the atomic Hamiltonian here.",
                "status": "dependency_mapped_open_derivation",
                "claim_ceiling": "hydrogenic formula bridge only",
            },
            {
                "step_id": "AT20-BRIDGE-05",
                "relation": "1/lambda = R_H (1/n_lower^2 - 1/n_upper^2)",
                "source_role": "standard Rydberg wavelength relation",
                "uet_role": "primary verifier uses this as the benchmark formula; UET-specific R_H derivation remains blocked.",
                "status": "source_backed_benchmark_formula",
                "claim_ceiling": "selected hydrogen spectrum benchmark",
            },
            {
                "step_id": "AT20-BRIDGE-06",
                "relation": "many-electron Hamiltonian = one-electron terms + electron-electron repulsion + exchange/correlation + relativistic/QED corrections",
                "source_role": "standard many-electron problem framing",
                "uet_role": "open target for future UET atomic engine; no validated UET many-electron operator exists in this topic yet.",
                "status": "blocked_theory_extension",
                "claim_ceiling": "cannot validate helium, periodic elements, or general atomic spectra",
            },
        ],
        "cross_topic_dependencies": [
            {
                "topic": "0.13_Thermodynamic_Bridge",
                "usable_now": "energy/information accounting context only",
                "not_yet_usable_as": "derivation of h, R_H, or spectral transition operators",
            },
            {
                "topic": "0.6_Electroweak_Physics",
                "usable_now": "source/context for alpha and charge-sector constants",
                "not_yet_usable_as": "closed electroweak derivation of atomic spectra",
            },
            {
                "topic": "0.17_Mass_Generation",
                "usable_now": "electron-mass dependency context",
                "not_yet_usable_as": "validated derivation of reduced-mass atomic levels",
            },
            {
                "topic": "0.23_Unity_Scale_Link",
                "usable_now": "dependency/scale gate",
                "not_yet_usable_as": "unity proof from atomic agreement",
            },
        ],
        "claim_boundary": "This manifest makes the bridge explicit: inherited Bohr/de Broglie/Rydberg formulas are allowed as standard-theory foundations, while UET derivation and many-electron closure remain blocked until separate artifacts exist.",
    }


def _nucleus_mass_kg(row: dict, codata: dict, ion_data: dict) -> float:
    constants = codata["constants"]
    if row["isotope_or_nucleus"] == "alpha_particle":
        return ion_data["mass_convention"]["alpha_particle_mass_kg"]["value"]
    if row["isotope_or_nucleus"] == "Li-7_approx":
        u_kg = ion_data["mass_convention"]["atomic_mass_constant_kg"]["value"]
        li7_u = ion_data["mass_convention"]["lithium_7_relative_atomic_mass_u"]["value"]
        return li7_u * u_kg - 3.0 * constants["m_e"]["value"]
    raise ValueError(f"Unsupported nucleus convention: {row['isotope_or_nucleus']}")


def build_hydrogen_like_checkpoint(codata: dict, ion_data: dict) -> dict:
    r_infinity = codata["constants"]["R_infinity"]["value"]
    electron_mass = codata["constants"]["m_e"]["value"]
    predictions = []
    for row in ion_data["lines"]:
        term = (1.0 / row["n_lower"] ** 2) - (1.0 / row["n_upper"] ** 2)
        nucleus_mass = _nucleus_mass_kg(row, codata, ion_data)
        r_z = r_infinity * row["Z"] ** 2 / (1.0 + electron_mass / nucleus_mass)
        predicted_nm = 1e9 / (r_z * term)
        observed_nm = row["observed_wavelength_nm"]
        error_ppm = abs(predicted_nm - observed_nm) / observed_nm * 1e6
        predictions.append(
            {
                "ion": row["ion"],
                "spectrum_label": row["spectrum_label"],
                "Z": row["Z"],
                "name": row["name"],
                "transition": row["transition"],
                "n_upper": row["n_upper"],
                "n_lower": row["n_lower"],
                "observed_wavelength_nm": observed_nm,
                "predicted_wavelength_nm_reduced_mass": predicted_nm,
                "wavelength_error_ppm": error_ppm,
                "source_status": row["source_status"],
                "source": row["source"],
                "source_locator": row["source_locator"],
                "line_structure_note": row["line_structure_note"],
            }
        )
    threshold = {
        "average_wavelength_error_ppm_max": 200.0,
        "max_wavelength_error_ppm_max": 300.0,
        "source_policy": "He II direct NIST handbook row; Li III secondary paper row citing NIST accepted only as provisional until direct ASD capture.",
    }
    avg_error_ppm = float(np.mean([row["wavelength_error_ppm"] for row in predictions]))
    max_error_ppm = float(np.max([row["wavelength_error_ppm"] for row in predictions]))
    status = (
        "PASS"
        if avg_error_ppm <= threshold["average_wavelength_error_ppm_max"]
        and max_error_ppm <= threshold["max_wavelength_error_ppm_max"]
        else "FAIL"
    )
    return {
        "schema_version": "1.0",
        "role": "hydrogen_like_reduced_mass_benchmark",
        "status": status,
        "claim_class": "C_provisional_selected_hydrogen_like_ion_benchmark",
        "formula": "R_Z = R_infinity Z^2 / (1 + m_e / M_nucleus); 1/lambda = R_Z (1/n_lower^2 - 1/n_upper^2)",
        "threshold": threshold,
        "metrics": {
            "line_count": len(predictions),
            "average_wavelength_error_ppm": avg_error_ppm,
            "max_wavelength_error_ppm": max_error_ppm,
            "direct_primary_rows": sum(1 for row in predictions if row["source_status"].startswith("primary")),
            "secondary_source_rows": sum(1 for row in predictions if row["source_status"].startswith("secondary")),
        },
        "limitations": [
            "Uses nonrelativistic reduced-mass hydrogenic scaling as a benchmark, not a UET first-principles derivation.",
            "Li III is source-referenced through a paper row citing NIST and still needs direct ASD capture.",
            "Fine-structure components are not resolved or fitted; rows are representative source wavelengths/blends.",
            "Cannot validate helium neutral atoms or many-electron elements.",
        ],
        "predictions": predictions,
    }


def build_atomic_claim_scope_gate(
    status: str,
    avg_error_ppm: float,
    max_error_ppm: float,
    slope_error_ppm: float,
    hydrogen_like_checkpoint: dict,
    source_evidence_readiness_matrix: dict,
    branch_claim_gate: dict,
) -> dict:
    controller_status = "WARN" if status == "PASS" else "FAIL"
    return {
        "schema_version": "1.0",
        "topic": "0.20_Atomic_Physics",
        "controller_status": controller_status,
        "controller_reason": (
            "The hydrogen Rydberg benchmark passed and selected hydrogen-like ion rows are provisionally gated, "
            "but export remains warning-gated because level-energy, direct Li III ASD capture, broader ion coverage, "
            "fine-structure, Lamb-shift, neutral helium, many-electron, and first-principles derivation branches are missing."
            if status == "PASS"
            else "The hydrogen Rydberg benchmark failed the declared residual thresholds."
        ),
        "claim_class": "C_hydrogen_rydberg_benchmark_only",
        "allowed_claims_now": [
            {
                "claim": "Selected hydrogen wavelengths match the standard Rydberg relation under the declared residual thresholds.",
                "status": status,
                "artifact_role": "primary hydrogen spectrum benchmark",
                "metrics": {
                    "average_wavelength_error_ppm": avg_error_ppm,
                    "max_wavelength_error_ppm": max_error_ppm,
                    "slope_error_ppm": slope_error_ppm,
                },
                "source_evidence_readiness": "nist_codata_working_copy_ready_for_review",
            },
            {
                "claim": "The CODATA R_H constant is used consistently in the benchmark.",
                "status": "CHECKPOINT_ONLY" if status == "PASS" else "BLOCKED",
                "artifact_role": "atomic constant consistency branch",
                "formula_role": "standard Rydberg relation, not UET first-principles derivation",
                "source_evidence_readiness": "codata_checkpoint_ready_for_review",
            },
            {
                "claim": "The topic now has an explicit formula bridge separating inherited Bohr/de Broglie/Rydberg physics from unproven UET derivation.",
                "status": "MANIFEST_ONLY",
                "artifact_role": "formula dependency bridge",
                "formula_role": "claim-boundary map, not a new empirical validation",
                "source_evidence_readiness": "local_manifest_ready_for_review",
            },
            {
                "claim": "Selected He+ and Li2+ one-electron ion wavelengths match the reduced-mass hydrogenic relation under provisional thresholds.",
                "status": hydrogen_like_checkpoint["status"],
                "artifact_role": "hydrogen-like ion reduced-mass benchmark",
                "metrics": hydrogen_like_checkpoint["metrics"],
                "source_evidence_readiness": "provisional_source_review_ready_with_direct_Li_III_ASD_capture_pending",
            },
        ],
        "blocked_claims": [
            {
                "claim": "UET derives the Rydberg relation or R_H from first principles.",
                "status": "BLOCKED",
                "blocking_reason": "The verifier uses the standard Rydberg relation with CODATA R_H; it is not a derivation artifact.",
                "next_evidence_required": [
                    "first-principles derivation package",
                    "formula audit for UET-specific R_H relation",
                    "independent validation artifact",
                ],
            },
            {
                "claim": "UET validates all hydrogen-like ions or derives their spectra from first principles.",
                "status": "BLOCKED",
                "blocking_reason": "The artifact now supports only selected source-referenced He+/Li2+ reduced-mass benchmark rows; direct Li III ASD capture, broader ion coverage, and UET derivation are still missing.",
                "next_evidence_required": [
                    "direct Li III ASD row capture",
                    "broader hydrogen-like ion spectral-line suite",
                    "fine-structure component policy",
                    "UET derivation artifact",
                ],
            },
            {
                "claim": "UET validates fine structure, Lamb shift, hyperfine structure, or QED corrections.",
                "status": "BLOCKED",
                "blocking_reason": "No source-backed precision datasets or residual artifacts for QED-scale effects are primary-gated.",
                "next_evidence_required": [
                    "fine-structure dataset",
                    "Lamb-shift dataset",
                    "hyperfine/QED correction artifact",
                ],
            },
            {
                "claim": "UET validates helium, many-electron atoms, or general atomic theory.",
                "status": "BLOCKED",
                "blocking_reason": "Helium and many-electron scripts are not primary source-gated benchmark artifacts.",
                "next_evidence_required": [
                    "helium source package",
                    "many-electron benchmark suite",
                    "uncertainty-aware residual thresholds",
                ],
            },
        ],
        "blocked_export_phrases": [
            "Rydberg constant derived from first principles",
            "all hydrogen-like ions validated",
            "atomic theory solved",
            "QED corrections validated",
            "Lamb shift explained",
            "helium validated",
            "many-electron atoms solved",
        ],
        "source_evidence_summary": source_evidence_readiness_matrix["summary"],
        "branch_claim_gate_summary": branch_claim_gate["summary"],
        "machine_readable_next_blockers": [
            "rydberg_derivation_artifact_missing",
            "hydrogen_level_energy_artifact_missing",
            "direct_li_iii_asd_capture_missing",
            "general_hydrogen_like_ion_suite_missing",
            "fine_structure_artifact_missing",
            "lamb_shift_artifact_missing",
            "helium_many_electron_artifact_missing",
        ],
        "claim_boundary": (
            "A PASS artifact supports only selected hydrogen Rydberg benchmark behavior with NIST/CODATA "
            "working copies plus provisional selected He+/Li2+ reduced-mass benchmark rows. It does not derive R_H, "
            "validate QED corrections, validate neutral helium or many-electron atoms, or close atomic theory."
        ),
    }


def run_rydberg_analysis():
    print("=" * 60)
    print("UET ATOMIC PHYSICS: RYDBERG VALIDATION")
    print("Data: NIST hydrogen spectrum + CODATA R_H")
    print("=" * 60)

    spectrum = load_json(SPECTRUM_PATH)
    codata = load_json(CODATA_PATH)
    ion_data = load_json(HYDROGEN_LIKE_ION_PATH)
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    atomic_formula_bridge_manifest = build_atomic_formula_bridge_manifest()
    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)
    write_json(ATOMIC_FORMULA_BRIDGE_PATH, atomic_formula_bridge_manifest)
    r_h = codata["constants"]["R_H"]["value"]
    r_infinity = codata["constants"]["R_infinity"]["value"]

    results = []
    x_vals = []
    y_vals = []
    for row in collect_lines(spectrum):
        term = (1.0 / row["n_lower"] ** 2) - (1.0 / row["n_upper"] ** 2)
        predicted_nm = 1e9 / (r_h * term)
        observed_nm = row["wavelength_vacuum_nm"]
        error_ppm = abs(predicted_nm - observed_nm) / observed_nm * 1e6
        inv_lam = 1.0 / (observed_nm * 1e-9)
        x_vals.append(term)
        y_vals.append(inv_lam)
        results.append(
            {
                **row,
                "geometric_term": term,
                "predicted_wavelength_nm": predicted_nm,
                "wavelength_error_ppm": error_ppm,
            }
        )
        print(
            f"  {row['name']}: observed={observed_nm:.4f} nm, "
            f"R_H prediction={predicted_nm:.4f} nm, error={error_ppm:.2f} ppm"
        )

    x_arr = np.array(x_vals)
    y_arr = np.array(y_vals)
    slope_origin = float(np.dot(x_arr, y_arr) / np.dot(x_arr, x_arr))
    slope_error_ppm = abs(slope_origin - r_h) / r_h * 1e6
    avg_error_ppm = float(np.mean([row["wavelength_error_ppm"] for row in results]))
    max_error_ppm = float(np.max([row["wavelength_error_ppm"] for row in results]))
    threshold = {
        "average_wavelength_error_ppm_max": 100.0,
        "max_wavelength_error_ppm_max": 250.0,
        "slope_error_ppm_max": 250.0,
    }
    status = (
        "PASS"
        if avg_error_ppm <= threshold["average_wavelength_error_ppm_max"]
        and max_error_ppm <= threshold["max_wavelength_error_ppm_max"]
        and slope_error_ppm <= threshold["slope_error_ppm_max"]
        else "FAIL"
    )
    hydrogen_like_checkpoint = build_hydrogen_like_checkpoint(codata, ion_data)
    atomic_claim_scope_gate = build_atomic_claim_scope_gate(
        status,
        avg_error_ppm,
        max_error_ppm,
        slope_error_ppm,
        hydrogen_like_checkpoint,
        source_evidence_readiness_matrix,
        branch_claim_gate,
    )

    artifact = {
        "schema_version": "1.2",
        "topic": "0.20_Atomic_Physics",
        "status": status,
        "claim_class": "C - source-backed internal hydrogen spectrum benchmark",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.20_Atomic_Physics/Code/03_Research/Research_Rydberg_Validation.py",
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "inputs": [
            {
                "path": str(SPECTRUM_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(SPECTRUM_PATH),
                "source": spectrum.get("source"),
                "doi": spectrum.get("publication", {}).get("doi"),
                "url": spectrum.get("publication", {}).get("url"),
            },
            {
                "path": str(CODATA_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(CODATA_PATH),
                "source": codata.get("source"),
                "doi": codata.get("publication", {}).get("doi"),
            },
            {
                "path": str(HYDROGEN_LIKE_ION_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(HYDROGEN_LIKE_ION_PATH),
                "source": ion_data.get("purpose"),
                "source_rows": [row["source_status"] for row in ion_data["lines"]],
            },
        ],
        "formula_ids": [
            "AT20-PHOTON-TRANSITION",
            "AT20-DEBROGLIE-STANDING-WAVE",
            "AT20-BOHR-HYDROGEN-ENERGY",
            "AT20-RYDBERG-WAVELENGTH",
            "AT20-RH-CODATA-CHECKPOINT",
            "AT20-SPECTRUM-RESIDUAL",
            "AT20-HYDROGENIC-Z2-CHECKPOINT",
            "AT20-UET-ATOMIC-BRIDGE-GATE",
        ],
        "threshold": threshold,
        "metrics": {
            "R_H_codata_m_inverse": r_h,
            "R_infinity_codata_m_inverse": r_infinity,
            "fitted_slope_through_origin_m_inverse": slope_origin,
            "slope_error_ppm": slope_error_ppm,
            "average_wavelength_error_ppm": avg_error_ppm,
            "max_wavelength_error_ppm": max_error_ppm,
            "line_count": len(results),
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
            "blocked_claim_exports": len(atomic_claim_scope_gate["blocked_export_phrases"]),
            "formula_bridge_steps": len(atomic_formula_bridge_manifest["dependency_chain"]),
            "hydrogen_like_checkpoint_predictions": len(hydrogen_like_checkpoint["predictions"]),
            "hydrogen_like_avg_error_ppm": hydrogen_like_checkpoint["metrics"]["average_wavelength_error_ppm"],
            "hydrogen_like_max_error_ppm": hydrogen_like_checkpoint["metrics"]["max_wavelength_error_ppm"],
        },
        "results": results,
        "limitations": [
            "This validates the standard Rydberg relation against the topic-local hydrogen spectrum working copy.",
            "It does not derive the Rydberg relation from UET first principles.",
            "The Bohr/de Broglie/Rydberg bridge is now explicit, but it remains inherited standard physics unless a UET derivation artifact is added.",
            "Hydrogen-like ion rows support only a provisional selected He+/Li2+ reduced-mass benchmark until direct Li III ASD capture and broader ion coverage are added.",
            "It does not validate fine structure, Lamb shift, helium, or many-electron atoms.",
        ],
    }
    artifact["atomic_formula_bridge_manifest"] = {
        "path": str(ATOMIC_FORMULA_BRIDGE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(atomic_formula_bridge_manifest, sort_keys=True).encode("utf-8")).hexdigest(),
        "dependency_steps": len(atomic_formula_bridge_manifest["dependency_chain"]),
        "cross_topic_dependencies": [row["topic"] for row in atomic_formula_bridge_manifest["cross_topic_dependencies"]],
        "claim_boundary": atomic_formula_bridge_manifest["claim_boundary"],
    }
    artifact["hydrogen_like_checkpoint"] = hydrogen_like_checkpoint
    artifact["source_evidence_intake_stub"] = {
        "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(source_evidence_intake_stub, sort_keys=True).encode("utf-8")).hexdigest(),
        "source_targets": [row["name"] for row in source_evidence_intake_stub["source_targets"]],
        "claim_boundary": source_evidence_intake_stub["claim_boundary"],
    }
    artifact["source_evidence_readiness_matrix"] = {
        "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(source_evidence_readiness_matrix, sort_keys=True).encode("utf-8")).hexdigest(),
        "summary": source_evidence_readiness_matrix["summary"],
        "claim_boundary": source_evidence_readiness_matrix["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(branch_claim_gate, sort_keys=True).encode("utf-8")).hexdigest(),
        "summary": branch_claim_gate["summary"],
        "claim_boundary": branch_claim_gate["claim_boundary"],
    }
    artifact["atomic_claim_scope_gate"] = atomic_claim_scope_gate
    artifact["interpretation"] = (
        "This artifact supports a hydrogen Rydberg benchmark branch, a bounded atomic-constant consistency branch, "
        "an explicit formula-bridge manifest from inherited Bohr/de Broglie/Rydberg physics into UET dependencies, "
        "and a provisional selected He+/Li2+ reduced-mass hydrogenic benchmark. It does not validate full atomic theory, "
        "fine structure, broad hydrogen-like ion coverage, neutral helium, or many-electron physics."
    )
    write_artifact(artifact)
    print(f"Average wavelength error: {avg_error_ppm:.2f} ppm")
    print(f"Max wavelength error: {max_error_ppm:.2f} ppm")
    print(f"Slope error: {slope_error_ppm:.2f} ppm")
    print(f"Artifact status: {status}")
    print(f"Artifact written: {ARTIFACT_PATH}")
    return status == "PASS"


if __name__ == "__main__":
    success = run_rydberg_analysis()
    sys.exit(0 if success else 1)
