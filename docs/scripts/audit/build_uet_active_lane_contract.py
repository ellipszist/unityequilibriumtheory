"""Build the explicit units/observable contract for active UET lanes.

This is a closure register, not a claim-promotion artifact.  It makes the remaining
F3/F7 gaps concrete and prevents normalized variables from being reported as SI
observables.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs/core/artifacts/uet_active_lane_units_observable_register.json"


def build() -> dict[str, Any]:
    lanes: list[dict[str, Any]] = [
        {
            "lane_id": "matter_space_characteristic_cone_v1",
            "variables": {"C": "dimensionless normalized collective coordinate", "Phi": "dimensionless normalized response", "Pi": "normalized response rate"},
            "unit_lane": "normalized",
            "standard_counterpart": "damped hyperbolic non-conserved order-parameter dynamics",
            "observable_operator": "O[C,Phi,Pi] = sampled field profiles, arrival radius and ledger diagnostics",
            "observable_status": "INTERNAL_SIMULATION_ONLY",
            "units_status": "CLOSED_NORMALIZED_ONLY",
            "uncertainty_status": "NUMERICAL_REFINEMENT_ONLY",
            "open_items": ["no SI map", "no material calibration", "C is not mass density"],
            "evidence": ["docs/core/artifacts/matter_space_characteristic_cone_verification.json"],
        },
        {
            "lane_id": "matter_space_conserved_phase_comparator",
            "variables": {"C": "normalized conserved phase/order coordinate", "mu_C": "normalized chemical potential"},
            "unit_lane": "normalized",
            "standard_counterpart": "Cahn-Hilliard conserved gradient-flow comparator",
            "observable_operator": "O[C] = mass/order integral, interface width and structure factor",
            "observable_status": "INTERNAL_DIAGNOSTIC",
            "units_status": "CLOSED_NORMALIZED_ONLY",
            "uncertainty_status": "REPLICATE_AND_TEMPORAL_ACQUISITION_OPEN",
            "open_items": ["changing-C finite cone is blocked by high-k dispersion", "material units open"],
            "evidence": ["docs/core/artifacts/matter_space_causal_lane_selection.json", "docs/core/artifacts/matter_space_phase_pilot.json"],
        },
        {
            "lane_id": "resource_selection_persistence",
            "variables": {"x": "normalized resource-allocation state", "E_available": "normalized available-resource ledger"},
            "unit_lane": "normalized",
            "standard_counterpart": "finite-state resource-selection / repeated-game diagnostic",
            "observable_operator": "O[x] = state trajectory, cooperation/conflict persistence and dissipated-work proxy",
            "observable_status": "INTERNAL_DIAGNOSTIC",
            "units_status": "CLOSED_NORMALIZED_ONLY",
            "uncertainty_status": "PARAMETER_SENSITIVITY_OPEN",
            "open_items": ["no physical energy/work/temperature mapping", "not an intention or teleological law"],
            "evidence": ["docs/core/artifacts/resource_selection_dynamic_game_verification.json", "docs/core/artifacts/resource_selection_thermal_bridge_verification.json"],
        },
        {
            "lane_id": "thermal_cattaneo_bridge",
            "variables": {"T": "normalized temperature proxy", "q": "normalized heat-flux proxy", "R_gen": "normalized trace/dissipation proxy"},
            "unit_lane": "normalized",
            "standard_counterpart": "Fourier and Cattaneo heat transport",
            "observable_operator": "O[T,q] = lag, phase, hysteresis and entropy-production proxy",
            "observable_status": "SIMULATION_ONLY_OPEN_DIMENSIONAL_MAP",
            "units_status": "BLOCKED_SI_MAP",
            "uncertainty_status": "EXTERNAL_SOURCE_PACKAGE_OPEN",
            "open_items": ["Phi/C to T and q map not derived", "normalized proxy is not calorimetry"],
            "evidence": ["docs/core/artifacts/thermal_observable_bridge_verification.json", "docs/core/artifacts/resource_selection_thermal_bridge_verification.json"],
        },
        {
            "lane_id": "o2_finite_density_eos",
            "variables": {"mu": "natural-unit chemical potential", "n": "natural-unit Noether charge density", "p": "natural-unit pressure"},
            "unit_lane": "natural_units",
            "standard_counterpart": "tree-level relativistic O(2) finite-density condensate",
            "observable_operator": "O[n,p] = charge density, pressure and sound-speed response",
            "observable_status": "FORMAL_CONSTITUTIVE_ONLY",
            "units_status": "CLOSED_NATURAL_OPEN_SI",
            "uncertainty_status": "EXTERNAL_COEFFICIENT_MATCH_OPEN",
            "open_items": ["not universal definition of C", "finite-temperature transport and Kubo values open"],
            "evidence": ["docs/core/artifacts/o2_finite_density_eos_verification.json", "docs/core/artifacts/covariant_superfluid_transport_verification.json"],
        },
        {
            "lane_id": "impact_carrier_observer",
            "variables": {"impact": "physical coupling event", "Psi_carrier": "carrier/field excitation", "R_obs": "detector record"},
            "unit_lane": "standard_physics_mapping_required",
            "standard_counterpart": "source-carrier-receiver-detector causal chain",
            "observable_operator": "O[Psi] = detector response after propagation delay",
            "observable_status": "SIMULATION_ONLY",
            "units_status": "BLOCKED_BY_CARRIER_MAP",
            "uncertainty_status": "DETECTOR_RESPONSE_AND_SOURCE_PROVENANCE_OPEN",
            "standard_control": "normalized standard-photon source-propagation-detector comparator",
            "open_items": ["R_gen is not photon/neutrino/positron", "no universal carrier identity", "SI detector map and external provenance remain open"],
            "evidence": ["docs/core/artifacts/impact_effect_core_verification.json", "docs/core/artifacts/carrier_observer_thought_experiment.json", "docs/core/artifacts/photon_observer_baseline_verification.json"],
        },
        {
            "lane_id": "gravity_orbit_cosmology",
            "variables": {"g_mu_nu": "standard metric candidate", "T_mu_nu": "standard stress-energy candidate", "C_orb": "unclosed collective coordinate"},
            "unit_lane": "relativistic_dimensional_contract_required",
            "standard_counterpart": "Newtonian/GR many-body and covariant balance baseline",
            "observable_operator": "O[g,T] = orbit, lensing, redshift and frame observables",
            "observable_status": "BLOCKED",
            "units_status": "BLOCKED",
            "uncertainty_status": "PROVENANCE_AND_RESIDUAL_POLICY_OPEN",
            "open_items": ["no Einstein derivation", "no global open-universe claim"],
            "evidence": ["docs/core/artifacts/orbit_cosmology_correspondence_gate.json", "docs/core/artifacts/uet_gr_research_program_gate.json"],
        },
    ]
    counts: dict[str, int] = {}
    for lane in lanes:
        status = lane["observable_status"]
        counts[status] = counts.get(status, 0) + 1
    return {
        "schema_version": "1.0",
        "artifact": "uet_active_lane_units_observable_register",
        "generated_at": date.today().isoformat(),
        "audit_status": "PASS_WITH_OPEN_LANES",
        "purpose": "make F3 units and F7 observable gaps explicit for every active research lane",
        "rule": "normalized or natural-unit results are not SI predictions without an explicit conversion, measurement operator and uncertainty contract",
        "lane_count": len(lanes),
        "observable_status_counts": dict(sorted(counts.items())),
        "lanes": lanes,
        "foundation_effect": {
            "F3_units": "BLOCKED_UNTIL_DIMENSIONAL_LANE_CLOSURE",
            "F7_observable_mapping": "BLOCKED_UNTIL_MEASUREMENT_OPERATOR_AND_UNCERTAINTY_CLOSURE",
            "claim_ceiling": "internal normalized/natural-unit diagnostics and conditional constitutive relations only",
        },
        "next_controller": "close one dimensional thermal lane with source-locked material data before any external fit or physical claim",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = build()
    if not args.no_write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"audit_status={result['audit_status']}")
        print(f"lane_count={result['lane_count']}")
        print(f"observable_status_counts={result['observable_status_counts']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
