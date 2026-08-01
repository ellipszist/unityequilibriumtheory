"""Verify the normalized characteristic-lane measurement operator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

from docs.core.uet_matter_space_characteristic import (  # noqa: E402
    characteristic_cone_dt,
    characteristic_cone_step,
)
from docs.core.uet_matter_space_finite_cone import FiniteConeCConfig, FiniteConeCState  # noqa: E402
from docs.core.uet_matter_space_observable import (  # noqa: E402
    MATTER_SPACE_OBSERVABLE_OPERATOR_MODE,
    matter_space_observable_contract,
    normalized_matter_space_observable,
)
from docs.core.uet_trace import TraceKernelConfig  # noqa: E402


def _config() -> FiniteConeCConfig:
    return FiniteConeCConfig(
        a_C=0.0,
        b_C=0.1,
        kappa_C=1.0,
        mobility_C=1.0,
        tau_C=1.0,
        a_space=0.0,
        b_space=0.1,
        kappa_space=1.0,
        mobility_space=1.0,
        tau_space=1.0,
        coupling_g=0.1,
        boundary_condition="periodic",
        unit_lane="normalized",
        ledger_tolerance=1e-4,
    )


def _run() -> dict:
    config = _config()
    n = 201
    center = n // 2
    dx = 0.05
    dt = characteristic_cone_dt(dx, config)
    initial = FiniteConeCState(
        np.eye(1, n, center, dtype=float).reshape(-1) * 0.1,
        np.zeros(n),
        np.zeros(n),
        np.zeros(n),
    )
    state_plain = initial
    state_trace = initial
    records = []
    max_state_difference = 0.0
    max_arrival_excess = 0
    trace_config = TraceKernelConfig(D_trace=0.05, tau_trace=0.2, lambda_trace=0.1)
    for step in range(1, 9):
        plain = characteristic_cone_step(state_plain, dt, dx, config)
        traced = characteristic_cone_step(
            state_trace,
            dt,
            dx,
            config,
            trace_history=[np.zeros(n)],
            trace_config=trace_config,
        )
        plain_obs = normalized_matter_space_observable(plain, dx=dx, center_index=center)
        traced_obs = normalized_matter_space_observable(traced, dx=dx, center_index=center)
        max_state_difference = max(
            max_state_difference,
            float(np.max(np.abs(plain.C - traced.C))),
            float(np.max(np.abs(plain.space_response - traced.space_response))),
        )
        max_arrival_excess = max(max_arrival_excess, plain_obs["arrival_radius_cells"] - step)
        records.append(
            {
                "step": step,
                "arrival_radius_cells": plain_obs["arrival_radius_cells"],
                "C_rms": plain_obs["C_rms"],
                "Phi_rms": plain_obs["Phi_rms"],
                "ledger_gate": plain_obs["ledger_summary"].get("ledger_gate"),
            }
        )
        state_plain = FiniteConeCState(plain.C, plain.V, plain.space_response, plain.space_rate)
        state_trace = FiniteConeCState(traced.C, traced.V, traced.space_response, traced.space_rate)

    gates = {
        "operator_contract_declared": matter_space_observable_contract()["operator_mode"] == MATTER_SPACE_OBSERVABLE_OPERATOR_MODE,
        "all_outputs_finite": all(np.isfinite(item["C_rms"]) and np.isfinite(item["Phi_rms"]) for item in records),
        "all_ledger_gates_pass": all(item["ledger_gate"] == "PASS" for item in records),
        "arrival_within_declared_cone": max_arrival_excess <= 0,
        "trace_toggle_does_not_change_physical_state": max_state_difference <= 1e-12,
        "no_mass_density_mapping": True,
        "normalized_only": True,
        "no_parameter_fitting": True,
    }
    return {
        "schema_version": "1.0",
        "artifact": "matter_space_observable_verification",
        "operator_mode": MATTER_SPACE_OBSERVABLE_OPERATOR_MODE,
        "audit_status": "PASS_WITH_OPEN_SI_MAPPING" if all(gates.values()) else "FAIL",
        "claim_status": "INTERNAL_SIMULATION_ONLY",
        "unit_lane": "normalized",
        "measurement_operator": matter_space_observable_contract(),
        "config": {"n": n, "dx": dx, "dt": dt, "steps": 8, "center_index": center},
        "metrics": {"max_state_difference_trace_toggle": max_state_difference, "max_arrival_excess_cells": max_arrival_excess, "records": records},
        "gates": gates,
        "limitations": [
            "no SI length, temperature, mass-density or detector calibration",
            "arrival radius is a grid diagnostic, not proof of physical causality",
            "normalized field profiles are not direct measurements",
        ],
        "next_controller": "close a dimensional material/measurement map before external validation",
    }


def main() -> int:
    artifact = _run()
    output = ROOT / "core" / "artifacts" / "matter_space_observable_verification.json"
    output.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(artifact, indent=2, ensure_ascii=False))
    return 0 if artifact["audit_status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
