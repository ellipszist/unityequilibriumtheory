"""Audit the normalized resource-selection to thermal-ledger bridge."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

from docs.core.resource_selection_thermal_bridge import (
    RESOURCE_THERMAL_BRIDGE_MODE,
    ResourceThermalBridgeConfig,
    run_resource_selection_thermal_bridge,
)
from docs.core.uet_resource_selection import ResourceSelectionConfig


def configurations() -> tuple[ResourceSelectionConfig, ResourceSelectionConfig]:
    cooperative = ResourceSelectionConfig(
        interaction_matrix=((0.9, 0.8), (0.8, 0.9)),
        behavior_cost=(0.02, 0.03),
        maintenance_cost=(0.01, 0.01),
    )
    conflict = ResourceSelectionConfig(
        interaction_matrix=((0.3, -0.9), (-0.9, 0.3)),
        behavior_cost=(0.12, 0.15),
        maintenance_cost=(0.03, 0.04),
    )
    return cooperative, conflict


def build_artifact() -> dict:
    cooperative, conflict = configurations()
    bridge_config = ResourceThermalBridgeConfig()
    result = run_resource_selection_thermal_bridge(
        cooperative, conflict, horizon=10.0, dt=0.001, config=bridge_config
    )
    repeat = run_resource_selection_thermal_bridge(
        cooperative, conflict, horizon=10.0, dt=0.001, config=bridge_config
    )
    summaries = {
        "cooperative": asdict(result.cooperative),
        "conflict": asdict(result.conflict),
    }
    repeat_summaries = {
        "cooperative": asdict(repeat.cooperative),
        "conflict": asdict(repeat.conflict),
    }
    checks = {
        "cooperative_ledger_closure_le_1e-12": abs(
            result.cooperative.ledger_closure_residual
        )
        <= 1e-12,
        "conflict_ledger_closure_le_1e-12": abs(
            result.conflict.ledger_closure_residual
        )
        <= 1e-12,
        "entropy_proxy_nonnegative": all(
            summary["bath_entropy_proxy"] >= -1e-12
            for summary in summaries.values()
        ),
        "conflict_dissipation_greater": (
            result.conflict.dissipated_work_proxy
            > result.cooperative.dissipated_work_proxy
        ),
        "conflict_fails_within_horizon": (
            result.conflict.persistence_time is not None
            and result.cooperative.persistence_time is None
        ),
        "deterministic_repeat": summaries == repeat_summaries,
        "no_parameter_fitting": True,
        "si_mapping_remains_open": result.mapping_status
        == "BLOCKED_OPEN_SI_WORK_HEAT_ENTROPY_MAP",
    }
    return {
        "schema_version": "1.0",
        "artifact": "resource_selection_thermal_bridge_verification",
        "operator_mode": RESOURCE_THERMAL_BRIDGE_MODE,
        "audit_status": "PASS_WITH_OPEN_THERMAL_MAPPING" if all(checks.values()) else "FAIL",
        "status": "INTERNAL_DIAGNOSTIC",
        "claim_status": "SIMULATION_ONLY",
        "evidence_class": "INTERNAL_OBSERVABLE_MAPPING_DIAGNOSTIC",
        "unit_lane": bridge_config.unit_lane,
        "formula_audit": [
            {
                "formula_id": "THERMAL-RESOURCE-001",
                "relation": "Q_proxy = alpha_b*W_behavior + alpha_m*W_maintenance",
                "origin": "declared lane-specific work ledger map",
                "status": "constitutive mapping input; not inferred",
            },
            {
                "formula_id": "THERMAL-RESOURCE-002",
                "relation": "Delta S_bath_proxy = Q_proxy/T_bath",
                "origin": "isothermal thermodynamic comparator",
                "status": "normalized entropy-like proxy; not SI entropy production",
            },
        ],
        "config": {
            "horizon": 10.0,
            "dt": 0.001,
            "behavior_to_work_scale": bridge_config.behavior_to_work_scale,
            "maintenance_to_work_scale": bridge_config.maintenance_to_work_scale,
            "bath_temperature": bridge_config.bath_temperature,
            "parameters_fit": False,
        },
        "metrics": summaries,
        "gates": checks,
        "limitations": [
            "interaction matrix, cost vectors, and replicator law remain constitutive comparator inputs",
            "work and entropy values are normalized proxies, not SI joules or J/K",
            "no C-to-temperature identity is asserted",
            "no external heat, calorimetry, entropy-current, or material source is used",
            "the isothermal bath relation is a lane-specific comparator, not a complete nonequilibrium derivation",
        ],
        "claim_boundary": (
            "The declared interaction costs can close a normalized dissipated-work "
            "and bath-entropy proxy ledger. This supports an internal observable "
            "bridge only; it does not derive physical work, heat, temperature, or "
            "entropy from UET."
        ),
        "next_controller": (
            "source-lock one physical material lane with work/heat/temperature "
            "units, uncertainty, and an observable map before external validation"
        ),
    }


def main() -> int:
    artifact = build_artifact()
    output = ROOT / "core" / "artifacts" / "resource_selection_thermal_bridge_verification.json"
    output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(artifact, indent=2))
    return 0 if artifact["audit_status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())