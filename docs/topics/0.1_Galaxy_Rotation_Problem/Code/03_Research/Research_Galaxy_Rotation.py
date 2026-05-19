"""
Research: Galaxy Rotation Validation (V3.0)
===========================================
Internal repository comparison against working-copy galaxy rotation data.
"""

import importlib
import json
import platform
import sys
from pathlib import Path

import numpy as np

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs import ROOT_PATH
from docs.core.reproducibility import generate_artifact, hash_dataset, hash_file, save_artifact


root_path = ROOT_PATH
topic_path = root_path / "docs" / "topics" / "0.1_Galaxy_Rotation_Problem"
engine_path = topic_path / "Code" / "01_Engine"
if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

try:
    Engine_Galaxy_V3 = importlib.import_module("Engine_Galaxy_V3")
    UETGalaxyEngine = Engine_Galaxy_V3.UETGalaxyEngine
except ImportError as exc:
    print(f"ENGINE IMPORT ERROR: {exc}")
    sys.exit(1)


def load_data():
    """Load SPARC working-copy data from JSON."""
    data_path = topic_path / "Data" / "03_Research" / "sparc_data.json"
    if not data_path.exists():
        print(f"SPARC data not found at {data_path}")
        return []

    with data_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_entry(entry):
    """Map the current working-copy schema into engine and metric fields."""
    mass_disk = float(entry.get("M_disk_Msun", entry.get("mass_disk", 0.0)) or 0.0)
    radius_disk = float(entry.get("R_disk_kpc", entry.get("radius_disk", 0.0)) or 0.0)
    radius_obs = float(entry.get("R_kpc", 0.0) or 0.0)
    velocity_obs = float(entry.get("v_obs", 0.0) or 0.0)
    mass_bulge = float(entry.get("M_bulge_Msun", entry.get("mass_bulge", 0.0)) or 0.0)
    redshift = float(entry.get("redshift", 0.0) or 0.0)
    return {
        "name": entry.get("name", "Unknown"),
        "radius_obs_kpc": radius_obs,
        "velocity_obs_km_s": velocity_obs,
        "mass_disk_msun": mass_disk,
        "radius_disk_kpc": radius_disk,
        "mass_bulge_msun": mass_bulge,
        "redshift": redshift,
        "galaxy_type": entry.get("type", "Unknown"),
    }


def build_galaxy_model_gate(avg_error=None, pass_rate=None, processed_entries=0, skipped_entries=0):
    has_metric = avg_error is not None and pass_rate is not None and processed_entries > 0
    model_pass = bool(has_metric and avg_error < 15.0 and pass_rate > 0.0)
    return {
        "schema_version": "1.0",
        "topic": "0.1_Galaxy_Rotation_Problem",
        "purpose": "Separate verifier run-contract status from galaxy-model residual evidence.",
        "run_contract_gate": {
            "status": "PASS" if processed_entries > 0 else "FAIL",
            "processed_entries": processed_entries,
            "skipped_entries": skipped_entries,
            "claim_class": "C - internal summary-row benchmark execution",
        },
        "summary_row_model_gate": {
            "status": "PASS" if model_pass else "FAIL",
            "average_error_percent": avg_error,
            "pass_rate_percent": pass_rate,
            "thresholds": {
                "average_error_percent_max": 15.0,
                "pass_rate_percent_min": 1.0,
            },
            "claim_class": "model-residual blocker",
            "supports": "Only a summary-row internal residual benchmark over the repository working copy.",
            "does_not_support": "A full SPARC curve replication, dark-matter replacement, or galaxy-dynamics closure claim.",
        },
        "source_lock_gate": {
            "status": "OPEN",
            "required_inputs": [
                "upstream SPARC file identity",
                "row semantics and radius convention",
                "full radial curve arrays or declared one-point benchmark scope",
                "preprocessing script and source hash manifest",
            ],
        },
        "baseline_comparison_gate": {
            "status": "OPEN",
            "required_comparators": [
                "same-row MOND or dark-matter baseline artifact",
                "metric-equivalent competitor run",
                "documented threshold for comparative success",
            ],
        },
        "replacement_claim_gate": {
            "status": "BLOCKED",
            "blocked_claims": [
                "dark-matter replacement",
                "full SPARC replication",
                "galaxy-rotation theory closure",
                "out-of-sample prediction",
            ],
        },
        "claim_boundary": (
            "This gate lets the verifier run and residual model evidence diverge. "
            "A runnable artifact does not imply galaxy-model acceptance."
        ),
    }


