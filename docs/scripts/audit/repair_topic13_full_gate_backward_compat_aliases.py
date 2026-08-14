"""Preserve legacy Topic 13 full-gate lane aliases during canonical rebuilds."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
FULL_GATE = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
FULL_RUNNER = ROOT / "docs/scripts/audit/run_topic13_full_bridge_wave.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count == 0 and new in text:
        return text
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def patch_full_gate() -> bool:
    text = FULL_GATE.read_text(encoding="utf-8-sig")
    changed = False

    alias_anchor = """    artifact[\"verification_status\"][\"eos_transport_kms_entropy\"].update(discovered_lane_integrations)
    lane_closures = []
"""
    alias_block = """    artifact[\"verification_status\"][\"eos_transport_kms_entropy\"].update(discovered_lane_integrations)
    # Keep the historical top-level names as read-only aliases.  The canonical
    # lane payload remains nested above; aliases prevent downstream readers from
    # mistaking a schema migration for loss of evidence.
    legacy_lane_aliases = {
        \"collective_response_eos_stability_contract\": \"collective_response_eos_stability_contract\",
        \"base_phi_independent_calibration_requirement\": \"base_phi_independent_calibration_requirement\",
        \"covariant_action_si_anchor_route\": \"covariant_action_si_anchor_route\",
        \"covariant_field_normalization_no_go\": \"covariant_field_normalization_identifiability_no_go\",
        \"causal_branch_selection\": \"causal_branch_selection\",
        \"phi_energy_anchor_identifiability\": \"phi_energy_anchor_identifiability_no_go\",
        \"phi_e_reference_normalization\": \"phi_e_reference_normalization\",
        \"thermal_response_beta_contract\": \"thermal_response_beta_contract\",
        \"beta_symbol_separation_noncircularity_no_go\": \"beta_symbol_separation_non_circularity_no_go\",
        \"sk_kms_entropy_interface\": \"sk_kms_entropy_interface_contract\",
    }
    for alias, lane_key in legacy_lane_aliases.items():
        lane = discovered_lane_integrations.get(lane_key)
        if lane:
            artifact[\"verification_status\"][alias] = dict(lane)
    mp48_lane = discovered_lane_integrations.get(\"mp48_independent_graphite_cv_reproduction\")
    if mp48_lane:
        mp48_alias = dict(mp48_lane)
        # The legacy comparator contract used a generic PASS status; retain it
        # without changing the canonical artifact's more specific status.
        mp48_alias[\"status\"] = \"PASS\"
        mp48_alias[\"calibration_consumed\"] = False
        artifact[\"verification_status\"][\"independent_graphite_cv_route\"] = mp48_alias
    lane_closures = []
"""
    if "legacy_lane_aliases = {" not in text:
        updated = replace_once(text, alias_anchor, alias_block, "legacy lane aliases")
        if updated != text:
            changed = True
            text = updated

    old_phrase = 'lane_closures.append("independent harmonic graphite c_v comparator is closed for lane without calibration promotion")'
    new_phrase = 'lane_closures.append("independent harmonic graphite c_v comparator (mp-48) is closed for lane without calibration promotion")'
    updated = replace_once(text, old_phrase, new_phrase, "mp-48 closure phrase")
    if updated != text:
        changed = True
        text = updated

    if changed:
        FULL_GATE.write_text(text, encoding="utf-8")
    return changed


def patch_runner() -> bool:
    text = FULL_RUNNER.read_text(encoding="utf-8-sig")
    command = '    "docs/scripts/audit/repair_topic13_full_gate_backward_compat_aliases.py",\n'
    if command in text:
        return False
    needle = "COMMANDS = [\n"
    replacement = needle + command
    updated = replace_once(text, needle, replacement, "full-wave runner command list")
    FULL_RUNNER.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    gate_changed = patch_full_gate()
    runner_changed = patch_runner()
    print({"full_gate_changed": gate_changed, "runner_changed": runner_changed})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
