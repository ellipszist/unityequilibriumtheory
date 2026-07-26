"""Generate the C-to-mass-density identifiability artifact."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

from docs.core.mass_density_correspondence import (  # noqa: E402
    MassDensityLaneConfig,
    integrated_density,
    mass_density_from_point_masses,
    max_absolute_difference,
    max_relative_difference,
    normalized_shape,
)
from docs.core.relational_two_body_baseline import (  # noqa: E402
    RelationalBaselineConfig,
    circular_initial_state,
    interaction_coordinate,
)


def build_artifact() -> dict:
    baseline = RelationalBaselineConfig(steps=0)
    lane = MassDensityLaneConfig()
    state = circular_initial_state(baseline)
    scaled_baseline = RelationalBaselineConfig(
        G=baseline.G,
        mass_a=2.0 * baseline.mass_a,
        mass_b=2.0 * baseline.mass_b,
        separation_reference=baseline.separation_reference,
        dt=baseline.dt,
        steps=baseline.steps,
        signal_speed=baseline.signal_speed,
    )
    scaled_state = circular_initial_state(scaled_baseline)

    c_original = interaction_coordinate(state, baseline.separation_reference)
    c_scaled = interaction_coordinate(
        scaled_state, scaled_baseline.separation_reference
    )
    density_original, dx = mass_density_from_point_masses(
        state, baseline.mass_a, baseline.mass_b, lane
    )
    density_scaled, scaled_dx = mass_density_from_point_masses(
        scaled_state, scaled_baseline.mass_a, scaled_baseline.mass_b, lane
    )
    shape_original = normalized_shape(density_original, dx)
    shape_scaled = normalized_shape(density_scaled, scaled_dx)
    total_original = integrated_density(density_original, dx)
    total_scaled = integrated_density(density_scaled, scaled_dx)
    density_scale_residual = max_relative_difference(
        density_scaled,
        [2.0 * value for value in density_original],
    )
    shape_residual = max_relative_difference(shape_original, shape_scaled)
    c_residual = abs(c_original - c_scaled)
    density_difference = max_absolute_difference(density_original, density_scaled)

    gates = {
        "same_geometry_C_le_1e-12": c_residual <= 1e-12,
        "density_integral_original_le_1e-6": abs(total_original - 2.0) <= 1e-6,
        "density_integral_scaled_le_1e-6": abs(total_scaled - 4.0) <= 1e-6,
        "density_linear_mass_scaling_le_1e-12": density_scale_residual <= 1e-12,
        "normalized_shape_invariance_le_1e-12": shape_residual <= 1e-12,
        "direct_C_only_nonidentifiability_confirmed": c_residual <= 1e-12
        and density_difference > 1e-6,
    }

    return {
        "schema_version": "1.0",
        "artifact": "mass_density_correspondence_verification",
        "audit_status": "PASS_WITH_BLOCKED_MAPPING" if all(gates.values()) else "FAIL",
        "mapping_status": "BLOCKED_DIRECT_C_ONLY",
        "claim_status": "SIMULATION_ONLY",
        "evidence_class": "INTERNAL_IDENTIFIABILITY_DIAGNOSTIC",
        "unit_lane": "normalized_code_mass_per_code_length",
        "standard_counterpart": "kernel-smoothed point-mass density observable",
        "uet_status": "C_TO_RHO_DIRECT_MAP_NOT_IDENTIFIED",
        "config": {
            "grid_min": lane.grid_min,
            "grid_max": lane.grid_max,
            "grid_points": lane.grid_points,
            "kernel_width": lane.kernel_width,
            "mass_scale_factor": 2.0,
        },
        "formula_audit": [
            {
                "formula_id": "RHO-KERNEL-001",
                "relation": "rho(x)=m_A W_epsilon(x-x_A)+m_B W_epsilon(x-x_B)",
                "variables_and_units": "rho code mass/code length; m code mass; x and epsilon code length",
                "constant_origin": "standard_observable_definition_with_declared_kernel",
                "proof_status": "definition / checked local",
                "verification_role": "synthetic density observable",
                "failure_mode": "kernel width, grid truncation, or density amplitude is hidden",
                "next_hardening_step": "select a physical mass-density measurement operator and source package",
            },
            {
                "formula_id": "RHO-C-IDENT-002",
                "relation": "same geometry-only C with mass-rescaled rho",
                "variables_and_units": "C dimensionless; rho normalized code density",
                "constant_origin": "identifiability_construction",
                "proof_status": "checked local diagnostic",
                "verification_role": "direct-map blocker",
                "failure_mode": "C is declared equal to rho despite non-unique amplitude",
                "next_hardening_step": "add an explicit matter-amplitude/source state or abandon direct C-to-rho mapping",
            },
            {
                "formula_id": "RHO-AUGMENTED-003",
                "relation": "rho=A_m*rho_hat(C,geometry,matter_source;theta)",
                "variables_and_units": "A_m carries density amplitude; rho_hat is normalized shape; all dimensions remain open",
                "constant_origin": "heuristic_bridge",
                "proof_status": "open",
                "verification_role": "next candidate lane only",
                "failure_mode": "amplitude is fitted on the same data and misreported as a derived prediction",
                "next_hardening_step": "derive dimensional amplitude/source contract and lock it before data fitting",
            },
        ],
        "metrics": {
            "C_original": c_original,
            "C_mass_rescaled": c_scaled,
            "C_residual": c_residual,
            "density_integral_original": total_original,
            "density_integral_mass_rescaled": total_scaled,
            "density_scale_residual": density_scale_residual,
            "normalized_shape_residual": shape_residual,
            "density_difference_max": density_difference,
            "mass_density_ratio": total_scaled / total_original,
            "interpretation": "C alone does not identify mass-density amplitude in the current relational lane",
        },
        "gates": gates,
        "limitations": [
            "normalized synthetic density observable only",
            "direct C-to-rho mapping is intentionally blocked by a constructive degeneracy",
            "no SI conversion, galaxy data, fit, uncertainty, or holdout test",
            "the Gaussian kernel is an observable definition, not a UET derivation",
        ],
    }


def main() -> int:
    artifact = build_artifact()
    output = ROOT / "core" / "artifacts" / "mass_density_correspondence_verification.json"
    output.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(artifact, indent=2, ensure_ascii=False))
    return 0 if artifact["audit_status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