def build_galaxy_claim_scope_gate(status, galaxy_model_gate, avg_error=None, pass_rate=None):
    model_status = galaxy_model_gate["summary_row_model_gate"]["status"]
    controller_status = "WARN" if status in {"PASS", "WARN"} else "FAIL"
    if model_status != "PASS":
        controller_status = "FAIL"
    return {
        "schema_version": "1.0",
        "topic": "0.1_Galaxy_Rotation_Problem",
        "controller_status": controller_status,
        "controller_reason": (
            "The verifier ran, but export remains blocked because the summary-row model gate fails or stronger source-lock/baseline gates are open."
            if controller_status == "FAIL"
            else "The summary-row benchmark passed, but export remains warning-gated because full-curve SPARC, source-lock, baseline, and out-of-sample gates are open."
        ),
        "claim_class": "C_summary_row_internal_benchmark_only",
        "allowed_claims_now": [
            {
                "claim": "The repository summary-row verifier ran over the checked-in galaxy working copy.",
                "status": galaxy_model_gate["run_contract_gate"]["status"],
                "artifact_role": "run-contract benchmark",
                "metrics": {
                    "average_error_percent": avg_error,
                    "pass_rate_percent": pass_rate,
                },
                "source_evidence_readiness": "working_copy_not_full_sparc_archive",
            },
            {
                "claim": "The current model may be discussed only as an internal summary-row residual experiment.",
                "status": "DIAGNOSTIC_ONLY" if model_status == "PASS" else "BLOCKED_BY_RESIDUAL",
                "artifact_role": "summary-row model gate",
                "formula_role": "heuristic bridge terms and scaling anchors still open",
                "source_evidence_readiness": "pending_row_semantics_and_curve_arrays",
            },
        ],
        "blocked_claims": [
            {
                "claim": "UET replaces dark matter for galaxy rotation curves.",
                "status": "BLOCKED",
                "blocking_reason": "Comparator baseline artifacts, lensing evidence, uncertainty handling, and out-of-sample tests are missing.",
                "next_evidence_required": [
                    "same-row MOND/dark-matter comparator artifact",
                    "uncertainty-aware metric definition",
                    "out-of-sample validation suite",
                ],
            },
            {
                "claim": "UET replicates the full upstream SPARC rotation-curve archive.",
                "status": "BLOCKED",
                "blocking_reason": "The current verifier uses one summary radius and velocity per galaxy, not full radial curve arrays.",
                "next_evidence_required": [
                    "upstream SPARC file identity",
                    "full radial curve arrays",
                    "preprocessing manifest with hashes",
                ],
            },
            {
                "claim": "UET closes galaxy-dynamics theory.",
                "status": "BLOCKED",
                "blocking_reason": "Heuristic bridge constants and radius semantics remain open.",
                "next_evidence_required": [
                    "derivation or sensitivity audit for bridge constants",
                    "source-locked radius convention",
                    "cross-galaxy and morphology-stratified baselines",
                ],
            },
        ],
        "blocked_export_phrases": [
            "dark matter replaced",
            "full SPARC replication",
            "galaxy rotation problem solved",
            "zero curve fitting",
            "out-of-sample prediction validated",
            "galaxy dynamics closed",
        ],
        "machine_readable_next_blockers": [
            "summary_row_model_gate_not_passed" if model_status != "PASS" else "full_curve_sparc_archive_missing",
            "source_lock_manifest_missing",
            "row_semantics_radius_convention_open",
            "competitor_baseline_artifact_missing",
            "heuristic_bridge_sensitivity_missing",
            "out_of_sample_validation_missing",
        ],
        "galaxy_model_gate_summary": {
            "run_contract_status": galaxy_model_gate["run_contract_gate"]["status"],
            "summary_row_model_status": model_status,
            "source_lock_status": galaxy_model_gate["source_lock_gate"]["status"],
            "baseline_comparison_status": galaxy_model_gate["baseline_comparison_gate"]["status"],
            "replacement_claim_status": galaxy_model_gate["replacement_claim_gate"]["status"],
        },
        "claim_boundary": (
            "A runnable artifact supports only an internal summary-row benchmark over the repository working copy. "
            "It does not support dark-matter replacement, full SPARC replication, zero-fit claims, "
            "out-of-sample prediction, or galaxy-dynamics closure."
        ),
    }


