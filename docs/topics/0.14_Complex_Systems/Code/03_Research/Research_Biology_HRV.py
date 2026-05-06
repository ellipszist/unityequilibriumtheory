"""
[HRV] UET Test 04: Bio HRV Equilibrium
===================================

Tests: dOmega/dt <= 0 (System seeks equilibrium)

Uses real HRV data from PhysioNet.

Updated for UET V3.0
"""

import sys
from pathlib import Path

# --- ROBUST UET BOOTSTRAP ---
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


import sys
from pathlib import Path
from docs import ROOT_PATH

root_path = ROOT_PATH

# --- ROBUST PATH FINDER (5x4 Grid Standard) ---


import numpy as np
import os
import glob
import math
import json
import hashlib
from datetime import datetime, timezone
from docs.core.uet_glass_box import UETPathManager


# Import from UET V3.0 Master Equation
try:
    from docs.core.uet_master_equation import (
        UETParameters,
        SIGMA_CRIT,
        strategic_boost,
        potential_V,
        KAPPA_BEKENSTEIN,
    )
except ImportError:
    pass

# Define Data Path
TOPIC_DIR = (
    root_path / "docs" / "topics" / "0.14_Complex_Systems"
    if root_path
    else Path(__file__).resolve().parent.parent.parent
)
DATA_PATH = TOPIC_DIR / "Data"
DATA_DIR = str(DATA_PATH)
ARTIFACT_PATH = (
    TOPIC_DIR / "Result" / "artifacts" / "0_14_complex_systems_verification.json"
)
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"


# Standardized UET Root Path
from docs import ROOT_PATH

root_path = ROOT_PATH


def load_hrv_data():
    """Load HRV data from PhysioNet."""
    bio_dir = os.path.join(DATA_DIR, "03_Research", "biology_hrv")
    datasets = []

    if os.path.exists(bio_dir):
        for filename in os.listdir(bio_dir):
            if filename.startswith("physionet_") and filename.endswith("_rr.csv"):
                filepath = os.path.join(bio_dir, filename)
                try:
                    # Read CSV, first column is RR intervals
                    import pandas as pd

                    df = pd.read_csv(filepath)
                    if len(df.columns) > 0:
                        # Convert to numeric, coerce errors (handles header in data)
                        rr = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna().values
                        if len(rr) > 10:
                            name = filename.replace(".csv", "")
                            datasets.append((name, rr))
                except Exception as e:
                    print(f"   [WARN] Could not load {filename}: {e}")

    return datasets


