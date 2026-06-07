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
HYDROGEN_LEVEL_PATH = TOPIC_DIR / "Data" / "03_Research" / "hydrogen_spectra_data.json"
HYDROGEN_LIKE_ION_PATH = TOPIC_DIR / "Data" / "03_Research" / "hydrogen_like_ion_spectrum.json"
PRECISION_SPECTROSCOPY_PATH = TOPIC_DIR / "Data" / "03_Research" / "hydrogen_precision_spectroscopy_sources.json"
HYDROGEN_LAMB_SHIFT_PATH = TOPIC_DIR / "Data" / "03_Research" / "hydrogen_lamb_shift_correction_sources.json"
HYDROGEN_HYPERFINE_21CM_PATH = TOPIC_DIR / "Data" / "03_Research" / "hydrogen_hyperfine_21cm_sources.json"
HYDROGEN_HYPERFINE_FERMI_CONSTANTS_PATH = TOPIC_DIR / "Data" / "03_Research" / "hydrogen_hyperfine_fermi_constants.json"
HELIUM_MANY_ELECTRON_PATH = TOPIC_DIR / "Data" / "03_Research" / "helium_many_electron_sources.json"
HELIUM_TRANSITION_ASSIGNMENTS_PATH = TOPIC_DIR / "Data" / "03_Research" / "helium_transition_assignments.json"
HELIUM_GROUND_STATE_ENERGY_PATH = TOPIC_DIR / "Data" / "03_Research" / "helium_ground_state_energy_sources.json"
HELIUM_QD_HOLDOUT_PATH = TOPIC_DIR / "Data" / "03_Research" / "helium_quantum_defect_holdout_sources.json"
ATOMIC_PREDICTIVE_V1_PARAMETER_MANIFEST_PATH = (
    TOPIC_DIR / "Data" / "03_Research" / "atomic_predictive_v1_parameter_manifest.json"
)
ATOMIC_PREDICTIVE_V1_THRESHOLD_MANIFEST_PATH = (
    TOPIC_DIR / "Data" / "03_Research" / "atomic_predictive_v1_threshold_manifest.json"
)
ATOMIC_PREDICTIVE_V1_OPERATOR_MANIFEST_PATH = (
    TOPIC_DIR / "Data" / "03_Research" / "atomic_predictive_v1_fixed_correction_operator_manifest.json"
)
ATOMIC_PREDICTIVE_V1_OPERATOR_BUILD_SPEC_MANIFEST_PATH = (
    TOPIC_DIR / "Data" / "03_Research" / "atomic_predictive_v1_operator_build_spec_manifest.json"
)
CHIANTI_HE_I_MANIFEST_PATH = (
    TOPIC_DIR / "Data" / "03_Research" / "external_holdouts" / "chianti_he_i" / "source_manifest.json"
)
LEGACY_MULTI_ELECTRON_PATH = TOPIC_DIR / "Code" / "03_Research" / "Research_Multi_Electron.py"
LEGACY_THREE_BODY_PATH = TOPIC_DIR / "Code" / "03_Research" / "Research_Atomic_ThreeBody.py"
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_20_atomic_physics_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"
ATOMIC_FORMULA_BRIDGE_PATH = TOPIC_DIR / "Data" / "03_Research" / "atomic_formula_bridge_manifest.json"
SPEED_OF_LIGHT_M_PER_S = 299_792_458.0
PLANCK_EV_S = 4.135667696e-15
ELEMENTARY_CHARGE_C = 1.602176634e-19
EV_PER_CM_INVERSE = PLANCK_EV_S * SPEED_OF_LIGHT_M_PER_S * 100.0


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
                    "wavelength_vacuum_uncertainty_nm": line.get("wavelength_vacuum_uncertainty_nm"),
                    "wavelength_uncertainty_basis": line.get("wavelength_uncertainty_basis"),
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
                "status_hint": "source_referenced_rounded_level_energy_rows",
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
                "status_hint": "source_package_ready_model_blocked",
                "evidence_entries": [
                    "fine_structure_dataset",
                    "lamb_shift_dataset",
                    "hyperfine_dataset",
                    "comparison_artifact",
                    "observable_scope",
                    "unit_basis",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Helium and many-electron package",
                "priority": "medium",
                "status_hint": "source_package_and_same_family_holdouts_ready_model_blocked",
                "evidence_entries": [
                    "helium_dataset",
                    "helium_quantum_defect_holdout_dataset",
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
            "pending_fields": ["official_or_upstream_line_uncertainty_capture"],
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
            "fields_complete": 5,
            "fields_pending": 1,
            "pending_fields": ["direct_level_table_transcription_precision"],
            "ready_for_source_review": True,
            "blocking_reason": "Ready for rounded-level source review: uses a local level table and NIST ionization-energy anchor, but still needs direct per-level ASD transcription precision.",
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
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "comparison_artifact",
                "primary_lamb_and_hyperfine_metrology_locators",
            ],
            "ready_for_source_review": True,
            "blocking_reason": "Precision targets are source-referenced, but no Dirac/QED/recoil/proton-radius/hyperfine correction model or residual artifact is primary-gated yet.",
        },
        {
            "name": "Helium and many-electron package",
            "priority": "medium",
            "fields_total": 7,
            "fields_complete": 6,
            "fields_pending": 2,
            "pending_fields": [
                "independent_external_helium_holdouts",
                "many_electron_model_and_thresholds",
            ],
            "ready_for_source_review": True,
            "blocking_reason": "Neutral helium source rows and same-source-family quantum-defect holdouts are ready for source review, but independent external holdouts and a two-electron Hamiltonian/correlation model remain blocked.",
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
            "branches_total": 9,
            "accepted_now": 5,
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
                "status": "accepted_rounded_level_energy_benchmark_branch",
                "allowed_usage_now": "Selected rounded hydrogen n-level energies may be cited as a source-referenced benchmark when the artifact gate passes.",
                "blocker_to_stronger_claim": "Need direct ASD per-level transcription precision, uncertainty propagation, and fine-structure/Lamb-shift separation before precision level claims.",
            },
            {
                "branch": "Hydrogen-like ion branch",
                "status": "accepted_provisional_source_referenced_benchmark_branch",
                "allowed_usage_now": "Selected He+ and Li2+ one-electron ion rows may be cited as a provisional reduced-mass hydrogenic benchmark when the artifact gate passes.",
                "blocker_to_stronger_claim": "Need direct primary ASD capture for Li III, source precision normalization, fine-structure component policy, and more ions before claiming general hydrogen-like ion validation.",
            },
            {
                "branch": "Fine-structure and Lamb-shift branch",
                "status": "source_package_ready_model_blocked",
                "allowed_usage_now": "May cite only as a prepared precision-source package for future fine/Lamb/hyperfine artifacts.",
                "blocker_to_stronger_claim": "Need Dirac/QED/recoil/proton-radius/hyperfine model, uncertainty propagation, and residual thresholds before precision claims.",
            },
            {
                "branch": "Helium and many-electron branch",
                "status": "source_package_ready_model_blocked",
                "allowed_usage_now": "May cite only as a prepared neutral-helium source package plus diagnostic quantum-defect residual/prediction gates for future many-electron artifacts.",
                "blocker_to_stronger_claim": "Need independent external holdouts, a correlated two-electron Hamiltonian/spectral model, uncertainty policy, and residual thresholds before helium or many-electron claims.",
            },
            {
                "branch": "Helium quantum-defect prediction branch",
                "status": "same_source_family_holdout_model_blocked",
                "allowed_usage_now": "May cite only as a limited source-calibrated He I quantum-defect diagnostic with same-source-family holdouts.",
                "blocker_to_stronger_claim": "Need independent external holdout lines and a CI/correlated model that predicts quantum defects instead of fitting them.",
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
                "relation": "nu_1S_2S = c R_H (1 - 1/4) + Delta nu_precision",
                "source_role": "standard nonrelativistic 1S-2S baseline plus missing precision corrections",
                "uet_role": "diagnostic gap sizing only; UET-specific Dirac/QED/recoil/proton-radius correction derivation remains blocked.",
                "status": "baseline_computed_open_precision_model",
                "claim_ceiling": "nonrelativistic precision-target residual diagnostic",
            },
            {
                "step_id": "AT20-BRIDGE-07",
                "relation": "E_nj/h = -c R_H/n^2 [1 + alpha^2/n (1/(j+1/2) - 3/(4n))]",
                "source_role": "leading Dirac/fine-structure baseline for hydrogen levels",
                "uet_role": "diagnostic gap sizing only; UET-specific alpha/orbital/Hamiltonian derivation and QED terms remain blocked.",
                "status": "dirac_baseline_computed_open_qed_model",
                "claim_ceiling": "leading fine-structure residual diagnostic",
            },
            {
                "step_id": "AT20-BRIDGE-08",
                "relation": "nu_1S_2S = nu_Dirac + (L_2S - L_1S) + Delta nu_recoil/proton-size/QED-residual",
                "source_role": "empirical Lamb-shift handoff for precision residual sizing",
                "uet_role": "source-referenced correction handoff only; UET-specific QED/recoil/proton-size derivation remains blocked.",
                "status": "empirical_lamb_handoff_computed_open_qed_decomposition",
                "claim_ceiling": "Lamb source handoff diagnostic, not QED validation",
            },
            {
                "step_id": "AT20-BRIDGE-09",
                "relation": "lambda_21cm = c / nu_hfs",
                "source_role": "source-locked neutral hydrogen hyperfine transition bookkeeping",
                "uet_role": "target for future UET hyperfine Hamiltonian work; no magnetic-moment/QED/proton-structure derivation exists yet.",
                "status": "source_locked_open_hyperfine_hamiltonian",
                "claim_ceiling": "21 cm source and unit bookkeeping only",
            },
            {
                "step_id": "AT20-BRIDGE-10",
                "relation": "nu_F = (8/3) alpha^2 c R_infinity (m_e/m_p) g_p",
                "source_role": "leading Fermi-contact hyperfine baseline",
                "uet_role": "diagnostic baseline only; UET-specific magnetic-moment, recoil, QED, and proton-structure derivation remains blocked.",
                "status": "fermi_baseline_computed_open_higher_order_corrections",
                "claim_ceiling": "21 cm leading hyperfine residual diagnostic",
            },
            {
                "step_id": "AT20-BRIDGE-11",
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
    if row["isotope_or_nucleus"] == "C-12_approx":
        u_kg = ion_data["mass_convention"]["atomic_mass_constant_kg"]["value"]
        c12_u = ion_data["mass_convention"]["carbon_12_relative_atomic_mass_u"]["value"]
        return c12_u * u_kg - 6.0 * constants["m_e"]["value"]
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
                "benchmark_lane": row.get("benchmark_lane", "primary_selected_benchmark"),
                "observed_wavelength_nm": observed_nm,
                "predicted_wavelength_nm_reduced_mass": predicted_nm,
                "wavelength_error_ppm": error_ppm,
                "source_status": row["source_status"],
                "source": row["source"],
                "source_locator": row["source_locator"],
                "line_structure_note": row["line_structure_note"],
            }
        )
    primary_predictions = [
        row for row in predictions if row["benchmark_lane"] == "primary_selected_benchmark"
    ]
    stress_predictions = [
        row for row in predictions if row["benchmark_lane"] == "extended_stress_test"
    ]
    threshold = {
        "average_wavelength_error_ppm_max": 200.0,
        "max_wavelength_error_ppm_max": 300.0,
        "source_policy": "Primary selected benchmark currently uses He II direct NIST handbook row and Li III secondary paper row citing NIST. C VI is kept in an extended stress-test lane until higher-Z fine/QED policy is added.",
    }
    avg_error_ppm = float(np.mean([row["wavelength_error_ppm"] for row in primary_predictions]))
    max_error_ppm = float(np.max([row["wavelength_error_ppm"] for row in primary_predictions]))
    stress_avg_error_ppm = (
        float(np.mean([row["wavelength_error_ppm"] for row in stress_predictions]))
        if stress_predictions
        else None
    )
    stress_max_error_ppm = (
        float(np.max([row["wavelength_error_ppm"] for row in stress_predictions]))
        if stress_predictions
        else None
    )
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
            "primary_benchmark_line_count": len(primary_predictions),
            "extended_stress_test_line_count": len(stress_predictions),
            "average_wavelength_error_ppm": avg_error_ppm,
            "max_wavelength_error_ppm": max_error_ppm,
            "extended_stress_test_average_wavelength_error_ppm": stress_avg_error_ppm,
            "extended_stress_test_max_wavelength_error_ppm": stress_max_error_ppm,
            "direct_primary_rows": sum(1 for row in predictions if row["source_status"].startswith("primary")),
            "secondary_source_rows": sum(1 for row in predictions if row["source_status"].startswith("secondary")),
            "nist_reference_compilation_rows": sum(1 for row in predictions if row["source_status"].startswith("nist_reference")),
        },
        "limitations": [
            "Uses nonrelativistic reduced-mass hydrogenic scaling as a benchmark, not a UET first-principles derivation.",
            "Li III is source-referenced through a paper row citing NIST and still needs direct ASD capture.",
            "C VI is included only as an extended higher-Z stress test; it is not counted in the primary selected-ion PASS/FAIL gate.",
            "Fine-structure components are not resolved or fitted; rows are representative source wavelengths/blends.",
            "Cannot validate helium neutral atoms or many-electron elements.",
        ],
        "extended_stress_test": {
            "status": "STRESS_TEST_RECORDED_FINE_QED_POLICY_OPEN" if stress_predictions else "NOT_PRESENT",
            "claim_class": "diagnostic_only_not_general_hydrogen_like_validation",
            "threshold_policy": "No PASS threshold is assigned to the higher-Z stress lane until source precision, fine-structure, and QED policy are added.",
            "predictions": stress_predictions,
        },
        "predictions": predictions,
    }


def build_hydrogen_like_domain_coverage_gate(hydrogen_like_checkpoint: dict, ion_data: dict) -> dict:
    predictions = hydrogen_like_checkpoint["predictions"]
    represented_z = sorted({row["Z"] for row in predictions})
    benchmark_lanes = sorted({row["benchmark_lane"] for row in predictions})
    primary_rows = [row for row in predictions if row["benchmark_lane"] == "primary_selected_benchmark"]
    stress_rows = [row for row in predictions if row["benchmark_lane"] == "extended_stress_test"]
    source_status_counts = {}
    for row in predictions:
        source_status_counts[row["source_status"]] = source_status_counts.get(row["source_status"], 0) + 1

    coverage_rows = [
        {
            "coverage_id": "one_electron_primary_rows",
            "status": "PARTIAL",
            "evidence": f"{len(primary_rows)} primary selected rows are present for Z={sorted({row['Z'] for row in primary_rows})}.",
            "blocker": "Primary lane is selected-row only and includes Li III through a secondary paper row citing NIST.",
        },
        {
            "coverage_id": "higher_z_stress_lane",
            "status": "RECORDED_NOT_PASS_GATED",
            "evidence": f"{len(stress_rows)} stress row is present for Z={sorted({row['Z'] for row in stress_rows})}.",
            "blocker": "No fine-structure/QED/source-precision policy exists for higher-Z PASS/FAIL.",
        },
        {
            "coverage_id": "direct_primary_source_capture",
            "status": "PARTIAL",
            "evidence": {
                "source_status_counts": source_status_counts,
                "direct_primary_rows": hydrogen_like_checkpoint["metrics"]["direct_primary_rows"],
                "secondary_source_rows": hydrogen_like_checkpoint["metrics"]["secondary_source_rows"],
            },
            "blocker": "Direct primary ASD capture is still missing for Li III.",
        },
        {
            "coverage_id": "multi_transition_suite",
            "status": "MISSING",
            "evidence": "Current rows are all 2 -> 1 Lyman-alpha style targets.",
            "blocker": "Need multiple transitions and components per ion before broad hydrogen-like validation.",
        },
        {
            "coverage_id": "fine_qed_policy",
            "status": "MISSING",
            "evidence": "Line-structure notes explicitly mark representative wavelengths/blends.",
            "blocker": "Fine-structure, Lamb/QED, recoil, and finite-nuclear-size policy is not primary-gated.",
        },
    ]
    blocking_rows = [row for row in coverage_rows if row["status"] != "READY"]
    return {
        "schema_version": "1.0",
        "role": "hydrogen_like_domain_coverage_gate",
        "status": "DOMAIN_EXPANSION_MAPPED_BROAD_VALIDATION_BLOCKED",
        "claim_class": "coverage_diagnostic_only",
        "formula_id": "AT20-HYDROGEN-LIKE-DOMAIN-COVERAGE",
        "represented_z": represented_z,
        "benchmark_lanes": benchmark_lanes,
        "coverage_rows": coverage_rows,
        "metrics": {
            "represented_z_count": len(represented_z),
            "represented_z_min": min(represented_z) if represented_z else None,
            "represented_z_max": max(represented_z) if represented_z else None,
            "primary_selected_row_count": len(primary_rows),
            "extended_stress_row_count": len(stress_rows),
            "source_status_count": source_status_counts,
            "coverage_check_count": len(coverage_rows),
            "blocking_coverage_check_count": len(blocking_rows),
            "all_rows_same_transition": len({row["transition"] for row in predictions}) == 1,
        },
        "next_required_artifacts": [
            "direct Li III ASD/source-page capture",
            "multi-ion and multi-transition hydrogen-like source package",
            "fine-structure/QED/recoil/finite-size policy before higher-Z PASS thresholds",
            "uncertainty-aware thresholds split by low-Z primary rows and higher-Z stress rows",
        ],
        "claim_boundary": "This gate maps hydrogen-like ion coverage only. It does not upgrade selected He+/Li2+ rows or C VI stress diagnostics into broad hydrogen-like ion validation.",
    }


def build_hydrogen_level_energy_benchmark(level_rows: list[dict]) -> dict:
    ionization_energy_ev = 13.5984
    results = []
    for row in level_rows:
        n = int(row["n"])
        observed_ev = float(row["Energy_eV"])
        predicted_ev = -ionization_energy_ev / (n * n)
        error_ppm = abs(predicted_ev - observed_ev) / abs(observed_ev) * 1e6
        results.append(
            {
                "n": n,
                "level": row["Level"],
                "observed_energy_eV": observed_ev,
                "predicted_energy_eV_from_ionization_anchor": predicted_ev,
                "energy_error_ppm": error_ppm,
            }
        )
    threshold = {
        "average_energy_error_ppm_max": 150.0,
        "max_energy_error_ppm_max": 250.0,
        "source_policy": "Rounded local n-level rows are checked against the NIST H ionization-energy anchor of 13.5984 eV; direct per-level ASD precision capture remains pending.",
    }
    avg_error_ppm = float(np.mean([row["energy_error_ppm"] for row in results]))
    max_error_ppm = float(np.max([row["energy_error_ppm"] for row in results]))
    status = (
        "PASS"
        if avg_error_ppm <= threshold["average_energy_error_ppm_max"]
        and max_error_ppm <= threshold["max_energy_error_ppm_max"]
        else "FAIL"
    )
    return {
        "schema_version": "1.0",
        "role": "hydrogen_rounded_level_energy_benchmark",
        "status": status,
        "claim_class": "C_source_referenced_rounded_hydrogen_level_benchmark",
        "formula": "E_n = -E_ionization / n^2",
        "source_anchor": {
            "name": "Hydrogen ionization energy",
            "value_eV": ionization_energy_ev,
            "source": "NIST Cross Section Atom Information / Atomic Data for Hydrogen",
            "url": "https://physics.nist.gov/cgi-bin/Ionization/atom.php?element=H",
            "source_status": "primary_nist_ionization_energy_anchor",
        },
        "threshold": threshold,
        "metrics": {
            "level_count": len(results),
            "average_energy_error_ppm": avg_error_ppm,
            "max_energy_error_ppm": max_error_ppm,
        },
        "limitations": [
            "This is a rounded n-level benchmark anchored to NIST hydrogen ionization energy.",
            "It does not validate fine-structure, Lamb-shift, hyperfine, or QED level splitting.",
            "It does not derive the hydrogen energy formula from UET first principles.",
            "Direct ASD per-level transcription precision remains pending.",
        ],
        "results": results,
    }


def build_precision_spectroscopy_gate(precision_sources: dict) -> dict:
    rows = precision_sources["rows"]
    status_counts = {}
    for row in rows:
        status_counts[row["current_artifact_status"]] = status_counts.get(row["current_artifact_status"], 0) + 1
    return {
        "schema_version": "1.0",
        "role": "hydrogen_precision_spectroscopy_source_gate",
        "status": "SOURCE_READY_MODEL_BLOCKED",
        "claim_class": "source_package_only_no_precision_validation",
        "source_row_count": len(rows),
        "targets": [
            {
                "target_id": row["target_id"],
                "observable": row["observable"],
                "value": row["value"],
                "uncertainty": row.get("uncertainty"),
                "unit": row["unit"],
                "source_type": row["source_type"],
                "current_artifact_status": row["current_artifact_status"],
                "blocker": row["blocker"],
            }
            for row in rows
        ],
        "status_counts": status_counts,
        "required_model_components": precision_sources["required_model_components"],
        "limitations": [
            "No precision residual is computed in this gate.",
            "The package prepares targets for future Dirac/QED/recoil/proton-radius/hyperfine artifacts only.",
            "Secondary-source rows must be upgraded to primary locators before public precision claims.",
            "This gate cannot be cited as Lamb-shift, hyperfine, fine-structure, or QED validation.",
        ],
        "claim_boundary": precision_sources["claim_boundary"],
    }


def build_precision_baseline_gate(precision_sources: dict, codata: dict) -> dict:
    """Compute the nonrelativistic Rydberg baseline for the sourced 1S-2S target."""
    target = next(row for row in precision_sources["rows"] if row["target_id"] == "H-1S-2S-CENTROID")
    r_h = codata["constants"]["R_H"]["value"]
    predicted_hz = SPEED_OF_LIGHT_M_PER_S * r_h * (1.0 - 1.0 / 4.0)
    observed_hz = float(target["value"])
    residual_hz = predicted_hz - observed_hz
    residual_ppm = abs(residual_hz) / observed_hz * 1e6
    uncertainty_hz = float(target.get("uncertainty", 0.0))
    sigma_offset = abs(residual_hz) / uncertainty_hz if uncertainty_hz else None
    return {
        "schema_version": "1.0",
        "role": "hydrogen_precision_nonrelativistic_baseline_gate",
        "status": "BASELINE_COMPUTED_MODEL_INCOMPLETE",
        "claim_class": "nonrelativistic_baseline_only_no_precision_validation",
        "formula_id": "AT20-HYDROGEN-1S2S-RYDBERG-BASELINE",
        "target_id": target["target_id"],
        "formula": "nu_1S_2S = c * R_H * (1 - 1/4)",
        "constants": {
            "speed_of_light_m_per_s": SPEED_OF_LIGHT_M_PER_S,
            "R_H_m_inverse": r_h,
        },
        "observed": {
            "value_hz": observed_hz,
            "uncertainty_hz": uncertainty_hz,
            "source_type": target["source_type"],
            "doi": target.get("doi"),
            "url": target.get("url"),
        },
        "prediction": {
            "nonrelativistic_rydberg_baseline_hz": predicted_hz,
            "residual_hz": residual_hz,
            "absolute_residual_hz": abs(residual_hz),
            "residual_ppm": residual_ppm,
            "sigma_offset_vs_measurement_uncertainty": sigma_offset,
        },
        "required_to_close_precision": [
            "Dirac fine-structure expansion for level energies",
            "reduced-mass and recoil correction convention audit",
            "radiative/QED Lamb-shift contribution",
            "finite proton-size contribution",
            "uncertainty propagation and residual threshold",
            "independent source locators for all precision rows",
        ],
        "limitations": [
            "This computes only the standard nonrelativistic Rydberg baseline for the 1S-2S centroid.",
            "The residual is expected to remain open because precision corrections are intentionally excluded.",
            "This gate cannot be cited as fine-structure, Lamb-shift, hyperfine, QED, or UET first-principles validation.",
        ],
    }


def _hydrogen_dirac_expansion_level_frequency_hz(n: int, j: float, r_h: float, alpha: float) -> float:
    correction = (alpha**2 / n) * (1.0 / (j + 0.5) - 3.0 / (4.0 * n))
    return -SPEED_OF_LIGHT_M_PER_S * r_h / (n**2) * (1.0 + correction)


def build_precision_dirac_baseline_gate(precision_sources: dict, codata: dict) -> dict:
    """Add the leading Dirac/fine-structure level correction for the sourced 1S-2S target."""
    target = next(row for row in precision_sources["rows"] if row["target_id"] == "H-1S-2S-CENTROID")
    r_h = codata["constants"]["R_H"]["value"]
    alpha = codata["constants"]["alpha"]["value"]
    level_1s_hz = _hydrogen_dirac_expansion_level_frequency_hz(1, 0.5, r_h, alpha)
    level_2s_hz = _hydrogen_dirac_expansion_level_frequency_hz(2, 0.5, r_h, alpha)
    predicted_hz = level_2s_hz - level_1s_hz
    observed_hz = float(target["value"])
    residual_hz = predicted_hz - observed_hz
    residual_ppm = abs(residual_hz) / observed_hz * 1e6
    uncertainty_hz = float(target.get("uncertainty", 0.0))
    sigma_offset = abs(residual_hz) / uncertainty_hz if uncertainty_hz else None
    return {
        "schema_version": "1.0",
        "role": "hydrogen_precision_dirac_fine_structure_baseline_gate",
        "status": "DIRAC_BASELINE_COMPUTED_QED_INCOMPLETE",
        "claim_class": "dirac_baseline_only_no_qed_precision_validation",
        "formula_id": "AT20-HYDROGEN-1S2S-DIRAC-BASELINE",
        "target_id": target["target_id"],
        "formula": "E_nj/h = -c R_H/n^2 * [1 + alpha^2/n * (1/(j+1/2) - 3/(4n))]",
        "levels": [
            {"label": "1S1/2", "n": 1, "j": 0.5, "level_frequency_hz": level_1s_hz},
            {"label": "2S1/2", "n": 2, "j": 0.5, "level_frequency_hz": level_2s_hz},
        ],
        "constants": {
            "speed_of_light_m_per_s": SPEED_OF_LIGHT_M_PER_S,
            "R_H_m_inverse": r_h,
            "alpha": alpha,
        },
        "observed": {
            "value_hz": observed_hz,
            "uncertainty_hz": uncertainty_hz,
            "source_type": target["source_type"],
            "doi": target.get("doi"),
            "url": target.get("url"),
        },
        "prediction": {
            "dirac_fine_structure_baseline_hz": predicted_hz,
            "residual_hz": residual_hz,
            "absolute_residual_hz": abs(residual_hz),
            "residual_ppm": residual_ppm,
            "sigma_offset_vs_measurement_uncertainty": sigma_offset,
        },
        "required_to_close_precision": [
            "full reduced-mass/recoil convention audit beyond R_H substitution",
            "radiative/QED Lamb-shift contribution for 1S and 2S",
            "finite proton-size contribution",
            "uncertainty propagation and residual threshold",
            "independent source locators for all precision rows",
        ],
        "limitations": [
            "This computes a leading Dirac/fine-structure expansion baseline for the 1S-2S centroid.",
            "It intentionally excludes Lamb-shift, radiative/QED, recoil beyond R_H, and finite-proton-size terms.",
            "This gate cannot be cited as Lamb-shift, hyperfine, QED, or UET first-principles validation.",
        ],
    }


def build_lamb_shift_handoff_gate(lamb_sources: dict, precision_dirac_baseline_gate: dict) -> dict:
    """Apply source-referenced Lamb shifts as an empirical handoff, not as a QED derivation."""
    rows = {row["target_id"]: row for row in lamb_sources["rows"]}
    lamb_1s_mhz = float(rows["H-1S-LAMB-SHIFT"]["value"])
    lamb_2s_mhz = float(rows["H-2S-LAMB-SHIFT"]["value"])
    lamb_1s_unc_mhz = float(rows["H-1S-LAMB-SHIFT"].get("uncertainty", 0.0))
    lamb_2s_unc_mhz = float(rows["H-2S-LAMB-SHIFT"].get("uncertainty", 0.0))
    lamb_delta_hz = (lamb_2s_mhz - lamb_1s_mhz) * 1e6
    lamb_delta_uncertainty_hz = ((lamb_1s_unc_mhz**2 + lamb_2s_unc_mhz**2) ** 0.5) * 1e6
    observed_hz = precision_dirac_baseline_gate["observed"]["value_hz"]
    dirac_baseline_hz = precision_dirac_baseline_gate["prediction"]["dirac_fine_structure_baseline_hz"]
    empirical_handoff_hz = dirac_baseline_hz + lamb_delta_hz
    residual_hz = empirical_handoff_hz - observed_hz
    residual_ppm = abs(residual_hz) / observed_hz * 1e6
    return {
        "schema_version": "1.0",
        "role": "hydrogen_lamb_shift_empirical_handoff_gate",
        "status": "EMPIRICAL_LAMB_HANDOFF_COMPUTED_MODEL_INCOMPLETE",
        "claim_class": "empirical_lamb_handoff_only_no_qed_validation",
        "formula_id": "AT20-HYDROGEN-1S2S-LAMB-HANDOFF",
        "formula": "nu_1S_2S_handoff = nu_Dirac_baseline + (L_2S - L_1S)",
        "source_status": lamb_sources["status"],
        "source_rows": [
            {
                "target_id": row["target_id"],
                "observable": row["observable"],
                "value": row["value"],
                "uncertainty": row.get("uncertainty"),
                "unit": row["unit"],
                "source_type": row["source_type"],
                "url": row["url"],
            }
            for row in lamb_sources["rows"]
        ],
        "correction": {
            "L_1S_MHz": lamb_1s_mhz,
            "L_2S_MHz": lamb_2s_mhz,
            "delta_L_2S_minus_1S_Hz": lamb_delta_hz,
            "delta_uncertainty_hz": lamb_delta_uncertainty_hz,
        },
        "prediction": {
            "dirac_baseline_hz": dirac_baseline_hz,
            "empirical_lamb_handoff_hz": empirical_handoff_hz,
            "observed_hz": observed_hz,
            "residual_hz": residual_hz,
            "absolute_residual_hz": abs(residual_hz),
            "residual_ppm": residual_ppm,
        },
        "required_to_close_precision": lamb_sources["required_model_components"],
        "limitations": [
            "This applies source-referenced Lamb-shift values as an empirical residual-sizing handoff.",
            "It is not a QED derivation and does not decompose self-energy, vacuum polarization, recoil, or proton-size terms.",
            "The 2S value uses a 2S-2P Lamb-shift convention and needs a term-convention audit before precision validation.",
            "This gate cannot be cited as QED, proton-radius, hyperfine, or UET first-principles validation.",
        ],
        "claim_boundary": lamb_sources["claim_boundary"],
    }


def build_hyperfine_21cm_gate(hyperfine_sources: dict, precision_sources: dict) -> dict:
    """Source-lock the 21 cm target and compute wavelength bookkeeping only."""
    recommended = hyperfine_sources["recommended_transition"]
    metrology = hyperfine_sources["metrology_cross_check"]
    precision_row = next(row for row in precision_sources["rows"] if row["target_id"] == "H-21CM-HYPERFINE")
    recommended_hz = float(recommended["value"]) * 1e6
    precision_row_hz = float(precision_row["value"]) * 1e6
    metrology_hz = float(metrology["value"])
    wavelength_m = SPEED_OF_LIGHT_M_PER_S / recommended_hz
    wavelength_cm = wavelength_m * 100.0
    metrology_delta_hz = metrology_hz - recommended_hz
    precision_row_delta_hz = precision_row_hz - recommended_hz
    return {
        "schema_version": "1.0",
        "role": "hydrogen_21cm_hyperfine_source_gate",
        "status": "SOURCE_READY_MODEL_BLOCKED",
        "claim_class": "source_locked_hyperfine_target_no_hamiltonian_validation",
        "formula_id": "AT20-HYDROGEN-21CM-HYPERFINE-SOURCE-GATE",
        "formula": "lambda_21cm = c / nu_hfs",
        "source_status": hyperfine_sources["status"],
        "recommended_frequency": {
            "value_hz": recommended_hz,
            "value_mhz": recommended["value"],
            "source_type": recommended["source_type"],
            "url": recommended["url"],
        },
        "metrology_cross_check": {
            "value_hz": metrology_hz,
            "uncertainty_hz": metrology.get("uncertainty"),
            "delta_vs_recommended_hz": metrology_delta_hz,
            "source_type": metrology["source_type"],
            "url": metrology["url"],
        },
        "topic_precision_row_delta": {
            "existing_precision_row_hz": precision_row_hz,
            "recommended_hz": recommended_hz,
            "delta_hz": precision_row_delta_hz,
        },
        "derived_bookkeeping": {
            "wavelength_m": wavelength_m,
            "wavelength_cm": wavelength_cm,
        },
        "required_to_close_hyperfine": hyperfine_sources["required_model_components"],
        "limitations": [
            "This gate source-locks the 21 cm target and computes wavelength bookkeeping only.",
            "It does not compute the Fermi-contact hyperfine Hamiltonian or magnetic-moment terms.",
            "It does not validate QED, recoil, finite-proton-structure, or UET first-principles hyperfine corrections.",
        ],
        "claim_boundary": hyperfine_sources["claim_boundary"],
    }


def build_hyperfine_fermi_baseline_gate(hyperfine_21cm_gate: dict, fermi_constants: dict, codata: dict) -> dict:
    """Compute the leading Fermi-contact hyperfine baseline."""
    constants = codata["constants"]
    alpha = constants["alpha"]["value"]
    r_infinity = constants["R_infinity"]["value"]
    electron_mass = constants["m_e"]["value"]
    proton_mass = constants["m_p"]["value"]
    proton_g_factor = fermi_constants["constants"]["proton_g_factor"]["value"]
    predicted_hz = (
        (8.0 / 3.0)
        * alpha**2
        * SPEED_OF_LIGHT_M_PER_S
        * r_infinity
        * (electron_mass / proton_mass)
        * proton_g_factor
    )
    observed_hz = hyperfine_21cm_gate["recommended_frequency"]["value_hz"]
    residual_hz = predicted_hz - observed_hz
    residual_ppm = abs(residual_hz) / observed_hz * 1e6
    return {
        "schema_version": "1.0",
        "role": "hydrogen_21cm_fermi_contact_baseline_gate",
        "status": "FERMI_BASELINE_COMPUTED_CORRECTIONS_OPEN",
        "claim_class": "fermi_contact_baseline_only_no_precision_hyperfine_validation",
        "formula_id": fermi_constants["formula"]["id"],
        "formula": fermi_constants["formula"]["expression"],
        "constants": {
            "alpha": alpha,
            "R_infinity_m_inverse": r_infinity,
            "electron_mass_kg": electron_mass,
            "proton_mass_kg": proton_mass,
            "proton_g_factor": proton_g_factor,
            "speed_of_light_m_per_s": SPEED_OF_LIGHT_M_PER_S,
        },
        "prediction": {
            "fermi_contact_baseline_hz": predicted_hz,
            "observed_reference_hz": observed_hz,
            "residual_hz": residual_hz,
            "absolute_residual_hz": abs(residual_hz),
            "residual_ppm": residual_ppm,
        },
        "required_to_close_hyperfine": [
            "mass and magnetic-moment convention audit",
            "reduced-mass/recoil correction",
            "radiative/QED correction",
            "finite proton-structure correction",
            "weak-interaction and higher-order correction policy",
            "uncertainty propagation and residual threshold",
        ],
        "limitations": fermi_constants["formula"]["limitations"],
        "claim_boundary": fermi_constants["claim_boundary"],
    }


def build_helium_many_electron_gate(helium_sources: dict) -> dict:
    rows = helium_sources["neutral_helium_lines"]
    return {
        "schema_version": "1.0",
        "role": "neutral_helium_many_electron_source_gate",
        "status": "SOURCE_READY_MODEL_BLOCKED",
        "claim_class": "source_package_only_no_many_electron_validation",
        "source_row_count": len(rows),
        "source": helium_sources["source"],
        "targets": [
            {
                "species": row["species"],
                "wavelength_nm": row["wavelength_nm"],
                "relative_intensity": row["relative_intensity"],
                "role": row["role"],
                "source_status": row["source_status"],
            }
            for row in rows
        ],
        "required_model_components": helium_sources["required_model_components"],
        "blocked_usages": helium_sources["blocked_usages"],
        "limitations": [
            "No neutral-helium wavelength residual is computed in this gate.",
            "The package prepares many-electron source targets only.",
            "A two-electron Hamiltonian, correlation treatment, line-component/blend policy, and uncertainty policy are required before validation.",
            "This gate cannot be cited as neutral-helium, many-electron, or periodic-table spectral validation.",
        ],
        "claim_boundary": helium_sources["claim_boundary"],
    }


def _nearest_helium_assignment(wavelength_nm: float, assignments: list[dict]) -> tuple[dict | None, float | None]:
    if not assignments:
        return None, None
    nearest = min(assignments, key=lambda row: abs(row["matching_source_target_nm"] - wavelength_nm))
    delta_nm = nearest["matching_source_target_nm"] - wavelength_nm
    if abs(delta_nm) <= 0.001:
        return nearest, delta_nm
    return None, delta_nm


