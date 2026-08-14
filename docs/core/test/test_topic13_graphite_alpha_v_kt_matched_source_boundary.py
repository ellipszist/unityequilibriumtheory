from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT_REL = "docs/core/artifacts/t13_graphite_alpha_v_kt_matched_source_boundary_audit.json"
FULL_REL = "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/topic13_full_thermodynamic_bridge_core_ready_gate.json"
REGISTER_REL = "docs/core/artifacts/uet_major_result_closure_register.json"
DEPENDENCY_REL = "docs/core/artifacts/uet_major_result_dependency_unlock_gate.json"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def test_current_alpha_v_kt_inventory_is_closed_as_a_scoped_boundary() -> None:
    audit = load(AUDIT_REL)
    assert audit["status"] == "PASS_SCOPED_GRAPHITE_ALPHA_V_K_T_MATCHED_SOURCE_BOUNDARY_NO_GO"
    assert audit["major_result"]["closure_level"] == "CLOSED_FOR_LANE"
    assert all(audit["checks"].values())
    assert audit["controlling_blocker"] == "same_grade_alpha_V_and_K_T_missing"
    assert audit["claim_boundary"].startswith("No numeric Cp-to-Cv correction")
    assert audit["source_pair_observations"]["hanfland_kt"]["same_state_alpha_V_available"] is False
    assert audit["source_pair_observations"]["bosak_elastic_bulk"]["thermal_K_T_claimed"] is False
    assert audit["source_pair_observations"]["tpg_alpha_v"]["same_specimen_for_both_axes"] is False
    assert audit["source_pair_observations"]["nelson_riley_alpha_v"]["same_specimen_alpha_V"] is False


def test_alpha_v_kt_boundary_is_projected_without_full_topic13_promotion() -> None:
    full = load(FULL_REL)
    register = load(REGISTER_REL)
    dependency = load(DEPENDENCY_REL)
    projected = full["verification_status"]["source_package"][
        "graphite_alpha_v_kt_matched_source_boundary"
    ]

    assert projected["major_result_id"] == "T13_GRAPHITE_ALPHA_V_K_T_MATCHED_SOURCE_BOUNDARY"
    assert projected["closure_level"] == "CLOSED_FOR_LANE"
    assert projected["audit"]["path"] == AUDIT_REL
    assert projected["audit"]["sha256"] == sha256(AUDIT_REL)
    assert any(item["path"] == AUDIT_REL for item in full["evidence_artifacts"])
    assert "same_grade_alpha_V_and_K_T_missing" in full["major_result"]["what_remains_open"]
    assert full["status"] == "BLOCKED_OPEN_T13_FULL_BRIDGE"
    assert full["claim_promotion"] is False
    assert any(
        item.get("major_result_id") == "T13_GRAPHITE_ALPHA_V_K_T_MATCHED_SOURCE_BOUNDARY"
        for item in register["entries"]
    )
    assert dependency["decisions"]["CORE_CURVED_3P1_OBSERVABLE_PARENT_READY"][
        "status"
    ] == "BLOCKED_DEPENDENCY"
