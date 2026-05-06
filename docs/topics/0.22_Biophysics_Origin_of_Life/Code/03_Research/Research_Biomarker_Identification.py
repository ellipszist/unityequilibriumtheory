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
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "data" / "03_Research" / "source_evidence_readiness_matrix.json"
SUBCLAIM_GATE_PATH = TOPIC_DIR / "data" / "03_Research" / "subclaim_gate.json"
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


def _load_json_if_exists(path: Path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _field(status: str, value: str):
    return {"field": "", "status": status, "value": value}


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


def _write_json(path: Path, payload: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _build_source_evidence_intake_stub():
    chb_source = _load_json_if_exists(ROOT / "docs" / "data" / "external" / "biophysics" / "eeg" / "chb_mit" / "source_record.json")
    bonn_source = _load_json_if_exists(ROOT / "docs" / "data" / "external" / "biophysics" / "eeg" / "bonn" / "source_record.json")
    tcga_source = _load_json_if_exists(ROOT / "docs" / "data" / "external" / "biophysics" / "omics" / "tcga" / "source_record.json")
    source_lock = _load_json_if_exists(TOPIC_DIR / "data" / "03_Research" / "source_lock_manifest.json")
    chb_reference = _load_json_if_exists(TOPIC_DIR / "data" / "03_Research" / "chb_mit_reference.json")

    chb_record = chb_reference.get("sample_seizure_stats", {}).get("chb01", {})
    chb_windows = ", ".join(
        f"{entry.get('file')}:{entry.get('start_s')}-{entry.get('end_s')}s"
        for entry in chb_record.get("seizure_times", [])
    )
    chb_units = f"{chb_reference.get('sampling_rate_hz', 'unknown')} Hz; seizure windows in seconds"
    chb_preprocess = (
        "Source-labeled summary only via chb_mit_reference.json, chb01_summary.txt, and seizure_phase_data.json; "
        "raw EDF files and hashes are not archived in this repository."
    )

    bonn_preprocess = (
        "Topic-local Z.txt and S.txt samples are normalized at runtime by engine scripts; upstream package URL, "
        "license, and exact subset retrieval metadata remain open."
    )
    tcga_preprocess = (
        "Current TCGA-labeled scripts use mock or synthetic matrices only; no real cohort matrix is archived yet."
    )

    payload = {
        "schema_version": "1.0",
        "topic": "0.22_Biophysics_Origin_of_Life",
        "purpose": "Structured intake stub for upstream EEG, omics, protein, and prebiotic evidence before data rewrites or claim upgrades.",
        "instructions": [
            "Attach upstream DOI or URL, local archive path, exact record or cohort identity, and preprocessing note before changing working-copy biomedical data.",
            "Record unit basis, assay or signal format, and whether the data are raw, derived, mock, or synthetic.",
            "Do not treat this file as evidence by itself; it is an intake and tracking layer."
        ],
        "source_targets": [
            {
                "name": "CHB-MIT raw EDF and seizure-window package",
                "priority": "immediate",
                "status": "partial",
                "evidence_fields": [
                    {
                        "field": "doi_or_url",
                        "status": "complete" if chb_source.get("doi_url") or chb_source.get("dataset_url") else "pending",
                        "value": chb_source.get("doi_url") or chb_source.get("dataset_url", ""),
                    },
                    {
                        "field": "local_path",
                        "status": "complete",
                        "value": "docs/data/external/biophysics/eeg/chb_mit/source_record.json; docs/topics/0.22_Biophysics_Origin_of_Life/data/03_Research/chb_mit_reference.json; docs/topics/0.22_Biophysics_Origin_of_Life/data/03_Research/chb01_summary.txt",
                    },
                    {
                        "field": "patient_or_record_identifier",
                        "status": "complete" if chb_record else "pending",
                        "value": "patient chb01; 7 annotated seizure files in local summary" if chb_record else "",
                    },
                    {
                        "field": "window_or_segment_identifier",
                        "status": "complete" if chb_windows else "pending",
                        "value": chb_windows,
                    },
                    {
                        "field": "unit_basis_and_sampling_rate",
                        "status": "complete" if chb_reference.get("sampling_rate_hz") else "pending",
                        "value": chb_units if chb_reference.get("sampling_rate_hz") else "",
                    },
                    {
                        "field": "preprocessing_or_extraction_note",
                        "status": "complete",
                        "value": chb_preprocess,
                    },
                ],
            },
            {
                "name": "Bonn EEG source package and license",
                "priority": "high",
                "status": "partial",
                "evidence_fields": [
                    {
                        "field": "doi_or_url",
                        "status": "complete" if bonn_source.get("known_reference_url") else "pending",
                        "value": bonn_source.get("known_reference_url", ""),
                    },
                    {
                        "field": "local_path",
                        "status": "complete",
                        "value": "docs/data/external/biophysics/eeg/bonn/source_record.json; docs/topics/0.22_Biophysics_Origin_of_Life/data/Bonn_EEG/Z.txt; docs/topics/0.22_Biophysics_Origin_of_Life/data/Bonn_EEG/S.txt",
                    },
                    {
                        "field": "subset_or_sample_identifier",
                        "status": "complete",
                        "value": "topic-local Bonn-style samples Z.txt (healthy) and S.txt (seizure)",
                    },
                    {
                        "field": "license_or_usage_terms",
                        "status": "pending",
                        "value": "",
                    },
                    {
                        "field": "unit_basis_and_sampling_rate",
                        "status": "pending",
                        "value": bonn_source.get("unit_convention", {}).get("signal", ""),
                    },
                    {
                        "field": "preprocessing_or_extraction_note",
                        "status": "complete",
                        "value": bonn_preprocess,
                    },
                ],
            },
            {
                "name": "TCGA or real omics matrix package",
                "priority": "high",
                "status": "partial",
                "evidence_fields": [
                    {
                        "field": "doi_or_url",
                        "status": "complete" if tcga_source.get("portal_url") else "pending",
                        "value": tcga_source.get("portal_url", ""),
                    },
                    {
                        "field": "local_path",
                        "status": "complete",
                        "value": "docs/data/external/biophysics/omics/tcga/source_record.json",
                    },
                    {
                        "field": "cohort_or_assay_identifier",
                        "status": "pending",
                        "value": "",
                    },
                    {
                        "field": "expression_unit_basis",
                        "status": "pending",
                        "value": tcga_source.get("unit_convention", {}).get("expression", ""),
                    },
                    {
                        "field": "sample_and_feature_filter_note",
                        "status": "pending",
                        "value": "",
                    },
                    {
                        "field": "preprocessing_or_extraction_note",
                        "status": "complete",
                        "value": tcga_preprocess,
                    },
                ],
            },
            {
                "name": "HP protein-folding benchmark package",
                "priority": "medium",
                "status": "pending",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "sequence_or_benchmark_identifier", "status": "pending", "value": ""},
                    {"field": "known_optimum_or_baseline", "status": "pending", "value": ""},
                    {"field": "unit_basis", "status": "pending", "value": ""},
                    {"field": "preprocessing_or_extraction_note", "status": "pending", "value": ""},
                ],
            },
            {
                "name": "Prebiotic or protocell chemistry evidence package",
                "priority": "medium",
                "status": "pending",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "reaction_network_or_experiment_identifier", "status": "pending", "value": ""},
                    {"field": "yield_or_concentration_unit_basis", "status": "pending", "value": ""},
                    {"field": "environment_or_boundary_condition_note", "status": "pending", "value": ""},
                    {"field": "preprocessing_or_extraction_note", "status": "pending", "value": ""},
                ],
            },
        ],
        "claim_boundary": (
            "This intake stub is for source evidence capture only. Filling it does not by itself justify "
            "origin-of-life, seizure, cancer, biomarker, or protein-folding claim upgrades."
        ),
        "source_lock_dependencies": source_lock.get("external_source_records", []),
    }
    return _write_json(SOURCE_EVIDENCE_INTAKE_PATH, payload)