def build_helium_transition_assignment_gap_gate(helium_sources: dict, helium_assignments: dict) -> dict:
    rows = helium_sources["neutral_helium_lines"]
    assignments = helium_assignments["assignments"]
    target_rows = []
    for row in rows:
        wavelength_nm = float(row["wavelength_nm"])
        frequency_hz = SPEED_OF_LIGHT_M_PER_S / (wavelength_nm * 1e-9)
        photon_energy_ev = PLANCK_EV_S * frequency_hz
        assignment, assignment_delta_nm = _nearest_helium_assignment(wavelength_nm, assignments)
        if assignment:
            level_delta_cm_inverse = assignment["upper_energy_cm_inverse"] - assignment["lower_energy_cm_inverse"]
            transition_assignment_status = assignment["assignment_status"]
            assignment_payload = {
                "matched_assignment_wavelength_nm": assignment["wavelength_nm"],
                "matching_delta_nm": assignment_delta_nm,
                "lower_energy_cm_inverse": assignment["lower_energy_cm_inverse"],
                "upper_energy_cm_inverse": assignment["upper_energy_cm_inverse"],
                "level_delta_cm_inverse": level_delta_cm_inverse,
                "lower_configuration": assignment["lower_configuration"],
                "lower_term": assignment["lower_term"],
                "lower_j": assignment["lower_j"],
                "upper_configuration": assignment["upper_configuration"],
                "upper_term": assignment["upper_term"],
                "upper_j": assignment["upper_j"],
                "source_locator": assignment["source_locator"],
            }
            if "component_policy" in assignment:
                assignment_payload["component_policy"] = assignment["component_policy"]
        else:
            transition_assignment_status = "missing_term_labels_and_upper_lower_states"
            assignment_payload = {
                "nearest_assignment_delta_nm": assignment_delta_nm,
            }
        target_rows.append(
            {
                "species": row["species"],
                "wavelength_nm": wavelength_nm,
                "relative_intensity": row["relative_intensity"],
                "photon_energy_ev": photon_energy_ev,
                "source_status": row["source_status"],
                "transition_assignment_status": transition_assignment_status,
                "assignment": assignment_payload,
            }
        )
    energies = [row["photon_energy_ev"] for row in target_rows]
    assigned_count = sum(1 for row in target_rows if row["transition_assignment_status"].startswith("assigned"))
    missing_count = len(target_rows) - assigned_count
    gate_status = (
        "SOURCE_ASSIGNMENTS_READY_MODEL_BLOCKED"
        if missing_count == 0
        else "PARTIAL_TERM_ASSIGNMENTS_READY_MODEL_BLOCKED"
    )
    source_readiness = (
        "source_assignments_ready_model_blocked"
        if missing_count == 0
        else "partial_term_assignments_ready_model_blocked"
    )
    blocked_requirements = [
        "two-electron Hamiltonian/correlation model",
        "transition selection-rule policy",
        "uncertainty propagation and residual thresholds",
    ]
    if missing_count:
        blocked_requirements.insert(0, "remaining source term labels for unassigned rows")
    return {
        "schema_version": "1.0",
        "role": "neutral_helium_transition_assignment_gap_gate",
        "status": gate_status,
        "source_evidence_readiness": source_readiness,
        "claim_class": "photon_energy_source_diagnostic_only_no_helium_validation",
        "formula_id": "AT20-HELIUM-PHOTON-ENERGY-GAP",
        "formula": "E_photon = h c / lambda",
        "assignment_source": helium_assignments["source"],
        "constants": {
            "speed_of_light_m_per_s": SPEED_OF_LIGHT_M_PER_S,
            "planck_constant_ev_s": PLANCK_EV_S,
        },
        "metrics": {
            "source_row_count": len(target_rows),
            "min_photon_energy_ev": min(energies),
            "max_photon_energy_ev": max(energies),
            "energy_span_ev": max(energies) - min(energies),
            "rows_with_transition_assignment": assigned_count,
            "rows_missing_transition_assignment": missing_count,
        },
        "targets": target_rows,
        "blocked_residual_model_requirements": blocked_requirements,
        "limitations": [
            "This gate computes photon energies from source wavelengths only.",
            "It cannot compute neutral-helium residuals until uncertainty propagation and a residual model are present.",
            "It is not a hydrogenic, two-electron, correlation, fine-structure, QED, or UET validation artifact.",
        ],
        "claim_boundary": helium_assignments["claim_boundary"],
    }


def build_helium_medium_normalization_gate(helium_transition_assignment_gap_gate: dict) -> dict:
    normalized_rows = []
    for row in helium_transition_assignment_gap_gate["targets"]:
        assignment = row["assignment"]
        if "level_delta_cm_inverse" not in assignment:
            continue
        level_delta_cm_inverse = assignment["level_delta_cm_inverse"]
        source_air_nm = row["wavelength_nm"]
        vacuum_equivalent_nm = 1.0e7 / level_delta_cm_inverse
        air_to_vacuum_factor = vacuum_equivalent_nm / source_air_nm
        air_vacuum_delta_nm = vacuum_equivalent_nm - source_air_nm
        normalized_rows.append(
            {
                "species": row["species"],
                "source_air_wavelength_nm": source_air_nm,
                "vacuum_equivalent_wavelength_nm_from_level_delta": vacuum_equivalent_nm,
                "air_to_vacuum_factor_from_source_and_levels": air_to_vacuum_factor,
                "air_vacuum_delta_nm": air_vacuum_delta_nm,
                "level_delta_cm_inverse": level_delta_cm_inverse,
                "transition_assignment_status": row["transition_assignment_status"],
                "source_locator": assignment["source_locator"],
            }
        )
    factors = [row["air_to_vacuum_factor_from_source_and_levels"] for row in normalized_rows]
    deltas = [row["air_vacuum_delta_nm"] for row in normalized_rows]
    complete = len(normalized_rows) == helium_transition_assignment_gap_gate["metrics"]["source_row_count"]
    plausible_factors = all(1.00020 <= factor <= 1.00035 for factor in factors)
    status = (
        "SOURCE_MEDIUM_NORMALIZATION_READY_MODEL_BLOCKED"
        if complete and plausible_factors
        else "MEDIUM_NORMALIZATION_REVIEW_REQUIRED"
    )
    return {
        "schema_version": "1.0",
        "role": "neutral_helium_wavelength_medium_normalization_gate",
        "status": status,
        "claim_class": "source_normalization_diagnostic_only_no_helium_validation",
        "formula_id": "AT20-HELIUM-MEDIUM-NORMALIZATION-GAP",
        "formula": "lambda_vacuum_nm = 1e7 / DeltaE_cm^-1; source visible wavelengths are treated as air wavelengths",
        "source_basis": "NIST ASD/handbook visible helium rows list air wavelengths; level-energy differences provide vacuum-equivalent wavenumber bookkeeping.",
        "metrics": {
            "source_row_count": helium_transition_assignment_gap_gate["metrics"]["source_row_count"],
            "normalized_row_count": len(normalized_rows),
            "rows_missing_normalization": helium_transition_assignment_gap_gate["metrics"]["source_row_count"]
            - len(normalized_rows),
            "min_air_to_vacuum_factor": min(factors) if factors else None,
            "max_air_to_vacuum_factor": max(factors) if factors else None,
            "min_air_vacuum_delta_nm": min(deltas) if deltas else None,
            "max_air_vacuum_delta_nm": max(deltas) if deltas else None,
        },
        "targets": normalized_rows,
        "blocked_residual_model_requirements": [
            "two-electron Hamiltonian/correlation model",
            "selection-rule and line-component/blend policy",
            "uncertainty propagation and residual thresholds",
        ],
        "limitations": [
            "This gate normalizes source wavelength medium using source level-energy differences only.",
            "It does not compute predicted helium energy levels from a Hamiltonian.",
            "It is not a neutral-helium validation or many-electron validation artifact.",
        ],
        "claim_boundary": "This gate supports wavelength-medium bookkeeping for selected He I rows only. It does not validate neutral-helium spectral prediction, electron correlation, or UET first-principles atomic theory.",
    }


def _term_multiplicity(term: str) -> str | None:
    match = re.match(r"(\d+)", term)
    return match.group(1) if match else None


def _term_has_odd_parity(term: str) -> bool:
    return "*" in term


def _e1_selection_status(lower_term: str, lower_j: int, upper_term: str, upper_j: int) -> str:
    same_spin = _term_multiplicity(lower_term) == _term_multiplicity(upper_term)
    parity_changes = _term_has_odd_parity(lower_term) != _term_has_odd_parity(upper_term)
    delta_j = abs(upper_j - lower_j)
    allowed_delta_j = delta_j <= 1 and not (lower_j == 0 and upper_j == 0)
    return "E1_ALLOWED_BY_TERM_POLICY" if same_spin and parity_changes and allowed_delta_j else "REVIEW_REQUIRED"


def build_helium_line_component_policy_gate(helium_transition_assignment_gap_gate: dict) -> dict:
    policy_rows = []
    total_components = 0
    allowed_components = 0
    blend_rows = 0
    for row in helium_transition_assignment_gap_gate["targets"]:
        assignment = row["assignment"]
        if "lower_term" not in assignment:
            policy_rows.append(
                {
                    "species": row["species"],
                    "source_wavelength_nm": row["wavelength_nm"],
                    "policy_status": "MISSING_ASSIGNMENT",
                    "component_count": 0,
                }
            )
            continue
        component_policy = assignment.get("component_policy")
        if component_policy:
            components = component_policy["components"]
            line_structure = component_policy["line_structure"]
            representative_component_rule = component_policy["representative_component_rule"]
            blend_rows += 1
        else:
            components = [
                {
                    "lower_j": assignment["lower_j"],
                    "upper_j": assignment["upper_j"],
                    "lower_energy_cm_inverse": assignment["lower_energy_cm_inverse"],
                    "upper_energy_cm_inverse": assignment["upper_energy_cm_inverse"],
                    "aki_s_inverse": None,
                    "ritz_air_wavelength_angstrom": None,
                }
            ]
            line_structure = "single_component_source_row"
            representative_component_rule = "source row is treated as a single selected component"
        component_checks = []
        for component in components:
            status = _e1_selection_status(
                assignment["lower_term"],
                int(component["lower_j"]),
                assignment["upper_term"],
                int(component["upper_j"]),
            )
            total_components += 1
            if status == "E1_ALLOWED_BY_TERM_POLICY":
                allowed_components += 1
            component_checks.append(
                {
                    "lower_j": component["lower_j"],
                    "upper_j": component["upper_j"],
                    "delta_j": abs(int(component["upper_j"]) - int(component["lower_j"])),
                    "selection_status": status,
                    "aki_s_inverse": component.get("aki_s_inverse"),
                    "ritz_air_wavelength_angstrom": component.get("ritz_air_wavelength_angstrom"),
                }
            )
        row_status = (
            "SOURCE_COMPONENT_POLICY_READY"
            if all(component["selection_status"] == "E1_ALLOWED_BY_TERM_POLICY" for component in component_checks)
            else "COMPONENT_POLICY_REVIEW_REQUIRED"
        )
        policy_rows.append(
            {
                "species": row["species"],
                "source_wavelength_nm": row["wavelength_nm"],
                "line_structure": line_structure,
                "representative_component_rule": representative_component_rule,
                "lower_term": assignment["lower_term"],
                "upper_term": assignment["upper_term"],
                "spin_policy": "same_multiplicity_required_for_this_E1_source_policy",
                "parity_policy": "odd/even parity change required for this E1 source policy",
                "component_count": len(components),
                "policy_status": row_status,
                "component_checks": component_checks,
                "source_locator": assignment["source_locator"],
            }
        )
    rows_ready = sum(1 for row in policy_rows if row["policy_status"] == "SOURCE_COMPONENT_POLICY_READY")
    status = (
        "SOURCE_COMPONENT_POLICY_READY_MODEL_BLOCKED"
        if rows_ready == helium_transition_assignment_gap_gate["metrics"]["source_row_count"]
        else "COMPONENT_POLICY_REVIEW_REQUIRED"
    )
    return {
        "schema_version": "1.0",
        "role": "neutral_helium_line_component_policy_gate",
        "status": status,
        "claim_class": "source_line_component_policy_only_no_helium_validation",
        "formula_id": "AT20-HELIUM-LINE-COMPONENT-POLICY-GAP",
        "selection_rule_policy": "E1 source-policy check: same spin multiplicity, parity change, and Delta J in {0,1} excluding 0->0.",
        "metrics": {
            "source_row_count": helium_transition_assignment_gap_gate["metrics"]["source_row_count"],
            "rows_with_component_policy": rows_ready,
            "rows_missing_component_policy": helium_transition_assignment_gap_gate["metrics"]["source_row_count"] - rows_ready,
            "blend_rows": blend_rows,
            "total_components_checked": total_components,
            "e1_allowed_components": allowed_components,
            "component_policy_review_required": total_components - allowed_components,
        },
        "targets": policy_rows,
        "blocked_residual_model_requirements": [
            "two-electron Hamiltonian/correlation model",
            "uncertainty propagation and residual thresholds",
            "resolved line-shape or intensity-weighted blend model for precision residuals",
        ],
        "limitations": [
            "This gate checks source line-component bookkeeping and basic E1 selection-rule consistency only.",
            "It does not calculate transition amplitudes, oscillator strengths, or helium energy levels from a Hamiltonian.",
            "Blend policy is sufficient for source bookkeeping, not for precision line-shape validation.",
        ],
        "claim_boundary": "This gate supports line-component source policy for selected He I rows only. It does not validate neutral-helium spectral prediction, electron correlation, or UET first-principles atomic theory.",
    }


def build_helium_ground_state_baseline_gate(helium_ground_sources: dict, codata: dict) -> dict:
    rows_by_quantity = {row["quantity"]: row for row in helium_ground_sources["rows"]}
    first_ie = rows_by_quantity["first_ionization_energy"]
    second_ie = rows_by_quantity["second_ionization_energy"]
    observed_total_binding_ev = first_ie["value_eV"] + second_ie["value_eV"]
    observed_uncertainty_ev = (first_ie["uncertainty_eV"] ** 2 + second_ie["uncertainty_eV"] ** 2) ** 0.5
    hartree_ev = codata["constants"]["E_h"]["value"] / ELEMENTARY_CHARGE_C

    independent_binding_ev = 2.0 * second_ie["value_eV"]
    independent_residual_ev = independent_binding_ev - observed_total_binding_ev
    independent_residual_percent = independent_residual_ev / observed_total_binding_ev * 100.0

    z = 2.0
    zeta_opt = z - 5.0 / 16.0
    variational_total_energy_hartree = zeta_opt**2 - 2.0 * z * zeta_opt + 5.0 * zeta_opt / 8.0
    variational_binding_ev = -variational_total_energy_hartree * hartree_ev
    variational_residual_ev = variational_binding_ev - observed_total_binding_ev
    variational_residual_percent = variational_residual_ev / observed_total_binding_ev * 100.0
    correlated_reference = helium_ground_sources["correlated_reference"]
    correlated_reference_binding_ev = -correlated_reference["energy_hartree"] * hartree_ev
    correlated_minus_observed_ev = correlated_reference_binding_ev - observed_total_binding_ev
    variational_gap_to_correlated_ev = correlated_reference_binding_ev - variational_binding_ev
    independent_gap_to_correlated_ev = correlated_reference_binding_ev - independent_binding_ev

    return {
        "schema_version": "1.0",
        "role": "neutral_helium_ground_state_two_electron_baseline_gate",
        "status": "BASELINE_RESIDUAL_COMPUTED_CORRELATION_MODEL_BLOCKED",
        "claim_class": "diagnostic_two_electron_baseline_only_no_helium_validation",
        "formula_ids": [
            "AT20-HELIUM-INDEPENDENT-ELECTRON-BASELINE",
            "AT20-HELIUM-VARIATIONAL-ZETA-BASELINE",
        ],
        "source": helium_ground_sources["source"],
        "correlated_reference": {
            "method": correlated_reference["method"],
            "state": correlated_reference["state"],
            "energy_hartree": correlated_reference["energy_hartree"],
            "binding_energy_eV_from_codata_hartree": correlated_reference_binding_ev,
            "binding_minus_observed_total_binding_eV": correlated_minus_observed_ev,
            "source": correlated_reference["source"],
            "claim_role": correlated_reference["claim_role"],
        },
        "observed_anchor": {
            "first_ionization_energy_eV": first_ie["value_eV"],
            "second_ionization_energy_eV": second_ie["value_eV"],
            "total_binding_energy_eV": observed_total_binding_ev,
            "total_binding_uncertainty_eV": observed_uncertainty_ev,
            "source_policy": "Neutral helium total binding is IE1(He I) + IE2(He II) from the NIST ASD ionization-energy query.",
        },
        "constants": {
            "hartree_energy_eV": hartree_ev,
            "elementary_charge_C_exact": ELEMENTARY_CHARGE_C,
        },
        "baselines": [
            {
                "baseline_id": "independent_hydrogenic_Z2_no_electron_electron_repulsion",
                "formula": "E_bind = 2 * IE2(He II)",
                "predicted_total_binding_eV": independent_binding_ev,
                "residual_eV_predicted_minus_observed": independent_residual_ev,
                "absolute_residual_eV": abs(independent_residual_ev),
                "residual_percent": independent_residual_percent,
                "gap_to_correlated_reference_eV": independent_gap_to_correlated_ev,
                "interpretation": "Overbinds because it treats both electrons as independent Z=2 hydrogenic electrons and omits electron-electron repulsion/screening.",
            },
            {
                "baseline_id": "uncorrelated_variational_effective_charge_1s2",
                "formula": "E(zeta) = zeta^2 - 2 Z zeta + (5/8) zeta Hartree; zeta = Z - 5/16",
                "z": z,
                "zeta_opt": zeta_opt,
                "predicted_total_energy_hartree": variational_total_energy_hartree,
                "predicted_total_binding_eV": variational_binding_ev,
                "residual_eV_predicted_minus_observed": variational_residual_ev,
                "absolute_residual_eV": abs(variational_residual_ev),
                "residual_percent": variational_residual_percent,
                "gap_to_correlated_reference_eV": variational_gap_to_correlated_ev,
                "interpretation": "Captures a first electron-electron repulsion/screening correction but remains an uncorrelated 1s^2 variational baseline.",
            },
        ],
        "correlation_gap_summary": {
            "independent_baseline_gap_to_correlated_reference_eV": independent_gap_to_correlated_ev,
            "variational_baseline_gap_to_correlated_reference_eV": variational_gap_to_correlated_ev,
            "correlated_reference_minus_observed_eV": correlated_minus_observed_ev,
            "interpretation": "The correlated reference is a nonrelativistic infinite-nuclear-mass target, while the observed ionization-energy anchor includes finite-mass, relativistic, QED, and experimental conventions; the difference is diagnostic only.",
        },
        "blocked_residual_model_requirements": [
            "correlated two-electron wavefunction or configuration-interaction basis",
            "singlet/triplet excited-state Hamiltonian residuals",
            "relativistic and QED correction policy",
            "uncertainty propagation and pass/fail thresholds",
        ],
        "limitations": [
            "This is a ground-state baseline diagnostic, not a neutral-helium spectral validation.",
            "The independent-electron baseline intentionally fails as a missing-interaction diagnostic.",
            "The variational effective-charge baseline is uncorrelated and cannot predict the visible transition set by itself.",
            "No UET-specific derivation of the two-electron Hamiltonian is supplied here.",
        ],
        "claim_boundary": helium_ground_sources["claim_boundary"],
    }


def build_helium_excited_state_target_gate(
    helium_transition_assignment_gap_gate: dict,
    helium_ground_state_baseline_gate: dict,
) -> dict:
    levels = {}
    transitions = []
    observed_total_binding_ev = helium_ground_state_baseline_gate["observed_anchor"]["total_binding_energy_eV"]
    correlated_reference_binding_ev = helium_ground_state_baseline_gate["correlated_reference"][
        "binding_energy_eV_from_codata_hartree"
    ]

    for row in helium_transition_assignment_gap_gate["targets"]:
        assignment = row["assignment"]
        if "level_delta_cm_inverse" not in assignment:
            continue
        for prefix in ("lower", "upper"):
            key = (
                assignment[f"{prefix}_configuration"],
                assignment[f"{prefix}_term"],
                assignment[f"{prefix}_j"],
                assignment[f"{prefix}_energy_cm_inverse"],
            )
            excitation_ev = assignment[f"{prefix}_energy_cm_inverse"] * EV_PER_CM_INVERSE
            levels[key] = {
                "configuration": assignment[f"{prefix}_configuration"],
                "term": assignment[f"{prefix}_term"],
                "j": assignment[f"{prefix}_j"],
                "excitation_energy_cm_inverse": assignment[f"{prefix}_energy_cm_inverse"],
                "excitation_energy_eV": excitation_ev,
                "binding_from_observed_anchor_eV": observed_total_binding_ev - excitation_ev,
                "binding_from_correlated_reference_eV": correlated_reference_binding_ev - excitation_ev,
            }
        level_delta_ev = assignment["level_delta_cm_inverse"] * EV_PER_CM_INVERSE
        transition_residual_ev = level_delta_ev - row["photon_energy_ev"]
        transitions.append(
            {
                "source_wavelength_nm_air": row["wavelength_nm"],
                "transition_assignment_status": row["transition_assignment_status"],
                "level_delta_cm_inverse": assignment["level_delta_cm_inverse"],
                "level_delta_eV": level_delta_ev,
                "air_wavelength_photon_energy_eV": row["photon_energy_ev"],
                "level_delta_minus_air_photon_eV": transition_residual_ev,
                "lower_label": f"{assignment['lower_configuration']} {assignment['lower_term']} J={assignment['lower_j']}",
                "upper_label": f"{assignment['upper_configuration']} {assignment['upper_term']} J={assignment['upper_j']}",
                "source_locator": assignment["source_locator"],
            }
        )

    level_rows = sorted(
        levels.values(),
        key=lambda item: (item["excitation_energy_cm_inverse"], item["configuration"], item["term"], item["j"]),
    )
    excitation_values = [row["excitation_energy_eV"] for row in level_rows]
    transition_residuals = [abs(row["level_delta_minus_air_photon_eV"]) for row in transitions]
    return {
        "schema_version": "1.0",
        "role": "neutral_helium_excited_state_target_gate",
        "status": "EXCITED_STATE_TARGETS_READY_MODEL_BLOCKED",
        "claim_class": "source_excited_state_targets_only_no_helium_validation",
        "formula_id": "AT20-HELIUM-EXCITED-STATE-TARGET-GAP",
        "formula": "E_excitation_eV = E_level_cm^-1 * h c; E_binding_target = E_ground_binding_anchor - E_excitation",
        "source_basis": "NIST term-level energies from selected He I transition assignments plus NIST ionization-energy and E-Hy-CI ground references.",
        "metrics": {
            "unique_level_count": len(level_rows),
            "transition_target_count": len(transitions),
            "min_excitation_energy_eV": min(excitation_values) if excitation_values else None,
            "max_excitation_energy_eV": max(excitation_values) if excitation_values else None,
            "max_air_photon_vs_level_delta_abs_eV": max(transition_residuals) if transition_residuals else None,
        },
        "ground_reference_context": {
            "observed_total_binding_energy_eV": observed_total_binding_ev,
            "correlated_reference_binding_energy_eV": correlated_reference_binding_ev,
            "correlated_reference_minus_observed_eV": helium_ground_state_baseline_gate["correlation_gap_summary"][
                "correlated_reference_minus_observed_eV"
            ],
        },
        "levels": level_rows,
        "transitions": transitions,
        "blocked_residual_model_requirements": [
            "correlated two-electron excited-state Hamiltonian model",
            "singlet/triplet and configuration-interaction basis policy",
            "finite-mass, relativistic, and QED correction convention",
            "uncertainty propagation and residual thresholds",
        ],
        "limitations": [
            "This gate prepares source target energies for excited states; it does not predict them.",
            "Binding targets depend on the selected ground-reference convention.",
            "Air photon-energy deltas are bookkeeping diagnostics; wavelength-medium-normalized residuals remain separate from model residuals.",
            "No UET-specific helium Hamiltonian derivation is supplied here.",
        ],
        "claim_boundary": "This gate supports excited-state target preparation only. It does not validate neutral-helium spectra, transition amplitudes, electron correlation, or UET first-principles atomic theory.",
    }


def parse_outer_principal_quantum_number(configuration: str) -> int | None:
    orbital_tokens = re.findall(r"(\d+)\s*[spdfgh]", configuration.replace(".", " "), flags=re.IGNORECASE)
    if not orbital_tokens:
        return None
    return int(orbital_tokens[-1])


def parse_outer_orbital_letter(configuration: str) -> str | None:
    orbital_tokens = re.findall(r"\d+\s*([spdfgh])", configuration.replace(".", " "), flags=re.IGNORECASE)
    if not orbital_tokens:
        return None
    return orbital_tokens[-1].upper()


def parse_term_multiplicity(term: str) -> str:
    match = re.match(r"(\d+)", term)
    return match.group(1) if match else "unknown"


def classify_nist_wavelength_medium_angstrom(wavelength_angstrom: float) -> str:
    if wavelength_angstrom < 2000.0:
        return "vacuum"
    if wavelength_angstrom <= 20000.0:
        return "standard_air"
    return "vacuum"


def build_helium_excited_hydrogenic_residual_gate(
    codata: dict,
    helium_ground_state_baseline_gate: dict,
    helium_excited_state_target_gate: dict,
) -> dict:
    first_ionization_ev = helium_ground_state_baseline_gate["observed_anchor"]["first_ionization_energy_eV"]
    r_infinity_ev = PLANCK_EV_S * SPEED_OF_LIGHT_M_PER_S * codata["constants"]["R_infinity"]["value"]
    rows = []

    for level in helium_excited_state_target_gate["levels"]:
        n_outer = parse_outer_principal_quantum_number(level["configuration"])
        if n_outer is None:
            rows.append(
                {
                    **level,
                    "outer_principal_quantum_number": None,
                    "baseline_status": "SKIPPED_CONFIGURATION_N_NOT_PARSED",
                }
            )
            continue

        observed_outer_binding_ev = first_ionization_ev - level["excitation_energy_eV"]
        zero_quantum_defect_binding_ev = r_infinity_ev / (n_outer**2)
        residual_ev = zero_quantum_defect_binding_ev - observed_outer_binding_ev
        effective_quantum_defect = (
            n_outer - (r_infinity_ev / observed_outer_binding_ev) ** 0.5
            if observed_outer_binding_ev > 0.0
            else None
        )
        rows.append(
            {
                **level,
                "outer_principal_quantum_number": n_outer,
                "observed_outer_binding_to_HeII_limit_eV": observed_outer_binding_ev,
                "zero_quantum_defect_hydrogenic_binding_eV": zero_quantum_defect_binding_ev,
                "residual_eV_predicted_minus_observed": residual_ev,
                "absolute_residual_eV": abs(residual_ev),
                "effective_quantum_defect_from_source_level": effective_quantum_defect,
                "baseline_status": "RESIDUAL_COMPUTED_MODEL_INCOMPLETE",
            }
        )

    computed_rows = [row for row in rows if row["baseline_status"] == "RESIDUAL_COMPUTED_MODEL_INCOMPLETE"]
    residuals = [row["absolute_residual_eV"] for row in computed_rows]
    quantum_defects = [
        row["effective_quantum_defect_from_source_level"]
        for row in computed_rows
        if row["effective_quantum_defect_from_source_level"] is not None
    ]
    return {
        "schema_version": "1.0",
        "role": "neutral_helium_excited_hydrogenic_residual_gate",
        "status": "HYDROGENIC_BASELINE_RESIDUAL_COMPUTED_CORRELATION_MODEL_BLOCKED",
        "claim_class": "diagnostic_single_active_electron_baseline_only_no_helium_validation",
        "formula_id": "AT20-HELIUM-ZERO-QUANTUM-DEFECT-BASELINE",
        "formula": "E_bind_pred = h c R_infinity / n^2; E_bind_observed = IE1(He I) - E_excitation",
        "source_basis": "NIST He I ionization limit plus NIST term-level excitation energies from selected transition assignments.",
        "metrics": {
            "computed_level_count": len(computed_rows),
            "skipped_level_count": len(rows) - len(computed_rows),
            "average_abs_binding_residual_eV": float(np.mean(residuals)) if residuals else None,
            "max_abs_binding_residual_eV": max(residuals) if residuals else None,
            "min_effective_quantum_defect": min(quantum_defects) if quantum_defects else None,
            "max_effective_quantum_defect": max(quantum_defects) if quantum_defects else None,
        },
        "constants": {
            "R_infinity_m_inverse": codata["constants"]["R_infinity"]["value"],
            "R_infinity_energy_eV": r_infinity_ev,
            "first_ionization_energy_eV": first_ionization_ev,
        },
        "levels": rows,
        "blocked_residual_model_requirements": [
            "source-backed singlet/triplet quantum-defect or configuration-interaction policy",
            "correlated two-electron excited-state Hamiltonian residuals",
            "transition-level residual thresholds separated from source wavelength-medium bookkeeping",
            "uncertainty propagation for term energies and ionization limit",
        ],
        "limitations": [
            "This baseline intentionally omits electron-core penetration, exchange, singlet/triplet splitting, and correlation.",
            "Large residuals and nonzero quantum defects are constraints for the next model, not evidence that the source targets are wrong.",
            "This gate still does not validate neutral-helium spectra or UET first-principles atomic theory.",
        ],
        "claim_boundary": "This gate supports only a diagnostic zero-quantum-defect residual baseline for selected He I excited levels. It cannot be cited as a helium spectral prediction or many-electron solution.",
    }


def build_helium_fixed_screening_baseline_gate(
    helium_excited_hydrogenic_residual_gate: dict,
) -> dict:
    """Fixed one-active-electron screening baseline; heuristic comparator, not CI."""
    r_infinity_ev = helium_excited_hydrogenic_residual_gate["constants"]["R_infinity_energy_eV"]
    screening_sigma_1s_core = 0.85
    nuclear_charge = 2.0
    fixed_outer_zeff = nuclear_charge - screening_sigma_1s_core
    rows = []

    for level in helium_excited_hydrogenic_residual_gate["levels"]:
        n_outer = level.get("outer_principal_quantum_number")
        if level.get("baseline_status") != "RESIDUAL_COMPUTED_MODEL_INCOMPLETE" or n_outer is None:
            rows.append(
                {
                    **level,
                    "fixed_screening_status": "SKIPPED_NO_ZERO_QD_BASELINE",
                }
            )
            continue
        observed_outer_binding_ev = level["observed_outer_binding_to_HeII_limit_eV"]
        fixed_screening_binding_ev = r_infinity_ev * (fixed_outer_zeff**2) / (n_outer**2)
        residual_ev = fixed_screening_binding_ev - observed_outer_binding_ev
        zero_qd_abs_residual_ev = level["absolute_residual_eV"]
        rows.append(
            {
                **level,
                "fixed_screening_status": "RESIDUAL_COMPUTED_FIXED_HEURISTIC_MODEL_INCOMPLETE",
                "fixed_screening_sigma_1s_core": screening_sigma_1s_core,
                "fixed_outer_effective_charge": fixed_outer_zeff,
                "fixed_screening_binding_eV": fixed_screening_binding_ev,
                "residual_eV_predicted_minus_observed": residual_ev,
                "absolute_residual_eV": abs(residual_ev),
                "zero_quantum_defect_absolute_residual_eV": zero_qd_abs_residual_ev,
                "absolute_residual_delta_vs_zero_qd_eV": abs(residual_ev) - zero_qd_abs_residual_ev,
            }
        )

    computed_rows = [
        row for row in rows if row["fixed_screening_status"] == "RESIDUAL_COMPUTED_FIXED_HEURISTIC_MODEL_INCOMPLETE"
    ]
    residuals = [row["absolute_residual_eV"] for row in computed_rows]
    zero_residuals = [row["zero_quantum_defect_absolute_residual_eV"] for row in computed_rows]
    improved_rows = [row for row in computed_rows if row["absolute_residual_delta_vs_zero_qd_eV"] < 0.0]
    return {
        "schema_version": "1.0",
        "role": "neutral_helium_fixed_screening_baseline_gate",
        "status": "FIXED_SCREENING_BASELINE_COMPUTED_HEURISTIC_ONLY",
        "claim_class": "fixed_parameter_screening_diagnostic_only_no_helium_validation",
        "formula_id": "AT20-HELIUM-FIXED-SCREENING-BASELINE",
        "formula": "E_bind_pred = h c R_infinity * Z_eff^2 / n^2; Z_eff fixed to 2 - 0.85 before evaluation.",
        "parameter_policy": {
            "nuclear_charge": nuclear_charge,
            "screening_sigma_1s_core": screening_sigma_1s_core,
            "fixed_outer_effective_charge": fixed_outer_zeff,
            "fit_to_current_rows": False,
            "holdout_leakage": False,
        },
        "metrics": {
            "computed_level_count": len(computed_rows),
            "average_abs_binding_residual_eV": float(np.mean(residuals)) if residuals else None,
            "max_abs_binding_residual_eV": max(residuals) if residuals else None,
            "zero_qd_average_abs_binding_residual_eV": float(np.mean(zero_residuals)) if zero_residuals else None,
            "zero_qd_max_abs_binding_residual_eV": max(zero_residuals) if zero_residuals else None,
            "rows_improved_vs_zero_qd": len(improved_rows),
            "rows_worse_or_equal_vs_zero_qd": len(computed_rows) - len(improved_rows),
        },
        "levels": rows,
        "blocked_residual_model_requirements": [
            "source-backed justification or replacement of the fixed screening coefficient",
            "singlet/triplet and angular-momentum-dependent correlation terms",
            "CI/correlated two-electron excited-state Hamiltonian",
            "uncertainty propagation and residual thresholds",
        ],
        "limitations": [
            "This is a fixed-parameter heuristic comparator, not a CI model and not a UET atomic operator.",
            "It intentionally does not fit screening to the current source rows or holdouts.",
            "Improvement over zero-quantum-defect is not required for the gate to be useful; worse residuals are recorded as constraints.",
        ],
        "claim_boundary": "This gate supports only a fixed-parameter helium screening baseline diagnostic. It cannot be cited as neutral-helium validation, many-electron closure, or UET first-principles spectral prediction.",
    }


def build_helium_quantum_defect_prediction_gate(
    helium_excited_hydrogenic_residual_gate: dict,
) -> dict:
    def quantum_defect_standard_error(rows: list[dict]) -> float | None:
        values = [row["effective_quantum_defect_from_source_level"] for row in rows]
        if len(values) < 2:
            return None
        return float(np.std(values, ddof=1) / (len(values) ** 0.5))

    def excitation_uncertainty_from_delta(r_infinity_energy_ev: float, n_outer: int, delta: float, delta_unc: float | None) -> float | None:
        if delta_unc is None:
            return None
        sensitivity = abs(-2.0 * r_infinity_energy_ev / ((n_outer - delta) ** 3))
        return sensitivity * delta_unc

    r_infinity_ev = helium_excited_hydrogenic_residual_gate["constants"]["R_infinity_energy_eV"]
    first_ionization_ev = helium_excited_hydrogenic_residual_gate["constants"]["first_ionization_energy_eV"]
    level_rows = [
        row
        for row in helium_excited_hydrogenic_residual_gate["levels"]
        if row["baseline_status"] == "RESIDUAL_COMPUTED_MODEL_INCOMPLETE"
        and row["effective_quantum_defect_from_source_level"] is not None
    ]
    series = {}
    for row in level_rows:
        orbital = parse_outer_orbital_letter(row["configuration"])
        multiplicity = parse_term_multiplicity(row["term"])
        series_key = f"{multiplicity}{orbital}" if orbital else f"{multiplicity}unknown"
        series.setdefault(series_key, []).append(row)

    predictions = []
    skipped = []
    for series_key, rows in sorted(series.items()):
        distinct_n = sorted({row["outer_principal_quantum_number"] for row in rows})
        for row in rows:
            training_rows = [
                candidate
                for candidate in rows
                if candidate["outer_principal_quantum_number"] != row["outer_principal_quantum_number"]
            ]
            if not training_rows:
                skipped.append(
                    {
                        "series_key": series_key,
                        "configuration": row["configuration"],
                        "term": row["term"],
                        "j": row["j"],
                        "outer_principal_quantum_number": row["outer_principal_quantum_number"],
                        "reason": "no_same_series_training_level_at_different_n",
                    }
                )
                continue
            delta_mean = float(
                np.mean([candidate["effective_quantum_defect_from_source_level"] for candidate in training_rows])
            )
            delta_standard_error = quantum_defect_standard_error(training_rows)
            n_outer = row["outer_principal_quantum_number"]
            predicted_binding_ev = r_infinity_ev / ((n_outer - delta_mean) ** 2)
            predicted_excitation_ev = first_ionization_ev - predicted_binding_ev
            predicted_excitation_uncertainty_ev = excitation_uncertainty_from_delta(
                r_infinity_ev, n_outer, delta_mean, delta_standard_error
            )
            residual_ev = predicted_excitation_ev - row["excitation_energy_eV"]
            predictions.append(
                {
                    "series_key": series_key,
                    "series_distinct_n": distinct_n,
                    "configuration": row["configuration"],
                    "term": row["term"],
                    "j": row["j"],
                    "outer_principal_quantum_number": n_outer,
                    "training_level_count": len(training_rows),
                    "training_distinct_n": sorted(
                        {candidate["outer_principal_quantum_number"] for candidate in training_rows}
                    ),
                    "calibrated_quantum_defect": delta_mean,
                    "calibrated_quantum_defect_standard_error": delta_standard_error,
                    "model_parameter_uncertainty_basis": (
                        "same-series source quantum-defect standard error from training rows"
                        if delta_standard_error is not None
                        else "not available with fewer than two training rows"
                    ),
                    "source_quantum_defect": row["effective_quantum_defect_from_source_level"],
                    "predicted_outer_binding_eV": predicted_binding_ev,
                    "observed_outer_binding_eV": row["observed_outer_binding_to_HeII_limit_eV"],
                    "predicted_excitation_energy_eV": predicted_excitation_ev,
                    "predicted_excitation_model_uncertainty_eV": predicted_excitation_uncertainty_ev,
                    "observed_excitation_energy_eV": row["excitation_energy_eV"],
                    "residual_eV_predicted_minus_observed": residual_ev,
                    "absolute_residual_eV": abs(residual_ev),
                }
            )

    residuals = [row["absolute_residual_eV"] for row in predictions]
    signed_residuals = [row["residual_eV_predicted_minus_observed"] for row in predictions]
    model_uncertainties = [
        row["predicted_excitation_model_uncertainty_eV"]
        for row in predictions
        if row.get("predicted_excitation_model_uncertainty_eV") is not None
    ]
    return {
        "schema_version": "1.0",
        "role": "neutral_helium_quantum_defect_prediction_gate",
        "status": "SOURCE_CALIBRATED_QD_LOO_RESIDUAL_COMPUTED_MODEL_BLOCKED",
        "claim_class": "source_calibrated_series_prediction_only_no_first_principles_helium_validation",
        "formula_id": "AT20-HELIUM-QUANTUM-DEFECT-LOO-PREDICTION",
        "formula": "E_bind_pred = h c R_infinity / (n - delta_series)^2; delta_series is fitted from same-series source levels at different n.",
        "source_basis": "Selected NIST He I term levels grouped by spin multiplicity and outer orbital letter.",
        "metrics": {
            "series_count": len(series),
            "series_with_leave_one_out_predictions": len(
                {row["series_key"] for row in predictions}
            ),
            "prediction_count": len(predictions),
            "skipped_level_count": len(skipped),
            "average_abs_excitation_residual_eV": float(np.mean(residuals)) if residuals else None,
            "max_abs_excitation_residual_eV": max(residuals) if residuals else None,
            "excitation_residual_rmse_eV": (
                float((np.mean([residual**2 for residual in signed_residuals])) ** 0.5)
                if signed_residuals
                else None
            ),
            "predictions_with_model_parameter_uncertainty_count": len(model_uncertainties),
            "max_predicted_excitation_model_uncertainty_eV": max(model_uncertainties) if model_uncertainties else None,
        },
        "series_summary": {
            key: {
                "level_count": len(rows),
                "distinct_n": sorted({row["outer_principal_quantum_number"] for row in rows}),
                "mean_source_quantum_defect": float(
                    np.mean([row["effective_quantum_defect_from_source_level"] for row in rows])
                ),
                "source_quantum_defect_standard_deviation": (
                    float(np.std([row["effective_quantum_defect_from_source_level"] for row in rows], ddof=1))
                    if len(rows) > 1
                    else None
                ),
                "source_quantum_defect_standard_error": quantum_defect_standard_error(rows),
                "model_parameter_uncertainty_status": (
                    "SERIES_STANDARD_ERROR_AVAILABLE" if len(rows) > 1 else "INSUFFICIENT_SERIES_ROWS"
                ),
            }
            for key, rows in sorted(series.items())
        },
        "predictions": predictions,
        "skipped": skipped,
        "blocked_residual_model_requirements": [
            "independent holdout lines not used for quantum-defect calibration",
            "official/source uncertainty propagation for term energies and ionization limit",
            "fine-structure/component policy for blended lines",
            "correlated two-electron or CI model that predicts quantum defects instead of fitting them",
        ],
        "limitations": [
            "This is a source-calibrated prediction diagnostic, not a first-principles model.",
            "Series with only one distinct n cannot be leave-one-out predicted by this gate.",
            "Model-parameter uncertainty uses same-series quantum-defect scatter only; it does not include official term-energy uncertainty or model inadequacy.",
            "The gate uses only selected visible-line-linked levels, so it cannot support broad helium validation.",
        ],
        "claim_boundary": "This gate supports only limited source-calibrated quantum-defect prediction diagnostics for selected He I levels. It cannot be cited as UET deriving helium spectra or solving many-electron atoms.",
    }


