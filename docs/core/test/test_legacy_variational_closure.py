import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "docs/core/artifacts/uet_legacy_variational_closure.json"


def load_artifact():
    return json.loads(ARTIFACT.read_text(encoding="utf-8-sig"))


def test_legacy_variational_audit_is_generated_and_blocked():
    artifact = load_artifact()
    assert artifact["audit_status"] == "PASS"
    assert artifact["closure_status"] == "BLOCKED"
    assert artifact["controlling_blockers"] == [
        "legacy_potential_derivative_pair",
        "legacy_information_gradient_sign",
    ]


def test_potential_pair_has_large_finite_difference_residual():
    artifact = load_artifact()
    finding = next(item for item in artifact["findings"] if item["finding_id"] == "legacy_potential_derivative_pair")
    assert finding["status"] == "CONTRADICTION"
    assert finding["metrics"]["finite_difference_max_absolute_residual"] > finding["metrics"]["threshold"]


def test_information_source_sign_is_explicitly_opposite():
    artifact = load_artifact()
    finding = next(item for item in artifact["findings"] if item["finding_id"] == "legacy_information_gradient_sign")
    assert finding["status"] == "CONTRADICTION"
    assert finding["expected_source_sign"] == -1
    assert finding["coded_source_sign"] == 1
    assert finding["c_source_sign_matches"] is True
