"""Add the Berut source-boundary artifact to the full Topic 13 lane map."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
NEEDLE = "'T13_UET_O2_NORMAL_THERMODYNAMIC_CONSISTENCY': 'uet_o2_normal_thermodynamic_consistency'"
REPLACEMENT = (
    "'T13_UET_O2_NORMAL_THERMODYNAMIC_CONSISTENCY': 'uet_o2_normal_thermodynamic_consistency', "
    "'T13_BERUT_SOURCE_PACKAGE_AVAILABILITY_BOUNDARY': 'berut_source_package_availability_boundary'"
)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    if "'T13_BERUT_SOURCE_PACKAGE_AVAILABILITY_BOUNDARY'" not in text:
        if NEEDLE not in text:
            raise SystemExit("full gate lane-map anchor not found")
        text = text.replace(NEEDLE, REPLACEMENT, 1)
        TARGET.write_text(text, encoding="utf-8")
        print("PATCHED_BERUT_SOURCE_LANE_KEY")
    else:
        print("BERUT_SOURCE_LANE_KEY_ALREADY_PRESENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