def build_helium_quantum_defect_holdout_gate(
    helium_ground_state_baseline_gate: dict,
    helium_quantum_defect_prediction_gate: dict,
    helium_qd_holdouts: dict,
) -> dict:
    first_ionization_ev = helium_ground_state_baseline_gate["observed_anchor"]["first_ionization_energy_eV"]
    r_infinity_ev = helium_quantum_defect_prediction_gate["predictions"][0]["predicted_outer_binding_eV"] * 0.0
    for key, series_row in helium_quantum_defect_prediction_gate["series_summary"].items():
        if series_row["distinct_n"]:
            # Recover R_inf energy from any source quantum defect row is not possible from summary alone.
            # The holdout gate uses the same value already recorded in the hydrogenic residual gate constants,
            # passed through the prediction rows below when available.
            break
    calibration_delta_by_series = {
        key: value["mean_source_quantum_defect"]
        for key, value in helium_quantum_defect_prediction_gate["series_summary"].items()
    }
    calibration_delta_uncertainty_by_series = {
        key: value.get("source_quantum_defect_standard_error")
        for key, value in helium_quantum_defect_prediction_gate["series_summary"].items()
    }
    empirical_loo_model_uncertainty_ev = helium_quantum_defect_prediction_gate["metrics"].get(
        "excitation_residual_rmse_eV"
    )
    if helium_quantum_defect_prediction_gate["predictions"]:
        sample = helium_quantum_defect_prediction_gate["predictions"][0]
        n_sample = sample["outer_principal_quantum_number"]
        delta_sample = sample["calibrated_quantum_defect"]
        r_infinity_ev = sample["predicted_outer_binding_eV"] * (n_sample - delta_sample) ** 2

    holdout_levels = {}
    for row in helium_qd_holdouts["holdout_levels"]:
        for prefix in ("lower", "upper"):
            energy = row[f"{prefix}_energy_cm_inverse"]
            if energy <= 0.0:
                continue
            key = (
                row[f"{prefix}_configuration"],
                row[f"{prefix}_term"],
                row[f"{prefix}_j"],
                energy,
            )
            holdout_levels[key] = {
                "holdout_id": row["holdout_id"],
                "source_wavelength_angstrom": row["wavelength_angstrom"],
                "source_wavelength_uncertainty_angstrom": row.get("wavelength_uncertainty_angstrom"),
                "source_wavelength_uncertainty_basis": row.get("wavelength_uncertainty_basis"),
                "configuration": row[f"{prefix}_configuration"],
                "term": row[f"{prefix}_term"],
                "j": row[f"{prefix}_j"],
                "excitation_energy_cm_inverse": energy,
                "excitation_energy_uncertainty_cm_inverse": row.get(f"{prefix}_energy_uncertainty_cm_inverse"),
                "excitation_energy_eV": energy * EV_PER_CM_INVERSE,
                "excitation_energy_uncertainty_eV": (
                    row.get(f"{prefix}_energy_uncertainty_cm_inverse") * EV_PER_CM_INVERSE
                    if row.get(f"{prefix}_energy_uncertainty_cm_inverse") is not None
                    else None
                ),
                "source_locator": row["source_locator"],
            }

    predictions = []
    skipped = []
    for level in sorted(holdout_levels.values(), key=lambda item: item["excitation_energy_cm_inverse"]):
        n_outer = parse_outer_principal_quantum_number(level["configuration"])
        orbital = parse_outer_orbital_letter(level["configuration"])
        multiplicity = parse_term_multiplicity(level["term"])
        series_key = f"{multiplicity}{orbital}" if orbital else f"{multiplicity}unknown"
        if n_outer is None or orbital is None:
            skipped.append({**level, "series_key": series_key, "reason": "configuration_not_parsed"})
            continue
        if series_key not in calibration_delta_by_series:
            skipped.append({**level, "series_key": series_key, "reason": "no_selected_calibration_series"})
            continue
        delta = calibration_delta_by_series[series_key]
        delta_uncertainty = calibration_delta_uncertainty_by_series.get(series_key)
        predicted_binding_ev = r_infinity_ev / ((n_outer - delta) ** 2)
        observed_binding_ev = first_ionization_ev - level["excitation_energy_eV"]
        predicted_excitation_ev = first_ionization_ev - predicted_binding_ev
        propagated_delta_uncertainty_ev = (
            abs(-2.0 * r_infinity_ev / ((n_outer - delta) ** 3)) * delta_uncertainty
            if delta_uncertainty is not None
            else None
        )
        if propagated_delta_uncertainty_ev is not None:
            predicted_excitation_model_uncertainty_ev = propagated_delta_uncertainty_ev
            model_uncertainty_basis = "selected-series source quantum-defect standard error propagated through level formula"
        else:
            predicted_excitation_model_uncertainty_ev = empirical_loo_model_uncertainty_ev
            model_uncertainty_basis = (
                "global leave-one-out excitation residual RMSE fallback because selected series has fewer than two calibration rows"
            )
        residual_ev = predicted_excitation_ev - level["excitation_energy_eV"]
        predictions.append(
            {
                **level,
                "series_key": series_key,
                "outer_principal_quantum_number": n_outer,
                "calibration_delta_source": "selected_level_series_mean_quantum_defect",
                "calibrated_quantum_defect": delta,
                "calibrated_quantum_defect_standard_error": delta_uncertainty,
                "model_parameter_uncertainty_basis": (
                    "selected-series source quantum-defect standard error"
                    if delta_uncertainty is not None
                    else "not available with fewer than two selected calibration rows"
                ),
                "predicted_excitation_model_uncertainty_basis": model_uncertainty_basis,
                "predicted_outer_binding_eV": predicted_binding_ev,
                "observed_outer_binding_eV": observed_binding_ev,
                "predicted_excitation_energy_eV": predicted_excitation_ev,
                "predicted_excitation_model_uncertainty_eV": predicted_excitation_model_uncertainty_ev,
                "observed_excitation_energy_eV": level["excitation_energy_eV"],
                "residual_eV_predicted_minus_observed": residual_ev,
                "absolute_residual_eV": abs(residual_ev),
            }
        )

    residuals = [row["absolute_residual_eV"] for row in predictions]
    prediction_uncertainties = [
        row["excitation_energy_uncertainty_eV"]
        for row in predictions
        if row.get("excitation_energy_uncertainty_eV") is not None
    ]
    model_uncertainties = [
        row["predicted_excitation_model_uncertainty_eV"]
        for row in predictions
        if row.get("predicted_excitation_model_uncertainty_eV") is not None
    ]
    return {
        "schema_version": "1.0",
        "role": "neutral_helium_quantum_defect_source_family_holdout_gate",
        "status": "SOURCE_FAMILY_HOLDOUT_RESIDUAL_COMPUTED_EXTERNAL_HOLDOUT_BLOCKED",
        "claim_class": "same_source_family_holdout_prediction_only_no_independent_validation",
        "formula_id": "AT20-HELIUM-QUANTUM-DEFECT-SOURCE-FAMILY-HOLDOUT",
        "formula": "E_bind_pred = h c R_infinity / (n - delta_selected_series)^2; holdout levels are excluded from the selected calibration set.",
        "source_basis": helium_qd_holdouts["source"],
        "split_policy": helium_qd_holdouts["split_policy"],
        "uncertainty_policy": helium_qd_holdouts.get("uncertainty_policy"),
        "metrics": {
            "holdout_source_row_count": len(helium_qd_holdouts["holdout_levels"]),
            "unique_holdout_level_count": len(holdout_levels),
            "prediction_count": len(predictions),
            "skipped_level_count": len(skipped),
            "average_abs_excitation_residual_eV": float(np.mean(residuals)) if residuals else None,
            "max_abs_excitation_residual_eV": max(residuals) if residuals else None,
            "predicted_levels_with_source_uncertainty_count": len(prediction_uncertainties),
            "max_source_excitation_uncertainty_eV": max(prediction_uncertainties) if prediction_uncertainties else None,
            "predicted_levels_with_model_parameter_uncertainty_count": len(model_uncertainties),
            "max_predicted_excitation_model_uncertainty_eV": max(model_uncertainties) if model_uncertainties else None,
            "source_uncertainty_policy_status": helium_qd_holdouts.get("uncertainty_policy", {}).get("status"),
        },
        "predictions": predictions,
        "skipped": skipped,
        "blocked_residual_model_requirements": [
            "independent external holdout source family",
            "larger singlet/triplet calibration suite with explicit train/test split",
            "model-parameter uncertainty propagation for fitted quantum defects and derived wavelength holdout rows",
            "CI or correlated two-electron model that predicts series defects",
        ],
        "limitations": [
            "Holdouts come from the same NIST source family, so they are not independent external validation.",
            "Rows without a selected calibration series are skipped rather than fit from the holdout set.",
            "Source uncertainties are transcription-rounding bounds, not official NIST measurement uncertainties.",
            "Model-parameter uncertainty uses selected-series quantum-defect scatter only; it does not include official term-energy uncertainty or model inadequacy.",
            "This gate tests extrapolation of fitted quantum defects, not first-principles helium theory.",
        ],
        "claim_boundary": helium_qd_holdouts["claim_boundary"],
    }


def build_helium_quantum_defect_wavelength_holdout_gate(
    helium_quantum_defect_holdout_gate: dict,
    helium_qd_holdouts: dict,
) -> dict:
    level_predictions = {
        (
            row["configuration"],
            row["term"],
            row["j"],
            row["observed_excitation_energy_eV"],
        ): row
        for row in helium_quantum_defect_holdout_gate["predictions"]
    }
    line_predictions = []
    skipped = []

    for row in helium_qd_holdouts["holdout_levels"]:
        source_medium = classify_nist_wavelength_medium_angstrom(row["wavelength_angstrom"])
        if abs(row["lower_energy_cm_inverse"]) > 0.0:
            skipped.append(
                {
                    "holdout_id": row["holdout_id"],
                    "source_wavelength_angstrom": row["wavelength_angstrom"],
                    "source_wavelength_uncertainty_angstrom": row.get("wavelength_uncertainty_angstrom"),
                    "source_wavelength_medium": source_medium,
                    "reason": "lower_level_not_ground_state_to_avoid_holdout_energy_leakage",
                }
            )
            continue

        upper_excitation_eV = row["upper_energy_cm_inverse"] * EV_PER_CM_INVERSE
        key = (
            row["upper_configuration"],
            row["upper_term"],
            row["upper_j"],
            upper_excitation_eV,
        )
        prediction = level_predictions.get(key)
        if prediction is None:
            skipped.append(
                {
                    "holdout_id": row["holdout_id"],
                    "source_wavelength_angstrom": row["wavelength_angstrom"],
                    "source_wavelength_uncertainty_angstrom": row.get("wavelength_uncertainty_angstrom"),
                    "source_wavelength_medium": source_medium,
                    "reason": "upper_level_not_predicted_by_holdout_gate",
                }
            )
            continue

        predicted_wavenumber_cm_inverse = prediction["predicted_excitation_energy_eV"] / EV_PER_CM_INVERSE
        predicted_wavelength_angstrom = 1.0e8 / predicted_wavenumber_cm_inverse
        predicted_excitation_model_uncertainty_eV = prediction.get("predicted_excitation_model_uncertainty_eV")
        predicted_wavelength_model_uncertainty_angstrom = (
            (1.0e8 * EV_PER_CM_INVERSE / (prediction["predicted_excitation_energy_eV"] ** 2))
            * predicted_excitation_model_uncertainty_eV
            if predicted_excitation_model_uncertainty_eV is not None
            else None
        )
        observed_wavelength_angstrom = row["wavelength_angstrom"]
        if source_medium == "vacuum":
            source_vacuum_equivalent_angstrom = observed_wavelength_angstrom
            medium_adjustment_status = "NO_AIR_CORRECTION_NEEDED_UNDER_NIST_CONVENTION"
        else:
            source_vacuum_equivalent_angstrom = None
            medium_adjustment_status = "AIR_TO_VACUUM_CONVERSION_REQUIRED_BEFORE_MODEL_RESIDUAL"
            skipped.append(
                {
                    "holdout_id": row["holdout_id"],
                    "source_wavelength_angstrom": row["wavelength_angstrom"],
                    "source_wavelength_uncertainty_angstrom": row.get("wavelength_uncertainty_angstrom"),
                    "source_wavelength_medium": source_medium,
                    "reason": "source_air_wavelength_requires_refractive_index_policy",
                }
            )
            continue
        residual_angstrom = predicted_wavelength_angstrom - observed_wavelength_angstrom
        residual_ppm = abs(residual_angstrom) / observed_wavelength_angstrom * 1.0e6
        line_predictions.append(
            {
                "holdout_id": row["holdout_id"],
                "source_wavelength_angstrom": observed_wavelength_angstrom,
                "source_wavelength_uncertainty_angstrom": row.get("wavelength_uncertainty_angstrom"),
                "source_wavelength_uncertainty_basis": row.get("wavelength_uncertainty_basis"),
                "source_wavelength_medium": source_medium,
                "source_vacuum_equivalent_angstrom": source_vacuum_equivalent_angstrom,
                "predicted_wavelength_angstrom": predicted_wavelength_angstrom,
                "predicted_wavelength_model_uncertainty_angstrom": predicted_wavelength_model_uncertainty_angstrom,
                "residual_angstrom_predicted_minus_source": residual_angstrom,
                "absolute_residual_angstrom": abs(residual_angstrom),
                "absolute_residual_nm": abs(residual_angstrom) * 0.1,
                "absolute_residual_ppm": residual_ppm,
                "predicted_wavenumber_cm_inverse": predicted_wavenumber_cm_inverse,
                "source_upper_energy_cm_inverse": row["upper_energy_cm_inverse"],
                "predicted_upper_excitation_energy_eV": prediction["predicted_excitation_energy_eV"],
                "predicted_upper_excitation_model_uncertainty_eV": predicted_excitation_model_uncertainty_eV,
                "source_upper_excitation_energy_eV": prediction["observed_excitation_energy_eV"],
                "upper_configuration": row["upper_configuration"],
                "upper_term": row["upper_term"],
                "upper_j": row["upper_j"],
                "source_locator": row["source_locator"],
                "medium_adjustment_status": medium_adjustment_status,
                "medium_policy": "NIST convention: wavelengths below 2000 A are vacuum; 2000-20000 A are standard air; above 20000 A are vacuum.",
            }
        )

    residuals_angstrom = [line["absolute_residual_angstrom"] for line in line_predictions]
    residuals_ppm = [line["absolute_residual_ppm"] for line in line_predictions]
    wavelength_uncertainties = [
        line["source_wavelength_uncertainty_angstrom"]
        for line in line_predictions
        if line.get("source_wavelength_uncertainty_angstrom") is not None
    ]
    wavelength_model_uncertainties = [
        line["predicted_wavelength_model_uncertainty_angstrom"]
        for line in line_predictions
        if line.get("predicted_wavelength_model_uncertainty_angstrom") is not None
    ]
    return {
        "schema_version": "1.0",
        "role": "neutral_helium_quantum_defect_wavelength_holdout_gate",
        "status": "SOURCE_FAMILY_HOLDOUT_WAVELENGTH_RESIDUAL_COMPUTED_EXTERNAL_HOLDOUT_BLOCKED",
        "claim_class": "same_source_family_wavelength_prediction_diagnostic_only_no_independent_validation",
        "formula_id": "AT20-HELIUM-QUANTUM-DEFECT-HOLDOUT-WAVELENGTH",
        "formula": "lambda_pred_A = 1e8 / (E_upper_pred_eV / (h c)); lower level restricted to ground-state holdouts to avoid lower-level leakage.",
        "source_basis": helium_qd_holdouts["source"],
        "uncertainty_policy": helium_qd_holdouts.get("uncertainty_policy"),
        "wavelength_medium_policy": {
            "basis": "NIST ASD/handbook wavelength convention",
            "vacuum_below_angstrom": 2000.0,
            "standard_air_from_angstrom": 2000.0,
            "standard_air_to_angstrom": 20000.0,
            "vacuum_above_angstrom": 20000.0,
            "source_url": "https://pml.nist.gov/PhysRefData/ASD/Html/lineshelp.html",
        },
        "metrics": {
            "holdout_line_count": len(helium_qd_holdouts["holdout_levels"]),
            "predicted_line_count": len(line_predictions),
            "skipped_line_count": len(skipped),
            "predicted_vacuum_line_count": sum(
                1 for line in line_predictions if line["source_wavelength_medium"] == "vacuum"
            ),
            "skipped_air_line_count": sum(
                1 for line in skipped if line.get("source_wavelength_medium") == "standard_air"
            ),
            "average_abs_wavelength_residual_angstrom": float(np.mean(residuals_angstrom)) if residuals_angstrom else None,
            "max_abs_wavelength_residual_angstrom": max(residuals_angstrom) if residuals_angstrom else None,
            "average_abs_wavelength_residual_ppm": float(np.mean(residuals_ppm)) if residuals_ppm else None,
            "max_abs_wavelength_residual_ppm": max(residuals_ppm) if residuals_ppm else None,
            "predicted_lines_with_source_uncertainty_count": len(wavelength_uncertainties),
            "max_source_wavelength_uncertainty_angstrom": max(wavelength_uncertainties) if wavelength_uncertainties else None,
            "predicted_lines_with_model_parameter_uncertainty_count": len(wavelength_model_uncertainties),
            "max_predicted_wavelength_model_uncertainty_angstrom": (
                max(wavelength_model_uncertainties) if wavelength_model_uncertainties else None
            ),
            "source_uncertainty_policy_status": helium_qd_holdouts.get("uncertainty_policy", {}).get("status"),
        },
        "predictions": line_predictions,
        "skipped": skipped,
        "blocked_residual_model_requirements": [
            "independent external spectral-line holdout source",
            "model-parameter uncertainty propagation from level prediction to wavelength residual",
            "air/vacuum conversion policy for future non-ground holdout lines in the standard-air range",
            "correlated two-electron or CI model that predicts line positions without fitted quantum defects",
        ],
        "limitations": [
            "Only ground-to-excited holdout lines are predicted to avoid using holdout lower-level energies.",
            "Predicted holdout lines in this gate are below 2000 A and are treated as vacuum wavelengths under the NIST convention.",
            "Holdout lines in the standard-air wavelength range are skipped until an air/vacuum conversion policy is applied.",
            "Source uncertainties are transcription-rounding bounds, not official NIST measurement uncertainties.",
            "Wavelength model uncertainty propagates fitted quantum-defect scatter only; it is not a complete line-position uncertainty.",
            "Same-source-family holdouts are not independent external validation.",
        ],
        "claim_boundary": "This gate supports only same-source-family He I wavelength holdout diagnostics. It does not validate helium spectra independently and does not derive line positions from first principles.",
    }


def build_atomic_prediction_baseline_comparator_gate(
    precision_baseline_gate: dict,
    precision_dirac_baseline_gate: dict,
    lamb_shift_handoff_gate: dict,
    hyperfine_fermi_baseline_gate: dict,
    helium_excited_hydrogenic_residual_gate: dict,
    helium_fixed_screening_baseline_gate: dict,
    helium_quantum_defect_prediction_gate: dict,
    helium_quantum_defect_holdout_gate: dict,
    helium_quantum_defect_wavelength_holdout_gate: dict,
) -> dict:
    helium_zero_avg = helium_excited_hydrogenic_residual_gate["metrics"]["average_abs_binding_residual_eV"]
    helium_fixed_avg = helium_fixed_screening_baseline_gate["metrics"]["average_abs_binding_residual_eV"]
    helium_loo_avg = helium_quantum_defect_prediction_gate["metrics"]["average_abs_excitation_residual_eV"]
    helium_holdout_avg = helium_quantum_defect_holdout_gate["metrics"]["average_abs_excitation_residual_eV"]
    precision_nonrel_ppm = precision_baseline_gate["prediction"]["residual_ppm"]
    precision_dirac_ppm = precision_dirac_baseline_gate["prediction"]["residual_ppm"]
    precision_lamb_ppm = lamb_shift_handoff_gate["prediction"]["residual_ppm"]
    comparator_rows = [
        {
            "comparator_id": "hydrogen_1s2s_nonrel_to_dirac",
            "domain": "hydrogen_precision",
            "baseline_model": "nonrelativistic Rydberg 1S-2S",
            "candidate_model": "leading Dirac fine-structure baseline",
            "baseline_residual_ppm": precision_nonrel_ppm,
            "candidate_residual_ppm": precision_dirac_ppm,
            "absolute_improvement_factor": precision_nonrel_ppm / precision_dirac_ppm,
            "claim_role": "diagnostic baseline comparison only; QED/recoil/proton-size terms remain open",
        },
        {
            "comparator_id": "hydrogen_1s2s_dirac_to_lamb_handoff",
            "domain": "hydrogen_precision",
            "baseline_model": "leading Dirac fine-structure baseline",
            "candidate_model": "empirical Lamb-shift handoff",
            "baseline_residual_ppm": precision_dirac_ppm,
            "candidate_residual_ppm": precision_lamb_ppm,
            "absolute_improvement_factor": precision_dirac_ppm / precision_lamb_ppm,
            "claim_role": "empirical handoff comparison only; not a QED derivation",
        },
        {
            "comparator_id": "helium_excited_zero_qd_to_fixed_screening",
            "domain": "neutral_helium_excited_levels",
            "baseline_model": "zero-quantum-defect hydrogenic baseline",
            "candidate_model": "fixed one-active-electron screening baseline",
            "baseline_avg_abs_residual_eV": helium_zero_avg,
            "candidate_avg_abs_residual_eV": helium_fixed_avg,
            "average_residual_improvement_factor": helium_zero_avg / helium_fixed_avg,
            "baseline_max_abs_residual_eV": helium_excited_hydrogenic_residual_gate["metrics"]["max_abs_binding_residual_eV"],
            "candidate_max_abs_residual_eV": helium_fixed_screening_baseline_gate["metrics"]["max_abs_binding_residual_eV"],
            "candidate_rows_improved_vs_baseline": helium_fixed_screening_baseline_gate["metrics"]["rows_improved_vs_zero_qd"],
            "claim_role": "fixed-parameter heuristic comparison only; not CI and not UET first-principles derivation",
        },
        {
            "comparator_id": "helium_excited_zero_qd_to_qd_loo",
            "domain": "neutral_helium_excited_levels",
            "baseline_model": "zero-quantum-defect hydrogenic baseline",
            "candidate_model": "same-source-series quantum-defect leave-one-out fit",
            "baseline_avg_abs_residual_eV": helium_zero_avg,
            "candidate_avg_abs_residual_eV": helium_loo_avg,
            "average_residual_improvement_factor": helium_zero_avg / helium_loo_avg,
            "baseline_max_abs_residual_eV": helium_excited_hydrogenic_residual_gate["metrics"]["max_abs_binding_residual_eV"],
            "candidate_max_abs_residual_eV": helium_quantum_defect_prediction_gate["metrics"]["max_abs_excitation_residual_eV"],
            "claim_role": "source-calibrated diagnostic comparison only; quantum defects are fitted, not derived",
        },
        {
            "comparator_id": "helium_excited_zero_qd_to_same_source_holdout",
            "domain": "neutral_helium_excited_levels",
            "baseline_model": "zero-quantum-defect hydrogenic baseline",
            "candidate_model": "selected-source calibrated quantum-defect model evaluated on same-source-family holdouts",
            "baseline_avg_abs_residual_eV": helium_zero_avg,
            "candidate_avg_abs_residual_eV": helium_holdout_avg,
            "average_residual_improvement_factor": helium_zero_avg / helium_holdout_avg,
            "baseline_max_abs_residual_eV": helium_excited_hydrogenic_residual_gate["metrics"]["max_abs_binding_residual_eV"],
            "candidate_max_abs_residual_eV": helium_quantum_defect_holdout_gate["metrics"]["max_abs_excitation_residual_eV"],
            "claim_role": "same-source-family holdout comparison only; not independent external validation",
        },
        {
            "comparator_id": "helium_wavelength_holdout_report",
            "domain": "neutral_helium_wavelengths",
            "baseline_model": "no CI/correlated wavelength comparator primary-gated",
            "candidate_model": "quantum-defect level prediction converted to ground-state holdout wavelengths",
            "candidate_avg_abs_residual_angstrom": helium_quantum_defect_wavelength_holdout_gate["metrics"][
                "average_abs_wavelength_residual_angstrom"
            ],
            "candidate_max_abs_residual_ppm": helium_quantum_defect_wavelength_holdout_gate["metrics"][
                "max_abs_wavelength_residual_ppm"
            ],
            "claim_role": "reported as candidate residual only until a CI/correlated or external baseline exists",
        },
        {
            "comparator_id": "hydrogen_21cm_fermi_baseline_report",
            "domain": "hydrogen_hyperfine",
            "baseline_model": "leading Fermi-contact hyperfine baseline",
            "candidate_model": "none primary-gated",
            "candidate_residual_ppm": hyperfine_fermi_baseline_gate["prediction"]["residual_ppm"],
            "claim_role": "gap-sizing baseline only; no corrected hyperfine Hamiltonian comparator is primary-gated",
        },
    ]
    return {
        "schema_version": "1.0",
        "role": "atomic_prediction_baseline_comparator_gate",
        "status": "INTERNAL_COMPARATOR_TABLE_READY_EXTERNAL_AND_CI_BASELINES_OPEN",
        "claim_class": "internal_comparator_diagnostic_only",
        "formula_id": "AT20-ATOMIC-PREDICTION-BASELINE-COMPARATOR",
        "purpose": "Make current atomic prediction diagnostics compare against named baselines before any broader predictive claim is exported.",
        "comparators": comparator_rows,
        "metrics": {
            "comparator_count": len(comparator_rows),
            "comparators_with_improvement_factor": sum(
                1 for row in comparator_rows if "absolute_improvement_factor" in row or "average_residual_improvement_factor" in row
            ),
            "comparators_missing_external_or_ci_baseline": 2,
            "helium_zero_qd_to_qd_loo_average_improvement_factor": helium_zero_avg / helium_loo_avg,
            "helium_zero_qd_to_fixed_screening_average_improvement_factor": helium_zero_avg / helium_fixed_avg,
            "helium_zero_qd_to_same_source_holdout_average_improvement_factor": helium_zero_avg / helium_holdout_avg,
            "hydrogen_1s2s_nonrel_to_dirac_improvement_factor": precision_nonrel_ppm / precision_dirac_ppm,
            "hydrogen_1s2s_dirac_to_lamb_handoff_improvement_factor": precision_dirac_ppm / precision_lamb_ppm,
        },
        "blocked_comparators": [
            "CI/correlated helium spectral residual baseline",
            "independent external helium wavelength holdout baseline",
            "higher-Z fine/QED comparator suite",
            "multi-atom many-electron benchmark comparator table",
            "UET-derived atomic operator residual lane",
        ],
        "claim_boundary": "This gate supports only internal comparator bookkeeping. It does not turn fitted quantum-defect, empirical Lamb-handoff, or Fermi-baseline diagnostics into first-principles predictions.",
    }


def build_hydrogen_rydberg_line_uncertainty_gate(spectrum: dict, results: list[dict]) -> dict:
    uncertainty_rows = [
        row for row in results if row.get("residual_to_source_uncertainty_ratio") is not None
    ]
    residual_ratios = [row["residual_to_source_uncertainty_ratio"] for row in uncertainty_rows]
    wavelength_uncertainties = [
        row["wavelength_vacuum_uncertainty_nm"]
        for row in uncertainty_rows
        if row.get("wavelength_vacuum_uncertainty_nm") is not None
    ]
    return {
        "schema_version": "1.0",
        "role": "hydrogen_rydberg_line_uncertainty_gate",
        "status": "TRANSCRIPTION_BOUND_RESIDUALS_COMPUTED_CLAIM_STILL_BLOCKED",
        "claim_class": "source_transcription_uncertainty_diagnostic_only",
        "formula_id": "AT20-HYDROGEN-RYDBERG-LINE-TRANSCRIPTION-BUDGET",
        "source_basis": spectrum.get("publication"),
        "uncertainty_policy": spectrum.get("uncertainty_policy"),
        "metrics": {
            "line_count": len(results),
            "lines_with_source_uncertainty_count": len(uncertainty_rows),
            "max_source_wavelength_uncertainty_nm": max(wavelength_uncertainties) if wavelength_uncertainties else None,
            "max_abs_wavelength_residual_nm": (
                max(row["absolute_wavelength_residual_nm"] for row in results) if results else None
            ),
            "max_residual_to_source_uncertainty_ratio": max(residual_ratios) if residual_ratios else None,
            "min_residual_to_source_uncertainty_ratio": min(residual_ratios) if residual_ratios else None,
        },
        "lines": [
            {
                "name": row["name"],
                "series": row["series"],
                "observed_wavelength_vacuum_nm": row["wavelength_vacuum_nm"],
                "source_wavelength_uncertainty_nm": row.get("wavelength_vacuum_uncertainty_nm"),
                "source_wavelength_uncertainty_basis": row.get("wavelength_uncertainty_basis"),
                "predicted_wavelength_nm": row["predicted_wavelength_nm"],
                "absolute_wavelength_residual_nm": row["absolute_wavelength_residual_nm"],
                "residual_to_source_uncertainty_ratio": row.get("residual_to_source_uncertainty_ratio"),
            }
            for row in results
        ],
        "limitations": [
            "Uncertainty values are transcription-rounding bounds from the local working copy, not official NIST measurement uncertainties.",
            "Residual-to-bound ratios diagnose working-copy precision only and do not validate UET-derived R_H or a complete atomic model.",
            "CODATA R_H is used as an input constant; model uncertainty for R_H derivation is not present.",
        ],
        "claim_boundary": "This gate supports only hydrogen Rydberg line transcription-bound diagnostics. It cannot be cited as uncertainty-qualified hydrogen validation or UET first-principles derivation.",
    }


def build_legacy_multielectron_code_audit_gate() -> dict:
    scripts = [
        {
            "script_id": "research_multi_electron",
            "path": LEGACY_MULTI_ELECTRON_PATH,
            "observed_role": "wrapper that calls Research_Atomic_ThreeBody.run_three_body",
            "evidence_status": "DEMO_WRAPPER_NOT_PRIMARY_EVIDENCE",
            "why_not_model": [
                "does not load helium source rows",
                "does not compute energy levels or line positions",
                "does not compare residuals to thresholds",
            ],
        },
        {
            "script_id": "research_atomic_three_body",
            "path": LEGACY_THREE_BODY_PATH,
            "observed_role": "engine-coupling smoke test using beta / beta sanity check",
            "evidence_status": "SMOKE_TEST_NOT_ATOMIC_MODEL",
            "why_not_model": [
                "does not implement a two-electron Hamiltonian",
                "does not model electron-electron correlation",
                "does not emit source-backed spectral residuals",
            ],
        },
    ]
    rows = []
    for script in scripts:
        path = script["path"]
        rows.append(
            {
                "script_id": script["script_id"],
                "path": str(path.relative_to(TOPIC_DIR)).replace("\\", "/"),
                "sha256": file_sha256(path) if path.exists() else None,
                "exists": path.exists(),
                "observed_role": script["observed_role"],
                "evidence_status": script["evidence_status"],
                "why_not_model": script["why_not_model"],
            }
        )
    return {
        "schema_version": "1.0",
        "role": "legacy_multielectron_code_audit_gate",
        "status": "LEGACY_CODE_CLASSIFIED_NOT_PRIMARY_EVIDENCE",
        "claim_class": "code_audit_and_overclaim_prevention_only",
        "formula_id": "AT20-LEGACY-MULTIELECTRON-CODE-AUDIT",
        "audited_scripts": rows,
        "metrics": {
            "script_count": len(rows),
            "scripts_present": sum(1 for row in rows if row["exists"]),
            "primary_evidence_script_count": 0,
            "ci_or_correlated_model_present": False,
            "spectral_residual_artifact_present": False,
        },
        "required_replacement_artifacts": [
            "fixed-parameter CI or correlated two-electron Hamiltonian residual gate",
            "source-backed helium excited-state residual rows",
            "uncertainty-aware thresholds for level and wavelength residuals",
            "explicit UET atomic operator only if derived parameters are locked before holdout evaluation",
        ],
        "claim_boundary": "These legacy scripts are recorded for audit continuity only. They cannot support helium validation, many-electron spectra, CI/correlation closure, or UET atomic prediction claims.",
    }


def build_uet_atomic_operator_readiness_gate(atomic_formula_bridge_manifest: dict) -> dict:
    requirements = [
        {
            "requirement_id": "UET-ATOM-01",
            "name": "constant_origin",
            "required_artifact": "Derive or source-lock the UET role of h, alpha, electron mass, charge, and R_H without treating CODATA inputs as derived outputs.",
            "current_status": "MISSING_DERIVATION",
            "current_evidence": "CODATA constants are source-locked as inputs; the formula bridge does not derive them from UET.",
            "blocking_dependency": ["0.6_Electroweak_Physics", "0.17_Mass_Generation"],
        },
        {
            "requirement_id": "UET-ATOM-02",
            "name": "quantized_action_bridge",
            "required_artifact": "Derive the de Broglie/Bohr standing-wave quantization condition from UET assumptions or explicitly keep it inherited.",
            "current_status": "INHERITED_STANDARD_PHYSICS_ONLY",
            "current_evidence": "atomic_formula_bridge_manifest records de Broglie/Bohr relations as inherited standard physics.",
            "blocking_dependency": ["0.13_Thermodynamic_Bridge", "0.23_Unity_Scale_Link"],
        },
        {
            "requirement_id": "UET-ATOM-03",
            "name": "atomic_hamiltonian_or_operator",
            "required_artifact": "Define a UET atomic Hamiltonian or transition operator that produces level energies and selection rules before holdout evaluation.",
            "current_status": "MISSING_OPERATOR",
            "current_evidence": "No primary-gated UET Hamiltonian or transition-operator artifact exists in 0.20.",
            "blocking_dependency": ["0.13_Thermodynamic_Bridge", "0.6_Electroweak_Physics"],
        },
        {
            "requirement_id": "UET-ATOM-04",
            "name": "correction_terms",
            "required_artifact": "Specify whether UET supplies QED/Lamb, recoil, proton-size, hyperfine, spin-orbit, and electron-correlation corrections or inherits them from standard theory.",
            "current_status": "MISSING_CORRECTION_POLICY",
            "current_evidence": "Current precision gates use standard baselines and empirical handoffs; correction decomposition is not UET-derived.",
            "blocking_dependency": ["0.6_Electroweak_Physics", "0.17_Mass_Generation"],
        },
        {
            "requirement_id": "UET-ATOM-05",
            "name": "parameter_lock_and_holdout_protocol",
            "required_artifact": "Declare all UET parameters before evaluating independent hydrogen-like, helium, and many-electron holdouts.",
            "current_status": "PROTOCOL_MAPPED_MODEL_MISSING",
            "current_evidence": "Predictive closure gate maps no-leakage and holdout requirements, but UET model parameters are absent.",
            "blocking_dependency": ["0.20_Atomic_Physics"],
        },
        {
            "requirement_id": "UET-ATOM-06",
            "name": "residual_and_uncertainty_gate",
            "required_artifact": "Emit source-backed residuals with propagated source/model uncertainty and thresholds for each UET prediction lane.",
            "current_status": "PARTIAL_DIAGNOSTIC_ONLY",
            "current_evidence": "Residual budgets exist for current standard/diagnostic lanes, but no UET operator residual lane exists.",
            "blocking_dependency": ["0.20_Atomic_Physics"],
        },
    ]
    blocking_requirements = [
        row
        for row in requirements
        if row["current_status"] not in {"READY", "PASS_INTERNAL"}
    ]
    return {
        "schema_version": "1.0",
        "role": "uet_atomic_operator_readiness_gate",
        "status": "UET_ATOMIC_OPERATOR_NOT_READY",
        "claim_class": "operator_readiness_and_derivation_gap_map_only",
        "formula_id": "AT20-UET-ATOMIC-OPERATOR-READINESS",
        "dependency_bridge": {
            "formula_bridge_dependency_steps": len(atomic_formula_bridge_manifest["dependency_chain"]),
            "cross_topic_dependencies": [row["topic"] for row in atomic_formula_bridge_manifest["cross_topic_dependencies"]],
            "bridge_claim_boundary": atomic_formula_bridge_manifest["claim_boundary"],
        },
        "requirements": requirements,
        "metrics": {
            "requirement_count": len(requirements),
            "blocking_requirement_count": len(blocking_requirements),
            "ready_requirement_count": len(requirements) - len(blocking_requirements),
            "uet_operator_residual_lane_present": False,
            "codata_constants_treated_as_inputs": True,
        },
        "blocked_claims": [
            "UET derives the Rydberg constant",
            "UET derives h or alpha inside 0.20",
            "UET supplies a validated atomic Hamiltonian",
            "UET predicts hydrogen, helium, or periodic-table spectra from first principles",
        ],
        "claim_boundary": "This gate is a readiness map only. It does not derive an atomic operator; it records the artifacts required before UET-specific atomic prediction claims are allowed.",
    }


