"""
Atomic predictive-v1 operator skeleton and diagnostic residual exporter.

This module is the future host for an accepted `delta_uet_or_ci` correction
operator. It may export diagnostic residual rows from existing verifier lanes,
but those rows are not accepted correction-operator evidence until a fixed
CI/correlated or UET atomic operator is implemented.
"""

from __future__ import annotations

import json
from pathlib import Path


def _diagnostic_residual_rows(
    helium_holdout_predictions: list[dict] | None,
    baseline_constants: dict | None,
) -> list[dict]:
    baseline_constants = baseline_constants or {}
    rydberg_energy_eV = baseline_constants.get("R_infinity_energy_eV")
    first_ionization_energy_eV = baseline_constants.get("first_ionization_energy_eV")
    rows = []
    for row in helium_holdout_predictions or []:
        n = row["outer_principal_quantum_number"]
        baseline_outer_binding_eV = (
            rydberg_energy_eV / (n * n) if rydberg_energy_eV is not None else None
        )
        baseline_excitation_energy_eV = (
            first_ionization_energy_eV - baseline_outer_binding_eV
            if first_ionization_energy_eV is not None and baseline_outer_binding_eV is not None
            else None
        )
        delta_energy_eV = (
            row["predicted_excitation_energy_eV"] - baseline_excitation_energy_eV
            if baseline_excitation_energy_eV is not None
            else None
        )
        baseline_residual_eV = (
            baseline_excitation_energy_eV - row["observed_excitation_energy_eV"]
            if baseline_excitation_energy_eV is not None
            else None
        )
        baseline_absolute_residual_eV = (
            abs(baseline_residual_eV) if baseline_residual_eV is not None else None
        )
        residual_improvement_eV = (
            baseline_absolute_residual_eV - row["absolute_residual_eV"]
            if baseline_absolute_residual_eV is not None
            else None
        )
        residual_improvement_ratio = (
            residual_improvement_eV / baseline_absolute_residual_eV
            if baseline_absolute_residual_eV not in (None, 0)
            else None
        )
        rows.append(
            {
                "row_id": f"operator_v1_diag_{row['holdout_id']}",
                "source_row_id": row["holdout_id"],
                "lane_id": "helium_quantum_defect_same_source_family_holdout",
                "operator_id": "empirical_quantum_defect_diagnostic_not_delta_uet_or_ci",
                "baseline_model_id": "zero_quantum_defect_hydrogenic_baseline",
                "diagnostic_model_id": "source_calibrated_quantum_defect_same_series_mean",
                "baseline_predicted_excitation_energy_eV": baseline_excitation_energy_eV,
                "baseline_outer_binding_eV": baseline_outer_binding_eV,
                "baseline_residual_eV_predicted_minus_observed": baseline_residual_eV,
                "baseline_absolute_residual_eV": baseline_absolute_residual_eV,
                "predicted_excitation_energy_eV": row["predicted_excitation_energy_eV"],
                "delta_energy_eV": delta_energy_eV,
                "observed_excitation_energy_eV": row["observed_excitation_energy_eV"],
                "absolute_residual_eV": row["absolute_residual_eV"],
                "residual_improvement_eV": residual_improvement_eV,
                "residual_improvement_ratio": residual_improvement_ratio,
                "model_uncertainty_eV": row.get("predicted_excitation_model_uncertainty_eV"),
                "source_uncertainty_eV_or_rounding_bound": row.get("excitation_energy_uncertainty_eV"),
                "uncertainty_computable": (
                    row.get("predicted_excitation_model_uncertainty_eV") is not None
                    and row.get("excitation_energy_uncertainty_eV") is not None
                ),
                "parameters_locked_before_evaluation": True,
                "used_for_parameter_fit": False,
                "source_family": "NIST_ASD_same_source_family",
                "claim_use": "diagnostic_only_not_validation",
                "source_locator": row.get("source_locator"),
                "residual_eV_predicted_minus_observed": row.get("residual_eV_predicted_minus_observed"),
                "uncertainty_basis": {
                    "model": row.get("predicted_excitation_model_uncertainty_basis"),
                    "source": "excitation-energy uncertainty converted from source transcription bound",
                },
                "delta_energy_basis": (
                    "diagnostic quantum-defect prediction minus zero-quantum-defect hydrogenic baseline; "
                    "not accepted as delta_uet_or_ci"
                ),
            }
        )
    return rows


