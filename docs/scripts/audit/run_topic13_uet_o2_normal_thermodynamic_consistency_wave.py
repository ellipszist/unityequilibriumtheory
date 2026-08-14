"""Run and integrate the normal-lane thermodynamic-consistency wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT_DIR = ROOT / "docs/scripts/audit"


def run(relative: str) -> int:
    completed = subprocess.run(
        [sys.executable, str(AUDIT_DIR / relative)],
        cwd=ROOT,
        check=False,
    )
    return completed.returncode


def main() -> int:
    for relative in (
        "audit_topic13_uet_o2_normal_thermodynamic_consistency.py",
        "repair_topic13_normal_thermodynamic_consistency_lane_key.py",
        "audit_topic13_full_bridge_gate.py",
        "sync_topic13_uet_o2_normal_thermodynamic_consistency.py",
        "audit_major_result_dependency_unlock.py",
    ):
        result = run(relative)
        if result != 0:
            return result
    print("PASS_TOPIC13_UET_O2_NORMAL_THERMODYNAMIC_CONSISTENCY_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
