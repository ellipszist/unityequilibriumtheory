"""
Build a machine-readable alignment gate for docs/core/00_inbox.

The inbox files are intake evidence, not canonical proof. This audit maps their
main operator claims to the current implemented/verifier artifact chain so the
next research wave starts from current blockers instead of replaying old prose.
"""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


def bootstrap() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = bootstrap()
CORE_DIR = ROOT / "docs" / "core"
INBOX_DIR = CORE_DIR / "00_inbox"
TOPIC_DIR = ROOT / "docs" / "topics" / "0.11_Phase_Transitions"
ARTIFACT_DIR = CORE_DIR / "artifacts"
JSON_PATH = ARTIFACT_DIR / "inbox_research_alignment_gate.json"
REPORT_PATH = CORE_DIR / "INBOX_RESEARCH_ALIGNMENT_AUDIT.md"

INBOX_FILES = [
    INBOX_DIR / "UET_Master_Equation_Analysis.md",
    INBOX_DIR / "implementation_plan.md",
    INBOX_DIR / "raw chat.md",
]

ARTIFACTS = {
    "wave5_spatial_scaling": TOPIC_DIR
    / "Result"
    / "artifacts"
    / "0_11_spatial_coupling_scaling.json",
    "wave6_coefficient_sensitivity": TOPIC_DIR
    / "Result"
    / "artifacts"
    / "0_11_spatial_coupling_sensitivity.json",
    "wave10_operator_requirement": TOPIC_DIR
    / "Result"
    / "artifacts"
    / "0_11_operator_form_requirement_gate.json",
    "wave12_v2_ablation": TOPIC_DIR
    / "Result"
    / "artifacts"
    / "0_11_spatial_coupled_v2_component_ablation.json",
    "wave16_spectral_core": TOPIC_DIR
    / "Result"
    / "artifacts"
    / "0_11_conserved_order_spectral_core_candidate.json",
    "wave23_estimator_sensitivity": TOPIC_DIR
    / "Result"
    / "artifacts"
    / "0_11_conserved_order_spectral_l16_estimator_sensitivity.json",
    "wave24_structure_factor_estimator": TOPIC_DIR
    / "Result"
    / "artifacts"
    / "0_11_conserved_order_spectral_l16_structure_factor_estimator.json",
    "wave25_structure_factor_multigrid": TOPIC_DIR
    / "Result"
    / "artifacts"
    / "0_11_conserved_order_spectral_structure_factor_multigrid_calibration.json",
}


