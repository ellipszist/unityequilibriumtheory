"""
UET Biophysics: Synthetic Biomarker Diagnostic
==============================================
Topic: 0.22 Biophysics & Origin of Life

This verifier exercises the biomarker-stability calculation path with seeded
synthetic positive controls. It is not a clinical or TCGA validation.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


TOPIC_DIR = Path(__file__).resolve().parents[2]
ROOT = TOPIC_DIR.parents[2]
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_22_biophysics_origin_of_life_verification.json"
DATA_INPUTS = [
    TOPIC_DIR / "data" / "03_Research" / "source_lock_manifest.json",
    TOPIC_DIR / "data" / "03_Research" / "chb_mit_reference.json",
    TOPIC_DIR / "data" / "03_Research" / "chb01_summary.txt",
    TOPIC_DIR / "data" / "03_Research" / "seizure_phase_data.json",
    TOPIC_DIR / "data" / "Bonn_EEG" / "Z.txt",
    TOPIC_DIR / "data" / "Bonn_EEG" / "S.txt",
    ROOT / "docs" / "data" / "external" / "biophysics" / "eeg" / "chb_mit" / "source_record.json",
    ROOT / "docs" / "data" / "external" / "biophysics" / "eeg" / "bonn" / "source_record.json",
    ROOT / "docs" / "data" / "external" / "biophysics" / "omics" / "tcga" / "source_record.json",
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


def _write_artifact(results, threshold, seed):
    inputs = _input_identity()
    missing_inputs = [item["path"] for item in inputs if item.get("missing")]
    status = "WARN" if results and not missing_inputs else "FAIL"

    artifact = {
        "schema_version": "1.1",
        "topic": "0.22_Biophysics_Origin_of_Life",
        "command": ".venv\\Scripts\\python.exe docs\\topics\\0.22_Biophysics_Origin_of_Life\\Code\\03_Research\\Research_Biomarker_Identification.py",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "claim_class": "D",
        "inputs": inputs,
        "metrics": {
            "synthetic_gene_count": 50,
            "synthetic_sample_count": 100,
            "stability_threshold": threshold,
            "random_seed": seed,
            "identified_biomarkers": results,
        },
        "thresholds": {
            "stability_below_threshold_flags_candidate": threshold,
            "expected_synthetic_positive_controls": ["GENE_007", "GENE_023"],
        },
        "warnings": [
            "Biomarker data in this verifier is synthetic; it is not a clinical or TCGA validation.",
            "EEG/TCGA source records and local EEG summaries are hashed for provenance but are not used by this biomarker verifier.",
            "Origin-of-life, neural, cancer, and protein-folding subclaims require separate verifier gates.",
        ],
        "interpretation": (
            "This artifact validates the synthetic biomarker diagnostic path only. It supports code-path "
            "hardening and formula auditing, not biomedical efficacy or origin-of-life proof."
        ),
    }
    if missing_inputs:
        artifact["warnings"].append(f"Missing declared provenance inputs: {missing_inputs}")

    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"\n[Artifact] Verification artifact written: {ARTIFACT_PATH}")
    print(f"[Artifact] Status: {status}")
    return artifact


def identify_biomarkers():
    seed = 22022
    np.random.seed(seed)

    print("UET BIOMARKER IDENTIFICATION: SYNTHETIC POSITIVE-CONTROL CHECK")
    print("=" * 60)

    gene_names = [f"GENE_{i:03d}" for i in range(50)]
    samples = 100
    data = np.random.normal(5, 0.5, (50, samples))

    data[7] = np.random.normal(5, 2.5, samples)
    data[23] = np.random.normal(5, 3.0, samples)

    print(f"Analyzing {len(gene_names)} synthetic candidate genes across {samples} samples...")

    results = []
    threshold = 0.5
    for i, gene in enumerate(gene_names):
        variance = float(np.var(data[i]))
        stability = 1.0 / (1.0 + variance)
        if stability < threshold:
            results.append(
                {
                    "gene": gene,
                    "stability": float(stability),
                    "variance": variance,
                    "status": "synthetic_positive_control_candidate",
                }
            )

    print("\n[Analysis Report]")
    if results:
        print(pd.DataFrame(results).to_string(index=False))
    else:
        print("No synthetic positive controls detected within current parameters.")

    print("\n[Interpretation]")
    print("Low stability flags high-variance synthetic controls; this is a diagnostic code-path check.")
    print("It must not be read as clinical biomarker validation.")

    artifact = _write_artifact(results, threshold, seed)
    return artifact["status"] != "FAIL"


if __name__ == "__main__":
    raise SystemExit(0 if identify_biomarkers() else 1)
