"""
UET Yang-Mills Mass Gap Validation
==================================
Internal benchmark against a selected lattice-QCD working copy.
"""

import importlib.util
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
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
if not ROOT:
    print("CRITICAL: UET docs root not found!")
    sys.exit(1)

from docs.core.reproducibility import generate_artifact, hash_dataset, hash_file, save_artifact


script_path = Path(__file__).resolve()
project_root = script_path.parents[5]
topic_dir = script_path.parents[2]
source_lock_path = topic_dir / "data" / "03_Research" / "source_lock_manifest.json"
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from docs.core.uet_glass_box import UETMetricLogger, UETPathManager

    engine_path = script_path.parents[1] / "01_Engine" / "Engine_Mass_Gap.py"
    spec = importlib.util.spec_from_file_location("Engine_Mass_Gap", engine_path)
    eng_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(eng_mod)
    UETMassGapEngine = eng_mod.UETMassGapEngine
except Exception as exc:
    print(f"CRITICAL SETUP ERROR: {exc}")
    sys.exit(1)


def load_lattice_data():
    """Load lattice working-copy data from JSON."""
    data_path = script_path.parents[2] / "data" / "03_Research" / "lattice_qcd_spectrum.json"
    if not data_path.exists():
        raise FileNotFoundError(f"Missing lattice data: {data_path}")

    with data_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_source_lock() -> dict:
    if not source_lock_path.exists():
        return {"external_source_records": [], "derived_inputs": [], "status": "MISSING"}
    return json.loads(source_lock_path.read_text(encoding="utf-8"))


def path_hash_record(path_string: str) -> dict:
    path = project_root / path_string
    return {
        "path": path_string,
        "sha256": hash_file(path) if path.exists() and path.is_file() else None,
        "status": "present" if path.exists() else "missing",
    }


def build_yang_mills_claim_scope_gate(
    status: str,
    error_percent: float,
    uncertainty_percent: float,
    residual_mev: float,
    source_lock: dict,
) -> dict:
    controller_status = "WARN" if status == "PASS" else status
    return {
        "schema_version": "1.0",
        "topic": "0.21_Yang_Mills_Mass_Gap",
        "controller_status": controller_status,
        "controller_reason": (
            "The selected scalar-glueball benchmark is inside the reference-row uncertainty, but export remains "
            "warning-gated because the artifact uses a fitted alpha sweep and lacks a multi-state spectrum, "
            "continuum-limit, and mathematical proof package."
            if status == "PASS"
            else "The verifier ran but the selected scalar-glueball residual exceeded the reference-row uncertainty."
        ),
        "claim_class": "C_calibration_benchmark_only",
        "allowed_claims_now": [
            {
                "claim": "The fitted alpha-sweep benchmark can match the selected scalar glueball reference row within the declared status rule.",
                "status": status,
                "artifact_role": "calibration-aware scalar benchmark",
                "metrics": {
                    "relative_error_percent": error_percent,
                    "reference_uncertainty_percent": uncertainty_percent,
                    "residual_mev": residual_mev,
                },
                "source_evidence_readiness": "source_backed_topic_working_copy",
            },
            {
                "claim": "The current engine can be discussed as an exploratory curvature-gap model.",
                "status": "DIAGNOSTIC_ONLY",
                "artifact_role": "mechanism diagnostic branch",
                "formula_role": "fitted curvature parameter sweep, not fixed theory constant",
                "source_evidence_readiness": "inherits_source_lock_manifest",
            },
        ],
        "blocked_claims": [
            {
                "claim": "UET proves the Clay Yang-Mills existence and mass-gap problem.",
                "status": "BLOCKED",
                "blocking_reason": "The artifact is a numeric calibration benchmark, not a constructive mathematical proof.",
                "next_evidence_required": [
                    "formal theorem statement",
                    "assumption registry",
                    "constructive proof artifact",
                    "independent mathematical review status",
                ],
            },
            {
                "claim": "UET validates the full glueball spectrum or confinement physics.",
                "status": "BLOCKED",
                "blocking_reason": "Only one selected scalar glueball row is primary-gated; tensor, pseudoscalar, and multi-state residuals are not gated.",
                "next_evidence_required": [
                    "multi-state glueball spectrum artifact",
                    "held-out lattice rows",
                    "continuum-limit and lattice-spacing checks",
                ],
            },
            {
                "claim": "The fitted alpha is a fixed UET theory constant.",
                "status": "BLOCKED",
                "blocking_reason": "The current verifier sweeps alpha as a best-fit calibration parameter.",
                "next_evidence_required": [
                    "fixed-parameter prediction protocol",
                    "pre-registered threshold policy",
                    "out-of-sample validation artifact",
                ],
            },
        ],
        "blocked_export_phrases": [
            "Clay Yang-Mills problem solved",
            "mass gap proven",
            "confinement proven",
            "full glueball spectrum validated",
            "alpha is fixed by theory",
            "Millennium problem supported",
        ],
        "source_lock_summary": {
            "status": source_lock.get("status", "present"),
            "external_source_records": len(source_lock.get("external_source_records", [])),
            "derived_inputs": len(source_lock.get("derived_inputs", [])),
        },
        "machine_readable_next_blockers": [
            "constructive_proof_package_missing",
            "multi_state_glueball_artifact_missing",
            "continuum_limit_check_missing",
            "fixed_parameter_prediction_missing",
            "independent_math_review_missing",
        ],
        "claim_boundary": (
            "A PASS/WARN artifact supports only a calibration-aware selected scalar glueball benchmark. "
            "It does not prove the Clay Yang-Mills mass-gap problem, validate confinement, validate the full "
            "glueball spectrum, or establish alpha as a fixed theory constant."
        ),
    }