def relpath(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def hash_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_record(path: Path, role: str) -> dict[str, Any]:
    exists = path.exists()
    return {
        "path": relpath(path),
        "role": role,
        "exists": exists,
        "sha256": hash_file(path) if exists else None,
        "bytes": path.stat().st_size if exists else None,
    }


def artifact_record(name: str, path: Path) -> dict[str, Any]:
    exists = path.exists()
    data = load_json(path) if exists else {}
    return {
        "id": name,
        "path": relpath(path),
        "exists": exists,
        "sha256": hash_file(path) if exists else None,
        "status": data.get("status"),
        "blocker_label": data.get("blocker_label"),
        "claim_class": data.get("claim_class"),
    }


def build_artifact() -> dict[str, Any]:
    sources = [
        source_record(
            INBOX_FILES[0],
            "analysis claim: local additive game/information terms are spatially blind; proposes multiplicative information and gradient game repairs",
        ),
        source_record(
            INBOX_FILES[1],
            "implementation plan: co-evolutionary options including kappa(C), dynamic beta_U, and multiplicative information",
        ),
        source_record(
            INBOX_FILES[2],
            "raw conversation intake containing the original concern about hidden standalone equations and engine alignment",
        ),
    ]
    artifacts = {name: artifact_record(name, path) for name, path in ARTIFACTS.items()}
    wave25 = artifacts["wave25_structure_factor_multigrid"]

    source_packaging_pass = all(record["exists"] and record["sha256"] for record in sources)
    artifact_chain_pass = (
        wave25["exists"]
        and wave25["blocker_label"]
        == "spectral_core_structure_factor_multigrid_domain_scale_saturated"
    )

    claim_map = [
        {
            "inbox_claim_id": "a_b_multiplicative_info_plus_gradient_game",
            "inbox_claim_summary": "Combine multiplicative information coupling with interface/gradient-sensitive game coupling.",
            "current_repo_state": "implemented_as_opt_in_diagnostic_then_blocked_by_scaling_gates",
            "evidence": [
                "wave5_spatial_scaling",
                "wave6_coefficient_sensitivity",
                "wave10_operator_requirement",
                "wave12_v2_ablation",
            ],
            "current_boundary": "A/B candidate availability and safety are not enough; beta and correlation gates stayed diagnostic or blocked.",
            "next_action": "Do not retune A/B coefficients as the next default path; only revisit with a new formula/unit gate.",
        },
        {
            "inbox_claim_id": "c_conserved_order_parameter",
            "inbox_claim_summary": "Use conserved-order/Cahn-Hilliard-like dynamics so mass/order is transported rather than locally destroyed.",
            "current_repo_state": "implemented_as_conserved_order_spectral_v1_and_bridge_passed",
            "evidence": [
                "wave16_spectral_core",
                "wave23_estimator_sensitivity",
                "wave24_structure_factor_estimator",
                "wave25_structure_factor_multigrid",
            ],
            "current_boundary": "Core spectral bridge exists, but multi-grid calibration shows the structure-factor estimator is domain-scale saturated.",
            "next_action": "Calibrate against larger grids, known/source-backed benchmarks, or a derived finite-size acceptance rule before exponent or universality claims.",
        },
        {
            "inbox_claim_id": "warped_space_kappa_of_c",
            "inbox_claim_summary": "Let the spatial stiffness/operator depend on the field, e.g. kappa(C) = kappa0 * (1 + alpha C^2).",
            "current_repo_state": "not_accepted_not_primary",
            "evidence": ["implementation_plan.md"],
            "current_boundary": "No formula-audit entry, unit closure, core opt-in mode, or scaling artifact currently accepts this path.",
            "next_action": "If pursued, start with formula/unit/provenance gate before code.",
        },
        {
            "inbox_claim_id": "dynamic_game_landscape_beta_u",
            "inbox_claim_summary": "Make beta_U evolve with interface conflict, e.g. d beta_U/dt = -gamma beta_U + mu |grad C|^2.",
            "current_repo_state": "not_accepted_not_primary",
            "evidence": ["implementation_plan.md"],
            "current_boundary": "No state-variable policy, unit closure, stability gate, or artifact currently accepts dynamic beta_U.",
            "next_action": "If pursued, define state evolution, conservation/safety gates, and claim boundary first.",
        },
        {
            "inbox_claim_id": "hidden_standalone_equation_risk",
            "inbox_claim_summary": "Earlier tests risked bypassing docs/core/uet_master_equation.py with standalone equations.",
            "current_repo_state": "mitigated_by_core_engine_path_gates",
            "evidence": [
                "wave5_spatial_scaling",
                "wave16_spectral_core",
                "wave24_structure_factor_estimator",
            ],
            "current_boundary": "Future candidates still need explicit engine-path gates before claim interpretation.",
            "next_action": "Keep engine alignment gates mandatory for every new operator or estimator verifier.",
        },
    ]

    gates = {
        "inbox_source_packaging_gate": {
            "status": "PASS" if source_packaging_pass else "BLOCKED",
            "required_condition": "All local inbox intake files must exist and have recorded hashes.",
            "source_count": len(sources),
            "hashed_source_count": sum(1 for record in sources if record["sha256"]),
        },
        "inbox_authority_boundary_gate": {
            "status": "PASS",
            "required_condition": "Inbox material must be treated as intake evidence, not canonical proof.",
            "claim_boundary": "Inbox claims can propose candidates; artifacts and formula gates control current status.",
        },
        "artifact_chain_gate": {
            "status": "PASS" if artifact_chain_pass else "BLOCKED",
            "required_condition": "The current 0.11 artifact chain must expose the latest controller.",
            "latest_expected_blocker": "spectral_core_structure_factor_multigrid_domain_scale_saturated",
            "latest_observed_blocker": wave25["blocker_label"],
        },
        "coverage_boundary_gate": {
            "status": "WARN",
            "required_condition": "Inbox options must be separated into implemented diagnostic paths, blocked paths, and unaccepted future paths.",
            "mapped_claim_count": len(claim_map),
            "claim_boundary": "Coverage means mapped to current evidence, not all options implemented or accepted.",
        },
        "next_controller_gate": {
            "status": "BLOCKED",
            "required_condition": "No broad UET phase-transition claim may be promoted until the current domain-scale calibration blocker is cleared.",
            "next_controller": "larger_grid_or_source_backed_structure_factor_estimator_calibration",
        },
    }

    return {
        "schema_version": "1.0",
        "audit_id": "core_inbox_research_alignment_gate",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "WARN",
        "blocker_label": "inbox_claims_mapped_current_controller_domain_scale_saturation",
        "claim_class": "source_intake_alignment_only",
        "sources": sources,
        "artifacts": list(artifacts.values()),
        "claim_map": claim_map,
        "gates": gates,
        "recommended_next_wave": {
            "step": "Calibrate the structure-factor estimator against larger grids, known/source-backed benchmarks, or a derived finite-size acceptance rule before adding new warped-space or dynamic-game operators.",
            "reason": "Wave 25 showed that the structure-factor margin replicates but remains domain-scale saturated; For Work prefers clearing the current controller before broadening scope.",
        },
        "limitations": [
            "This audit does not validate any inbox claim as physics.",
            "Mojibake in the inbox text is preserved as source evidence and should be cleaned only in a separate source-normalization pass.",
            "The raw inbox directory remains intake evidence; artifact gates, formula audits, and topic verifiers control claim wording.",
        ],
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
        },
    }


