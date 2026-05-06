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
    artifact_path = topic_path / "Result" / "artifacts" / "galaxy_rotation_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")


if __name__ == "__main__":
    run_validation()
