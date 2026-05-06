"""
UET Electroweak vs PDG 2025 Real-Data Comparison
================================================
Reads source-locked PDG SQLite data and compares UET electroweak engine outputs
against PDG 2025 summary-table values.

This script is strict about what it proves:
- It validates selected electroweak observables against a real upstream source.
- It does not claim a full Standard Model replacement.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

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

from docs import ROOT_PATH
from docs.core.reproducibility import generate_artifact, hash_dataset, hash_file, save_artifact


root_path = ROOT_PATH
topic_path = root_path / "docs" / "topics" / "0.6_Electroweak_Physics"
engine_path = topic_path / "Code" / "01_Engine"
reference_package_json = root_path / "docs" / "data" / "external" / "particle_physics" / "pdg" / "electroweak_reference_package.json"
source_lock_json = topic_path / "Data" / "03_Research" / "source_lock_manifest.json"
source_evidence_intake_json = topic_path / "Data" / "03_Research" / "source_evidence_intake_stub.json"
source_evidence_readiness_json = topic_path / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
branch_claim_gate_json = topic_path / "Data" / "03_Research" / "branch_claim_gate.json"
if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

try:
    from Engine_Electroweak import UETElectroweakSolver
except ImportError as exc:
    print(f"CRITICAL SETUP ERROR: {exc}")
    sys.exit(1)

def load_reference_package() -> dict:
    if not reference_package_json.exists():
        raise FileNotFoundError(f"Electroweak reference package not found: {reference_package_json}")
    return json.loads(reference_package_json.read_text(encoding="utf-8"))


def load_source_lock() -> dict:
    if not source_lock_json.exists():
        return {"external_source_records": [], "derived_inputs": [], "status": "MISSING"}
    return json.loads(source_lock_json.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def path_hash_record(path_string: str) -> dict:
    path = root_path / path_string
    return {
        "path": path_string,
        "sha256": hash_file(path) if path.exists() and path.is_file() else None,
        "status": "present" if path.exists() else "missing",
    }


def relative_error_percent(predicted: float, observed: float) -> float:
    return abs(predicted - observed) / abs(observed) * 100.0


def to_builtin(value):
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, dict):
        return {k: to_builtin(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_builtin(v) for v in value]
    return value


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.6_Electroweak_Physics",
        "purpose": "Source evidence intake before claim upgrades across the electroweak benchmark branches.",
        "source_targets": [
            {
                "name": "PDG 2025 core electroweak mass package",
                "priority": "immediate",
                "status_hint": "source_backed_ready",
                "evidence_entries": [
                    "sqlite_source_path",
                    "reference_package_path",
                    "mapping_audit_path",
                    "unit_basis",
                    "benchmark_role",
                    "extraction_note",
                ],
            },
            {
                "name": "Weak-mixing-angle and Fermi checked-local package",
                "priority": "high",
                "status_hint": "accepted_with_provenance_caveat",
                "evidence_entries": [
                    "checked_local_reference_path",
                    "mapping_audit_status",
                    "observable_scope",
                    "unit_basis",
                    "claim_boundary_note",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Neutron lifetime benchmark package",
                "priority": "high",
                "status_hint": "checked_local_secondary_gate",
                "evidence_entries": [
                    "benchmark_source_path",
                    "status_note",
                    "observable_scope",
                    "unit_basis",
                    "comparison_role",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Running-angle diagnostic package",
                "priority": "medium",
                "status_hint": "diagnostic_only_checked_local",
                "evidence_entries": [
                    "compiled_points_source",
                    "status_note",
                    "q_range_note",
                    "unit_basis",
                    "diagnostic_role",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Gauge-theory derivation or proof package",
                "priority": "medium",
                "status_hint": "not_closed",
                "evidence_entries": [
                    "proof_script_path",
                    "derivation_scope",
                    "artifact_path",
                    "status_rule",
                    "benchmark_identity",
                    "limitation_note",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself prove electroweak closure.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "PDG 2025 core electroweak mass package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Weak-mixing-angle and Fermi checked-local package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "direct_upstream_mapping",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The checked-local layer is organized and auditable, but direct upstream weak-angle mapping is still missing.",
        },
        {
            "name": "Neutron lifetime benchmark package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "external_source_lock",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The neutron lane is a checked-local benchmark gate, not yet a source-locked external package.",
        },
        {
            "name": "Running-angle diagnostic package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 3,
            "fields_pending": 3,
            "pending_fields": [
                "external_source_lock",
                "pass_fail_rule",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "Compiled running-angle points remain diagnostic-only and are not ready for benchmark-promotion review.",
        },
        {
            "name": "Gauge-theory derivation or proof package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "derivation_scope",
                "artifact_path",
                "status_rule",
                "benchmark_identity",
                "limitation_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "No audit-grade derivation or proof package currently closes the electroweak theory branch.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.6_Electroweak_Physics",
        "purpose": "Readiness matrix for source-evidence review across electroweak benchmark branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row has enough provenance structure for source review. It does not itself upgrade a claim.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.6_Electroweak_Physics",
        "purpose": "Claim gate for separate electroweak branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 3,
            "blocked_for_strong_claims": 3,
        },
        "branches": [
            {
                "branch": "Core PDG mass branch",
                "status": "accepted_source_backed_benchmark",
                "allowed_usage_now": "Source-backed benchmark for selected W, Z, and Higgs mass observables.",
                "blocker_to_stronger_claim": "Need broader electroweak observable coverage before promoting beyond selected benchmark status.",
            },
            {
                "branch": "Weak-mixing-angle and Fermi branch",
                "status": "accepted_with_provenance_caveat",
                "allowed_usage_now": "Accepted benchmark comparison with explicit checked-local caveat.",
                "blocker_to_stronger_claim": "Need direct upstream weak-angle mapping and cleaner source lock for full manuscript-grade promotion.",
            },
            {
                "branch": "Neutron lifetime branch",
                "status": "accepted_secondary_checked_local",
                "allowed_usage_now": "Secondary checked-local benchmark gate only.",
                "blocker_to_stronger_claim": "Need a direct external source lock rather than a checked-local benchmark package.",
            },
            {
                "branch": "Running-angle branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Diagnostic-only compiled-point lane.",
                "blocker_to_stronger_claim": "Need source-backed running-angle data and a justified pass/fail rule.",
            },
            {
                "branch": "Gauge-theory derivation branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Conceptual framing only.",
                "blocker_to_stronger_claim": "Need an audit-grade derivation or proof artifact beyond numerical benchmark agreement.",
            },
            {
                "branch": "Full Standard Model replacement claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by the current evidence package.",
                "blocker_to_stronger_claim": "Need substantially wider source-backed observable coverage and theoretical closure.",
            },
        ],
        "claim_boundary": "This gate cannot raise the topic above the current selected electroweak benchmark package.",
    }


def run_test() -> bool:
    print("=" * 70)
    print("UET ELECTROWEAK REAL-DATA TEST")
    print("Data: PDG 2025 SQLite + electroweak effective-angle snapshot")
    print("=" * 70)

    reference_package = load_reference_package()
    pdg = reference_package["references"]
    source_lock = load_source_lock()
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    write_json(source_evidence_intake_json, source_evidence_intake_stub)
    write_json(source_evidence_readiness_json, source_evidence_readiness_matrix)
    write_json(branch_claim_gate_json, branch_claim_gate)
    solver = UETElectroweakSolver()
    result = solver.solve()

    comparisons = {
        "sin2_theta_W": {
            "predicted": result.sin2_theta_W,
            "observed": pdg["sin2_theta_W_effective"]["value"],
            "unit": "dimensionless",
        },
        "m_W_GeV": {
            "predicted": result.m_W_predicted,
            "observed": pdg["m_W"]["value"],
            "unit": "GeV",
        },
        "m_H_GeV": {
            "predicted": result.m_Higgs_predicted,
            "observed": pdg["m_H"]["value"],
            "unit": "GeV",
        },
        "G_F_GeV_minus_2": {
            "predicted": result.fermi_constant,
            "observed": pdg["fermi_constant"]["value"],
            "unit": "GeV^-2",
        },
    }

    print("\n[1] ELECTROWEAK OBSERVABLES")
    print("-" * 70)
    print("| Observable | UET | PDG/reference | Rel. error |")
    print("| :-- | --: | --: | --: |")

    max_rel_error = 0.0
    for key, cmp in comparisons.items():
        err = relative_error_percent(cmp["predicted"], cmp["observed"])
        cmp["relative_error_percent"] = err
        max_rel_error = max(max_rel_error, err)
        print(
            f"| {key} | {cmp['predicted']:.6g} | {cmp['observed']:.6g} | {err:.3f}% |"
        )

    print("\n[2] INTERPRETATION")
    print("-" * 70)
    print(
        "This test checks whether the UET electroweak engine lands near real upstream\n"
        "electroweak scales and couplings. It does not prove the full gauge theory; it\n"
        "tests whether the numerical consequences of the engine are close to real PDG values."
    )

    # Strict but not theorem-level thresholds.
    passes = {
        "sin2_theta_W": comparisons["sin2_theta_W"]["relative_error_percent"] < 2.0,
        "m_W_GeV": comparisons["m_W_GeV"]["relative_error_percent"] < 2.0,
        "m_H_GeV": comparisons["m_H_GeV"]["relative_error_percent"] < 2.0,
        "G_F_GeV_minus_2": comparisons["G_F_GeV_minus_2"]["relative_error_percent"] < 0.5,
    }
    passed = all(passes.values())

    print("\n[3] PASS/FAIL GATES")
    print("-" * 70)
    for name, ok in passes.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")

    artifact = generate_artifact(
        topic="0.6_Electroweak_Physics",
        dataset_hash=hash_dataset(
            {
                "reference_package": str(reference_package_json.relative_to(root_path)),
                "reference_package_exists": reference_package_json.exists(),
                "m_W": pdg["m_W"]["value"],
                "m_Z": pdg["m_Z"]["value"],
                "m_H": pdg["m_H"]["value"],
                "sin2_theta_W_effective": pdg["sin2_theta_W_effective"]["value"],
                "G_F": pdg["fermi_constant"]["value"],
            }
        ),
        results=to_builtin({
            "status": "PASS" if passed else "FAIL",
            "audit": result.audit,
            "mW_mZ_ratio": result.mW_mZ_ratio,
            "theta_W_deg": result.theta_W_deg,
            "lambda_higgs": result.lambda_higgs,
            "comparisons": comparisons,
            "passes": passes,
            "source_evidence_readiness_summary": source_evidence_readiness_matrix["summary"],
            "branch_claim_gate_summary": branch_claim_gate["summary"],
        }),
        config={
            "source_locked_reference": str(reference_package_json.relative_to(root_path)),
            "pdg_sqlite_source": reference_package["pdg_sqlite_source"],
            "checked_local_reference_source": reference_package["checked_local_reference_source"],
            "source_lock_manifest": str(source_lock_json.relative_to(root_path)),
            "sin2_theta_reference_note": pdg["sin2_theta_W_effective"]["source_note"],
            "rule": "real-data comparison against PDG 2025 summary-table observables where available",
        },
        metrics={
            "max_relative_error_percent": max_rel_error,
            "m_W_relative_error_percent": comparisons["m_W_GeV"]["relative_error_percent"],
            "m_H_relative_error_percent": comparisons["m_H_GeV"]["relative_error_percent"],
            "G_F_relative_error_percent": comparisons["G_F_GeV_minus_2"]["relative_error_percent"],
            "sin2_theta_W_relative_error_percent": comparisons["sin2_theta_W"]["relative_error_percent"],
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
        },
        thresholds={
            "sin2_theta_W_max_relative_error_percent": 2.0,
            "m_W_max_relative_error_percent": 2.0,
            "m_H_max_relative_error_percent": 2.0,
            "G_F_max_relative_error_percent": 0.5,
        },
        notes="Real-data electroweak comparison using a structured source-locked PDG reference package plus explicit checked-local note for observables not yet directly mapped from the SQLite workflow.",
    )
    artifact["input_hashes"] = {
        "source_lock_manifest": hash_file(source_lock_json) if source_lock_json.exists() else None,
        "reference_package": hash_file(reference_package_json),
        "source_records": [
            path_hash_record(path) for path in source_lock.get("external_source_records", [])
        ],
    }
    artifact["source_lock"] = {
        "path": str(source_lock_json.relative_to(root_path)),
        "derived_inputs": source_lock.get("derived_inputs", []),
        "claim_boundary": source_lock.get("claim_boundary"),
    }
    artifact["source_evidence_intake_stub"] = {
        "path": str(source_evidence_intake_json.relative_to(topic_path)).replace("\\", "/"),
        "sha256": hash_file(source_evidence_intake_json),
        "source_targets": [row["name"] for row in source_evidence_intake_stub["source_targets"]],
        "claim_boundary": source_evidence_intake_stub["claim_boundary"],
    }
    artifact["source_evidence_readiness_matrix"] = {
        "path": str(source_evidence_readiness_json.relative_to(topic_path)).replace("\\", "/"),
        "sha256": hash_file(source_evidence_readiness_json),
        "summary": source_evidence_readiness_matrix["summary"],
        "claim_boundary": source_evidence_readiness_matrix["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(branch_claim_gate_json.relative_to(topic_path)).replace("\\", "/"),
        "sha256": hash_file(branch_claim_gate_json),
        "summary": branch_claim_gate["summary"],
        "claim_boundary": branch_claim_gate["claim_boundary"],
    }
    artifact["interpretation"] = (
        "This artifact supports selected electroweak benchmark agreement only. "
        "Core masses are source-backed, weak-angle and Fermi layers remain accepted with provenance caveats, "
        "and broader theory-closure claims remain blocked."
    )
    artifact["limitations"] = [
        "The current artifact certifies selected benchmark agreement, not full electroweak closure.",
        "Weak-mixing-angle and Fermi entries still depend on a checked-local layer for direct comparison.",
        "Running-angle points remain diagnostic-only and are not benchmark gates.",
        "Gauge-theory derivation and Standard Model replacement claims remain blocked.",
    ]
    artifact_path = topic_path / "Result" / "artifacts" / "electroweak_pdg_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"\nArtifact saved to {artifact_path}")
    print(f"\nRESULT: {'PASS' if passed else 'FAIL'}")
    return passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
