"""Expanded electroweak benchmark for topic 0.6 with explicit provenance separation."""

from __future__ import annotations

import json
import math
import sys
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
if not ROOT:
    print("CRITICAL: UET docs root not found!")
    sys.exit(1)


from docs import ROOT_PATH
from docs.core.reproducibility import generate_artifact, hash_dataset, hash_file, save_artifact


root_path = ROOT_PATH
topic_path = root_path / "docs" / "topics" / "0.6_Electroweak_Physics"
benchmark_package_json = root_path / "docs" / "data" / "external" / "particle_physics" / "pdg" / "electroweak_benchmark_package.json"
source_lock_json = topic_path / "Data" / "03_Research" / "source_lock_manifest.json"
source_evidence_intake_json = topic_path / "Data" / "03_Research" / "source_evidence_intake_stub.json"
source_evidence_readiness_json = topic_path / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
branch_claim_gate_json = topic_path / "Data" / "03_Research" / "branch_claim_gate.json"
engine_path = topic_path / "Code" / "01_Engine"
if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

from Engine_Electroweak import M_Z_GEV, UETElectroweakSolver


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def running_angle_prediction(q_gev: float) -> float:
    sin2_z = 0.23121
    slope = 0.0075
    if q_gev < 1e-4:
        q_gev = 1e-4
    return sin2_z * (1 + slope * math.log(M_Z_GEV / q_gev))


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