def _build_source_evidence_readiness_matrix(intake_stub: dict):
    rows = []
    ready = 0
    blocked = 0
    for target in intake_stub["source_targets"]:
        pending_fields = [field["field"] for field in target["evidence_fields"] if field.get("status") != "complete"]
        fields_total = len(target["evidence_fields"])
        fields_complete = fields_total - len(pending_fields)
        row_ready = not pending_fields
        if row_ready:
            ready += 1
        else:
            blocked += 1
        rows.append(
            {
                "name": target["name"],
                "priority": target["priority"],
                "fields_total": fields_total,
                "fields_complete": fields_complete,
                "fields_pending": len(pending_fields),
                "pending_fields": pending_fields,
                "target_status": target.get("status", "pending"),
                "ready_for_source_review": row_ready,
                "blocking_reason": "" if row_ready else "One or more required evidence fields are still pending.",
            }
        )
    payload = {
        "schema_version": "1.0",
        "topic": "0.22_Biophysics_Origin_of_Life",
        "purpose": "Readiness matrix for biomedical source evidence before data edits or claim upgrades.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready,
            "targets_blocked_by_pending_evidence": blocked,
        },
        "readiness_rows": rows,
        "claim_boundary": (
            "This matrix is a workflow gate only. A target marked ready still requires actual source review before "
            "working-copy or claim changes."
        ),
    }
    return _write_json(SOURCE_EVIDENCE_READINESS_PATH, payload)


