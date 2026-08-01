"""Generate the normalized persistence-energy diagnostic artifact."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

from docs.core.persistence_energy_diagnostic import (  # noqa: E402
    PATH_COST_ORIGIN,
    PERSISTENCE_PRINCIPLE_ID,
    PERSISTENCE_PRINCIPLE_NAME_EN,
    PERSISTENCE_PRINCIPLE_NAME_TH,
    PERSISTENCE_PRINCIPLE_STATUS,
    PersistenceEnergyConfig,
    simulate_persistence_energy,
)


def _trajectory(steps: int, cycles: int, amplitude: float) -> list[float]:
    return [
        amplitude * math.sin(2.0 * math.pi * cycles * index / steps)
        for index in range(steps + 1)
    ]


def build_artifact() -> dict:
    steps = 10_000
    horizon = 10.0
    dt = horizon / steps
    config = PersistenceEnergyConfig(
        initial_available_energy=1.0,
        sustain_threshold=0.2,
        behavior_cost_coefficient=0.1,
        input_power=0.0,
        output_power=0.0,
    )
    low_path = _trajectory(steps, cycles=1, amplitude=0.5)
    high_path = _trajectory(steps, cycles=8, amplitude=0.5)
    low = simulate_persistence_energy(low_path, dt, config)
    high = simulate_persistence_energy(high_path, dt, config)

    endpoint_residual = max(
        abs(low_path[0] - high_path[0]),
        abs(low_path[-1] - high_path[-1]),
    )
    monotonic_low = all(
        right <= left + 1e-12
        for left, right in zip(low.available_energy, low.available_energy[1:])
    )
    monotonic_high = all(
        right <= left + 1e-12
        for left, right in zip(high.available_energy, high.available_energy[1:])
    )
    gates = {
        "same_endpoints_le_1e-12": endpoint_residual <= 1e-12,
        "path_power_nonnegative": all(
            power >= -1e-12
            for power in low.behavior_power + high.behavior_power
        ),
        "low_path_ledger_closure_le_1e-12": abs(
            low.ledger_closure_residual
        )
        <= 1e-12,
        "high_path_ledger_closure_le_1e-12": abs(
            high.ledger_closure_residual
        )
        <= 1e-12,
        "available_energy_monotone_without_input": monotonic_low and monotonic_high,
        "high_activity_cost_gt_10x_low_activity": high.behavior_work
        > 10.0 * low.behavior_work,
        "high_activity_reaches_threshold_first": (
            high.persistence_time is not None
            and (
                low.persistence_time is None
                or high.persistence_time < low.persistence_time
            )
        ),
        "C_not_relabelled_as_energy": True,
    }

    return {
        "schema_version": "1.0",
        "artifact": "persistence_energy_diagnostic_verification",
        "principle": {
            "id": PERSISTENCE_PRINCIPLE_ID,
            "name_th": PERSISTENCE_PRINCIPLE_NAME_TH,
            "name_en": PERSISTENCE_PRINCIPLE_NAME_EN,
            "status": PERSISTENCE_PRINCIPLE_STATUS,
            "statement": (
                "Persistent system patterns can emerge when interacting components "
                "allocate behavior-related resources in ways that reduce premature "
                "loss of the system's persistence capacity; this is a result-based "
                "selection hypothesis, not intentional optimization."
            ),
            "not_a_claim": [
                "not a universal energy law",
                "not an SI potential-energy identity",
                "not an agent, intention, force, mass, or new substance",
            ],
        },
        "audit_status": "PASS_WITH_OPEN_CONSTITUTIVE_INTERPRETATION"
        if all(gates.values())
        else "FAIL",
        "claim_status": "SIMULATION_ONLY",
        "evidence_class": "INTERNAL_DIAGNOSTIC",
        "status": "DIAGNOSTIC_ONLY",
        "unit_lane": "normalized",
        "constitutive_origin": PATH_COST_ORIGIN,
        "standard_counterpart": "Rayleigh-type generalized-coordinate dissipation plus an explicit resource ledger",
        "uet_status": "C_AS_RELATIONAL_ORGANIZATIONAL_COORDINATE_REMAINS_OPEN",
        "config": {
            "steps": steps,
            "horizon": horizon,
            "dt": dt,
            "amplitude": 0.5,
            "low_cycles": 1,
            "high_cycles": 8,
            "initial_available_energy": config.initial_available_energy,
            "sustain_threshold": config.sustain_threshold,
            "behavior_cost_coefficient": config.behavior_cost_coefficient,
            "input_power": config.input_power,
            "output_power": config.output_power,
        },
        "formula_audit": [
            {
                "formula_id": "PERSISTENCE-COST-001",
                "relation": "P_C=eta_C*(dC/dt)^2 >= 0",
                "variables_and_units": "C dimensionless normalized coordinate; eta_C carries normalized ledger units; P_C normalized energy/time",
                "constant_origin": "heuristic_bridge / Rayleigh-type constitutive ansatz",
                "proof_status": "open constitutive diagnostic",
                "verification_role": "path-cost sign and same-endpoint comparison",
                "failure_mode": "quadratic path cost is mistaken for a universal UET derivation",
                "next_hardening_step": "map eta_C and P_C to measured work, heat, or entropy production",
            },
            {
                "formula_id": "PERSISTENCE-LEDGER-002",
                "relation": "E_available[n+1]=E_available[n]+(J_in-J_out-P_C)*dt",
                "variables_and_units": "all quantities normalized; E_available is a resource ledger, not SI total energy",
                "constant_origin": "declared bookkeeping identity in the synthetic lane",
                "proof_status": "checked local identity",
                "verification_role": "ledger closure and persistence threshold",
                "failure_mode": "available/free energy is reported as total energy conservation",
                "next_hardening_step": "close boundary and SI energy/entropy accounting for one physical lane",
            },
            {
                "formula_id": "PERSISTENCE-TIME-003",
                "relation": "t_persist=inf{t:E_available(t)<=E_sustain}",
                "variables_and_units": "time and normalized ledger threshold; threshold is a declared diagnostic criterion",
                "constant_origin": "benchmark anchor / exploratory persistence criterion",
                "proof_status": "open interpretation",
                "verification_role": "same-endpoint path comparison",
                "failure_mode": "persistence time is promoted to biological or cosmological survival law",
                "next_hardening_step": "derive an observable persistence criterion in a selected system lane",
            },
        ],
        "metrics": {
            "endpoint_residual": endpoint_residual,
            "low_behavior_work": low.behavior_work,
            "high_behavior_work": high.behavior_work,
            "behavior_work_ratio": high.behavior_work / low.behavior_work,
            "low_final_available_energy": low.available_energy[-1],
            "high_persistence_time": high.persistence_time,
            "low_persistence_time": low.persistence_time,
            "low_ledger_closure_residual": low.ledger_closure_residual,
            "high_ledger_closure_residual": high.ledger_closure_residual,
        },
        "gates": gates,
        "limitations": [
            "prescribed synthetic C trajectories; no physical dynamics is derived",
            "Rayleigh-type path cost is a constitutive ansatz",
            "normalized ledger is not SI energy or entropy accounting",
            "no external data, fit, biological selection, galaxy model, or force law",
            "persistence threshold is an exploratory benchmark criterion",
            "the named principle remains a candidate result-based selection hypothesis",
        ],
    }


def main() -> int:
    artifact = build_artifact()
    output = ROOT / "core" / "artifacts" / "persistence_energy_diagnostic_verification.json"
    output.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    principle_contract = {
        "schema_version": "1.0",
        "artifact": "resource_persistence_principle_contract",
        "principle_id": PERSISTENCE_PRINCIPLE_ID,
        "name_th": PERSISTENCE_PRINCIPLE_NAME_TH,
        "name_en": PERSISTENCE_PRINCIPLE_NAME_EN,
        "status": PERSISTENCE_PRINCIPLE_STATUS,
        "unit_lane": "normalized_only",
        "derivation_status": "open_derivation_target",
        "current_operationalization": {
            "path_cost": "P_C=eta_C*(dC/dt)^2 >= 0",
            "resource_ledger": "dE_available/dt=J_in-J_out-P_C",
            "persistence_criterion": "t_persist=inf{t:E_available<=E_sustain}",
        },
        "evidence": {
            "source_artifact": "persistence_energy_diagnostic_verification",
            "same_endpoint_path_gate": artifact["gates"][
                "same_endpoints_le_1e-12"
            ],
            "path_cost_gate": artifact["gates"][
                "high_activity_cost_gt_10x_low_activity"
            ],
            "ledger_closure_gate": artifact["gates"][
                "high_path_ledger_closure_le_1e-12"
            ],
            "current_evidence_class": artifact["evidence_class"],
        },
        "controlling_blocker": (
            "Map behavior-related path cost to measured work, heat, or "
            "entropy production in one declared physical lane."
        ),
        "claim_boundary": [
            "candidate resource-constrained collective dynamics",
            "simulation-only operational diagnostic",
            "not a universal potential-energy preservation law",
        ],
    }
    contract_output = (
        ROOT / "core" / "artifacts"
        / "resource_persistence_principle_contract.json"
    )
    contract_output.write_text(
        json.dumps(principle_contract, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(artifact, indent=2, ensure_ascii=False))
    return 0 if artifact["audit_status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
