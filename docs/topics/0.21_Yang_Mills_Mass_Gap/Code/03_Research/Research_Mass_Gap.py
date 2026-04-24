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

from docs.core.reproducibility import generate_artifact, hash_dataset, save_artifact


script_path = Path(__file__).resolve()
project_root = script_path.parents[5]
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
    data_path = script_path.parents[2] / "Data" / "03_Research" / "lattice_qcd_spectrum.json"
    if not data_path.exists():
        raise FileNotFoundError(f"Missing lattice data: {data_path}")

    with data_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_validation():
    print("=" * 60)
    print("UET YANG-MILLS: MASS GAP VALIDATION")
    print("=" * 60)

    json_data = load_lattice_data()
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

    print(f"Lattice scalar mass: {mass_mev:.2f} MeV")
    print(f"Best-fit alpha: {best_alpha:.3f}")
    print(f"Predicted mass: {best_prediction:.2f} MeV")
    print(f"Relative error: {error:.2f}%")

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
        dataset_hash=hash_dataset(json_data),
        results={
            "best_alpha": best_alpha,
            "best_prediction_mev": best_prediction,
            "reference_mass_mev": mass_mev,
        },
        config={"scale_gev": float(scale_gev), "alpha_sweep_points": int(len(alphas))},
        metrics={"relative_error_percent": float(error)},
        thresholds={},
        notes="Calibration-aware internal benchmark artifact against selected lattice data.",
    )
    artifact_path = script_path.parents[2] / "Result" / "artifacts" / "mass_gap_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")

    return True


if __name__ == "__main__":
    run_validation()