def _build_subclaim_gate():
    payload = {
        "schema_version": "1.0",
        "topic": "0.22_Biophysics_Origin_of_Life",
        "purpose": "Claim gate for separate biomedical and origin-of-life lanes inside the topic.",
        "summary": {
            "lanes_total": 6,
            "accepted_now": 1,
            "blocked_for_strong_claims": 5,
        },
        "lanes": [
            {
                "lane": "Synthetic biomarker diagnostic",
                "status": "accepted_diagnostic_only",
                "allowed_usage_now": "Code-path check for seeded synthetic positive controls only.",
                "blocker_to_stronger_claim": "Need real omics matrix, baseline statistics, and cohort-aware validation."
            },
            {
                "lane": "Neural seizure or EEG claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Source-labeled EEG reference and sandbox only.",
                "blocker_to_stronger_claim": "Need raw windows, preprocessing, record IDs, held-out metrics, and classifier artifact."
            },
            {
                "lane": "Cancer or TCGA entropy claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Mock-matrix sandbox only.",
                "blocker_to_stronger_claim": "Need real source-backed omics matrix, cohort definition, and statistical baseline."
            },
            {
                "lane": "Origin-of-life or homeostasis claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Entropy proxy or simulation framing only.",
                "blocker_to_stronger_claim": "Need real chemistry or reaction-network evidence plus environment entropy ledger."
            },
            {
                "lane": "Protein-folding claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "HP-model sandbox only.",
                "blocker_to_stronger_claim": "Need known benchmark optimum, deterministic search, and source-backed sequence package."
            },
            {
                "lane": "Cross-topic thermodynamic bridge usage",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Conceptual dependency only.",
                "blocker_to_stronger_claim": "Must inherit 0.13 limitations until source-normalized bridge evidence is closed."
            },
        ],
        "claim_boundary": "This gate cannot raise claim strength above the current synthetic biomarker diagnostic evidence.",
    }
    return _write_json(SUBCLAIM_GATE_PATH, payload)


def _write_artifact(results, threshold, seed):
    inputs = _input_identity()
    source_evidence_intake_stub = _build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = _build_source_evidence_readiness_matrix(source_evidence_intake_stub)
    subclaim_gate = _build_subclaim_gate()
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
        "source_evidence_intake_stub": {
            "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(ROOT)).replace("\\", "/"),
            "sha256": _sha256(SOURCE_EVIDENCE_INTAKE_PATH),
            "source_targets": [item["name"] for item in source_evidence_intake_stub["source_targets"]],
            "claim_boundary": "This intake stub is for source evidence capture only. It does not authorize data or claim upgrades by itself.",
        },
        "source_evidence_readiness_matrix": {
            "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(ROOT)).replace("\\", "/"),
            "sha256": _sha256(SOURCE_EVIDENCE_READINESS_PATH),
            "summary": source_evidence_readiness_matrix["summary"],
            "claim_boundary": "This readiness matrix is a workflow gate only. It tracks whether source evidence is still pending.",
        },
        "subclaim_gate": {
            "path": str(SUBCLAIM_GATE_PATH.relative_to(ROOT)).replace("\\", "/"),
            "sha256": _sha256(SUBCLAIM_GATE_PATH),
            "summary": subclaim_gate["summary"],
            "claim_boundary": "This gate records separate biomedical claim ceilings only. It cannot upgrade the topic beyond the current synthetic diagnostic.",
        },
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