def main() -> int:
    benchmark = load_json(benchmark_package_json)
    source_lock = load_json(source_lock_json) if source_lock_json.exists() else {"external_source_records": [], "derived_inputs": []}
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    write_json(source_evidence_intake_json, source_evidence_intake_stub)
    write_json(source_evidence_readiness_json, source_evidence_readiness_matrix)
    write_json(branch_claim_gate_json, branch_claim_gate)
    solver = UETElectroweakSolver()
    result = solver.solve()
    core = benchmark["core_observables"]
    neutron = benchmark["neutron_decay_benchmark"]
    running_points = benchmark["running_angle_diagnostic"]["points"]

    core_comparisons = {
        "sin2_theta_W": {
            "predicted": result.sin2_theta_W,
            "observed": core["sin2_theta_W_effective"]["value"],
            "relative_error_percent": relative_error_percent(result.sin2_theta_W, core["sin2_theta_W_effective"]["value"]),
        },
        "m_W_GeV": {
            "predicted": result.m_W_predicted,
            "observed": core["m_W"]["value"],
            "relative_error_percent": relative_error_percent(result.m_W_predicted, core["m_W"]["value"]),
        },
        "m_H_GeV": {
            "predicted": result.m_Higgs_predicted,
            "observed": core["m_H"]["value"],
            "relative_error_percent": relative_error_percent(result.m_Higgs_predicted, core["m_H"]["value"]),
        },
        "G_F_GeV_minus_2": {
            "predicted": result.fermi_constant,
            "observed": core["fermi_constant"]["value"],
            "relative_error_percent": relative_error_percent(result.fermi_constant, core["fermi_constant"]["value"]),
        },
        "neutron_lifetime_s": {
            "predicted": result.neutron_lifetime,
            "observed": neutron["best_lifetime_s"],
            "relative_error_percent": relative_error_percent(result.neutron_lifetime, neutron["best_lifetime_s"]),
        },
    }

    running_diagnostic = []
    for point in running_points:
        pred = running_angle_prediction(point["Q_GeV"])
        running_diagnostic.append(
            {
                "label": point["label"],
                "Q_GeV": point["Q_GeV"],
                "observed": point["sin2_theta_W"],
                "predicted": pred,
                "relative_error_percent": relative_error_percent(pred, point["sin2_theta_W"]),
                "provenance_status": point["provenance_status"],
            }
        )

    running_average_error = sum(item["relative_error_percent"] for item in running_diagnostic) / len(running_diagnostic)

    gates = {
        "sin2_theta_W": core_comparisons["sin2_theta_W"]["relative_error_percent"] < 2.0,
        "m_W_GeV": core_comparisons["m_W_GeV"]["relative_error_percent"] < 2.0,
        "m_H_GeV": core_comparisons["m_H_GeV"]["relative_error_percent"] < 2.0,
        "G_F_GeV_minus_2": core_comparisons["G_F_GeV_minus_2"]["relative_error_percent"] < 0.5,
        "neutron_lifetime_s": core_comparisons["neutron_lifetime_s"]["relative_error_percent"] < 2.0,
    }
    passed = all(gates.values())

    artifact = generate_artifact(
        topic="0.6_Electroweak_Physics",
        dataset_hash=hash_dataset(
            {
                "benchmark_package": str(benchmark_package_json.relative_to(root_path)),
                "sin2_theta_W": core["sin2_theta_W_effective"]["value"],
                "m_W": core["m_W"]["value"],
                "m_H": core["m_H"]["value"],
                "G_F": core["fermi_constant"]["value"],
                "neutron_lifetime_s": neutron["best_lifetime_s"],
            }
        ),
        results=to_builtin(
            {
                "status": "PASS" if passed else "FAIL",
                "core_comparisons": core_comparisons,
                "core_gates": gates,
                "running_angle_diagnostic": running_diagnostic,
                "running_angle_diagnostic_status": benchmark["running_angle_diagnostic"]["status"],
                "running_angle_average_error_percent": running_average_error,
                "source_evidence_readiness_summary": source_evidence_readiness_matrix["summary"],
                "branch_claim_gate_summary": branch_claim_gate["summary"],
            }
        ),
        config={
            "benchmark_package": str(benchmark_package_json.relative_to(root_path)),
            "source_lock_manifest": str(source_lock_json.relative_to(root_path)),
            "engine_path": str((topic_path / "Code" / "01_Engine" / "Engine_Electroweak.py").relative_to(root_path)),
            "interpretation": "Only the core observables plus neutron lifetime act as benchmark gates; running-angle points remain diagnostic-only because they are compiled local benchmarks.",
        },
        metrics={
            "max_core_relative_error_percent": max(v["relative_error_percent"] for v in core_comparisons.values()),
            "running_angle_average_error_percent": running_average_error,
            "neutron_lifetime_relative_error_percent": core_comparisons["neutron_lifetime_s"]["relative_error_percent"],
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
        },
        thresholds={
            "sin2_theta_W_max_relative_error_percent": 2.0,
            "m_W_max_relative_error_percent": 2.0,
            "m_H_max_relative_error_percent": 2.0,
            "G_F_max_relative_error_percent": 0.5,
            "neutron_lifetime_max_relative_error_percent": 2.0,
        },
        notes="Expanded electroweak benchmark separates source-linked core gates from checked-local diagnostic layers.",
    )
    artifact["input_hashes"] = {
        "source_lock_manifest": hash_file(source_lock_json) if source_lock_json.exists() else None,
        "benchmark_package": hash_file(benchmark_package_json),
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
        "This expanded artifact supports the selected core electroweak benchmark package and a secondary neutron benchmark. "
        "Running-angle points remain diagnostic-only, and broader electroweak-theory replacement claims remain blocked."
    )
    artifact["limitations"] = [
        "The current expanded artifact does not certify a full electroweak derivation.",
        "Weak-mixing-angle and neutron layers still include checked-local provenance constraints.",
        "Running-angle points remain diagnostic-only compiled benchmarks.",
        "Standard Model replacement claims remain unsupported by the current evidence package.",
    ]
    artifact_path = topic_path / "Result" / "artifacts" / "electroweak_expanded_benchmark.json"
    save_artifact(artifact, artifact_path)

    print("=" * 70)
    print("UET ELECTROWEAK EXPANDED BENCHMARK")
    print("=" * 70)
    for name, cmp in core_comparisons.items():
        print(f"{name}: pred={cmp['predicted']:.6g} obs={cmp['observed']:.6g} err={cmp['relative_error_percent']:.3f}%")
    print(f"running-angle diagnostic avg error: {running_average_error:.3f}%")
    print(f"Artifact saved to {artifact_path}")
    print(f"RESULT: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