def build_atomic_uncertainty_readiness_gate(
    hydrogen_rydberg_line_uncertainty_gate: dict,
    hydrogen_level_energy_benchmark: dict,
    hydrogen_like_checkpoint: dict,
    precision_baseline_gate: dict,
    precision_dirac_baseline_gate: dict,
    lamb_shift_handoff_gate: dict,
    hyperfine_21cm_gate: dict,
    hyperfine_fermi_baseline_gate: dict,
    helium_ground_state_baseline_gate: dict,
    helium_quantum_defect_prediction_gate: dict,
    helium_quantum_defect_holdout_gate: dict,
    helium_quantum_defect_wavelength_holdout_gate: dict,
) -> dict:
    lanes = [
        {
            "lane_id": "hydrogen_rydberg_lines",
            "source_uncertainty_status": "TRANSCRIPTION_ROUNDING_BOUNDS_ONLY",
            "model_uncertainty_status": "NOT_MODELED",
            "propagation_status": "PARTIAL_SOURCE_BOUND_DIAGNOSTIC_ONLY",
            "threshold_status": "FIXED_PPM_THRESHOLD_ONLY",
            "evidence": {
                "line_count": hydrogen_rydberg_line_uncertainty_gate["metrics"]["line_count"],
                "lines_with_source_uncertainty_count": hydrogen_rydberg_line_uncertainty_gate["metrics"][
                    "lines_with_source_uncertainty_count"
                ],
                "max_residual_to_source_uncertainty_ratio": hydrogen_rydberg_line_uncertainty_gate["metrics"][
                    "max_residual_to_source_uncertainty_ratio"
                ],
            },
        },
        {
            "lane_id": "hydrogen_level_energy",
            "source_uncertainty_status": "MISSING_DIRECT_ASD_LEVEL_UNCERTAINTY",
            "model_uncertainty_status": "NOT_MODELED",
            "propagation_status": "BLOCKED",
            "threshold_status": "FIXED_PPM_THRESHOLD_ONLY",
            "evidence": f"{hydrogen_level_energy_benchmark['metrics']['level_count']} rounded n-level rows are benchmarked without direct per-level ASD uncertainty.",
        },
        {
            "lane_id": "hydrogen_like_ions",
            "source_uncertainty_status": "PARTIAL_SOURCE_STATUS_WITHOUT_UNIFIED_UNCERTAINTY",
            "model_uncertainty_status": "FINE_QED_POLICY_OPEN",
            "propagation_status": "BLOCKED",
            "threshold_status": "PROVISIONAL_FIXED_PPM_THRESHOLD",
            "evidence": f"{hydrogen_like_checkpoint['metrics']['primary_benchmark_line_count']} primary He+/Li2+ rows are gated; C VI remains a higher-Z stress lane.",
        },
        {
            "lane_id": "hydrogen_1s2s_precision",
            "source_uncertainty_status": "MEASUREMENT_UNCERTAINTY_RECORDED",
            "model_uncertainty_status": "QED_RECOIL_PROTON_SIZE_MODEL_OPEN",
            "propagation_status": "PARTIAL_SOURCE_SIGMA_DIAGNOSTIC_ONLY",
            "threshold_status": "NO_PRECISION_PASS_THRESHOLD",
            "evidence": {
                "nonrel_sigma_offset": precision_baseline_gate["prediction"]["sigma_offset_vs_measurement_uncertainty"],
                "dirac_sigma_offset": precision_dirac_baseline_gate["prediction"]["sigma_offset_vs_measurement_uncertainty"],
            },
        },
        {
            "lane_id": "hydrogen_lamb_handoff",
            "source_uncertainty_status": "LAMB_SOURCE_UNCERTAINTY_COMBINED",
            "model_uncertainty_status": "EMPIRICAL_HANDOFF_NOT_QED_MODEL",
            "propagation_status": "PARTIAL_DELTA_UNCERTAINTY_ONLY",
            "threshold_status": "NO_QED_CLOSURE_THRESHOLD",
            "evidence": {
                "delta_uncertainty_hz": lamb_shift_handoff_gate["correction"]["delta_uncertainty_hz"],
                "residual_ppm": lamb_shift_handoff_gate["prediction"]["residual_ppm"],
            },
        },
        {
            "lane_id": "hydrogen_21cm_hyperfine",
            "source_uncertainty_status": "REFERENCE_FREQUENCY_UNCERTAINTY_PRESENT_WHERE_RECORDED",
            "model_uncertainty_status": "RECOIL_QED_PROTON_STRUCTURE_OPEN",
            "propagation_status": "BLOCKED",
            "threshold_status": "NO_HYPERFINE_CLOSURE_THRESHOLD",
            "evidence": {
                "reference_frequency_hz": hyperfine_21cm_gate["recommended_frequency"]["value_hz"],
                "fermi_residual_ppm": hyperfine_fermi_baseline_gate["prediction"]["residual_ppm"],
            },
        },
        {
            "lane_id": "helium_ground_state",
            "source_uncertainty_status": "IONIZATION_ENERGY_UNCERTAINTY_COMBINED",
            "model_uncertainty_status": "CORRELATION_RELATIVISTIC_FINITE_MASS_QED_OPEN",
            "propagation_status": "PARTIAL_OBSERVED_BINDING_UNCERTAINTY_ONLY",
            "threshold_status": "NO_CORRELATED_GROUND_CLOSURE_THRESHOLD",
            "evidence": {
                "observed_total_binding_uncertainty_eV": helium_ground_state_baseline_gate["observed_anchor"][
                    "total_binding_uncertainty_eV"
                ],
                "variational_residual_eV": helium_ground_state_baseline_gate["baselines"][1]["absolute_residual_eV"],
            },
        },
        {
            "lane_id": "helium_quantum_defect_levels",
            "source_uncertainty_status": "TRANSCRIPTION_ROUNDING_BOUNDS_FOR_HOLDOUTS_ONLY",
            "model_uncertainty_status": "FITTED_SERIES_PARAMETER_SCATTER_PROPAGATED_DIAGNOSTIC_ONLY",
            "propagation_status": "PARTIAL_FITTED_PARAMETER_SIGMA_DIAGNOSTIC_ONLY",
            "threshold_status": "DIAGNOSTIC_RESIDUALS_ONLY",
            "evidence": {
                "loo_prediction_count": helium_quantum_defect_prediction_gate["metrics"]["prediction_count"],
                "holdout_prediction_count": helium_quantum_defect_holdout_gate["metrics"]["prediction_count"],
                "loo_predictions_with_model_parameter_uncertainty": helium_quantum_defect_prediction_gate["metrics"][
                    "predictions_with_model_parameter_uncertainty_count"
                ],
                "holdout_predictions_with_model_parameter_uncertainty": helium_quantum_defect_holdout_gate["metrics"][
                    "predicted_levels_with_model_parameter_uncertainty_count"
                ],
            },
        },
        {
            "lane_id": "helium_holdout_wavelengths",
            "source_uncertainty_status": "TRANSCRIPTION_ROUNDING_BOUNDS_FOR_HOLDOUT_WAVELENGTHS_ONLY",
            "model_uncertainty_status": "FITTED_LEVEL_UNCERTAINTY_PROPAGATED_TO_WAVELENGTH_DIAGNOSTIC_ONLY",
            "propagation_status": "PARTIAL_LEVEL_TO_WAVELENGTH_SIGMA_DIAGNOSTIC_ONLY",
            "threshold_status": "DIAGNOSTIC_RESIDUALS_ONLY",
            "evidence": {
                "predicted_line_count": helium_quantum_defect_wavelength_holdout_gate["metrics"]["predicted_line_count"],
                "predicted_lines_with_model_parameter_uncertainty": helium_quantum_defect_wavelength_holdout_gate[
                    "metrics"
                ]["predicted_lines_with_model_parameter_uncertainty_count"],
                "max_abs_residual_ppm": helium_quantum_defect_wavelength_holdout_gate["metrics"][
                    "max_abs_wavelength_residual_ppm"
                ],
            },
        },
    ]
    blocked_lanes = [lane for lane in lanes if lane["propagation_status"] == "BLOCKED"]
    partial_lanes = [lane for lane in lanes if lane["propagation_status"].startswith("PARTIAL")]
    return {
        "schema_version": "1.0",
        "role": "atomic_uncertainty_readiness_gate",
        "status": "UNCERTAINTY_READINESS_MAPPED_PROPAGATION_INCOMPLETE",
        "claim_class": "uncertainty_readiness_diagnostic_only",
        "formula_id": "AT20-ATOMIC-UNCERTAINTY-READINESS-GATE",
        "purpose": "Map uncertainty readiness for atomic prediction and precision lanes before any uncertainty-aware spectral prediction claim.",
        "lanes": lanes,
        "metrics": {
            "lane_count": len(lanes),
            "propagation_blocked_lane_count": len(blocked_lanes),
            "partial_propagation_lane_count": len(partial_lanes),
            "lanes_with_source_uncertainty_present_or_partial": sum(
                1
                for lane in lanes
                if "UNCERTAINTY" in lane["source_uncertainty_status"]
                and not lane["source_uncertainty_status"].startswith("MISSING")
            ),
            "lanes_with_model_uncertainty_open": sum(1 for lane in lanes if "OPEN" in lane["model_uncertainty_status"]),
        },
        "next_required_artifacts": [
            "per-row source uncertainty fields for hydrogen/helium spectral lines and term energies",
            "official/source uncertainty replacement for helium transcription-rounding bounds",
            "model-parameter uncertainty for future CI/correlated parameters and non-fitted UET operators",
            "unit-aware propagation from level energies to wavelengths and frequencies for all lanes",
            "uncertainty-aware pass/fail thresholds separated by hydrogen, hydrogen-like ion, helium, and hyperfine lanes",
        ],
        "claim_boundary": "This gate maps uncertainty readiness only. It does not make residuals uncertainty-qualified until propagation rules and thresholds are implemented.",
    }


def build_atomic_residual_uncertainty_budget_gate(
    hydrogen_rydberg_line_uncertainty_gate: dict,
    precision_baseline_gate: dict,
    precision_dirac_baseline_gate: dict,
    lamb_shift_handoff_gate: dict,
    hyperfine_21cm_gate: dict,
    hyperfine_fermi_baseline_gate: dict,
    helium_ground_state_baseline_gate: dict,
    helium_quantum_defect_holdout_gate: dict,
    helium_quantum_defect_wavelength_holdout_gate: dict,
) -> dict:
    """Compute source-uncertainty residual budgets where current sources permit it."""

    def ratio(abs_residual, uncertainty):
        return abs_residual / uncertainty if uncertainty else None

    h_obs_unc_hz = precision_baseline_gate["observed"]["uncertainty_hz"]
    lamb_source_unc_hz = (
        lamb_shift_handoff_gate["correction"]["delta_uncertainty_hz"] ** 2 + h_obs_unc_hz**2
    ) ** 0.5
    hyperfine_cross_check_unc_hz = hyperfine_21cm_gate["metrology_cross_check"].get("uncertainty_hz")
    helium_ground_unc_ev = helium_ground_state_baseline_gate["observed_anchor"]["total_binding_uncertainty_eV"]
    helium_holdout_level_unc_ev = helium_quantum_defect_holdout_gate["metrics"].get(
        "max_source_excitation_uncertainty_eV"
    )
    helium_holdout_wavelength_unc_a = helium_quantum_defect_wavelength_holdout_gate["metrics"].get(
        "max_source_wavelength_uncertainty_angstrom"
    )
    rows = [
        {
            "budget_id": "hydrogen_rydberg_line_transcription_bound",
            "domain": "hydrogen_lines",
            "residual_quantity": "max_abs_wavelength_residual_nm",
            "absolute_residual": hydrogen_rydberg_line_uncertainty_gate["metrics"]["max_abs_wavelength_residual_nm"],
            "source_uncertainty": hydrogen_rydberg_line_uncertainty_gate["metrics"][
                "max_source_wavelength_uncertainty_nm"
            ],
            "source_uncertainty_basis": "transcription rounding bound for local NIST ASD wavelength working copy; official NIST measurement uncertainty not included",
            "residual_to_source_uncertainty_ratio": hydrogen_rydberg_line_uncertainty_gate["metrics"][
                "max_residual_to_source_uncertainty_ratio"
            ],
            "status": "MODEL_RESIDUAL_EXCEEDS_SOURCE_UNCERTAINTY",
            "claim_role": "working-copy precision diagnostic; CODATA R_H input is not a UET derivation",
        },
        {
            "budget_id": "hydrogen_1s2s_nonrel_source_sigma",
            "domain": "hydrogen_precision",
            "residual_quantity": "absolute_residual_hz",
            "absolute_residual": precision_baseline_gate["prediction"]["absolute_residual_hz"],
            "source_uncertainty": h_obs_unc_hz,
            "source_uncertainty_basis": "1S-2S measurement uncertainty only",
            "residual_to_source_uncertainty_ratio": ratio(
                precision_baseline_gate["prediction"]["absolute_residual_hz"], h_obs_unc_hz
            ),
            "status": "MODEL_RESIDUAL_EXCEEDS_SOURCE_UNCERTAINTY",
            "claim_role": "diagnostic gap sizing; nonrelativistic baseline lacks precision corrections",
        },
        {
            "budget_id": "hydrogen_1s2s_dirac_source_sigma",
            "domain": "hydrogen_precision",
            "residual_quantity": "absolute_residual_hz",
            "absolute_residual": precision_dirac_baseline_gate["prediction"]["absolute_residual_hz"],
            "source_uncertainty": h_obs_unc_hz,
            "source_uncertainty_basis": "1S-2S measurement uncertainty only",
            "residual_to_source_uncertainty_ratio": ratio(
                precision_dirac_baseline_gate["prediction"]["absolute_residual_hz"], h_obs_unc_hz
            ),
            "status": "MODEL_RESIDUAL_EXCEEDS_SOURCE_UNCERTAINTY",
            "claim_role": "diagnostic gap sizing; Dirac baseline lacks Lamb/QED/recoil/proton-size terms",
        },
        {
            "budget_id": "hydrogen_1s2s_lamb_handoff_source_sigma",
            "domain": "hydrogen_precision",
            "residual_quantity": "absolute_residual_hz",
            "absolute_residual": lamb_shift_handoff_gate["prediction"]["absolute_residual_hz"],
            "source_uncertainty": lamb_source_unc_hz,
            "source_uncertainty_basis": "quadrature of 1S-2S measurement and empirical Lamb-shift source uncertainties",
            "residual_to_source_uncertainty_ratio": ratio(
                lamb_shift_handoff_gate["prediction"]["absolute_residual_hz"], lamb_source_unc_hz
            ),
            "status": "MODEL_RESIDUAL_EXCEEDS_SOURCE_UNCERTAINTY",
            "claim_role": "empirical handoff diagnostic; residual remains too large for precision closure",
        },
        {
            "budget_id": "hydrogen_21cm_fermi_cross_check_sigma",
            "domain": "hydrogen_hyperfine",
            "residual_quantity": "absolute_residual_hz",
            "absolute_residual": hyperfine_fermi_baseline_gate["prediction"]["absolute_residual_hz"],
            "source_uncertainty": hyperfine_cross_check_unc_hz,
            "source_uncertainty_basis": "metrology cross-check uncertainty only; recommended NIST compilation uncertainty is not separately source-locked",
            "residual_to_source_uncertainty_ratio": ratio(
                hyperfine_fermi_baseline_gate["prediction"]["absolute_residual_hz"], hyperfine_cross_check_unc_hz
            ),
            "status": "MODEL_RESIDUAL_EXCEEDS_SOURCE_UNCERTAINTY",
            "claim_role": "leading Fermi-contact diagnostic; recoil/QED/proton-structure corrections remain open",
        },
        {
            "budget_id": "helium_ground_independent_baseline_source_sigma",
            "domain": "neutral_helium_ground_state",
            "residual_quantity": "absolute_residual_eV",
            "absolute_residual": helium_ground_state_baseline_gate["baselines"][0]["absolute_residual_eV"],
            "source_uncertainty": helium_ground_unc_ev,
            "source_uncertainty_basis": "quadrature of NIST IE1 and IE2 uncertainties",
            "residual_to_source_uncertainty_ratio": ratio(
                helium_ground_state_baseline_gate["baselines"][0]["absolute_residual_eV"], helium_ground_unc_ev
            ),
            "status": "MODEL_RESIDUAL_EXCEEDS_SOURCE_UNCERTAINTY",
            "claim_role": "intentional failure baseline exposing missing electron-electron interaction",
        },
        {
            "budget_id": "helium_ground_variational_baseline_source_sigma",
            "domain": "neutral_helium_ground_state",
            "residual_quantity": "absolute_residual_eV",
            "absolute_residual": helium_ground_state_baseline_gate["baselines"][1]["absolute_residual_eV"],
            "source_uncertainty": helium_ground_unc_ev,
            "source_uncertainty_basis": "quadrature of NIST IE1 and IE2 uncertainties",
            "residual_to_source_uncertainty_ratio": ratio(
                helium_ground_state_baseline_gate["baselines"][1]["absolute_residual_eV"], helium_ground_unc_ev
            ),
            "status": "MODEL_RESIDUAL_EXCEEDS_SOURCE_UNCERTAINTY",
            "claim_role": "uncorrelated variational diagnostic; correlation model remains required",
        },
        {
            "budget_id": "helium_qd_same_source_level_holdout_uncertainty",
            "domain": "neutral_helium_excited_levels",
            "residual_quantity": "absolute_residual_eV",
            "absolute_residual": helium_quantum_defect_holdout_gate["metrics"]["max_abs_excitation_residual_eV"],
            "source_uncertainty": helium_holdout_level_unc_ev,
            "source_uncertainty_basis": (
                "transcription rounding bound for observed holdout level energy; "
                "official NIST measurement uncertainty and model-parameter uncertainty not included"
            ),
            "residual_to_source_uncertainty_ratio": ratio(
                helium_quantum_defect_holdout_gate["metrics"]["max_abs_excitation_residual_eV"],
                helium_holdout_level_unc_ev,
            ),
            "status": (
                "MODEL_RESIDUAL_EXCEEDS_SOURCE_UNCERTAINTY"
                if helium_holdout_level_unc_ev
                else "SOURCE_UNCERTAINTY_MISSING"
            ),
            "claim_role": "same-source-family holdout diagnostic only",
        },
        {
            "budget_id": "helium_qd_wavelength_holdout_uncertainty",
            "domain": "neutral_helium_wavelengths",
            "residual_quantity": "absolute_residual_angstrom",
            "absolute_residual": helium_quantum_defect_wavelength_holdout_gate["metrics"][
                "max_abs_wavelength_residual_angstrom"
            ],
            "source_uncertainty": helium_holdout_wavelength_unc_a,
            "source_uncertainty_basis": (
                "transcription rounding bound for source wavelength; "
                "official NIST measurement uncertainty and model-parameter uncertainty not included"
            ),
            "residual_to_source_uncertainty_ratio": ratio(
                helium_quantum_defect_wavelength_holdout_gate["metrics"]["max_abs_wavelength_residual_angstrom"],
                helium_holdout_wavelength_unc_a,
            ),
            "status": (
                "MODEL_RESIDUAL_EXCEEDS_SOURCE_UNCERTAINTY"
                if helium_holdout_wavelength_unc_a
                else "SOURCE_UNCERTAINTY_MISSING"
            ),
            "claim_role": "same-source-family wavelength holdout diagnostic only",
        },
    ]
    computable_rows = [row for row in rows if row["residual_to_source_uncertainty_ratio"] is not None]
    source_missing_rows = [row for row in rows if row["status"] == "SOURCE_UNCERTAINTY_MISSING"]
    exceeds_rows = [row for row in rows if row["status"] == "MODEL_RESIDUAL_EXCEEDS_SOURCE_UNCERTAINTY"]
    return {
        "schema_version": "1.0",
        "role": "atomic_residual_uncertainty_budget_gate",
        "status": "RESIDUAL_BUDGETS_COMPUTED_CLAIM_STILL_BLOCKED",
        "claim_class": "uncertainty_budget_diagnostic_only",
        "formula_id": "AT20-ATOMIC-RESIDUAL-UNCERTAINTY-BUDGET",
        "purpose": "Convert available source uncertainties into residual-to-uncertainty ratios without promoting incomplete models.",
        "budget_rows": rows,
        "metrics": {
            "budget_row_count": len(rows),
            "computable_source_uncertainty_row_count": len(computable_rows),
            "source_uncertainty_missing_row_count": len(source_missing_rows),
            "model_residual_exceeds_source_uncertainty_count": len(exceeds_rows),
            "max_residual_to_source_uncertainty_ratio": max(
                row["residual_to_source_uncertainty_ratio"] for row in computable_rows
            )
            if computable_rows
            else None,
            "min_residual_to_source_uncertainty_ratio": min(
                row["residual_to_source_uncertainty_ratio"] for row in computable_rows
            )
            if computable_rows
            else None,
        },
        "next_required_artifacts": [
            "source uncertainty capture for same-source and independent helium holdouts",
            "model-parameter uncertainty for fitted quantum defects and future correlated/CI parameters",
            "uncertainty-aware pass/fail thresholds per lane",
            "residual budget rerun after QED, hyperfine, and correlated helium model terms are added",
        ],
        "claim_boundary": "This gate reports residual-to-source-uncertainty budgets only. It does not validate precision spectra, helium, QED, hyperfine structure, or UET first-principles prediction.",
    }


def build_atomic_fixed_parameter_model_readiness_gate(
    hydrogen_like_checkpoint: dict,
    precision_dirac_baseline_gate: dict,
    lamb_shift_handoff_gate: dict,
    hyperfine_fermi_baseline_gate: dict,
    helium_fixed_screening_baseline_gate: dict,
    helium_quantum_defect_prediction_gate: dict,
    helium_quantum_defect_holdout_gate: dict,
    atomic_prediction_baseline_comparator_gate: dict,
    legacy_multielectron_code_audit_gate: dict,
    uet_atomic_operator_readiness_gate: dict,
) -> dict:
    model_lanes = [
        {
            "model_id": "hydrogen_rydberg_codata_fixed_constant",
            "domain": "hydrogen_lines",
            "parameter_policy": "FIXED_FROM_CODATA_BEFORE_EVALUATION",
            "generative_status": "STANDARD_FORMULA_BENCHMARK_ONLY",
            "holdout_status": "INTERNAL_SOURCE_WORKING_COPY",
            "current_role": "accepted hydrogen benchmark, not UET-derived R_H",
            "evidence": "CODATA R_H and NIST/CODATA source hashes are recorded by the primary artifact.",
        },
        {
            "model_id": "hydrogen_like_reduced_mass_fixed_scaling",
            "domain": "one_electron_ions",
            "parameter_policy": "FIXED_CODATA_MASSES_AND_Z_BEFORE_EVALUATION",
            "generative_status": "PROVISIONAL_STANDARD_HYDROGENIC_BENCHMARK",
            "holdout_status": "SELECTED_SOURCE_ROWS_NOT_BROAD_HOLDOUT",
            "current_role": "selected He+/Li2+ benchmark plus C VI stress lane",
            "evidence": {
                "primary_prediction_count": hydrogen_like_checkpoint["metrics"]["primary_benchmark_line_count"],
                "stress_prediction_count": hydrogen_like_checkpoint["metrics"]["extended_stress_test_line_count"],
            },
        },
        {
            "model_id": "hydrogen_1s2s_dirac_fixed_baseline",
            "domain": "hydrogen_precision",
            "parameter_policy": "FIXED_CODATA_ALPHA_AND_R_H_BEFORE_EVALUATION",
            "generative_status": "PARTIAL_STANDARD_BASELINE",
            "holdout_status": "SOURCE_TARGET_DIAGNOSTIC_ONLY",
            "current_role": "sizes missing Lamb/QED/recoil/proton-size corrections",
            "evidence": {
                "dirac_residual_ppm": precision_dirac_baseline_gate["prediction"]["residual_ppm"],
            },
        },
        {
            "model_id": "hydrogen_1s2s_empirical_lamb_handoff",
            "domain": "hydrogen_precision",
            "parameter_policy": "EMPIRICAL_SOURCE_VALUES_INSERTED",
            "generative_status": "NOT_GENERATIVE_QED_MODEL",
            "holdout_status": "NO_INDEPENDENT_HOLDOUT",
            "current_role": "empirical residual handoff only",
            "evidence": {
                "lamb_handoff_residual_ppm": lamb_shift_handoff_gate["prediction"]["residual_ppm"],
            },
        },
        {
            "model_id": "hydrogen_21cm_fermi_fixed_baseline",
            "domain": "hydrogen_hyperfine",
            "parameter_policy": "FIXED_CODATA_AND_NIST_PROTON_G_FACTOR_BEFORE_EVALUATION",
            "generative_status": "LEADING_BASELINE_ONLY",
            "holdout_status": "SOURCE_TARGET_DIAGNOSTIC_ONLY",
            "current_role": "sizes missing recoil/QED/proton-structure corrections",
            "evidence": {
                "fermi_residual_ppm": hyperfine_fermi_baseline_gate["prediction"]["residual_ppm"],
            },
        },
        {
            "model_id": "helium_fixed_screening_baseline",
            "domain": "neutral_helium",
            "parameter_policy": "FIXED_HEURISTIC_SCREENING_BEFORE_EVALUATION",
            "generative_status": "FIXED_PARAMETER_HEURISTIC_BASELINE_ONLY",
            "holdout_status": "SELECTED_SOURCE_TARGET_DIAGNOSTIC_ONLY",
            "current_role": "fixed comparator between zero-quantum-defect and fitted quantum-defect lanes",
            "evidence": {
                "fixed_outer_effective_charge": helium_fixed_screening_baseline_gate["parameter_policy"][
                    "fixed_outer_effective_charge"
                ],
                "average_abs_residual_eV": helium_fixed_screening_baseline_gate["metrics"][
                    "average_abs_binding_residual_eV"
                ],
            },
        },
        {
            "model_id": "helium_quantum_defect_series_fit",
            "domain": "neutral_helium",
            "parameter_policy": "FITTED_FROM_SOURCE_SERIES",
            "generative_status": "NOT_FIXED_PARAMETER_FIRST_PRINCIPLES_MODEL",
            "holdout_status": "SAME_SOURCE_FAMILY_HOLDOUT_ONLY",
            "current_role": "source-calibrated diagnostic; cannot derive quantum defects",
            "evidence": {
                "loo_prediction_count": helium_quantum_defect_prediction_gate["metrics"]["prediction_count"],
                "same_source_holdout_prediction_count": helium_quantum_defect_holdout_gate["metrics"]["prediction_count"],
            },
        },
        {
            "model_id": "legacy_multielectron_three_body_scripts",
            "domain": "neutral_helium",
            "parameter_policy": "NO_SPECTRAL_MODEL_PARAMETERS",
            "generative_status": "LEGACY_SMOKE_TEST_NOT_PRIMARY_EVIDENCE",
            "holdout_status": "NO_SOURCE_HOLDOUT_EVALUATION",
            "current_role": "audit continuity only; explicitly excluded from helium prediction evidence",
            "evidence": {
                "audited_script_count": legacy_multielectron_code_audit_gate["metrics"]["script_count"],
                "primary_evidence_script_count": legacy_multielectron_code_audit_gate["metrics"][
                    "primary_evidence_script_count"
                ],
                "ci_or_correlated_model_present": legacy_multielectron_code_audit_gate["metrics"][
                    "ci_or_correlated_model_present"
                ],
            },
        },
        {
            "model_id": "helium_ci_or_correlated_two_electron_model",
            "domain": "neutral_helium",
            "parameter_policy": "MISSING",
            "generative_status": "REQUIRED_NOT_PRESENT",
            "holdout_status": "BLOCKED",
            "current_role": "required next model family for fixed-parameter helium prediction",
            "evidence": "No in-repo CI/correlated excited-state residual model is primary-gated.",
        },
        {
            "model_id": "uet_atomic_operator",
            "domain": "cross_atomic",
            "parameter_policy": "MISSING",
            "generative_status": "REQUIRED_NOT_PRESENT_FOR_UET_PREDICTION_CLAIM",
            "holdout_status": "BLOCKED",
            "current_role": "required for UET-derived spectra rather than inherited standard formulas",
            "evidence": {
                "operator_readiness_status": uet_atomic_operator_readiness_gate["status"],
                "blocking_requirement_count": uet_atomic_operator_readiness_gate["metrics"][
                    "blocking_requirement_count"
                ],
                "uet_operator_residual_lane_present": uet_atomic_operator_readiness_gate["metrics"][
                    "uet_operator_residual_lane_present"
                ],
            },
        },
    ]
    fixed_or_standard = [
        lane
        for lane in model_lanes
        if lane["parameter_policy"].startswith("FIXED")
        and lane["generative_status"] in {"STANDARD_FORMULA_BENCHMARK_ONLY", "PROVISIONAL_STANDARD_HYDROGENIC_BENCHMARK", "PARTIAL_STANDARD_BASELINE", "LEADING_BASELINE_ONLY"}
    ]
    fixed_heuristics = [lane for lane in model_lanes if lane["parameter_policy"].startswith("FIXED_HEURISTIC")]
    fitted_not_fixed = [lane for lane in model_lanes if lane["parameter_policy"].startswith("FITTED")]
    missing_required = [lane for lane in model_lanes if lane["parameter_policy"] == "MISSING"]
    return {
        "schema_version": "1.0",
        "role": "atomic_fixed_parameter_model_readiness_gate",
        "status": "FIXED_PARAMETER_READINESS_MAPPED_GENERATIVE_MODEL_MISSING",
        "claim_class": "model_readiness_diagnostic_only",
        "formula_id": "AT20-ATOMIC-FIXED-PARAMETER-MODEL-READINESS",
        "purpose": "Separate fixed standard baselines, empirical handoffs, fitted diagnostics, and missing generative models before any predictive atomic-spectrum claim.",
        "model_lanes": model_lanes,
        "metrics": {
            "model_lane_count": len(model_lanes),
            "fixed_or_standard_baseline_count": len(fixed_or_standard),
            "fixed_heuristic_baseline_count": len(fixed_heuristics),
            "fitted_not_fixed_count": len(fitted_not_fixed),
            "missing_required_model_count": len(missing_required),
            "comparator_count": atomic_prediction_baseline_comparator_gate["metrics"]["comparator_count"],
        },
        "next_required_artifacts": [
            "CI/correlated two-electron helium residual gate with parameters declared before holdout evaluation",
            "explicit UET atomic Hamiltonian or transition-operator derivation if UET-specific prediction is claimed",
            "parameter manifest separating constants, calibrated parameters, fitted diagnostics, and forbidden holdout-leakage fields",
            "rerun of comparator and uncertainty gates using the fixed-parameter model output",
        ],
        "claim_boundary": "This gate maps model-readiness only. It does not make fitted quantum defects, empirical Lamb handoffs, or inherited standard formulas into UET first-principles predictions.",
    }


def build_atomic_predictive_model_closure_gate(
    hydrogen_like_checkpoint: dict,
    hydrogen_like_domain_coverage_gate: dict,
    precision_dirac_baseline_gate: dict,
    lamb_shift_handoff_gate: dict,
    hyperfine_fermi_baseline_gate: dict,
    helium_excited_hydrogenic_residual_gate: dict,
    helium_quantum_defect_prediction_gate: dict,
    helium_quantum_defect_holdout_gate: dict,
    helium_quantum_defect_wavelength_holdout_gate: dict,
    atomic_prediction_baseline_comparator_gate: dict,
    atomic_uncertainty_readiness_gate: dict,
    atomic_residual_uncertainty_budget_gate: dict,
    atomic_fixed_parameter_model_readiness_gate: dict,
    legacy_multielectron_code_audit_gate: dict,
    uet_atomic_operator_readiness_gate: dict,
) -> dict:
    closure_checks = [
        {
            "check_id": "AT20-PRED-01",
            "requirement": "Declare calibration rows, holdout rows, and no-leakage split before any spectral prediction claim.",
            "current_state": "PARTIAL",
            "evidence": [
                "selected He I levels have leave-one-out calibration diagnostics",
                "additional He I rows are held out from the selected calibration package",
                "wavelength holdout gate restricts ground-state transitions to avoid lower-level energy leakage",
            ],
            "remaining_blocker": "Holdouts are still from the same NIST source family; independent external rows are missing.",
        },
        {
            "check_id": "AT20-PRED-02",
            "requirement": "Compare every claimed prediction against a named baseline, not only against zero error.",
            "current_state": "PASS_INTERNAL",
            "evidence": [
                "atomic_prediction_baseline_comparator_gate records named baseline/candidate rows",
                f"{atomic_prediction_baseline_comparator_gate['metrics']['comparator_count']} comparator rows are machine-readable",
                "helium zero-quantum-defect, quantum-defect, precision Dirac, empirical Lamb-handoff, and Fermi-contact lanes are compared or explicitly reported as missing stronger comparator",
            ],
            "remaining_blocker": "No CI/correlated helium spectral baseline and no multi-atom periodic-table comparator suite are primary-gated.",
        },
        {
            "check_id": "AT20-PRED-03",
            "requirement": "Use a generative physics model whose parameters are fixed before the holdout set is evaluated.",
            "current_state": "PARTIAL",
            "evidence": [
                "atomic_fixed_parameter_model_readiness_gate separates fixed standard baselines, empirical handoffs, fitted diagnostics, and missing required generative models",
                f"{atomic_fixed_parameter_model_readiness_gate['metrics']['model_lane_count']} model lanes are machine-readable",
                f"{atomic_fixed_parameter_model_readiness_gate['metrics']['missing_required_model_count']} required model lanes remain missing",
                "legacy_multielectron_code_audit_gate classifies existing multi-electron scripts as smoke/demo code, not primary spectral evidence",
                f"uet_atomic_operator_readiness_gate has {uet_atomic_operator_readiness_gate['metrics']['blocking_requirement_count']} blocking requirements",
            ],
            "remaining_blocker": "Readiness is mapped, but a fixed-parameter CI/correlated helium model or explicit UET atomic operator is still missing.",
        },
        {
            "check_id": "AT20-PRED-04",
            "requirement": "Propagate source and model uncertainty into residual thresholds.",
            "current_state": "PARTIAL",
            "evidence": [
                "atomic_uncertainty_readiness_gate maps source/model/propagation/threshold status by lane",
                f"{atomic_uncertainty_readiness_gate['metrics']['lane_count']} uncertainty lanes are machine-readable",
                f"{atomic_uncertainty_readiness_gate['metrics']['propagation_blocked_lane_count']} lanes still have blocked propagation",
                f"atomic_residual_uncertainty_budget_gate computes {atomic_residual_uncertainty_budget_gate['metrics']['computable_source_uncertainty_row_count']} source-uncertainty budget rows",
                f"{atomic_residual_uncertainty_budget_gate['metrics']['source_uncertainty_missing_row_count']} budget rows still lack source uncertainty",
            ],
            "remaining_blocker": "Residual budgets are computed where possible, but source uncertainty, model uncertainty, and uncertainty-aware thresholds are still incomplete.",
        },
        {
            "check_id": "AT20-PRED-05",
            "requirement": "Cover domain expansion from hydrogen to hydrogen-like ions, helium, and multi-electron atoms with separate gates.",
            "current_state": "PARTIAL",
            "evidence": [
                "selected He+ and Li2+ rows pass provisional reduced-mass thresholds",
                "C VI is recorded as a higher-Z stress lane",
                f"hydrogen_like_domain_coverage_gate maps {hydrogen_like_domain_coverage_gate['metrics']['coverage_check_count']} coverage checks",
                "neutral helium source, ground, excited, quantum-defect, and wavelength diagnostics are present",
            ],
            "remaining_blocker": "Broad hydrogen-like ion coverage, direct Li III ASD capture, higher-Z fine/QED policy, and a multi-atom many-electron benchmark suite remain missing.",
        },
    ]
    open_count = sum(1 for row in closure_checks if row["current_state"] in {"PARTIAL", "FAIL_OPEN"})
    fail_open_count = sum(1 for row in closure_checks if row["current_state"] == "FAIL_OPEN")
    return {
        "schema_version": "1.0",
        "role": "atomic_spectral_predictive_model_closure_gate",
        "status": "PREDICTIVE_CLAIM_BLOCKED_REQUIREMENTS_OPEN",
        "claim_class": "governance_gate_no_new_physics_validation",
        "formula_id": "AT20-ATOMIC-PREDICTIVE-CLOSURE-GATE",
        "purpose": "Define the minimum artifact requirements before 0.20 can claim predictive atomic spectra beyond bounded diagnostics.",
        "checks": closure_checks,
        "metrics": {
            "closure_check_count": len(closure_checks),
            "open_or_partial_check_count": open_count,
            "fail_open_check_count": fail_open_count,
            "hydrogen_like_primary_prediction_count": hydrogen_like_checkpoint["metrics"]["primary_benchmark_line_count"],
            "hydrogen_like_domain_coverage_blocking_check_count": hydrogen_like_domain_coverage_gate["metrics"][
                "blocking_coverage_check_count"
            ],
            "hydrogen_like_represented_z_count": hydrogen_like_domain_coverage_gate["metrics"]["represented_z_count"],
            "helium_zero_qd_avg_abs_residual_eV": helium_excited_hydrogenic_residual_gate["metrics"]["average_abs_binding_residual_eV"],
            "helium_quantum_defect_loo_prediction_count": helium_quantum_defect_prediction_gate["metrics"]["prediction_count"],
            "helium_quantum_defect_holdout_prediction_count": helium_quantum_defect_holdout_gate["metrics"]["prediction_count"],
            "helium_wavelength_holdout_prediction_count": helium_quantum_defect_wavelength_holdout_gate["metrics"]["predicted_line_count"],
            "helium_wavelength_holdout_predicted_vacuum_line_count": helium_quantum_defect_wavelength_holdout_gate["metrics"]["predicted_vacuum_line_count"],
            "precision_1s2s_dirac_residual_ppm": precision_dirac_baseline_gate["prediction"]["residual_ppm"],
            "precision_1s2s_lamb_handoff_residual_ppm": lamb_shift_handoff_gate["prediction"]["residual_ppm"],
            "hyperfine_21cm_fermi_residual_ppm": hyperfine_fermi_baseline_gate["prediction"]["residual_ppm"],
            "uncertainty_readiness_lane_count": atomic_uncertainty_readiness_gate["metrics"]["lane_count"],
            "uncertainty_propagation_blocked_lane_count": atomic_uncertainty_readiness_gate["metrics"][
                "propagation_blocked_lane_count"
            ],
            "uncertainty_budget_row_count": atomic_residual_uncertainty_budget_gate["metrics"]["budget_row_count"],
            "uncertainty_budget_computable_row_count": atomic_residual_uncertainty_budget_gate["metrics"][
                "computable_source_uncertainty_row_count"
            ],
            "uncertainty_budget_source_missing_row_count": atomic_residual_uncertainty_budget_gate["metrics"][
                "source_uncertainty_missing_row_count"
            ],
            "fixed_parameter_model_lane_count": atomic_fixed_parameter_model_readiness_gate["metrics"]["model_lane_count"],
            "missing_required_model_count": atomic_fixed_parameter_model_readiness_gate["metrics"][
                "missing_required_model_count"
            ],
            "legacy_multielectron_scripts_audited": legacy_multielectron_code_audit_gate["metrics"]["scripts_present"],
            "legacy_multielectron_primary_evidence_script_count": legacy_multielectron_code_audit_gate["metrics"][
                "primary_evidence_script_count"
            ],
            "uet_atomic_operator_blocking_requirement_count": uet_atomic_operator_readiness_gate["metrics"][
                "blocking_requirement_count"
            ],
            "uet_operator_residual_lane_present": uet_atomic_operator_readiness_gate["metrics"][
                "uet_operator_residual_lane_present"
            ],
        },
        "promotion_requirements": [
            "independent external helium holdout rows with source locators and hashes",
            "uncertainty propagation for level energies, wavelengths, QED corrections, and hyperfine residuals",
            "CI/correlated two-electron spectral model or explicit UET atomic operator with fixed parameters before holdout evaluation",
            "baseline comparator table covering zero-quantum-defect, empirical quantum-defect, CI/correlated, and any UET correction lane",
            "multi-atom benchmark suite split by one-electron ions, two-electron atoms, alkali-like atoms, and heavier many-electron systems",
        ],
        "blocked_claims": [
            "UET predicts all atomic spectra",
            "0.20 validates periodic-table spectra",
            "helium spectra are solved from first principles",
            "quantum defects are derived rather than source-calibrated",
            "precision QED/hyperfine corrections are closed",
        ],
        "claim_boundary": "This gate is a closure contract only. It records what a predictive atomic model must prove and keeps current 0.20 evidence at diagnostic/benchmark status.",
    }


