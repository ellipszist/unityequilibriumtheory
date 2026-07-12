"""Run and aggregate the bounded Book 1 economics hardening lane for Topic 0.25."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from economic_hardening_common import (
    ARTIFACT_DIR,
    CLAIM_GATE,
    FORMULA_GATE,
    HOLDOUT_POLICY,
    PARAMETER_POLICY,
    RESEARCH_DATA,
    ROOT,
    SOURCE_MANIFEST,
    SOURCE_READINESS,
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
    "resource_equation": ARTIFACT_DIR / "0_25_uet_resource_equation_audit.json",
    "stone_balloon": ARTIFACT_DIR / "0_25_stone_balloon_audit.json",
    "energy_density": ARTIFACT_DIR / "0_25_energy_density_audit.json",
    "wage_productivity": ARTIFACT_DIR / "0_25_wage_productivity_audit.json",
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
            run("Research_UET_Resource_Equation_Audit.py"),
            run("Research_Stone_Balloon_Audit.py"),
            run("Research_Energy_Density_Audit.py"),
            run("Research_Wage_Productivity_Audit.py"),
        ]
    )
    readiness = load_json(SOURCE_READINESS)
    sub_artifacts = {name: artifact_reference(path) for name, path in SUB_ARTIFACTS.items()}
    source_ready = readiness.get("status") == "PASS"
    sub_complete = all(item["status"] not in {"MISSING", "WARN"} for item in sub_artifacts.values())
    controller_status = "DESCRIPTIVE_DIAGNOSTIC_ONLY"
    status = "DIAGNOSTIC_COMPLETE" if source_ready and sub_complete else "WARN"
    next_blockers = list(readiness.get("blockers", []))
    if not source_ready and not next_blockers:
        next_blockers.append("Source-readiness gate is absent or not PASS.")
    for name, item in sub_artifacts.items():
        if item["status"] in {"MISSING", "WARN"}:
            next_blockers.append(f"{name}: {item['status']}")
            next_blockers.extend(item.get("blockers", []))
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
    }
    write_json(CLAIM_GATE, claim_gate)
    artifact = {
        "schema_version": "1.0",
        "topic": "0.25_Strategy_Power_Economics",
        "status": status,
        "generated_at_utc": utc_now(),
        "command": "python docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Verify_UET_Economics_Hardening.py",
        "environment": runtime_environment(),
        "claim_class": "C - internal economic data integrity and historical diagnostic benchmark",
        "formula_ids": ["EC25-UET-RESOURCE-ENGINE", "EC25-UET-MONETARY-RESOURCE-MISMATCH", "EC25-UET-WAGE-PRODUCTIVITY-GAP"],
        "source_manifest": artifact_reference(SOURCE_MANIFEST),
        "source_readiness": readiness,
        "formula_gate": artifact_reference(FORMULA_GATE),
        "parameter_policy": artifact_reference(PARAMETER_POLICY),
        "holdout_policy": artifact_reference(HOLDOUT_POLICY),
        "sub_artifacts": sub_artifacts,
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
