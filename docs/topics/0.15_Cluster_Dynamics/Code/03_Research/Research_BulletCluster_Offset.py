"""
UET Research: Bullet Cluster Offset
===================================
Topic 0.15 diagnostic verifier.

This script checks whether the topic-local toy collision model reproduces only the
qualitative sign of the Bullet Cluster lensing/X-ray separation. It does not
calibrate the separation in kpc and must not be used as a dark-matter replacement
proof.
"""

import json
import platform
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path


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
    print("CRITICAL: UET docs root not found")
    sys.exit(1)


TOPIC_DIR = ROOT / "docs" / "topics" / "0.15_Cluster_Dynamics"
DATA_PATH = TOPIC_DIR / "Data" / "Bullet_Cluster_Coordinates.json"
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_15_cluster_dynamics_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"


def file_sha256(path):
    digest = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_bullet_coordinates():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def simulate_collision():
    dt = 0.1
    steps = 300
    x_gas = -10.0
    x_halo = -10.0
    v_gas = 1.0
    v_halo = 1.0
    drag_gas = 0.05
    drag_halo = 0.0
    center = 0.0

    for _ in range(steps):
        if abs(x_gas - center) < 2.0:
            v_gas *= 1.0 - drag_gas
        if abs(x_halo - center) < 2.0:
            v_halo *= 1.0 - drag_halo
        x_gas += v_gas * dt
        x_halo += v_halo * dt

    return {
        "dt": dt,
        "steps": steps,
        "drag_gas": drag_gas,
        "drag_halo": drag_halo,
        "x_gas_final_model_units": x_gas,
        "x_halo_final_model_units": x_halo,
        "offset_model_units": x_halo - x_gas,
    }


