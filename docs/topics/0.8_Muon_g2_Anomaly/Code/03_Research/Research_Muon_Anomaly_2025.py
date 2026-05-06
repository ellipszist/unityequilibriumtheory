"""
UET Muon g-2 Anomaly Research (2025 source-locked experiment + theory)
======================================================================
Topic: 0.8 Muon g-2 Anomaly
Goal: Compare the UET anomaly prediction against the source-locked 2025 experimental
result and the source-locked Muon g-2 Theory Initiative 2025 Standard-Model comparator.
"""

from __future__ import annotations

import json
import math
import sys
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
    print("CRITICAL: UET docs root not found!")
    sys.exit(1)


from docs import ROOT_PATH
from docs.core.reproducibility import generate_artifact, hash_dataset, save_artifact


root_path = ROOT_PATH
topic_dir = root_path / "docs" / "topics" / "0.8_Muon_g2_Anomaly"
experimental_json = root_path / "docs" / "data" / "external" / "particle_physics" / "muon_g2" / "fermilab_muon_g2_2025_experiment.json"
theory_json = root_path / "docs" / "data" / "external" / "particle_physics" / "muon_g2" / "theory" / "muon_g2_theory_2025_total_sm.json"
baseline_package_json = root_path / "docs" / "data" / "external" / "particle_physics" / "muon_g2" / "theory" / "muon_g2_baseline_package.json"
source_evidence_intake_json = topic_dir / "Data" / "03_Research" / "source_evidence_intake_stub.json"
source_evidence_readiness_json = topic_dir / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
branch_claim_gate_json = topic_dir / "Data" / "03_Research" / "branch_claim_gate.json"
engine_path = topic_dir / "Code" / "01_Engine"
LEGACY_UET_REFERENCE_DELTA = 2.51e-9

if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

