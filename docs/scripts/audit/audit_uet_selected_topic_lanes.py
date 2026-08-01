"""Rerun Topics 0.11 and 0.13 on the selected normalized characteristic lane.

This audit deliberately writes new artifacts.  It never relabels the older
matter-space pilot outputs and it does not claim SI or external validation.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docs.core.uet_matter_space_characteristic import (  # noqa: E402
    CHARACTERISTIC_CONE_OPERATOR_MODE,
    characteristic_cone_dt,
    characteristic_cone_step,
)
from docs.core.uet_matter_space_finite_cone import (  # noqa: E402
    FiniteConeCConfig,
    FiniteConeCState,
)
from docs.core.uet_matter_space_observable import (  # noqa: E402
    normalized_matter_space_observable,
)
from docs.core.uet_trace import TraceKernelConfig  # noqa: E402


N = 161
DX = 0.05
STEPS = 20
OMEGA = 0.75


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def config(coupling: float = 0.1) -> FiniteConeCConfig:
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
        coupling_g=coupling,
        boundary_condition="periodic",
        unit_lane="normalized",
        ledger_tolerance=1.0e-4,
    )


def trace_config() -> TraceKernelConfig:
    return TraceKernelConfig(
        D_trace=0.05,
        tau_trace=0.2,
        lambda_trace=0.1,
        source_normalization="normalized",
        boundary_condition="periodic",
    )


def radius(field: np.ndarray, center: int, threshold: float = 1.0e-12) -> int:
    active = np.flatnonzero(np.abs(field) > threshold)
    if active.size == 0:
        return 0
    return int(max(abs(int(active.min()) - center), abs(int(active.max()) - center)))


def run(
    state: FiniteConeCState,
    cfg: FiniteConeCConfig,
    *,
    steps: int = STEPS,
    source_fn=None,
    include_trace: bool = True,
) -> dict[str, Any]:
    dt = characteristic_cone_dt(DX, cfg)
    center = N // 2
    history: list[np.ndarray] = []
    records: list[dict[str, Any]] = []
    max_ledger = 0.0
    max_energy_increase = 0.0
    source_min = np.inf
    for index in range(steps):
        t = (index + 1) * dt
        matter_source, space_source = (source_fn(t) if source_fn is not None else (None, None))
        result = characteristic_cone_step(
            state,
            dt,
            DX,
            cfg,
            matter_source=matter_source,
            space_source=space_source,
            trace_history=history if include_trace else None,
            trace_config=trace_config() if include_trace else None,
        )
        state = FiniteConeCState(result.C, result.V, result.space_response, result.space_rate)
        trace_source = float(np.max(np.asarray(result.diagnostics.get("trace_source", 0.0))))
        source_min = min(source_min, trace_source)
        max_ledger = max(max_ledger, abs(float(result.energy_ledger["closure_relative"])))
        max_energy_increase = max(max_energy_increase, float(result.energy_ledger["actual_delta"]))
        history.append(np.full(N, trace_source, dtype=float))
        observed = normalized_matter_space_observable(result, dx=DX, center_index=center)
        records.append(
            {
                "step": index + 1,
                "time": t,
                "radius_cells": max(
                    radius(state.C, center), radius(state.space_response, center)
                ),
                "C_rms": observed["C_rms"],
                "Phi_rms": observed["Phi_rms"],
                "ledger_gate": result.energy_ledger["ledger_gate"],
                "trace_source": trace_source,
            }
        )
    return {
        "state": state,
        "records": records,
        "dt": dt,
        "max_ledger_relative_residual": max_ledger,
        "max_closed_energy_increase": max_energy_increase,
        "minimum_trace_source": source_min,
        "all_finite": bool(
            np.all(np.isfinite(state.C))
            and np.all(np.isfinite(state.space_response))
            and np.all(np.isfinite(state.space_rate))
        ),
    }


def localized_state() -> FiniteConeCState:
    C = np.zeros(N, dtype=float)
    C[N // 2] = 0.1
    return FiniteConeCState(C, np.zeros(N), np.zeros(N), np.zeros(N))


def driven_source(amplitude: float = 0.2):
    center = N // 2

    def source(t: float):
        space = np.zeros(N, dtype=float)
        space[center] = amplitude * np.sin(OMEGA * t)
        return None, space

    return source


def base_metadata(prereg: Path, artifact_name: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "artifact": artifact_name,
        "operator_mode": CHARACTERISTIC_CONE_OPERATOR_MODE,
        "unit_lane": "normalized",
        "preregistration": {
            "path": str(prereg.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(prereg),
            "parameter_fitting": False,
            "external_numeric_inputs": [],
        },
        "claim_status": "SIMULATION_ONLY",
        "physical_observable_status": "OPEN_SI_MAPPING",
        "mass_density_mapping": "NOT_DEFINED",
        "trace_backreaction": False,
        "no_field_clipping": True,
        "no_parameter_fitting": True,
        "limitations": [
            "strict CFL=1 compact support is a numerical control, not a covariant proof",
            "C is a non-conserved collective candidate and is not mass density",
            "the observable operator is normalized and detector-independent",
            "no external thermal or phase-transition data are consumed",
        ],
    }


def build_phase_artifact() -> dict[str, Any]:
    prereg = ROOT / "docs/topics/0.11_Phase_Transitions/Data/03_Research/matter_space_characteristic_lane_preregistration.json"
    cfg = config()
    localized = run(localized_state(), cfg)
    zero_phi = run(localized_state(), cfg, include_trace=False)
    altered = localized_state()
    altered.space_response[N // 2] = 0.08
    altered.space_rate[N // 2] = 0.05
    different_space = run(altered, cfg, include_trace=False)
    same_state_trace_off = run(localized_state(), cfg, include_trace=False)
    same_state_trace_on = run(localized_state(), cfg, include_trace=True)
    radius_ok = all(row["radius_cells"] <= row["step"] for row in localized["records"])
    state_difference = float(
        max(
            np.sqrt(np.mean(np.square(zero_phi["state"].C - different_space["state"].C))),
            np.sqrt(np.mean(np.square(zero_phi["state"].space_response - different_space["state"].space_response))),
        )
    )
    trace_difference = float(
        max(
            np.max(np.abs(same_state_trace_off["state"].C - same_state_trace_on["state"].C)),
            np.max(np.abs(same_state_trace_off["state"].space_response - same_state_trace_on["state"].space_response)),
        )
    )
    gates = {
        "all_finite": localized["all_finite"],
        "compact_support_no_prearrival": radius_ok,
        "ledger_gates_pass": localized["max_ledger_relative_residual"] <= cfg.ledger_tolerance,
        "closed_energy_not_increasing": localized["max_closed_energy_increase"] <= 1.0e-9,
        "same_C_different_space_state_changes_future": state_difference > 1.0e-6,
        "trace_toggle_does_not_change_future_state": trace_difference <= 1.0e-12,
    }
    artifact = base_metadata(prereg, "matter_space_0_11_characteristic_lane_rerun")
    artifact.update(
        {
            "topic": "0.11_Phase_Transitions",
            "status": "INTERNAL_DIAGNOSTIC",
            "verification_status": "PASS" if all(gates.values()) else "FAIL",
            "controller": "topic_structure_factor_replicate_temporal_acquisition_and_foundation_units",
            "config": {"n": N, "dx": DX, "dt": localized["dt"], "steps": STEPS, "declared_cone_speed": 1.0},
            "metrics": {
                "max_ledger_relative_residual": localized["max_ledger_relative_residual"],
                "max_closed_energy_increase": localized["max_closed_energy_increase"],
                "minimum_trace_source": localized["minimum_trace_source"],
                "same_C_different_space_state_future_difference": state_difference,
                "trace_toggle_physical_difference": trace_difference,
                "arrival_radius_cells": localized["records"][-1]["radius_cells"],
            },
            "gates": gates,
            "observables": localized["records"],
            "claim_boundary": "selected normalized characteristic-lane internal diagnostic; no universality, mass, particle, GR, or empirical claim",
        }
    )
    return artifact


def build_thermal_artifact() -> dict[str, Any]:
    prereg = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/matter_space_characteristic_thermal_lane_preregistration.json"
    cfg = config()
    driven = run(FiniteConeCState(np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)), cfg, source_fn=driven_source())
    center = N // 2
    target = center + 5
    arrivals = [row for row in driven["records"] if row["radius_cells"] >= 5]
    arrival_time = float(arrivals[0]["time"]) if arrivals else None
    emission_time = driven["dt"]
    expected = emission_time + 5.0 * DX / 1.0
    speed = None if arrival_time is None else 5.0 * DX / (arrival_time - emission_time)
    gates = {
        "all_finite": driven["all_finite"],
        "source_nonnegative_trace": driven["minimum_trace_source"] >= -1.0e-12,
        "ledger_gates_pass": driven["max_ledger_relative_residual"] <= cfg.ledger_tolerance,
        "causal_arrival_recorded": arrival_time is not None,
        "causal_arrival_within_five_percent": speed is not None and abs(speed - 1.0) <= 0.05,
        "no_external_data_consumed": True,
    }
    artifact = base_metadata(prereg, "matter_space_0_13_characteristic_thermal_lane_rerun")
    artifact.update(
        {
            "topic": "0.13_Thermodynamic_Bridge",
            "status": "SIMULATION_ONLY",
            "verification_status": "PASS" if all(gates.values()) else "FAIL",
            "controller": "open_SI_Phi_to_temperature_mapping_and_external_source_package",
            "config": {"n": N, "dx": DX, "dt": driven["dt"], "steps": STEPS, "declared_cone_speed": 1.0, "forcing": "normalized_center_source_sin(0.75*t)"},
            "metrics": {
                "max_ledger_relative_residual": driven["max_ledger_relative_residual"],
                "max_closed_energy_increase": driven["max_closed_energy_increase"],
                "minimum_trace_source": driven["minimum_trace_source"],
                "target_radius_cells": 5,
                "emission_time": emission_time,
                "expected_arrival_time": expected,
                "measured_arrival_time": arrival_time,
                "measured_speed": speed,
            },
            "gates": gates,
            "observables": driven["records"],
            "external_validation": {"status": "NOT_CONSUMED", "rows": 0},
            "claim_boundary": "normalized causal control simulation only; no temperature identity, SI heat flux, or external validation",
        }
    )
    return artifact


def main() -> int:
    phase_path = ROOT / "docs/topics/0.11_Phase_Transitions/Result/artifacts/matter_space_0_11_characteristic_lane_rerun.json"
    thermal_path = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/matter_space_0_13_characteristic_thermal_lane_rerun.json"
    phase_path.parent.mkdir(parents=True, exist_ok=True)
    thermal_path.parent.mkdir(parents=True, exist_ok=True)
    phase = build_phase_artifact()
    thermal = build_thermal_artifact()
    phase_path.write_text(json.dumps(phase, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    thermal_path.write_text(json.dumps(thermal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"phase": phase["verification_status"], "thermal": thermal["verification_status"], "phase_artifact": str(phase_path.relative_to(ROOT)), "thermal_artifact": str(thermal_path.relative_to(ROOT))}, indent=2))
    return 0 if phase["verification_status"] == "PASS" and thermal["verification_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
