from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_PATH = ROOT / "docs/core/artifacts/uet_major_result_closure_contract.json"
REGISTER_PATH = ROOT / "docs/core/artifacts/uet_major_result_closure_register.json"
T13_GATE_PATH = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/topic13_full_thermodynamic_bridge_core_ready_gate.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def test_major_result_contract_has_required_fields_and_levels() -> None:
    contract = load(CONTRACT_PATH)
    assert contract["claim_promotion"] is False
    assert "CLOSED_FOR_CORE" in contract["closure_levels"]
    assert "major_result_id" in contract["required_fields"]
    assert "WHAT_IS_ACTUALLY_CLOSED" in contract["required_report_headings"]


def test_register_reports_results_without_counting_pass_as_closure() -> None:
    contract = load(CONTRACT_PATH)
    register = load(REGISTER_PATH)
    required = set(contract["required_fields"])
    allowed = set(contract["closure_levels"])
    assert register["claim_promotion"] is False
    assert register["closure_levels_are_progress_labels_not_readiness_labels"] is True
    for entry in register["entries"]:
        assert required <= set(entry)
        assert entry["closure_level"] in allowed
    o2 = next(entry for entry in register["entries"] if entry["major_result_id"] == "CORE_O2_TREE_LEVEL_EOS_LANE")
    assert o2["verification_status"] == "PASS_TREE_LEVEL_PARTIAL"
    assert o2["closure_level"] == "PARTIAL"


def test_topic13_full_gate_preserves_current_blockers_and_holdout_boundary() -> None:
    gate = load(T13_GATE_PATH)
    assert gate["status"] == "BLOCKED_OPEN_T13_FULL_BRIDGE"
    assert gate["major_result"]["closure_level"] == "PARTIAL"
    causal = gate["verification_status"]["causal_full_candidate_or_formal_no_go_branch"]
    assert causal["status"] == "BLOCKED"
    assert causal["status_role"] == "full_candidate_readiness_gate"
    assert causal["lane_status"] == "PASS"
    assert causal["lane_closure_level"] == "CLOSED_FOR_LANE"
    assert gate["verification_status"]["alpha_Phi_K"]["status"] == "BLOCKED"
    assert gate["verification_status"]["holdout_integrity"]["status"] == "PASS"
    assert gate["verification_status"]["holdout_integrity"]["holdout_consumed"] is False
    assert gate["equation_or_mapping"]["dimensional"] == "Delta_Tq = alpha_Phi_K * Delta_Phi"
    assert gate["claim_promotion"] is False
