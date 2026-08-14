"""Extend the formal bridge audit for legacy Topic 13 evidence schemas."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_formal_bridge_boundary.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = (
        '        "target_or_holdout_witness_unused": checks.get("no_holdout_or_target_in_witness"),\n'
        '        "xie_unused": checks.get("xie_2026_not_accessed") or checks.get("xie_2026_not_consumed"),\n'
    )
    new = (
        '        "target_or_holdout_witness_unused": checks.get("no_holdout_or_target_in_witness"),\n'
        '        "target_not_used": checks.get("target_data_not_used"),\n'
        '        "prior_no_go_target_unused": checks.get("no_target_or_holdout_in_prior_no_go"),\n'
        '        "holdout_unused": checks.get("holdout_not_accessed") or checks.get("holdout_not_consumed"),\n'
        '        "calibration_excludes_holdout": checks.get("calibration_path_excludes_holdout"),\n'
        '        "xie_unused": checks.get("xie_2026_not_accessed") or checks.get("xie_2026_not_consumed"),\n'
    )
    if old not in text:
        raise SystemExit("formal bridge no-claim flag block not found")
    text = text.replace(old, new, 1)

    old = (
        '        "numeric_alpha_not_emitted": checks.get("numeric_alpha_not_emitted"),\n'
        '        "numeric_transport_not_emitted": checks.get("numeric_transport_coefficient_not_emitted"),\n'
        '        "no_default_physical_coefficient": checks.get("no_default_physical_coefficient_is_allowed"),\n'
    )
    new = (
        '        "numeric_alpha_not_emitted": checks.get("numeric_alpha_not_emitted"),\n'
        '        "base_alpha_not_calibrated": checks.get("no_base_alpha_calibration_emitted"),\n'
        '        "numeric_transport_not_emitted": checks.get("numeric_transport_coefficient_not_emitted"),\n'
        '        "no_default_physical_coefficient": checks.get("no_default_physical_coefficient_is_allowed"),\n'
    )
    if old not in text:
        raise SystemExit("formal bridge coefficient flag block not found")
    text = text.replace(old, new, 1)
    TARGET.write_text(text, encoding="utf-8")
    print("REPAIRED_FORMAL_BRIDGE_SCHEMA_COMPATIBILITY_V2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
