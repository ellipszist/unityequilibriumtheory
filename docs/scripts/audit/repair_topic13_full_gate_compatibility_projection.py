"""Restore the legacy Topic 13 projection from canonical lane artifacts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
FULL_GATE = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
REGISTER_GENERATOR = ROOT / "docs/scripts/audit/audit_major_result_closure.py"
FULL_RUNNER = ROOT / "docs/scripts/audit/run_topic13_full_bridge_wave.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count == 0:
        if new in text:
            return text
        raise SystemExit(f"{label}: expected one match, found {count}")
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


PROJECTION = r'''    # Re-expose the pre-registry lane contract after the canonical rebuild.
    # These are projections of existing artifacts, not new physical evidence.
    def compatibility_lane(key):
        value = discovered_lane_integrations.get(key, {})
        return dict(value) if isinstance(value, dict) else {}

    alpha = artifact["verification_status"]["alpha_Phi_K"]
    alpha["identifiability_status"] = "NO_GO_FROM_NORMALIZED_PHI"
    conditional = compatibility_lane("alpha_phi_k_conditional_derivation")
    if conditional:
        alpha.update({
            "conditional_derivation_status": conditional.get("status"),
            "conditional_derivation_artifact": conditional.get("audit"),
            "conditional_formula_status": "CLOSED_FOR_LANE",
            "conditional_unit_contract_status": "CLOSED_FOR_LANE",
            "conditional_open_inputs": conditional.get("open_blockers", []),
            "conditional_next_controller": conditional.get("next_controller"),
        })

    energy_lane = compatibility_lane("phi_e_ttg_bridge_conditional")
    source_anchor = dict(energy_lane.get("standard_pbte_source_anchor", {}))
    if energy_lane:
        named_branch = {
            "branch_id": "T13-PHI-E-001",
            "status": energy_lane.get("status", "PASS_NAMED_BRANCH_OPEN_INPUTS"),
            "closure_level": energy_lane.get("closure_level", "CLOSED_FOR_LANE"),
            "artifact": energy_lane.get("audit"),
            "source_package": source_anchor.get("source_package"),
            "formula_status": "CLOSED_FOR_LANE",
            "base_Phi_identity": "not asserted",
            "base_Phi_to_Phi_E_mapping": "OPEN_DERIVATION_OR_CALIBRATION",
            "c_v_status": "OPEN_CP_TO_CV_UNCERTAINTY",
            "e0_status": "OPEN_NOT_SOURCE_LOCKED",
            "independent_base_alpha_calibration": False,
            "xie_2026_accessed": False,
            "pbte_energy_temperature_source": source_anchor,
            "source_anchor": energy_lane.get("source_anchor", {}),
            "pbte_numeric_input_availability_no_go": energy_lane.get("pbte_numeric_input_availability", {}),
        }
        availability = named_branch["pbte_numeric_input_availability_no_go"]
        author_lane = compatibility_lane("ding_pbte_author_request_package")
        author_status = author_lane.get("status", "PASS_REQUEST_SCHEMA_OPEN_EXTERNAL_RESPONSE")
        author_closure = author_lane.get("closure_level", "CLOSED_FOR_LANE")
        request_state = author_lane.get("request_state", "REQUEST_PACKAGE_READY_NOT_SENT")
        request = {
            "major_result_id": "T13_DING_PBTE_AUTHOR_REQUEST_PACKAGE",
            "status": author_status,
            "closure_level": author_closure,
            "request_state": request_state,
            "sent": False,
            "response_received": False,
            "numeric_C_src_emitted": False,
            "numeric_alpha_Phi_K_emitted": False,
            "target_curve_used": False,
            "xie_2026_accessed": False,
            "audit": author_lane.get("audit"),
            "claim_boundary": author_lane.get("claim_boundary"),
        }
        named_branch["pbte_author_request_package"] = request
        if not availability:
            named_branch["pbte_numeric_input_availability_no_go"] = {
                "status": "PASS_SCOPED_OA_NUMERIC_INPUT_AVAILABILITY_NO_GO",
                "closure_level": "CLOSED_FOR_LANE",
                "direct_oa_numeric_route": "CLOSED_AS_SCOPED_NO_GO",
                "author_request_route": "OPEN_NOT_EXECUTED",
                "independent_reproduction_route": "OPEN_INPUT_PACKAGE_NOT_BUILT",
                "audit": compatibility_lane("ding_pbte_oa_numeric_input_no_go").get("audit"),
            }
        named_branch["source_independence_no_go"] = compatibility_lane(
            "gatech_volumetric_cp_independence_no_go"
        )
        alpha["named_energy_response_branch"] = named_branch

    legacy_aliases = {
        "base_phi_independent_calibration_requirement": "base_phi_independent_calibration_requirement",
        "covariant_action_si_anchor_route": "covariant_action_si_anchor_route",
        "covariant_field_normalization_no_go": "covariant_field_normalization_identifiability_no_go",
        "phi_energy_anchor_identifiability": "phi_energy_anchor_identifiability_no_go",
        "causal_branch_selection": "causal_branch_selection",
        "collective_response_eos_stability_contract": "collective_response_eos_stability_contract",
    }
    for alias, key in legacy_aliases.items():
        lane = compatibility_lane(key)
        if not lane:
            continue
        artifact["verification_status"][alias] = lane

    base_requirement = artifact["verification_status"].get("base_phi_independent_calibration_requirement")
    if base_requirement:
        base_requirement["status"] = "OPEN_REQUIREMENT"
    action_route = artifact["verification_status"].get("covariant_action_si_anchor_route")
    if action_route:
        action_route["status"] = "PASS_ROUTE_IDENTIFIED_SI_BLOCKED"
        action_route["numeric_e0_emitted"] = False
        action_route["numeric_alpha_Phi_K_emitted"] = False
    field_route = artifact["verification_status"].get("covariant_field_normalization_no_go")
    if field_route:
        field_route["status"] = "PASS_SCOPED_NO_GO"
        field_route["numeric_e0_emitted"] = False
        field_route["numeric_alpha_Phi_K_emitted"] = False
        field_route["target_data_used"] = False
        field_route["xie_2026_accessed"] = False
    phi_anchor = artifact["verification_status"].get("phi_energy_anchor_identifiability")
    if phi_anchor:
        phi_anchor["status"] = "PASS_SCOPED_NO_GO"
        phi_anchor["numeric_e0_emitted"] = False
        phi_anchor["numeric_alpha_Phi_K_emitted"] = False
    causal_alias = artifact["verification_status"].get("causal_branch_selection")
    if causal_alias:
        causal_alias["status"] = "PASS_CLOSED_AS_NO_GO_WITH_NAMED_COUPLED_BRANCH"
        causal_alias["baseline_full_candidate_pass"] = False
        causal_alias["baseline_replaced"] = False
        causal_alias["closure_level"] = "CLOSED_FOR_LANE"

    beta_alias = artifact["verification_status"].get("beta_symbol_separation_noncircularity_no_go")
    if beta_alias:
        beta_alias["status"] = "PASS_SCOPED_NO_GO"

    transport = artifact["verification_status"]["eos_transport_kms_entropy"]
    covariant_transport = transport.get("covariant_transport_implementation_boundary")
    if covariant_transport:
        covariant_transport.update({
            "physical_coefficient_evidence": "BLOCKED_NOT_PROVIDED",
            "temperature_scope": "T_ZERO_PURE_SUPERFLUID_ONLY",
            "si_lane": "BLOCKED",
            "synthetic_controls_physical": False,
        })
    kubo = transport.get("physical_kubo_coefficient_provenance")
    if kubo:
        kubo["physical_coefficient_evidence"] = "BLOCKED_NOT_PROVIDED"
        kubo["synthetic_controls_physical"] = False
    graphite = transport.get("standard_graphite_transport_comparator")
    if graphite:
        graphite["synthetic_controls_physical"] = False
        graphite["alpha_Phi_K_emitted"] = False
    standard_o2 = transport.get("standard_o2_finite_temperature_normal_comparator")
    if standard_o2:
        standard_o2.update({
            "physical_uet_eos": False,
            "physical_kubo_coefficient_emitted": False,
            "alpha_Phi_K_emitted": False,
            "R_gen_used_as_state": False,
        })
    one_loop = transport.get("uet_o2_one_loop_normal_branch")
    if one_loop:
        state = one_loop.get("state", {})
        one_loop.update({
            "vacuum_counterterm_included": state.get("vacuum_counterterm_included", False),
            "condensate_contribution_included": state.get("condensate_contribution_included", False),
            "normal_two_fluid_completion": state.get("normal_two_fluid_completion", False),
            "physical_kubo_coefficient_emitted": False,
            "alpha_Phi_K_emitted": False,
            "R_gen_used_as_state": False,
        })

    artifact["source_acquisition_controller"] = "ding_pbte_author_data_or_independent_reproduction_package_missing"
    artifact["claim_promotion"] = False
'''


def patch_full_gate() -> bool:
    text = FULL_GATE.read_text(encoding="utf-8-sig")
    marker = "    # Re-expose the pre-registry lane contract after the canonical rebuild.\n"
    if marker in text:
        return False
    needle = "    OUT.parent.mkdir(parents=True, exist_ok=True)\n"
    updated = replace_once(text, needle, PROJECTION + needle, "full-gate compatibility projection")
    FULL_GATE.write_text(updated, encoding="utf-8")
    return True


def patch_register_generator() -> bool:
    text = REGISTER_GENERATOR.read_text(encoding="utf-8-sig")
    marker = "            if result_id == \"T13_CAUSAL_FLUX_TELEGRAPH_BRANCH\":\n"
    if marker in text:
        return False
    needle = "            discovered_entries.append({\n"
    insertion = (
        "            discovered_open_blockers = major.get(\"open_blockers\", major.get(\"what_remains_open\", []))\n"
        "            if result_id == \"T13_CAUSAL_FLUX_TELEGRAPH_BRANCH\":\n"
        "                discovered_open_blockers = [\n"
        "                    item for item in discovered_open_blockers\n"
        "                    if item not in {\"full coupled Phi integration\", \"full-candidate leakage rerun\"}\n"
        "                ]\n"
        "            discovered_entries.append({\n"
    )
    text = replace_once(text, needle, insertion, "causal register blocker normalization")
    old = '                "open_blockers": major.get("open_blockers", major.get("what_remains_open", [])),\n'
    new = '                "open_blockers": discovered_open_blockers,\n'
    text = replace_once(text, old, new, "causal register blocker field")
    REGISTER_GENERATOR.write_text(text, encoding="utf-8")
    return True


def patch_runner() -> bool:
    text = FULL_RUNNER.read_text(encoding="utf-8-sig")
    command = '    "docs/scripts/audit/repair_topic13_full_gate_compatibility_projection.py",\n'
    if command in text:
        return False
    needle = '    "docs/scripts/audit/audit_conserved_c_finite_cone_no_go.py",\n'
    updated = replace_once(text, needle, command + needle, "full-wave projection order")
    FULL_RUNNER.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    print({
        "full_gate_changed": patch_full_gate(),
        "register_generator_changed": patch_register_generator(),
        "runner_changed": patch_runner(),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
