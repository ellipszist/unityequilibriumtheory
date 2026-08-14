"""Normalize NumPy boolean checks before JSON serialization."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_uet_o2_condensate_goldstone_ideal_lane.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = '    status = "PASS_T0_CONDENSATE_GOLDSTONE_IDEAL_LANE" if all(checks.values()) else "FAIL_T0_CONDENSATE_GOLDSTONE_IDEAL_LANE"\n'
    new = '    checks = {key: bool(value) for key, value in checks.items()}\n    status = "PASS_T0_CONDENSATE_GOLDSTONE_IDEAL_LANE" if all(checks.values()) else "FAIL_T0_CONDENSATE_GOLDSTONE_IDEAL_LANE"\n'
    if old not in text:
        raise SystemExit("expected status line was not found")
    TARGET.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("REPAIRED_TOPIC13_UET_O2_CONDENSATE_GOLDSTONE_JSON_CHECKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