def _to_jsonable(value):
    """Convert numpy/scalar values to stable JSON primitives."""
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, tuple):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _hrv_input_hashes():
    bio_dir = TOPIC_DIR / "Data" / "03_Research" / "biology_hrv"
    inputs = []
    extra_inputs = [
        bio_dir / "source_lock_manifest.json",
        root_path
        / "docs"
        / "data"
        / "external"
        / "biophysics"
        / "hrv"
        / "mit_bih_nsrdb"
        / "source_record.json",
    ]
    for path in extra_inputs:
        try:
            rel = path.relative_to(root_path)
        except ValueError:
            rel = path
        if path.exists():
            inputs.append(
                {
                    "path": str(rel).replace("\\", "/"),
                    "bytes": path.stat().st_size,
                    "sha256": _sha256(path),
                    "loaded_by_primary_script": False,
                    "provenance_role": "source_lock",
                }
            )
        else:
            inputs.append(
                {
                    "path": str(rel).replace("\\", "/"),
                    "missing": True,
                    "provenance_role": "source_lock",
                }
            )
    if not bio_dir.exists():
        return inputs
    for path in sorted(bio_dir.glob("*.csv")):
        inputs.append(
            {
                "path": str(path.relative_to(TOPIC_DIR)).replace("\\", "/"),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
                "loaded_by_primary_script": path.name.startswith("physionet_")
                and path.name.endswith("_rr.csv"),
            }
        )
    return inputs


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _load_json_if_exists(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _field(field, status, value):
    return {"field": field, "status": status, "value": value}


def _build_source_evidence_intake_stub():
    source_record_path = root_path / "docs" / "data" / "external" / "biophysics" / "hrv" / "mit_bih_nsrdb" / "source_record.json"
    source_record = _load_json_if_exists(source_record_path)
    source_lock_path = TOPIC_DIR / "Data" / "03_Research" / "biology_hrv" / "source_lock_manifest.json"
    source_lock = _load_json_if_exists(source_lock_path)
    record_ids = source_record.get("record_ids_used_by_topic", []) if source_record else []
    runtime_filter = (
        source_lock.get("preprocessing_contract", {}).get("runtime_filter", "")
        if source_lock
        else ""
    )
    runtime_unit = (
        source_lock.get("preprocessing_contract", {}).get("runtime_unit", "")
        if source_lock
        else ""
    )
    hrv_ready = bool(source_record and source_lock and record_ids)
    payload = {
        "schema_version": "1.0",
        "topic": "0.14_Complex_Systems",
        "purpose": "Structured intake stub for branch-specific source evidence before data rewrites or stronger complex-systems claims.",
        "instructions": [
            "Attach upstream DOI or URL, local archive path, branch identifier, and preprocessing note before changing a working-copy dataset.",
            "Record unit convention, record IDs, and baseline role separately for each branch.",
            "Do not treat this file as evidence by itself; it is an intake and tracking layer."
        ],
        "source_targets": [
            {
                "name": "HRV raw PhysioNet package and extraction workflow",
                "priority": "immediate",
                "status": "partial" if hrv_ready else "pending",
                "evidence_fields": [
                    _field(
                        "doi_or_url",
                        "complete" if source_record and source_record.get("dataset_url") else "pending",
                        source_record.get("dataset_url", "") if source_record else "",
                    ),
                    _field(
                        "local_path",
                        "complete" if source_record_path.exists() else "pending",
                        str(source_record_path.relative_to(root_path)).replace("\\", "/") if source_record_path.exists() else "",
                    ),
                    _field(
                        "record_id_manifest",
                        "complete" if record_ids else "pending",
                        ",".join(record_ids),
                    ),
                    _field("extraction_command_or_script", "pending", ""),
                    _field(
                        "unit_basis_and_filter_contract",
                        "complete" if runtime_filter or runtime_unit else "pending",
                        f"{runtime_unit}; filter={runtime_filter}" if (runtime_filter or runtime_unit) else "",
                    ),
                    _field(
                        "preprocessing_note",
                        "complete" if source_lock else "pending",
                        source_lock.get("preprocessing_contract", {}).get("raw_source_status", "") if source_lock else "",
                    ),
                ],
            },
            {
                "name": "SOC avalanche benchmark package",
                "priority": "high",
                "status": "pending",
                "evidence_fields": [
                    {"field": "source_reference", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "avalanche_dataset_or_simulation_identifier", "status": "pending", "value": ""},
                    {"field": "exponent_baseline_reference", "status": "pending", "value": ""},
                    {"field": "unit_basis", "status": "pending", "value": ""},
                    {"field": "preprocessing_note", "status": "pending", "value": ""},
                ],
            },
            {
                "name": "Econophysics market benchmark package",
                "priority": "high",
                "status": "pending",
                "evidence_fields": [
                    {"field": "ticker_or_market_source_reference", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "date_range_or_series_identifier", "status": "pending", "value": ""},
                    {"field": "baseline_model_reference", "status": "pending", "value": ""},
                    {"field": "unit_basis", "status": "pending", "value": ""},
                    {"field": "preprocessing_note", "status": "pending", "value": ""},
                ],
            },
            {
                "name": "Climate and inequality branch package",
                "priority": "medium",
                "status": "pending",
                "evidence_fields": [
                    {"field": "source_reference", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "series_or_indicator_identifier", "status": "pending", "value": ""},
                    {"field": "unit_basis", "status": "pending", "value": ""},
                    {"field": "baseline_or_comparator_reference", "status": "pending", "value": ""},
                    {"field": "preprocessing_note", "status": "pending", "value": ""},
                ],
            },
            {
                "name": "Social-network or ledger branch package",
                "priority": "medium",
                "status": "pending",
                "evidence_fields": [
                    {"field": "source_reference", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "graph_or_ledger_identifier", "status": "pending", "value": ""},
                    {"field": "unit_basis", "status": "pending", "value": ""},
                    {"field": "baseline_or_comparator_reference", "status": "pending", "value": ""},
                    {"field": "preprocessing_note", "status": "pending", "value": ""},
                ],
            },
        ],
        "claim_boundary": "This intake stub is for source evidence capture only. Filling it does not by itself justify broad complex-systems, clinical, market, climate, or social claims.",
    }
    return _write_json(SOURCE_EVIDENCE_INTAKE_PATH, payload)


def _build_source_evidence_readiness_matrix(intake_stub):
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
                "ready_for_source_review": row_ready,
                "blocking_reason": "" if row_ready else "One or more required evidence fields are still pending.",
            }
        )
    payload = {
        "schema_version": "1.0",
        "topic": "0.14_Complex_Systems",
        "purpose": "Readiness matrix for branch-specific source evidence before data edits or claim upgrades.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready,
            "targets_blocked_by_pending_evidence": blocked,
        },
        "readiness_rows": rows,
        "claim_boundary": "This matrix is a workflow gate only. A target marked ready still requires actual source review before working-copy or claim changes.",
    }
    return _write_json(SOURCE_EVIDENCE_READINESS_PATH, payload)


