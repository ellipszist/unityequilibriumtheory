"""Audit whether current graphite sources form a same-state alpha_V/K_T pair."""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs/core/artifacts/t13_graphite_alpha_v_kt_matched_source_boundary_audit.json"

AUDIT_PATHS = {
    "nist_alpha_v": ROOT / "docs/core/artifacts/t13_nist_graphite_alpha_v_source_boundary_audit.json",
    "hanfland_kt": ROOT / "docs/core/artifacts/t13_graphite_isothermal_kt_source_audit.json",
    "bosak_elastic_bulk": ROOT / "docs/core/artifacts/t13_graphite_elastic_bulk_modulus_source_audit.json",
    "tpg_alpha_v": ROOT / "docs/core/artifacts/t13_tpg_anisotropic_alpha_v_source_audit.json",
    "nelson_riley_alpha_v": ROOT / "docs/core/artifacts/t13_natural_graphite_nelson_riley_alpha_v_source_audit.json",
}

PACKAGE_PATHS = {
    "nist_alpha_v": ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/nist_axm5q1_density_source_package.json",
    "hanfland_kt": ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/hanfland_1989_graphite_isothermal_kt_source_package.json",
    "bosak_elastic_bulk": ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/bosak_2007_graphite_elastic_bulk_source_package.json",
    "tpg_alpha_v": ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/ihep_2001_32_tpg_anisotropic_alpha_v_source_package.json",
    "nelson_riley_alpha_v": ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/argonne_anl_5524_nelson_riley_alpha_v_source_package.json",
}

