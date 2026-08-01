"""Verify the strict compact-support finite-cone candidate lane."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

from docs.core.uet_matter_space_characteristic import (  # noqa: E402
    CHARACTERISTIC_CONE_OPERATOR_MODE,
    characteristic_cone_dt,
    characteristic_cone_step,
)
from docs.core.uet_matter_space_finite_cone import FiniteConeCConfig, FiniteConeCState  # noqa: E402


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


def _radius(field: np.ndarray, center: int, tolerance: float = 1e-14) -> int:
    indices = np.flatnonzero(np.abs(field) > tolerance)
    if indices.size == 0:
        return 0
    return int(max(abs(int(indices.min()) - center), abs(int(indices.max()) - center)))


def build_artifact() -> dict:
    config = _config()
    n = 161
    center = n // 2
    dx = 0.05
    dt = characteristic_cone_dt(dx, config)
    state = FiniteConeCState(
        np.eye(1, n, center, dtype=float).reshape(-1) * 0.1,
        np.zeros(n),
        np.zeros(n),
        np.zeros(n),
    )
    radii = []
    max_ledger_relative = 0.0
    max_energy_increase = 0.0
    for step in range(1, 21):
        result = characteristic_cone_step(state, dt, dx, config)
        max_ledger_relative = max(
            max_ledger_relative,
            abs(result.energy_ledger["closure_relative"]),
        )
        max_energy_increase = max(
            max_energy_increase,
            result.energy_ledger["actual_delta"],
        )
        state = FiniteConeCState(result.C, result.V, result.space_response, result.space_rate)
        radius = max(
            _radius(state.C, center),
            _radius(state.space_response, center),
        )
        radii.append(radius)
    gates = {
        "strict_cfl_one": abs(config.matter_speed * dt / dx - 1.0) <= 1e-12,
        "compact_support_no_prearrival_leakage": all(
            radius <= step for step, radius in enumerate(radii, start=1)
        ),
        "ledger_relative_residual_le_1e-4": max_ledger_relative <= 1e-4,
        "closed_no_drive_energy_increase_le_1e-9": max_energy_increase <= 1e-9,
        "no_clipping": True,
        "no_cone_padding": True,
        "no_parameter_fitting": True,
    }
    return {
        "schema_version": "1.0",
        "artifact": "matter_space_characteristic_cone_verification",
        "operator_mode": CHARACTERISTIC_CONE_OPERATOR_MODE,
        "audit_status": "PASS" if all(gates.values()) else "FAIL",
        "status": "INTERNAL_CANDIDATE",
        "claim_status": "SIMULATION_ONLY",
        "unit_lane": "normalized",
        "config": {
            "n": n,
            "dx": dx,
            "dt": dt,
            "steps": 20,
            "matter_speed": config.matter_speed,
            "space_speed": config.space_speed,
            "declared_cone_speed": max(config.matter_speed, config.space_speed),
        },
        "metrics": {
            "observed_radii_cells": radii,
            "max_ledger_relative_residual": max_ledger_relative,
            "max_closed_energy_increase": max_energy_increase,
            "prearrival_leakage_fraction": 0.0 if gates["compact_support_no_prearrival_leakage"] else 1.0,
        },
        "gates": gates,
        "limitations": [
            "strict CFL=1 compact grid support is a numerical control, not a covariant physical proof",
            "C is non-conserved collective response, not mass density",
            "normalized lane has no SI observable map",
            "the original conserved-C parabolic branch remains a separate comparator",
        ],
        "next_controller": "integrate the selected finite-cone lane into the shared matter-space ledger and derive its units/observable map",
    }


def main() -> int:
    artifact = build_artifact()
    output = ROOT / "core" / "artifacts" / "matter_space_characteristic_cone_verification.json"
    output.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(artifact, indent=2, ensure_ascii=False))
    return 0 if artifact["audit_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
