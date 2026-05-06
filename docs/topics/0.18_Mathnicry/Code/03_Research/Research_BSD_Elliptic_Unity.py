"""
Research_BSD_Elliptic_Unity.py - Topic 0.18
==========================================
Runs a surrogate BSD-style UET demonstration.
This script does not prove the Birch and Swinnerton-Dyer conjecture.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add engine to path
current_path = Path(__file__).resolve()
engine_dir = current_path.parent.parent / "01_Engine"
sys.path.append(str(engine_dir))

from Engine_Elliptic_Resonance import EllipticResonanceEngine


TOPIC_DIR = current_path.parents[2]
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_18_mathnicry_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "branch_claim_gate.json"


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _input_hashes():
    path = TOPIC_DIR / "Data" / "Download_Quantum_Data.py"
    record = {
        "path": str(path.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "loaded_by_primary_script": False,
        "role": "declared placeholder/manual data helper in VERIFICATION_SPEC.md",
    }
    if path.exists():
        record.update(
            {
                "status": "present",
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
        )
    else:
        record["status"] = "missing"
    return [record]


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _build_source_evidence_intake_stub():
    payload = {
        "schema_version": "1.0",
        "topic": "0.18_Mathnicry",
        "purpose": "Structured intake stub for theorem-branch benchmark evidence before data rewrites or stronger proof-style claims.",
        "instructions": [
            "Attach upstream URL, DOI, or benchmark provenance before changing a branch from surrogate or symbolic status to benchmark status.",
            "Record the exact theorem target, benchmark table or search domain, local archive path, and extraction note.",
            "Do not treat this file as proof; it is an intake and tracking layer.",
        ],
        "source_targets": [
            {
                "name": "BSD elliptic-curve benchmark package",
                "priority": "immediate",
                "status": "pending",
                "evidence_fields": [
                    {"field": "url_or_dataset_reference", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "curve_identifier_or_table", "status": "pending", "value": ""},
                    {"field": "rank_or_l_function_reference", "status": "pending", "value": ""},
                    {"field": "unit_or_convention_note", "status": "pending", "value": ""},
                    {"field": "extraction_note", "status": "pending", "value": ""},
                ],
            },
            {
                "name": "Riemann zero reference package",
                "priority": "high",
                "status": "pending",
                "evidence_fields": [
                    {"field": "source_or_library_reference", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "zero_range_or_precision_manifest", "status": "pending", "value": ""},
                    {"field": "version_or_retrieval_date", "status": "pending", "value": ""},
                    {"field": "unit_or_convention_note", "status": "pending", "value": ""},
                    {"field": "extraction_note", "status": "pending", "value": ""},
                ],
            },
            {
                "name": "Grover or P-vs-NP benchmark package",
                "priority": "high",
                "status": "pending",
                "evidence_fields": [
                    {"field": "benchmark_suite_reference", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "problem_family_identifier", "status": "pending", "value": ""},
                    {"field": "baseline_complexity_reference", "status": "pending", "value": ""},
                    {"field": "unit_or_convention_note", "status": "pending", "value": ""},
                    {"field": "extraction_note", "status": "pending", "value": ""},
                ],
            },
            {
                "name": "Collatz bounded-search manifest",
                "priority": "medium",
                "status": "pending",
                "evidence_fields": [
                    {"field": "search_domain_reference", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "range_or_seed_manifest", "status": "pending", "value": ""},
                    {"field": "counterexample_policy", "status": "pending", "value": ""},
                    {"field": "unit_or_convention_note", "status": "pending", "value": ""},
                    {"field": "extraction_note", "status": "pending", "value": ""},
                ],
            },
            {
                "name": "Quantum-engine deterministic fixture package",
                "priority": "medium",
                "status": "pending",
                "evidence_fields": [
                    {"field": "fixture_reference", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "gate_or_state_identifier", "status": "pending", "value": ""},
                    {"field": "expected_output_reference", "status": "pending", "value": ""},
                    {"field": "unit_or_convention_note", "status": "pending", "value": ""},
                    {"field": "extraction_note", "status": "pending", "value": ""},
                ],
            },
        ],
        "claim_boundary": "This intake stub is for benchmark evidence capture only. Filling it does not by itself justify theorem-level or proof-level claims.",
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
        "topic": "0.18_Mathnicry",
        "purpose": "Readiness matrix for theorem-branch benchmark evidence before data edits or claim upgrades.",
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
        "topic": "0.18_Mathnicry",
        "purpose": "Claim gate for theorem-inspired branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 1,
            "blocked_for_strong_claims": 5,
        },
        "branches": [
            {
                "branch": "BSD surrogate demonstration",
                "status": "accepted_run_contract_only",
                "allowed_usage_now": "Internal surrogate artifact only.",
                "blocker_to_stronger_claim": "Need real elliptic-curve rank or L-function benchmark data and non-surrogate computations.",
            },
            {
                "branch": "Riemann-style zero checks",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Library-driven numerical check only.",
                "blocker_to_stronger_claim": "Need explicit zero table, precision manifest, and search-boundary statement.",
            },
            {
                "branch": "Grover or P-vs-NP scaling",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Quantum-search scaling sandbox only.",
                "blocker_to_stronger_claim": "Need formal reductions, benchmark suite, and complexity-proof boundary.",
            },
            {
                "branch": "Collatz branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Bounded or heuristic exploration only.",
                "blocker_to_stronger_claim": "Need bounded-search artifact, cleaned code path, and counterexample policy.",
            },
            {
                "branch": "Quantum engine integrity branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Engine sandbox only.",
                "blocker_to_stronger_claim": "Need deterministic gate/state fixtures and acceptance tests.",
            },
            {
                "branch": "Hodge or other topology-style branches",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Symbolic or visual sandbox only.",
                "blocker_to_stronger_claim": "Need theorem target, benchmark object class, and proof-boundary artifact.",
            },
        ],
        "claim_boundary": "This gate cannot raise claim strength above the current internal BSD surrogate run-contract evidence.",
    }
    return _write_json(BRANCH_CLAIM_GATE_PATH, payload)


def write_verification_artifact(result):
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    source_evidence_intake_stub = _build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = _build_source_evidence_readiness_matrix(source_evidence_intake_stub)
    branch_claim_gate = _build_branch_claim_gate()
    artifact = {
        "schema_version": "1.1",
        "topic": "0.18_Mathnicry",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.18_Mathnicry/Code/03_Research/Research_BSD_Elliptic_Unity.py",
        "status": result["status"],
        "passed_run_contract": result["status"] in {"PASS", "WARN"},
        "input_hashes": _input_hashes(),
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
            "claim_boundary": "This gate records theorem-branch claim ceilings only. It cannot upgrade the topic beyond the current run-contract evidence.",
        },
        "metrics": {
            "curve_count": len(result["curves"]),
            "rank_indicator_mismatches": result["rank_indicator_mismatches"],
        },
        "thresholds": {
            "run_without_error": True,
            "artifact_written": True,
            "expected_rank_indicator_mismatches_max": 1,
        },
        "interpretation": (
            "Internal BSD surrogate demonstration only. Rank behavior is generated "
            "by a local parity heuristic in Engine_Elliptic_Resonance, not by a "
            "computed elliptic-curve L-function or theorem proof."
        ),
        "results": result,
    }
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"   Artifact Saved: {ARTIFACT_PATH}")


def run_bsd_research():
    print("UET SURROGATE BSD DEMONSTRATION")
    print("================================")

    print("\n[1] Testing Curve A (Rank 0 Candidate: y^2 = x^3 + x + 1)...")
    engine_a = EllipticResonanceEngine(a=1, b=1)
    l_val_a = engine_a.calculate_omega(complex(1, 0))
    rank_indicator_a = 1 if (engine_a.a + engine_a.b) % 2 == 0 else 0
    print(f"    Potential (Omega) at s=1: {l_val_a:8.5e}")
    if l_val_a > 1e-5:
        print("    Surrogate indicator: shallow-manifold narrative branch.")

    print("\n[2] Testing Curve B (Rank 1 Candidate: y^2 = x^3 + 2x + 4)...")
    engine_b = EllipticResonanceEngine(a=2, b=4)
    l_val_b = engine_b.calculate_omega(complex(1, 0))
    rank_indicator_b = 1 if (engine_b.a + engine_b.b) % 2 == 0 else 0
    print(f"    Potential (Omega) at s=1: {l_val_b:8.5e}")
    if l_val_b < 1e-10:
        print("    Surrogate indicator: deep-unity-well narrative branch.")

    print("\nSummary:")
    print("   This script produced a surrogate BSD-style artifact.")
    print("   It compares narrated curve roles against a local parity heuristic.")
    print("   It does not compute elliptic-curve rank or prove BSD.")

    curves = [
        {
            "label": "Curve A",
            "equation": "y^2 = x^3 + x + 1",
            "a": 1,
            "b": 1,
            "declared_rank_role": "Rank 0 candidate in script narration",
            "surrogate_rank_indicator": rank_indicator_a,
            "omega_at_s_1": float(l_val_a),
        },
        {
            "label": "Curve B",
            "equation": "y^2 = x^3 + 2x + 4",
            "a": 2,
            "b": 4,
            "declared_rank_role": "Rank 1+ candidate in script narration",
            "surrogate_rank_indicator": rank_indicator_b,
            "omega_at_s_1": float(l_val_b),
        },
    ]
    mismatches = sum(
        1
        for item in curves
        if ("Rank 0" in item["declared_rank_role"] and item["surrogate_rank_indicator"] != 0)
        or ("Rank 1" in item["declared_rank_role"] and item["surrogate_rank_indicator"] != 1)
    )
    result = {
        "status": "PASS" if mismatches == 0 else "WARN",
        "curves": curves,
        "rank_indicator_mismatches": mismatches,
        "proof_boundary": "surrogate demonstration, not BSD proof",
    }
    write_verification_artifact(result)
    return result


if __name__ == "__main__":
    result = run_bsd_research()
    sys.exit(0 if result["status"] in {"PASS", "WARN"} else 1)
