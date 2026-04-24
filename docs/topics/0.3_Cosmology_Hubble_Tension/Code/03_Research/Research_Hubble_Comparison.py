"""
UET Cosmology and Hubble Tension Comparison
===========================================
Internal comparison using published H0 reference values and the repository cosmology engine.
"""

import sys
from pathlib import Path

from docs import ROOT_PATH
from docs.core.reproducibility import generate_artifact, hash_dataset, save_artifact


root_path = ROOT_PATH
topic_path = root_path / "docs" / "topics" / "0.3_Cosmology_Hubble_Tension"
engine_path = topic_path / "Code" / "01_Engine"
if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

try:
    from Engine_Cosmology import UETCosmologyEngine
except ImportError as exc:
    print(f"CRITICAL SETUP ERROR: {exc}")
    sys.exit(1)


H0_PLANCK = 67.4
H0_SHOES = 73.04
TENSION_SIGMA = 4.8


def run_test():
    """Run the repository Hubble-comparison benchmark."""
    print("=" * 70)
    print("UET COSMOLOGY - HUBBLE TENSION TEST")
    print("Data: Planck 2018 + SH0ES 2022")
    print("=" * 70)

    engine = UETCosmologyEngine()
    res = engine.solve_hubble_tension(H0_PLANCK, H0_SHOES)
    h0_early_uet = float(res["H0_early_uet"])
    h0_late_uet = float(res["H0_late_uet"])
    delta_h0_uet = float(res["Delta_H0"])
    beta = float(res["beta"])
    beta_source = str(res.get("beta_source", "unspecified"))
    solver_beta = float(res.get("solver_beta", beta))

    observed_delta = H0_SHOES - H0_PLANCK
    error = abs(delta_h0_uet - observed_delta) / observed_delta * 100
    passed = error < 20

    print(f"Planck 2018 (CMB): {H0_PLANCK} km/s/Mpc")
    print(f"SH0ES 2022 (local): {H0_SHOES} km/s/Mpc")
    print(f"Observed Delta H0: {observed_delta:.2f} km/s/Mpc")
    print(f"UET early value: {h0_early_uet:.2f} km/s/Mpc")
    print(f"UET late value: {h0_late_uet:.2f} km/s/Mpc")
    print(f"UET Delta H0: {delta_h0_uet:.2f} km/s/Mpc")
    print(f"Hubble frame beta: {beta:.4f} ({beta_source})")
    print(f"Generic solver beta: {solver_beta:.4e}")
    print(f"Relative error: {error:.1f}%")
    print(f"Status: {'PASS' if passed else 'FAIL'}")

    try:
        import matplotlib.pyplot as plt

        fig_dir = topic_path / "Result" / "artifacts"
        fig_dir.mkdir(parents=True, exist_ok=True)
        output_path = fig_dir / "hubble_tension_resolution.png"

        labels = ["Planck 2018", "SH0ES 2022", "UET late"]
        values = [H0_PLANCK, H0_SHOES, h0_late_uet]

        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=["#1f77b4", "#d62728", "#2ca02c"])
        plt.ylabel("Hubble Constant (km/s/Mpc)")
        plt.title("Repository Hubble Comparison")
        plt.ylim(60, 80)
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Plot saved to {output_path}")
    except Exception as exc:
        print(f"Visualization skipped: {exc}")

    artifact = generate_artifact(
        topic="0.3_Cosmology_Hubble_Tension",
        dataset_hash=hash_dataset(
            {
                "H0_PLANCK": H0_PLANCK,
                "H0_SHOES": H0_SHOES,
                "TENSION_SIGMA": TENSION_SIGMA,
            }
        ),
        results={
            "H0_early_uet": h0_early_uet,
            "H0_late_uet": h0_late_uet,
            "delta_h0_uet": delta_h0_uet,
            "hubble_frame_beta": beta,
            "hubble_frame_beta_source": beta_source,
            "generic_solver_beta": solver_beta,
            "status": "PASS" if passed else "FAIL",
        },
        config={
            "relative_error_threshold_percent": 20.0,
            "no_fitting_rule": "hubble_frame_beta is sqrt(ALPHA_EM), not optimized against H0 data",
        },
        metrics={"relative_error_percent": float(error)},
        thresholds={"max_relative_error_percent": 20.0},
        notes="Internal comparison artifact using published H0 reference values.",
    )
    artifact_path = topic_path / "Result" / "artifacts" / "hubble_comparison_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")

    return passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
