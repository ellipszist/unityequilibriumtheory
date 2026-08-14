"""Add the lane-result key map required by the canonical Topic 13 gate builder."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"

LANE_KEY_BY_ID = {
    "T13_ALPHA_PHI_K_NORMALIZED_SCALE_NO_GO": "alpha_phi_k_normalized_scale_no_go",
    "T13_BASE_PHI_INDEPENDENT_CALIBRATION_REQUIREMENT": "base_phi_independent_calibration_requirement",
    "T13_BETA_SYMBOL_SEPARATION_NONCIRCULARITY_NO_GO": "beta_symbol_separation_non_circularity_no_go",
    "T13_CAUSAL_BRANCH_SELECTION": "causal_branch_selection",
    "T13_CAUSAL_FLUX_PHI_COUPLED_LANE": "causal_flux_phi_coupled_lane",
    "T13_CAUSAL_FLUX_TELEGRAPH_BRANCH": "causal_flux_telegraph_branch",
    "T13_COLLECTIVE_RESPONSE_EOS_STABILITY_CONTRACT": "collective_response_eos_stability_contract",
    "T13_COVARIANT_ACTION_SI_ANCHOR_ROUTE": "covariant_action_si_anchor_route",
    "T13_COVARIANT_FIELD_NORMALIZATION_IDENTIFIABILITY_NO_GO": "covariant_field_normalization_identifiability_no_go",
    "T13_COVARIANT_TRANSPORT_IMPLEMENTATION_BOUNDARY": "covariant_transport_implementation_boundary",
    "T13_CP_CV_CORRECTION_CONTRACT": "cp_cv_correction_contract",
    "T13_ALPHA_PHI_K_CONDITIONAL_DERIVATION": "alpha_phi_k_conditional_derivation",
    "T13_DING_PBTE_AUTHOR_REQUEST_PACKAGE": "ding_pbte_author_request_package",
    "T13_DING_PBTE_ENERGY_TEMPERATURE_MAPPING": "ding_pbte_energy_temperature_mapping",
    "T13_DING_PBTE_OA_NUMERIC_INPUT_NO_GO": "ding_pbte_oa_numeric_input_no_go",
    "T13_GATECH_STANDARD_TRANSPORT_COMPARATOR": "standard_graphite_transport_comparator",
    "T13_GATECH_VOLUMETRIC_CP_INDEPENDENCE_NO_GO": "gatech_volumetric_cp_independence_no_go",
    "T13_MP48_INDEPENDENT_GRAPHITE_CV_REPRODUCTION": "mp48_independent_graphite_cv_reproduction",
    "T13_PHYSICAL_KUBO_COEFFICIENT_PROVENANCE_GATE": "physical_kubo_coefficient_provenance",
    "T13_PHI_E_REFERENCE_NORMALIZATION": "phi_e_reference_normalization",
    "T13_PHI_E_TTG_BRIDGE_CONDITIONAL": "phi_e_ttg_bridge_conditional",
    "T13_PHI_ENERGY_ANCHOR_IDENTIFIABILITY_NO_GO": "phi_energy_anchor_identifiability_no_go",
    "T13_SK_KMS_ENTROPY_INTERFACE_CONTRACT": "sk_kms_entropy_interface_contract",
    "T13_SOURCE_CP_95CI_ANCHOR": "source_cp_95ci_anchor",
    "T13_STANDARD_O2_FINITE_TEMPERATURE_NORMAL_COMPARATOR": "standard_o2_finite_temperature_normal_comparator",
    "T13_THERMAL_RESPONSE_BETA_CONTRACT": "thermal_response_beta_contract",
    "T13_UET_O2_CONDENSATE_FLUCTUATION_SPECTRUM": "uet_o2_condensate_fluctuation_spectrum",
    "T13_UET_O2_CONDENSATE_GOLDSTONE_IDEAL_LANE": "uet_o2_condensate_goldstone_ideal_lane",
    "T13_UET_O2_ONE_LOOP_CONVERGENCE": "uet_o2_one_loop_convergence",
    "T13_UET_O2_ONE_LOOP_NORMAL_BRANCH": "uet_o2_one_loop_normal_branch",
    "T13_UET_O2_ONE_LOOP_THERMAL_UV_BOUNDARY": "uet_o2_one_loop_uv_boundary",
}


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    if "LANE_KEY_BY_ID = {" in text:
        print("FULL_GATE_LANE_KEY_MAPPING_ALREADY_PRESENT")
        return 0

    marker = (
        'OUT = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/'
        'topic13_full_thermodynamic_bridge_core_ready_gate.json"\n\n\n'
    )
    mapping = "LANE_KEY_BY_ID = " + repr(LANE_KEY_BY_ID) + "\n\n\n"
    if text.count(marker) != 1:
        raise SystemExit(f"full-gate module marker count: {text.count(marker)}")
    TARGET.write_text(text.replace(marker, marker + mapping, 1), encoding="utf-8")
    print("ADDED_FULL_GATE_LANE_KEY_MAPPING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
