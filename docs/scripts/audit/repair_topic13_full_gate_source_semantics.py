from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "    source_ready = normalized_source_ready\n",
        "    # A figure-derived normalized route is sufficient for the comparison\n    # lane, but full Topic 13 still requires raw-author C_src or an\n    # accepted independent reproduction package.\n    source_ready = raw_author_source_ready\n",
        "full source readiness",
    )
    text = replace_once(
        text,
        '            "controlling_blocker": None if source_ready else "ttg_numeric_source_package_is_provisional",\n',
        '            "controlling_blocker": None if source_ready else "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing",\n',
        "source blocker",
    )
    text = replace_once(
        text,
        '    source_level_blockers = {\n        "independent_same_grade_density_or_direct_volumetric_heat_capacity_missing",\n        "same_grade_alpha_V_and_K_T_missing",\n        "material_regime_mapping_to_TTG_not_closed",\n    }\n',
        '    source_level_blockers = {\n        "independent_same_grade_density_or_direct_volumetric_heat_capacity_missing",\n        "same_grade_alpha_V_and_K_T_missing",\n        "material_regime_mapping_to_TTG_not_closed",\n        "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing",\n    }\n',
        "source blocker projection compatibility",
    )
    TARGET.write_text(text, encoding="utf-8")
    print("patched", TARGET)


if __name__ == "__main__":
    main()
