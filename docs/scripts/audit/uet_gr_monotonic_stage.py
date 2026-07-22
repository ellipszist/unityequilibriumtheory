"""Preserve the newest verified GR-program stage during upstream reruns.

The GR research chain is intentionally rerunnable from its earliest audit.
Earlier generators must therefore recognize later stable artifacts instead of
silently moving the shared program gate backwards.  This helper applies only
when the sourced hyperbolic phase-field comparator artifact is present and
passes its strict audit.
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


def apply_latest_hyperbolic_phase_field_stage(
    out: Path,
    *payloads: dict[str, Any],
) -> bool:
    """Apply the latest downstream stage to earlier generated payloads."""

    comparator = _load_comparator(out)
    if comparator is None:
        return False
    for payload in payloads:
        _update_payload(payload, comparator)
    for payload in payloads:
        if payload.get("artifact") != "uet_gr_research_program_gate":
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
