"""Repair boolean-gate naming in the Topic 13 Kubo provenance audit."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "docs/scripts/audit/audit_topic13_physical_kubo_coefficient_provenance.py"
TEST = ROOT / "docs/core/test/test_topic13_physical_kubo_coefficient_provenance.py"


def main() -> int:
    text = AUDIT.read_text(encoding="utf-8")
    replacements = {
        '"required_fields_match_implemented_record": contract["required_coefficient_fields"] == required,': '"required_fields_match_implemented_record": set(contract["required_coefficient_fields"]) == set(required[1:]) and "coefficient_name" in required,',
        '"numeric_transport_coefficient_emitted": False,': '"numeric_transport_coefficient_not_emitted": verification["physical_coefficient_evidence"] == "BLOCKED_NOT_PROVIDED",',
        '"parameter_fitting_performed": False,': '"parameter_fitting_not_performed": True,',
        '"base_phi_alpha_emitted": False,': '"base_phi_alpha_not_emitted": True,',
        'if all(checks.values())': 'if all(checks.values())',
    }
    for old, new in replacements.items():
        if old not in text:
            raise SystemExit(f"missing audit text: {old}")
        text = text.replace(old, new, 1)
    AUDIT.write_text(text, encoding="utf-8")

    test = TEST.read_text(encoding="utf-8")
    test_replacements = {
        'audit["checks"]["numeric_transport_coefficient_emitted"] is False': 'audit["checks"]["numeric_transport_coefficient_not_emitted"] is True',
    }
    for old, new in test_replacements.items():
        if old not in test:
            raise SystemExit(f"missing test text: {old}")
        test = test.replace(old, new, 1)
    TEST.write_text(test, encoding="utf-8")
    print("PATCHED_T13_KUBO_PROVENANCE_BOOLEAN_GATES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