def run_validation():
    print("=" * 60)
    print("UET YANG-MILLS: MASS GAP VALIDATION")
    print("=" * 60)

    json_data = load_lattice_data()
    source_lock = load_source_lock()
    lattice_states = json_data["states"]
    scalar_glueball = next(state for state in lattice_states if "Scalar" in state["state"])
    mass_mev = float(scalar_glueball["mass_mev"])
    uncertainty_percent = (
        float(scalar_glueball["uncertainty"]) / float(scalar_glueball["mass_r0_units"]) * 100
    )

    engine = UETMassGapEngine()
    alphas = np.linspace(-0.5, -0.01, 50)
    scale_gev = 3.0
    uet_masses = []

    for alpha in alphas:
        gap_dim = engine.estimate_mass_gap(alpha=alpha, gamma=0.5)
        uet_masses.append(gap_dim * scale_gev * 1000)

    uet_masses = np.asarray(uet_masses)
    diffs = np.abs(uet_masses - mass_mev)
    best_idx = int(np.argmin(diffs))
    best_alpha = float(alphas[best_idx])
    best_prediction = float(uet_masses[best_idx])
    error = abs(best_prediction - mass_mev) / mass_mev * 100
    uncertainty_mev = float(scalar_glueball["uncertainty"]) * float(json_data["metadata"]["hc_mev_fm"]) / float(json_data["metadata"]["r0_physical_value_fm"])
    residual_mev = best_prediction - mass_mev
    status = "PASS" if error <= uncertainty_percent else "WARN"

    print(f"Lattice scalar mass: {mass_mev:.2f} MeV")
    print(f"Best-fit alpha: {best_alpha:.3f}")
    print(f"Predicted mass: {best_prediction:.2f} MeV")
    print(f"Relative error: {error:.2f}%")
    yang_mills_claim_scope_gate = build_yang_mills_claim_scope_gate(
        status,
        float(error),
        float(uncertainty_percent),
        float(residual_mev),
        source_lock,
    )

    result_dir = UETPathManager.get_result_dir("0.21", "Mass_Gap_Validation", category="showcase")
    UETMetricLogger("MassGap_Val", topic_id="0.21", category="showcase")

    plt.figure(figsize=(10, 6))
    plt.plot(
        alphas,
        uet_masses,
        "b-",
        linewidth=2,
        label=r"UET Mass Gap Prediction ($\Delta \sim \sqrt{|\alpha|}$)",
    )
    plt.axhline(
        y=mass_mev,
        color="r",
        linestyle="--",
        label=f"Lattice QCD reference: {mass_mev:.0f} MeV",
    )
    plt.fill_between(
        alphas,
        mass_mev * (1 - uncertainty_percent / 100),
        mass_mev * (1 + uncertainty_percent / 100),
        color="r",
        alpha=0.1,
        label="Lattice uncertainty",
    )
    plt.plot(best_alpha, best_prediction, "go", markersize=10, label=f"Best fit alpha={best_alpha:.2f}")
    plt.title("Yang-Mills Mass Gap: UET vs Selected Lattice Reference")
    plt.xlabel(r"UET Field Curvature Parameter ($\alpha$)")
    plt.ylabel("Mass Gap (MeV)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.text(alphas[10], 500, "Confinement region", fontsize=10, color="blue")

    save_path = result_dir / "Mass_Gap_Validation_Plot.png"
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Plot saved to {save_path}")

    artifact = generate_artifact(
        topic="0.21_Yang_Mills_Mass_Gap",
        dataset_hash=hash_dataset({
            "lattice_data": json_data,
            "source_lock_sha256": hash_file(source_lock_path) if source_lock_path.exists() else None,
        }),
        results={
            "status": status,
            "best_alpha": best_alpha,
            "best_prediction_mev": best_prediction,
            "reference_mass_mev": mass_mev,
            "residual_mev": residual_mev,
            "reference_uncertainty_mev": uncertainty_mev,
            "reference_uncertainty_percent": uncertainty_percent,
            "calibration_mode": "alpha sweep best-fit",
        },
        config={
            "scale_gev": float(scale_gev),
            "alpha_sweep_points": int(len(alphas)),
            "alpha_min": float(alphas[0]),
            "alpha_max": float(alphas[-1]),
            "gamma": 0.5,
            "source_lock_manifest": str(source_lock_path.relative_to(project_root)),
        },
        metrics={"relative_error_percent": float(error)},
        thresholds={
            "reference_uncertainty_percent": float(uncertainty_percent),
            "status_rule": "PASS only if residual is within selected lattice-row uncertainty; otherwise WARN unless the run fails.",
        },
        notes="Calibration-aware internal benchmark artifact against selected lattice data; WARN is expected when best-fit residual exceeds the selected lattice-row uncertainty.",
    )
    artifact["metrics"]["blocked_claim_exports"] = len(
        yang_mills_claim_scope_gate["blocked_export_phrases"]
    )
    artifact["input_hashes"] = {
        "source_lock_manifest": hash_file(source_lock_path) if source_lock_path.exists() else None,
        "lattice_working_copy": hash_file(topic_dir / "data" / "03_Research" / "lattice_qcd_spectrum.json"),
        "benchmark_script": hash_file(script_path),
        "engine": hash_file(script_path.parents[1] / "01_Engine" / "Engine_Mass_Gap.py"),
        "source_records": [
            path_hash_record(path) for path in source_lock.get("external_source_records", [])
        ],
    }
    artifact["claim_boundary"] = (
        "WARN/PASS status applies only to a calibration-aware scalar glueball benchmark. "
        "It is not a proof of the Clay Yang-Mills mass-gap problem."
    )
    artifact["yang_mills_claim_scope_gate"] = yang_mills_claim_scope_gate
    artifact_path = topic_dir / "Result" / "artifacts" / "mass_gap_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")

    return status in {"PASS", "WARN"}


if __name__ == "__main__":
    run_validation()