def build_atomic_predictive_model_spec_gate(
    atomic_predictive_model_closure_gate: dict,
    atomic_fixed_parameter_model_readiness_gate: dict,
    uet_atomic_operator_readiness_gate: dict,
    hydrogen_like_domain_coverage_gate: dict,
    atomic_uncertainty_readiness_gate: dict,
) -> dict:
    model_contract = {
        "model_form": "E_or_nu_pred = standard_baseline(domain, constants, quantum_numbers) + delta_uet_or_ci(domain, locked_parameters, quantum_numbers)",
        "baseline_requirement": "Use the strongest applicable named standard baseline before adding any UET correction term.",
        "correction_requirement": (
            "The correction term must be declared as a Hamiltonian/operator, energy-level correction, or transition-frequency "
            "correction with units before holdout rows are evaluated."
        ),
        "parameter_requirement": "All fitted, calibrated, inherited, and forbidden holdout-leakage parameters must be listed before evaluation.",
        "evaluation_requirement": "Every prediction lane must include holdout rows, named baseline comparator rows, uncertainty propagation, and fixed thresholds.",
    }
    development_lanes = [
        {
            "lane_id": "one_electron_hydrogenic",
            "baseline": "reduced-mass Rydberg/Bohr relation",
            "current_artifacts": ["hydrogen_like_checkpoint", "hydrogen_like_domain_coverage_gate"],
            "ready_state": "PARTIAL",
            "next_model_step": "Add direct Li III source capture and multi-transition hydrogen-like rows before fitting or claiming new corrections.",
        },
        {
            "lane_id": "hydrogen_precision",
            "baseline": "Dirac baseline plus explicit QED/Lamb/recoil/proton-size correction decomposition",
            "current_artifacts": ["precision_dirac_baseline_gate", "lamb_shift_handoff_gate", "hyperfine_fermi_baseline_gate"],
            "ready_state": "BLOCKED_MODEL_MISSING",
            "next_model_step": "Replace empirical handoff with source-backed correction decomposition and uncertainty propagation.",
        },
        {
            "lane_id": "helium_two_electron",
            "baseline": "CI/correlated two-electron Hamiltonian or declared UET atomic operator",
            "current_artifacts": [
                "helium_ground_state_baseline_gate",
                "helium_quantum_defect_prediction_gate",
                "helium_quantum_defect_holdout_gate",
            ],
            "ready_state": "BLOCKED_GENERATIVE_MODEL_MISSING",
            "next_model_step": "Add fixed-parameter CI/correlated residual gate or a UET operator that predicts quantum defects rather than fitting them.",
        },
        {
            "lane_id": "periodic_table_expansion",
            "baseline": "domain-split suites for one-electron ions, two-electron atoms, alkali-like atoms, and heavier many-electron systems",
            "current_artifacts": ["atomic_predictive_model_closure_gate"],
            "ready_state": "BLOCKED_DOMAIN_PACKAGE_MISSING",
            "next_model_step": "Build a multi-atom source package with train/holdout splits and comparator baselines per atomic family.",
        },
    ]
    implementation_blockers = [
        {
            "blocker_id": "uet_operator_absent",
            "status": "BLOCKING",
            "evidence": f"{uet_atomic_operator_readiness_gate['metrics']['blocking_requirement_count']} UET operator requirements remain blocking.",
            "required_artifact": "UET Hamiltonian/transition-operator derivation with units and fixed parameter policy.",
        },
        {
            "blocker_id": "fixed_parameter_model_missing",
            "status": "BLOCKING",
            "evidence": f"{atomic_fixed_parameter_model_readiness_gate['metrics']['missing_required_model_count']} required model lanes are missing.",
            "required_artifact": "Fixed-parameter CI/correlated or UET spectral residual gate.",
        },
        {
            "blocker_id": "uncertainty_thresholds_incomplete",
            "status": "BLOCKING",
            "evidence": f"{atomic_uncertainty_readiness_gate['metrics']['propagation_blocked_lane_count']} uncertainty lanes still block propagation.",
            "required_artifact": "Uncertainty-aware residual thresholds for each prediction lane.",
        },
        {
            "blocker_id": "domain_coverage_incomplete",
            "status": "BLOCKING",
            "evidence": f"{hydrogen_like_domain_coverage_gate['metrics']['blocking_coverage_check_count']} hydrogen-like coverage checks remain blocking.",
            "required_artifact": "Multi-ion and multi-transition source packages with fine/QED policy.",
        },
    ]
    blocking_count = sum(1 for row in implementation_blockers if row["status"] == "BLOCKING")
    lane_blocking_count = sum(1 for row in development_lanes if row["ready_state"].startswith("BLOCKED"))
    return {
        "schema_version": "1.0",
        "role": "atomic_predictive_model_specification_gate",
        "status": "SPEC_MAPPED_IMPLEMENTATION_BLOCKED",
        "claim_class": "model_specification_only",
        "formula_id": "AT20-ATOMIC-PREDICTIVE-MODEL-SPEC",
        "model_contract": model_contract,
        "development_lanes": development_lanes,
        "implementation_blockers": implementation_blockers,
        "metrics": {
            "development_lane_count": len(development_lanes),
            "development_lanes_blocked": lane_blocking_count,
            "implementation_blocker_count": len(implementation_blockers),
            "blocking_implementation_blocker_count": blocking_count,
            "closure_checks_open_or_partial": atomic_predictive_model_closure_gate["metrics"][
                "open_or_partial_check_count"
            ],
            "fixed_parameter_missing_required_model_count": atomic_fixed_parameter_model_readiness_gate["metrics"][
                "missing_required_model_count"
            ],
            "uet_operator_blocking_requirement_count": uet_atomic_operator_readiness_gate["metrics"][
                "blocking_requirement_count"
            ],
            "hydrogen_like_domain_coverage_blocking_check_count": hydrogen_like_domain_coverage_gate["metrics"][
                "blocking_coverage_check_count"
            ],
            "uncertainty_propagation_blocked_lane_count": atomic_uncertainty_readiness_gate["metrics"][
                "propagation_blocked_lane_count"
            ],
        },
        "minimum_first_implementation": [
            "Pick one narrow lane, preferably one-electron hydrogen-like ions or helium two-electron residuals.",
            "Freeze constants and parameters before reading holdout rows.",
            "Emit predictions for held-out transitions with baseline comparator residuals.",
            "Propagate source and model uncertainty into the threshold decision.",
            "Record any UET correction as an explicit operator/correction term with units, not as narrative interpretation.",
        ],
        "claim_boundary": "This gate specifies how a predictive atomic model must be built. It does not implement the missing UET operator or upgrade current diagnostics into broad predictions.",
    }


def build_atomic_first_predictive_implementation_candidate_gate(
    atomic_predictive_model_spec_gate: dict,
    helium_quantum_defect_prediction_gate: dict,
    helium_quantum_defect_holdout_gate: dict,
    helium_quantum_defect_wavelength_holdout_gate: dict,
    atomic_prediction_baseline_comparator_gate: dict,
    atomic_residual_uncertainty_budget_gate: dict,
) -> dict:
    candidate_lanes = [
        {
            "lane_id": "helium_quantum_defect_source_family_holdout",
            "model_form": "E_bind_pred = h c R_infinity / (n - delta_selected_series)^2",
            "parameter_source": "delta_selected_series fitted from selected NIST He I calibration levels before holdout evaluation",
            "baseline": "zero-quantum-defect hydrogenic baseline",
            "holdout_type": "same_source_family",
            "readiness": "CANDIDATE_READY_DIAGNOSTIC_ONLY",
            "evidence": {
                "calibration_prediction_count": helium_quantum_defect_prediction_gate["metrics"]["prediction_count"],
                "level_holdout_prediction_count": helium_quantum_defect_holdout_gate["metrics"]["prediction_count"],
                "wavelength_holdout_prediction_count": helium_quantum_defect_wavelength_holdout_gate["metrics"][
                    "predicted_line_count"
                ],
                "source_uncertainty_policy_status": helium_quantum_defect_holdout_gate["metrics"].get(
                    "source_uncertainty_policy_status"
                ),
            },
            "claim_ceiling": "same-source-family diagnostic only; not independent helium validation",
        },
        {
            "lane_id": "hydrogen_like_multi_transition_holdout",
            "model_form": "reduced-mass Rydberg baseline plus future correction policy",
            "parameter_source": "no fit allowed until multi-transition source package exists",
            "baseline": "reduced-mass hydrogenic Rydberg relation",
            "holdout_type": "missing",
            "readiness": "BLOCKED_SOURCE_PACKAGE_MISSING",
            "evidence": {
                "reason": "current hydrogen-like package has only 2 -> 1 rows for Z=2,3,6",
            },
            "claim_ceiling": "coverage diagnostic only",
        },
        {
            "lane_id": "explicit_uet_atomic_operator_holdout",
            "model_form": "standard_baseline + delta_uet(domain, locked_parameters, quantum_numbers)",
            "parameter_source": "UET operator parameters must be locked before holdout evaluation",
            "baseline": "strongest applicable standard baseline",
            "holdout_type": "missing",
            "readiness": "BLOCKED_OPERATOR_MISSING",
            "evidence": {
                "reason": "atomic_predictive_model_spec_gate marks implementation blocked",
                "blocking_implementation_blockers": atomic_predictive_model_spec_gate["metrics"][
                    "blocking_implementation_blocker_count"
                ],
            },
            "claim_ceiling": "specification only",
        },
    ]
    selected = candidate_lanes[0]
    success_criteria = [
        {
            "criterion_id": "FIT-01",
            "description": "Parameters are fitted only from calibration rows and not from holdout rows.",
            "status": "READY_DIAGNOSTIC",
            "evidence": "helium holdout gate uses selected-series calibration deltas and skips rows without a selected calibration series",
        },
        {
            "criterion_id": "HOLDOUT-01",
            "description": "Holdout predictions exist for levels and at least one spectral line.",
            "status": "READY_DIAGNOSTIC",
            "evidence": {
                "level_holdout_prediction_count": helium_quantum_defect_holdout_gate["metrics"]["prediction_count"],
                "wavelength_holdout_prediction_count": helium_quantum_defect_wavelength_holdout_gate["metrics"][
                    "predicted_line_count"
                ],
            },
        },
        {
            "criterion_id": "BASELINE-01",
            "description": "Candidate residuals are compared to a named baseline.",
            "status": "READY_INTERNAL",
            "evidence": f"{atomic_prediction_baseline_comparator_gate['metrics']['comparator_count']} comparator rows are present",
        },
        {
            "criterion_id": "UNCERTAINTY-01",
            "description": "Source and model uncertainty are recorded, but thresholds are not yet uncertainty-qualified.",
            "status": "PARTIAL",
            "evidence": {
                "source_uncertainty_policy_status": helium_quantum_defect_holdout_gate["metrics"].get(
                    "source_uncertainty_policy_status"
                ),
                "residual_budget_rows": atomic_residual_uncertainty_budget_gate["metrics"]["budget_row_count"],
            },
        },
        {
            "criterion_id": "EXTERNAL-01",
            "description": "Independent external validation source exists.",
            "status": "BLOCKED",
            "evidence": "current holdout rows are same-source-family NIST rows",
        },
    ]
    blocking_criteria = [row for row in success_criteria if row["status"] == "BLOCKED"]
    partial_criteria = [row for row in success_criteria if row["status"] == "PARTIAL"]
    return {
        "schema_version": "1.0",
        "role": "atomic_first_predictive_implementation_candidate_gate",
        "status": "FIRST_IMPLEMENTATION_CANDIDATE_SELECTED_EXTERNAL_VALIDATION_BLOCKED",
        "claim_class": "implementation_candidate_diagnostic_only",
        "formula_id": "AT20-ATOMIC-FIRST-PREDICTIVE-IMPLEMENTATION-CANDIDATE",
        "selected_lane_id": selected["lane_id"],
        "candidate_lanes": candidate_lanes,
        "success_criteria": success_criteria,
        "metrics": {
            "candidate_lane_count": len(candidate_lanes),
            "ready_diagnostic_lane_count": sum(
                1 for row in candidate_lanes if row["readiness"] == "CANDIDATE_READY_DIAGNOSTIC_ONLY"
            ),
            "blocked_candidate_lane_count": sum(1 for row in candidate_lanes if row["readiness"].startswith("BLOCKED")),
            "success_criterion_count": len(success_criteria),
            "partial_success_criterion_count": len(partial_criteria),
            "blocking_success_criterion_count": len(blocking_criteria),
            "selected_level_holdout_prediction_count": helium_quantum_defect_holdout_gate["metrics"]["prediction_count"],
            "selected_wavelength_holdout_prediction_count": helium_quantum_defect_wavelength_holdout_gate["metrics"][
                "predicted_line_count"
            ],
            "selected_level_holdout_avg_abs_residual_eV": helium_quantum_defect_holdout_gate["metrics"][
                "average_abs_excitation_residual_eV"
            ],
            "selected_wavelength_holdout_avg_abs_residual_angstrom": helium_quantum_defect_wavelength_holdout_gate[
                "metrics"
            ]["average_abs_wavelength_residual_angstrom"],
        },
        "next_required_artifacts": [
            "independent external He I holdout source package with hashes and source locators",
            "uncertainty-aware thresholds for level and wavelength holdout residuals",
            "CI/correlated two-electron or explicit UET operator lane that predicts quantum defects rather than fitting them",
            "same candidate-lane report rerun after external holdouts and model uncertainty are added",
        ],
        "claim_boundary": "This gate selects the most practical first implementation lane from current evidence. It does not promote same-source-family helium diagnostics into independent validation or first-principles UET prediction.",
    }


