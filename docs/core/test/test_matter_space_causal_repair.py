"""Tests for the causal discretization repair boundary."""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "artifacts" / "causal_discretization_repair_artifact.json"


def load() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def test_reference_repair_passes_but_full_candidate_stays_blocked() -> None:
    artifact = load()
    assert artifact["repair_status"] == "REFERENCE_AND_PHI_AND_SPLIT_LEDGER_PASS_RESPONSE_CONE_OPEN"
    assert artifact["reference_status"] == "PASS"
    assert artifact["default_full_candidate_status"] == "BLOCKED"
    assert artifact["status"] == "BLOCKED"


def test_reference_has_compact_support_without_numerical_padding() -> None:
    artifact = load()
    checks = artifact["checks"]
    assert checks["reference_compact_support"] is True
    assert checks["reference_uses_strict_cfl"] is True
    assert checks["no_clipping_or_cone_padding"] is True
    assert artifact["reference_lane"]["metrics"]["prearrival_leakage_fraction"] == 0.0


def test_next_controller_is_changing_C_response_cone_integration() -> None:
    artifact = load()
    assert artifact["controlling_blocker"] == "changing_C_response_cone_and_full_operator_integration_missing"
    assert artifact["checks"]["reference_energy_ledger_closed"] is True
    assert artifact["checks"]["causal_discrete_gradient_partial_closure"] is True
    assert artifact["checks"]["causal_split_shared_ledger_pass"] is True
    assert artifact["checks"]["full_coupled_integration_closed"] is False
    assert any("changing-C response cone" in item for item in artifact["integration_requirements"])
