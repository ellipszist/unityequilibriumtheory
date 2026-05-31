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
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_20_atomic_physics_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"
ATOMIC_FORMULA_BRIDGE_PATH = TOPIC_DIR / "Data" / "03_Research" / "atomic_formula_bridge_manifest.json"
SPEED_OF_LIGHT_M_PER_S = 299_792_458.0
PLANCK_EV_S = 4.135667696e-15


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
                "status_hint": "source_package_ready_model_blocked",
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
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "artifact_paths",
                "many_electron_model_and_thresholds",
            ],
            "ready_for_source_review": True,
            "blocking_reason": "Neutral helium source rows are ready for source review, but no two-electron Hamiltonian/correlation model or residual artifact is primary-gated yet.",
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
            "accepted_now": 5,
            "blocked_for_strong_claims": 3,
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
                "allowed_usage_now": "May cite only as a prepared neutral-helium source package for future many-electron artifacts.",
                "blocker_to_stronger_claim": "Need a two-electron Hamiltonian/correlation model, line-component/blend policy, uncertainty policy, and residual thresholds before helium or many-electron claims.",
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
                "blocking_reason": "Neutral helium source rows, photon energies, term assignments, wavelength-medium normalization, and line-component/blend policy are now packaged, but a two-electron Hamiltonian/correlation residual artifact is still missing.",
                "next_evidence_required": [
                    "two-electron Hamiltonian/correlation model",
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
    hydrogen_level_energy_benchmark = build_hydrogen_level_energy_benchmark(hydrogen_level_rows)
    hydrogen_like_checkpoint = build_hydrogen_like_checkpoint(codata, ion_data)
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
        ],
        "formula_ids": [
            "AT20-PHOTON-TRANSITION",
            "AT20-DEBROGLIE-STANDING-WAVE",
            "AT20-BOHR-HYDROGEN-ENERGY",
            "AT20-HYDROGEN-LEVEL-ENERGY-BENCHMARK",
            "AT20-RYDBERG-WAVELENGTH",
            "AT20-RH-CODATA-CHECKPOINT",
            "AT20-SPECTRUM-RESIDUAL",
            "AT20-HYDROGENIC-Z2-CHECKPOINT",
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
            "hydrogen_level_count": hydrogen_level_energy_benchmark["metrics"]["level_count"],
            "hydrogen_level_avg_error_ppm": hydrogen_level_energy_benchmark["metrics"]["average_energy_error_ppm"],
            "hydrogen_level_max_error_ppm": hydrogen_level_energy_benchmark["metrics"]["max_energy_error_ppm"],
            "hydrogen_like_checkpoint_predictions": len(hydrogen_like_checkpoint["predictions"]),
            "hydrogen_like_avg_error_ppm": hydrogen_like_checkpoint["metrics"]["average_wavelength_error_ppm"],
            "hydrogen_like_max_error_ppm": hydrogen_like_checkpoint["metrics"]["max_wavelength_error_ppm"],
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
        },
        "results": results,
        "limitations": [
            "This validates the standard Rydberg relation against the topic-local hydrogen spectrum working copy.",
            "It does not derive the Rydberg relation from UET first principles.",
            "The Bohr/de Broglie/Rydberg bridge is now explicit, but it remains inherited standard physics unless a UET derivation artifact is added.",
            "Hydrogen level-energy rows support only rounded n-level benchmark language until direct ASD per-level precision is captured.",
            "Hydrogen-like ion rows support only a provisional selected He+/Li2+ reduced-mass benchmark; C VI is a higher-Z stress test until fine/QED policy and broader ion coverage are added.",
            "Precision spectroscopy rows are source-package targets; the 1S-2S nonrelativistic, leading Dirac, and empirical Lamb handoff baselines plus 21 cm source/Fermi gates are diagnostics only and do not validate hyperfine Hamiltonian closure, QED, helium, or many-electron atoms.",
            "Neutral helium rows have photon energies, term assignments, wavelength-medium normalization, and line-component policy computed but still do not validate electron correlation or many-electron spectra.",
        ],
    }
    artifact["atomic_formula_bridge_manifest"] = {
        "path": str(ATOMIC_FORMULA_BRIDGE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(atomic_formula_bridge_manifest, sort_keys=True).encode("utf-8")).hexdigest(),
        "dependency_steps": len(atomic_formula_bridge_manifest["dependency_chain"]),
        "cross_topic_dependencies": [row["topic"] for row in atomic_formula_bridge_manifest["cross_topic_dependencies"]],
        "claim_boundary": atomic_formula_bridge_manifest["claim_boundary"],
    }
    artifact["hydrogen_level_energy_benchmark"] = hydrogen_level_energy_benchmark
    artifact["hydrogen_like_checkpoint"] = hydrogen_like_checkpoint
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
        "a precision spectroscopy source gate, and a neutral helium source/assignment/medium-normalization/component-policy gate. It does not validate full atomic theory, "
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
