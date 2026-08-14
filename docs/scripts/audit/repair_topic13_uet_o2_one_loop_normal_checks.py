"""Repair false-positive admission checks for the one-loop normal audit."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "docs/scripts/audit/audit_topic13_uet_o2_one_loop_normal_branch.py"


def main() -> int:
    text = AUDIT.read_text(encoding="utf-8")
    old = '''"kubo_is_not_emitted": "Kubo" not in json.dumps(contract),'''
    new = '''"kubo_is_not_emitted": (
            "Kubo" not in json.dumps(contract)
            and "kubo" not in json.dumps(contract)
            and "physical_Kubo_coefficient" not in json.dumps(contract)
        ),'''
    if old not in text:
        raise SystemExit("one-loop Kubo check not found")
    AUDIT.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("PATCHED_T13_UET_O2_ONE_LOOP_NORMAL_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
