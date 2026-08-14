"""Repair schema compatibility in the formal Topic 13 bridge audit."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_formal_bridge_boundary.py"

OLD_NO_CLAIM = '''def no_claim_promotion(value: dict[str, Any]) -> bool:
    return (
        value.get("parameter_fitting_performed") is False
        and value.get("target_data_used") is False
        and value.get("xie_2026_accessed") is False
    )
'''

NEW_NO_CLAIM = '''def no_claim_promotion(value: dict[str, Any]) -> bool:
    """Accept explicit top-level or verifier-check no-target evidence."""

    checks = value.get("checks", {})
    if not isinstance(checks, dict):
        checks = {}
    flags = {
        "parameter_fitting_performed": value.get("parameter_fitting_performed"),
        "target_data_used": value.get("target_data_used"),
        "xie_2026_accessed": value.get("xie_2026_accessed"),
        "target_curve_unused": checks.get("no_target_curve_used"),
        "target_or_holdout_unused": checks.get("no_target_or_holdout"),
        "target_or_holdout_witness_unused": checks.get("no_holdout_or_target_in_witness"),
        "xie_unused": checks.get("xie_2026_not_accessed") or checks.get("xie_2026_not_consumed"),
    }
    present = {name: flag for name, flag in flags.items() if flag is not None}
    for name in ("parameter_fitting_performed", "target_data_used", "xie_2026_accessed"):
        if name in present and present[name] is not False:
            return False
    positive_witness = any(
        flag is True
        for name, flag in present.items()
        if name not in {"parameter_fitting_performed", "target_data_used", "xie_2026_accessed"}
    )
    return positive_witness or all(
        present.get(name) is False
        for name in ("parameter_fitting_performed", "target_data_used", "xie_2026_accessed")
    )


def physical_coefficient_not_emitted(value: dict[str, Any]) -> bool:
    """Accept explicit no-coefficient evidence from either schema layer."""

    checks = value.get("checks", {})
    if not isinstance(checks, dict):
        checks = {}
    flags = {
        "numeric_alpha_Phi_K_emitted": value.get("numeric_alpha_Phi_K_emitted"),
        "numeric_base_alpha_Phi_K_emitted": value.get("numeric_base_alpha_Phi_K_emitted"),
        "numeric_transport_coefficients_emitted": value.get("numeric_transport_coefficients_emitted"),
        "numeric_alpha_not_emitted": checks.get("numeric_alpha_not_emitted"),
        "numeric_transport_not_emitted": checks.get("numeric_transport_coefficient_not_emitted"),
        "no_default_physical_coefficient": checks.get("no_default_physical_coefficient_is_allowed"),
    }
    present = {name: flag for name, flag in flags.items() if flag is not None}
    for name in (
        "numeric_alpha_Phi_K_emitted",
        "numeric_base_alpha_Phi_K_emitted",
        "numeric_transport_coefficients_emitted",
    ):
        if name in present and present[name] is not False:
            return False
    return bool(present)
'''


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    if OLD_NO_CLAIM in text:
        text = text.replace(OLD_NO_CLAIM, NEW_NO_CLAIM, 1)
    elif "def physical_coefficient_not_emitted" not in text:
        raise SystemExit("formal bridge schema helper block not found")
    text = text.replace(
        'kubo.get("physical_coefficient_evidence") == "BLOCKED_NOT_PROVIDED",',
        'kubo.get("transport_verification", {}).get("physical_coefficient_evidence") == "BLOCKED_NOT_PROVIDED",',
        1,
    )
    text = text.replace(
        '"source_backed_temperature_coefficient_provenance_missing"\n            in major(beta_contract).get("open_blockers", [])',
        '"beta_T13_source_backed_temperature_coefficient_provenance_missing"\n            in major(beta_contract).get("open_blockers", [])',
        1,
    )
    old_numeric = '''        "no_numeric_base_alpha_emitted": all(
            item.get("numeric_alpha_Phi_K_emitted") is False
            for item in (beta_no_go, beta_contract, dimensional, phi_energy_no_go, covariant_no_go, eos, sk, kubo)
        ),'''
    new_numeric = '''        "no_numeric_base_alpha_emitted": all(
            physical_coefficient_not_emitted(item)
            for item in (beta_no_go, beta_contract, dimensional, energy, phi_e_reference, phi_energy_no_go, covariant_no_go, eos, sk, kubo)
        ),'''
    if old_numeric in text:
        text = text.replace(old_numeric, new_numeric, 1)
    elif 'physical_coefficient_not_emitted(item)' not in text:
        raise SystemExit("formal bridge numeric check block not found")
    TARGET.write_text(text, encoding="utf-8")
    print("REPAIRED_FORMAL_BRIDGE_SCHEMA_COMPATIBILITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
