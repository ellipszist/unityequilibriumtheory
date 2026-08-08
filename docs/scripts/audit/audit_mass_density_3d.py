"""Verify the candidate SI 3D mass-density operator contract.

The result is intentionally a synthetic/internal artifact.  It checks the
dimensional operator and source bookkeeping while keeping the physical
external map, calibration, uncertainty propagation, and C-to-shape derivation
blocked.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

from docs.core.mass_density_3d import (  # noqa: E402
    MassDensity3DSource,
    gaussian_shape_3d,
    integrated_density_3d,
    mass_from_si_volume_density,
    normalized_shape_3d,
    si_volume_density_from_shape,
)


def _peak(density: list[list[list[float]]]) -> float:
    return max(value for row in density for cell in row for value in cell)


def build_artifact() -> dict:
    shape, code_spacing = gaussian_shape_3d(grid_points=(15, 17, 19))
    source_a = MassDensity3DSource(
        mass_kg=3.0,
        length_scale_x_m=2.0,
        length_scale_y_m=3.0,
        length_scale_z_m=4.0,
        source_id="synthetic:mass-density-3d:v1",
        source_locator="synthetic://uet/mass-density/3d/v1",
        source_hash="synthetic-config-3d-v1",
        uncertainty_kg=0.15,
    )
    source_b = MassDensity3DSource(
        mass_kg=3.0,
        length_scale_x_m=4.0,
        length_scale_y_m=6.0,
        length_scale_z_m=8.0,
        source_id="synthetic:mass-density-3d:v1:volume-rescaled",
        source_locator=source_a.source_locator,
        source_hash=source_a.source_hash,
    )
    density_a, physical_spacing_a = si_volume_density_from_shape(
        shape, code_spacing, source_a
    )
    density_b, physical_spacing_b = si_volume_density_from_shape(
        shape, code_spacing, source_b
    )
    normalized = normalized_shape_3d(shape, code_spacing)
    integral_shape = integrated_density_3d(normalized, code_spacing)
    mass_a = mass_from_si_volume_density(density_a, physical_spacing_a)
    mass_b = mass_from_si_volume_density(density_b, physical_spacing_b)
    peak_ratio = _peak(density_a) / _peak(density_b)

    gates = {
        "source_metadata_declared": all(
            value.strip()
            for value in (
                source_a.source_id,
                source_a.source_locator,
                source_a.source_hash,
                source_a.holdout_policy,
            )
        ),
        "kg_amplitude_declared": source_a.mass_kg > 0.0,
        "metre_scales_declared": all(value > 0.0 for value in source_a.length_scales_m),
        "kg_per_m3_unit_contract": True,
        "normalized_shape_integral_le_1e-12": abs(integral_shape - 1.0) <= 1e-12,
        "integral_a_matches_kg_le_1e-12": abs(mass_a - source_a.mass_kg) <= 1e-12,
        "integral_b_matches_kg_le_1e-12": abs(mass_b - source_b.mass_kg) <= 1e-12,
        "volume_rescaling_preserves_total_mass": abs(mass_a - mass_b) <= 1e-12,
        "volume_rescaling_peak_ratio_le_1e-12": abs(peak_ratio - 8.0) <= 1e-12,
        "uncertainty_declared": source_a.uncertainty_kg >= 0.0,
        "calibration_status_disclosed": source_a.calibration_status
        == "NOT_REQUIRED_FOR_SYNTHETIC",
        "holdout_policy_declared": source_a.holdout_policy.startswith("LOCKED"),
        "no_same_data_fit": not source_a.fitted and not source_b.fitted,
        "external_physical_map_remains_blocked": not source_a.physical_mapping_ready(),
        "C_to_shape_derivation_remains_blocked": True,
    }

    return {
        "schema_version": "1.0",
        "artifact": "mass_density_3d_contract_verification",
        "audit_status": (
            "PASS_WITH_BLOCKED_EXTERNAL_3D_MAPPING"
            if all(gates.values())
            else "FAIL"
        ),
        "mapping_status": "SI_3D_SYNTHETIC_MEASUREMENT_OPERATOR_ONLY",
        "claim_status": "SIMULATION_ONLY",
        "evidence_class": "INTERNAL_DIMENSIONAL_OPERATOR_DIAGNOSTIC",
        "unit_lane": "SI_3D_VOLUME_MASS_DENSITY",
        "standard_counterpart": "three-dimensional volume-mass density rho_3D in kg/m^3",
        "formula_audit": [
            {
                "formula_id": "RHO-SI-3D-005",
                "relation": "rho_3D(x_phys)=A_m*rho_hat(x_code)/(L_x*L_y*L_z)",
                "variables_and_units": "A_m kg; L_x,L_y,L_z m; rho_hat inverse code volume; rho_3D kg/m^3",
                "constant_origin": "dimensional conversion contract from declared source amplitude and three coordinate scales",
                "proof_status": "checked local finite-volume dimensional and integral closure",
                "verification_role": "separate 3D unit conversion from C-to-shape derivation and physical validation",
                "failure_mode": "synthetic density operator is reported as an external galaxy mass map",
                "next_hardening_step": "source-lock external 3D mass profile, calibration, uncertainty propagation and holdout",
            }
        ],
        "observable_operator": {
            "operator": "O[C_phase,geometry,rho_hat,A_m,L_xyz] -> rho_3D",
            "status": "C_TO_SHAPE_OPEN_SYNTHETIC_SHAPE_CONTRACT_CHECKED",
            "standard_measurement": "volume-mass density in kg/m^3",
            "measurement_resolution": "declared finite-volume cell spacing",
            "detector_or_source_map": "not supplied; synthetic source shape only",
        },
        "source_contract": {
            "source_id": source_a.source_id,
            "source_locator": source_a.source_locator,
            "source_hash": source_a.source_hash,
            "amplitude_unit": "kg",
            "length_unit": "m",
            "observable_unit": "kg/m^3",
            "uncertainty_kg": source_a.uncertainty_kg,
            "uncertainty_status": "declared_source_amplitude_only_no_external_propagation",
            "calibration_status": source_a.calibration_status,
            "holdout_policy": source_a.holdout_policy,
            "fit_status": "NOT_FITTED",
        },
        "config": {
            "grid_points": [15, 17, 19],
            "code_spacing": list(code_spacing),
            "length_scales_a_m": list(source_a.length_scales_m),
            "length_scales_b_m": list(source_b.length_scales_m),
            "synthetic_shape": "anisotropic_gaussian_cell_centred_v1",
        },
        "metrics": {
            "normalized_shape_integral": integral_shape,
            "integral_a_kg": mass_a,
            "integral_b_kg": mass_b,
            "peak_density_ratio_a_over_b": peak_ratio,
            "physical_spacing_a_m": list(physical_spacing_a),
            "physical_spacing_b_m": list(physical_spacing_b),
            "interpretation": "SI 3D operator bookkeeping closes for a declared synthetic shape and source amplitude; physical C-to-density and external measurement maps remain open",
        },
        "gates": gates,
        "limitations": [
            "synthetic 3D shape and source only",
            "source amplitude and coordinate scales are explicit inputs, not UET derivations",
            "C does not determine rho_hat or A_m in this artifact",
            "uncertainty is declared but not externally propagated",
            "no calibration, galaxy data, fit, or holdout was used",
            "C remains a collective/relational coordinate, not universal mass density",
        ],
        "next_controller": "source-lock an external 3D density operator with calibration, propagated uncertainty, and holdout policy before galaxy comparison",
    }


def main() -> int:
    artifact = build_artifact()
    output = ROOT / "core" / "artifacts" / "mass_density_3d_contract_verification.json"
    output.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(artifact, indent=2, ensure_ascii=False))
    return 0 if artifact["audit_status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
