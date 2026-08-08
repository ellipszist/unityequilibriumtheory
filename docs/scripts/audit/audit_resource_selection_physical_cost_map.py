"""Audit the opt-in dimensional cost-map contract.

The audit proves contract behavior and deliberate blocking.  It does not claim
that a physical cost scale has been sourced or derived.
"""

from __future__ import annotations

import json
import sys
from math import isclose
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

from docs.core.resource_selection_physical_cost_map import (
    PHYSICAL_COST_MAP_OPERATOR_MODE,
    PHYSICAL_COST_MAP_STATUS,
    PhysicalCostMapRecord,
    PhysicalCostMapValidationError,
    map_normalized_work_to_si,
)


def main() -> int:
    open_record = PhysicalCostMapRecord(
        map_id="open-map",
        material_or_system="unresolved-material-lane",
    )
    open_rejected = False
    try:
        map_normalized_work_to_si(0.25, 0.1, open_record)
    except PhysicalCostMapValidationError:
        open_rejected = True

    fit_rejected = False
    try:
        PhysicalCostMapRecord(
            map_id="fit-map",
            material_or_system="target-material",
            behavior_energy_scale_j=2.0,
            maintenance_energy_scale_j=3.0,
            bath_temperature_k=300.0,
            source_locator="fit://target-data",
            source_hash="fit-only",
            uncertainty_record="not-independent",
            measurement_operator_id="heat",
            parameter_origin="fit",
        ).validate_contract()
    except PhysicalCostMapValidationError:
        fit_rejected = True

    fixture_record = PhysicalCostMapRecord(
        map_id="synthetic-contract-fixture",
        material_or_system="synthetic-material",
        behavior_energy_scale_j=2.0,
        maintenance_energy_scale_j=3.0,
        bath_temperature_k=300.0,
        source_locator="synthetic://physical-cost-contract",
        source_hash="fixture-hash",
        uncertainty_record="fixture-only; not external evidence",
        measurement_operator_id="integrated_heat_fixture",
        parameter_origin="test_fixture",
        status="TEST_ONLY",
    )
    fixture_result = map_normalized_work_to_si(0.25, 0.1, fixture_record)
    gates = {
        "open_map_is_rejected": open_rejected,
        "fit_origin_is_rejected": fit_rejected,
        "fixture_heat_formula_closes": isclose(
            fixture_result.heat_j, 0.8, rel_tol=0.0, abs_tol=1e-12
        ),
        "fixture_entropy_formula_closes": isclose(
            fixture_result.entropy_j_per_k, 0.8 / 300.0, rel_tol=0.0, abs_tol=1e-12
        ),
        "no_default_physical_scale": (
            open_record.behavior_energy_scale_j is None
            and open_record.maintenance_energy_scale_j is None
        ),
        "measurement_operator_is_explicit": bool(
            fixture_result.measurement_operator_id
        ),
    }
    artifact = {
        "schema_version": "1.0",
        "artifact": "resource_selection_physical_cost_map_verification",
        "operator_mode": PHYSICAL_COST_MAP_OPERATOR_MODE,
        "audit_status": (
            "PASS_WITH_BLOCKED_INDEPENDENT_CALIBRATION"
            if all(gates.values())
            else "FAIL"
        ),
        "status": "INTERNAL_CONTRACT",
        "claim_status": "CONTRACT_ONLY",
        "evidence_class": "INTERNAL_CONTRACT",
        "unit_lane": "si_contract_only",
        "physical_mapping_status": PHYSICAL_COST_MAP_STATUS,
        "formula_audit": [
            {
                "formula_id": "PHYSICAL-COST-001",
                "relation": "Q_J=alpha_b*W_behavior+alpha_m*W_maintenance",
                "origin": "explicit dimensional mapping contract",
                "status": "contractual; alpha values are not inferred",
            },
            {
                "formula_id": "PHYSICAL-COST-002",
                "relation": "Delta_S_bath_J_per_K=Q_J/T_bath_K",
                "origin": "isothermal thermodynamic comparator",
                "status": "contractual; not external entropy evidence",
            },
        ],
        "fixture": {
            "behavior_work_normalized": 0.25,
            "maintenance_work_normalized": 0.1,
            "behavior_energy_scale_j": 2.0,
            "maintenance_energy_scale_j": 3.0,
            "bath_temperature_k": 300.0,
            "heat_j": fixture_result.heat_j,
            "entropy_j_per_k": fixture_result.entropy_j_per_k,
            "parameters_fit": False,
            "evidence_status": "TEST_ONLY",
        },
        "gates": gates,
        "limitations": [
            "the fixture is a contract test, not a material measurement",
            "no independent alpha_b or alpha_m source is supplied",
            "no calorimetry/heat-flux dataset, uncertainty distribution, or detector response is supplied",
            "normalized C and normalized work are not identified with temperature or SI energy",
            "a ready map must be derived or source-locked and cannot be fit to the target result",
        ],
        "claim_boundary": (
            "The SI conversion interface is explicit and blocks incomplete or fitted maps; "
            "no physical heat, entropy, or persistence prediction is promoted."
        ),
        "next_controller": (
            "source-lock independent alpha_b and alpha_m in one material lane with "
            "calorimetry or heat-flux measurement, uncertainty, detector operator, and holdout"
        ),
    }
    output = ROOT / "core" / "artifacts" / "resource_selection_physical_cost_map_verification.json"
    output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(artifact, indent=2))
    return 0 if artifact["audit_status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
