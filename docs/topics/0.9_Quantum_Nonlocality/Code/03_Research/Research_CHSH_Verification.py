"""Topic 0.9 verification: CHSH/Bell benchmark audit with evidence and claim gates."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from datetime import UTC, datetime
from pathlib import Path


def bootstrap_repo() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    raise RuntimeError("Repository root with docs/core was not found.")


ROOT = bootstrap_repo()
TOPIC = ROOT / "docs" / "topics" / "0.9_Quantum_Nonlocality"
DATA = TOPIC / "Data" / "03_Research"
ARTIFACT = TOPIC / "Result" / "artifacts" / "0_9_quantum_nonlocality_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = DATA / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = DATA / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = DATA / "branch_claim_gate.json"
SOURCE_LOCK_MANIFEST_PATH = DATA / "source_lock_manifest.json"
HENSEN_REFERENCE_PATH = ROOT / "docs" / "data" / "external" / "quantum_nonlocality" / "hensen_2015_chsh_reference_package.json"
SUMMARY_REFERENCE_PATH = ROOT / "docs" / "data" / "external" / "quantum_nonlocality" / "bell_inequality_summary_reference_package.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def load_json_if_exists(path: Path) -> dict | None:
    if not path.exists():
        return None
    return load_json(path)


def field(name: str, status: str, value) -> dict:
    return {"field": name, "status": status, "value": value}


def build_source_evidence_intake_stub() -> dict:
    hensen_package = load_json_if_exists(HENSEN_REFERENCE_PATH)
    summary_package = load_json_if_exists(SUMMARY_REFERENCE_PATH)
    return {
        "schema_version": "1.0",
        "topic": "0.9_Quantum_Nonlocality",
        "purpose": "Source evidence intake before data normalization or claim upgrades for CHSH and adjacent quantum lanes.",
        "source_targets": [
            {
                "name": "Hensen 2015 CHSH benchmark package",
                "priority": "immediate",
                "status": "complete" if hensen_package else "pending",
                "evidence_entries": [
                    field("doi_or_url", "complete" if hensen_package and hensen_package.get("doi") else "pending", hensen_package.get("doi", "") if hensen_package else ""),
                    field("local_path", "complete" if hensen_package else "pending", str(HENSEN_REFERENCE_PATH.relative_to(ROOT)).replace("\\", "/") if hensen_package else ""),
                    field("table_or_result_identifier", "complete" if hensen_package else "pending", hensen_package.get("result_identifier", "") if hensen_package else ""),
                    field("retrieval_date", "complete" if hensen_package else "pending", hensen_package.get("retrieval_or_packaging_date", "") if hensen_package else ""),
                    field("unit_basis", "complete" if hensen_package else "pending", json.dumps(hensen_package.get("unit_basis", {}), ensure_ascii=False) if hensen_package else ""),
                    field("extraction_note", "complete" if hensen_package else "pending", hensen_package.get("extraction_note", "") if hensen_package else ""),
                ],
            },
            {
                "name": "Raw Bell event-count or supplementary package",
                "priority": "high",
                "status": "pending",
                "evidence_entries": [
                    field("doi_or_url", "pending", ""),
                    field("local_path", "pending", ""),
                    field("supplement_or_table_identifier", "pending", ""),
                    field("retrieval_date", "pending", ""),
                    field("license_or_access_note", "pending", ""),
                    field("extraction_note", "pending", ""),
                ],
            },
            {
                "name": "Secondary Bell summary file provenance",
                "priority": "high",
                "status": "complete" if summary_package else "pending",
                "evidence_entries": [
                    field("upstream_reference", "complete" if summary_package and summary_package.get("doi") else "pending", summary_package.get("doi", "") if summary_package else ""),
                    field("local_path", "complete" if summary_package else "pending", str(SUMMARY_REFERENCE_PATH.relative_to(ROOT)).replace("\\", "/") if summary_package else ""),
                    field("summary_generation_note", "complete" if summary_package else "pending", summary_package.get("result_identifier", "") if summary_package else ""),
                    field("retrieval_date", "complete" if summary_package else "pending", summary_package.get("retrieval_or_packaging_date", "") if summary_package else ""),
                    field("unit_basis", "complete" if summary_package else "pending", json.dumps(summary_package.get("unit_basis", {}), ensure_ascii=False) if summary_package else ""),
                    field("extraction_note", "complete" if summary_package else "pending", summary_package.get("extraction_note", "") if summary_package else ""),
                ],
            },
            {
                "name": "Qubit or adjacent quantum-lane source package",
                "priority": "medium",
                "status": "pending",
                "evidence_entries": [
                    field("dataset_identity", "pending", ""),
                    field("doi_or_url", "pending", ""),
                    field("local_path", "pending", ""),
                    field("lane_scope", "pending", ""),
                    field("unit_basis", "pending", ""),
                    field("extraction_note", "pending", ""),
                ],
            },
        ],
        "claim_boundary": "This intake stub is for provenance capture only. It does not authorize upgrades to UET nonlocality or adjacent quantum-lane claims.",
    }


def build_source_evidence_readiness_matrix(intake_stub: dict) -> dict:
    rows = []
    ready_count = 0
    for target in intake_stub["source_targets"]:
        pending_fields = [entry["field"] for entry in target["evidence_entries"] if entry.get("status") != "complete"]
        row = {
            "name": target["name"],
            "priority": target["priority"],
            "fields_total": len(target["evidence_entries"]),
            "fields_complete": len(target["evidence_entries"]) - len(pending_fields),
            "fields_pending": len(pending_fields),
            "pending_fields": pending_fields,
            "ready_for_source_review": not pending_fields,
            "blocking_reason": "" if not pending_fields else "One or more required evidence fields are still pending.",
        }
        rows.append(row)
        if row["ready_for_source_review"]:
            ready_count += 1

    return {
        "schema_version": "1.0",
        "topic": "0.9_Quantum_Nonlocality",
        "purpose": "Readiness matrix for source-evidence review before quantum-nonlocality claim upgrades.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A target marked ready still requires real source review. This gate does not itself upgrade a claim.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.9_Quantum_Nonlocality",
        "purpose": "Claim gate for separate evidence lanes inside the quantum nonlocality topic.",
        "summary": {
            "branches_total": 5,
            "accepted_now": 1,
            "blocked_for_strong_claims": 4,
        },
        "branches": [
            {
                "branch": "CHSH benchmark branch",
                "status": "accepted_run_contract_only",
                "allowed_usage_now": "Source-referenced internal Bell-violation benchmark only.",
                "blocker_to_stronger_claim": "Need raw-event or supplemental provenance and uncertainty-aware reconstruction.",
            },
            {
                "branch": "UET topological filament branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Conceptual bridge only.",
                "blocker_to_stronger_claim": "Need derivation artifact that maps the UET bridge to standard CHSH correlations.",
            },
            {
                "branch": "Qubit mechanics or relaxation branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Separate future verifier lane only.",
                "blocker_to_stronger_claim": "Need source-backed qubit dataset and dedicated verifier artifact.",
            },
            {
                "branch": "Double-slit or tunneling branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Separate exploratory lane only.",
                "blocker_to_stronger_claim": "Need independent datasets, formulas, and verification artifacts for each lane.",
            },
            {
                "branch": "Solved nonlocality or mechanism-replacement claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need first-principles derivation, predictive success, and external benchmark support beyond CHSH consistency.",
            },
        ],
        "claim_boundary": "This gate cannot raise the topic beyond the current CHSH run-contract evidence.",
    }


def main() -> int:
    hensen_path = DATA / "bell_test_2015.json"
    summary_path = DATA / "bell_inequality_data.json"
    hensen = load_json(hensen_path)
    summary = load_json(summary_path)

    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix(source_evidence_intake_stub)
    branch_claim_gate = build_branch_claim_gate()

    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)

    s_value = float(hensen["data"]["S_value"]["value"])
    s_error = float(hensen["data"]["S_value"]["error"])
    classical_bound = float(hensen["data"]["local_hidden_var_bound"])
    qm_max = float(hensen["data"]["qm_max"])
    p_value = float(hensen["data"]["p_value"])
    tsirelson_exact = 2.0 * math.sqrt(2.0)

    margin_over_local = s_value - classical_bound
    lower_1sigma = s_value - s_error
    tsirelson_gap = abs(qm_max - tsirelson_exact)

    thresholds = {
        "s_value_must_exceed_local_bound": classical_bound,
        "lower_1sigma_must_exceed_local_bound": classical_bound,
        "p_value_max": 0.05,
        "tsirelson_rounding_error_max": 0.001,
    }

    checks = {
        "s_value_exceeds_local_bound": s_value > classical_bound,
        "lower_1sigma_exceeds_local_bound": lower_1sigma > classical_bound,
        "p_value_ok": p_value < thresholds["p_value_max"],
        "tsirelson_reference_ok": tsirelson_gap <= thresholds["tsirelson_rounding_error_max"],
        "source_has_doi": bool(hensen.get("doi")),
    }

    blockers = []
    if not checks["lower_1sigma_exceeds_local_bound"]:
        blockers.append("The lower 1-sigma CHSH value does not clear the local-realist bound.")
    if not checks["p_value_ok"]:
        blockers.append("The recorded p-value does not clear the provisional p<0.05 gate.")
    if not checks["tsirelson_reference_ok"]:
        blockers.append("The stored quantum benchmark is not sufficiently close to 2*sqrt(2).")
    if not checks["source_has_doi"]:
        blockers.append("Primary Bell-test working copy does not record a DOI.")

    status = "PASS" if all(checks.values()) else "WARN"

    artifact = {
        "schema_version": "1.2",
        "topic": "0.9_Quantum_Nonlocality",
        "status": status,
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "command": "python docs/topics/0.9_Quantum_Nonlocality/Code/03_Research/Research_CHSH_Verification.py",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "claim_class": "C - source-referenced internal CHSH benchmark",
        "formula_ids": [
            "QN09-CHSH-PARAMETER",
            "QN09-LOCAL-REALIST-BOUND",
            "QN09-TSIRELSON-BOUND",
            "QN09-PVALUE-GATE",
        ],
        "inputs": [
            {
                "name": "bell_test_2015",
                "path": str(hensen_path.relative_to(ROOT)).replace("\\", "/"),
                "source": hensen.get("source"),
                "doi": hensen.get("doi"),
                "sha256": sha256(hensen_path),
            },
            {
                "name": "bell_inequality_data",
                "path": str(summary_path.relative_to(ROOT)).replace("\\", "/"),
                "source": summary.get("source"),
                "sha256": sha256(summary_path),
            },
            {
                "name": "source_lock_manifest",
                "path": str(SOURCE_LOCK_MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(SOURCE_LOCK_MANIFEST_PATH),
            },
            {
                "name": "hensen_2015_reference_package",
                "path": str(HENSEN_REFERENCE_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(HENSEN_REFERENCE_PATH),
            },
            {
                "name": "bell_summary_reference_package",
                "path": str(SUMMARY_REFERENCE_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(SUMMARY_REFERENCE_PATH),
            },
        ],
        "source_evidence_intake_stub": {
            "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(TOPIC)).replace("\\", "/"),
            "sha256": sha256(SOURCE_EVIDENCE_INTAKE_PATH),
            "source_targets": [item["name"] for item in source_evidence_intake_stub["source_targets"]],
            "claim_boundary": source_evidence_intake_stub["claim_boundary"],
        },
        "source_evidence_readiness_matrix": {
            "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(TOPIC)).replace("\\", "/"),
            "sha256": sha256(SOURCE_EVIDENCE_READINESS_PATH),
            "summary": source_evidence_readiness_matrix["summary"],
            "claim_boundary": source_evidence_readiness_matrix["claim_boundary"],
        },
        "branch_claim_gate": {
            "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(TOPIC)).replace("\\", "/"),
            "sha256": sha256(BRANCH_CLAIM_GATE_PATH),
            "summary": branch_claim_gate["summary"],
            "claim_boundary": branch_claim_gate["claim_boundary"],
        },
        "threshold": thresholds,
        "checks": checks,
        "blockers": blockers,
        "metrics": {
            "S_value": s_value,
            "S_error": s_error,
            "local_realist_bound": classical_bound,
            "margin_over_local_bound": margin_over_local,
            "lower_1sigma": lower_1sigma,
            "p_value": p_value,
            "qm_max_recorded": qm_max,
            "tsirelson_exact": tsirelson_exact,
            "tsirelson_rounding_gap": tsirelson_gap,
        },
        "interpretation": "Source-referenced internal CHSH benchmark only. This does not derive UET topology or replace the standard nonlocality framework.",
        "limitations": [
            "This artifact verifies a source-referenced CHSH benchmark and Tsirelson-bound consistency.",
            "It does not derive the UET topological-filament explanation from first principles.",
            "It does not reproduce raw event-count analysis from the Hensen et al. experiment.",
            "Qubit, tunneling, double-slit, and LC-unity scripts are outside this primary verifier.",
        ],
    }

    write_json(ARTIFACT, artifact)

    print("UET QUANTUM NONLOCALITY: CHSH CONSISTENCY CHECK")
    print(f"  status: {status}")
    print(f"  S = {s_value:.3f} +/- {s_error:.3f}")
    print(f"  local bound = {classical_bound:.3f}")
    print(f"  p-value = {p_value:.3f}")
    print(f"  Tsirelson recorded/exact = {qm_max:.6f} / {tsirelson_exact:.6f}")
    print(f"  artifact: {ARTIFACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
