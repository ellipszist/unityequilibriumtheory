"""Boundary tests for the Topic 0.13 dimensional-observable gate."""

from docs.scripts.audit.audit_uet_main_theory_dimensional_observable import build_artifacts


def test_dimensional_gate_blocks_without_fabricating_calibration() -> None:
    audit, gate = build_artifacts()
    assert audit["audit_status"] == "PASS_ACCOUNTING"
    assert gate["dimensional_observable_status"] == "BLOCKED"
    assert gate["holdout_status"] == "LOCKED_UNCONSUMED"
    assert gate["claim_promotion"] is False


def test_all_three_controlling_gaps_remain_explicit() -> None:
    _, gate = build_artifacts()
    assert set(gate["controlling_blockers"]) == {
        "thermal_numeric_source_package_missing",
        "alpha_phi_k_independent_calibration_missing",
        "thermal_prearrival_leakage_gate_failed",
    }
