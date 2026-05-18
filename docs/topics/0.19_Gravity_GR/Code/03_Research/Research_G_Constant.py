"""
Test: Gravitational Constant G
==============================
Topic 0.19 diagnostic verifier.

This script checks that the gravity engine's constant package matches the
topic-local CODATA 2018 working copy. It is a source-constant checkpoint, not a
derivation of G, Einstein equations, light bending, or singularity avoidance.
"""

import importlib.util
import json
import platform
import sys
from datetime import datetime, timezone
from hashlib import sha256
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
if ROOT is None:
    print("CRITICAL: UET docs root not found")
    sys.exit(1)

TOPIC_DIR = ROOT / "docs" / "topics" / "0.19_Gravity_GR"
DATA_PATH = TOPIC_DIR / "Data" / "03_Research" / "codata_2018_gravity.json"
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_19_gravity_gr_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"


def file_sha256(path):
    digest = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_engine():
    engine_file = TOPIC_DIR / "Code" / "01_Engine" / "Engine_Gravity_GR.py"
    spec = importlib.util.spec_from_file_location("Engine_Gravity_GR", str(engine_file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.UETGravityEngine


def load_codata():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def write_artifact(artifact):
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.19_Gravity_GR",
        "purpose": "Source evidence intake before upgrading claims across constants, weak-field gravity, equivalence, and GR-validation branches.",
        "source_targets": [
            {
                "name": "CODATA constant checkpoint package",
                "priority": "immediate",
                "status_hint": "source_backed_working_copy",
                "evidence_entries": [
                    "working_copy_json_path",
                    "doi_or_upstream_archive",
                    "observable_scope",
                    "unit_basis",
                    "hash_lock",
                    "benchmark_role",
                ],
            },
            {
                "name": "Weak-field validation package",
                "priority": "high",
                "status_hint": "formula_registry_only",
                "evidence_entries": [
                    "light_bending_dataset",
                    "perihelion_dataset",
                    "artifact_paths",
                    "observable_scope",
                    "unit_basis",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Equivalence-principle package",
                "priority": "high",
                "status_hint": "open_diagnostic_lane",
                "evidence_entries": [
                    "microscope_dataset_path",
                    "eta_uncertainty_field",
                    "comparison_artifact",
                    "observable_scope",
                    "unit_basis",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Short-range gravity package",
                "priority": "high",
                "status_hint": "secondary_comparator_lane",
                "evidence_entries": [
                    "eotwash_dataset_paths",
                    "source_normalization_note",
                    "artifact_path",
                    "observable_scope",
                    "unit_basis",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "General-relativity closure package",
                "priority": "medium",
                "status_hint": "blocked_theory_branch",
                "evidence_entries": [
                    "einstein_equation_derivation",
                    "singularity_artifact",
                    "cross_topic_dependency_map",
                    "observable_scope",
                    "artifact_path",
                    "upgrade_requirement",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself validate general relativity or quantum gravity.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "CODATA constant checkpoint package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Weak-field validation package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "light_bending_dataset",
                "perihelion_dataset",
                "artifact_paths",
                "unit_basis",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "Weak-field formulas are present in the registry, but there are no source-backed validation artifacts for light bending or perihelion.",
        },
        {
            "name": "Equivalence-principle package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 2,
            "fields_pending": 4,
            "pending_fields": [
                "eta_uncertainty_field",
                "comparison_artifact",
                "observable_scope",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "MICROSCOPE data exists locally, but the current lane does not yet compare engine outputs to the reported eta uncertainty.",
        },
        {
            "name": "Short-range gravity package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 3,
            "fields_pending": 3,
            "pending_fields": [
                "source_normalization_note",
                "artifact_path",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "Eot-Wash data exists, but there is no primary artifact that tests a declared UET parameter point against the exclusion curve.",
        },
        {
            "name": "General-relativity closure package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "einstein_equation_derivation",
                "singularity_artifact",
                "cross_topic_dependency_map",
                "observable_scope",
                "artifact_path",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "There is no source-backed derivation or validation package for GR closure, singularity avoidance, or quantum-gravity claims.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.19_Gravity_GR",
        "purpose": "Readiness matrix for source-evidence review across gravity and GR branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row has enough provenance structure for source review. It does not by itself upgrade GR or gravity claims.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.19_Gravity_GR",
        "purpose": "Claim gate for separate gravity and GR branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 2,
            "blocked_for_strong_claims": 4,
        },
        "branches": [
            {
                "branch": "CODATA constant checkpoint branch",
                "status": "accepted_source_backed_checkpoint_branch",
                "allowed_usage_now": "Accepted constant-package checkpoint branch against the CODATA working copy.",
                "blocker_to_stronger_claim": "Need derivation or broader physical validation before promoting beyond a source-constant checkpoint.",
            },
            {
                "branch": "Planck-unit definition branch",
                "status": "accepted_derived_constant_branch",
                "allowed_usage_now": "Accepted Planck-unit definition branch computed from the engine constant package.",
                "blocker_to_stronger_claim": "Planck units are derived from constants and do not independently validate gravity or GR.",
            },
            {
                "branch": "Weak-field validation branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Formula-registry and demo only.",
                "blocker_to_stronger_claim": "Need source-backed light-bending or perihelion artifacts.",
            },
            {
                "branch": "Equivalence-principle branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Open diagnostic only.",
                "blocker_to_stronger_claim": "Need eta comparison against MICROSCOPE uncertainty in a machine-readable artifact.",
            },
            {
                "branch": "Short-range gravity branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Secondary comparator only.",
                "blocker_to_stronger_claim": "Need artifacted comparison against the Eot-Wash exclusion curve.",
            },
            {
                "branch": "General-relativity and singularity-resolution claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need Einstein-equation, classical-test, and singularity-related artifacts beyond the current constant checkpoint.",
            },
        ],
        "claim_boundary": "This gate keeps the topic at source-constant checkpoint status, not general-relativity closure.",
    }


def build_gravity_claim_scope_gate(
    status: str,
    error_percent: float | None,
    threshold_percent: float,
    source_evidence_readiness_matrix: dict,
    branch_claim_gate: dict,
) -> dict:
    controller_status = "WARN" if status == "PASS" else "FAIL"
    return {
        "schema_version": "1.0",
        "topic": "0.19_Gravity_GR",
        "controller_status": controller_status,
        "controller_reason": (
            "The CODATA G checkpoint passed, but export remains warning-gated because weak-field, "
            "equivalence-principle, short-range, Einstein-equation, and singularity artifacts are missing."
            if status == "PASS"
            else "The CODATA G checkpoint failed the declared relative-error threshold."
        ),
        "claim_class": "C_source_constant_checkpoint_only",
        "allowed_claims_now": [
            {
                "claim": "The engine constant package matches the local CODATA G working copy under the declared threshold.",
                "status": status,
                "artifact_role": "source-constant checkpoint",
                "metric": "relative_error_percent",
                "metric_value": error_percent,
                "threshold": threshold_percent,
                "source_evidence_readiness": "codata_checkpoint_ready_for_review",
            },
            {
                "claim": "Planck units are internally derived from the engine constants.",
                "status": "DEFINITION_ONLY" if status == "PASS" else "BLOCKED",
                "artifact_role": "derived constant branch",
                "formula_role": "standard definitions, not independent gravity validation",
                "source_evidence_readiness": "inherits_constant_checkpoint",
            },
        ],
        "blocked_claims": [
            {
                "claim": "UET derives G from first principles.",
                "status": "BLOCKED",
                "blocking_reason": "The current verifier compares a copied/source constant against CODATA; it is not a derivation artifact.",
                "next_evidence_required": [
                    "derivation package",
                    "formula audit for independent G relation",
                    "uncertainty and dimensional analysis",
                ],
            },
            {
                "claim": "UET validates general relativity or Einstein field equations.",
                "status": "BLOCKED",
                "blocking_reason": "No Einstein-equation, classical-test, or metric-solution artifact is primary-gated.",
                "next_evidence_required": [
                    "light-bending artifact",
                    "perihelion-precession artifact",
                    "metric/EFE derivation or comparison package",
                ],
            },
            {
                "claim": "UET validates equivalence principle, short-range gravity, singularity avoidance, or quantum-gravity closure.",
                "status": "BLOCKED",
                "blocking_reason": "MICROSCOPE, Eot-Wash, singularity, and quantum-gravity branches lack primary artifacts.",
                "next_evidence_required": [
                    "MICROSCOPE eta comparison artifact",
                    "Eot-Wash exclusion-curve artifact",
                    "singularity and quantum-gravity benchmark package",
                ],
            },
        ],
        "blocked_export_phrases": [
            "G derived from first principles",
            "general relativity validated",
            "Einstein equations derived",
            "equivalence principle proved",
            "singularities resolved",
            "quantum gravity closed",
        ],
        "source_evidence_summary": source_evidence_readiness_matrix["summary"],
        "branch_claim_gate_summary": branch_claim_gate["summary"],
        "machine_readable_next_blockers": [
            "g_derivation_artifact_missing",
            "light_bending_artifact_missing",
            "perihelion_precession_artifact_missing",
            "microscope_eta_comparison_missing",
            "eotwash_short_range_artifact_missing",
            "einstein_equation_closure_missing",
            "singularity_artifact_missing",
        ],
        "claim_boundary": (
            "A PASS artifact supports only the CODATA constant checkpoint and derived Planck-unit definitions. "
            "It does not derive G, validate GR, prove equivalence, test short-range gravity, resolve singularities, "
            "or close quantum gravity."
        ),
    }


def test_gravitational_constant():
    print("=" * 60)
    print("Test: Gravitational Constant G")
    print("=" * 60)

    codata = load_codata()
    constants = codata["constants"]
    engine = load_engine()()
    planck = engine.get_planck_units()
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)

    g_codata = constants["G"]["value"]
    g_engine = planck["G"]
    rel_uncertainty_percent = constants["G"]["relative_uncertainty"] * 100
    threshold_percent = max(rel_uncertainty_percent, 0.0001)

    if np.isnan(g_engine) or g_engine == 0:
        error_percent = None
        status = "FAIL"
        failure_reason = "Engine returned NaN or zero for G."
    else:
        error_percent = abs(g_engine - g_codata) / g_codata * 100
        status = "PASS" if error_percent <= threshold_percent else "FAIL"
        failure_reason = None if status == "PASS" else "Engine G differs from CODATA checkpoint beyond threshold."

    print(f"CODATA 2018: G = {g_codata:.5e}")
    print(f"Engine value: G = {g_engine:.5e}")
    print(f"Error: {error_percent:.8f}%")
    print(f"Artifact status: {status}")
    gravity_claim_scope_gate = build_gravity_claim_scope_gate(
        status,
        error_percent,
        threshold_percent,
        source_evidence_readiness_matrix,
        branch_claim_gate,
    )

    artifact = {
        "schema_version": "1.1",
        "topic": "0.19_Gravity_GR",
        "status": status,
        "claim_class": "C - source-constant internal checkpoint only",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.19_Gravity_GR/Code/03_Research/Research_G_Constant.py",
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "inputs": [
            {
                "path": str(DATA_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_sha256(DATA_PATH),
                "source": codata.get("source"),
                "doi": codata.get("publication", {}).get("doi"),
            }
        ],
        "formula_ids": [
            "GR19-CONSTANT-PACKAGE",
            "GR19-PLANCK-UNITS",
            "GR19-G-CHECKPOINT",
        ],
        "threshold": {
            "max_relative_error_percent": threshold_percent,
            "codata_relative_uncertainty_percent": rel_uncertainty_percent,
        },
        "metrics": {
            "G_codata": g_codata,
            "G_engine": g_engine,
            "relative_error_percent": error_percent,
            "planck_length_m": planck["length"],
            "planck_time_s": planck["time"],
            "planck_mass_kg": planck["mass"],
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
            "blocked_claim_exports": len(gravity_claim_scope_gate["blocked_export_phrases"]),
        },
        "failure_reason": failure_reason,
        "limitations": [
            "This verifies that the engine constant package matches the CODATA working copy.",
            "It does not derive G from UET first principles.",
            "It does not validate Einstein field equations, light bending, perihelion precession, or singularity avoidance.",
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
    artifact["gravity_claim_scope_gate"] = gravity_claim_scope_gate
    artifact["interpretation"] = (
        "This artifact supports a source-constant checkpoint branch and a Planck-unit definition branch. "
        "It does not validate weak-field tests, the equivalence principle, or general relativity as a whole."
    )
    write_artifact(artifact)
    print(f"Artifact written: {ARTIFACT_PATH}")
    return status == "PASS"


if __name__ == "__main__":
    success = test_gravitational_constant()
    sys.exit(0 if success else 1)
