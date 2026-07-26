"""Generate the deterministic relational two-body baseline artifact."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

from docs.core.relational_two_body_baseline import (  # noqa: E402
    RelationalBaselineConfig,
    circular_initial_state,
    delayed_observation,
    force_on_a,
    force_on_a_from_coordinate,
    galilean_boost,
    interaction_coordinate,
    interaction_energy,
    interaction_energy_from_coordinate,
    total_energy,
    total_momentum,
    trajectory,
)


def _relative_error(value: float, reference: float) -> float:
    scale = max(1.0, abs(reference))
    return abs(value - reference) / scale


def build_artifact() -> dict:
    config = RelationalBaselineConfig()
    initial = circular_initial_state(config)
    states = trajectory(initial, config)

    energy_values = [total_energy(state, config) for state in states]
    momentum_values = [total_momentum(state, config) for state in states]
    initial_energy = energy_values[0]
    max_energy_drift = max(
        _relative_error(value, initial_energy) for value in energy_values
    )
    max_momentum_drift = max(
        (momentum[0] ** 2 + momentum[1] ** 2) ** 0.5 for momentum in momentum_values
    )

    mapping_energy_errors = []
    mapping_force_errors = []
    for state in states[:: max(1, len(states) // 20)]:
        direct_energy = interaction_energy(state, config)
        mapped_energy = interaction_energy_from_coordinate(state, config)
        direct_force = force_on_a(state, config)
        mapped_force = force_on_a_from_coordinate(state, config)
        mapping_energy_errors.append(_relative_error(mapped_energy, direct_energy))
        mapping_force_errors.append(
            max(
                _relative_error(mapped_force[0], direct_force[0]),
                _relative_error(mapped_force[1], direct_force[1]),
            )
        )

    boost = (0.37, -0.21)
    boosted_initial = galilean_boost(initial, boost)
    boosted_states = trajectory(boosted_initial, config)
    galilean_c_error = max(
        abs(
            interaction_coordinate(state, config.separation_reference)
            - interaction_coordinate(boosted, config.separation_reference)
        )
        for state, boosted in zip(states, boosted_states)
    )

    observer = (5.0, 0.0)
    event_index = config.steps // 4
    observation = delayed_observation(
        states,
        event_index,
        observer,
        config.signal_speed,
    )

    scaled_config = RelationalBaselineConfig(
        G=config.G,
        mass_a=2.0 * config.mass_a,
        mass_b=2.0 * config.mass_b,
        separation_reference=config.separation_reference,
        dt=config.dt,
        steps=config.steps,
        signal_speed=config.signal_speed,
    )
    same_geometry = initial
    c_original = interaction_coordinate(
        same_geometry, config.separation_reference
    )
    c_scaled = interaction_coordinate(
        same_geometry, scaled_config.separation_reference
    )
    energy_original = interaction_energy(same_geometry, config)
    energy_scaled = interaction_energy(same_geometry, scaled_config)
    force_original = force_on_a(same_geometry, config)
    force_scaled = force_on_a(same_geometry, scaled_config)

    gates = {
        "coordinate_energy_residual_le_1e-12": max(mapping_energy_errors) <= 1e-12,
        "coordinate_force_residual_le_1e-12": max(mapping_force_errors) <= 1e-12,
        "energy_relative_drift_le_1e-4": max_energy_drift <= 1e-4,
        "momentum_drift_le_1e-12": max_momentum_drift <= 1e-12,
        "galilean_relative_coordinate_invariance_le_1e-10": galilean_c_error
        <= 1e-10,
        "finite_positive_observation_delay": observation["delay"] > 0.0,
        "source_state_differs_at_arrival": observation["past_state_separation"]
        > 1e-8,
        "same_geometry_C_under_mass_rescale": abs(c_original - c_scaled) <= 1e-12,
        "mass_changes_interaction_amplitude": abs(energy_scaled / energy_original - 4.0)
        <= 1e-12
        and abs(force_scaled[0] / force_original[0] - 4.0) <= 1e-12,
    }

    return {
        "schema_version": "1.0",
        "artifact": "relational_two_body_baseline_verification",
        "audit_status": "PASS" if all(gates.values()) else "FAIL",
        "claim_status": "SIMULATION_ONLY",
        "evidence_class": "INTERNAL_CHECKED_COMPARATOR",
        "unit_lane": "normalized_comparator",
        "standard_counterpart": "Newtonian two-body mechanics with finite-signal observer record",
        "uet_status": "CANDIDATE_CORRESPONDENCE_OPEN",
        "config": {
            "G": config.G,
            "mass_a": config.mass_a,
            "mass_b": config.mass_b,
            "separation_reference": config.separation_reference,
            "dt": config.dt,
            "steps": config.steps,
            "signal_speed": config.signal_speed,
        },
        "formula_audit": [
            {
                "formula_id": "REL-TWO-C-001",
                "relation": "C_AB = -r_ref / r",
                "variables_and_units": "C_AB dimensionless normalized relational coordinate; r_ref and r code-unit lengths",
                "constant_origin": "topic_derived_relation",
                "proof_status": "definition / checked local",
                "verification_role": "correspondence diagnostic",
                "failure_mode": "C is treated as mass or energy without a lane mapping",
                "next_hardening_step": "derive or compare a physical interaction observable for a selected lane",
            },
            {
                "formula_id": "REL-TWO-U-002",
                "relation": "U_AB = -G*m_A*m_B/r = U_0*C_AB",
                "variables_and_units": "U normalized interaction potential; masses and G are standard counterpart code-unit inputs",
                "constant_origin": "standard_counterpart_relation",
                "proof_status": "identity / checked local",
                "verification_role": "mapping gate",
                "failure_mode": "the mapping is described as a UET derivation of gravity",
                "next_hardening_step": "select a dimensional lane and source-lock G and mass conventions",
            },
            {
                "formula_id": "REL-TWO-F-003",
                "relation": "F_A = -grad_xA U_AB; m_A*a_A = F_A",
                "variables_and_units": "F and acceleration use normalized comparator units; m_A remains a separate standard parameter",
                "constant_origin": "standard_counterpart_relation",
                "proof_status": "identity / checked local",
                "verification_role": "force/mass separation gate",
                "failure_mode": "C is used as the inertial mass without evidence",
                "next_hardening_step": "test a declared C-to-rho or C-to-interaction map against holdout observables",
            },
            {
                "formula_id": "REL-TWO-OBS-004",
                "relation": "t_o = t_e + |x_A(t_e)-x_O|/u",
                "variables_and_units": "t and distance are normalized; u is a declared finite signal speed",
                "constant_origin": "standard finite-signal comparator relation",
                "proof_status": "definition / checked local",
                "verification_role": "observer-layer diagnostic",
                "failure_mode": "received past record is labelled as the source's current state",
                "next_hardening_step": "add Lorentz-covariant signal propagation as a separate lane",
            },
        ],
        "metrics": {
            "max_coordinate_energy_relative_error": max(mapping_energy_errors),
            "max_coordinate_force_relative_error": max(mapping_force_errors),
            "max_energy_relative_drift": max_energy_drift,
            "max_momentum_drift": max_momentum_drift,
            "galilean_coordinate_max_error": galilean_c_error,
            "observation": observation,
            "mass_scale_diagnostic": {
                "same_geometry_coordinate_original": c_original,
                "same_geometry_coordinate_mass_rescaled": c_scaled,
                "potential_scale_ratio": energy_scaled / energy_original,
                "force_x_scale_ratio": force_scaled[0] / force_original[0],
                "interpretation": "geometry-only C does not identify mass amplitude",
            },
        },
        "gates": gates,
        "limitations": [
            "normalized comparator only; no SI units",
            "standard Newtonian counterpart, not a UET gravity derivation",
            "C-to-potential map is a declared correspondence choice",
            "no galaxy data, fitting, uncertainty, or holdout claim",
            "observer layer is Newtonian finite-signal, not Lorentz covariant",
        ],
    }


def main() -> int:
    artifact = build_artifact()
    output = ROOT / "core" / "artifacts" / "relational_two_body_baseline_verification.json"
    output.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(artifact, indent=2, ensure_ascii=False))
    return 0 if artifact["audit_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