def build_observation_summary(data):
    components = data["components"]
    rows = []
    for key, component in components.items():
        rows.append(
            {
                "component": key,
                "offset_kpc": component["offset_kpc"],
                "lensing_peak_label": component["lensing_peak"]["label"],
                "xray_peak_label": component["xray_peak"]["label"],
                "observed_separation_positive": component["offset_kpc"] > 0,
            }
        )
    return rows


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.15_Cluster_Dynamics",
        "purpose": "Source evidence intake before upgrading claims across Bullet Cluster, virial, and information-halo cluster branches.",
        "source_targets": [
            {
                "name": "Bullet Cluster offset benchmark package",
                "priority": "immediate",
                "status_hint": "working_copy_benchmark_with_real_source_label",
                "evidence_entries": [
                    "working_copy_json_path",
                    "upstream_url_or_doi",
                    "transcription_note",
                    "observable_scope",
                    "unit_basis",
                    "benchmark_role",
                ],
            },
            {
                "name": "Bullet Cluster dimensional calibration package",
                "priority": "high",
                "status_hint": "qualitative_only_open",
                "evidence_entries": [
                    "ra_dec_to_kpc_method",
                    "offset_magnitude_gate",
                    "calibration_artifact_path",
                    "geometry_scope",
                    "unit_basis",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Virial and mass-temperature benchmark package",
                "priority": "high",
                "status_hint": "secondary_source_labeled_datasets",
                "evidence_entries": [
                    "cluster_virial_dataset_paths",
                    "chandra_dataset_path",
                    "upstream_source_package",
                    "artifact_paths",
                    "unit_basis",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Information-halo grid engine package",
                "priority": "high",
                "status_hint": "model_unit_engine_diagnostic",
                "evidence_entries": [
                    "engine_path",
                    "unit_mapping_note",
                    "lensing_comparison_artifact",
                    "grid_parameter_policy",
                    "claim_boundary_note",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Cluster dark-matter replacement package",
                "priority": "medium",
                "status_hint": "blocked_theory_branch",
                "evidence_entries": [
                    "multi_cluster_held_out_suite",
                    "lensing_map_comparison",
                    "virial_bridge_sensitivity",
                    "cross_topic_dependency_map",
                    "artifact_path",
                    "upgrade_requirement",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself validate a dark-matter-free cluster theory.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "Bullet Cluster offset benchmark package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "upstream_url_or_doi",
                "transcription_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The Bullet Cluster working copy has a real source label, but archival pointer and transcription audit are not yet frozen.",
        },
        {
            "name": "Bullet Cluster dimensional calibration package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "ra_dec_to_kpc_method",
                "offset_magnitude_gate",
                "calibration_artifact_path",
                "geometry_scope",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The current verifier checks only separation sign and has no calibrated kpc magnitude model.",
        },
        {
            "name": "Virial and mass-temperature benchmark package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 3,
            "fields_pending": 3,
            "pending_fields": [
                "upstream_source_package",
                "artifact_paths",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "Secondary virial and mass-temperature datasets exist but are not yet primary-gated with dedicated artifacts.",
        },
        {
            "name": "Information-halo grid engine package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 2,
            "fields_pending": 4,
            "pending_fields": [
                "unit_mapping_note",
                "lensing_comparison_artifact",
                "grid_parameter_policy",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The information-halo engine remains a model-unit diagnostic without physical lensing calibration.",
        },
        {
            "name": "Cluster dark-matter replacement package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "multi_cluster_held_out_suite",
                "lensing_map_comparison",
                "virial_bridge_sensitivity",
                "cross_topic_dependency_map",
                "artifact_path",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "There is no held-out multi-cluster package or lensing-map comparison that would support a dark-matter replacement claim.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.15_Cluster_Dynamics",
        "purpose": "Readiness matrix for source-evidence review across cluster-dynamics benchmark and theory branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row has enough provenance structure for source review. It does not by itself upgrade cluster or dark-matter claims.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.15_Cluster_Dynamics",
        "purpose": "Claim gate for separate cluster-dynamics branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 2,
            "blocked_for_strong_claims": 4,
        },
        "branches": [
            {
                "branch": "Bullet Cluster qualitative offset branch",
                "status": "accepted_qualitative_diagnostic_branch",
                "allowed_usage_now": "Accepted qualitative sign-match diagnostic for Bullet Cluster separation direction only.",
                "blocker_to_stronger_claim": "Need calibrated kpc offset modeling before promoting beyond a qualitative branch.",
            },
            {
                "branch": "Cluster-scale mechanism bridge branch",
                "status": "accepted_mechanism_diagnostic_branch",
                "allowed_usage_now": "Accepted mechanism-diagnostic branch for exploratory cluster-scale information-field behavior only.",
                "blocker_to_stronger_claim": "Need multi-cluster sensitivity and dimensional calibration before using it as physical evidence.",
            },
            {
                "branch": "Virial discrepancy branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Secondary comparator only.",
                "blocker_to_stronger_claim": "Need dedicated virial artifacts with source-normalized datasets and sensitivity controls.",
            },
            {
                "branch": "Information-halo lensing branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Model-unit diagnostic only.",
                "blocker_to_stronger_claim": "Need physical unit mapping and lensing-map comparison.",
            },
            {
                "branch": "Bullet Cluster magnitude-prediction branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need calibrated kpc magnitude prediction with numeric thresholds against observed offsets.",
            },
            {
                "branch": "Dark-matter replacement claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need held-out multi-cluster and lensing evidence beyond the current toy diagnostic.",
            },
        ],
        "claim_boundary": "This gate keeps the topic at qualitative cluster-diagnostic status, not dark-matter replacement closure.",
    }


def build_cluster_claim_scope_gate(
    status: str,
    model: dict,
    observations: list[dict],
    source_evidence_readiness_matrix: dict,
    branch_claim_gate: dict,
) -> dict:
    sign_match = model["offset_model_units"] > 0 and all(
        row["observed_separation_positive"] for row in observations
    )
    return {
        "schema_version": "1.0",
        "topic": "0.15_Cluster_Dynamics",
        "controller_status": status,
        "controller_reason": (
            "The qualitative Bullet Cluster separation sign matches, but export remains WARN because "
            "the model has no kpc calibration, lensing-map comparison, or held-out multi-cluster gate."
            if status == "WARN"
            else "The qualitative Bullet Cluster separation-sign gate failed."
        ),
        "claim_class": "D_qualitative_cluster_diagnostic_only",
        "allowed_claims_now": [
            {
                "claim": "The toy model reproduces the qualitative gas/halo separation direction for the local Bullet Cluster working copy.",
                "status": "WARN" if sign_match else "FAIL",
                "artifact_role": "qualitative sign diagnostic",
                "metric": "offset_sign_match",
                "metric_value": sign_match,
                "source_evidence_readiness": "working_copy_not_fully_archived",
            },
            {
                "claim": "Cluster-scale information-field behavior may be discussed as a bounded mechanism diagnostic.",
                "status": "DIAGNOSTIC_ONLY",
                "artifact_role": "mechanism diagnostic branch",
                "formula_role": "dimensionless toy drag, not calibrated kpc dynamics",
                "source_evidence_readiness": "pending_dimensional_calibration",
            },
        ],
        "blocked_claims": [
            {
                "claim": "UET predicts the Bullet Cluster kpc offsets.",
                "status": "BLOCKED",
                "blocking_reason": "The current model-unit offset is not calibrated to the observed 480 kpc and 120 kpc offsets.",
                "next_evidence_required": [
                    "kpc calibration artifact",
                    "numeric magnitude thresholds",
                    "uncertainty-aware observed-offset package",
                ],
            },
            {
                "claim": "UET replaces dark matter at cluster scale.",
                "status": "BLOCKED",
                "blocking_reason": "No held-out multi-cluster suite or lensing-map comparison supports a replacement claim.",
                "next_evidence_required": [
                    "held-out multi-cluster benchmark",
                    "lensing-map comparison artifact",
                    "virial and mass-temperature source-locked artifacts",
                ],
            },
            {
                "claim": "UET resolves JWST early galaxy or cluster formation tensions.",
                "status": "BLOCKED",
                "blocking_reason": "JWST formation scripts are not the primary artifact and are not source-gated here.",
                "next_evidence_required": [
                    "source-locked JWST candidate package",
                    "LCDM baseline definition",
                    "formation-rate uncertainty artifact",
                ],
            },
        ],
        "blocked_export_phrases": [
            "Bullet Cluster solved",
            "dark matter replaced",
            "cluster virial discrepancy resolved",
            "lensing mass map predicted",
            "JWST age problem resolved",
        ],
        "source_evidence_summary": source_evidence_readiness_matrix["summary"],
        "branch_claim_gate_summary": branch_claim_gate["summary"],
        "machine_readable_next_blockers": [
            "bullet_cluster_kpc_calibration_missing",
            "lensing_map_comparison_missing",
            "held_out_multi_cluster_suite_missing",
            "virial_artifacts_not_primary_gated",
            "jwst_formation_claim_not_primary_gated",
        ],
        "claim_boundary": (
            "A WARN artifact supports only qualitative Bullet Cluster separation-sign diagnostics and bounded "
            "mechanism discussion. It does not predict kpc offsets, replace dark matter, resolve virial "
            "discrepancies, or validate JWST formation claims."
        ),
    }


def main():
    print("=" * 60)
    print("UET RESEARCH: BULLET CLUSTER OFFSET DIAGNOSTIC")
    print("=" * 60)

    data = load_bullet_coordinates()
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)
    observations = build_observation_summary(data)
    model = simulate_collision()
    model_positive = model["offset_model_units"] > 0
    observed_positive = all(row["observed_separation_positive"] for row in observations)

    status = "WARN" if model_positive and observed_positive else "FAIL"
    failure_reason = None
    if status == "WARN":
        failure_reason = (
            "Qualitative separation sign matches, but the toy model is not "
            "dimensionally calibrated to kpc offsets."
        )
    else:
        failure_reason = "Toy model failed even the qualitative separation-sign gate."

    print(f"System: {data['system']}")
    print(f"Reference: {data['reference']}")
    for row in observations:
        print(f"Observed {row['component']} offset: {row['offset_kpc']} kpc")
    print(f"Model offset: {model['offset_model_units']:.2f} model units")
    print(f"Artifact status: {status}")
    cluster_claim_scope_gate = build_cluster_claim_scope_gate(
        status,
        model,
        observations,
        source_evidence_readiness_matrix,
        branch_claim_gate,
    )

    artifact = {
        "schema_version": "1.1",
        "topic": "0.15_Cluster_Dynamics",
        "status": status,
        "claim_class": "D - qualitative diagnostic only",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.15_Cluster_Dynamics/Code/03_Research/Research_BulletCluster_Offset.py",
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "inputs": [
            {
                "path": str(DATA_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(DATA_PATH),
                "source": data["reference"],
                "system": data["system"],
                "unit_system": data["scale"],
            }
        ],
        "formula_ids": [
            "CL15-DRAG-TOY",
            "CL15-OFFSET-SIGN-GATE",
        ],
        "threshold": {
            "qualitative_offset_sign_match_required": True,
            "dimensional_kpc_calibration_required_for_PASS": True,
        },
        "metrics": {
            "observed_offsets_kpc": {
                row["component"]: row["offset_kpc"] for row in observations
            },
            "model_offset_model_units": model["offset_model_units"],
            "offset_sign_match": model_positive and observed_positive,
            "dimensional_calibration_present": False,
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
            "blocked_claim_exports": len(cluster_claim_scope_gate["blocked_export_phrases"]),
        },
        "model": model,
        "observations": observations,
        "failure_reason": failure_reason,
        "limitations": [
            "The current collision model is one-dimensional and dimensionless.",
            "The artifact supports only a qualitative separation-sign diagnostic.",
            "It does not predict the observed 480 kpc or 120 kpc offsets.",
            "It does not establish a dark-matter-free cluster theory.",
        ],
    }
    artifact["source_evidence_intake_stub"] = {
        "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(source_evidence_intake_stub, sort_keys=True).encode("utf-8")).hexdigest(),
        "source_targets": [row["name"] for row in source_evidence_intake_stub["source_targets"]],
        "claim_boundary": source_evidence_intake_stub["claim_boundary"],
    }
    artifact["source_evidence_readiness_matrix"] = {
        "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(source_evidence_readiness_matrix, sort_keys=True).encode("utf-8")).hexdigest(),
        "summary": source_evidence_readiness_matrix["summary"],
        "claim_boundary": source_evidence_readiness_matrix["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(branch_claim_gate, sort_keys=True).encode("utf-8")).hexdigest(),
        "summary": branch_claim_gate["summary"],
        "claim_boundary": branch_claim_gate["claim_boundary"],
    }
    artifact["cluster_claim_scope_gate"] = cluster_claim_scope_gate
    artifact["interpretation"] = (
        "This artifact supports a qualitative Bullet Cluster sign-match branch and a bounded cluster mechanism-diagnostic branch. "
        "It does not validate cluster-scale dark-matter replacement."
    )

    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Artifact written: {ARTIFACT_PATH}")
    return 0 if status in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    sys.exit(main())