def run_validation():
    """Execute the full validation sweep."""
    print("Starting UET galaxy rotation validation...")
    data = load_data()
    if not data:
        return

    results = []
    errors = []
    skipped = []
    data_path = topic_path / "Data" / "03_Research" / "sparc_data.json"

    for entry in data:
        row = normalize_entry(entry)
        name = row["name"]
        try:
            if row["radius_obs_kpc"] <= 0 or row["velocity_obs_km_s"] <= 0:
                skipped.append({"name": name, "reason": "nonpositive radius or observed velocity"})
                continue
            if row["mass_disk_msun"] <= 0 or row["radius_disk_kpc"] <= 0:
                skipped.append({"name": name, "reason": "missing disk mass or disk radius"})
                continue

            gal_params = type(
                "GalaxyRow",
                (),
                {
                    "name": name,
                    "mass_disk": row["mass_disk_msun"],
                    "radius_disk": row["radius_disk_kpc"],
                    "mass_bulge": row["mass_bulge_msun"],
                    "redshift": row["redshift"],
                },
            )()
            engine = UETGalaxyEngine(gal_params)
            v_pred = float(engine.compute_velocity_at_radius(row["radius_obs_kpc"]))
            mape = abs((v_pred - row["velocity_obs_km_s"]) / row["velocity_obs_km_s"]) * 100
            if np.isnan(mape) or np.isinf(mape):
                skipped.append({"name": name, "reason": "invalid metric value"})
                continue

            errors.append(float(mape))
            results.append(
                {
                    "name": name,
                    "galaxy_type": row["galaxy_type"],
                    "radius_obs_kpc": row["radius_obs_kpc"],
                    "velocity_obs_km_s": row["velocity_obs_km_s"],
                    "velocity_pred_km_s": v_pred,
                    "absolute_percent_error": float(mape),
                    "within_15_percent": bool(mape < 15.0),
                }
            )
        except Exception as exc:
            skipped.append({"name": name, "reason": str(exc)})
            print(f"Error processing {name}: {exc}")

    if not errors:
        artifact = generate_artifact(
            topic="0.1_Galaxy_Rotation_Problem",
            dataset_hash=hash_dataset(data),
            results={
                "status": "FAIL",
                "processed_entries": 0,
                "skipped_entries": len(skipped),
            },
            config={"error_threshold_percent": 15.0},
            metrics={},
            thresholds={"max_average_error_percent": 15.0},
            notes="Verifier ran but the current working-copy schema or row coverage produced no valid comparisons.",
        )
        artifact["input_hashes"] = {"sparc_working_copy": hash_file(data_path)}
        artifact["skipped_entries"] = skipped[:20]
        artifact["claim_boundary"] = (
            "No scientific acceptance result is available when the verifier produces no valid comparisons."
        )
        artifact["galaxy_model_gate"] = build_galaxy_model_gate(
            processed_entries=0,
            skipped_entries=len(skipped),
        )
        artifact["galaxy_claim_scope_gate"] = build_galaxy_claim_scope_gate(
            "FAIL",
            artifact["galaxy_model_gate"],
        )
        artifact_path = topic_path / "Result" / "artifacts" / "galaxy_rotation_validation.json"
        save_artifact(artifact, artifact_path)
        print("No valid comparisons were produced.")
        print(f"Artifact saved to {artifact_path}")
        return

    avg_error = float(np.mean(errors))
    pass_rate = float(np.sum(np.array(errors) < 15.0) / len(errors) * 100)
    status = "PASS" if avg_error < 15.0 else "WARN"

    print("\n" + "=" * 40)
    print("VALIDATION COMPLETE")
    print(f"Mean Error Rate: {avg_error:.2f}%")
    print(f"Pass Rate (<15% Error): {pass_rate:.1f}%")
    print("=" * 40)

    artifact = generate_artifact(
        topic="0.1_Galaxy_Rotation_Problem",
        dataset_hash=hash_dataset(data),
        results={
            "status": status,
            "processed_entries": len(results),
            "skipped_entries": len(skipped),
            "average_error_percent": avg_error,
            "pass_rate_percent": pass_rate,
        },
        config={"error_threshold_percent": 15.0},
        metrics={
            "average_error_percent": avg_error,
            "pass_rate_percent": pass_rate,
        },
        thresholds={"max_average_error_percent": 15.0},
        notes="Internal benchmark artifact generated from repository summary-row working-copy galaxy data.",
    )
    artifact["input_hashes"] = {
        "sparc_working_copy": hash_file(data_path),
    }
    artifact["results_by_galaxy"] = results
    artifact["skipped_entries"] = skipped[:20]
    artifact["environment"] = {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
    }
    artifact["claim_boundary"] = (
        "This artifact measures a summary-row internal benchmark over the repository working copy; "
        "it is not a full upstream SPARC curve replication."
    )
    artifact["galaxy_model_gate"] = build_galaxy_model_gate(
        avg_error=avg_error,
        pass_rate=pass_rate,
        processed_entries=len(results),
        skipped_entries=len(skipped),
    )
    artifact["galaxy_claim_scope_gate"] = build_galaxy_claim_scope_gate(
        status,
        artifact["galaxy_model_gate"],
        avg_error=avg_error,
        pass_rate=pass_rate,
    )
    artifact_path = topic_path / "Result" / "artifacts" / "galaxy_rotation_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")


if __name__ == "__main__":
    run_validation()
