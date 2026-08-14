"""Repair contract-field and zero-residual predicates in the ideal-lane audit."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_uet_o2_condensate_goldstone_ideal_lane.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old_trace = '        "trace_is_absent_and_has_no_backreaction": response_contract["derived_trace_input"] is False and response_contract["derived_trace_backreaction"] is False and transport_contract["trace_input"] is False and transport_contract["trace_backreaction"] is False,\n'
    new_trace = '        "trace_is_absent_and_has_no_backreaction": response_contract["derived_trace_imported"] is False and response_contract["derived_trace_backreaction"] is False and transport_contract["trace_input"] is False and transport_contract["trace_backreaction"] is False,\n'
    if old_trace not in text:
        raise SystemExit("expected trace contract predicate was not found")
    text = text.replace(old_trace, new_trace, 1)

    old_phi = '        "Phi_is_response_input": "response" in response_contract["interaction"].lower() and "Phi" not in eos_contract["conserved_coordinate"],\n'
    new_phi = '        "Phi_is_response_input": response_contract["normalized_matter_space_map"] == "PARTIAL_RESPONSE_ONLY" and "Phi" not in eos_contract["conserved_coordinate"],\n'
    if old_phi not in text:
        raise SystemExit("expected Phi predicate was not found")
    text = text.replace(old_phi, new_phi, 1)

    old_zero = '''        "stationarity_closes": relative_error(
            (mass_sq - eos_config.matter.matter_kinetic * MU**2) * amplitude
            + eos_config.matter.matter_quartic * amplitude**3,
            0.0,
        ) <= 1.0e-12,
'''
    new_zero = '''        "stationarity_closes": abs(
            (mass_sq - eos_config.matter.matter_kinetic * MU**2) * amplitude
            + eos_config.matter.matter_quartic * amplitude**3
        ) <= 1.0e-12,
'''
    if old_zero not in text:
        raise SystemExit("expected stationarity predicate was not found")
    text = text.replace(old_zero, new_zero, 1)
    TARGET.write_text(text, encoding="utf-8")
    print("REPAIRED_TOPIC13_UET_O2_CONDENSATE_GOLDSTONE_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
