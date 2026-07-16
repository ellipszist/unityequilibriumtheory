"""Run and aggregate the bounded Book 1 economics hardening lane for Topic 0.25."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from economic_hardening_common import (
    ARTIFACT_DIR,
    CAUSAL_DAG,
    CLAIM_MATRIX,
    CLAIM_GATE,
    FORMULA_GATE,
    HOLDOUT_POLICY,
    MEASUREMENT_ARTIFACT,
    PARAMETER_POLICY,
    PANEL_STATUS,
    RESEARCH_DATA,
    RESEARCH_REGISTER,
    ROOT,
    SOURCE_MANIFEST,
    SOURCE_READINESS,
    VARIABLE_DICTIONARY,
    WARN_GATE_REGISTRY,
    WELFARE_ARTIFACT,
    WELFARE_SOURCE_MANIFEST,
    load_json,
    relative,
    runtime_environment,
    sha256,
    utc_now,
    write_json,
)


ARTIFACT = ARTIFACT_DIR / "0_25_uet_economics_verification.json"
HERE = Path(__file__).resolve().parent
SUB_ARTIFACTS = {
    "measurement_validity": MEASUREMENT_ARTIFACT,
    "welfare": WELFARE_ARTIFACT,
    "resource_equation": ARTIFACT_DIR / "0_25_uet_resource_equation_audit.json",
    "stone_balloon": ARTIFACT_DIR / "0_25_stone_balloon_audit.json",
    "energy_density": ARTIFACT_DIR / "0_25_energy_density_audit.json",
    "wage_productivity": ARTIFACT_DIR / "0_25_wage_productivity_audit.json",
}
LEGACY_DOC_ROOT = ROOT / "docs/topics/0.25_Strategy_Power_Economics/Doc"


def legacy_claim_quarantine() -> dict:
    docs = sorted(LEGACY_DOC_ROOT.rglob("*.md")) if LEGACY_DOC_ROOT.exists() else []
    missing_warning = []
    for path in docs:
        content = path.read_text(encoding="utf-8", errors="replace")
        if "Legacy claim boundary" not in content:
            missing_warning.append(relative(path))
    return {
        "status": "PASS" if docs and not missing_warning else "WARN",
        "files_scanned": len(docs),
        "missing_boundary_warning_files": missing_warning,
        "required_boundary_phrase": "Legacy claim boundary",
        "claim_effect": "Legacy notes remain quarantined from topic status and primary Book 1 evidence.",
    }


def run(script: str, arguments: list[str] | None = None) -> dict:
    command = [sys.executable, str(HERE / script)] + (arguments or [])
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    return {
        "script": relative(HERE / script),
        "command": command,
        "exit_code": completed.returncode,
        "stdout_tail": completed.stdout[-1200:],
        "stderr_tail": completed.stderr[-1200:],
    }


def artifact_reference(path: Path) -> dict:
    payload = load_json(path)
    return {
        "path": relative(path),
        "exists": path.exists(),
        "sha256": sha256(path) if path.exists() else None,
        "status": payload.get("status", "PRESENT" if path.exists() else "MISSING"),
        "controller_status": payload.get("controller_status"),
        "blockers": payload.get("blockers", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-sources", action="store_true", help="Download public FRED source files before running the non-network diagnostics.")
    args = parser.parse_args()
    commands = []
    if args.refresh_sources:
        commands.append(run("Research_UET_Economics_Source_Package.py", ["--refresh"]))
    elif not SOURCE_MANIFEST.exists():
        commands.append(run("Research_UET_Economics_Source_Package.py"))
    commands.extend(
        [
            run("Research_UET_Economics_Panel.py"),
            run("Research_UET_Measurement_Validity_Audit.py"),
            run("Research_UET_Welfare_Audit.py"),
            run("Research_UET_Resource_Equation_Audit.py"),
            run("Research_Stone_Balloon_Audit.py"),
            run("Research_Energy_Density_Audit.py"),
            run("Research_Wage_Productivity_Audit.py"),
        ]
    )
    readiness = load_json(SOURCE_READINESS)
    source_manifest_payload = load_json(SOURCE_MANIFEST)
    welfare_source_manifest_payload = load_json(WELFARE_SOURCE_MANIFEST)
    transform_manifest_payload = load_json(RESEARCH_DATA / "uet_us_economics_transform_manifest.json")
    panel_payload = load_json(PANEL_STATUS)
    formula_payload = load_json(FORMULA_GATE)
    parameter_payload = load_json(PARAMETER_POLICY)
    holdout_payload = load_json(HOLDOUT_POLICY)
    research_register_payload = load_json(RESEARCH_REGISTER)
    variable_dictionary_payload = load_json(VARIABLE_DICTIONARY)
    causal_dag_payload = load_json(CAUSAL_DAG)
    claim_matrix_payload = load_json(CLAIM_MATRIX)
    warn_gate_registry_payload = load_json(WARN_GATE_REGISTRY)
    architecture_files = {
        "research_register": RESEARCH_REGISTER,
        "variable_dictionary": VARIABLE_DICTIONARY,
        "causal_dag": CAUSAL_DAG,
        "claim_matrix": CLAIM_MATRIX,
        "warn_gate_registry": WARN_GATE_REGISTRY,
    }
    architecture_missing = [name for name, path in architecture_files.items() if not path.exists()]
    architecture_gate_rows = warn_gate_registry_payload.get("gates", [])
    architecture_blockers = [
        f"{row.get('gate_id')}: {row.get('status')}"
        for row in architecture_gate_rows
        if row.get("controlling") and row.get("status") not in {"PASS", "PASS_WITH_BOUNDARY"}
    ]
    if architecture_missing:
        architecture_blockers.extend(f"architecture_file_missing: {name}" for name in architecture_missing)
    sub_artifacts = {name: artifact_reference(path) for name, path in SUB_ARTIFACTS.items()}
    sub_artifact_payloads = {name: load_json(path) for name, path in SUB_ARTIFACTS.items()}
    legacy_quarantine = legacy_claim_quarantine()
    source_ready = readiness.get("status") == "PASS"
    command_failures = [f"{item['script']}: exit_code={item['exit_code']}" for item in commands if item.get("exit_code") != 0]
    sub_complete = (
        not command_failures
        and legacy_quarantine["status"] == "PASS"
        and all(item["status"] not in {"MISSING", "WARN"} for item in sub_artifacts.values())
    )
    controller_status = "DESCRIPTIVE_DIAGNOSTIC_ONLY"
    status = "DIAGNOSTIC_COMPLETE" if source_ready and sub_complete else "WARN"
    next_blockers = list(readiness.get("blockers", []))
    next_blockers.extend(command_failures)
    if legacy_quarantine["status"] != "PASS":
        next_blockers.append("legacy_claim_quarantine: WARN")
        next_blockers.extend(legacy_quarantine["missing_boundary_warning_files"])
    if not source_ready and not next_blockers:
        next_blockers.append("Source-readiness gate is absent or not PASS.")
    for name, item in sub_artifacts.items():
        if item["status"] in {"MISSING", "WARN"}:
            next_blockers.append(f"{name}: {item['status']}")
            next_blockers.extend(item.get("blockers", []))
    next_blockers.extend(architecture_blockers)
    if architecture_blockers:
        status = "WARN"
    claim_gate = {
        "schema_version": "1.0",
        "topic": "0.25_Strategy_Power_Economics",
        "gate": "uet_book1_economics_claim_gate",
        "controller_status": controller_status,
        "allowed_claims_now": [
            "The topic contains a source-gated U.S. historical diagnostic architecture.",
            "A completed artifact may report its predeclared descriptive comparison results and failures.",
        ],
        "blocked_claims": [
            "R=N+K+I is a derived or confirmed economic law.",
            "Fiat money causally created inflation, wage divergence, or wealth transfer.",
            "Gold or equities are validated scaling pegs or superior assets.",
            "A policy, strategy, social-stabilization, or Nash-equilibrium claim is validated.",
        ],
        "machine_readable_next_blockers": sorted(set(next_blockers)),
        "claim_boundary": "All results remain internal, descriptive, and non-causal pending source completion, human review, causal design, and external replication.",
        "strategy_social_quarantine": "Strategy, power, Nash, and social-stabilization notes remain exploratory and excluded from core economics evidence.",
    }
    write_json(CLAIM_GATE, claim_gate)
    artifact = {
        "schema_version": "1.1",
        "topic": "0.25_Strategy_Power_Economics",
        "status": status,
        "generated_at_utc": utc_now(),
        "command": "python docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Verify_UET_Economics_Hardening.py",
        "environment": runtime_environment(),
        "claim_class": "C - internal economic data integrity and historical diagnostic benchmark",
        "formula_ids": ["EC25-UET-RESOURCE-ENGINE", "EC25-UET-MONETARY-RESOURCE-MISMATCH", "EC25-UET-WAGE-PRODUCTIVITY-GAP"],
        "source_manifest": artifact_reference(SOURCE_MANIFEST),
        "welfare_source_manifest": artifact_reference(WELFARE_SOURCE_MANIFEST),
        "source_readiness": readiness,
        "source_transformation_manifest": artifact_reference(RESEARCH_DATA / "uet_us_economics_transform_manifest.json"),
        "panel_status": artifact_reference(PANEL_STATUS),
        "execution_gate": {"all_commands_exit_zero": not command_failures, "command_failures": command_failures},
        "legacy_claim_quarantine": legacy_quarantine,
        "formula_gate": artifact_reference(FORMULA_GATE),
        "parameter_policy": artifact_reference(PARAMETER_POLICY),
        "holdout_policy": artifact_reference(HOLDOUT_POLICY),
        "research_architecture": {
            "current_package_tier": research_register_payload.get("current_package_tier", "Package Tier A"),
            "target_evidence_grade": research_register_payload.get("target_evidence_grade", "Evidence Grade A"),
            "current_claim_class": research_register_payload.get("current_claim_class", "C"),
            "active_waves": [row for row in research_register_payload.get("waves", []) if row.get("status") == "IN_PROGRESS"],
            "strategy_social_quarantine": research_register_payload.get("strategy_social_quarantine", {}),
            "architecture_status": "PASS" if not architecture_blockers else "WARN",
            "controlling_gate_blockers": sorted(set(architecture_blockers)),
            "file_references": {name: artifact_reference(path) for name, path in architecture_files.items()},
            "warn_gate_registry": warn_gate_registry_payload,
        },
        "sub_artifacts": sub_artifacts,
        "evidence_bundle": {
            "retrieval_vintage": source_manifest_payload.get("retrieval_vintage"),
            "source_records_with_hashes": source_manifest_payload.get("sources", []),
            "welfare_source_records_with_hashes": welfare_source_manifest_payload.get("sources", []),
            "source_transformation_manifest": transform_manifest_payload,
            "panel_status_payload": panel_payload,
            "formula_gate_payload": formula_payload,
            "parameter_policy_payload": parameter_payload,
            "holdout_policy_payload": holdout_payload,
            "research_register_payload": research_register_payload,
            "variable_dictionary_payload": variable_dictionary_payload,
            "causal_dag_payload": causal_dag_payload,
            "claim_matrix_payload": claim_matrix_payload,
            "warn_gate_registry_payload": warn_gate_registry_payload,
            "sub_artifact_payloads": sub_artifact_payloads,
        },
        "commands": commands,
        "economics_claim_scope_gate": claim_gate,
        "limitations": [
            "The Book 1 economic relations are operationalized as source-dependent proxies, not derivations.",
            "The 1971 regime summaries are non-causal and exclude 1971-1973 from pre/post descriptive comparisons.",
            "An internal candidate signal cannot upgrade Claim Class C or support policy, asset-superiority, or strategic-superiority claims.",
        ],
    }
    write_json(ARTIFACT, artifact)
    print(f"UET Book 1 economics hardening: {status}")
    print(f"  controller: {controller_status}")
    print(f"  artifact: {ARTIFACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
