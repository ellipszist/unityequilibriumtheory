"""Run and integrate the fixed-background Gaussian finite-temperature lane."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def run(script: str) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "docs/scripts/audit" / script)],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    run("audit_topic13_uet_o2_condensate_gaussian_thermal.py")
    run("repair_topic13_gaussian_thermal_lane_key.py")
    run("repair_topic13_gaussian_thermal_sync_syntax.py")
    run("repair_topic13_gaussian_thermal_formula_literal.py")
    run("audit_topic13_full_bridge_gate.py")
    run("sync_topic13_uet_o2_condensate_gaussian_thermal.py")
    run("audit_major_result_dependency_unlock.py")
    print("PASS_TOPIC13_UET_O2_CONDENSATE_GAUSSIAN_FINITE_T_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
