"""Regenerate the foundation dependency gate from current repository evidence.

This gate is intentionally conservative.  A selected normalized lane may pass its
own verifier without promoting the foundation or any physical downstream claim.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs/core/artifacts/uet_foundation_dependency_gate.json"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {rel(path)}")
    return value


def build_gate() -> dict[str, Any]:
    inventory_path = ROOT / "docs/core/artifacts/uet_foundation_equation_inventory.json"
    code_path = ROOT / "docs/core/artifacts/uet_code_surface_inventory.json"
    matrix_path = ROOT / "docs/core/artifacts/uet_foundation_correspondence_matrix.json"
    registry_path = ROOT / "docs/core/artifacts/uet_equation_correspondence_registry.json"
    compat_path = ROOT / "docs/core/artifacts/uet_foundation_compatibility_gate.json"
    characteristic_path = ROOT / "docs/core/artifacts/matter_space_characteristic_cone_verification.json"
    causal_lane_path = ROOT / "docs/core/artifacts/matter_space_causal_lane_selection.json"
    pilot_sync_path = ROOT / "docs/core/artifacts/matter_space_topic_pilot_sync.json"
    lane_contract_path = ROOT / "docs/core/artifacts/uet_active_lane_units_observable_register.json"
    coverage_path = ROOT / "docs/core/artifacts/uet_foundation_coverage_closure.json"
    correspondence_full_path = ROOT / "docs/core/artifacts/uet_full_correspondence_coverage.json"
    correspondence_manifest_path = ROOT / "docs/core/artifacts/uet_topic_formula_correspondence_manifest.json"
    observable_path = ROOT / "docs/core/artifacts/matter_space_observable_verification.json"
    wording_path = ROOT / "docs/core/artifacts/impact_effect_legacy_wording_audit.json"
    inventory = load(inventory_path)
    code = load(code_path)
    matrix = load(matrix_path)
    registry = load(registry_path)
    compat = load(compat_path)
    characteristic = load(characteristic_path)
    causal_lane = load(causal_lane_path)
    pilot_sync = load(pilot_sync_path)
    lane_contract = load(lane_contract_path)
    coverage = load(coverage_path)
    correspondence_full = load(correspondence_full_path)
    correspondence_manifest = load(correspondence_manifest_path)
    observable_map = load(observable_path)
    wording = load(wording_path)

    characteristic_pass = characteristic.get("audit_status") == "PASS"
    selected_lane = causal_lane.get("selected_lane", {})
    selected_lane_status = causal_lane.get("audit_status", "UNKNOWN")
    topic_rerun_open = (
        pilot_sync.get("topic_0_11", {}).get("rerun_status", "").startswith("NOT_RERUN")
        or pilot_sync.get("topic_0_13", {}).get("rerun_status", "").startswith("NOT_RERUN")
    )
    registry_entries = registry.get("entries", [])
    missing_scope = inventory.get("coverage", {}).get("missing_scope", [])
    code_unlinked = code.get("coverage", {}).get("unlinked_core_file_count", 0)
    matrix_blocked = matrix.get("matrix_status") == "BLOCKED"

    gates = {
        "F0_inventory": {
            "status": "PASS_CONDITIONAL_WITH_EXPLICIT_QUARANTINES" if coverage.get("coverage_gate_status") == "PASS_WITH_EXPLICIT_QUARANTINES" else "BLOCKED",
            "reason": "Every discovered code surface and formula-audit row is now assigned to a declared family or explicitly quarantined; correspondence and physical meaning remain separate gates.",
            "evidence": [rel(inventory_path), rel(code_path), rel(coverage_path)],
            "metrics": {
                "formula_audit_files": inventory.get("coverage", {}).get("formula_audit_file_count"),
                "formula_rows": inventory.get("coverage", {}).get("parsed_formula_row_count"),
                "core_python_files": code.get("coverage", {}).get("core_python_file_count"),
                "candidate_code_surfaces": code.get("coverage", {}).get("candidate_surface_count"),
                "unlinked_core_files": code_unlinked,
                "coverage_gate_status": coverage.get("coverage_gate_status"),
                "explicit_quarantine_surface_count": coverage.get("summary", {}).get("code_status_counts", {}).get("EXPLICITLY_QUARANTINED", 0),
            },
            "required_next_artifact": "full correspondence/unit/observable matrix for inventoried rows",
        },
        "F1_ontology": {
            "status": "PASS_CONDITIONAL" if registry_entries else "BLOCKED",
            "reason": "Lane-specific C, Phi, Pi, R_gen and standard physical quantities are separated; universal identity remains prohibited.",
            "evidence": [rel(registry_path), rel(compat_path), rel(wording_path)],
            "required_next_artifact": (
                wording.get("next_controller", "active prose legacy wording review")
                + "; lane-level ontology closure remains required"
            ),
        },
        "F2_physical_correspondence": {
            "status": "BLOCKED_OPEN_CORRESPONDENCE_ROWS" if correspondence_full.get("matrix_status") == "BLOCKED_OPEN_CORRESPONDENCE_ROWS" else ("BLOCKED" if matrix_blocked else "PASS_CONDITIONAL"),
            "reason": "All inventoried topic rows now have an explicit correspondence record, but open standard-counterpart/derivation/observable mappings remain.",
            "evidence": [rel(matrix_path), rel(correspondence_full_path), rel(correspondence_manifest_path), rel(registry_path)],
            "metrics": {
                "topic_formula_rows": correspondence_full.get("coverage", {}).get("topic_formula_row_count"),
                "open_correspondence_rows": correspondence_full.get("coverage", {}).get("open_correspondence_row_count"),
                "central_registry_linked_rows": correspondence_full.get("coverage", {}).get("central_registry_linked_topic_rows"),
                "manifest_rows": correspondence_manifest.get("coverage", {}).get("manifest_rows"),
                "manifest_rows_missing": correspondence_manifest.get("coverage", {}).get("rows_missing_from_manifest"),
                "measurement_operator_records": correspondence_manifest.get("coverage", {}).get("measurement_operator_records"),
                "measurement_operator_open_rows": correspondence_manifest.get("coverage", {}).get("measurement_operator_open_rows"),
            },
            "required_next_artifact": "resolve the 152 open standard-counterpart rows, 263 open measurement-operator records, and 159 rows without a central-registry relation",
        },
        "F3_units": {
            "status": "BLOCKED",
            "reason": "Normalized and natural-unit contracts exist for selected lanes; complete SI/dimensional observable contracts are not closed.",
            "evidence": [rel(registry_path), rel(lane_contract_path)],
            "metrics": {"active_lane_count": lane_contract.get("lane_count"), "units_contract_status": lane_contract.get("foundation_effect", {}).get("F3_units")},
            "required_next_artifact": "unit closure register for every active physical lane",
        },
        "F4_derivation": {
            "status": "BLOCKED" if compat.get("controlling_blockers") else "PASS_CONDITIONAL",
            "reason": "Canonical candidate relations and O(2) EOS derivation are recorded, while heuristic bridges and legacy conflicts remain open.",
            "evidence": [rel(compat_path), rel(registry_path)],
            "required_next_artifact": "derivation-origin audit covering every inventoried relation",
        },
        "F5_formal_verification": {
            "status": "PASS_CONDITIONAL",
            "reason": "Selected canonical/characteristic lanes have local formal checks; legacy and unclosed families remain quarantined.",
            "evidence": [rel(compat_path), rel(characteristic_path)],
            "required_next_artifact": "registry-linked verification matrix for all active families",
        },
        "F6_numerical_verification": {
            "status": "PASS_CONDITIONAL_SELECTED_LANE" if characteristic_pass else "BLOCKED",
            "reason": "The selected characteristic cone lane passes its normalized verifier; the old full coupled lane and changing conserved-C lane retain separate blockers.",
            "evidence": [rel(characteristic_path), rel(causal_lane_path)],
            "metrics": {
                "selected_lane_audit": characteristic.get("audit_status"),
                "selected_lane_status": selected_lane_status,
                "selected_operator": selected_lane.get("operator_mode"),
                "prearrival_leakage_fraction": characteristic.get("metrics", {}).get("prearrival_leakage_fraction"),
            },
            "required_next_artifact": "lane-specific topic reruns and a separately closed conserved/causal branch decision",
        },
        "F7_observable_mapping": {
            "status": "BLOCKED",
            "reason": "Internal normalized diagnostics exist, but physical measurement operators, dimensional maps and uncertainty contracts are incomplete.",
            "evidence": [rel(pilot_sync_path), rel(lane_contract_path), rel(observable_path), rel(registry_path)],
            "metrics": {"normalized_operator_status": observable_map.get("audit_status"), "si_status": observable_map.get("measurement_operator", {}).get("SI_status")},
            "metrics": {"active_lane_count": lane_contract.get("lane_count"), "observable_status_counts": lane_contract.get("observable_status_counts", {})},
            "required_next_artifact": "observable mapping register with units, resolution and uncertainty for each active lane",
        },
        "F8_data_and_claim": {
            "status": "BLOCKED",
            "reason": "Downstream evidence is simulation/internal or dependency-blocked; no foundation claim can be promoted to external physical validation.",
            "evidence": [rel(pilot_sync_path), "docs/core/artifacts/uet_foundation_extended_wave_closure.json"],
            "required_next_artifact": "source-locked external data package plus preregistered holdout policy",
        },
    }

    overall = "BLOCKED" if any(item["status"] == "BLOCKED" for item in gates.values()) else "PASS_CONDITIONAL"
    return {
        "schema_version": "1.1",
        "artifact": "uet_foundation_dependency_gate",
        "generated_at": date.today().isoformat(),
        "audit_status": "PASS",
        "status": overall,
        "wave_type": "foundation_first_workflow",
        "controlling_blocker": "foundation_coverage_units_observable_and_external_claim_gates_incomplete",
        "claim_ceiling": "candidate normalized effective models and explicitly labelled internal/simulation diagnostics; no universal C, mass, particle or global-cosmology claim",
        "authority": "docs/topics/For Work/EQUATION_RESEARCH_AND_PHYSICAL_CORRESPONDENCE_STANDARD.md",
        "protocol": "docs/core/artifacts/uet_equation_research_protocol.json",
        "registry": rel(registry_path),
        "gates": gates,
        "finite_cone_C_lane": {
            "status": "PASS_WITH_DEFERRED_CONSERVED_BRANCH" if characteristic_pass else "BLOCKED",
            "operator_mode": selected_lane.get("operator_mode", "matter_space_characteristic_cone_v1"),
            "standard_counterpart": "damped hyperbolic non-conserved order-parameter dynamics",
            "unit_lane": "normalized_only_v1",
            "evidence": [rel(characteristic_path), rel(causal_lane_path)],
            "controller": "conserved_changing_C_high_k_blocker_and_topic_observable_reruns" if characteristic_pass else "characteristic_lane_verifier",
            "claim_ceiling": "candidate normalized finite-cone collective-response lane; no mass/density/covariant/empirical claim",
            "deferred_branches": {
                "conserved_C_changing_response": "BLOCKED_HIGH_K_DISPERSION",
                "legacy_full_coupled_operator": "BLOCKED_PREARRIVAL_OR_DOMAIN_OF_DEPENDENCE",
            },
        },
        "coverage_snapshot": {
            "registry_entry_count": len(registry_entries),
            "inventory_missing_scope_count": len(missing_scope),
            "code_unlinked_core_files": code_unlinked,
            "matrix_status": matrix.get("matrix_status"),
            "topic_rerun_open": topic_rerun_open,
        },
        "downstream_policy": {
            "new_foundational_equations": "BLOCKED",
            "new_core_operators": "ALLOWED_ONLY_AS_EXPLICIT_OPT_IN_DIAGNOSTIC_WITH_REGISTRY_ENTRY",
            "ontology_and_formula_audits": "ALLOWED",
            "synthetic_diagnostics": "ALLOWED_WITH_SIMULATION_ONLY_LABEL",
            "physical_data_claims": "BLOCKED",
            "existing_downstream_topics": "retain current status; no promotion",
        },
        "next_controller": "close coverage closure manifest, units/observable register, then rerun selected 0.11/0.13 lanes",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    try:
        gate = build_gate()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"audit_status=FAIL\nERROR: {exc}")
        return 1
    if not args.no_write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(gate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(gate, indent=2, ensure_ascii=False))
    else:
        print(f"audit_status={gate['audit_status']}")
        print(f"status={gate['status']}")
        print(f"finite_cone_C_lane={gate['finite_cone_C_lane']['status']}")
        print(f"controlling_blocker={gate['controlling_blocker']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
