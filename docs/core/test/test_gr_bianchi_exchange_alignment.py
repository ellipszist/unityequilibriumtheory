"""Artifact alignment tests for the covariant balance wave."""

from __future__ import annotations

import json
from pathlib import Path

from docs.scripts.audit.audit_uet_gr_covariant_balance import build_artifacts

ARTIFACT_DIR = Path(__file__).resolve().parents[1] / "artifacts"


def _read(name: str) -> dict[str, object]:
    return json.loads((ARTIFACT_DIR / name).read_text(encoding="utf-8"))


def test_balance_verification_passes_local_identity_gates() -> None:
    artifact = _read("covariant_bianchi_exchange_verification.json")
    assert artifact["status"] == "PASS"
    assert set(artifact["gates"].values()) == {"PASS"}
    assert artifact["symbolic"]["identity_exact"] is True
    assert artifact["numeric"]["identity_max_abs_difference"] <= 1e-12
    assert artifact["run_contract"]["curved_derivative_solver"] is False
    assert artifact["run_contract"]["causal_kernel"] is False
    assert artifact["run_contract"]["global_energy_theorem"] is False


def test_exchange_contract_separates_matter_number_and_stress_balance() -> None:
    artifact = _read("covariant_exchange_contract.json")
    assert artifact["status"] == "CANDIDATE"
    assert "-epsilon_nc" in artifact["matter_stress_balance"]
    assert "+epsilon_nc" in artifact["response_balance"]
    assert "independent" in artifact["matter_number_balance"]
    assert artifact["global_universe_closure"] == "UNRESOLVED"
    assert artifact["derived_trace_backreaction"] is False


def test_program_gate_advances_controller_without_topic_promotion() -> None:
    artifact = _read("uet_gr_research_program_gate.json")
    assert artifact["status"] == "BLOCKED"
    assert artifact["program_stage"] in {
        "COVARIANT_CONSERVATIVE_BALANCE_VERIFIED",
        "CAUSAL_NONCLOSED_CONSTITUTIVE_KERNEL_VERIFIED",
        "CONTROLLED_RESPONSE_REDUCTION_PARTIAL",
    }
    assert artifact["sector_status"]["covariant_exchange_bianchi_balance"] == "PASS"
    assert artifact["sector_status"]["causal_nonclosed_sector"] in {
        "NOT_IMPLEMENTED",
        "PASS_CONSTITUTIVE_1P1D",
    }
    assert artifact["controlling_blocker"] in {
        "causal_nonclosed_influence_functional_missing",
        "controlled_covariant_to_matter_space_reduction_missing",
        "covariant_matter_action_and_reciprocal_coupling_missing",
    }
    assert artifact["topic_0_19_status_impact"] == "NONE"
    assert artifact["claim_promotion"] == "BLOCKED"


def test_in_memory_balance_artifacts_match_persisted_gate_state() -> None:
    verification, contract, program = build_artifacts()
    assert verification["gates"] == _read("covariant_bianchi_exchange_verification.json")["gates"]
    assert contract["status"] == _read("covariant_exchange_contract.json")["status"]
    assert program["controlling_blocker"] == _read("uet_gr_research_program_gate.json")["controlling_blocker"]
