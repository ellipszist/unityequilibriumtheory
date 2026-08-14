from pathlib import Path


path = Path("docs/scripts/audit/audit_topic13_full_bridge_gate.py")
text = path.read_text(encoding="utf-8")
old = '''    source_level_blockers = {
        "independent_same_grade_density_or_direct_volumetric_heat_capacity_missing",
        "same_grade_alpha_V_and_K_T_missing",
        "material_regime_mapping_to_TTG_not_closed",
        "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing",
    }
    # Keep the major-result projection readable: only the full-gate
    # controllers belong here. Lane-specific open inputs remain nested in
    # verification_status and evidence artifacts.
    artifact["major_result"]["what_remains_open"] = list(dict.fromkeys(blockers))
'''
new = '''    source_level_blockers = {
        "independent_same_grade_density_or_direct_volumetric_heat_capacity_missing",
        "same_grade_alpha_V_and_K_T_missing",
        "material_regime_mapping_to_TTG_not_closed",
        "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing",
    }
    source_independence_lane = discovered_lane_integrations.get(
        "gatech_volumetric_cp_independence_no_go", {}
    )
    # Preserve unresolved source-dependency blockers in the major-result
    # projection. A scoped no-go closes the circular route, but does not close
    # the independent source requirement that the no-go exposes.
    for blocker in source_independence_lane.get("open_blockers", []):
        if blocker in source_level_blockers:
            blockers.append(blocker)
    # Keep the major-result projection readable: only the full-gate
    # controllers and explicit source prerequisites belong here. Lane-specific
    # diagnostics remain nested in verification_status and evidence artifacts.
    artifact["major_result"]["what_remains_open"] = list(dict.fromkeys(blockers))
'''
if text.count(old) != 1:
    raise SystemExit(f"expected one source blocker projection, found {text.count(old)}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("restored explicit source-dependency blockers in the Topic 13 major-result projection")
