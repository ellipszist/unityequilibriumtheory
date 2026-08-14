"""Regression checks for the conditional natural-unit action route."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "docs/core/artifacts/t13_covariant_action_si_anchor_route_audit.json"


def test_action_route_is_natural_only_and_si_mapping_is_blocked() -> None:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8-sig"))
    assert artifact["status"] == "PASS_NATURAL_UNIT_ROUTE_IDENTIFIED_SI_MAPPING_BLOCKED"
    assert artifact["major_result"]["closure_level"] == "CLOSED_FOR_LANE"
    assert artifact["checks"]["formula_defaults_not_physical"] is True
    assert artifact["checks"]["formula_si_gate_open"] is True
    assert artifact["controlling_blocker"] == "system_specific_SI_contract_and_covariant_Phi_to_normalized_Phi_map_missing"
