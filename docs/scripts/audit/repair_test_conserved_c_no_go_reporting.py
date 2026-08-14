"""Update the causal no-go regression test for split baseline/lane reporting."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/core/test/test_conserved_c_no_go_assessment.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = '''    assert causal["full_candidate_pass"] is False
    assert gate["status"] == "BLOCKED_OPEN_T13_FULL_BRIDGE"
    assert gate["controlling_blocker"] == (
        "dimensional_phi_energy_anchor_or_independent_alpha_calibration_missing"
    )
    assert causal["controlling_blocker"] == "original_conserved_c_gradient_baseline_blocked"
'''
    new = '''    assert causal["full_candidate_pass"] is False
    assert causal["baseline_status"] == "BLOCKED"
    assert causal["structural_question_closure"] == "CLOSED_AS_NO_GO"
    assert any("original conserved-C" in item for item in gate["major_result"]["baseline_open_items"])
    assert gate["status"] == "BLOCKED_OPEN_T13_FULL_BRIDGE"
    assert gate["controlling_blocker"] == (
        "dimensional_phi_energy_anchor_or_independent_alpha_calibration_missing"
    )
    assert "original_conserved_c_gradient_baseline_blocked" not in gate["major_result"]["what_remains_open"]
'''
    if new not in text:
        if old not in text:
            raise SystemExit("causal regression test anchor not found")
        text = text.replace(old, new, 1)
        TARGET.write_text(text, encoding="utf-8")
    print("PASS_REPAIRED_CONSERVED_C_NO_GO_REPORTING_TEST")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
