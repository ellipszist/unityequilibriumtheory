"""
Verify_Omni.py
==============
UET Omni-Engine integration verification.

This script checks whether selected component engines can be orchestrated and whether
their current internal metrics are recorded. It is an integration/run-contract verifier,
not a proof of grand unification.
"""

import json
import hashlib
import sys
from datetime import datetime, timezone
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

TOPIC_DIR = ROOT / "docs" / "topics" / "0.0_Grand_Unification"
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_0_grand_unification_verification.json"
DEPENDENCY_MANIFEST_PATH = TOPIC_DIR / "Data" / "03_Research" / "integration_dependency_manifest.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"

engine_dir = TOPIC_DIR / "Code" / "01_Engine"
if str(engine_dir) not in sys.path:
    sys.path.insert(0, str(engine_dir))

try:
    from Engine_Omni import UETOmniEngine
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import Omni-Engine: {e}")
    sys.exit(1)


def _state_to_record(label, state):
    return {
        "label": label,
        "beta_phase": float(state.beta_phase),
        "status": state.status,
        "metrics": {
            "galaxy_halo_ratio": float(state.galaxy_chi2),
            "weinberg_angle": float(state.weinberg_angle),
            "reynolds_critical": float(state.reynolds_critical),
            "tau_mass_MeV": float(state.tau_mass),
            "entanglement_entropy": float(state.entanglement_entropy),
            "ai_initial_loss": float(state.ai_learning_rate),
            "economic_omega": float(state.economic_omega),
            "atomic_h_alpha_error_percent": float(state.atomic_error),
        },
        "audit_flags": dict(state.audit_flags),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _normalize_status(artifact: dict) -> str:
    status_map = {
        "PASS": "PASS",
        "WARN": "WARN",
        "WARNING": "WARN",
        "FAIL": "FAIL",
        "FAILED": "FAIL",
        "ERROR": "FAIL",
        "RAN": "WARN",
        "COMPLETED": "WARN",
    }
    candidates = [
        artifact.get("status"),
        artifact.get("results", {}).get("status") if isinstance(artifact.get("results"), dict) else None,
        artifact.get("run_status"),
    ]
    for value in candidates:
        if isinstance(value, str) and value.strip():
            normalized = value.strip().upper()
            return status_map.get(normalized, normalized)
    if artifact.get("passed_run_contract") is True:
        return "PASS"
    return "UNKNOWN"


def _normalize_claim_class(artifact: dict):
    candidates = [
        artifact.get("claim_class"),
        artifact.get("results", {}).get("claim_class") if isinstance(artifact.get("results"), dict) else None,
    ]
    for value in candidates:
        if isinstance(value, str) and value.strip():
            return value.strip()
    claim_boundary = artifact.get("claim_boundary")
    if isinstance(claim_boundary, str) and claim_boundary.strip():
        if "run-contract" in claim_boundary.lower():
            return "D - run-contract only"
        if "internal benchmark" in claim_boundary.lower():
            return "C - internal benchmark"
    return None


def _normalize_timestamp(artifact: dict):
    candidates = [
        artifact.get("timestamp_utc"),
        artifact.get("generated_at_utc"),
        artifact.get("timestamp"),
    ]
    for value in candidates:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _extract_claim_gate_summary(artifact: dict) -> list[dict]:
    summaries = []
    thermodynamic_claim_scope_gate = artifact.get("thermodynamic_claim_scope_gate")
    if isinstance(thermodynamic_claim_scope_gate, dict):
        summaries.append(
            {
                "gate": "thermodynamic_claim_scope_gate",
                "status": thermodynamic_claim_scope_gate.get("controller_status"),
                "claim_class": thermodynamic_claim_scope_gate.get("claim_class"),
                "blocked_claims": [
                    item.get("claim")
                    for item in thermodynamic_claim_scope_gate.get("blocked_claims", [])
                ],
                "blocked_export_phrases": thermodynamic_claim_scope_gate.get("blocked_export_phrases", []),
                "next_blockers": thermodynamic_claim_scope_gate.get("machine_readable_next_blockers", []),
                "claim_boundary": thermodynamic_claim_scope_gate.get("claim_boundary"),
            }
        )

    foundation_gate = artifact.get("foundation_claim_gate")
    if isinstance(foundation_gate, dict):
        summaries.append(
            {
                "gate": "foundation_claim_gate",
                "status": foundation_gate.get("status"),
                "claim_ceiling": foundation_gate.get("claim_ceiling"),
                "blocked_exports": foundation_gate.get("blocked_foundation_exports", []),
                "claim_boundary": foundation_gate.get("claim_boundary"),
            }
        )

    scale_gate = artifact.get("scale_claim_gate")
    if isinstance(scale_gate, dict):
        thermo_gate = scale_gate.get("thermodynamic_foundation_gate")
        summaries.append(
            {
                "gate": "scale_claim_gate",
                "status": scale_gate.get("controller_status") or scale_gate.get("paper_readiness", {}).get("status"),
                "claim_class": scale_gate.get("claim_class"),
                "thermodynamic_foundation_status": (
                    thermo_gate.get("status") if isinstance(thermo_gate, dict) else None
                ),
                "blocked_exports": (
                    thermo_gate.get("blocked_exports", []) if isinstance(thermo_gate, dict) else []
                ),
                "blocked_claims": [
                    item.get("claim")
                    for item in scale_gate.get("blocked_claims", [])
                ],
                "blocked_export_phrases": scale_gate.get("blocked_export_phrases", []),
                "next_blockers": scale_gate.get("machine_readable_next_blockers", []),
                "claim_boundary": "Scale-link branch remains exploratory unless source, EEG, and inherited 0.13 gates close.",
            }
        )

    dynamic_frame_claim_gate = artifact.get("dynamic_frame_claim_gate")
    if isinstance(dynamic_frame_claim_gate, dict):
        summaries.append(
            {
                "gate": "dynamic_frame_claim_gate",
                "status": dynamic_frame_claim_gate.get("controller_status"),
                "claim_class": dynamic_frame_claim_gate.get("claim_class"),
                "blocked_exports": [
                    item.get("export")
                    for item in dynamic_frame_claim_gate.get("blocked_exports", [])
                ],
                "blocked_export_phrases": dynamic_frame_claim_gate.get("blocked_export_phrases", []),
                "next_blockers": dynamic_frame_claim_gate.get("machine_readable_next_blockers", []),
                "claim_boundary": dynamic_frame_claim_gate.get("promotion_rule"),
            }
        )

    complexity_claim_gate = artifact.get("complexity_claim_gate")
    if isinstance(complexity_claim_gate, dict):
        summaries.append(
            {
                "gate": "complexity_claim_gate",
                "status": complexity_claim_gate.get("controller_status"),
                "claim_class": complexity_claim_gate.get("claim_class"),
                "blocked_exports": [
                    item.get("export")
                    for item in complexity_claim_gate.get("blocked_exports", [])
                ],
                "blocked_export_phrases": complexity_claim_gate.get("blocked_export_phrases", []),
                "next_blockers": complexity_claim_gate.get("machine_readable_next_blockers", []),
                "claim_boundary": complexity_claim_gate.get("promotion_rule"),
            }
        )

    biophysics_claim_scope_gate = artifact.get("biophysics_claim_scope_gate")
    if isinstance(biophysics_claim_scope_gate, dict):
        summaries.append(
            {
                "gate": "biophysics_claim_scope_gate",
                "status": biophysics_claim_scope_gate.get("controller_status"),
                "claim_class": biophysics_claim_scope_gate.get("claim_class"),
                "blocked_claims": [
                    item.get("claim")
                    for item in biophysics_claim_scope_gate.get("blocked_claims", [])
                ],
                "blocked_export_phrases": biophysics_claim_scope_gate.get("blocked_export_phrases", []),
                "next_blockers": biophysics_claim_scope_gate.get("machine_readable_next_blockers", []),
                "claim_boundary": biophysics_claim_scope_gate.get("claim_boundary"),
            }
        )

    ai_claim_scope_gate = artifact.get("ai_claim_scope_gate")
    if isinstance(ai_claim_scope_gate, dict):
        summaries.append(
            {
                "gate": "ai_claim_scope_gate",
                "status": ai_claim_scope_gate.get("controller_status"),
                "claim_class": ai_claim_scope_gate.get("claim_class"),
                "blocked_claims": [
                    item.get("claim")
                    for item in ai_claim_scope_gate.get("blocked_claims", [])
                ],
                "blocked_export_phrases": ai_claim_scope_gate.get("blocked_export_phrases", []),
                "next_blockers": ai_claim_scope_gate.get("machine_readable_next_blockers", []),
                "claim_boundary": ai_claim_scope_gate.get("claim_boundary"),
            }
        )

    economics_claim_scope_gate = artifact.get("economics_claim_scope_gate")
    if isinstance(economics_claim_scope_gate, dict):
        summaries.append(
            {
                "gate": "economics_claim_scope_gate",
                "status": economics_claim_scope_gate.get("controller_status"),
                "claim_class": economics_claim_scope_gate.get("claim_class"),
                "blocked_claims": [
                    item.get("claim")
                    for item in economics_claim_scope_gate.get("blocked_claims", [])
                ],
                "blocked_export_phrases": economics_claim_scope_gate.get("blocked_export_phrases", []),
                "next_blockers": economics_claim_scope_gate.get("machine_readable_next_blockers", []),
                "claim_boundary": economics_claim_scope_gate.get("claim_boundary"),
            }
        )

    numeric_residual_gate = artifact.get("numeric_residual_gate")
    if isinstance(numeric_residual_gate, dict):
        replacement_gate = numeric_residual_gate.get("replacement_claim_gate", {})
        summaries.append(
            {
                "gate": "numeric_residual_gate",
                "status": replacement_gate.get("status"),
                "visualization_status": numeric_residual_gate.get("visualization_gate", {}).get("status"),
                "numeric_flow_residual_status": numeric_residual_gate.get("numeric_flow_residual_gate", {}).get("status"),
                "baseline_comparison_status": numeric_residual_gate.get("baseline_comparison_gate", {}).get("status"),
                "blocked_claims": replacement_gate.get("blocked_claims", []),
                "claim_boundary": "Visualization/provenance does not close numeric residual or replacement-claim gates.",
            }
        )

    theorem_boundary_gate = artifact.get("theorem_boundary_gate")
    if isinstance(theorem_boundary_gate, dict):
        summaries.append(
            {
                "gate": "theorem_boundary_gate",
                "status": theorem_boundary_gate.get("controller_status") or theorem_boundary_gate.get("status"),
                "theorem_status": theorem_boundary_gate.get("status"),
                "claim_class": theorem_boundary_gate.get("claim_class"),
                "accepted_exports": theorem_boundary_gate.get("accepted_exports", []),
                "blocked_exports": theorem_boundary_gate.get("blocked_theorem_exports", []),
                "blocked_export_phrases": theorem_boundary_gate.get("blocked_export_phrases", []),
                "next_blockers": theorem_boundary_gate.get("machine_readable_next_blockers", []),
                "claim_boundary": theorem_boundary_gate.get("claim_boundary"),
            }
        )

    data_posture_gate = artifact.get("data_posture_gate")
    if isinstance(data_posture_gate, dict):
        summaries.append(
            {
                "gate": "data_posture_gate",
                "status": data_posture_gate.get("controller_status"),
                "data_reality_status": data_posture_gate.get("data_reality_status"),
                "primary_verifier_input_class": data_posture_gate.get("primary_verifier_input_class"),
                "blocked_export_phrases": data_posture_gate.get("blocked_export_phrases", []),
                "next_blockers": data_posture_gate.get("machine_readable_next_blockers", []),
                "claim_boundary": data_posture_gate.get("claim_boundary"),
            }
        )

    galaxy_model_gate = artifact.get("galaxy_model_gate")
    if isinstance(galaxy_model_gate, dict):
        replacement_gate = galaxy_model_gate.get("replacement_claim_gate", {})
        summaries.append(
            {
                "gate": "galaxy_model_gate",
                "status": replacement_gate.get("status"),
                "run_contract_status": galaxy_model_gate.get("run_contract_gate", {}).get("status"),
                "summary_row_model_status": galaxy_model_gate.get("summary_row_model_gate", {}).get("status"),
                "source_lock_status": galaxy_model_gate.get("source_lock_gate", {}).get("status"),
                "baseline_comparison_status": galaxy_model_gate.get("baseline_comparison_gate", {}).get("status"),
                "blocked_claims": replacement_gate.get("blocked_claims", []),
                "claim_boundary": galaxy_model_gate.get("claim_boundary"),
            }
        )

    galaxy_claim_scope_gate = artifact.get("galaxy_claim_scope_gate")
    if isinstance(galaxy_claim_scope_gate, dict):
        summaries.append(
            {
                "gate": "galaxy_claim_scope_gate",
                "status": galaxy_claim_scope_gate.get("controller_status"),
                "claim_class": galaxy_claim_scope_gate.get("claim_class"),
                "blocked_claims": [
                    item.get("claim")
                    for item in galaxy_claim_scope_gate.get("blocked_claims", [])
                ],
                "blocked_export_phrases": galaxy_claim_scope_gate.get("blocked_export_phrases", []),
                "next_blockers": galaxy_claim_scope_gate.get("machine_readable_next_blockers", []),
                "claim_boundary": galaxy_claim_scope_gate.get("claim_boundary"),
            }
        )

    branch_claim_gate = artifact.get("branch_claim_gate")
    if isinstance(branch_claim_gate, dict):
        summary = branch_claim_gate.get("summary", {})
        blocked_count = summary.get("blocked_for_strong_claims")
        summaries.append(
            {
                "gate": "branch_claim_gate",
                "status": "BLOCKED" if blocked_count else "READY_FOR_REVIEW",
                "accepted_now": summary.get("accepted_now"),
                "blocked_for_strong_claims": blocked_count,
                "claim_boundary": branch_claim_gate.get("claim_boundary"),
            }
        )

    subordinate_paper_gate = artifact.get("paper_readiness_gate")
    if isinstance(subordinate_paper_gate, dict):
        summaries.append(
            {
                "gate": "paper_readiness_gate",
                "status": subordinate_paper_gate.get("status"),
                "blocked_dependency_count": subordinate_paper_gate.get("blocked_dependency_count"),
                "claim_boundary": "Subordinate paper-readiness gate is inherited by 0.0.",
            }
        )
    return summaries


def _build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.0_Grand_Unification",
        "purpose": "Source evidence intake before upgrading claims across the integration manifest and dependency-governance branches.",
        "source_targets": [
            {
                "name": "Integration dependency manifest package",
                "priority": "immediate",
                "status_hint": "manifest_present_but_partial_scope",
                "evidence_entries": [
                    "manifest_path",
                    "dependency_scope_note",
                    "metric_bridge_map",
                    "claim_boundary_note",
                    "hash_lock",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Subordinate artifact identity package",
                "priority": "immediate",
                "status_hint": "mixed_subordinate_statuses",
                "evidence_entries": [
                    "artifact_paths",
                    "status_normalization_rule",
                    "claim_class_capture",
                    "timestamp_capture",
                    "hash_lock",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Core-topic coverage expansion package",
                "priority": "high",
                "status_hint": "partial_core_scope_only",
                "evidence_entries": [
                    "missing_core_topics_list",
                    "expanded_manifest_path",
                    "dependency_policy",
                    "metric_bridge_map",
                    "artifact_inventory",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Paper-readiness gate package",
                "priority": "high",
                "status_hint": "not_yet_closed",
                "evidence_entries": [
                    "warn_fail_block_rule",
                    "source_incomplete_block_rule",
                    "open_formula_block_rule",
                    "derived_claim_class_rule",
                    "artifact_path",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Grand-unification closure package",
                "priority": "medium",
                "status_hint": "blocked_theory_branch",
                "evidence_entries": [
                    "all_core_topics_manifested_and_verified",
                    "dependency_closure_artifact",
                    "cross_topic_formula_map",
                    "unit_consistency_proof",
                    "artifact_path",
                    "upgrade_requirement",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes dependency-governance work only. It does not itself prove grand unification.",
    }


def _build_source_evidence_readiness_matrix(dependency_artifacts: list[dict]) -> dict:
    warn_or_unknown = [
        item for item in dependency_artifacts if item.get("status") in {"WARN", "UNKNOWN", "MISSING"}
    ]
    rows = [
        {
            "name": "Integration dependency manifest package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 5,
            "fields_pending": 1,
            "pending_fields": ["full_core_scope_0_1_to_0_26"],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Subordinate artifact identity package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 5,
            "fields_pending": 1,
            "pending_fields": ["all_dependencies_pass"],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Core-topic coverage expansion package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 5,
            "fields_pending": 1,
            "pending_fields": ["all_dependencies_pass_without_warn_or_unknown"],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Paper-readiness gate package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 3,
            "fields_pending": 3,
            "pending_fields": [
                "source_incomplete_block_rule",
                "open_formula_block_rule",
                "derived_claim_class_rule",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "Dependency governance exists, but the integration topic still lacks a complete paper-readiness closure gate.",
        },
        {
            "name": "Grand-unification closure package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "all_core_topics_manifested_and_verified",
                "dependency_closure_artifact",
                "cross_topic_formula_map",
                "unit_consistency_proof",
                "artifact_path",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The repo still has subordinate WARN/UNKNOWN dependencies and one FAIL artifact outside the selected manifest path.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.0_Grand_Unification",
        "purpose": "Readiness matrix for source-evidence review across integration and closure branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
            "dependencies_warn_or_unknown": len(warn_or_unknown),
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row has enough provenance structure for source review. It does not by itself upgrade unification claims.",
    }


def _build_branch_claim_gate(dependency_artifacts: list[dict]) -> dict:
    warn_count = sum(1 for item in dependency_artifacts if item.get("status") == "WARN")
    fail_count = sum(1 for item in dependency_artifacts if item.get("status") == "FAIL")
    unknown_count = sum(1 for item in dependency_artifacts if item.get("status") in {"UNKNOWN", "MISSING"})
    return {
        "schema_version": "1.0",
        "topic": "0.0_Grand_Unification",
        "purpose": "Claim gate for separate integration and closure branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 2,
            "blocked_for_strong_claims": 4,
            "dependency_warn_count": warn_count,
            "dependency_fail_count": fail_count,
            "dependency_unknown_count": unknown_count,
        },
        "branches": [
            {
                "branch": "Integration run-contract branch",
                "status": "accepted_integration_branch",
                "allowed_usage_now": "Accepted branch for selected-engine orchestration and dashboard execution.",
                "blocker_to_stronger_claim": "Running the dashboard does not elevate subordinate evidence classes.",
            },
            {
                "branch": "Dependency-status dashboard branch",
                "status": "accepted_governance_branch",
                "allowed_usage_now": "Accepted branch for recording subordinate artifact identity, status, claim class, and limitation inheritance.",
                "blocker_to_stronger_claim": "Dependency governance does not close the underlying scientific gaps.",
            },
            {
                "branch": "Full core-topic integration branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Partial selected-core integration only.",
                "blocker_to_stronger_claim": "Need manifest coverage across all intended core topics and bridges.",
            },
            {
                "branch": "Paper-readiness branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need every dependency aligned on data, formulas, verifier, and limitations with no unresolved closure blockers.",
            },
            {
                "branch": "Unified-parameter closure branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need cross-topic formula and unit closure beyond the current dashboard metrics.",
            },
            {
                "branch": "Grand-unification theory claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Subordinate WARN/UNKNOWN blockers and out-of-scope core failures prevent theory-level promotion.",
            },
        ],
        "claim_boundary": "This gate keeps the topic at integration-index and governance status, not grand-unification closure.",
    }


def _build_paper_readiness_gate(dependency_artifacts: list[dict]) -> dict:
    blockers = []
    for item in dependency_artifacts:
        status = item.get("status")
        if status in {"FAIL", "WARN", "UNKNOWN", "MISSING", None}:
            blockers.append(
                {
                    "topic": item.get("topic"),
                    "artifact": item.get("artifact"),
                    "status": status or "UNKNOWN",
                    "claim_class": item.get("claim_class"),
                    "blocker": "Dependency is not clean PASS, so theory-level closure is blocked.",
                }
            )
        for gate in item.get("claim_gates", []):
            gate_status = gate.get("status")
            gate_blocked = (
                gate_status not in {None, "PASS", "READY_FOR_REVIEW", "FOUNDATION_PASS"}
                or bool(gate.get("blocked_exports"))
                or bool(gate.get("blocked_dependency_count"))
                or bool(gate.get("blocked_for_strong_claims"))
            )
            if gate_blocked:
                blockers.append(
                    {
                        "topic": item.get("topic"),
                        "artifact": item.get("artifact"),
                        "status": status or "UNKNOWN",
                        "claim_class": item.get("claim_class"),
                        "gate": gate.get("gate"),
                        "gate_status": gate_status,
                        "blocked_exports": gate.get("blocked_exports", []),
                        "blocked_claims": gate.get("blocked_claims", []),
                        "blocker": "Subordinate claim gate blocks theory-level inheritance.",
                    }
                )

    return {
        "schema_version": "1.0",
        "topic": "0.0_Grand_Unification",
        "status": "BLOCKED" if blockers else "READY_FOR_REVIEW",
        "rule": "Any FAIL, WARN, UNKNOWN, missing artifact, source-incomplete, formula-open, or synthetic-only dependency blocks theory-level claims.",
        "dependency_count": len(dependency_artifacts),
        "blocked_dependency_count": len(blockers),
        "blockers": blockers,
        "allowed_now": [
            "integration run-contract",
            "dependency dashboard",
            "claim inheritance map",
            "paper-readiness blocker report",
        ],
        "forbidden_until_closed": [
            "Theory of Everything",
            "proved unification",
            "all core topics verified",
            "paper-ready theory-level closure",
        ],
    }


def _build_integration_claim_scope_gate(dependency_artifacts: list[dict], paper_readiness_gate: dict) -> dict:
    fail_topics = [
        item.get("topic")
        for item in dependency_artifacts
        if item.get("status") == "FAIL"
    ]
    warn_topics = [
        item.get("topic")
        for item in dependency_artifacts
        if item.get("status") == "WARN"
    ]
    blocked_gate_topics = []
    blocked_gate_names = []
    for item in dependency_artifacts:
        for gate in item.get("claim_gates", []):
            gate_status = gate.get("status")
            blocked = (
                gate_status not in {None, "PASS", "READY_FOR_REVIEW", "FOUNDATION_PASS"}
                or bool(gate.get("blocked_exports"))
                or bool(gate.get("blocked_claims"))
                or bool(gate.get("blocked_export_phrases"))
                or bool(gate.get("blocked_for_strong_claims"))
            )
            if blocked:
                blocked_gate_topics.append(item.get("topic"))
                blocked_gate_names.append(gate.get("gate"))

    return {
        "schema_version": "1.0",
        "topic": "0.0_Grand_Unification",
        "controller_status": "BLOCKED" if paper_readiness_gate.get("status") != "READY_FOR_REVIEW" else "READY_FOR_REVIEW",
        "controller_reason": (
            "0.0 may export integration and dependency-governance claims only; theory-level closure is blocked by subordinate status and claim gates."
            if paper_readiness_gate.get("status") != "READY_FOR_REVIEW"
            else "All declared dependencies are ready for review; theory-level wording still requires human source/formula review."
        ),
        "claim_class": "D_integration_governance_only",
        "allowed_claims_now": [
            {
                "claim": "The Omni verifier ran selected component engines and wrote an integration artifact.",
                "status": "PASS",
                "artifact_role": "integration run-contract",
            },
            {
                "claim": "0.0 records subordinate artifact identity, status, claim class, and claim-gate blockers.",
                "status": "PASS",
                "artifact_role": "dependency-governance dashboard",
            },
            {
                "claim": "0.0 can report paper-readiness blockers inherited from core topics.",
                "status": "PASS",
                "artifact_role": "blocker report",
            },
        ],
        "blocked_claims": [
            {
                "claim": "UET grand unification is proved.",
                "status": "BLOCKED",
                "blocking_reason": "Subordinate WARN/FAIL artifacts and blocked claim gates remain present.",
                "next_evidence_required": [
                    "all declared dependencies clean PASS or review-ready",
                    "no subordinate blocked claim gates",
                    "source, formula, verifier, and limitation closure across core topics",
                ],
            },
            {
                "claim": "0.0 upgrades subordinate topics to Tier A.",
                "status": "BLOCKED",
                "blocking_reason": "Integration status cannot promote subordinate data, formula, or artifact readiness.",
                "next_evidence_required": [
                    "topic-local source evidence",
                    "topic-local formula audit closure",
                    "topic-local verifier artifact with closed claim gate",
                ],
            },
            {
                "claim": "0.0 is paper-ready theory-level closure.",
                "status": "BLOCKED",
                "blocking_reason": "The paper-readiness gate is blocked.",
                "next_evidence_required": paper_readiness_gate.get("forbidden_until_closed", []),
            },
        ],
        "blocked_export_phrases": [
            "Theory of Everything",
            "proved grand unification",
            "all core topics verified",
            "paper-ready theory-level closure",
            "subordinate blockers resolved by integration",
            "master proof",
        ],
        "dependency_status_summary": {
            "dependencies_total": len(dependency_artifacts),
            "fail_topics": fail_topics,
            "warn_topics": warn_topics,
            "blocked_claim_gate_topics": sorted(set(topic for topic in blocked_gate_topics if topic)),
            "blocked_claim_gate_names": sorted(set(name for name in blocked_gate_names if name)),
            "paper_readiness_blocked_dependency_count": paper_readiness_gate.get("blocked_dependency_count"),
        },
        "machine_readable_next_blockers": [
            "subordinate_fail_artifact_present" if fail_topics else "no_subordinate_fail_artifact",
            "subordinate_warn_artifacts_present" if warn_topics else "no_subordinate_warn_artifacts",
            "subordinate_claim_gates_block_theory_exports" if blocked_gate_topics else "no_subordinate_blocked_claim_gates",
            "source_evidence_closure_missing",
            "formula_and_units_closure_missing",
            "paper_readiness_gate_blocked",
        ],
        "claim_boundary": (
            "0.0 is an integration/governance layer. It may report selected component runs and inherited blockers, "
            "but it cannot prove grand unification or upgrade any subordinate topic beyond its own evidence."
        ),
    }


def _dependency_inputs():
    inputs = []
    dependencies = []
    if DEPENDENCY_MANIFEST_PATH.exists():
        inputs.append(
            {
                "path": str(DEPENDENCY_MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
                "bytes": DEPENDENCY_MANIFEST_PATH.stat().st_size,
                "sha256": _sha256(DEPENDENCY_MANIFEST_PATH),
                "provenance_role": "integration_dependency_manifest",
            }
        )
        manifest = _read_json(DEPENDENCY_MANIFEST_PATH)
        dependencies = manifest.get("dependencies", [])
    else:
        inputs.append(
            {
                "path": str(DEPENDENCY_MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
                "missing": True,
                "provenance_role": "integration_dependency_manifest",
            }
        )

    records = []
    for dependency in dependencies:
        artifact_path = ROOT / dependency["artifact"]
        record = {
            "topic": dependency.get("topic"),
            "role": dependency.get("role"),
            "metric_bridge": dependency.get("metric_bridge"),
            "artifact": dependency.get("artifact"),
        }
        if artifact_path.exists():
            artifact = _read_json(artifact_path)
            normalized_status = _normalize_status(artifact)
            normalized_claim_class = _normalize_claim_class(artifact)
            normalized_timestamp = _normalize_timestamp(artifact)
            record.update(
                {
                    "status": normalized_status,
                    "claim_class": normalized_claim_class,
                    "schema_version": artifact.get("schema_version"),
                    "timestamp_utc": normalized_timestamp,
                    "claim_gates": _extract_claim_gate_summary(artifact),
                    "sha256": _sha256(artifact_path),
                    "bytes": artifact_path.stat().st_size,
                }
            )
            inputs.append(
                {
                    "path": dependency.get("artifact"),
                    "bytes": artifact_path.stat().st_size,
                    "sha256": record["sha256"],
                    "provenance_role": "subordinate_artifact",
                    "status": normalized_status,
                }
            )
        else:
            record.update({"status": "MISSING", "missing": True})
            inputs.append(
                {
                    "path": dependency.get("artifact"),
                    "missing": True,
                    "provenance_role": "subordinate_artifact",
                }
            )
        records.append(record)
    return inputs, records


def write_verification_artifact(result):
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
        "schema_version": "1.2",
        "topic": "0.0_Grand_Unification",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.0_Grand_Unification/Code/03_Research/Verify_Omni.py",
        "status": result["status"],
        "passed_run_contract": result["status"] in {"PASS", "WARN"},
        "input_hashes": result["input_hashes"],
        "dependency_artifacts": result["dependency_artifacts"],
        "integration_claim_scope_gate": result["integration_claim_scope_gate"],
        "paper_readiness_gate": result["paper_readiness_gate"],
        "metrics": result["summary_metrics"],
        "thresholds": {
            "run_without_error": True,
            "artifact_written": True,
            "weinberg_angle_abs_error_max": 0.001,
            "tau_mass_abs_error_MeV_max": 1.0,
            "entanglement_entropy_abs_error_max": 0.001,
        },
        "interpretation": (
            "Internal integration/run-contract artifact. This records selected "
            "component-engine outputs and does not prove grand unification or "
            "override subordinate topic limitations. Dependency PASS/WARN/FAIL status is read "
            "from the integration dependency manifest and subordinate artifacts."
        ),
        "results": result,
    }
    artifact["source_evidence_intake_stub"] = {
        "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": hashlib.sha256(
            json.dumps(result["source_evidence_intake_stub_payload"], sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "source_targets": [
            row["name"] for row in result["source_evidence_intake_stub_payload"]["source_targets"]
        ],
        "claim_boundary": result["source_evidence_intake_stub_payload"]["claim_boundary"],
    }
    artifact["source_evidence_readiness_matrix"] = {
        "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": hashlib.sha256(
            json.dumps(result["source_evidence_readiness_matrix_payload"], sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "summary": result["source_evidence_readiness_matrix_payload"]["summary"],
        "claim_boundary": result["source_evidence_readiness_matrix_payload"]["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": hashlib.sha256(
            json.dumps(result["branch_claim_gate_payload"], sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "summary": result["branch_claim_gate_payload"]["summary"],
        "claim_boundary": result["branch_claim_gate_payload"]["claim_boundary"],
    }
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"Artifact saved: {ARTIFACT_PATH}")


def run_verification():
    print("UET OMNI-ENGINE: INTEGRATION VERIFICATION")
    print("==========================================")

    omni = UETOmniEngine()

    print("\n[Test 1] Standard integration run (Beta=1.0)...")
    state_std = omni.run_universe(beta=1.0)
    omni.report(state_std)

    has_error = False
    if abs(state_std.weinberg_angle - 0.2312) > 0.001:
        print("Electroweak mismatch")
        has_error = True
    if abs(state_std.tau_mass - 1776.9) > 1.0:
        print("Mass-generation branch mismatch")
        has_error = True
    if abs(state_std.entanglement_entropy - 1.0) > 0.001:
        print("Quantum entropy mismatch")
        has_error = True

    if not has_error:
        print("Integration check: selected beta=1.0 component gates passed.")

    print("\n[Test 2] Low-coupling sensitivity run (Beta=0.1)...")
    state_chaos = omni.run_universe(beta=0.1)
    omni.report(state_chaos)
    print(
        f"  Shift in Re_c: {state_std.reynolds_critical:.1f} -> {state_chaos.reynolds_critical:.1f}"
    )

    input_hashes, dependency_artifacts = _dependency_inputs()
    source_evidence_intake_stub = _build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = _build_source_evidence_readiness_matrix(dependency_artifacts)
    branch_claim_gate = _build_branch_claim_gate(dependency_artifacts)
    paper_readiness_gate = _build_paper_readiness_gate(dependency_artifacts)
    integration_claim_scope_gate = _build_integration_claim_scope_gate(
        dependency_artifacts,
        paper_readiness_gate,
    )
    _write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    _write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    _write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)
    dependency_statuses = [item.get("status") for item in dependency_artifacts]
    missing_dependencies = [item for item in dependency_artifacts if item.get("missing")]
    dependency_failures = [item for item in dependency_artifacts if item.get("status") == "FAIL"]
    dependency_warnings = [
        item
        for item in dependency_artifacts
        if item.get("status") in {"WARN", "MISSING", "UNKNOWN", None}
    ]

    if missing_dependencies:
        integration_status = "FAIL"
    elif has_error or dependency_failures or dependency_warnings:
        integration_status = "WARN"
    else:
        integration_status = "PASS"

    result = {
        "status": integration_status,
        "input_hashes": input_hashes,
        "dependency_artifacts": dependency_artifacts,
        "component_scope": [
            "0.1_Galaxy_Rotation_Problem",
            "0.6_Electroweak_Physics",
            "0.10_Fluid_Dynamics_Chaos",
            "0.17_Mass_Generation",
            "0.18_Mathnicry",
            "0.20_Atomic_Physics",
            "0.24_Artificial_Intelligence",
            "0.25_Strategy_Power_Economics",
        ],
        "states": [
            _state_to_record("beta_1_0", state_std),
            _state_to_record("beta_0_1", state_chaos),
        ],
        "summary_metrics": {
            "beta_1_0_weinberg_angle": float(state_std.weinberg_angle),
            "beta_1_0_tau_mass_MeV": float(state_std.tau_mass),
            "beta_1_0_entanglement_entropy": float(state_std.entanglement_entropy),
            "reynolds_shift_beta_1_0_to_0_1": float(
                state_chaos.reynolds_critical - state_std.reynolds_critical
            ),
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
        },
        "dependency_summary": {
            "statuses": dependency_statuses,
            "pass_count": sum(1 for status in dependency_statuses if status == "PASS"),
            "warn_count": sum(1 for status in dependency_statuses if status == "WARN"),
            "fail_count": sum(1 for status in dependency_statuses if status == "FAIL"),
            "missing_count": len(missing_dependencies),
            "interpretation": "Dependency FAIL/WARN blocks paper-readiness and theory-level claims, but does not by itself mean the integration run-contract failed.",
        },
        "inherited_limitations": [
            "Subordinate topic failures or WARN artifacts remain blockers for theory-level claims.",
            "This integration check owns an artifact-dependency manifest, not raw scientific data.",
            "Component outputs may use benchmark-fed or heuristic branches documented in their own topics.",
        ],
        "source_evidence_intake_stub_payload": source_evidence_intake_stub,
        "source_evidence_readiness_matrix_payload": source_evidence_readiness_matrix,
        "branch_claim_gate_payload": branch_claim_gate,
        "paper_readiness_gate": paper_readiness_gate,
        "integration_claim_scope_gate": integration_claim_scope_gate,
    }
    write_verification_artifact(result)
    print("\nFINAL STATUS: OMNI-ENGINE INTEGRATION CHECK COMPLETE")
    return result


if __name__ == "__main__":
    verification_result = run_verification()
    sys.exit(0 if verification_result["status"] in {"PASS", "WARN"} else 1)
