"""Repair stale formal-boundary reporting in the Topic 13 full gate."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count == 0:
        if new in text:
            return text
        raise SystemExit(f"missing {label} block")
    if count != 1:
        raise SystemExit(f"ambiguous {label} block: {count}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = """        \"non_circular_bridge\": {
            \"status\": \"PASS\" if bridge_derived else \"BLOCKED\",
            \"constraint_gate_status\": constraint_gates.get(\"uet_bridge_derivation_gate\", {}).get(\"status\"),
            \"landauer_non_derivation_gate\": constraint_gates.get(\"landauer_coefficient_non_derivation_gate\", {}).get(\"status\"),
            \"controlling_blocker\": \"non_circular_uet_bridge_and_beta_derivation_missing\" if not bridge_derived else None,
        },
"""
    new = """        \"non_circular_bridge\": {
            # Formal boundary closure does not imply physical bridge closure.
            \"status\": \"PASS\" if bridge_derived else \"BLOCKED\",
            \"constraint_gate_status\": constraint_gates.get(\"uet_bridge_derivation_gate\", {}).get(\"status\"),
            \"landauer_non_derivation_gate\": constraint_gates.get(\"landauer_coefficient_non_derivation_gate\", {}).get(\"status\"),
            \"formal_boundary_status\": discovered_lane_integrations.get(\"formal_non_circular_bridge_boundary\", {}).get(\"status\", \"OPEN\"),
            \"formal_boundary_closure_level\": discovered_lane_integrations.get(\"formal_non_circular_bridge_boundary\", {}).get(\"closure_level\", \"OPEN\"),
            \"formal_boundary_audit\": discovered_lane_integrations.get(\"formal_non_circular_bridge_boundary\", {}).get(\"audit\"),
            \"physical_derivation_status\": \"PASS\" if bridge_derived else \"BLOCKED\",
            \"physical_derivation_controlling_blocker\": \"non_circular_uet_bridge_and_beta_derivation_missing\" if not bridge_derived else None,
            \"controlling_blocker\": \"non_circular_uet_bridge_and_beta_derivation_missing\" if not bridge_derived else None,
        },
"""
    text = replace_once(text, old, new, "non-circular bridge")

    old = '        "next_action": "Close the causal branch/no-go record, independent alpha_Phi_K, source rows, non-circular bridge, and EOS/transport/KMS/entropy gates in order.",\n'
    new = '        "next_action": "Acquire an independent base-Phi SI energy/observable anchor or paired Phi/SI record; obtain Ding numeric C_src(T) or an accepted independent reproduction; source-lock beta_T13 and one state-matched physical Kubo coefficient; then complete EOS/transport/KMS/entropy gates. The original conserved-C question is closed only as a scoped no-go and remains blocked as the original baseline.",\n'
    text = replace_once(text, old, new, "next action")

    old = """    artifact[\"verification_status\"][\"eos_transport_kms_entropy\"].update(preserved_lane_integrations)
    # Current source artifacts must override stale records from an older gate.
    artifact[\"verification_status\"][\"eos_transport_kms_entropy\"].update(discovered_lane_integrations)
    artifact[\"major_result\"][\"what_is_closed\"] = list(dict.fromkeys([
        *artifact[\"major_result\"].get(\"what_is_closed\", []),
        *previous_major.get(\"what_is_closed\", []),
    ]))
"""
    new = """    artifact[\"verification_status\"][\"eos_transport_kms_entropy\"].update(preserved_lane_integrations)
    # Current source artifacts must override stale records from an older gate.
    artifact[\"verification_status\"][\"eos_transport_kms_entropy\"].update(discovered_lane_integrations)
    lane_closures = []
    if discovered_lane_integrations.get(\"formal_non_circular_bridge_boundary\", {}).get(\"closure_level\") == \"CLOSED_FOR_LANE\":
        lane_closures.append(\"formal non-circular bridge boundary is closed for lane; physical beta, base-Phi SI anchor, and transport provenance remain open\")
    if discovered_lane_integrations.get(\"mp48_independent_graphite_cv_reproduction\", {}).get(\"closure_level\") == \"CLOSED_FOR_LANE\":
        lane_closures.append(\"independent harmonic graphite c_v comparator is closed for lane without calibration promotion\")
    if discovered_lane_integrations.get(\"ding_fig1d_normalized_source_lane\", {}).get(\"closure_level\") == \"CLOSED_FOR_LANE\":
        lane_closures.append(\"permitted Ding Fig. 1d normalized-source lane is closed for lane without raw-author or alpha claims\")
    artifact[\"major_result\"][\"what_is_closed\"] = list(dict.fromkeys([
        *artifact[\"major_result\"].get(\"what_is_closed\", []),
        *lane_closures,
        *previous_major.get(\"what_is_closed\", []),
    ]))
"""
    text = replace_once(text, old, new, "closure reporting")
    TARGET.write_text(text, encoding="utf-8")
    print("REPAIRED_FULL_GATE_FORMAL_BOUNDARY_REPORTING_V2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
