"""Preserve the newest verified GR-program stage during upstream reruns.

The GR research chain is intentionally rerunnable from its earliest audit.
Earlier generators must therefore recognize later stable artifacts instead of
silently moving the shared program gate backwards.  This helper applies the
sourced comparator stage and, when present, the later fixed-cone feasibility
stage together with its audit metadata.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

COMPARATOR_ARTIFACT = (
    "hyperbolic_phase_field_external_comparator_verification.json"
)
COMPARATOR_EVIDENCE = "PARTIAL_EXTERNAL_COMPARATOR"
LATEST_STAGE = "EXTERNAL_HYPERBOLIC_PHASE_FIELD_COMPARATOR_FORMULA_VERIFIED"
OLD_CONTROLLER = "first_order_hyperbolic_phase_field_uv_closure_missing"
LATEST_CONTROLLER = (
    "uniform_subluminal_hyperbolic_phase_field_and_covariant_mapping_missing"
)
FEASIBILITY_ARTIFACT = "hyperbolic_phase_field_causal_feasibility.json"
FEASIBILITY_EVIDENCE = "PARTIAL_ANALYTIC_CAUSAL_BRIDGE"
FEASIBILITY_STAGE = (
    "FIXED_LIGHT_CONE_FEASIBILITY_AND_LOCAL_CURRENT_MAP_VERIFIED"
)
FEASIBILITY_CONTROLLER = "noether_density_to_phase_field_order_parameter_map_missing"
MAPPING_GATE_ARTIFACT = "hyperbolic_phase_field_covariant_mapping_gate.json"
PROGRAM_TOPIC = "docs/core UET GR non-closed response"



def _load_comparator(out: Path) -> dict[str, Any] | None:
    path = out / COMPARATOR_ARTIFACT
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if payload.get("audit_status") != "PASS":
        return None
    if payload.get("evidence_status") != COMPARATOR_EVIDENCE:
        return None
    return payload


def _load_feasibility(out: Path) -> dict[str, Any] | None:
    path = out / FEASIBILITY_ARTIFACT
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if payload.get("audit_status") != "PASS":
        return None
    if payload.get("evidence_status") != FEASIBILITY_EVIDENCE:
        return None
    return payload




def _rewrite_controller(value: Any) -> Any:
    if isinstance(value, str):
        return LATEST_CONTROLLER if value == OLD_CONTROLLER else value
    if isinstance(value, list):
        return [_rewrite_controller(item) for item in value]
    if isinstance(value, dict):
        return {key: _rewrite_controller(item) for key, item in value.items()}
    return value


def _update_payload(payload: dict[str, Any], comparator: dict[str, Any]) -> None:
    rewritten = _rewrite_controller(payload)
    payload.clear()
    payload.update(rewritten)
    payload["downstream_hyperbolic_phase_field"] = {
        "artifact": COMPARATOR_ARTIFACT,
        "audit_status": comparator["audit_status"],
        "evidence_status": comparator["evidence_status"],
        "role": "external_fixed_parameter_formula_comparator",
        "uet_derivation": "BLOCKED",
        "uniform_subluminal_limit": "BLOCKED",
    }
    completed = payload.get("completed_formula_gates")
    if isinstance(completed, list):
        marker = "external_hyperbolic_phase_field_comparator_formula"
        if marker not in completed:
            completed.append(marker)
    blocked = payload.get("blocked_gates")
    if isinstance(blocked, dict) and "first_order_hyperbolic_gradient_phase_field" in blocked:
        blocked["uet_native_first_order_hyperbolic_gradient_phase_field"] = blocked.pop(
            "first_order_hyperbolic_gradient_phase_field"
        )
        blocked["uniform_subluminal_cahn_hilliard_limit"] = "BLOCKED"



def _rewrite_feasibility_controller(value: Any) -> Any:
    if isinstance(value, str):
        if value in {OLD_CONTROLLER, LATEST_CONTROLLER}:
            return FEASIBILITY_CONTROLLER
        return value
    if isinstance(value, list):
        return [_rewrite_feasibility_controller(item) for item in value]
    if isinstance(value, dict):
        return {
            key: _rewrite_feasibility_controller(item)
            for key, item in value.items()
        }
    return value


def _update_feasibility_payload(
    payload: dict[str, Any],
    comparator: dict[str, Any],
    feasibility: dict[str, Any],
) -> None:
    rewritten = _rewrite_feasibility_controller(payload)
    payload.clear()
    payload.update(rewritten)
    payload["downstream_hyperbolic_phase_field"] = {
        "artifact": COMPARATOR_ARTIFACT,
        "audit_status": comparator["audit_status"],
        "evidence_status": comparator["evidence_status"],
        "role": "external_fixed_parameter_formula_comparator",
        "causal_feasibility_artifact": FEASIBILITY_ARTIFACT,
        "causal_feasibility_status": feasibility["audit_status"],
        "fixed_light_cone_parameter_domain": "PASS_NORMALIZED_ANALYTIC",
        "uniform_subluminal_limit": "NO_GO_EXACT_PARABOLIC_LIMIT",
        "uet_derivation": "BLOCKED",
    }
    completed = payload.get("completed_formula_gates")
    if isinstance(completed, list):
        for marker in (
            "fixed_light_cone_parameter_inequalities",
            "external_q_to_local_current_law_map",
        ):
            if marker not in completed:
                completed.append(marker)



def apply_latest_hyperbolic_phase_field_stage(
    out: Path,
    *payloads: dict[str, Any],
) -> bool:
    """Apply the latest downstream stage to earlier generated payloads."""

    comparator = _load_comparator(out)
    if comparator is None:
        return False
    feasibility = _load_feasibility(out)
    for payload in payloads:
        _update_payload(payload, comparator)
    if feasibility is not None:
        for payload in payloads:
            _update_feasibility_payload(payload, comparator, feasibility)
    for payload in payloads:
        if payload.get("artifact") != "uet_gr_research_program_gate":
            continue
        if feasibility is not None:
            payload["topic"] = PROGRAM_TOPIC
            payload["version"] = "wave8_v1"
            payload["benchmark_role"] = "program_gate"
            payload["method_label"] = "monotonic_gr_research_stage_gate"
            payload["input_identity"] = {
                "causal_feasibility_artifact": (
                    f"docs/core/artifacts/{FEASIBILITY_ARTIFACT}"
                ),
                "covariant_mapping_gate": (
                    f"docs/core/artifacts/{MAPPING_GATE_ARTIFACT}"
                ),
            }
            payload["notes"] = [
                "The controlling blocker is the physical density/order-parameter state map.",
                "Thermal SK/KMS completion is downstream of the classical covariant lane.",
            ]
            payload["program_stage"] = FEASIBILITY_STAGE
            payload["controlling_blocker"] = FEASIBILITY_CONTROLLER
            sectors = payload.setdefault("sector_status", {})
            sectors["gradient_phase_field_causality"] = (
                "PASS_EXTERNAL_FIXED_PARAMETER_COMPARATOR_ONLY"
            )
            sectors["fixed_light_cone_parameter_domain"] = (
                "PASS_NORMALIZED_ANALYTIC"
            )
            sectors["uniform_subluminal_phase_field_limit"] = (
                "NO_GO_FOR_EXACT_PARABOLIC_LIMIT"
            )
            sectors["local_current_law_mapping"] = (
                "PASS_ALGEBRAIC_MOBILITY_ONE"
            )
            sectors["uet_covariant_phase_field_mapping"] = "BLOCKED"
            sectors["entropy_current_kms_completion"] = "BLOCKED"
            payload["reason"] = (
                "Exact normalized fixed-cone inequalities and a local "
                "mobility-one current-law map are verified, but the external "
                "order parameter is not mapped to the UET Noether density."
            )
            payload["status"] = "BLOCKED"
            payload["claim_promotion"] = "BLOCKED"
            payload["global_universe_closure"] = "UNRESOLVED"
            payload["topic_0_11_status_impact"] = "NONE"
            payload["topic_0_19_status_impact"] = "NONE"
            continue
        payload["program_stage"] = LATEST_STAGE
        payload["controlling_blocker"] = LATEST_CONTROLLER
        sectors = payload.setdefault("sector_status", {})
        sectors["gradient_phase_field_causality"] = (
            "PASS_EXTERNAL_FIXED_PARAMETER_COMPARATOR_ONLY"
        )
        sectors["uniform_subluminal_phase_field_limit"] = "BLOCKED"
        sectors["uet_covariant_phase_field_mapping"] = "BLOCKED"
        payload["reason"] = (
            "A sourced external first-order hyperbolic phase-field comparator "
            "closes at formula level for fixed parameters, but it is not "
            "UET-derived and its parabolic Cahn-Hilliard scaling is not "
            "uniformly subluminal."
        )
        payload["status"] = "BLOCKED"
        payload["claim_promotion"] = "BLOCKED"
        payload["global_universe_closure"] = "UNRESOLVED"
        payload["topic_0_11_status_impact"] = "NONE"
        payload["topic_0_19_status_impact"] = "NONE"
    return True
