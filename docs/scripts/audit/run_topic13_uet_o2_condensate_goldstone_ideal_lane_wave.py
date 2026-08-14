"""Run and integrate the T=0 condensate/Goldstone ideal-lane wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "docs/scripts/audit" / script)], cwd=ROOT, check=True)


def main() -> int:
    run("audit_topic13_uet_o2_condensate_goldstone_ideal_lane.py")
    run("sync_topic13_uet_o2_condensate_goldstone_ideal_lane.py")
    print("PASS_TOPIC13_UET_O2_CONDENSATE_GOLDSTONE_IDEAL_LANE_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