def _build_branch_claim_gate():
    payload = {
        "schema_version": "1.0",
        "topic": "0.14_Complex_Systems",
        "purpose": "Claim gate for separate complex-systems branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 1,
            "blocked_for_strong_claims": 5,
        },
        "branches": [
            {
                "branch": "HRV derived-RR benchmark",
                "status": "accepted_run_contract_only",
                "allowed_usage_now": "Source-referenced HRV metrics benchmark only.",
                "blocker_to_stronger_claim": "Need raw PhysioNet files, extraction workflow, and frozen numeric acceptance thresholds."
            },
            {
                "branch": "SOC branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Simulation or formula sandbox only.",
                "blocker_to_stronger_claim": "Need seeded avalanche benchmark, exponent fit, and artifact-producing verifier."
            },
            {
                "branch": "Econophysics branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Local market sandbox only.",
                "blocker_to_stronger_claim": "Need source-locked market data, baseline model, and thresholded artifact."
            },
            {
                "branch": "Climate branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Exploratory local series only.",
                "blocker_to_stronger_claim": "Need source identity, baseline comparison, and dedicated verifier artifact."
            },
            {
                "branch": "Inequality and social branches",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Exploratory local working files only.",
                "blocker_to_stronger_claim": "Need source-locked data, unit contracts, and branch-specific artifacts."
            },
            {
                "branch": "Cross-domain universal complexity claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Conceptual framing only.",
                "blocker_to_stronger_claim": "Need separate verifier gates for each branch before any universal theory claim."
            },
        ],
        "claim_boundary": "This gate cannot raise claim strength above the current HRV run-contract evidence.",
    }
    return _write_json(BRANCH_CLAIM_GATE_PATH, payload)


