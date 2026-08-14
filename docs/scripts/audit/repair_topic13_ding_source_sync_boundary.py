"""Keep Ding figure-derived readiness separate from Full Topic 13 readiness."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/sync_topic13_ding_source_mapping_gate.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"repair anchor not found: {label}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = "\n".join(
        [
            '    source["source_ready_for_full_closure"] = source_ready',
            '    source["provisional_source_present"] = True',
            '    source["raw_author_numeric_source_present"] = bool(',
            '        audit["checks"].get("raw_author_numeric_source_present")',
            "    )",
            "",
        ]
    )
    new = "\n".join(
        [
            '    raw_author_numeric_source_present = bool(',
            '        audit["checks"].get("raw_author_numeric_source_present")',
            "    )",
            "    # A permitted figure route is usable for normalized comparison,",
            "    # but it is not the raw author numeric package required by the",
            "    # Full Topic 13 source gate.",
            '    source["figure_derived_numeric_route_ready"] = source_ready',
            '    source["source_ready_for_full_closure"] = raw_author_numeric_source_present',
            '    source["provisional_source_present"] = True',
            '    source["raw_author_numeric_source_present"] = raw_author_numeric_source_present',
            "",
        ]
    )
    text = replace_once(text, old, new, "source readiness split")

    old = "\n".join(
        [
            "    if source_ready:",
            "        closed_source_result = (",
            '            "permitted Ding 2022 figure-derived normalized source with closed printed-legend mapping"',
            "        )",
            '        closed = gate["major_result"].setdefault("what_is_closed", [])',
            "        if closed_source_result not in closed:",
            "            closed.append(closed_source_result)",
            '        blocker = remains[0] if remains else "alpha_Phi_K_independent_calibration_missing"',
            '        gate["next_action"] = (',
            '            "Derive alpha_Phi_K from the declared bridge or create an independent calibration "',
            '            "record using training/calibration data only; do not read or tune on Xie 2026."',
            "        )",
            "    else:",
        ]
    )
    new = "\n".join(
        [
            "    if source_ready:",
            "        closed_source_result = (",
            '            "permitted Ding 2022 figure-derived normalized source with closed printed-legend mapping"',
            "        )",
            '        closed = gate["major_result"].setdefault("what_is_closed", [])',
            "        if closed_source_result not in closed:",
            "            closed.append(closed_source_result)",
            '        provisional_blocker = "ttg_numeric_source_package_is_provisional"',
            "        if provisional_blocker not in remains:",
            "            remains.insert(0, provisional_blocker)",
            "        blocker = provisional_blocker",
            '        gate["next_action"] = (',
            '            "Acquire a permitted raw-author or independently reproduced numeric TTG package with "',
            '            "units and uncertainty, then derive alpha_Phi_K or create an independent calibration "',
            '            "record using training/calibration data only; do not read or tune on Xie 2026."',
            "        )",
            "    else:",
        ]
    )
    text = replace_once(text, old, new, "provisional blocker preservation")
    TARGET.write_text(text, encoding="utf-8")
    print("PASS_REPAIRED_TOPIC13_DING_SOURCE_SYNC_BOUNDARY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