def run_atomic_operator_v1(
    helium_holdout_predictions: list[dict] | None = None,
    baseline_constants: dict | None = None,
    write_artifact_path: str | Path | None = None,
) -> dict:
    """Return the current operator-v1 gate without accepting a correction operator."""
    residual_rows = _diagnostic_residual_rows(helium_holdout_predictions, baseline_constants)
    baseline_residuals = [
        row["baseline_absolute_residual_eV"]
        for row in residual_rows
        if row["baseline_absolute_residual_eV"] is not None
    ]
    diagnostic_residuals = [row["absolute_residual_eV"] for row in residual_rows]
    improvements = [
        row["residual_improvement_eV"]
        for row in residual_rows
        if row["residual_improvement_eV"] is not None
    ]
    residual_artifact = {
        "schema_version": "1.0",
        "artifact_id": "atomic_predictive_v1_operator_residual_rows",
        "status": "DIAGNOSTIC_RESIDUAL_ROWS_EXPORTED_OPERATOR_NOT_ACCEPTED"
        if residual_rows
        else "OPERATOR_V1_SKELETON_READY_RESIDUALS_MISSING",
        "claim_class": "diagnostic_residual_rows_no_validation_claim",
        "accepted_as_delta_uet_or_ci": False,
        "execution_mode": "diagnostic_export_only",
        "residual_rows": residual_rows,
        "metrics": {
            "residual_row_count": len(residual_rows),
            "accepted_operator_count": 0,
            "parameters_locked_before_evaluation_count": sum(
                1 for row in residual_rows if row["parameters_locked_before_evaluation"]
            ),
            "used_for_parameter_fit_count": sum(1 for row in residual_rows if row["used_for_parameter_fit"]),
            "diagnostic_only_row_count": sum(
                1 for row in residual_rows if row["claim_use"] == "diagnostic_only_not_validation"
            ),
            "uncertainty_computable_row_count": sum(
                1 for row in residual_rows if row.get("uncertainty_computable") is True
            ),
            "delta_energy_populated_count": sum(
                1 for row in residual_rows if row["delta_energy_eV"] is not None
            ),
            "baseline_residual_populated_count": len(baseline_residuals),
            "residual_improvement_populated_count": len(improvements),
            "residual_improved_row_count": sum(
                1 for value in improvements if value is not None and value > 0
            ),
            "average_baseline_abs_residual_eV": (
                sum(baseline_residuals) / len(baseline_residuals) if baseline_residuals else None
            ),
            "average_diagnostic_abs_residual_eV": (
                sum(diagnostic_residuals) / len(diagnostic_residuals) if diagnostic_residuals else None
            ),
            "average_residual_improvement_eV": (
                sum(improvements) / len(improvements) if improvements else None
            ),
            "max_residual_improvement_eV": max(improvements) if improvements else None,
        },
        "claim_boundary": (
            "Rows exported here are same-source-family diagnostic residual rows. "
            "They do not implement or validate delta_uet_or_ci."
        ),
    }
    if write_artifact_path is not None:
        path = Path(write_artifact_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(residual_artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "atomic_predictive_v1_operator_residual_gate": {
            "schema_version": "1.0",
            "role": "atomic_predictive_v1_operator_residual_gate",
            "status": residual_artifact["status"],
            "claim_class": "operator_skeleton_or_diagnostic_rows_no_validation_claim",
            "operator_id": "delta_uet_or_ci",
            "accepted_as_delta_uet_or_ci": False,
            "execution_mode": "diagnostic_export_only",
            "residual_rows": residual_rows,
            "metrics": residual_artifact["metrics"],
            "blocked_claims": [
                "operator skeleton is an implemented correction operator",
                "diagnostic residual rows validate atomic spectra",
                "accepted_operator_count can rise before residual and uncertainty artifacts exist",
            ],
            "next_required_artifacts": [
                "Data/03_Research/atomic_predictive_v1_operator_parameters.json",
                "Result/artifacts/atomic_predictive_v1_operator_residual_rows.json",
                "Data/03_Research/atomic_predictive_v1_operator_uncertainty_policy.json",
            ],
            "claim_boundary": "This skeleton only establishes the target entrypoint. It does not implement or validate delta_uet_or_ci.",
        }
    }


if __name__ == "__main__":
    gate = run_atomic_operator_v1()["atomic_predictive_v1_operator_residual_gate"]
    print(gate["status"])
