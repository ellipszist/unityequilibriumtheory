"""Preserve source-level blockers in the Topic 13 full-result report."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
RUNNER = ROOT / "docs/scripts/audit/run_topic13_full_bridge_wave.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    marker = "    source_level_blockers = {\n"
    if marker in text:
        print("FULL_GATE_SUBRESULT_BLOCKERS_ALREADY_PRESENT")
        return 0
    needle = "    artifact[\"major_result\"][\"what_remains_open\"] = list(dict.fromkeys([\n"
    insertion = (
        "    source_level_blockers = {\n"
        "        \"independent_same_grade_density_or_direct_volumetric_heat_capacity_missing\",\n"
        "        \"same_grade_alpha_V_and_K_T_missing\",\n"
        "        \"material_regime_mapping_to_TTG_not_closed\",\n"
        "    }\n"
        "    artifact[\"major_result\"][\"what_remains_open\"] = list(dict.fromkeys([\n"
    )
    if text.count(needle) != 1:
        raise SystemExit(f"full-gate blocker report anchor: expected one match, found {text.count(needle)}")
    TARGET.write_text(text.replace(needle, insertion, 1), encoding="utf-8")

    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    command = '    "docs/scripts/audit/repair_topic13_full_gate_preserve_subresult_blockers.py",\n'
    if command not in runner_text:
        runner_needle = '    "docs/scripts/audit/repair_topic13_full_gate_final_compatibility_fields.py",\n'
        if runner_text.count(runner_needle) != 1:
            raise SystemExit("runner final repair anchor not found")
        RUNNER.write_text(runner_text.replace(runner_needle, runner_needle + command, 1), encoding="utf-8")
    print("ADDED_FULL_GATE_SUBRESULT_BLOCKERS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