LOWITZER_CANDIDATE = ROOT / (
    "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/"
    "lowitzer_2006_graphite_pvt_candidate_source_package.json"
)
TOHEI_TABLE = ROOT / (
    "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/"
    "tohei_2006_graphite_alpha_v_kt_table_comparator_source_package.json"
)
FAROOQUI_IG210 = ROOT / (
    "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/"
    "farooqui_2022_ig210_thermophysical_source_package.json"
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def all_holdout_locked(artifacts: dict[str, dict], packages: dict[str, dict]) -> bool:
    records = [*artifacts.values(), *packages.values()]
    for record in records:
        policy = record.get("holdout_policy", {})
        if not policy:
            continue
        if any(
            policy.get(key) is True
            for key in (
                "xie_2026_accessed",
                "xie_2026_source_data_consumed",
                "target_curve_used",
                "alpha_fit_used",
                "used_for_fit",
                "used_for_tuning",
                "used_for_calibration",
            )
        ):
            return False
    return True


def main() -> int:
    audits = {key: load_json(path) for key, path in AUDIT_PATHS.items()}
    packages = {key: load_json(path) for key, path in PACKAGE_PATHS.items()}
    lowitzer = load_json(LOWITZER_CANDIDATE)
    tohei = load_json(TOHEI_TABLE)
    farooqui = load_json(FAROOQUI_IG210)
    nist = audits["nist_alpha_v"]
    hanfland = audits["hanfland_kt"]
    bosak = audits["bosak_elastic_bulk"]
    tpg = audits["tpg_alpha_v"]
    nelson = audits["nelson_riley_alpha_v"]
    hanfland_contract = packages["hanfland_kt"]["thermodynamic_contract"]
    tpg_boundary = packages["tpg_alpha_v"]["source"]["material_regime_boundary"]

    checks = {
        "nist_alpha_source_is_lane_locked": nist["status"]
        == "PASS_SCOPED_NIST_ALPHA_V_SOURCE_BOUNDARY",
        "nist_alpha_has_rows": len(nist.get("rows", [])) >= 4,
        "nist_is_axm_5q1": nist["source"]["source_id"] == "nist_srm_260_89_axm_5q1_graphite",
        "nist_does_not_emit_kt": nist.get("numeric_K_T_emitted", False) is False,
        "hanfland_kt_source_is_lane_locked": hanfland["status"]
        == "PASS_SCOPED_ISOTHERMAL_GRAPHITE_K_T_SOURCE",
        "hanfland_is_natural_graphite_powder": "natural graphite powder"
        in hanfland["source"]["material"].lower(),
        "hanfland_same_state_alpha_is_missing": hanfland_contract[
            "same_state_alpha_V_available"
        ]
        is False,
        "hanfland_ding_mapping_is_open": hanfland_contract[
            "Ding_material_regime_mapping_closed"
        ]
        is False,
        "bosak_bulk_is_not_thermal_kt": any(
            "thermal isothermal K_T" in item
            for item in bosak["source"]["source_limitations"]
        ),
        "bosak_ding_mapping_is_not_claimed": any(
            "not demonstrated to be the Ding TTG sample" in item
            for item in bosak["source"]["source_limitations"]
        ),
        "tpg_same_specimen_is_false": tpg_boundary["same_specimen_for_both_axes"]
        is False,
        "tpg_same_temperature_is_false": tpg_boundary["same_temperature_point"]
        is False,
        "tpg_ding_mapping_is_open": tpg_boundary[
            "ding_ttg_material_regime_mapping_closed"
        ]
        is False,
        "nelson_uncertainty_is_not_row_level": "no row-level statistical uncertainty"
        in nelson["source"]["uncertainty_boundary"],
        "nelson_same_specimen_is_false": nelson["derived_comparator"][
            "same_specimen_alpha_V"
        ]
        is False,
        "all_current_pairs_fail_same_state_contract": hanfland_contract[
            "same_state_alpha_V_available"
        ]
        is False
        and tpg["derived_comparator"]["same_state_K_T"] is False
        and nelson["derived_comparator"]["same_state_K_T"] is False,
        "lowitzer_candidate_is_abstract_only": lowitzer["source"]["payload_state"] == "ABSTRACT_ONLY",
        "lowitzer_has_no_numeric_alpha_rows": lowitzer["pair_contract"]["numeric_alpha_V_rows_available"] is False,
        "lowitzer_has_no_numeric_kt_rows": lowitzer["pair_contract"]["numeric_K_T_rows_available"] is False,
        "lowitzer_has_no_source_grade_uncertainty": lowitzer["pair_contract"]["source_grade_uncertainty_available"] is False,
        "lowitzer_does_not_close_pair": lowitzer["pair_contract"]["same_state_alpha_V_and_K_T_pair_closed"] is False,
        "lowitzer_ding_mapping_is_open": lowitzer["pair_contract"]["Ding_material_regime_mapping_closed"] is False,
        "lowitzer_does_not_emit_correction": lowitzer["pair_contract"]["numeric_cp_cv_correction_emitted"] is False,
        "tohei_is_a_primary_table_comparator": tohei["source"]["payload_state"]
        == "REMOTE_PRIMARY_TABLE_LOCATOR_SCREENED",
        "tohei_has_numeric_graphite_alpha_and_b0": tohei["pair_contract"][
            "numeric_table_alpha_V_present"
        ]
        and tohei["pair_contract"]["numeric_table_K_T_or_B0_present"],
        "tohei_same_calculation_pair_is_explicit": tohei["pair_contract"][
            "same_calculation_alpha_V_and_B0_pair_present"
        ],
        "tohei_experimental_pair_is_not_same_specimen": tohei["pair_contract"][
            "same_specimen_experimental_alpha_V_and_K_T_pair_established"
        ]
        is False,
        "tohei_uncertainty_is_not_promoted": tohei["pair_contract"][
            "source_grade_uncertainty_available"
        ]
        is False,
        "tohei_ding_mapping_is_open": tohei["pair_contract"][
            "Ding_material_regime_mapping_closed"
        ]
        is False,
        "tohei_does_not_emit_correction": tohei["pair_contract"][
            "numeric_cp_cv_correction_emitted"
        ]
        is False,
        "farooqui_source_is_lane_locked": farooqui["status"]
        == "SOURCE_LOCKED_IG210_THERMOPHYSICAL_COMPARATOR_KT_OPEN",
        "farooqui_has_same_grade_rows": farooqui["derived_comparator"][
            "same_grade_ig210_source"
        ]
        is True
        and farooqui["derived_comparator"]["row_count"] == 3,
        "farooqui_has_alpha_l_cp_and_k": farooqui["derived_comparator"][
            "thermal_expansion_alpha_l_present"
        ]
        and farooqui["derived_comparator"]["specific_heat_Cp_present"]
        and all(
            "thermal_conductivity_W_per_m_K" in row
            for row in farooqui["source_rows"]
        ),
        "farooqui_same_state_kt_is_missing": farooqui["derived_comparator"][
            "same_state_K_T_present"
        ]
        is False,
        "farooqui_cv_is_missing": farooqui["derived_comparator"]["c_v_present"]
        is False,
        "farooqui_ding_mapping_is_open": farooqui["derived_comparator"][
            "Ding_TTG_material_match_closed"
        ]
        is False,
        "farooqui_does_not_emit_alpha": farooqui["derived_comparator"][
            "alpha_Phi_K_calibration_emitted"
        ]
        is False,
        "holdout_is_unconsumed": all_holdout_locked(audits, packages)
        and all_holdout_locked(
            {"lowitzer": lowitzer, "tohei": tohei, "farooqui": farooqui}, {}
        ),
    }
    status = (
        "PASS_SCOPED_GRAPHITE_ALPHA_V_K_T_MATCHED_SOURCE_BOUNDARY_NO_GO"
        if all(checks.values())
        else "FAIL_GRAPHITE_ALPHA_V_K_T_MATCHED_SOURCE_BOUNDARY_AUDIT"
    )

    evidence = []
    evidence_paths = [
        *AUDIT_PATHS.items(),
        *PACKAGE_PATHS.items(),
        ("lowitzer_candidate", LOWITZER_CANDIDATE),
        ("tohei_table_comparator", TOHEI_TABLE),
        ("farooqui_ig210_thermophysical", FAROOQUI_IG210),
    ]
    for key, path in evidence_paths:
        evidence.append(
            {
                "role": key,
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
            }
        )

    report = {
        "schema_version": "t13-graphite-alpha-v-kt-matched-source-boundary-v1",
        "artifact": "t13_graphite_alpha_v_kt_matched_source_boundary_audit",
        "generated_at": date.today().isoformat(),
        "status": status,
        "major_result": {
            "major_result_id": "T13_GRAPHITE_ALPHA_V_K_T_MATCHED_SOURCE_BOUNDARY",
            "topic": "0.13_Thermodynamic_Bridge",
            "closure_level": "CLOSED_FOR_LANE" if status.startswith("PASS") else "OPEN",
            "what_is_closed": (
                "The current archived graphite source inventory, including the "
                "screened Lowitzer P-V-T candidate, Tohei table comparator, and "
                "source-locked IG210 thermophysical comparator, cannot form a "
                "same-state, same-grade alpha_V/K_T pair with source-grade "
                "uncertainty for the Cp-to-Cv correction. The individual alpha_V "
                "and K_T comparator lanes remain separate. Tohei supplies a "
                "numeric same-calculation QHA pair and separately sourced "
                "experimental table values, but neither closes the source-grade "
                "correction contract. The IG210 rows supply same-grade C_p and "
                "alpha_l values but no same-state K_T."
            ),
            "equation_or_mapping": {
                "cp_cv_correction": "c_p^V - c_v^V = T * alpha_V^2 * K_T",
                "volumetric_conversion": "c_p^V = rho * c_p; c_v^V = c_p^V - T * alpha_V^2 * K_T",
            },
            "units": {
                "alpha_V": "K^-1",
                "K_T": "Pa",
                "temperature": "K",
                "volumetric_heat_capacity": "J m^-3 K^-1",
            },
            "derivation_class": "source compatibility and uncertainty-boundary audit; no UET derivation",
            "observable": "same-state graphite alpha_V/K_T correction inputs",
            "data_role": "SOURCE_PROVENANCE_BOUNDARY_NOT_CALIBRATION",
            "evidence_artifacts": evidence,
            "verification_status": status,
            "open_blockers": [
                "same_grade_alpha_V_and_K_T_missing",
                "same_state_IG210_K_T_missing",
                "density_uncertainty_not_source_locked",
                "material_regime_mapping_to_TTG_not_closed",
                "c_v_source_uncertainty_not_closed",
                "alpha_Phi_K_independent_calibration_missing",
            ],
            "dependency_unlocked": (
                "Current alpha_V/K_T source-pair inventory boundary only; no "
                "Cp-to-Cv input closure, Ding C_src, alpha_Phi_K, Full Topic 13, "
                "Core, or Gravity unlock"
            ),
            "claim_boundary": (
                "This closes a route-level source compatibility boundary, including "
                "the screened abstract-only Lowitzer candidate, not the existence "
                "of all possible future alpha_V/K_T data. It is not a same-state "
                "thermodynamic correction, Ding validation, UET calibration, TTG "
                "prediction, or external validation."
            ),
        },
        "source_pair_observations": {
            "nist_alpha_v": {
                "source_id": nist["source"]["source_id"],
                "material": nist["source"]["source"]["material"]
                if "source" in nist["source"]
                else nist["source"]["material"],
                "alpha_V_rows": len(nist.get("rows", [])),
                "K_T_emitted": nist.get("numeric_K_T_emitted", False),
                "source_sha256": nist["source"]["sha256"],
            },
            "hanfland_kt": {
                "source_id": hanfland["source"]["source_id"],
                "material": hanfland["source"]["material"],
                "temperature_K": hanfland["source"]["temperature_K"],
                "same_state_alpha_V_available": hanfland_contract[
                    "same_state_alpha_V_available"
                ],
                "source_sha256": hanfland["source"]["sha256"],
            },
            "bosak_elastic_bulk": {
                "source_id": bosak["source"]["source_id"],
                "material": bosak["source"]["material"],
                "temperature_scope": bosak["source"]["temperature_scope"],
                "thermal_K_T_claimed": False,
                "source_sha256": bosak["source"]["sha256"],
            },
            "tpg_alpha_v": {
                "source_id": tpg["source"]["source_id"],
                "same_specimen_for_both_axes": tpg_boundary[
                    "same_specimen_for_both_axes"
                ],
                "same_temperature_point": tpg_boundary["same_temperature_point"],
                "same_state_K_T": tpg["derived_comparator"]["same_state_K_T"],
                "source_sha256": tpg["source"]["sha256"],
            },
            "nelson_riley_alpha_v": {
                "source_id": nelson["source"]["source_id"],
                "same_specimen_alpha_V": nelson["derived_comparator"][
                    "same_specimen_alpha_V"
                ],
                "alpha_V_uncertainty_status": nelson["derived_comparator"][
                    "alpha_V_uncertainty_status"
                ],
                "source_sha256": nelson["source"]["sha256"],
            },
            "lowitzer_pvt_candidate": {
                "source_id": lowitzer["source"]["source_id"],
                "payload_state": lowitzer["source"]["payload_state"],
                "reported_scope": lowitzer["source"]["reported_scope"],
                "abstract_reported_fit_values": lowitzer["source"]["abstract_reported_fit_values"],
                "numeric_alpha_V_rows_available": lowitzer["pair_contract"]["numeric_alpha_V_rows_available"],
                "numeric_K_T_rows_available": lowitzer["pair_contract"]["numeric_K_T_rows_available"],
                "source_grade_uncertainty_available": lowitzer["pair_contract"]["source_grade_uncertainty_available"],
                "same_state_alpha_V_and_K_T_pair_closed": lowitzer["pair_contract"]["same_state_alpha_V_and_K_T_pair_closed"],
                "local_raw_sha256": lowitzer["source"]["local_raw_sha256"],
            },
            "tohei_table_comparator": {
                "source_id": tohei["source"]["source_id"],
                "payload_state": tohei["source"]["payload_state"],
                "source_locator": tohei["source"]["source_locator"],
                "calculated_graphite_pair": tohei["pair_contract"][
                    "same_calculation_alpha_V_and_B0_pair_present"
                ],
                "experimental_same_specimen_pair": tohei["pair_contract"][
                    "same_specimen_experimental_alpha_V_and_K_T_pair_established"
                ],
                "source_grade_uncertainty_available": tohei["pair_contract"][
                    "source_grade_uncertainty_available"
                ],
                "Ding_material_regime_mapping_closed": tohei["pair_contract"][
                    "Ding_material_regime_mapping_closed"
                ],
                "source_sha256": None,
            },
            "farooqui_ig210_thermophysical": {
                "source_id": farooqui["source"]["source_id"],
                "material": farooqui["source"]["material"],
                "temperature_scope": farooqui["source"]["temperature_scope"],
                "row_count": farooqui["derived_comparator"]["row_count"],
                "same_grade_source": farooqui["derived_comparator"][
                    "same_grade_ig210_source"
                ],
                "same_state_K_T_present": farooqui["derived_comparator"][
                    "same_state_K_T_present"
                ],
                "c_v_present": farooqui["derived_comparator"]["c_v_present"],
                "Ding_material_regime_mapping_closed": farooqui[
                    "derived_comparator"
                ]["Ding_TTG_material_match_closed"],
                "source_sha256": sha256(FAROOQUI_IG210),
            },
        },
        "checks": checks,
        "controlling_blocker": "same_grade_alpha_V_and_K_T_missing",
        "next_controller": (
            "Acquire a permitted full Lowitzer P-V-T payload or a permitted "
            "same-state IG210 K_T record, then seek a source-grade "
            "same-specimen/state-matched alpha_V and isothermal K_T source "
            "with uncertainty and Ding-regime mapping. The Tohei table may "
            "remain a comparator, and the Farooqui IG210 rows remain a "
            "thermophysical comparator; neither may be combined into a "
            "source-grade correction by assumption."
            ),
        "claim_boundary": (
            "No numeric Cp-to-Cv correction, Ding C_src, alpha_Phi_K, TTG "
            "prediction, or Full Topic 13 closure is emitted."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": status,
                "artifact": OUT.relative_to(ROOT).as_posix(),
                "failed_checks": [key for key, value in checks.items() if not value],
            },
            indent=2,
        )
    )
    return 0 if status.startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