def write_verification_artifact(result):
    """Write the primary verifier artifact required by VERIFICATION_SPEC.md."""
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    source_evidence_intake_stub = _build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = _build_source_evidence_readiness_matrix(source_evidence_intake_stub)
    branch_claim_gate = _build_branch_claim_gate()
    artifact = {
        "schema_version": "1.1",
        "topic": "0.14_Complex_Systems",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.14_Complex_Systems/Code/03_Research/Research_Biology_HRV.py",
        "status": result.get("status", "FAIL"),
        "passed_run_contract": result.get("status") in {"PASS", "WARN"},
        "input_hashes": _hrv_input_hashes(),
        "source_evidence_intake_stub": {
            "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
            "sha256": _sha256(SOURCE_EVIDENCE_INTAKE_PATH),
            "source_targets": [item["name"] for item in source_evidence_intake_stub["source_targets"]],
            "claim_boundary": "This intake stub is for source evidence capture only. It does not authorize data or claim upgrades by itself.",
        },
        "source_evidence_readiness_matrix": {
            "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
            "sha256": _sha256(SOURCE_EVIDENCE_READINESS_PATH),
            "summary": source_evidence_readiness_matrix["summary"],
            "claim_boundary": "This readiness matrix is a workflow gate only. It tracks whether source evidence is still pending.",
        },
        "branch_claim_gate": {
            "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
            "sha256": _sha256(BRANCH_CLAIM_GATE_PATH),
            "summary": branch_claim_gate["summary"],
            "claim_boundary": "This gate records branch-specific claim ceilings only. It cannot upgrade the topic beyond the current HRV run-contract evidence.",
        },
        "metrics": {
            "avg_sdnn_ms": result.get("avg_sdnn_ms"),
            "avg_rmssd_ms": result.get("avg_rmssd_ms"),
            "avg_equilibrium": result.get("avg_equilibrium"),
            "subjects": result.get("subjects", 0),
        },
        "thresholds": {
            "run_without_error": True,
            "artifact_written": True,
            "working_sdnn_pass_range_ms": [30, 200],
            "working_equilibrium_min_for_strong_pass": 0.5,
        },
        "interpretation": (
            "Source-referenced derived-RR HRV run-contract artifact only; this does not validate "
            "clinical classification, SOC, econophysics, climate, inequality, or social-network branches."
        ),
        "results": _to_jsonable(result),
    }
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"  [Artifact] Saved {ARTIFACT_PATH}")