def render_report(artifact: dict[str, Any]) -> str:
    gates = artifact["gates"]
    claim_rows = []
    for item in artifact["claim_map"]:
        claim_rows.append(
            "| `{}` | {} | {} | {} |".format(
                item["inbox_claim_id"],
                item["current_repo_state"],
                item["current_boundary"],
                item["next_action"],
            )
        )

    source_rows = []
    for source in artifact["sources"]:
        source_rows.append(
            f"- `{source['path']}`: `{source['sha256']}` ({source['bytes']} bytes)"
        )

    return "\n".join(
        [
            "# Inbox Research Alignment Audit",
            "",
            "**Status:** source-intake alignment gate. This report treats `docs/core/00_inbox/` as intake evidence, not canonical proof.",
            "",
            "## Source Package",
            "",
            *source_rows,
            "",
            "## Gate Summary",
            "",
            f"- `inbox_source_packaging_gate`: `{gates['inbox_source_packaging_gate']['status']}`",
            f"- `inbox_authority_boundary_gate`: `{gates['inbox_authority_boundary_gate']['status']}`",
            f"- `artifact_chain_gate`: `{gates['artifact_chain_gate']['status']}`",
            f"- `coverage_boundary_gate`: `{gates['coverage_boundary_gate']['status']}`",
            f"- `next_controller_gate`: `{gates['next_controller_gate']['status']}`",
            "",
            "## Claim Map",
            "",
            "| Inbox claim | Current repo state | Current boundary | Next action |",
            "| :-- | :-- | :-- | :-- |",
            *claim_rows,
            "",
            "## Current Controller",
            "",
            f"`{artifact['recommended_next_wave']['step']}`",
            "",
            artifact["recommended_next_wave"]["reason"],
            "",
            "## Claim Boundary",
            "",
            "This audit does not promote UET phase-transition, universality, RG, or material claims. It only maps inbox claims to the current artifact chain so the next hardening wave starts from the active blocker.",
            "",
        ]
    )


def main() -> None:
    artifact = build_artifact()
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")
    REPORT_PATH.write_text(render_report(artifact), encoding="utf-8")
    print(json.dumps(artifact["gates"], indent=2, sort_keys=True))
    print(f"Wrote {relpath(JSON_PATH)}")
    print(f"Wrote {relpath(REPORT_PATH)}")


if __name__ == "__main__":
    main()