from Engine_Muon_G2 import UETMuonG2Solver


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def uet_muon_anomaly() -> float:
    solver = UETMuonG2Solver()
    return solver.calculate_uet_correction()


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.8_Muon_g2_Anomaly",
        "purpose": "Source evidence intake before upgrading claims across the muon g-2 benchmark, sensitivity, and downstream particle-physics branches.",
        "source_targets": [
            {
                "name": "2025 experiment package",
                "priority": "immediate",
                "status_hint": "source_backed_ready",
                "evidence_entries": [
                    "official_source_html_path",
                    "extracted_json_path",
                    "observable_scope",
                    "unit_basis",
                    "uncertainty_field",
                    "benchmark_role",
                ],
            },
            {
                "name": "2025 theory comparator package",
                "priority": "immediate",
                "status_hint": "source_backed_ready",
                "evidence_entries": [
                    "official_source_html_path",
                    "extracted_json_path",
                    "observable_scope",
                    "unit_basis",
                    "uncertainty_field",
                    "benchmark_role",
                ],
            },
            {
                "name": "Structured baseline package",
                "priority": "high",
                "status_hint": "source_backed_ready_with_local_diagnostic_lanes",
                "evidence_entries": [
                    "baseline_package_path",
                    "canonical_baseline_label",
                    "historical_local_labels",
                    "provenance_status_fields",
                    "diagnostic_boundary_note",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Live engine anomaly derivation package",
                "priority": "high",
                "status_hint": "accepted_benchmark_gate_with_derivation_gap",
                "evidence_entries": [
                    "engine_source_path",
                    "formula_registry_entry",
                    "parameter_origin_note",
                    "observable_scope",
                    "derivation_gap_note",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Alternate-theory and downstream particle-consistency package",
                "priority": "medium",
                "status_hint": "blocked_expansion_branch",
                "evidence_entries": [
                    "alternate_theory_inputs",
                    "held_out_comparator_package",
                    "downstream_topic_dependency_map",
                    "claim_boundary_note",
                    "artifact_paths",
                    "upgrade_requirement",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself resolve the muon g-2 anomaly.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "2025 experiment package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "2025 theory comparator package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Structured baseline package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 5,
            "fields_pending": 1,
            "pending_fields": ["held_out_external_theory_expansion"],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Live engine anomaly derivation package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "first_principles_derivation",
                "hadronic_or_electroweak_bridge_closure",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The live engine is benchmark-compatible but still lacks a fuller first-principles derivation package.",
        },
        {
            "name": "Alternate-theory and downstream particle-consistency package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "alternate_theory_inputs",
                "held_out_comparator_package",
                "downstream_topic_dependency_map",
                "artifact_paths",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The topic does not yet cover a held-out alternate-theory suite or downstream particle-consistency map.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.8_Muon_g2_Anomaly",
        "purpose": "Readiness matrix for source-evidence review across muon g-2 benchmark and theory-expansion branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row has enough provenance structure for source review. It does not by itself upgrade anomaly-resolution claims.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.8_Muon_g2_Anomaly",
        "purpose": "Claim gate for separate muon g-2 branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 3,
            "blocked_for_strong_claims": 3,
        },
        "branches": [
            {
                "branch": "2025 source-locked benchmark branch",
                "status": "accepted_source_backed_benchmark",
                "allowed_usage_now": "Accepted benchmark compatibility branch against the source-locked 2025 experiment-theory package.",
                "blocker_to_stronger_claim": "Need stronger derivation and broader held-out comparators before treating this as anomaly closure.",
            },
            {
                "branch": "Sensitivity and benchmark-shift diagnostic branch",
                "status": "accepted_diagnostic_branch",
                "allowed_usage_now": "Accepted diagnostic branch showing how the live engine compares across canonical and historical baselines.",
                "blocker_to_stronger_claim": "Diagnostics do not by themselves establish scientific preference among theory packages.",
            },
            {
                "branch": "Legacy-reference discipline branch",
                "status": "accepted_workflow_governance_branch",
                "allowed_usage_now": "Accepted workflow-governance branch that prevents stale hardcoded references from standing in for the live engine.",
                "blocker_to_stronger_claim": "Governance improvements do not increase the underlying physics evidence by themselves.",
            },
            {
                "branch": "First-principles anomaly derivation branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported beyond a compact engine benchmark term.",
                "blocker_to_stronger_claim": "Need a fuller derivation tying the engine term to hadronic and electroweak structure rather than benchmark compatibility alone.",
            },
            {
                "branch": "Alternate-theory exclusion branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need held-out alternate-theory packages and comparator discipline beyond local historical baselines.",
            },
            {
                "branch": "Downstream particle-theory support claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "May only be cited as a constrained benchmark artifact by related particle topics.",
                "blocker_to_stronger_claim": "Need cross-topic consistency with electroweak, hadronic, and mass-generation branches before claiming wider support.",
            },
        ],
        "claim_boundary": "This gate keeps the topic at benchmark-compatibility status and blocks anomaly-closure claims.",
    }


def run_research() -> bool:
    print("=" * 60)
    print("UET MUON g-2 ANOMALY RESEARCH")
    print("Data: 2025 source-locked experiment + 2025 source-locked theory comparator")
    print("=" * 60)

    exp_data = load_json(experimental_json)
    theory_data = load_json(theory_json)
    baseline_package = load_json(baseline_package_json)
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    write_json(source_evidence_intake_json, source_evidence_intake_stub)
    write_json(source_evidence_readiness_json, source_evidence_readiness_matrix)
    write_json(branch_claim_gate_json, branch_claim_gate)

    a_exp = exp_data["data"]["a_mu_exp"]
    exp_err = exp_data["data"]["combined_error"]
    a_sm = theory_data["data"]["a_mu_sm_total"]["value"]
    sm_err = theory_data["data"]["a_mu_sm_total"]["uncertainty"]

    delta_val = a_exp - a_sm
    delta_err = math.sqrt(exp_err**2 + sm_err**2)
    sigma = delta_val / delta_err if delta_err else float("inf")
    uet_delta = uet_muon_anomaly()
    legacy_reference_delta = LEGACY_UET_REFERENCE_DELTA
    deviation = abs(uet_delta - delta_val)
    z_score = deviation / delta_err if delta_err else float("inf")
    legacy_reference_z_score = abs(legacy_reference_delta - delta_val) / delta_err if delta_err else float("inf")

    print(f"Experimental a_mu (2025):         {a_exp:.12f}")
    print(f"Experimental combined error:      {exp_err:.3e}")
    print(f"SM comparator (WP25):            {a_sm:.12f}")
    print(f"SM comparator uncertainty:        {sm_err:.3e}")
    print(f"Derived delta_a_mu:               {delta_val*1e9:.3f} x 10^-9")
    print(f"Derived significance:             {sigma:.2f} sigma")
    print(f"UET engine prediction for excess: {uet_delta*1e9:.3f} x 10^-9")
    print(f"Difference (UET - derived delta): {deviation*1e9:.3f} x 10^-9")
    print(f"Compatibility z-score:            {z_score:.2f} sigma")

    passes = z_score < 2.0
    print("PASS" if passes else "FAIL")

    artifact = generate_artifact(
        topic="0.8_Muon_g2_Anomaly",
        dataset_hash=hash_dataset(
            {
                "experimental_source": str(experimental_json.relative_to(root_path)),
                "theory_source": str(theory_json.relative_to(root_path)),
                "a_mu_exp_2025": a_exp,
                "a_mu_sm_wp25": a_sm,
            }
        ),
        results={
            "status": "PASS" if passes else "FAIL",
            "claim_class": "C source-backed internal benchmark" if passes else "model-hardening blocker",
            "a_mu_exp_2025": a_exp,
            "a_mu_sm_wp25": a_sm,
            "delta_a_mu_derived": delta_val,
            "delta_error_derived": delta_err,
            "significance_sigma_derived": sigma,
            "engine_delta": uet_delta,
            "legacy_reference_delta": legacy_reference_delta,
            "deviation": deviation,
            "engine_z_score_2025": z_score,
            "legacy_reference_z_score_2025": legacy_reference_z_score,
            "z_score": z_score,
            "source_evidence_readiness_summary": source_evidence_readiness_matrix["summary"],
            "branch_claim_gate_summary": branch_claim_gate["summary"],
            "baseline_package_summary": {
                "path": str(baseline_package_json.relative_to(root_path)),
                "canonical_verification_baseline": baseline_package["canonical_verification_baseline"],
                "baseline_count": len(baseline_package["baselines"]),
            },
        },
        config={
            "experimental_source_locked": str(experimental_json.relative_to(root_path)),
            "theory_source_locked": str(theory_json.relative_to(root_path)),
            "baseline_package": str(baseline_package_json.relative_to(root_path)),
        },
        metrics={
            "delta_a_mu_derived_times_1e9": delta_val * 1e9,
            "engine_delta_times_1e9": uet_delta * 1e9,
            "legacy_reference_delta_times_1e9": legacy_reference_delta * 1e9,
            "engine_z_score_2025": z_score,
            "legacy_reference_z_score_2025": legacy_reference_z_score,
            "z_score": z_score,
            "significance_sigma_derived": sigma,
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
        },
        thresholds={"max_compatibility_z_score": 2.0},
        notes=(
            "Both the experimental and theory comparator inputs are now source-locked to 2025 references. "
            "The UET comparator is taken from Engine_Muon_G2 rather than a topic-local hardcoded anomaly constant."
        ),
    )
    artifact["source_evidence_intake_stub"] = {
        "path": str(source_evidence_intake_json.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(source_evidence_intake_stub),
        "source_targets": [row["name"] for row in source_evidence_intake_stub["source_targets"]],
        "claim_boundary": source_evidence_intake_stub["claim_boundary"],
    }
    artifact["source_evidence_readiness_matrix"] = {
        "path": str(source_evidence_readiness_json.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(source_evidence_readiness_matrix),
        "summary": source_evidence_readiness_matrix["summary"],
        "claim_boundary": source_evidence_readiness_matrix["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(branch_claim_gate_json.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(branch_claim_gate),
        "summary": branch_claim_gate["summary"],
        "claim_boundary": branch_claim_gate["claim_boundary"],
    }
    artifact["interpretation"] = (
        "This artifact supports a source-backed 2025 benchmark-compatibility claim and related sensitivity diagnostics. "
        "It does not resolve the muon g-2 anomaly or exclude alternate theory packages."
    )
    artifact["limitations"] = [
        "The live engine remains a compact benchmark-compatible term rather than a fully closed first-principles derivation.",
        "Historical local baselines remain diagnostic only and do not compete with the canonical 2025 source-locked package.",
        "Alternate-theory exclusion and broader downstream particle-consistency claims remain blocked.",
    ]
    artifact_path = topic_dir / "Result" / "artifacts" / "muon_g2_2025_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")
    return passes


if __name__ == "__main__":
    sys.exit(0 if run_research() else 1)