def build_atomic_predictive_v1_parameter_lock_gate(
    parameter_manifest: dict,
    atomic_first_predictive_implementation_candidate_gate: dict,
    helium_quantum_defect_holdout_gate: dict,
    helium_external_holdout_residual_crosscheck_gate: dict,
) -> dict:
    constants = parameter_manifest.get("constants", [])
    calibrated_parameters = parameter_manifest.get("calibrated_parameters", [])
    future_required = parameter_manifest.get("future_locked_parameters_required", [])
    forbidden_fields = parameter_manifest.get("forbidden_leakage_fields", [])
    missing_future = [row for row in future_required if row.get("current_status") == "missing"]
    leakage_policy_present = bool(forbidden_fields) and all(
        "holdout" in field or "external_holdouts" in field for field in forbidden_fields
    )
    selected_lane_match = (
        parameter_manifest.get("selected_lane_id")
        == "helium_quantum_defect_then_ci_or_uet_correction_v1"
        and atomic_first_predictive_implementation_candidate_gate["selected_lane_id"]
        == parameter_manifest.get("current_diagnostic_lane_id")
    )
    policy_checks = [
        {
            "check_id": "PARAM-01",
            "requirement": "Selected manifest lane must match the first implementation candidate.",
            "status": "PASS" if selected_lane_match else "FAIL",
            "evidence": {
                "manifest_selected_lane_id": parameter_manifest.get("selected_lane_id"),
                "manifest_current_diagnostic_lane_id": parameter_manifest.get("current_diagnostic_lane_id"),
                "candidate_selected_lane_id": atomic_first_predictive_implementation_candidate_gate["selected_lane_id"],
            },
        },
        {
            "check_id": "PARAM-02",
            "requirement": "Constants must be marked as inherited/not fitted before holdout evaluation.",
            "status": "PASS" if constants and all(row.get("fit_status") == "not_fitted" for row in constants) else "FAIL",
            "evidence": {"constant_count": len(constants)},
        },
        {
            "check_id": "PARAM-03",
            "requirement": "Calibrated parameters must identify calibration source and holdout leakage policy.",
            "status": "PASS"
            if calibrated_parameters
            and all(row.get("calibration_source_path") and row.get("holdout_leakage_policy") for row in calibrated_parameters)
            else "FAIL",
            "evidence": {"calibrated_parameter_count": len(calibrated_parameters)},
        },
        {
            "check_id": "PARAM-04",
            "requirement": "Forbidden holdout/external fields must be listed before validation claims.",
            "status": "PASS" if leakage_policy_present else "FAIL",
            "evidence": {"forbidden_leakage_field_count": len(forbidden_fields)},
        },
        {
            "check_id": "PARAM-05",
            "requirement": "Future CI/correlated or UET correction parameters must remain explicit blockers until implemented.",
            "status": "PARTIAL_BLOCKED_GENERATIVE_MODEL_MISSING" if missing_future else "PASS",
            "evidence": {"missing_future_locked_parameter_count": len(missing_future)},
        },
    ]
    fail_count = sum(1 for row in policy_checks if row["status"] == "FAIL")
    partial_count = sum(1 for row in policy_checks if row["status"].startswith("PARTIAL"))
    status = (
        "PARAMETER_LOCK_POLICY_FAIL"
        if fail_count
        else "PARAMETER_MANIFEST_READY_GENERATIVE_MODEL_MISSING"
        if partial_count
        else "PARAMETER_MANIFEST_READY"
    )
    return {
        "schema_version": "1.0",
        "role": "atomic_predictive_v1_parameter_lock_gate",
        "status": status,
        "claim_class": "parameter_lock_diagnostic_only",
        "formula_id": "AT20-ATOMIC-PREDICTIVE-V1-PARAMETER-LOCK",
        "manifest": {
            "path": str(ATOMIC_PREDICTIVE_V1_PARAMETER_MANIFEST_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
            "sha256": file_sha256(ATOMIC_PREDICTIVE_V1_PARAMETER_MANIFEST_PATH),
            "manifest_id": parameter_manifest.get("manifest_id"),
            "selected_lane_id": parameter_manifest.get("selected_lane_id"),
            "current_diagnostic_lane_id": parameter_manifest.get("current_diagnostic_lane_id"),
        },
        "policy_checks": policy_checks,
        "metrics": {
            "constant_count": len(constants),
            "calibrated_parameter_count": len(calibrated_parameters),
            "future_locked_parameter_required_count": len(future_required),
            "missing_future_locked_parameter_count": len(missing_future),
            "forbidden_leakage_field_count": len(forbidden_fields),
            "policy_check_count": len(policy_checks),
            "policy_fail_count": fail_count,
            "policy_partial_count": partial_count,
            "same_source_level_holdout_prediction_count": helium_quantum_defect_holdout_gate["metrics"][
                "prediction_count"
            ],
            "external_crosscheck_row_count": helium_external_holdout_residual_crosscheck_gate["metrics"][
                "crosscheck_row_count"
            ],
        },
        "next_required_artifacts": [
            row["required_artifact"] for row in missing_future if row.get("required_artifact")
        ]
        + [
            "rerun v1 fixed-correction report after fixed correction parameters are added",
            "source-lineage gate proving whether external rows are independent or cross-check-only",
        ],
        "blocked_claims": parameter_manifest.get("blocked_claims", []),
        "claim_boundary": parameter_manifest.get("claim_boundary"),
    }


def build_atomic_predictive_v1_threshold_gate(
    threshold_manifest: dict,
    helium_quantum_defect_holdout_gate: dict,
    helium_quantum_defect_wavelength_holdout_gate: dict,
    atomic_predictive_v1_parameter_lock_gate: dict,
) -> dict:
    current_metric_values = {
        "max_abs_excitation_residual_eV": helium_quantum_defect_holdout_gate["metrics"][
            "max_abs_excitation_residual_eV"
        ],
        "max_abs_wavelength_residual_angstrom": helium_quantum_defect_wavelength_holdout_gate["metrics"][
            "max_abs_wavelength_residual_angstrom"
        ],
        "max_abs_wavelength_residual_ppm": helium_quantum_defect_wavelength_holdout_gate["metrics"][
            "max_abs_wavelength_residual_ppm"
        ],
    }
    threshold_rows = []
    for row in threshold_manifest.get("thresholds", []):
        metric = row["metric"]
        current_value = current_metric_values.get(metric)
        if current_value is None:
            comparison_status = "MISSING_METRIC"
            passes = False
        elif row["operator"] == "<=":
            passes = current_value <= row["value"]
            comparison_status = "PASS_DIAGNOSTIC" if passes else "FAIL_DIAGNOSTIC"
        else:
            passes = False
            comparison_status = "UNSUPPORTED_OPERATOR"
        threshold_rows.append(
            {
                "threshold_id": row["threshold_id"],
                "lane": row["lane"],
                "metric": metric,
                "operator": row["operator"],
                "threshold_value": row["value"],
                "unit": row["unit"],
                "current_value": current_value,
                "comparison_status": comparison_status,
                "validation_ready": row.get("validation_ready", False),
                "basis": row.get("basis"),
            }
        )
    diagnostic_pass_count = sum(1 for row in threshold_rows if row["comparison_status"] == "PASS_DIAGNOSTIC")
    diagnostic_fail_count = sum(1 for row in threshold_rows if row["comparison_status"] == "FAIL_DIAGNOSTIC")
    validation_ready_count = sum(1 for row in threshold_rows if row["validation_ready"])
    status = (
        "THRESHOLD_DIAGNOSTIC_FAIL"
        if diagnostic_fail_count
        else "THRESHOLD_MANIFEST_READY_DIAGNOSTIC_ONLY_VALIDATION_BLOCKED"
    )
    return {
        "schema_version": "1.0",
        "role": "atomic_predictive_v1_threshold_gate",
        "status": status,
        "claim_class": "threshold_manifest_diagnostic_only",
        "formula_id": "AT20-ATOMIC-PREDICTIVE-V1-THRESHOLD-GATE",
        "manifest": {
            "path": str(ATOMIC_PREDICTIVE_V1_THRESHOLD_MANIFEST_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
            "sha256": file_sha256(ATOMIC_PREDICTIVE_V1_THRESHOLD_MANIFEST_PATH),
            "manifest_id": threshold_manifest.get("manifest_id"),
            "selected_lane_id": threshold_manifest.get("selected_lane_id"),
            "current_diagnostic_lane_id": threshold_manifest.get("current_diagnostic_lane_id"),
            "validation_use_allowed": threshold_manifest.get("threshold_policy", {}).get("validation_use_allowed"),
        },
        "threshold_rows": threshold_rows,
        "metrics": {
            "threshold_count": len(threshold_rows),
            "diagnostic_pass_count": diagnostic_pass_count,
            "diagnostic_fail_count": diagnostic_fail_count,
            "validation_ready_threshold_count": validation_ready_count,
            "parameter_lock_missing_future_parameter_count": atomic_predictive_v1_parameter_lock_gate["metrics"][
                "missing_future_locked_parameter_count"
            ],
            "max_level_residual_eV": current_metric_values["max_abs_excitation_residual_eV"],
            "max_wavelength_residual_angstrom": current_metric_values["max_abs_wavelength_residual_angstrom"],
            "max_wavelength_residual_ppm": current_metric_values["max_abs_wavelength_residual_ppm"],
        },
        "required_for_validation_upgrade": threshold_manifest.get("required_for_validation_upgrade", []),
        "blocked_claims": threshold_manifest.get("blocked_claims", []),
        "claim_boundary": threshold_manifest.get("claim_boundary"),
    }


def build_atomic_predictive_v1_fixed_correction_operator_gate(
    operator_manifest: dict,
    atomic_predictive_v1_parameter_lock_gate: dict,
    atomic_fixed_parameter_model_readiness_gate: dict,
    uet_atomic_operator_readiness_gate: dict,
) -> dict:
    candidates = operator_manifest.get("operator_candidates", [])
    accepted_candidates = [row for row in candidates if row.get("accepted_as_delta_uet_or_ci")]
    missing_candidates = [row for row in candidates if row.get("current_status") == "MISSING"]
    diagnostic_only_candidates = [
        row for row in candidates if row.get("current_status", "").startswith("DIAGNOSTIC_ONLY")
    ]
    contract = operator_manifest.get("operator_contract", {})
    contract_checks = [
        {
            "check_id": "OPERATOR-01",
            "requirement": "The required correction operator ID and model form must be declared.",
            "status": "PASS" if contract.get("required_operator_id") == "delta_uet_or_ci" else "FAIL",
            "evidence": {
                "required_operator_id": contract.get("required_operator_id"),
                "required_model_form": operator_manifest.get("required_model_form"),
            },
        },
        {
            "check_id": "OPERATOR-02",
            "requirement": "At least one accepted fixed CI/correlated or explicit UET correction operator must be implemented before validation claims.",
            "status": "BLOCKED_NO_ACCEPTED_FIXED_CORRECTION_OPERATOR"
            if not accepted_candidates
            else "PASS",
            "evidence": {
                "accepted_operator_count": len(accepted_candidates),
                "missing_candidate_count": len(missing_candidates),
                "diagnostic_only_candidate_count": len(diagnostic_only_candidates),
            },
        },
        {
            "check_id": "OPERATOR-03",
            "requirement": "The current empirical quantum-defect lane must not be treated as delta_uet_or_ci.",
            "status": "PASS"
            if all(not row.get("accepted_as_delta_uet_or_ci") for row in diagnostic_only_candidates)
            else "FAIL",
            "evidence": [row["candidate_id"] for row in diagnostic_only_candidates],
        },
        {
            "check_id": "OPERATOR-04",
            "requirement": "Parameter-lock gate must keep future correction parameters as explicit blockers while the operator is missing.",
            "status": "PASS"
            if atomic_predictive_v1_parameter_lock_gate["metrics"]["missing_future_locked_parameter_count"] >= 1
            else "FAIL",
            "evidence": atomic_predictive_v1_parameter_lock_gate["metrics"][
                "missing_future_locked_parameter_count"
            ],
        },
        {
            "check_id": "OPERATOR-05",
            "requirement": "UET operator readiness must remain blocking until derivation/residual artifacts exist.",
            "status": "PASS"
            if uet_atomic_operator_readiness_gate["metrics"]["blocking_requirement_count"] > 0
            else "FAIL",
            "evidence": {
                "uet_blocking_requirement_count": uet_atomic_operator_readiness_gate["metrics"][
                    "blocking_requirement_count"
                ],
                "uet_operator_residual_lane_present": uet_atomic_operator_readiness_gate["metrics"][
                    "uet_operator_residual_lane_present"
                ],
            },
        },
    ]
    fail_count = sum(1 for row in contract_checks if row["status"] == "FAIL")
    blocking_count = sum(1 for row in contract_checks if row["status"].startswith("BLOCKED"))
    status = (
        "OPERATOR_CONTRACT_FAIL"
        if fail_count
        else "OPERATOR_CONTRACT_READY_IMPLEMENTATION_MISSING"
        if blocking_count
        else "OPERATOR_CONTRACT_READY"
    )
    return {
        "schema_version": "1.0",
        "role": "atomic_predictive_v1_fixed_correction_operator_gate",
        "status": status,
        "claim_class": "fixed_correction_operator_contract_no_validation_claim",
        "formula_id": "AT20-ATOMIC-PREDICTIVE-V1-FIXED-CORRECTION-OPERATOR",
        "manifest": {
            "path": str(ATOMIC_PREDICTIVE_V1_OPERATOR_MANIFEST_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
            "sha256": file_sha256(ATOMIC_PREDICTIVE_V1_OPERATOR_MANIFEST_PATH),
            "manifest_id": operator_manifest.get("manifest_id"),
            "selected_lane_id": operator_manifest.get("selected_lane_id"),
            "required_model_form": operator_manifest.get("required_model_form"),
        },
        "operator_contract": contract,
        "operator_candidates": candidates,
        "contract_checks": contract_checks,
        "metrics": {
            "operator_candidate_count": len(candidates),
            "accepted_operator_count": len(accepted_candidates),
            "missing_operator_candidate_count": len(missing_candidates),
            "diagnostic_only_candidate_count": len(diagnostic_only_candidates),
            "contract_check_count": len(contract_checks),
            "contract_fail_count": fail_count,
            "contract_blocking_count": blocking_count,
            "fixed_parameter_missing_required_model_count": atomic_fixed_parameter_model_readiness_gate["metrics"][
                "missing_required_model_count"
            ],
            "uet_operator_blocking_requirement_count": uet_atomic_operator_readiness_gate["metrics"][
                "blocking_requirement_count"
            ],
        },
        "pass_conditions_for_validation_upgrade": operator_manifest.get("pass_conditions_for_validation_upgrade", []),
        "blocked_claims": operator_manifest.get("blocked_claims", []),
        "next_required_artifacts": [
            row.get("required_artifact") for row in missing_candidates if row.get("required_artifact")
        ]
        + [
            "operator residual lane consumed by atomic_predictive_v1_diagnostic_report_gate",
            "validation-ready threshold manifest after operator uncertainty is available",
        ],
        "claim_boundary": operator_manifest.get("claim_boundary"),
    }


def build_atomic_predictive_v1_operator_candidate_resolution_gate(
    operator_manifest: dict,
    atomic_fixed_parameter_model_readiness_gate: dict,
    atomic_prediction_baseline_comparator_gate: dict,
    atomic_predictive_v1_fixed_correction_operator_gate: dict,
    uet_atomic_operator_readiness_gate: dict,
) -> dict:
    model_lanes = {
        row["model_id"]: row for row in atomic_fixed_parameter_model_readiness_gate.get("model_lanes", [])
    }
    manifest_candidates = {
        row["candidate_id"]: row for row in operator_manifest.get("operator_candidates", [])
    }
    resolution_rows = [
        {
            "candidate_id": "standard_bohr_rydberg_hydrogenic_baseline",
            "candidate_source": "formula bridge and hydrogen/hydrogen-like baseline gates",
            "current_use": "standard_baseline",
            "delta_uet_or_ci_resolution": "REJECTED_AS_DELTA_BASELINE_ONLY",
            "accepted_as_delta_uet_or_ci": False,
            "reason": "Bohr/Rydberg/hydrogenic formulas define the baseline side of the model equation, not the correction operator.",
            "evidence": {
                "hydrogen_like_comparator_count": atomic_prediction_baseline_comparator_gate["metrics"][
                    "comparator_count"
                ],
            },
        },
        {
            "candidate_id": "hydrogen_dirac_lamb_empirical_handoff",
            "candidate_source": "precision baseline and Lamb handoff gates",
            "current_use": "precision_gap_sizing_diagnostic",
            "delta_uet_or_ci_resolution": "REJECTED_AS_DELTA_EMPIRICAL_HANDOFF_NOT_OPERATOR",
            "accepted_as_delta_uet_or_ci": False,
            "reason": "Dirac is inherited standard physics and the Lamb handoff uses empirical source values; neither is a UET or fixed CI correction operator for the selected helium lane.",
            "evidence": {
                "hydrogen_1s2s_dirac_to_lamb_handoff_improvement_factor": atomic_prediction_baseline_comparator_gate[
                    "metrics"
                ]["hydrogen_1s2s_dirac_to_lamb_handoff_improvement_factor"],
            },
        },
        {
            "candidate_id": "helium_fixed_screening_heuristic",
            "candidate_source": "atomic_fixed_parameter_model_readiness_gate",
            "current_use": "fixed_parameter_heuristic_comparator",
            "delta_uet_or_ci_resolution": "REJECTED_AS_DELTA_HEURISTIC_NOT_CI_OR_UET_OPERATOR",
            "accepted_as_delta_uet_or_ci": False,
            "reason": "The fixed-screening lane is locked before evaluation, but its screening coefficient is heuristic and it is not a CI/correlated two-electron or UET operator.",
            "evidence": model_lanes.get("helium_fixed_screening_baseline", {}).get("evidence"),
        },
        {
            "candidate_id": "empirical_quantum_defect_current_diagnostic",
            "candidate_source": "operator manifest and helium quantum-defect gates",
            "current_use": "same_source_family_diagnostic_prediction",
            "delta_uet_or_ci_resolution": "REJECTED_AS_DELTA_FITTED_DIAGNOSTIC",
            "accepted_as_delta_uet_or_ci": manifest_candidates.get(
                "empirical_quantum_defect_current_diagnostic", {}
            ).get("accepted_as_delta_uet_or_ci", False),
            "reason": manifest_candidates.get("empirical_quantum_defect_current_diagnostic", {}).get(
                "reason"
            ),
            "evidence": model_lanes.get("helium_quantum_defect_series_fit", {}).get("evidence"),
        },
        {
            "candidate_id": "legacy_multielectron_three_body_scripts",
            "candidate_source": "legacy code audit gate",
            "current_use": "audit_continuity_only",
            "delta_uet_or_ci_resolution": "REJECTED_AS_DELTA_SMOKE_TEST_NOT_SPECTRAL_MODEL",
            "accepted_as_delta_uet_or_ci": False,
            "reason": "Legacy scripts do not emit source-backed helium level or line residuals and are excluded from primary evidence.",
            "evidence": model_lanes.get("legacy_multielectron_three_body_scripts", {}).get("evidence"),
        },
        {
            "candidate_id": "fixed_parameter_ci_or_correlated_two_electron",
            "candidate_source": "operator manifest",
            "current_use": "missing_acceptable_operator_path",
            "delta_uet_or_ci_resolution": "ACCEPTABLE_CLASS_MISSING_IMPLEMENTATION",
            "accepted_as_delta_uet_or_ci": manifest_candidates.get(
                "fixed_parameter_ci_or_correlated_two_electron", {}
            ).get("accepted_as_delta_uet_or_ci", False),
            "reason": "This is an allowed operator class, but no primary-gated fixed-parameter CI/correlated residual lane exists yet.",
            "required_artifact": manifest_candidates.get(
                "fixed_parameter_ci_or_correlated_two_electron", {}
            ).get("required_artifact"),
        },
        {
            "candidate_id": "explicit_uet_atomic_operator",
            "candidate_source": "operator manifest and UET operator readiness gate",
            "current_use": "missing_acceptable_operator_path",
            "delta_uet_or_ci_resolution": "ACCEPTABLE_CLASS_MISSING_DERIVATION_AND_RESIDUAL_LANE",
            "accepted_as_delta_uet_or_ci": manifest_candidates.get("explicit_uet_atomic_operator", {}).get(
                "accepted_as_delta_uet_or_ci", False
            ),
            "reason": "This is an allowed operator class, but UET derivation, fixed parameters, and source-backed residual artifacts are still absent.",
            "evidence": {
                "uet_operator_readiness_status": uet_atomic_operator_readiness_gate["status"],
                "uet_operator_blocking_requirement_count": uet_atomic_operator_readiness_gate["metrics"][
                    "blocking_requirement_count"
                ],
                "uet_operator_residual_lane_present": uet_atomic_operator_readiness_gate["metrics"][
                    "uet_operator_residual_lane_present"
                ],
            },
            "required_artifact": manifest_candidates.get("explicit_uet_atomic_operator", {}).get(
                "required_artifact"
            ),
        },
    ]
    accepted_rows = [row for row in resolution_rows if row["accepted_as_delta_uet_or_ci"]]
    missing_acceptable_rows = [
        row for row in resolution_rows if row["delta_uet_or_ci_resolution"].startswith("ACCEPTABLE_CLASS_MISSING")
    ]
    rejected_existing_rows = [
        row
        for row in resolution_rows
        if row["delta_uet_or_ci_resolution"].startswith("REJECTED")
    ]
    status = (
        "OPERATOR_CANDIDATE_RESOLUTION_READY_NO_ACCEPTED_DELTA"
        if not accepted_rows
        else "OPERATOR_CANDIDATE_RESOLUTION_READY_WITH_ACCEPTED_DELTA"
    )
    return {
        "schema_version": "1.0",
        "role": "atomic_predictive_v1_operator_candidate_resolution_gate",
        "status": status,
        "claim_class": "operator_candidate_resolution_no_validation_claim",
        "formula_id": "AT20-ATOMIC-PREDICTIVE-V1-OPERATOR-CANDIDATE-RESOLUTION",
        "purpose": "Resolve common candidate formulas and model lanes against the delta_uet_or_ci contract so existing formulas cannot be mistaken for an implemented predictive correction operator.",
        "required_model_form": operator_manifest.get("required_model_form"),
        "fixed_correction_operator_gate_status": atomic_predictive_v1_fixed_correction_operator_gate["status"],
        "resolution_rows": resolution_rows,
        "metrics": {
            "candidate_resolution_count": len(resolution_rows),
            "accepted_delta_uet_or_ci_count": len(accepted_rows),
            "rejected_existing_candidate_count": len(rejected_existing_rows),
            "missing_acceptable_operator_path_count": len(missing_acceptable_rows),
            "fixed_correction_contract_blocking_count": atomic_predictive_v1_fixed_correction_operator_gate[
                "metrics"
            ]["contract_blocking_count"],
            "uet_operator_blocking_requirement_count": uet_atomic_operator_readiness_gate["metrics"][
                "blocking_requirement_count"
            ],
        },
        "blocked_claims": [
            "standard Bohr/Rydberg/Dirac formulas are the UET correction operator",
            "empirical Lamb or quantum-defect handoffs count as fixed delta_uet_or_ci",
            "fixed-screening heuristic residuals validate a CI/correlated or UET operator",
            "legacy smoke-test scripts are primary spectral evidence",
        ],
        "next_required_artifacts": [
            "fixed-parameter CI/correlated two-electron operator residual lane with source-backed helium levels",
            "explicit UET atomic Hamiltonian or transition operator derivation with units and locked parameters",
            "operator uncertainty output consumed by predictive-v1 threshold gate",
            "non-NIST independent He I validation package after the operator is implemented",
        ],
        "claim_boundary": "This gate is a candidate-resolution and anti-overclaim artifact. It does not implement delta_uet_or_ci and does not validate atomic spectra.",
    }


def build_atomic_predictive_v1_operator_build_spec_gate(
    operator_build_spec_manifest: dict,
    atomic_predictive_v1_fixed_correction_operator_gate: dict,
    atomic_predictive_v1_operator_candidate_resolution_gate: dict,
) -> dict:
    lanes = operator_build_spec_manifest.get("implementation_lanes", [])
    forbidden_shortcuts = operator_build_spec_manifest.get("forbidden_shortcuts", [])
    minimum_artifacts = operator_build_spec_manifest.get("minimum_first_build_artifacts", [])
    accepted_operator_count = atomic_predictive_v1_fixed_correction_operator_gate["metrics"][
        "accepted_operator_count"
    ]
    lane_rows = []
    for lane in lanes:
        required_inputs = lane.get("required_inputs", [])
        required_outputs = lane.get("required_outputs", [])
        acceptance_gates = lane.get("acceptance_gates", [])
        lane_rows.append(
            {
                "lane_id": lane["lane_id"],
                "operator_class": lane["operator_class"],
                "priority": lane["priority"],
                "current_status": lane["current_status"],
                "required_input_count": len(required_inputs),
                "required_output_count": len(required_outputs),
                "acceptance_gate_count": len(acceptance_gates),
                "implementation_ready": bool(required_inputs and required_outputs and acceptance_gates),
                "accepted_as_implemented": lane["current_status"] == "ACCEPTED_IMPLEMENTED",
                "required_inputs": required_inputs,
                "required_outputs": required_outputs,
                "acceptance_gates": acceptance_gates,
            }
        )
    accepted_lanes = [row for row in lane_rows if row["accepted_as_implemented"]]
    implementation_missing_lanes = [
        row for row in lane_rows if row["current_status"].endswith("MISSING")
    ]
    spec_checks = [
        {
            "check_id": "BUILD-SPEC-01",
            "requirement": "Manifest must identify the required operator ID and model form.",
            "status": "PASS"
            if operator_build_spec_manifest.get("operator_target", {}).get("required_operator_id")
            == "delta_uet_or_ci"
            and operator_build_spec_manifest.get("operator_target", {}).get("required_model_form")
            else "FAIL",
            "evidence": operator_build_spec_manifest.get("operator_target"),
        },
        {
            "check_id": "BUILD-SPEC-02",
            "requirement": "At least one implementation lane must declare inputs, outputs, and acceptance gates.",
            "status": "PASS" if any(row["implementation_ready"] for row in lane_rows) else "FAIL",
            "evidence": {
                "lane_count": len(lane_rows),
                "implementation_ready_lane_count": sum(1 for row in lane_rows if row["implementation_ready"]),
            },
        },
        {
            "check_id": "BUILD-SPEC-03",
            "requirement": "Forbidden shortcuts must be explicit before implementation work starts.",
            "status": "PASS" if forbidden_shortcuts else "FAIL",
            "evidence": forbidden_shortcuts,
        },
        {
            "check_id": "BUILD-SPEC-04",
            "requirement": "Minimum first-build artifacts must be declared.",
            "status": "PASS" if minimum_artifacts else "FAIL",
            "evidence": minimum_artifacts,
        },
        {
            "check_id": "BUILD-SPEC-05",
            "requirement": "No operator may be accepted until the fixed-correction gate records an implemented operator.",
            "status": "BLOCKED_IMPLEMENTATION_MISSING"
            if accepted_operator_count == 0
            else "PASS",
            "evidence": {
                "accepted_operator_count": accepted_operator_count,
                "candidate_resolution_accepted_delta_count": atomic_predictive_v1_operator_candidate_resolution_gate[
                    "metrics"
                ]["accepted_delta_uet_or_ci_count"],
            },
        },
    ]
    fail_count = sum(1 for row in spec_checks if row["status"] == "FAIL")
    blocking_count = sum(1 for row in spec_checks if row["status"].startswith("BLOCKED"))
    status = (
        "OPERATOR_BUILD_SPEC_FAIL"
        if fail_count
        else "OPERATOR_BUILD_SPEC_READY_IMPLEMENTATION_MISSING"
        if blocking_count
        else "OPERATOR_BUILD_SPEC_READY_OPERATOR_IMPLEMENTED"
    )
    return {
        "schema_version": "1.0",
        "role": "atomic_predictive_v1_operator_build_spec_gate",
        "status": status,
        "claim_class": "operator_build_spec_no_validation_claim",
        "formula_id": "AT20-ATOMIC-PREDICTIVE-V1-OPERATOR-BUILD-SPEC",
        "manifest": {
            "path": str(ATOMIC_PREDICTIVE_V1_OPERATOR_BUILD_SPEC_MANIFEST_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
            "sha256": file_sha256(ATOMIC_PREDICTIVE_V1_OPERATOR_BUILD_SPEC_MANIFEST_PATH),
            "manifest_id": operator_build_spec_manifest.get("manifest_id"),
            "status": operator_build_spec_manifest.get("status"),
        },
        "operator_target": operator_build_spec_manifest.get("operator_target"),
        "implementation_lanes": lane_rows,
        "spec_checks": spec_checks,
        "forbidden_shortcuts": forbidden_shortcuts,
        "minimum_first_build_artifacts": minimum_artifacts,
        "pass_conditions_for_accepting_operator": operator_build_spec_manifest.get(
            "pass_conditions_for_accepting_operator", []
        ),
        "metrics": {
            "implementation_lane_count": len(lane_rows),
            "implementation_ready_lane_count": sum(1 for row in lane_rows if row["implementation_ready"]),
            "implementation_missing_lane_count": len(implementation_missing_lanes),
            "accepted_implemented_lane_count": len(accepted_lanes),
            "required_input_total_count": sum(row["required_input_count"] for row in lane_rows),
            "required_output_total_count": sum(row["required_output_count"] for row in lane_rows),
            "acceptance_gate_total_count": sum(row["acceptance_gate_count"] for row in lane_rows),
            "forbidden_shortcut_count": len(forbidden_shortcuts),
            "minimum_first_build_artifact_count": len(minimum_artifacts),
            "spec_check_count": len(spec_checks),
            "spec_fail_count": fail_count,
            "spec_blocking_count": blocking_count,
            "accepted_fixed_correction_operator_count": accepted_operator_count,
        },
        "blocked_claims": [
            "operator build spec is an implemented predictive model",
            "implementation-ready inputs and outputs imply accepted delta_uet_or_ci",
            "validation thresholds can be upgraded before operator uncertainty exists",
        ],
        "next_required_artifacts": minimum_artifacts,
        "claim_boundary": operator_build_spec_manifest.get("claim_boundary"),
    }


def build_atomic_predictive_v1_diagnostic_report_gate(
    atomic_predictive_v1_parameter_manifest: dict,
    atomic_predictive_v1_threshold_manifest: dict,
    helium_quantum_defect_holdout_gate: dict,
    helium_quantum_defect_wavelength_holdout_gate: dict,
    atomic_predictive_v1_parameter_lock_gate: dict,
    atomic_predictive_v1_threshold_gate: dict,
    atomic_predictive_v1_fixed_correction_operator_gate: dict,
    helium_external_holdout_lineage_decision_gate: dict,
) -> dict:
    level_predictions = [
        {
            "holdout_id": row["holdout_id"],
            "series_key": row["series_key"],
            "configuration": row["configuration"],
            "term": row["term"],
            "outer_principal_quantum_number": row["outer_principal_quantum_number"],
            "predicted_excitation_energy_eV": row["predicted_excitation_energy_eV"],
            "observed_excitation_energy_eV": row["observed_excitation_energy_eV"],
            "absolute_residual_eV": row["absolute_residual_eV"],
            "model_uncertainty_eV": row.get("predicted_excitation_model_uncertainty_eV"),
            "source_locator": row["source_locator"],
        }
        for row in helium_quantum_defect_holdout_gate.get("predictions", [])
    ]
    wavelength_predictions = [
        {
            "holdout_id": row["holdout_id"],
            "upper_configuration": row["upper_configuration"],
            "upper_term": row["upper_term"],
            "source_wavelength_angstrom": row["source_wavelength_angstrom"],
            "predicted_wavelength_angstrom": row["predicted_wavelength_angstrom"],
            "absolute_residual_angstrom": row["absolute_residual_angstrom"],
            "absolute_residual_ppm": row["absolute_residual_ppm"],
            "model_uncertainty_angstrom": row.get("predicted_wavelength_model_uncertainty_angstrom"),
            "source_locator": row["source_locator"],
        }
        for row in helium_quantum_defect_wavelength_holdout_gate.get("predictions", [])
    ]
    validation_blockers = [
        {
            "blocker_id": "V1-BLOCK-OPERATOR",
            "status": "BLOCKING",
            "evidence": atomic_predictive_v1_fixed_correction_operator_gate["status"],
            "required_artifact": "fixed-parameter CI/correlated or UET correction operator with units",
        },
        {
            "blocker_id": "V1-BLOCK-SOURCE",
            "status": "BLOCKING"
            if helium_external_holdout_lineage_decision_gate["metrics"]["non_nist_source_required"]
            else "PASS",
            "evidence": helium_external_holdout_lineage_decision_gate["decision"],
            "required_artifact": "non-NIST independent He I holdout package",
        },
        {
            "blocker_id": "V1-BLOCK-THRESHOLD",
            "status": "BLOCKING"
            if atomic_predictive_v1_threshold_gate["metrics"]["validation_ready_threshold_count"] == 0
            else "PASS",
            "evidence": (
                f"{atomic_predictive_v1_threshold_gate['metrics']['validation_ready_threshold_count']} "
                "validation-ready thresholds"
            ),
            "required_artifact": "validation-ready source/model uncertainty threshold policy",
        },
    ]
    diagnostic_threshold_fail_count = atomic_predictive_v1_threshold_gate["metrics"]["diagnostic_fail_count"]
    blocking_count = sum(1 for row in validation_blockers if row["status"] == "BLOCKING")
    implementation_status = (
        "DIAGNOSTIC_REPORT_FAIL"
        if diagnostic_threshold_fail_count
        else "DIAGNOSTIC_REPORT_READY_VALIDATION_BLOCKED"
    )
    return {
        "schema_version": "1.0",
        "role": "atomic_predictive_v1_diagnostic_report_gate",
        "status": implementation_status,
        "claim_class": "diagnostic_prediction_report_no_validation_claim",
        "formula_id": "AT20-ATOMIC-PREDICTIVE-V1-DIAGNOSTIC-REPORT",
        "selected_lane_id": atomic_predictive_v1_parameter_manifest.get("selected_lane_id"),
        "current_diagnostic_lane_id": atomic_predictive_v1_parameter_manifest.get("current_diagnostic_lane_id"),
        "model_equation": atomic_predictive_v1_parameter_manifest.get("model_contract", {}).get("required_form"),
        "current_diagnostic_equation": atomic_predictive_v1_parameter_manifest.get("model_contract", {}).get(
            "current_diagnostic_form"
        ),
        "implementation_state": {
            "current_operator": "empirical_quantum_defect_same_source_family_diagnostic",
            "missing_operator": atomic_predictive_v1_parameter_manifest.get("model_contract", {}).get(
                "missing_predictive_component"
            ),
            "parameter_lock_status": atomic_predictive_v1_parameter_lock_gate["status"],
            "threshold_status": atomic_predictive_v1_threshold_gate["status"],
            "fixed_correction_operator_status": atomic_predictive_v1_fixed_correction_operator_gate["status"],
            "external_lineage_decision": helium_external_holdout_lineage_decision_gate["decision"],
        },
        "level_holdout_predictions": level_predictions,
        "wavelength_holdout_predictions": wavelength_predictions,
        "threshold_rows": atomic_predictive_v1_threshold_gate["threshold_rows"],
        "validation_blockers": validation_blockers,
        "metrics": {
            "level_holdout_prediction_count": len(level_predictions),
            "wavelength_holdout_prediction_count": len(wavelength_predictions),
            "max_level_abs_residual_eV": helium_quantum_defect_holdout_gate["metrics"][
                "max_abs_excitation_residual_eV"
            ],
            "max_wavelength_abs_residual_angstrom": helium_quantum_defect_wavelength_holdout_gate["metrics"][
                "max_abs_wavelength_residual_angstrom"
            ],
            "max_wavelength_abs_residual_ppm": helium_quantum_defect_wavelength_holdout_gate["metrics"][
                "max_abs_wavelength_residual_ppm"
            ],
            "diagnostic_threshold_pass_count": atomic_predictive_v1_threshold_gate["metrics"][
                "diagnostic_pass_count"
            ],
            "diagnostic_threshold_fail_count": diagnostic_threshold_fail_count,
            "validation_ready_threshold_count": atomic_predictive_v1_threshold_gate["metrics"][
                "validation_ready_threshold_count"
            ],
            "validation_blocker_count": blocking_count,
            "accepted_fixed_correction_operator_count": atomic_predictive_v1_fixed_correction_operator_gate[
                "metrics"
            ]["accepted_operator_count"],
            "independent_validation_allowed": False,
        },
        "blocked_claims": [
            "diagnostic threshold pass proves independent prediction",
            "empirical quantum-defect holdouts are a UET atomic operator",
            "same-source-family NIST rows validate helium spectra",
            "CHIANTI cross-check rows validate helium spectra despite NIST-lineage dependency",
        ],
        "next_required_artifacts": [
            "fixed-parameter CI/correlated or UET correction operator that fills delta_uet_or_ci",
            "non-NIST independent He I source package with source hashes and uncertainty policy",
            "validation-ready threshold manifest declared before independent holdout evaluation",
            "v1 validation report comparing standard baseline, empirical quantum defect, CI/correlated, and UET correction residuals",
        ],
        "claim_boundary": "This gate is the first v1 diagnostic prediction report. It records current holdout predictions and threshold checks, but validation remains blocked because the correction operator, non-NIST source package, and validation-ready thresholds are missing.",
    }


def build_helium_external_holdout_lineage_decision_gate(
    chianti_he_i_manifest: dict,
    helium_external_holdout_acquisition_gate: dict,
    helium_external_holdout_residual_crosscheck_gate: dict,
) -> dict:
    raw_files = chianti_he_i_manifest.get("raw_files", [])
    overlap_rows = chianti_he_i_manifest.get("overlap_rows", [])
    lineage_review = chianti_he_i_manifest.get("lineage_review", {})
    nist_lineage_raw_files = [
        row
        for row in raw_files
        if "NIST" in row.get("lineage_note", "") or "NIST" in lineage_review.get("known_dependency", "")
    ]
    nist_lineage_overlap_rows = [
        row
        for row in overlap_rows
        if row.get("lineage_status", "").startswith("CROSS_CHECK_ONLY")
    ]
    wavelength_rounding_pass = helium_external_holdout_residual_crosscheck_gate["metrics"][
        "wavelength_display_rounding_pass_count"
    ]
    upper_energy_review_count = helium_external_holdout_residual_crosscheck_gate["metrics"][
        "upper_energy_source_version_review_count"
    ]
    decision_checks = [
        {
            "check_id": "LINEAGE-01",
            "requirement": "Raw files and overlap row locators must be captured before lineage decision.",
            "status": "PASS"
            if helium_external_holdout_acquisition_gate["metrics"]["raw_file_hash_count"] == len(raw_files)
            and len(overlap_rows)
            else "FAIL",
            "evidence": {
                "raw_file_count": len(raw_files),
                "raw_file_hash_count": helium_external_holdout_acquisition_gate["metrics"]["raw_file_hash_count"],
                "overlap_row_count": len(overlap_rows),
            },
        },
        {
            "check_id": "LINEAGE-02",
            "requirement": "Source metadata must be reviewed for dependency on the current NIST source family.",
            "status": "CROSSCHECK_ONLY_NOT_INDEPENDENT" if nist_lineage_raw_files else "INDEPENDENCE_NOT_EXCLUDED",
            "evidence": lineage_review.get("known_dependency"),
        },
        {
            "check_id": "LINEAGE-03",
            "requirement": "Residual deltas may be computed but cannot override source-family dependency.",
            "status": "PASS_DIAGNOSTIC_ONLY",
            "evidence": {
                "crosscheck_row_count": helium_external_holdout_residual_crosscheck_gate["metrics"]["crosscheck_row_count"],
                "wavelength_display_rounding_pass_count": wavelength_rounding_pass,
                "upper_energy_source_version_review_count": upper_energy_review_count,
            },
        },
    ]
    fail_count = sum(1 for row in decision_checks if row["status"] == "FAIL")
    decision = "CROSSCHECK_ONLY_NOT_INDEPENDENT" if nist_lineage_raw_files else "MORE_LINEAGE_REVIEW_REQUIRED"
    status = "LINEAGE_DECISION_FAIL" if fail_count else f"LINEAGE_DECISION_{decision}"
    return {
        "schema_version": "1.0",
        "role": "helium_external_holdout_lineage_decision_gate",
        "status": status,
        "decision": decision,
        "claim_class": "source_lineage_decision_no_validation_claim",
        "formula_id": "AT20-HELIUM-EXTERNAL-HOLDOUT-LINEAGE-DECISION",
        "source_family": chianti_he_i_manifest.get("source_family"),
        "decision_checks": decision_checks,
        "metrics": {
            "raw_file_count": len(raw_files),
            "raw_file_hash_count": helium_external_holdout_acquisition_gate["metrics"]["raw_file_hash_count"],
            "overlap_row_count": len(overlap_rows),
            "nist_lineage_raw_file_count": len(nist_lineage_raw_files),
            "crosscheck_only_overlap_row_count": len(nist_lineage_overlap_rows),
            "wavelength_display_rounding_pass_count": wavelength_rounding_pass,
            "upper_energy_source_version_review_count": upper_energy_review_count,
            "independent_validation_allowed": False,
            "non_nist_source_required": True,
        },
        "allowed_use": [
            "external database cross-check diagnostics",
            "source-version reconciliation work",
            "evidence for why non-NIST independent holdouts are still required",
        ],
        "blocked_use": [
            "independent external helium validation",
            "parameter tuning for predictive v1 lane",
            "claim upgrade for helium quantum-defect holdouts",
        ],
        "next_required_artifacts": [
            "non-NIST He I measurement or independent compilation source package with raw/table hashes",
            "source-version reconciliation note for CHIANTI-vs-current upper-energy deltas",
            "validation-ready external holdout gate after independent source package is captured",
        ],
        "claim_boundary": "This gate decides that the current CHIANTI He I package is cross-check-only because the captured metadata records NIST ASD lineage. It narrows the blocker but does not provide independent validation.",
    }


def build_atomic_predictive_model_blueprint_gate(
    atomic_predictive_model_closure_gate: dict,
    atomic_predictive_model_spec_gate: dict,
    atomic_first_predictive_implementation_candidate_gate: dict,
    atomic_predictive_v1_parameter_lock_gate: dict,
    atomic_predictive_v1_threshold_gate: dict,
    atomic_predictive_v1_fixed_correction_operator_gate: dict,
    helium_external_holdout_lineage_decision_gate: dict,
    atomic_prediction_baseline_comparator_gate: dict,
    atomic_uncertainty_readiness_gate: dict,
    atomic_fixed_parameter_model_readiness_gate: dict,
    uet_atomic_operator_readiness_gate: dict,
    helium_external_holdout_acquisition_gate: dict,
    helium_external_holdout_residual_crosscheck_gate: dict,
) -> dict:
    blueprint_steps = [
        {
            "step_id": "BLUEPRINT-01",
            "name": "domain_lane",
            "requirement": "Choose one domain lane before modeling: one-electron hydrogenic, hydrogen precision, helium two-electron, or periodic-table expansion.",
            "current_decision": atomic_first_predictive_implementation_candidate_gate["selected_lane_id"],
            "status": "READY_DIAGNOSTIC_LANE_SELECTED",
            "evidence": "The first candidate gate selects the narrow helium quantum-defect same-source-family lane because it already has level and wavelength holdout diagnostics.",
        },
        {
            "step_id": "BLUEPRINT-02",
            "name": "model_equation",
            "requirement": "Represent predictions as standard_baseline plus an explicit correction term with units.",
            "current_decision": atomic_predictive_model_spec_gate["model_contract"]["model_form"],
            "status": "PARTIAL_OPERATOR_CONTRACT_READY_IMPLEMENTATION_MISSING",
            "evidence": (
                "The model spec declares the baseline-plus-correction form and the fixed-correction operator gate "
                f"records {atomic_predictive_v1_fixed_correction_operator_gate['metrics']['operator_candidate_count']} "
                "operator candidates, but "
                f"{atomic_predictive_v1_fixed_correction_operator_gate['metrics']['accepted_operator_count']} "
                "are accepted as implemented."
            ),
        },
        {
            "step_id": "BLUEPRINT-03",
            "name": "parameter_lock",
            "requirement": "Freeze constants, calibrated parameters, and forbidden holdout-leakage fields before evaluating holdouts.",
            "current_decision": atomic_predictive_v1_parameter_lock_gate["status"],
            "status": "PARTIAL_PARAMETER_MANIFEST_READY_GENERATIVE_MODEL_MISSING",
            "evidence": (
                f"{atomic_predictive_v1_parameter_lock_gate['metrics']['calibrated_parameter_count']} calibrated "
                "parameter policy rows and "
                f"{atomic_predictive_v1_parameter_lock_gate['metrics']['forbidden_leakage_field_count']} forbidden "
                "leakage fields are declared; generative CI/UET correction parameters remain missing."
            ),
        },
        {
            "step_id": "BLUEPRINT-04",
            "name": "holdout_protocol",
            "requirement": "Evaluate on rows that were not used to calibrate parameters, with independent external rows required for validation.",
            "current_decision": "same-source-family helium holdouts are allowed only as diagnostics",
            "status": "PARTIAL_EXTERNAL_VALIDATION_BLOCKED",
            "evidence": (
                f"{atomic_first_predictive_implementation_candidate_gate['metrics']['selected_level_holdout_prediction_count']} "
                "level holdouts and "
                f"{atomic_first_predictive_implementation_candidate_gate['metrics']['selected_wavelength_holdout_prediction_count']} "
                "wavelength holdouts exist, but external validation remains blocked."
            ),
        },
        {
            "step_id": "BLUEPRINT-05",
            "name": "baseline_comparator",
            "requirement": "Compare every claimed prediction against named standard and empirical baselines.",
            "current_decision": "internal comparator table present",
            "status": "PASS_INTERNAL_EXTERNAL_COMPARATORS_OPEN",
            "evidence": f"{atomic_prediction_baseline_comparator_gate['metrics']['comparator_count']} comparator rows are machine-readable.",
        },
        {
            "step_id": "BLUEPRINT-06",
            "name": "uncertainty_threshold",
            "requirement": "Propagate source and model uncertainty, then apply thresholds declared before evaluation.",
            "current_decision": atomic_predictive_v1_threshold_gate["status"],
            "status": "PARTIAL_THRESHOLD_MANIFEST_READY_VALIDATION_BLOCKED",
            "evidence": (
                f"{atomic_predictive_v1_threshold_gate['metrics']['diagnostic_pass_count']} diagnostic thresholds pass, "
                f"{atomic_predictive_v1_threshold_gate['metrics']['validation_ready_threshold_count']} thresholds are validation-ready, "
                "and official/source uncertainty plus a non-NIST independent source package remain required."
            ),
        },
        {
            "step_id": "BLUEPRINT-07",
            "name": "source_lineage",
            "requirement": "Classify cross-check sources by lineage before treating residuals as validation evidence.",
            "current_decision": helium_external_holdout_lineage_decision_gate["decision"],
            "status": "PARTIAL_LINEAGE_DECISION_CROSSCHECK_ONLY_NON_NIST_SOURCE_REQUIRED",
            "evidence": (
                f"{helium_external_holdout_lineage_decision_gate['metrics']['nist_lineage_raw_file_count']} CHIANTI raw files carry NIST lineage notes; "
                f"{helium_external_holdout_lineage_decision_gate['metrics']['crosscheck_only_overlap_row_count']} overlap rows remain cross-check-only; "
                "non-NIST source package is still required."
            ),
        },
    ]
    blocked_steps = [row for row in blueprint_steps if row["status"].startswith("BLOCKED")]
    partial_steps = [row for row in blueprint_steps if row["status"].startswith("PARTIAL")]
    internal_pass_steps = [row for row in blueprint_steps if row["status"].startswith("PASS_INTERNAL")]
    ready_steps = [row for row in blueprint_steps if row["status"].startswith("READY")]
    first_v1_lane = {
        "lane_id": "helium_quantum_defect_then_ci_or_uet_correction_v1",
        "allowed_current_use": "diagnostic blueprint only",
        "implementation_order": [
            "keep the current helium quantum-defect holdout lane as a smoke-test harness",
            "add a fixed-parameter CI/correlated or explicit UET correction operator that predicts level corrections rather than fitting holdout rows",
            "freeze a parameter manifest before holdout evaluation",
            "rerun same-source-family holdouts only as internal diagnostics",
            "add non-NIST independent He I rows before validation claims",
            "compare residuals against zero-quantum-defect, empirical quantum-defect, CI/correlated, and any UET correction lane",
        ],
        "claim_ceiling": "A successful v1 may claim a bounded holdout prediction lane only after parameter lock, uncertainty thresholds, and independent source lineage are closed.",
    }
    return {
        "schema_version": "1.0",
        "role": "atomic_predictive_model_blueprint_gate",
        "status": "BLUEPRINT_READY_IMPLEMENTATION_AND_VALIDATION_BLOCKED",
        "claim_class": "predictive_model_blueprint_no_validation_claim",
        "formula_id": "AT20-ATOMIC-PREDICTIVE-MODEL-BLUEPRINT",
        "purpose": "Turn the predictive-model question into a machine-readable build plan that separates real prediction from fit diagnostics.",
        "blueprint_steps": blueprint_steps,
        "first_v1_lane": first_v1_lane,
        "metrics": {
            "blueprint_step_count": len(blueprint_steps),
            "ready_step_count": len(ready_steps),
            "internal_pass_step_count": len(internal_pass_steps),
            "partial_step_count": len(partial_steps),
            "blocked_step_count": len(blocked_steps),
            "closure_open_or_partial_checks": atomic_predictive_model_closure_gate["metrics"]["open_or_partial_check_count"],
            "parameter_lock_policy_fail_count": atomic_predictive_v1_parameter_lock_gate["metrics"][
                "policy_fail_count"
            ],
            "parameter_lock_policy_partial_count": atomic_predictive_v1_parameter_lock_gate["metrics"][
                "policy_partial_count"
            ],
            "parameter_lock_missing_future_parameter_count": atomic_predictive_v1_parameter_lock_gate["metrics"][
                "missing_future_locked_parameter_count"
            ],
            "threshold_manifest_diagnostic_pass_count": atomic_predictive_v1_threshold_gate["metrics"][
                "diagnostic_pass_count"
            ],
            "threshold_manifest_validation_ready_count": atomic_predictive_v1_threshold_gate["metrics"][
                "validation_ready_threshold_count"
            ],
            "fixed_correction_operator_candidate_count": atomic_predictive_v1_fixed_correction_operator_gate["metrics"][
                "operator_candidate_count"
            ],
            "fixed_correction_operator_accepted_count": atomic_predictive_v1_fixed_correction_operator_gate["metrics"][
                "accepted_operator_count"
            ],
            "fixed_correction_operator_contract_blocking_count": atomic_predictive_v1_fixed_correction_operator_gate[
                "metrics"
            ]["contract_blocking_count"],
            "external_lineage_independent_validation_allowed": helium_external_holdout_lineage_decision_gate["metrics"][
                "independent_validation_allowed"
            ],
            "external_lineage_non_nist_source_required": helium_external_holdout_lineage_decision_gate["metrics"][
                "non_nist_source_required"
            ],
            "spec_blocking_implementation_blockers": atomic_predictive_model_spec_gate["metrics"][
                "blocking_implementation_blocker_count"
            ],
            "selected_level_holdout_prediction_count": atomic_first_predictive_implementation_candidate_gate["metrics"][
                "selected_level_holdout_prediction_count"
            ],
            "selected_wavelength_holdout_prediction_count": atomic_first_predictive_implementation_candidate_gate[
                "metrics"
            ]["selected_wavelength_holdout_prediction_count"],
            "uet_operator_blocking_requirement_count": uet_atomic_operator_readiness_gate["metrics"][
                "blocking_requirement_count"
            ],
            "external_crosscheck_row_count": helium_external_holdout_residual_crosscheck_gate["metrics"][
                "crosscheck_row_count"
            ],
            "external_crosscheck_blocked_requirement_count": helium_external_holdout_residual_crosscheck_gate[
                "metrics"
            ]["blocked_requirement_count"],
        },
        "blocked_claims": [
            "same-source-family holdouts prove independent prediction",
            "a fitted quantum-defect diagnostic is a UET derivation",
            "CHIANTI cross-check residuals validate helium spectra despite NIST-lineage dependency",
            "standard Rydberg/Dirac/QED baselines alone prove UET atomic theory",
        ],
        "next_required_artifacts": [
            "parameter manifest for the selected v1 lane",
            "fixed-parameter CI/correlated or explicit UET correction operator with units",
            "non-NIST independent He I holdout package",
            "uncertainty-aware residual thresholds declared before holdout evaluation",
            "v1 validation report that compares standard baseline, empirical fit, CI/correlated, and UET correction residuals",
        ],
        "claim_boundary": "This blueprint answers how to build a predictive atomic model. It is not itself a predictive implementation or validation artifact.",
    }


def build_helium_external_holdout_acquisition_gate(
    atomic_first_predictive_implementation_candidate_gate: dict,
    chianti_he_i_manifest: dict,
) -> dict:
    chianti_source = chianti_he_i_manifest["source_family"]
    chianti_overlap_rows = [
        {
            "current_holdout_id": row["current_holdout_id"],
            "current_wavelength_angstrom": row["current_nist_wavelength_angstrom"],
            "candidate_wavelength_angstrom": row["chianti_wavelength_angstrom"],
            "candidate_upper_energy_cm_inverse": row["chianti_upper_energy_observed_cm_inverse"],
            "chianti_wgfa_line_number": row["chianti_wgfa_line_number"],
            "chianti_elvlc_upper_line_number": row["chianti_elvlc_upper_line_number"],
            "match_status": row["match_status"],
            "lineage_status": row["lineage_status"],
        }
        for row in chianti_he_i_manifest["overlap_rows"]
    ]
    raw_file_count = len(chianti_he_i_manifest["raw_files"])
    raw_file_hash_count = sum(1 for row in chianti_he_i_manifest["raw_files"] if row.get("sha256"))
    source_candidates = [
        {
            "candidate_id": "chianti_he_i_v11_table",
            "source_family": chianti_source["name"],
            "source_version": chianti_source.get("version"),
            "source_url": chianti_source["html_table_url"],
            "metadata_url": chianti_source["metadata_url"],
            "candidate_role": "external_database_cross_check_candidate",
            "raw_capture_status": chianti_he_i_manifest["status"],
            "raw_files": chianti_he_i_manifest["raw_files"],
            "overlap_with_selected_lane": chianti_overlap_rows,
            "lineage_review": chianti_he_i_manifest["lineage_review"],
            "capture_requirements": [
                "record exact line indices, lower/upper configurations, terms, energies, wavelength, gf, and A values",
                "compare source lineage against the current NIST Handbook/ASD source family",
                "mark any row whose observed energy/wavelength lineage is NIST-derived as cross-check-only",
            ],
        },
        {
            "candidate_id": "non_nist_measurement_or_compilation",
            "source_family": "to_be_selected",
            "source_url": None,
            "metadata_url": None,
            "candidate_role": "true_independent_validation_target",
            "overlap_with_selected_lane": [],
            "lineage_review": {
                "status": "MISSING",
                "reason": "No in-repo non-NIST He I measurement or independent compilation package has been source-locked.",
                "use_boundary": "Required before helium holdout diagnostics can be upgraded to independent validation.",
            },
            "capture_requirements": [
                "source DOI/URL and page/table locator",
                "raw table or machine transcription with hash",
                "wavelength medium convention and uncertainty fields",
                "line-component/blend policy",
                "explicit proof that rows were not used in the selected calibration package",
            ],
        },
    ]
    selected_candidate = source_candidates[0]
    blocking_requirements = [
        {
            "requirement_id": "EXT-HE-01",
            "status": "PARTIAL_CANDIDATE_IDENTIFIED",
            "description": "Identify an external source candidate with overlapping He I holdout lines.",
            "evidence": "CHIANTI He I table contains candidate matches for the 522.21309 A and 537.02992 A current holdout rows.",
        },
        {
            "requirement_id": "EXT-HE-02",
            "status": "READY_RAW_CAPTURED",
            "description": "Archive raw/source rows and hashes before the candidate can enter verifier inputs.",
            "evidence": f"{raw_file_count} raw CHIANTI files captured with {raw_file_hash_count} SHA256 hashes and {len(chianti_overlap_rows)} overlap rows recorded.",
        },
        {
            "requirement_id": "EXT-HE-03",
            "status": "BLOCKED_LINEAGE_NOT_INDEPENDENT",
            "description": "Prove the source family is independent from the NIST family used by current calibration/holdout rows.",
            "evidence": "CHIANTI metadata records NIST ASD Version 2.0 lineage for observed He I data.",
        },
        {
            "requirement_id": "EXT-HE-04",
            "status": "BLOCKED_SOURCE_VERSION_REVIEW_REQUIRED",
            "description": "Review source-version deltas before external residuals are interpreted as anything beyond cross-check diagnostics.",
            "evidence": "The residual cross-check gate declares display-rounding policy, but CHIANTI-vs-current upper-energy deltas require source-version reconciliation.",
        },
    ]
    blocking_count = sum(1 for row in blocking_requirements if row["status"].startswith("BLOCKED"))
    return {
        "schema_version": "1.0",
        "role": "helium_external_holdout_acquisition_gate",
        "status": "RAW_CAPTURE_READY_CROSSCHECK_ONLY_SOURCE_VERSION_REVIEW_OPEN",
        "claim_class": "source_acquisition_gate_only",
        "formula_id": "AT20-HELIUM-EXTERNAL-HOLDOUT-ACQUISITION",
        "selected_first_candidate_lane": atomic_first_predictive_implementation_candidate_gate["selected_lane_id"],
        "source_candidates": source_candidates,
        "selected_acquisition_candidate": selected_candidate["candidate_id"],
        "blocking_requirements": blocking_requirements,
        "metrics": {
            "candidate_source_count": len(source_candidates),
            "candidate_sources_with_overlap_count": sum(1 for row in source_candidates if row["overlap_with_selected_lane"]),
            "overlap_line_candidate_count": len(selected_candidate["overlap_with_selected_lane"]),
            "raw_file_count": raw_file_count,
            "raw_file_hash_count": raw_file_hash_count,
            "blocking_requirement_count": len(blocking_requirements),
            "blocked_requirement_count": blocking_count,
            "first_candidate_level_holdout_count": atomic_first_predictive_implementation_candidate_gate["metrics"][
                "selected_level_holdout_prediction_count"
            ],
            "first_candidate_wavelength_holdout_count": atomic_first_predictive_implementation_candidate_gate["metrics"][
                "selected_wavelength_holdout_prediction_count"
            ],
        },
        "next_required_artifacts": [
            "non-NIST source package for independent-validation use",
            "non-NIST measurement or compilation source package because CHIANTI is NIST-dependent",
            "external-holdout residual gate rerun after source capture and uncertainty thresholds are declared",
        ],
        "claim_boundary": "This gate narrows the external-holdout blocker. It identifies candidate source families but does not add external validation rows to the model and does not upgrade helium diagnostics.",
    }


def build_helium_external_holdout_residual_crosscheck_gate(
    helium_qd_holdouts: dict,
    chianti_he_i_manifest: dict,
    helium_external_holdout_acquisition_gate: dict,
) -> dict:
    chianti_display_policy = {
        "wavelength_rounding_bound_angstrom": 0.0005,
        "upper_energy_rounding_bound_cm_inverse": 0.0005,
        "basis": "half last shown decimal place in captured CHIANTI wgfa wavelengths (0.001 A) and elvlc observed energies (0.001 cm^-1)",
    }
    holdout_rows = {row["holdout_id"]: row for row in helium_qd_holdouts["holdout_levels"]}
    crosscheck_rows = []
    skipped_rows = []

    for candidate in chianti_he_i_manifest["overlap_rows"]:
        holdout = holdout_rows.get(candidate["current_holdout_id"])
        if holdout is None:
            skipped_rows.append(
                {
                    "current_holdout_id": candidate["current_holdout_id"],
                    "reason": "current holdout row not found in helium_quantum_defect_holdout_sources.json",
                }
            )
            continue

        wavelength_delta_angstrom = candidate["chianti_wavelength_angstrom"] - holdout["wavelength_angstrom"]
        wavelength_abs_delta_angstrom = abs(wavelength_delta_angstrom)
        wavelength_delta_ppm = wavelength_abs_delta_angstrom / holdout["wavelength_angstrom"] * 1e6
        upper_energy_delta_cm_inverse = (
            candidate["chianti_upper_energy_observed_cm_inverse"] - holdout["upper_energy_cm_inverse"]
        )
        upper_energy_abs_delta_cm_inverse = abs(upper_energy_delta_cm_inverse)
        wavelength_uncertainty = holdout.get("wavelength_uncertainty_angstrom")
        upper_energy_uncertainty = holdout.get("upper_energy_uncertainty_cm_inverse")
        combined_wavelength_rounding_bound = (
            (wavelength_uncertainty or 0.0) + chianti_display_policy["wavelength_rounding_bound_angstrom"]
        )
        combined_energy_rounding_bound = (
            (upper_energy_uncertainty or 0.0)
            + chianti_display_policy["upper_energy_rounding_bound_cm_inverse"]
        )

        crosscheck_rows.append(
            {
                "current_holdout_id": candidate["current_holdout_id"],
                "current_source_family": "NIST Handbook persistent lines",
                "candidate_source_family": chianti_he_i_manifest["source_family"]["name"],
                "current_wavelength_angstrom": holdout["wavelength_angstrom"],
                "chianti_wavelength_angstrom": candidate["chianti_wavelength_angstrom"],
                "wavelength_delta_angstrom": wavelength_delta_angstrom,
                "wavelength_abs_delta_angstrom": wavelength_abs_delta_angstrom,
                "wavelength_abs_delta_ppm": wavelength_delta_ppm,
                "current_upper_energy_cm_inverse": holdout["upper_energy_cm_inverse"],
                "chianti_upper_energy_observed_cm_inverse": candidate[
                    "chianti_upper_energy_observed_cm_inverse"
                ],
                "upper_energy_delta_cm_inverse": upper_energy_delta_cm_inverse,
                "upper_energy_abs_delta_cm_inverse": upper_energy_abs_delta_cm_inverse,
                "wavelength_transcription_bound_angstrom": wavelength_uncertainty,
                "wavelength_delta_to_transcription_bound_ratio": (
                    wavelength_abs_delta_angstrom / wavelength_uncertainty
                    if wavelength_uncertainty
                    else None
                ),
                "combined_wavelength_rounding_bound_angstrom": combined_wavelength_rounding_bound,
                "wavelength_delta_to_combined_rounding_bound_ratio": (
                    wavelength_abs_delta_angstrom / combined_wavelength_rounding_bound
                    if combined_wavelength_rounding_bound
                    else None
                ),
                "wavelength_rounding_policy_status": (
                    "PASS_DISPLAY_ROUNDING_CONSISTENT"
                    if wavelength_abs_delta_angstrom <= combined_wavelength_rounding_bound
                    else "REVIEW_DISPLAY_ROUNDING_EXCEEDED"
                ),
                "upper_energy_transcription_bound_cm_inverse": upper_energy_uncertainty,
                "upper_energy_delta_to_transcription_bound_ratio": (
                    upper_energy_abs_delta_cm_inverse / upper_energy_uncertainty
                    if upper_energy_uncertainty
                    else None
                ),
                "combined_upper_energy_rounding_bound_cm_inverse": combined_energy_rounding_bound,
                "upper_energy_delta_to_combined_rounding_bound_ratio": (
                    upper_energy_abs_delta_cm_inverse / combined_energy_rounding_bound
                    if combined_energy_rounding_bound
                    else None
                ),
                "upper_energy_rounding_policy_status": (
                    "PASS_DISPLAY_ROUNDING_CONSISTENT"
                    if upper_energy_abs_delta_cm_inverse <= combined_energy_rounding_bound
                    else "BLOCKED_SOURCE_VERSION_RECONCILIATION_REQUIRED"
                ),
                "chianti_wgfa_line_number": candidate["chianti_wgfa_line_number"],
                "chianti_elvlc_upper_line_number": candidate["chianti_elvlc_upper_line_number"],
                "lineage_status": candidate["lineage_status"],
                "interpretation": "cross-check delta only; not independent residual validation because CHIANTI is NIST-lineage and source-version reconciliation remains open",
            }
        )

    wavelength_residuals = [row["wavelength_abs_delta_angstrom"] for row in crosscheck_rows]
    wavelength_ppm = [row["wavelength_abs_delta_ppm"] for row in crosscheck_rows]
    energy_residuals = [row["upper_energy_abs_delta_cm_inverse"] for row in crosscheck_rows]
    wavelength_policy_pass_count = sum(
        1 for row in crosscheck_rows if row["wavelength_rounding_policy_status"].startswith("PASS")
    )
    energy_policy_block_count = sum(
        1 for row in crosscheck_rows if row["upper_energy_rounding_policy_status"].startswith("BLOCKED")
    )
    return {
        "schema_version": "1.0",
        "role": "helium_external_holdout_residual_crosscheck_gate",
        "status": "CROSSCHECK_RESIDUALS_COMPUTED_NOT_INDEPENDENT_SOURCE_VERSION_REVIEW_OPEN",
        "claim_class": "external_database_crosscheck_diagnostic_only",
        "formula_id": "AT20-HELIUM-EXTERNAL-HOLDOUT-RESIDUAL-CROSSCHECK",
        "threshold_policy": {
            "status": "DISPLAY_ROUNDING_POLICY_DECLARED_VALIDATION_BLOCKED",
            "role": "screening_policy_only_not_validation_threshold",
            "chianti_display_policy": chianti_display_policy,
            "current_source_policy": helium_qd_holdouts.get("uncertainty_policy"),
            "interpretation": "Wavelength deltas may pass display-rounding consistency while energy deltas can still require source-version reconciliation. This policy cannot validate helium prediction.",
        },
        "source_basis": {
            "current_holdout_package": helium_qd_holdouts["source"],
            "candidate_manifest_status": chianti_he_i_manifest["status"],
            "candidate_lineage_status": chianti_he_i_manifest["lineage_review"]["status"],
            "acquisition_gate_status": helium_external_holdout_acquisition_gate["status"],
        },
        "metrics": {
            "crosscheck_row_count": len(crosscheck_rows),
            "skipped_row_count": len(skipped_rows),
            "raw_file_count": len(chianti_he_i_manifest["raw_files"]),
            "raw_file_hash_count": sum(1 for row in chianti_he_i_manifest["raw_files"] if row.get("sha256")),
            "average_abs_wavelength_delta_angstrom": float(np.mean(wavelength_residuals))
            if wavelength_residuals
            else None,
            "max_abs_wavelength_delta_angstrom": max(wavelength_residuals) if wavelength_residuals else None,
            "average_abs_wavelength_delta_ppm": float(np.mean(wavelength_ppm)) if wavelength_ppm else None,
            "max_abs_wavelength_delta_ppm": max(wavelength_ppm) if wavelength_ppm else None,
            "average_abs_upper_energy_delta_cm_inverse": float(np.mean(energy_residuals))
            if energy_residuals
            else None,
            "max_abs_upper_energy_delta_cm_inverse": max(energy_residuals) if energy_residuals else None,
            "wavelength_display_rounding_pass_count": wavelength_policy_pass_count,
            "upper_energy_source_version_review_count": energy_policy_block_count,
            "blocked_requirement_count": 2,
        },
        "crosscheck_rows": crosscheck_rows,
        "skipped_rows": skipped_rows,
        "blocked_claims": [
            "independent external helium validation",
            "uncertainty-qualified CHIANTI-vs-NIST agreement",
            "first-principles helium prediction",
        ],
        "next_required_artifacts": [
            "source-version review for CHIANTI-vs-current upper-energy deltas that exceed combined display rounding",
            "non-NIST source package because CHIANTI is NIST-dependent",
        ],
        "claim_boundary": "This gate computes CHIANTI-vs-current holdout deltas after raw capture. It is not an external validation gate and cannot upgrade same-source-family helium prediction diagnostics.",
    }


def build_helium_external_holdout_source_version_reconciliation_gate(
    chianti_he_i_manifest: dict,
    helium_external_holdout_residual_crosscheck_gate: dict,
) -> dict:
    reconciliation_rows = []
    for row in helium_external_holdout_residual_crosscheck_gate.get("crosscheck_rows", []):
        upper_energy_status = row["upper_energy_rounding_policy_status"]
        wavelength_status = row["wavelength_rounding_policy_status"]
        source_version_required = upper_energy_status.startswith("BLOCKED")
        reconciliation_rows.append(
            {
                "current_holdout_id": row["current_holdout_id"],
                "current_upper_energy_cm_inverse": row["current_upper_energy_cm_inverse"],
                "chianti_upper_energy_observed_cm_inverse": row[
                    "chianti_upper_energy_observed_cm_inverse"
                ],
                "upper_energy_abs_delta_cm_inverse": row["upper_energy_abs_delta_cm_inverse"],
                "combined_upper_energy_rounding_bound_cm_inverse": row[
                    "combined_upper_energy_rounding_bound_cm_inverse"
                ],
                "upper_energy_delta_to_combined_rounding_bound_ratio": row[
                    "upper_energy_delta_to_combined_rounding_bound_ratio"
                ],
                "current_wavelength_angstrom": row["current_wavelength_angstrom"],
                "chianti_wavelength_angstrom": row["chianti_wavelength_angstrom"],
                "wavelength_abs_delta_ppm": row["wavelength_abs_delta_ppm"],
                "wavelength_rounding_policy_status": wavelength_status,
                "upper_energy_rounding_policy_status": upper_energy_status,
                "classification": "SOURCE_VERSION_RECONCILIATION_REQUIRED"
                if source_version_required
                else "DISPLAY_ROUNDING_CONSISTENT",
                "allowed_use": "cross-check bookkeeping only",
                "blocked_use": "validation residual, parameter tuning input, or claim upgrade",
                "source_locator": {
                    "chianti_wgfa_line_number": row["chianti_wgfa_line_number"],
                    "chianti_elvlc_upper_line_number": row["chianti_elvlc_upper_line_number"],
                    "current_source_family": row["current_source_family"],
                    "candidate_source_family": row["candidate_source_family"],
                    "lineage_status": row["lineage_status"],
                },
            }
        )

    source_version_rows = [
        row
        for row in reconciliation_rows
        if row["classification"] == "SOURCE_VERSION_RECONCILIATION_REQUIRED"
    ]
    wavelength_rounding_rows = [
        row
        for row in reconciliation_rows
        if row["wavelength_rounding_policy_status"].startswith("PASS")
    ]
    upper_energy_deltas = [row["upper_energy_abs_delta_cm_inverse"] for row in reconciliation_rows]
    upper_energy_ratios = [
        row["upper_energy_delta_to_combined_rounding_bound_ratio"]
        for row in reconciliation_rows
        if row["upper_energy_delta_to_combined_rounding_bound_ratio"] is not None
    ]
    status = (
        "SOURCE_VERSION_RECONCILIATION_REQUIRED"
        if source_version_rows
        else "SOURCE_VERSION_RECONCILED_BY_DISPLAY_ROUNDING"
    )
    return {
        "schema_version": "1.0",
        "role": "helium_external_holdout_source_version_reconciliation_gate",
        "status": status,
        "claim_class": "source_version_reconciliation_gate_no_validation_claim",
        "formula_id": "AT20-HELIUM-EXTERNAL-HOLDOUT-SOURCE-VERSION-RECONCILIATION",
        "source_basis": {
            "candidate_manifest_status": chianti_he_i_manifest["status"],
            "candidate_source_family": chianti_he_i_manifest["source_family"],
            "candidate_lineage_status": chianti_he_i_manifest["lineage_review"]["status"],
            "residual_crosscheck_status": helium_external_holdout_residual_crosscheck_gate["status"],
        },
        "metrics": {
            "reconciliation_row_count": len(reconciliation_rows),
            "source_version_reconciliation_required_count": len(source_version_rows),
            "display_rounding_consistent_wavelength_count": len(wavelength_rounding_rows),
            "max_upper_energy_abs_delta_cm_inverse": max(upper_energy_deltas)
            if upper_energy_deltas
            else None,
            "max_upper_energy_delta_to_rounding_bound_ratio": max(upper_energy_ratios)
            if upper_energy_ratios
            else None,
        },
        "reconciliation_rows": reconciliation_rows,
        "blocked_claims": [
            "CHIANTI upper-energy deltas validate He I level predictions",
            "source-version deltas can be ignored because wavelength display rounding passes",
            "CHIANTI can become independent validation without non-NIST source lineage",
        ],
        "next_required_artifacts": [
            "source-version locator comparing current NIST source version with CHIANTI NIST ASD v2.0/Fuhr et al. lineage",
            "non-NIST He I source package for independent validation",
            "validation-ready thresholds after source-version reconciliation and source uncertainty capture",
        ],
        "claim_boundary": "This gate separates wavelength display-rounding consistency from upper-energy source-version reconciliation. It is diagnostic source bookkeeping only and cannot validate helium predictions.",
    }


def build_atomic_claim_scope_gate(
    status: str,
    avg_error_ppm: float,
    max_error_ppm: float,
    slope_error_ppm: float,
    hydrogen_level_energy_benchmark: dict,
    hydrogen_like_checkpoint: dict,
    precision_spectroscopy_gate: dict,
    precision_baseline_gate: dict,
    precision_dirac_baseline_gate: dict,
    lamb_shift_handoff_gate: dict,
    hyperfine_21cm_gate: dict,
    hyperfine_fermi_baseline_gate: dict,
    helium_many_electron_gate: dict,
    helium_transition_assignment_gap_gate: dict,
    helium_medium_normalization_gate: dict,
    helium_line_component_policy_gate: dict,
    helium_ground_state_baseline_gate: dict,
    helium_excited_state_target_gate: dict,
    helium_excited_hydrogenic_residual_gate: dict,
    helium_quantum_defect_prediction_gate: dict,
    helium_quantum_defect_holdout_gate: dict,
    helium_quantum_defect_wavelength_holdout_gate: dict,
    atomic_predictive_model_closure_gate: dict,
    atomic_predictive_v1_fixed_correction_operator_gate: dict,
    atomic_predictive_v1_diagnostic_report_gate: dict,
    source_evidence_readiness_matrix: dict,
    branch_claim_gate: dict,
) -> dict:
    controller_status = "WARN" if status == "PASS" else "FAIL"
    return {
        "schema_version": "1.0",
        "topic": "0.20_Atomic_Physics",
        "controller_status": controller_status,
        "controller_reason": (
            "The hydrogen Rydberg benchmark, rounded hydrogen level-energy benchmark, and selected hydrogen-like ion rows are gated, "
            "but export remains warning-gated because direct level-table precision, direct Li III ASD capture, broader ion coverage, "
            "precision correction models, many-electron residual models, and first-principles derivation branches are missing."
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
                "claim": "Selected rounded hydrogen n-level energies match the ionization-energy anchored Bohr relation under declared thresholds.",
                "status": hydrogen_level_energy_benchmark["status"],
                "artifact_role": "hydrogen level-energy benchmark",
                "metrics": hydrogen_level_energy_benchmark["metrics"],
                "source_evidence_readiness": "rounded_level_source_review_ready_with_direct_ASD_precision_pending",
            },
            {
                "claim": "Selected He+ and Li2+ one-electron ion wavelengths match the reduced-mass hydrogenic relation under provisional thresholds; C VI is recorded separately as a higher-Z stress test.",
                "status": hydrogen_like_checkpoint["status"],
                "artifact_role": "hydrogen-like ion reduced-mass benchmark",
                "metrics": hydrogen_like_checkpoint["metrics"],
                "source_evidence_readiness": "provisional_source_review_ready_with_direct_Li_III_ASD_capture_pending",
            },
            {
                "claim": "Hydrogen precision spectroscopy targets for 1S-2S, Lamb shift, and 21 cm hyperfine are organized for future artifacts.",
                "status": precision_spectroscopy_gate["status"],
                "artifact_role": "precision spectroscopy source gate",
                "metrics": {
                    "source_row_count": precision_spectroscopy_gate["source_row_count"],
                    "required_model_components": len(precision_spectroscopy_gate["required_model_components"]),
                },
                "source_evidence_readiness": "source_package_ready_model_blocked",
            },
            {
                "claim": "The nonrelativistic Rydberg baseline for the hydrogen 1S-2S precision target is computed as a residual diagnostic.",
                "status": precision_baseline_gate["status"],
                "artifact_role": "precision baseline residual gate",
                "metrics": {
                    "target_id": precision_baseline_gate["target_id"],
                    "absolute_residual_hz": precision_baseline_gate["prediction"]["absolute_residual_hz"],
                    "residual_ppm": precision_baseline_gate["prediction"]["residual_ppm"],
                },
                "source_evidence_readiness": "source_ready_model_incomplete",
            },
            {
                "claim": "The leading Dirac/fine-structure baseline for the hydrogen 1S-2S precision target is computed as a residual diagnostic.",
                "status": precision_dirac_baseline_gate["status"],
                "artifact_role": "precision Dirac baseline residual gate",
                "metrics": {
                    "target_id": precision_dirac_baseline_gate["target_id"],
                    "absolute_residual_hz": precision_dirac_baseline_gate["prediction"]["absolute_residual_hz"],
                    "residual_ppm": precision_dirac_baseline_gate["prediction"]["residual_ppm"],
                },
                "source_evidence_readiness": "source_ready_qed_model_incomplete",
            },
            {
                "claim": "Source-referenced Lamb-shift values are applied as an empirical 1S-2S residual handoff after the Dirac baseline.",
                "status": lamb_shift_handoff_gate["status"],
                "artifact_role": "empirical Lamb-shift handoff gate",
                "metrics": {
                    "absolute_residual_hz": lamb_shift_handoff_gate["prediction"]["absolute_residual_hz"],
                    "residual_ppm": lamb_shift_handoff_gate["prediction"]["residual_ppm"],
                    "delta_L_2S_minus_1S_Hz": lamb_shift_handoff_gate["correction"]["delta_L_2S_minus_1S_Hz"],
                },
                "source_evidence_readiness": "source_package_ready_empirical_handoff_model_blocked",
            },
            {
                "claim": "The neutral hydrogen 21 cm hyperfine target is source-locked and converted to wavelength bookkeeping for future hyperfine artifacts.",
                "status": hyperfine_21cm_gate["status"],
                "artifact_role": "21 cm hyperfine source gate",
                "metrics": {
                    "recommended_frequency_hz": hyperfine_21cm_gate["recommended_frequency"]["value_hz"],
                    "wavelength_cm": hyperfine_21cm_gate["derived_bookkeeping"]["wavelength_cm"],
                    "topic_precision_row_delta_hz": hyperfine_21cm_gate["topic_precision_row_delta"]["delta_hz"],
                },
                "source_evidence_readiness": "source_package_ready_model_blocked",
            },
            {
                "claim": "A leading Fermi-contact baseline for the hydrogen 21 cm hyperfine transition is computed as a residual diagnostic.",
                "status": hyperfine_fermi_baseline_gate["status"],
                "artifact_role": "21 cm Fermi-contact baseline gate",
                "metrics": {
                    "fermi_contact_baseline_hz": hyperfine_fermi_baseline_gate["prediction"]["fermi_contact_baseline_hz"],
                    "absolute_residual_hz": hyperfine_fermi_baseline_gate["prediction"]["absolute_residual_hz"],
                    "residual_ppm": hyperfine_fermi_baseline_gate["prediction"]["residual_ppm"],
                },
                "source_evidence_readiness": "source_constants_ready_corrections_open",
            },
            {
                "claim": "Neutral helium visible spectral targets are organized for future many-electron artifacts.",
                "status": helium_many_electron_gate["status"],
                "artifact_role": "neutral helium many-electron source gate",
                "metrics": {
                    "source_row_count": helium_many_electron_gate["source_row_count"],
                    "required_model_components": len(helium_many_electron_gate["required_model_components"]),
                },
                "source_evidence_readiness": "source_package_ready_model_blocked",
            },
            {
                "claim": "Neutral helium source wavelengths have photon energies computed and term assignments source-locked, but residual modeling remains blocker-gated.",
                "status": helium_transition_assignment_gap_gate["status"],
                "artifact_role": "neutral helium transition-assignment gap gate",
                "metrics": helium_transition_assignment_gap_gate["metrics"],
                "source_evidence_readiness": helium_transition_assignment_gap_gate["source_evidence_readiness"],
            },
            {
                "claim": "Neutral helium visible wavelengths have air/vacuum medium normalization computed from source level-energy differences, but residual modeling remains blocker-gated.",
                "status": helium_medium_normalization_gate["status"],
                "artifact_role": "neutral helium wavelength-medium normalization gate",
                "metrics": helium_medium_normalization_gate["metrics"],
                "source_evidence_readiness": "source_medium_normalization_ready_model_blocked",
            },
            {
                "claim": "Neutral helium line-component and blend policy is source-packaged for selected rows, but residual modeling remains blocker-gated.",
                "status": helium_line_component_policy_gate["status"],
                "artifact_role": "neutral helium line-component policy gate",
                "metrics": helium_line_component_policy_gate["metrics"],
                "source_evidence_readiness": "source_component_policy_ready_model_blocked",
            },
            {
                "claim": "Neutral helium ground-state total binding is compared against independent-electron and uncorrelated variational two-electron baselines as residual diagnostics.",
                "status": helium_ground_state_baseline_gate["status"],
                "artifact_role": "neutral helium ground-state baseline residual gate",
                "metrics": {
                    "observed_total_binding_energy_eV": helium_ground_state_baseline_gate["observed_anchor"]["total_binding_energy_eV"],
                    "independent_baseline_absolute_residual_eV": helium_ground_state_baseline_gate["baselines"][0]["absolute_residual_eV"],
                    "variational_baseline_absolute_residual_eV": helium_ground_state_baseline_gate["baselines"][1]["absolute_residual_eV"],
                    "variational_gap_to_correlated_reference_eV": helium_ground_state_baseline_gate["correlation_gap_summary"]["variational_baseline_gap_to_correlated_reference_eV"],
                },
                "source_evidence_readiness": "source_ionization_energy_ready_correlation_model_blocked",
            },
            {
                "claim": "Neutral helium excited-state level targets are prepared from source term energies for future correlated spectral residuals.",
                "status": helium_excited_state_target_gate["status"],
                "artifact_role": "neutral helium excited-state target gate",
                "metrics": helium_excited_state_target_gate["metrics"],
                "source_evidence_readiness": "source_excited_state_targets_ready_model_blocked",
            },
            {
                "claim": "A zero-quantum-defect hydrogenic residual baseline is computed for selected neutral-helium excited levels.",
                "status": helium_excited_hydrogenic_residual_gate["status"],
                "artifact_role": "neutral helium excited hydrogenic residual gate",
                "metrics": helium_excited_hydrogenic_residual_gate["metrics"],
                "source_evidence_readiness": "source_targets_ready_single_active_electron_baseline_model_blocked",
            },
            {
                "claim": "A source-calibrated quantum-defect model makes limited leave-one-out predictions for selected neutral-helium series.",
                "status": helium_quantum_defect_prediction_gate["status"],
                "artifact_role": "neutral helium quantum-defect prediction gate",
                "metrics": helium_quantum_defect_prediction_gate["metrics"],
                "source_evidence_readiness": "selected_source_levels_ready_calibrated_prediction_model_blocked",
            },
            {
                "claim": "Additional same-source-family He I rows are used as holdouts for limited quantum-defect prediction diagnostics.",
                "status": helium_quantum_defect_holdout_gate["status"],
                "artifact_role": "neutral helium quantum-defect source-family holdout gate",
                "metrics": helium_quantum_defect_holdout_gate["metrics"],
                "source_evidence_readiness": "same_source_family_holdouts_ready_independent_external_validation_blocked",
            },
            {
                "claim": "Selected same-source-family He I holdout wavelengths are predicted from quantum-defect level predictions.",
                "status": helium_quantum_defect_wavelength_holdout_gate["status"],
                "artifact_role": "neutral helium quantum-defect wavelength holdout gate",
                "metrics": helium_quantum_defect_wavelength_holdout_gate["metrics"],
                "source_evidence_readiness": "same_source_family_wavelength_holdouts_ready_external_validation_and_uncertainty_blocked",
            },
            {
                "claim": "A predictive atomic-spectra closure contract now defines what must pass before claiming broad atomic prediction.",
                "status": atomic_predictive_model_closure_gate["status"],
                "artifact_role": "atomic spectral predictive model closure gate",
                "metrics": atomic_predictive_model_closure_gate["metrics"],
                "source_evidence_readiness": "governance_contract_ready_predictive_claim_blocked",
            },
            {
                "claim": "The selected predictive-v1 lane now has a diagnostic report that collects current same-source-family predictions, thresholds, and validation blockers.",
                "status": atomic_predictive_v1_diagnostic_report_gate["status"],
                "artifact_role": "atomic predictive-v1 diagnostic report gate",
                "metrics": atomic_predictive_v1_diagnostic_report_gate["metrics"],
                "source_evidence_readiness": "diagnostic_report_ready_validation_blocked",
            },
            {
                "claim": "The selected predictive-v1 lane now has a fixed-correction operator contract separating empirical quantum-defect diagnostics from acceptable CI/UET correction operators.",
                "status": atomic_predictive_v1_fixed_correction_operator_gate["status"],
                "artifact_role": "atomic predictive-v1 fixed correction operator gate",
                "metrics": atomic_predictive_v1_fixed_correction_operator_gate["metrics"],
                "source_evidence_readiness": "operator_contract_ready_implementation_missing",
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
                "blocking_reason": "The artifact now supports selected source-referenced He+/Li2+ reduced-mass benchmark rows and records C VI as a higher-Z stress test; direct Li III ASD capture, broader source-locked ion coverage, higher-Z fine/QED policy, and UET derivation are still missing.",
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
                "blocking_reason": "Precision targets are source-packaged; nonrelativistic, leading Dirac, empirical Lamb handoff, 21 cm source bookkeeping, and Fermi-contact baseline residuals are computed, but no first-principles QED/recoil/proton-radius/hyperfine correction model is primary-gated.",
                "next_evidence_required": [
                    "primary locators for secondary precision rows",
                    "Dirac fine-structure model",
                    "QED Lamb-shift model",
                    "hyperfine Hamiltonian model",
                    "uncertainty-aware residual artifact",
                ],
            },
            {
                "claim": "UET validates helium, many-electron atoms, or general atomic theory.",
                "status": "BLOCKED",
                "blocking_reason": "Neutral helium source rows, photon energies, term assignments, wavelength-medium normalization, line-component/blend policy, ground-state baseline residual diagnostics, excited-state targets, zero-quantum-defect residual baselines, limited source-calibrated quantum-defect predictions, same-source-family holdout diagnostics, and selected holdout wavelength predictions are now packaged, but a correlated two-electron Hamiltonian/spectral residual artifact is still missing.",
                "next_evidence_required": [
                    "correlated two-electron Hamiltonian/spectral model",
                    "singlet/triplet quantum-defect or configuration-interaction policy",
                    "uncertainty-aware residual thresholds",
                    "multi-atom benchmark suite",
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
            "direct_hydrogen_level_table_precision_missing",
            "direct_li_iii_asd_capture_missing",
            "general_hydrogen_like_ion_suite_missing",
            "precision_model_artifact_missing",
            "primary_precision_locators_incomplete",
            "helium_many_electron_model_artifact_missing",
            "helium_quantum_defect_or_ci_policy_missing",
            "independent_helium_prediction_holdout_missing",
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
    hydrogen_level_rows = load_json(HYDROGEN_LEVEL_PATH)
    ion_data = load_json(HYDROGEN_LIKE_ION_PATH)
    precision_sources = load_json(PRECISION_SPECTROSCOPY_PATH)
    lamb_shift_sources = load_json(HYDROGEN_LAMB_SHIFT_PATH)
    hyperfine_21cm_sources = load_json(HYDROGEN_HYPERFINE_21CM_PATH)
    hyperfine_fermi_constants = load_json(HYDROGEN_HYPERFINE_FERMI_CONSTANTS_PATH)
    helium_sources = load_json(HELIUM_MANY_ELECTRON_PATH)
    helium_assignments = load_json(HELIUM_TRANSITION_ASSIGNMENTS_PATH)
    helium_ground_sources = load_json(HELIUM_GROUND_STATE_ENERGY_PATH)
    helium_qd_holdouts = load_json(HELIUM_QD_HOLDOUT_PATH)
    atomic_predictive_v1_parameter_manifest = load_json(ATOMIC_PREDICTIVE_V1_PARAMETER_MANIFEST_PATH)
    atomic_predictive_v1_threshold_manifest = load_json(ATOMIC_PREDICTIVE_V1_THRESHOLD_MANIFEST_PATH)
    atomic_predictive_v1_operator_manifest = load_json(ATOMIC_PREDICTIVE_V1_OPERATOR_MANIFEST_PATH)
    atomic_predictive_v1_operator_build_spec_manifest = load_json(
        ATOMIC_PREDICTIVE_V1_OPERATOR_BUILD_SPEC_MANIFEST_PATH
    )
    chianti_he_i_manifest = load_json(CHIANTI_HE_I_MANIFEST_PATH)
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
        absolute_residual_nm = abs(predicted_nm - observed_nm)
        wavelength_uncertainty_nm = row.get("wavelength_vacuum_uncertainty_nm")
        residual_to_uncertainty_ratio = (
            absolute_residual_nm / wavelength_uncertainty_nm if wavelength_uncertainty_nm else None
        )
        error_ppm = absolute_residual_nm / observed_nm * 1e6
        inv_lam = 1.0 / (observed_nm * 1e-9)
        x_vals.append(term)
        y_vals.append(inv_lam)
        results.append(
            {
                **row,
                "geometric_term": term,
                "predicted_wavelength_nm": predicted_nm,
                "absolute_wavelength_residual_nm": absolute_residual_nm,
                "residual_to_source_uncertainty_ratio": residual_to_uncertainty_ratio,
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
    line_uncertainty_rows = [
        row for row in results if row.get("residual_to_source_uncertainty_ratio") is not None
    ]
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
    hydrogen_rydberg_line_uncertainty_gate = build_hydrogen_rydberg_line_uncertainty_gate(spectrum, results)
    hydrogen_level_energy_benchmark = build_hydrogen_level_energy_benchmark(hydrogen_level_rows)
    hydrogen_like_checkpoint = build_hydrogen_like_checkpoint(codata, ion_data)
    hydrogen_like_domain_coverage_gate = build_hydrogen_like_domain_coverage_gate(hydrogen_like_checkpoint, ion_data)
    precision_spectroscopy_gate = build_precision_spectroscopy_gate(precision_sources)
    precision_baseline_gate = build_precision_baseline_gate(precision_sources, codata)
    precision_dirac_baseline_gate = build_precision_dirac_baseline_gate(precision_sources, codata)
    lamb_shift_handoff_gate = build_lamb_shift_handoff_gate(lamb_shift_sources, precision_dirac_baseline_gate)
    hyperfine_21cm_gate = build_hyperfine_21cm_gate(hyperfine_21cm_sources, precision_sources)
    hyperfine_fermi_baseline_gate = build_hyperfine_fermi_baseline_gate(
        hyperfine_21cm_gate, hyperfine_fermi_constants, codata
    )
    helium_many_electron_gate = build_helium_many_electron_gate(helium_sources)
    helium_transition_assignment_gap_gate = build_helium_transition_assignment_gap_gate(
        helium_sources, helium_assignments
    )
    helium_medium_normalization_gate = build_helium_medium_normalization_gate(
        helium_transition_assignment_gap_gate
    )
    helium_line_component_policy_gate = build_helium_line_component_policy_gate(
        helium_transition_assignment_gap_gate
    )
    helium_ground_state_baseline_gate = build_helium_ground_state_baseline_gate(
        helium_ground_sources, codata
    )
    helium_excited_state_target_gate = build_helium_excited_state_target_gate(
        helium_transition_assignment_gap_gate, helium_ground_state_baseline_gate
    )
    helium_excited_hydrogenic_residual_gate = build_helium_excited_hydrogenic_residual_gate(
        codata, helium_ground_state_baseline_gate, helium_excited_state_target_gate
    )
    helium_fixed_screening_baseline_gate = build_helium_fixed_screening_baseline_gate(
        helium_excited_hydrogenic_residual_gate
    )
    helium_quantum_defect_prediction_gate = build_helium_quantum_defect_prediction_gate(
        helium_excited_hydrogenic_residual_gate
    )
    helium_quantum_defect_holdout_gate = build_helium_quantum_defect_holdout_gate(
        helium_ground_state_baseline_gate,
        helium_quantum_defect_prediction_gate,
        helium_qd_holdouts,
    )
    helium_quantum_defect_wavelength_holdout_gate = build_helium_quantum_defect_wavelength_holdout_gate(
        helium_quantum_defect_holdout_gate,
        helium_qd_holdouts,
    )
    atomic_prediction_baseline_comparator_gate = build_atomic_prediction_baseline_comparator_gate(
        precision_baseline_gate,
        precision_dirac_baseline_gate,
        lamb_shift_handoff_gate,
        hyperfine_fermi_baseline_gate,
        helium_excited_hydrogenic_residual_gate,
        helium_fixed_screening_baseline_gate,
        helium_quantum_defect_prediction_gate,
        helium_quantum_defect_holdout_gate,
        helium_quantum_defect_wavelength_holdout_gate,
    )
    legacy_multielectron_code_audit_gate = build_legacy_multielectron_code_audit_gate()
    uet_atomic_operator_readiness_gate = build_uet_atomic_operator_readiness_gate(atomic_formula_bridge_manifest)
    atomic_uncertainty_readiness_gate = build_atomic_uncertainty_readiness_gate(
        hydrogen_rydberg_line_uncertainty_gate,
        hydrogen_level_energy_benchmark,
        hydrogen_like_checkpoint,
        precision_baseline_gate,
        precision_dirac_baseline_gate,
        lamb_shift_handoff_gate,
        hyperfine_21cm_gate,
        hyperfine_fermi_baseline_gate,
        helium_ground_state_baseline_gate,
        helium_quantum_defect_prediction_gate,
        helium_quantum_defect_holdout_gate,
        helium_quantum_defect_wavelength_holdout_gate,
    )
    atomic_residual_uncertainty_budget_gate = build_atomic_residual_uncertainty_budget_gate(
        hydrogen_rydberg_line_uncertainty_gate,
        precision_baseline_gate,
        precision_dirac_baseline_gate,
        lamb_shift_handoff_gate,
        hyperfine_21cm_gate,
        hyperfine_fermi_baseline_gate,
        helium_ground_state_baseline_gate,
        helium_quantum_defect_holdout_gate,
        helium_quantum_defect_wavelength_holdout_gate,
    )
    atomic_fixed_parameter_model_readiness_gate = build_atomic_fixed_parameter_model_readiness_gate(
        hydrogen_like_checkpoint,
        precision_dirac_baseline_gate,
        lamb_shift_handoff_gate,
        hyperfine_fermi_baseline_gate,
        helium_fixed_screening_baseline_gate,
        helium_quantum_defect_prediction_gate,
        helium_quantum_defect_holdout_gate,
        atomic_prediction_baseline_comparator_gate,
        legacy_multielectron_code_audit_gate,
        uet_atomic_operator_readiness_gate,
    )
    atomic_predictive_model_closure_gate = build_atomic_predictive_model_closure_gate(
        hydrogen_like_checkpoint,
        hydrogen_like_domain_coverage_gate,
        precision_dirac_baseline_gate,
        lamb_shift_handoff_gate,
        hyperfine_fermi_baseline_gate,
        helium_excited_hydrogenic_residual_gate,
        helium_quantum_defect_prediction_gate,
        helium_quantum_defect_holdout_gate,
        helium_quantum_defect_wavelength_holdout_gate,
        atomic_prediction_baseline_comparator_gate,
        atomic_uncertainty_readiness_gate,
        atomic_residual_uncertainty_budget_gate,
        atomic_fixed_parameter_model_readiness_gate,
        legacy_multielectron_code_audit_gate,
        uet_atomic_operator_readiness_gate,
    )
    atomic_predictive_model_spec_gate = build_atomic_predictive_model_spec_gate(
        atomic_predictive_model_closure_gate,
        atomic_fixed_parameter_model_readiness_gate,
        uet_atomic_operator_readiness_gate,
        hydrogen_like_domain_coverage_gate,
        atomic_uncertainty_readiness_gate,
    )
    atomic_first_predictive_implementation_candidate_gate = (
        build_atomic_first_predictive_implementation_candidate_gate(
            atomic_predictive_model_spec_gate,
            helium_quantum_defect_prediction_gate,
            helium_quantum_defect_holdout_gate,
            helium_quantum_defect_wavelength_holdout_gate,
            atomic_prediction_baseline_comparator_gate,
            atomic_residual_uncertainty_budget_gate,
        )
    )
    helium_external_holdout_acquisition_gate = build_helium_external_holdout_acquisition_gate(
        atomic_first_predictive_implementation_candidate_gate,
        chianti_he_i_manifest,
    )
    helium_external_holdout_residual_crosscheck_gate = (
        build_helium_external_holdout_residual_crosscheck_gate(
            helium_qd_holdouts,
            chianti_he_i_manifest,
            helium_external_holdout_acquisition_gate,
        )
    )
    helium_external_holdout_source_version_reconciliation_gate = (
        build_helium_external_holdout_source_version_reconciliation_gate(
            chianti_he_i_manifest,
            helium_external_holdout_residual_crosscheck_gate,
        )
    )
    atomic_predictive_v1_parameter_lock_gate = build_atomic_predictive_v1_parameter_lock_gate(
        atomic_predictive_v1_parameter_manifest,
        atomic_first_predictive_implementation_candidate_gate,
        helium_quantum_defect_holdout_gate,
        helium_external_holdout_residual_crosscheck_gate,
    )
    atomic_predictive_v1_threshold_gate = build_atomic_predictive_v1_threshold_gate(
        atomic_predictive_v1_threshold_manifest,
        helium_quantum_defect_holdout_gate,
        helium_quantum_defect_wavelength_holdout_gate,
        atomic_predictive_v1_parameter_lock_gate,
    )
    helium_external_holdout_lineage_decision_gate = build_helium_external_holdout_lineage_decision_gate(
        chianti_he_i_manifest,
        helium_external_holdout_acquisition_gate,
        helium_external_holdout_residual_crosscheck_gate,
    )
    atomic_predictive_v1_fixed_correction_operator_gate = build_atomic_predictive_v1_fixed_correction_operator_gate(
        atomic_predictive_v1_operator_manifest,
        atomic_predictive_v1_parameter_lock_gate,
        atomic_fixed_parameter_model_readiness_gate,
        uet_atomic_operator_readiness_gate,
    )
    atomic_predictive_v1_operator_candidate_resolution_gate = (
        build_atomic_predictive_v1_operator_candidate_resolution_gate(
            atomic_predictive_v1_operator_manifest,
            atomic_fixed_parameter_model_readiness_gate,
            atomic_prediction_baseline_comparator_gate,
            atomic_predictive_v1_fixed_correction_operator_gate,
            uet_atomic_operator_readiness_gate,
        )
    )
    atomic_predictive_v1_operator_build_spec_gate = build_atomic_predictive_v1_operator_build_spec_gate(
        atomic_predictive_v1_operator_build_spec_manifest,
        atomic_predictive_v1_fixed_correction_operator_gate,
        atomic_predictive_v1_operator_candidate_resolution_gate,
    )
    atomic_predictive_v1_diagnostic_report_gate = build_atomic_predictive_v1_diagnostic_report_gate(
        atomic_predictive_v1_parameter_manifest,
        atomic_predictive_v1_threshold_manifest,
        helium_quantum_defect_holdout_gate,
        helium_quantum_defect_wavelength_holdout_gate,
        atomic_predictive_v1_parameter_lock_gate,
        atomic_predictive_v1_threshold_gate,
        atomic_predictive_v1_fixed_correction_operator_gate,
        helium_external_holdout_lineage_decision_gate,
    )
    atomic_predictive_model_blueprint_gate = build_atomic_predictive_model_blueprint_gate(
        atomic_predictive_model_closure_gate,
        atomic_predictive_model_spec_gate,
        atomic_first_predictive_implementation_candidate_gate,
        atomic_predictive_v1_parameter_lock_gate,
        atomic_predictive_v1_threshold_gate,
        atomic_predictive_v1_fixed_correction_operator_gate,
        helium_external_holdout_lineage_decision_gate,
        atomic_prediction_baseline_comparator_gate,
        atomic_uncertainty_readiness_gate,
        atomic_fixed_parameter_model_readiness_gate,
        uet_atomic_operator_readiness_gate,
        helium_external_holdout_acquisition_gate,
        helium_external_holdout_residual_crosscheck_gate,
    )
    atomic_claim_scope_gate = build_atomic_claim_scope_gate(
        status,
        avg_error_ppm,
        max_error_ppm,
        slope_error_ppm,
        hydrogen_level_energy_benchmark,
        hydrogen_like_checkpoint,
        precision_spectroscopy_gate,
        precision_baseline_gate,
        precision_dirac_baseline_gate,
        lamb_shift_handoff_gate,
        hyperfine_21cm_gate,
        hyperfine_fermi_baseline_gate,
        helium_many_electron_gate,
        helium_transition_assignment_gap_gate,
        helium_medium_normalization_gate,
        helium_line_component_policy_gate,
        helium_ground_state_baseline_gate,
        helium_excited_state_target_gate,
        helium_excited_hydrogenic_residual_gate,
        helium_quantum_defect_prediction_gate,
        helium_quantum_defect_holdout_gate,
        helium_quantum_defect_wavelength_holdout_gate,
        atomic_predictive_model_closure_gate,
        atomic_predictive_v1_fixed_correction_operator_gate,
        atomic_predictive_v1_diagnostic_report_gate,
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
                "uncertainty_policy_status": spectrum.get("uncertainty_policy", {}).get("status"),
            },
            {
                "path": str(CODATA_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(CODATA_PATH),
                "source": codata.get("source"),
                "doi": codata.get("publication", {}).get("doi"),
            },
            {
                "path": str(HYDROGEN_LEVEL_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(HYDROGEN_LEVEL_PATH),
                "source": "Local rounded hydrogen n-level working copy anchored to NIST H ionization energy.",
                "source_status": "source_referenced_local_level_rows",
            },
            {
                "path": str(HYDROGEN_LIKE_ION_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(HYDROGEN_LIKE_ION_PATH),
                "source": ion_data.get("purpose"),
                "source_rows": [row["source_status"] for row in ion_data["lines"]],
            },
            {
                "path": str(PRECISION_SPECTROSCOPY_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(PRECISION_SPECTROSCOPY_PATH),
                "source": precision_sources.get("purpose"),
                "status": precision_sources.get("status"),
                "source_rows": [row["target_id"] for row in precision_sources["rows"]],
            },
            {
                "path": str(HYDROGEN_LAMB_SHIFT_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(HYDROGEN_LAMB_SHIFT_PATH),
                "source": lamb_shift_sources.get("purpose"),
                "status": lamb_shift_sources.get("status"),
                "source_rows": [row["target_id"] for row in lamb_shift_sources["rows"]],
            },
            {
                "path": str(HYDROGEN_HYPERFINE_21CM_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(HYDROGEN_HYPERFINE_21CM_PATH),
                "source": hyperfine_21cm_sources.get("purpose"),
                "status": hyperfine_21cm_sources.get("status"),
                "source_rows": [
                    hyperfine_21cm_sources["recommended_transition"]["target_id"],
                    hyperfine_21cm_sources["metrology_cross_check"]["target_id"],
                ],
            },
            {
                "path": str(HYDROGEN_HYPERFINE_FERMI_CONSTANTS_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(HYDROGEN_HYPERFINE_FERMI_CONSTANTS_PATH),
                "source": hyperfine_fermi_constants.get("purpose"),
                "status": hyperfine_fermi_constants.get("status"),
                "source_rows": ["proton_g_factor"],
            },
            {
                "path": str(HELIUM_MANY_ELECTRON_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(HELIUM_MANY_ELECTRON_PATH),
                "source": helium_sources.get("purpose"),
                "status": helium_sources.get("status"),
                "source_rows": [row["wavelength_nm"] for row in helium_sources["neutral_helium_lines"]],
            },
            {
                "path": str(HELIUM_TRANSITION_ASSIGNMENTS_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(HELIUM_TRANSITION_ASSIGNMENTS_PATH),
                "source": helium_assignments.get("purpose"),
                "status": helium_assignments.get("status"),
                "source_rows": [row["wavelength_nm"] for row in helium_assignments["assignments"]],
            },
            {
                "path": str(HELIUM_GROUND_STATE_ENERGY_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(HELIUM_GROUND_STATE_ENERGY_PATH),
                "source": helium_ground_sources.get("purpose"),
                "status": helium_ground_sources.get("status"),
                "source_rows": [row["quantity"] for row in helium_ground_sources["rows"]],
            },
            {
                "path": str(HELIUM_QD_HOLDOUT_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(HELIUM_QD_HOLDOUT_PATH),
                "source": helium_qd_holdouts.get("purpose"),
                "status": helium_qd_holdouts.get("status"),
                "source_rows": [row["holdout_id"] for row in helium_qd_holdouts["holdout_levels"]],
            },
            {
                "path": str(ATOMIC_PREDICTIVE_V1_PARAMETER_MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(ATOMIC_PREDICTIVE_V1_PARAMETER_MANIFEST_PATH),
                "source": atomic_predictive_v1_parameter_manifest.get("purpose"),
                "status": atomic_predictive_v1_parameter_manifest.get("status"),
                "source_rows": [
                    atomic_predictive_v1_parameter_manifest.get("selected_lane_id"),
                    atomic_predictive_v1_parameter_manifest.get("current_diagnostic_lane_id"),
                ],
            },
            {
                "path": str(ATOMIC_PREDICTIVE_V1_THRESHOLD_MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(ATOMIC_PREDICTIVE_V1_THRESHOLD_MANIFEST_PATH),
                "source": atomic_predictive_v1_threshold_manifest.get("purpose"),
                "status": atomic_predictive_v1_threshold_manifest.get("status"),
                "source_rows": [
                    row["threshold_id"] for row in atomic_predictive_v1_threshold_manifest.get("thresholds", [])
                ],
            },
            {
                "path": str(ATOMIC_PREDICTIVE_V1_OPERATOR_MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(ATOMIC_PREDICTIVE_V1_OPERATOR_MANIFEST_PATH),
                "source": atomic_predictive_v1_operator_manifest.get("purpose"),
                "status": atomic_predictive_v1_operator_manifest.get("status"),
                "source_rows": [
                    row["candidate_id"] for row in atomic_predictive_v1_operator_manifest.get("operator_candidates", [])
                ],
            },
            {
                "path": str(ATOMIC_PREDICTIVE_V1_OPERATOR_BUILD_SPEC_MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(ATOMIC_PREDICTIVE_V1_OPERATOR_BUILD_SPEC_MANIFEST_PATH),
                "source": atomic_predictive_v1_operator_build_spec_manifest.get("purpose"),
                "status": atomic_predictive_v1_operator_build_spec_manifest.get("status"),
                "source_rows": [
                    row["lane_id"]
                    for row in atomic_predictive_v1_operator_build_spec_manifest.get("implementation_lanes", [])
                ],
            },
            {
                "path": str(CHIANTI_HE_I_MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(CHIANTI_HE_I_MANIFEST_PATH),
                "source": chianti_he_i_manifest["source_family"]["name"],
                "status": chianti_he_i_manifest["status"],
                "source_rows": [row["current_holdout_id"] for row in chianti_he_i_manifest["overlap_rows"]],
            },
        ],
        "formula_ids": [
            "AT20-PHOTON-TRANSITION",
            "AT20-DEBROGLIE-STANDING-WAVE",
            "AT20-BOHR-HYDROGEN-ENERGY",
            "AT20-HYDROGEN-LEVEL-ENERGY-BENCHMARK",
            "AT20-RYDBERG-WAVELENGTH",
            "AT20-RH-CODATA-CHECKPOINT",
            "AT20-SPECTRUM-RESIDUAL",
            "AT20-HYDROGEN-RYDBERG-LINE-TRANSCRIPTION-BUDGET",
            "AT20-HYDROGENIC-Z2-CHECKPOINT",
            "AT20-HYDROGEN-LIKE-DOMAIN-COVERAGE",
            "AT20-HYDROGEN-PRECISION-SOURCE-GATE",
            "AT20-HYDROGEN-1S2S-RYDBERG-BASELINE",
            "AT20-HYDROGEN-1S2S-DIRAC-BASELINE",
            "AT20-HYDROGEN-1S2S-LAMB-HANDOFF",
            "AT20-HYDROGEN-21CM-HYPERFINE-SOURCE-GATE",
            "AT20-HYDROGEN-21CM-FERMI-BASELINE",
            "AT20-HELIUM-MANY-ELECTRON-SOURCE-GATE",
            "AT20-HELIUM-PHOTON-ENERGY-GAP",
            "AT20-HELIUM-MEDIUM-NORMALIZATION-GAP",
            "AT20-HELIUM-LINE-COMPONENT-POLICY-GAP",
            "AT20-HELIUM-INDEPENDENT-ELECTRON-BASELINE",
            "AT20-HELIUM-VARIATIONAL-ZETA-BASELINE",
            "AT20-HELIUM-EXCITED-STATE-TARGET-GAP",
            "AT20-HELIUM-ZERO-QUANTUM-DEFECT-BASELINE",
            "AT20-HELIUM-FIXED-SCREENING-BASELINE",
            "AT20-HELIUM-QUANTUM-DEFECT-LOO-PREDICTION",
            "AT20-HELIUM-QUANTUM-DEFECT-SOURCE-FAMILY-HOLDOUT",
            "AT20-HELIUM-QUANTUM-DEFECT-HOLDOUT-WAVELENGTH",
            "AT20-LEGACY-MULTIELECTRON-CODE-AUDIT",
            "AT20-ATOMIC-PREDICTION-BASELINE-COMPARATOR",
            "AT20-ATOMIC-UNCERTAINTY-READINESS-GATE",
            "AT20-ATOMIC-RESIDUAL-UNCERTAINTY-BUDGET",
            "AT20-ATOMIC-FIXED-PARAMETER-MODEL-READINESS",
            "AT20-ATOMIC-PREDICTIVE-CLOSURE-GATE",
            "AT20-ATOMIC-PREDICTIVE-MODEL-SPEC",
            "AT20-ATOMIC-FIRST-PREDICTIVE-IMPLEMENTATION-CANDIDATE",
            "AT20-ATOMIC-PREDICTIVE-V1-PARAMETER-LOCK",
            "AT20-ATOMIC-PREDICTIVE-V1-THRESHOLD-GATE",
            "AT20-ATOMIC-PREDICTIVE-V1-FIXED-CORRECTION-OPERATOR",
            "AT20-ATOMIC-PREDICTIVE-V1-OPERATOR-CANDIDATE-RESOLUTION",
            "AT20-ATOMIC-PREDICTIVE-V1-OPERATOR-BUILD-SPEC",
            "AT20-ATOMIC-PREDICTIVE-V1-DIAGNOSTIC-REPORT",
            "AT20-ATOMIC-PREDICTIVE-MODEL-BLUEPRINT",
            "AT20-HELIUM-EXTERNAL-HOLDOUT-ACQUISITION",
            "AT20-HELIUM-EXTERNAL-HOLDOUT-RESIDUAL-CROSSCHECK",
            "AT20-HELIUM-EXTERNAL-HOLDOUT-SOURCE-VERSION-RECONCILIATION",
            "AT20-HELIUM-EXTERNAL-HOLDOUT-LINEAGE-DECISION",
            "AT20-UET-ATOMIC-BRIDGE-GATE",
            "AT20-UET-ATOMIC-OPERATOR-READINESS",
        ],
        "threshold": threshold,
        "metrics": {
            "R_H_codata_m_inverse": r_h,
            "R_infinity_codata_m_inverse": r_infinity,
            "fitted_slope_through_origin_m_inverse": slope_origin,
            "slope_error_ppm": slope_error_ppm,
            "average_wavelength_error_ppm": avg_error_ppm,
            "max_wavelength_error_ppm": max_error_ppm,
            "hydrogen_rydberg_lines_with_source_uncertainty": hydrogen_rydberg_line_uncertainty_gate["metrics"][
                "lines_with_source_uncertainty_count"
            ],
            "hydrogen_rydberg_max_residual_to_source_uncertainty_ratio": hydrogen_rydberg_line_uncertainty_gate[
                "metrics"
            ]["max_residual_to_source_uncertainty_ratio"],
            "line_count": len(results),
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
            "blocked_claim_exports": len(atomic_claim_scope_gate["blocked_export_phrases"]),
            "formula_bridge_steps": len(atomic_formula_bridge_manifest["dependency_chain"]),
            "hydrogen_level_count": hydrogen_level_energy_benchmark["metrics"]["level_count"],
            "hydrogen_level_avg_error_ppm": hydrogen_level_energy_benchmark["metrics"]["average_energy_error_ppm"],
            "hydrogen_level_max_error_ppm": hydrogen_level_energy_benchmark["metrics"]["max_energy_error_ppm"],
            "hydrogen_like_checkpoint_predictions": len(hydrogen_like_checkpoint["predictions"]),
            "hydrogen_like_avg_error_ppm": hydrogen_like_checkpoint["metrics"]["average_wavelength_error_ppm"],
            "hydrogen_like_max_error_ppm": hydrogen_like_checkpoint["metrics"]["max_wavelength_error_ppm"],
            "hydrogen_like_represented_z_count": hydrogen_like_domain_coverage_gate["metrics"]["represented_z_count"],
            "hydrogen_like_domain_coverage_blocking_checks": hydrogen_like_domain_coverage_gate["metrics"][
                "blocking_coverage_check_count"
            ],
            "precision_source_rows": precision_spectroscopy_gate["source_row_count"],
            "precision_required_model_components": len(precision_spectroscopy_gate["required_model_components"]),
            "precision_1s2s_baseline_residual_hz": precision_baseline_gate["prediction"]["absolute_residual_hz"],
            "precision_1s2s_baseline_residual_ppm": precision_baseline_gate["prediction"]["residual_ppm"],
            "precision_1s2s_dirac_baseline_residual_hz": precision_dirac_baseline_gate["prediction"]["absolute_residual_hz"],
            "precision_1s2s_dirac_baseline_residual_ppm": precision_dirac_baseline_gate["prediction"]["residual_ppm"],
            "precision_1s2s_lamb_handoff_residual_hz": lamb_shift_handoff_gate["prediction"]["absolute_residual_hz"],
            "precision_1s2s_lamb_handoff_residual_ppm": lamb_shift_handoff_gate["prediction"]["residual_ppm"],
            "hyperfine_21cm_reference_hz": hyperfine_21cm_gate["recommended_frequency"]["value_hz"],
            "hyperfine_21cm_wavelength_cm": hyperfine_21cm_gate["derived_bookkeeping"]["wavelength_cm"],
            "hyperfine_21cm_topic_row_delta_hz": hyperfine_21cm_gate["topic_precision_row_delta"]["delta_hz"],
            "hyperfine_21cm_fermi_baseline_residual_hz": hyperfine_fermi_baseline_gate["prediction"]["absolute_residual_hz"],
            "hyperfine_21cm_fermi_baseline_residual_ppm": hyperfine_fermi_baseline_gate["prediction"]["residual_ppm"],
            "helium_source_rows": helium_many_electron_gate["source_row_count"],
            "helium_required_model_components": len(helium_many_electron_gate["required_model_components"]),
            "helium_photon_energy_min_ev": helium_transition_assignment_gap_gate["metrics"]["min_photon_energy_ev"],
            "helium_photon_energy_max_ev": helium_transition_assignment_gap_gate["metrics"]["max_photon_energy_ev"],
            "helium_rows_with_transition_assignment": helium_transition_assignment_gap_gate["metrics"]["rows_with_transition_assignment"],
            "helium_rows_missing_transition_assignment": helium_transition_assignment_gap_gate["metrics"]["rows_missing_transition_assignment"],
            "helium_medium_normalized_rows": helium_medium_normalization_gate["metrics"]["normalized_row_count"],
            "helium_medium_rows_missing_normalization": helium_medium_normalization_gate["metrics"]["rows_missing_normalization"],
            "helium_air_to_vacuum_factor_min": helium_medium_normalization_gate["metrics"]["min_air_to_vacuum_factor"],
            "helium_air_to_vacuum_factor_max": helium_medium_normalization_gate["metrics"]["max_air_to_vacuum_factor"],
            "helium_component_policy_rows": helium_line_component_policy_gate["metrics"]["rows_with_component_policy"],
            "helium_blend_rows": helium_line_component_policy_gate["metrics"]["blend_rows"],
            "helium_components_checked": helium_line_component_policy_gate["metrics"]["total_components_checked"],
            "helium_e1_allowed_components": helium_line_component_policy_gate["metrics"]["e1_allowed_components"],
            "helium_ground_observed_total_binding_eV": helium_ground_state_baseline_gate["observed_anchor"]["total_binding_energy_eV"],
            "helium_ground_independent_baseline_residual_eV": helium_ground_state_baseline_gate["baselines"][0]["absolute_residual_eV"],
            "helium_ground_variational_baseline_residual_eV": helium_ground_state_baseline_gate["baselines"][1]["absolute_residual_eV"],
            "helium_ground_variational_gap_to_correlated_reference_eV": helium_ground_state_baseline_gate["correlation_gap_summary"]["variational_baseline_gap_to_correlated_reference_eV"],
            "helium_ground_correlated_reference_minus_observed_eV": helium_ground_state_baseline_gate["correlation_gap_summary"]["correlated_reference_minus_observed_eV"],
            "helium_excited_state_unique_levels": helium_excited_state_target_gate["metrics"]["unique_level_count"],
            "helium_excited_state_transition_targets": helium_excited_state_target_gate["metrics"]["transition_target_count"],
            "helium_excited_state_max_air_photon_vs_level_delta_abs_eV": helium_excited_state_target_gate["metrics"]["max_air_photon_vs_level_delta_abs_eV"],
            "helium_excited_hydrogenic_residual_levels": helium_excited_hydrogenic_residual_gate["metrics"]["computed_level_count"],
            "helium_excited_hydrogenic_avg_abs_residual_eV": helium_excited_hydrogenic_residual_gate["metrics"]["average_abs_binding_residual_eV"],
            "helium_excited_hydrogenic_max_abs_residual_eV": helium_excited_hydrogenic_residual_gate["metrics"]["max_abs_binding_residual_eV"],
            "helium_excited_hydrogenic_quantum_defect_min": helium_excited_hydrogenic_residual_gate["metrics"]["min_effective_quantum_defect"],
            "helium_excited_hydrogenic_quantum_defect_max": helium_excited_hydrogenic_residual_gate["metrics"]["max_effective_quantum_defect"],
            "helium_fixed_screening_avg_abs_residual_eV": helium_fixed_screening_baseline_gate["metrics"]["average_abs_binding_residual_eV"],
            "helium_fixed_screening_max_abs_residual_eV": helium_fixed_screening_baseline_gate["metrics"]["max_abs_binding_residual_eV"],
            "helium_fixed_screening_rows_improved_vs_zero_qd": helium_fixed_screening_baseline_gate["metrics"]["rows_improved_vs_zero_qd"],
            "helium_quantum_defect_prediction_count": helium_quantum_defect_prediction_gate["metrics"]["prediction_count"],
            "helium_quantum_defect_prediction_avg_abs_residual_eV": helium_quantum_defect_prediction_gate["metrics"]["average_abs_excitation_residual_eV"],
            "helium_quantum_defect_prediction_max_abs_residual_eV": helium_quantum_defect_prediction_gate["metrics"]["max_abs_excitation_residual_eV"],
            "helium_quantum_defect_holdout_prediction_count": helium_quantum_defect_holdout_gate["metrics"]["prediction_count"],
            "helium_quantum_defect_holdout_skipped_levels": helium_quantum_defect_holdout_gate["metrics"]["skipped_level_count"],
            "helium_quantum_defect_holdout_avg_abs_residual_eV": helium_quantum_defect_holdout_gate["metrics"]["average_abs_excitation_residual_eV"],
            "helium_quantum_defect_holdout_max_abs_residual_eV": helium_quantum_defect_holdout_gate["metrics"]["max_abs_excitation_residual_eV"],
            "helium_quantum_defect_wavelength_holdout_prediction_count": helium_quantum_defect_wavelength_holdout_gate["metrics"]["predicted_line_count"],
            "helium_quantum_defect_wavelength_holdout_skipped_lines": helium_quantum_defect_wavelength_holdout_gate["metrics"]["skipped_line_count"],
            "helium_quantum_defect_wavelength_holdout_avg_abs_residual_angstrom": helium_quantum_defect_wavelength_holdout_gate["metrics"]["average_abs_wavelength_residual_angstrom"],
            "helium_quantum_defect_wavelength_holdout_max_abs_residual_angstrom": helium_quantum_defect_wavelength_holdout_gate["metrics"]["max_abs_wavelength_residual_angstrom"],
            "helium_quantum_defect_wavelength_holdout_avg_abs_residual_ppm": helium_quantum_defect_wavelength_holdout_gate["metrics"]["average_abs_wavelength_residual_ppm"],
            "helium_quantum_defect_wavelength_holdout_max_abs_residual_ppm": helium_quantum_defect_wavelength_holdout_gate["metrics"]["max_abs_wavelength_residual_ppm"],
            "legacy_multielectron_scripts_audited": legacy_multielectron_code_audit_gate["metrics"]["scripts_present"],
            "legacy_multielectron_primary_evidence_script_count": legacy_multielectron_code_audit_gate["metrics"][
                "primary_evidence_script_count"
            ],
            "atomic_prediction_comparator_count": atomic_prediction_baseline_comparator_gate["metrics"]["comparator_count"],
            "atomic_prediction_comparators_missing_external_or_ci_baseline": atomic_prediction_baseline_comparator_gate[
                "metrics"
            ]["comparators_missing_external_or_ci_baseline"],
            "atomic_uncertainty_readiness_lanes": atomic_uncertainty_readiness_gate["metrics"]["lane_count"],
            "atomic_uncertainty_propagation_blocked_lanes": atomic_uncertainty_readiness_gate["metrics"][
                "propagation_blocked_lane_count"
            ],
            "atomic_uncertainty_budget_rows": atomic_residual_uncertainty_budget_gate["metrics"]["budget_row_count"],
            "atomic_uncertainty_budget_computable_rows": atomic_residual_uncertainty_budget_gate["metrics"][
                "computable_source_uncertainty_row_count"
            ],
            "atomic_uncertainty_budget_source_missing_rows": atomic_residual_uncertainty_budget_gate["metrics"][
                "source_uncertainty_missing_row_count"
            ],
            "atomic_uncertainty_budget_max_ratio": atomic_residual_uncertainty_budget_gate["metrics"][
                "max_residual_to_source_uncertainty_ratio"
            ],
            "atomic_fixed_parameter_model_lanes": atomic_fixed_parameter_model_readiness_gate["metrics"]["model_lane_count"],
            "atomic_missing_required_model_lanes": atomic_fixed_parameter_model_readiness_gate["metrics"][
                "missing_required_model_count"
            ],
            "uet_atomic_operator_blocking_requirements": uet_atomic_operator_readiness_gate["metrics"][
                "blocking_requirement_count"
            ],
            "uet_operator_residual_lane_present": uet_atomic_operator_readiness_gate["metrics"][
                "uet_operator_residual_lane_present"
            ],
            "atomic_predictive_closure_open_or_partial_checks": atomic_predictive_model_closure_gate["metrics"]["open_or_partial_check_count"],
            "atomic_predictive_closure_fail_open_checks": atomic_predictive_model_closure_gate["metrics"]["fail_open_check_count"],
            "atomic_predictive_model_spec_blockers": atomic_predictive_model_spec_gate["metrics"][
                "blocking_implementation_blocker_count"
            ],
            "atomic_predictive_model_spec_blocked_lanes": atomic_predictive_model_spec_gate["metrics"][
                "development_lanes_blocked"
            ],
            "atomic_first_predictive_candidate_blockers": atomic_first_predictive_implementation_candidate_gate[
                "metrics"
            ]["blocking_success_criterion_count"],
            "atomic_first_predictive_candidate_selected_level_holdouts": (
                atomic_first_predictive_implementation_candidate_gate["metrics"][
                    "selected_level_holdout_prediction_count"
                ]
            ),
            "atomic_first_predictive_candidate_selected_wavelength_holdouts": (
                atomic_first_predictive_implementation_candidate_gate["metrics"][
                    "selected_wavelength_holdout_prediction_count"
                ]
            ),
            "atomic_predictive_v1_parameter_lock_policy_fail_count": atomic_predictive_v1_parameter_lock_gate[
                "metrics"
            ]["policy_fail_count"],
            "atomic_predictive_v1_missing_future_locked_parameters": atomic_predictive_v1_parameter_lock_gate[
                "metrics"
            ]["missing_future_locked_parameter_count"],
            "atomic_predictive_v1_threshold_diagnostic_pass_count": atomic_predictive_v1_threshold_gate["metrics"][
                "diagnostic_pass_count"
            ],
            "atomic_predictive_v1_threshold_validation_ready_count": atomic_predictive_v1_threshold_gate["metrics"][
                "validation_ready_threshold_count"
            ],
            "atomic_predictive_v1_fixed_correction_accepted_operators": (
                atomic_predictive_v1_fixed_correction_operator_gate["metrics"]["accepted_operator_count"]
            ),
            "atomic_predictive_v1_fixed_correction_blocking_checks": (
                atomic_predictive_v1_fixed_correction_operator_gate["metrics"]["contract_blocking_count"]
            ),
            "atomic_predictive_v1_operator_candidate_resolutions": (
                atomic_predictive_v1_operator_candidate_resolution_gate["metrics"][
                    "candidate_resolution_count"
                ]
            ),
            "atomic_predictive_v1_operator_candidate_accepted_deltas": (
                atomic_predictive_v1_operator_candidate_resolution_gate["metrics"][
                    "accepted_delta_uet_or_ci_count"
                ]
            ),
            "atomic_predictive_v1_operator_candidate_rejected_existing": (
                atomic_predictive_v1_operator_candidate_resolution_gate["metrics"][
                    "rejected_existing_candidate_count"
                ]
            ),
            "atomic_predictive_v1_operator_candidate_missing_acceptable_paths": (
                atomic_predictive_v1_operator_candidate_resolution_gate["metrics"][
                    "missing_acceptable_operator_path_count"
                ]
            ),
            "atomic_predictive_v1_operator_build_spec_lanes": (
                atomic_predictive_v1_operator_build_spec_gate["metrics"]["implementation_lane_count"]
            ),
            "atomic_predictive_v1_operator_build_spec_ready_lanes": (
                atomic_predictive_v1_operator_build_spec_gate["metrics"]["implementation_ready_lane_count"]
            ),
            "atomic_predictive_v1_operator_build_spec_missing_lanes": (
                atomic_predictive_v1_operator_build_spec_gate["metrics"]["implementation_missing_lane_count"]
            ),
            "atomic_predictive_v1_operator_build_spec_blocking_checks": (
                atomic_predictive_v1_operator_build_spec_gate["metrics"]["spec_blocking_count"]
            ),
            "atomic_predictive_v1_report_validation_blockers": atomic_predictive_v1_diagnostic_report_gate["metrics"][
                "validation_blocker_count"
            ],
            "atomic_predictive_v1_report_level_holdout_predictions": atomic_predictive_v1_diagnostic_report_gate[
                "metrics"
            ]["level_holdout_prediction_count"],
            "atomic_predictive_v1_report_wavelength_holdout_predictions": atomic_predictive_v1_diagnostic_report_gate[
                "metrics"
            ]["wavelength_holdout_prediction_count"],
            "atomic_predictive_model_blueprint_steps": atomic_predictive_model_blueprint_gate["metrics"][
                "blueprint_step_count"
            ],
            "atomic_predictive_model_blueprint_blocked_steps": atomic_predictive_model_blueprint_gate["metrics"][
                "blocked_step_count"
            ],
            "atomic_predictive_model_blueprint_partial_steps": atomic_predictive_model_blueprint_gate["metrics"][
                "partial_step_count"
            ],
            "helium_external_holdout_candidate_sources": helium_external_holdout_acquisition_gate["metrics"][
                "candidate_source_count"
            ],
            "helium_external_holdout_overlap_candidates": helium_external_holdout_acquisition_gate["metrics"][
                "overlap_line_candidate_count"
            ],
            "helium_external_holdout_raw_files": helium_external_holdout_acquisition_gate["metrics"]["raw_file_count"],
            "helium_external_holdout_blocked_requirements": helium_external_holdout_acquisition_gate["metrics"][
                "blocked_requirement_count"
            ],
            "helium_external_holdout_crosscheck_rows": helium_external_holdout_residual_crosscheck_gate["metrics"][
                "crosscheck_row_count"
            ],
            "helium_external_holdout_crosscheck_max_abs_wavelength_delta_ppm": (
                helium_external_holdout_residual_crosscheck_gate["metrics"]["max_abs_wavelength_delta_ppm"]
            ),
            "helium_external_holdout_crosscheck_max_abs_upper_energy_delta_cm_inverse": (
                helium_external_holdout_residual_crosscheck_gate["metrics"][
                    "max_abs_upper_energy_delta_cm_inverse"
                ]
            ),
            "helium_external_holdout_source_version_reconciliation_rows": (
                helium_external_holdout_source_version_reconciliation_gate["metrics"][
                    "reconciliation_row_count"
                ]
            ),
            "helium_external_holdout_source_version_reconciliation_required": (
                helium_external_holdout_source_version_reconciliation_gate["metrics"][
                    "source_version_reconciliation_required_count"
                ]
            ),
            "helium_external_holdout_source_version_max_upper_energy_delta_cm_inverse": (
                helium_external_holdout_source_version_reconciliation_gate["metrics"][
                    "max_upper_energy_abs_delta_cm_inverse"
                ]
            ),
            "helium_external_holdout_lineage_independent_validation_allowed": (
                helium_external_holdout_lineage_decision_gate["metrics"]["independent_validation_allowed"]
            ),
            "helium_external_holdout_lineage_non_nist_source_required": (
                helium_external_holdout_lineage_decision_gate["metrics"]["non_nist_source_required"]
            ),
        },
        "results": results,
        "limitations": [
            "This validates the standard Rydberg relation against the topic-local hydrogen spectrum working copy.",
            "It does not derive the Rydberg relation from UET first principles.",
            "The Bohr/de Broglie/Rydberg bridge is now explicit, but it remains inherited standard physics unless a UET derivation artifact is added.",
            "Hydrogen level-energy rows support only rounded n-level benchmark language until direct ASD per-level precision is captured.",
            "Hydrogen-like ion rows support only a provisional selected He+/Li2+ reduced-mass benchmark; C VI is a higher-Z stress test until fine/QED policy and broader ion coverage are added.",
            "Precision spectroscopy rows are source-package targets; the 1S-2S nonrelativistic, leading Dirac, and empirical Lamb handoff baselines plus 21 cm source/Fermi gates are diagnostics only and do not validate hyperfine Hamiltonian closure, QED, helium, or many-electron atoms.",
            "Neutral helium rows have photon energies, term assignments, wavelength-medium normalization, line-component policy, ground-state baseline residuals, excited-state targets, zero-quantum-defect residual baselines, limited source-calibrated quantum-defect predictions, same-source-family holdout diagnostics, and selected holdout wavelength predictions computed but still do not validate electron correlation or many-electron spectra.",
            "The atomic predictive-model specification gate maps the required baseline-plus-correction contract, but the UET operator and fixed-parameter generative model remain missing.",
            "The atomic predictive-v1 parameter-lock gate now records allowed calibration parameters and forbidden holdout/external leakage fields; future CI/UET correction parameters remain missing.",
            "The atomic predictive-v1 threshold gate now records diagnostic residual thresholds for the selected lane, but zero thresholds are validation-ready.",
            "The atomic predictive-v1 fixed-correction operator gate defines the delta_uet_or_ci contract and records zero accepted fixed correction operators implemented.",
            "The atomic predictive-v1 operator candidate resolution gate classifies current standard, heuristic, empirical, and legacy candidates against the delta_uet_or_ci contract; current accepted correction operators remain zero.",
            "The atomic predictive-v1 operator build-spec gate defines implementation lanes, I/O, acceptance gates, forbidden shortcuts, and minimum first-build artifacts, but accepted implemented lanes remain zero.",
            "The atomic predictive-v1 diagnostic report records same-source-family level and wavelength predictions with diagnostic threshold checks, but validation remains blocked by the missing fixed CI/UET correction operator, non-NIST source package, and validation-ready thresholds.",
            "The helium external-holdout lineage decision gate classifies CHIANTI He I as cross-check-only because the captured metadata records NIST ASD lineage.",
            "The atomic predictive-model blueprint gate turns the build path into seven auditable steps; source lineage is now decided as cross-check-only, while parameter lock and thresholds remain partial until the missing generative model and validation-ready uncertainty policy exist.",
            "The first predictive implementation candidate gate selects the same-source-family helium quantum-defect holdout lane as the narrowest current diagnostic path, but external validation remains blocked.",
            "The helium external-holdout acquisition gate identifies CHIANTI He I as an external database cross-check candidate with raw files and hashes captured, but independent validation requires a non-NIST source package.",
            "The helium external-holdout residual cross-check gate computes CHIANTI-vs-current holdout deltas, but it remains cross-check-only because CHIANTI is NIST-lineage and validation-ready uncertainty thresholds are not resolved.",
            "The helium external-holdout source-version reconciliation gate keeps wavelength display-rounding consistency separate from upper-energy source-version deltas; current upper-energy rows remain diagnostic-only until source-version reconciliation is closed.",
        ],
    }
    artifact["atomic_formula_bridge_manifest"] = {
        "path": str(ATOMIC_FORMULA_BRIDGE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(atomic_formula_bridge_manifest, sort_keys=True).encode("utf-8")).hexdigest(),
        "dependency_steps": len(atomic_formula_bridge_manifest["dependency_chain"]),
        "cross_topic_dependencies": [row["topic"] for row in atomic_formula_bridge_manifest["cross_topic_dependencies"]],
        "claim_boundary": atomic_formula_bridge_manifest["claim_boundary"],
    }
    artifact["hydrogen_rydberg_line_uncertainty_gate"] = hydrogen_rydberg_line_uncertainty_gate
    artifact["hydrogen_level_energy_benchmark"] = hydrogen_level_energy_benchmark
    artifact["hydrogen_like_checkpoint"] = hydrogen_like_checkpoint
    artifact["hydrogen_like_domain_coverage_gate"] = hydrogen_like_domain_coverage_gate
    artifact["precision_spectroscopy_gate"] = precision_spectroscopy_gate
    artifact["precision_baseline_gate"] = precision_baseline_gate
    artifact["precision_dirac_baseline_gate"] = precision_dirac_baseline_gate
    artifact["lamb_shift_handoff_gate"] = lamb_shift_handoff_gate
    artifact["hyperfine_21cm_gate"] = hyperfine_21cm_gate
    artifact["hyperfine_fermi_baseline_gate"] = hyperfine_fermi_baseline_gate
    artifact["helium_many_electron_gate"] = helium_many_electron_gate
    artifact["helium_transition_assignment_gap_gate"] = helium_transition_assignment_gap_gate
    artifact["helium_medium_normalization_gate"] = helium_medium_normalization_gate
    artifact["helium_line_component_policy_gate"] = helium_line_component_policy_gate
    artifact["helium_ground_state_baseline_gate"] = helium_ground_state_baseline_gate
    artifact["helium_excited_state_target_gate"] = helium_excited_state_target_gate
    artifact["helium_excited_hydrogenic_residual_gate"] = helium_excited_hydrogenic_residual_gate
    artifact["helium_fixed_screening_baseline_gate"] = helium_fixed_screening_baseline_gate
    artifact["helium_quantum_defect_prediction_gate"] = helium_quantum_defect_prediction_gate
    artifact["helium_quantum_defect_holdout_gate"] = helium_quantum_defect_holdout_gate
    artifact["helium_quantum_defect_wavelength_holdout_gate"] = helium_quantum_defect_wavelength_holdout_gate
    artifact["legacy_multielectron_code_audit_gate"] = legacy_multielectron_code_audit_gate
    artifact["uet_atomic_operator_readiness_gate"] = uet_atomic_operator_readiness_gate
    artifact["atomic_prediction_baseline_comparator_gate"] = atomic_prediction_baseline_comparator_gate
    artifact["atomic_uncertainty_readiness_gate"] = atomic_uncertainty_readiness_gate
    artifact["atomic_residual_uncertainty_budget_gate"] = atomic_residual_uncertainty_budget_gate
    artifact["atomic_fixed_parameter_model_readiness_gate"] = atomic_fixed_parameter_model_readiness_gate
    artifact["atomic_predictive_model_closure_gate"] = atomic_predictive_model_closure_gate
    artifact["atomic_predictive_model_spec_gate"] = atomic_predictive_model_spec_gate
    artifact["atomic_first_predictive_implementation_candidate_gate"] = (
        atomic_first_predictive_implementation_candidate_gate
    )
    artifact["atomic_predictive_v1_parameter_lock_gate"] = atomic_predictive_v1_parameter_lock_gate
    artifact["atomic_predictive_v1_threshold_gate"] = atomic_predictive_v1_threshold_gate
    artifact["atomic_predictive_v1_fixed_correction_operator_gate"] = (
        atomic_predictive_v1_fixed_correction_operator_gate
    )
    artifact["atomic_predictive_v1_operator_candidate_resolution_gate"] = (
        atomic_predictive_v1_operator_candidate_resolution_gate
    )
    artifact["atomic_predictive_v1_operator_build_spec_gate"] = (
        atomic_predictive_v1_operator_build_spec_gate
    )
    artifact["atomic_predictive_v1_diagnostic_report_gate"] = atomic_predictive_v1_diagnostic_report_gate
    artifact["atomic_predictive_model_blueprint_gate"] = atomic_predictive_model_blueprint_gate
    artifact["helium_external_holdout_acquisition_gate"] = helium_external_holdout_acquisition_gate
    artifact["helium_external_holdout_residual_crosscheck_gate"] = (
        helium_external_holdout_residual_crosscheck_gate
    )
    artifact["helium_external_holdout_source_version_reconciliation_gate"] = (
        helium_external_holdout_source_version_reconciliation_gate
    )
    artifact["helium_external_holdout_lineage_decision_gate"] = helium_external_holdout_lineage_decision_gate
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
        "a rounded hydrogen n-level energy benchmark, a provisional selected He+/Li2+ reduced-mass hydrogenic benchmark plus C VI stress-test lane, "
        "a precision spectroscopy source gate, and a neutral helium source/assignment/medium-normalization/component-policy/ground-baseline/excited-target/hydrogenic-residual/quantum-defect-prediction/holdout/wavelength-holdout gate. It does not validate full atomic theory, "
        "fine structure, Lamb shift, hyperfine structure, QED corrections, broad hydrogen-like ion coverage, "
        "neutral helium residuals, or many-electron physics."
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
