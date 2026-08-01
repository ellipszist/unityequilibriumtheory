"""Synchronize Topic 0.11/0.13 pilot claims with current core lane decisions.

This audit does not rerun topic simulations.  It prevents old pilot artifacts
from being read as if they used the newly selected characteristic lane.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]


def load(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def build_artifact() -> dict[str, Any]:
    lane = load("docs/core/artifacts/matter_space_causal_lane_selection.json")
    characteristic = load("docs/core/artifacts/matter_space_characteristic_cone_verification.json")
    phase = load("docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_matter_space_phase_coupling_diagnostic.json")
    thermal = load("docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/matter_space_thermal_control.json")
    phase_rerun = load("docs/topics/0.11_Phase_Transitions/Result/artifacts/matter_space_0_11_characteristic_lane_rerun.json")
    thermal_rerun = load("docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/matter_space_0_13_characteristic_thermal_lane_rerun.json")
    observable = load("docs/core/artifacts/matter_space_observable_verification.json")
    thermal_map = load("docs/core/artifacts/thermal_observable_bridge_verification.json")
    resource_map = load("docs/core/artifacts/resource_selection_thermal_bridge_verification.json")

    checks = {
        "selected_characteristic_lane_passes": (
            lane["selected_lane"]["operator_mode"] == "matter_space_characteristic_cone_v1"
            and characteristic["audit_status"] == "PASS"
        ),
        "phase_pilot_remains_internal_simulation_only": (
            phase["status"] == "INTERNAL_DIAGNOSTIC"
            and phase["simulation_status"] == "SIMULATION_ONLY"
            and phase["dependency_status"] == "BLOCKED"
        ),
        "phase_pilot_controller_preserved": bool(phase.get("controller")),
        "phase_selected_lane_rerun_passes": phase_rerun["verification_status"] == "PASS",
        "thermal_pilot_remains_simulation_only": (
            thermal["status"] == "SIMULATION_ONLY"
            and thermal["dependency_status"] == "BLOCKED"
        ),
        "thermal_prearrival_blocker_preserved": (
            thermal["gates"]["prearrival_leakage"] is False
        ),
        "thermal_mapping_boundary_preserved": (
            thermal_map["status"] == "BLOCKED_OPEN_MAPPING"
            and resource_map["audit_status"] == "PASS_WITH_OPEN_THERMAL_MAPPING"
        ),
        "normalized_observable_contract_passes": observable["audit_status"] == "PASS_WITH_OPEN_SI_MAPPING",
        "thermal_selected_lane_rerun_passes": thermal_rerun["verification_status"] == "PASS",
        "external_validation_not_claimed": (
            thermal["external_validation"] is False
            and thermal_map["claim_status"] == "SIMULATION_ONLY"
            and resource_map["claim_status"] == "SIMULATION_ONLY"
        ),
    }
    return {
        "schema_version": "1.0",
        "artifact": "matter_space_topic_pilot_sync",
        "audit_status": "PASS_WITH_INHERITED_BLOCKERS" if all(checks.values()) else "FAIL",
        "claim_status": "INTERNAL_DIAGNOSTIC_ONLY",
        "selected_core_lane": {
            "operator_mode": lane["selected_lane"]["operator_mode"],
            "status": lane["selected_lane"]["status"],
            "claim_status": lane["selected_lane"]["claim_status"],
            "artifact": lane["selected_lane"]["artifact"],
        },
        "topic_0_11": {
            "status": "SYNCED_INTERNAL_DIAGNOSTIC",
            "source_artifact": "docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_matter_space_phase_coupling_diagnostic.json",
            "prior_operator_mode": phase["operator_mode"],
            "selected_lane_available": True,
            "selected_lane_rerun_artifact": "docs/topics/0.11_Phase_Transitions/Result/artifacts/matter_space_0_11_characteristic_lane_rerun.json",
            "rerun_status": "RERUN_SELECTED_LANE_PASS_SIMULATION_ONLY",
            "controller": phase["controller"],
            "claim_boundary": "normalized simulation-only diagnostic; no universality, mass-generation, particle, or empirical claim",
        },
        "topic_0_13": {
            "status": "SYNCED_SIMULATION_ONLY",
            "source_artifact": "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/matter_space_thermal_control.json",
            "prior_operator_mode": thermal["operator_mode"],
            "selected_lane_available": True,
            "selected_lane_rerun_artifact": "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/matter_space_0_13_characteristic_thermal_lane_rerun.json",
            "rerun_status": "RERUN_SELECTED_LANE_PASS_SIMULATION_ONLY_OPEN_SI_MAPPING",
            "controller": thermal["controlling_blocker"],
            "claim_boundary": "Fourier/Cattaneo/trace and normalized matter-space diagnostic; no external validation or SI C-to-T identity",
        },
        "new_internal_bridge": {
            "artifact": "docs/core/artifacts/resource_selection_thermal_bridge_verification.json",
            "status": resource_map["audit_status"],
            "claim_boundary": resource_map["claim_boundary"],
        },
        "checks": checks,
        "next_controller": (
            "preserve 0.11/0.13 selected-lane reruns as simulation-only; close SI "
            "observable mapping and external-data gates before validation claims"
        ),
    }


def main() -> int:
    artifact = build_artifact()
    output = ROOT / "docs/core/artifacts/matter_space_topic_pilot_sync.json"
    output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(artifact, indent=2))
    return 0 if artifact["audit_status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
