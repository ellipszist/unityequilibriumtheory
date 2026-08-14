"""Repair the final Topic 13 legacy field mappings in the canonical generator."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
FULL_GATE = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
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


def patch_generator() -> bool:
    text = FULL_GATE.read_text(encoding="utf-8-sig")
    original = text

    old = "'T13_CAUSAL_BRANCH_SELECTION': 'causal_branch_selection',"
    new = old + " 'T13_CAUSAL_THERMAL_BRANCH_SELECTION': 'causal_branch_selection',"
    if "'T13_CAUSAL_THERMAL_BRANCH_SELECTION': 'causal_branch_selection'" not in text:
        text = replace_once(text, old, new, "causal thermal branch result mapping")

    old = (
        '        named_branch["source_independence_no_go"] = compatibility_lane(\n'
        '            "gatech_volumetric_cp_independence_no_go"\n'
        "        )\n"
        '        alpha["named_energy_response_branch"] = named_branch\n'
    )
    new = (
        '        source_independence = compatibility_lane(\n'
        '            "gatech_volumetric_cp_independence_no_go"\n'
        "        )\n"
        "        if source_independence:\n"
        '            source_independence["same_workbook_density_inversion_allowed"] = False\n'
        '            source_independence["same_workbook_volumetric_cp_inversion_allowed"] = False\n'
        '        named_branch["source_independence_no_go"] = source_independence\n'
        '        alpha["named_energy_response_branch"] = named_branch\n'
    )
    if old in text and new not in text:
        text = replace_once(text, old, new, "source-independence legacy fields")

    if text != original:
        FULL_GATE.write_text(text, encoding="utf-8")
    return text != original


def patch_runner() -> bool:
    text = FULL_RUNNER.read_text(encoding="utf-8-sig")
    command = '    "docs/scripts/audit/repair_topic13_full_gate_final_compatibility_fields.py",\n'
    if command in text:
        return False
    needle = '    "docs/scripts/audit/repair_topic13_full_gate_compatibility_projection.py",\n'
    updated = replace_once(text, needle, command + needle, "final compatibility repair order")
    FULL_RUNNER.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    print({"generator_changed": patch_generator(), "runner_changed": patch_runner()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
