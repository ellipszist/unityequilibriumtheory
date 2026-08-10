from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GATE = ROOT / "docs/core/artifacts/uet_major_result_dependency_unlock_gate.json"


def test_downstream_major_results_remain_blocked_until_topic13_core_ready() -> None:
    artifact = json.loads(GATE.read_text(encoding="utf-8-sig"))
    assert artifact["claim_promotion"] is False
    assert artifact["status"] == "BLOCKED_DOWNSTREAM_MAJOR_RESULTS"
    assert artifact["decisions"]["CORE_CURVED_3P1_OBSERVABLE_PARENT_READY"]["status"] == "BLOCKED_DEPENDENCY"
    assert artifact["decisions"]["GR_CLASSICAL_COMPATIBILITY_LANE"]["status"] == "BLOCKED_DEPENDENCY"
    assert artifact["decisions"]["CONSTITUTIVE_TRANSPORT_CORE_LANE"]["status"] == "BLOCKED_DEPENDENCY"
    assert artifact["decisions"]["GALAXY_COMPATIBILITY_TRACK"]["status"] == "BLOCKED_DEPENDENCY"