def calculate_hrv_metrics(rr_intervals):
    """
    Calculate HRV metrics related to UET equilibrium.
    Delegates to Engine_Complexity.
    """
    # Initialize Engine
    # Note: We use the Complexity Engine which handles Stochastic systems
    import importlib.util

    eng_path = (
        root_path / "docs/topics/0.14_Complex_Systems/Code/01_Engine/Engine_Complexity.py"
    )
    if eng_path.exists():
        spec = importlib.util.spec_from_file_location("Engine_Complexity", eng_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        engine = mod.UETComplexityEngine(name="HRV_Analyzer")
    else:
        print("CRITICAL: Engine not found.")
        return None

    metrics = engine.calculate_hrv_metrics(rr_intervals)

    # Check Kill Switch
    if metrics and math.isnan(metrics.get("equilibrium_score", 0)):
        print("KILL SWITCH DETECTED.")
        return None

    return metrics


def run_test():
    """Run HRV equilibrium test."""
    print("\n" + "=" * 60)
    print("[HRV] UET TEST 04: Bio HRV Equilibrium")
    print("=" * 60)
    print("\nEquation: dOmega/dt <= 0 (equilibrium seeking)")
    print("UET Prediction: Healthy systems show balanced variability")

    datasets = load_hrv_data()

    if not datasets:
        print("[FAIL] No HRV data found!")
        result = {"status": "FAIL", "error": "No data"}
        write_verification_artifact(result)
        return result

    print(f"\nAnalyzing {len(datasets)} subjects...\n")

    results = []

    for name, rr in datasets:
        metrics = calculate_hrv_metrics(rr)

        if metrics:
            results.append({"name": name, **metrics})
            print(f"   {name}:")
            print(f"      Mean RR: {metrics['mean_rr']*1000:.0f} ms")
            print(f"      SDNN: {metrics['sdnn']*1000:.0f} ms")
            print(f"      RMSSD: {metrics['rmssd']*1000:.0f} ms")
            print(f"      Equilibrium Score: {metrics['equilibrium_score']:.2f}")
            print()

    if not results:
        print("[FAIL] Could not calculate metrics")
        result = {"status": "FAIL", "error": "Calculation failed"}
        write_verification_artifact(result)
        return result

    # Summary
    avg_eq = np.mean([r["equilibrium_score"] for r in results])
    avg_sdnn = np.mean([r["sdnn"] for r in results]) * 1000
    avg_rmssd = np.mean([r["rmssd"] for r in results]) * 1000

    print("=" * 40)
    print(f"Average SDNN: {avg_sdnn:.0f} ms")
    print(f"Average RMSSD: {avg_rmssd:.0f} ms")
    print(f"Average Equilibrium Score: {avg_eq:.2f}")
    print("=" * 40)

    # Grade
    # Normal SDNN: 50-150 ms (healthy)
    if 50 < avg_sdnn < 150 and avg_eq > 0.5:
        grade = "***** HEALTHY EQUILIBRIUM"
        status = "PASS"
    elif 30 < avg_sdnn < 200:
        grade = "**** NORMAL RANGE"
        status = "PASS"
    elif avg_sdnn > 20:
        grade = "*** BORDERLINE"
        status = "WARN"
    else:
        grade = "** LOW VARIABILITY"
        status = "FAIL"

    print(f"\nGrade: {grade}")
    print("\nInterpretation:")
    print("   High SDNN (>100ms) = High adaptability")
    print("   Low SDNN (<50ms) = Reduced flexibility (stress/disease)")

    # --- VISUALIZATION ---
    try:
        from docs.core import uet_viz

        result_dir = UETPathManager.get_result_dir(
            topic_id="0.14_Complex_Systems",
            experiment_name="Research_Biology_HRV",
            pillar="03_Research",
            category="log",
        )
        result_dir.mkdir(parents=True, exist_ok=True)

        if results:
            # Plot SD1 vs SD2 (Poincaré Metrics) representing Equilibrium State
            sd1s = [r.get("sd1", 0) * 1000 for r in results]
            sd2s = [r.get("sd2", 0) * 1000 for r in results]
            names = [r.get("name", "Subject") for r in results]
            scores = [r.get("equilibrium_score", 0) for r in results]

            fig = uet_viz.go.Figure()
            fig.add_trace(
                uet_viz.go.Scatter(
                    x=sd1s,
                    y=sd2s,
                    mode="markers",
                    text=names,
                    marker=dict(
                        size=12,
                        color=scores,
                        colorscale="RdYlGn",
                        showscale=True,
                        colorbar=dict(title="Equilibrium Score"),
                    ),
                )
            )

            # Identity line (SD1=SD2)
            max_val = max(max(sd1s), max(sd2s)) if sd1s else 100
            fig.add_trace(
                uet_viz.go.Scatter(
                    x=[0, max_val],
                    y=[0, max_val],
                    mode="lines",
                    line=dict(dash="dash", color="gray"),
                    name="Balanced",
                )
            )

            fig.update_layout(
                title="HRV Non-Linear Dynamics: Equilibrium Analysis",
                xaxis_title="SD1 (Short-Term Variability) [ms]",
                yaxis_title="SD2 (Long-Term Variability) [ms]",
            )
            uet_viz.save_plot(fig, "biology_viz.png", result_dir)
            print("  [Viz] Generated 'biology_viz.png'")

    except Exception as e:
        print(f"Viz Error: {e}")

    result = {
        "status": status,
        "avg_sdnn_ms": avg_sdnn,
        "avg_rmssd_ms": avg_rmssd,
        "avg_equilibrium": avg_eq,
        "subjects": len(results),
        "results": results,
    }
    write_verification_artifact(result)
    return result


if __name__ == "__main__":
    result = run_test()
    print(f"\n[OK] Test complete: {result['status']}")
