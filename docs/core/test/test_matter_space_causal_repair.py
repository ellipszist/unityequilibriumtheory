"""Tests for the causal discretization repair boundary."""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "artifacts" / "causal_discretization_repair_artifact.json"


def load() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def test_reference_repair_passes_but_full_candidate_stays_blocked() -> None:
    artifact = load()
    assert artifact["repair_status"] == "REFERENCE_PASS_FULL_COUPLED_INTEGRATION_OPEN"
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


def test_next_controller_is_full_coupled_energy_and_functional_integration() -> None:
    artifact = load()
    assert artifact["controlling_blocker"] == "full_coupled_causal_scheme_energy_and_functional_integration_missing"
    assert artifact["checks"]["reference_energy_ledger_closed"] is False
    assert artifact["checks"]["full_coupled_integration_closed"] is False
    assert any("shared discrete energy/ledger relation" in item for item in artifact["integration_requirements"])
