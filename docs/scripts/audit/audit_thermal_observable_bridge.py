"""Generate the normalized C-to-thermal observable bridge artifact."""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

from docs.core.thermal_observable_bridge import (  # noqa: E402
    ThermalObservableBridgeConfig,
    run_thermal_observable_bridge,
)


def build_artifact() -> dict:
    base_config = ThermalObservableBridgeConfig()
    base = run_thermal_observable_bridge(base_config)
    scaled_config = replace(base_config, C_to_temperature_gain=2.0 * base_config.C_to_temperature_gain)
    scaled = run_thermal_observable_bridge(scaled_config)

    path_work_residual = abs(base.C_path_work - scaled.C_path_work)
    entropy_ratio = scaled.fourier_entropy_proxy / base.fourier_entropy_proxy
    gates = {
        "C_path_work_invariant_under_gain_change_le_1e-12": path_work_residual
        <= 1e-12,
        "base_temperature_positive": base.minimum_temperature > 0.0,
        "scaled_temperature_positive": scaled.minimum_temperature > 0.0,
        "Fourier_entropy_source_nonnegative": base.minimum_fourier_entropy_source
        >= -1e-12,
        "Cattaneo_entropy_proxy_nonnegative": base.minimum_cattaneo_entropy_source
        >= -1e-12,
        "Cattaneo_numeric_reference_residual_le_1e-5": base.cattaneo_reference_residual
        <= 1e-5,
        "gain_change_changes_thermal_proxy": entropy_ratio > 1.5,
        "C_to_T_gain_remains_open": True,
    }
    return {
        "schema_version": "1.0",
        "artifact": "thermal_observable_bridge_verification",
        "audit_status": "PASS_WITH_BLOCKED_OPEN_MAPPING"
        if all(gates.values())
        else "FAIL",
        "claim_status": "SIMULATION_ONLY",
        "evidence_class": "INTERNAL_OBSERVABLE_MAPPING_DIAGNOSTIC",
        "status": "BLOCKED_OPEN_MAPPING",
        "unit_lane": "normalized",
        "standard_counterpart": "Fourier and Cattaneo heat transport with a local entropy-production proxy",
        "uet_status": "C_IS_NOT_TEMPERATURE_OR_HEAT_FLUX",
        "config": {
            "spatial_points": base_config.spatial_points,
            "time_steps": base_config.time_steps,
            "duration": base_config.duration,
            "C_amplitude": base_config.C_amplitude,
            "temperature_background": base_config.temperature_background,
            "base_C_to_temperature_gain": base_config.C_to_temperature_gain,
            "scaled_C_to_temperature_gain": scaled_config.C_to_temperature_gain,
            "conductivity": base_config.conductivity,
            "tau_q": base_config.tau_q,
            "drive_omega": base_config.drive_omega,
        },
        "formula_audit": [
            {
                "formula_id": "THERMAL-MAP-001",
                "relation": "T_norm=T0+alpha_T*C",
                "variables_and_units": "C dimensionless normalized coordinate; T_norm and T0 normalized temperature proxy; alpha_T normalized gain",
                "constant_origin": "open_placeholder / heuristic bridge",
                "proof_status": "open correspondence diagnostic",
                "verification_role": "gain identifiability blocker",
                "failure_mode": "C is called temperature or alpha_T is fitted and reported as derived",
                "next_hardening_step": "derive or source-lock a dimensional observable map with uncertainty",
            },
            {
                "formula_id": "THERMAL-FOURIER-002",
                "relation": "q_F=-k*grad(T), sigma_F=q_F^2/(k*T^2)>=0",
                "variables_and_units": "normalized k, T, q, and entropy-production proxy; SI W/m2 and W/(K*m3) not active",
                "constant_origin": "standard comparator relation",
                "proof_status": "checked local sign diagnostic",
                "verification_role": "standard heat/entropy comparator",
                "failure_mode": "normalized proxy is promoted to physical calorimetry",
                "next_hardening_step": "close physical heat-flux and entropy units for one material lane",
            },
            {
                "formula_id": "THERMAL-CATTANEO-003",
                "relation": "tau_q*dq/dt+q=-k*grad(T)",
                "variables_and_units": "normalized q, k, tau_q, T and spatial gradient",
                "constant_origin": "source-locked standard comparator form",
                "proof_status": "checked local numerical/analytic comparator",
                "verification_role": "causal delayed heat-flux control",
                "failure_mode": "Cattaneo control is presented as UET derivation",
                "next_hardening_step": "connect to an allowed external source package after observable map closure",
            },
        ],
        "metrics": {
            "C_path_work_base": base.C_path_work,
            "C_path_work_scaled_gain": scaled.C_path_work,
            "C_path_work_residual": path_work_residual,
            "Fourier_entropy_proxy_base": base.fourier_entropy_proxy,
            "Fourier_entropy_proxy_scaled_gain": scaled.fourier_entropy_proxy,
            "Fourier_entropy_proxy_ratio": entropy_ratio,
            "Cattaneo_entropy_proxy_base": base.cattaneo_entropy_proxy,
            "Cattaneo_entropy_proxy_scaled_gain": scaled.cattaneo_entropy_proxy,
            "Cattaneo_reference_residual": base.cattaneo_reference_residual,
            "minimum_temperature_base": base.minimum_temperature,
            "minimum_temperature_scaled_gain": scaled.minimum_temperature,
            "minimum_fourier_entropy_source": base.minimum_fourier_entropy_source,
            "minimum_cattaneo_entropy_source": base.minimum_cattaneo_entropy_source,
            "interpretation": "fixed C path does not identify thermal observable amplitude without an independent C-to-T gain",
        },
        "gates": gates,
        "limitations": [
            "prescribed synthetic periodic C path; no UET physical dynamics",
            "alpha_T is an open mapping coefficient and is not fitted",
            "all quantities are normalized; no SI temperature, flux, or entropy claim",
            "Cattaneo entropy quantity is a local proxy, not a complete extended entropy current",
            "no external source data, holdout, galaxy model, or extra force",
        ],
    }


def main() -> int:
    artifact = build_artifact()
    output = ROOT / "core" / "artifacts" / "thermal_observable_bridge_verification.json"
    output.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(artifact, indent=2, ensure_ascii=False))
    return 0 if artifact["audit_status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
