"""Run and integrate the one-loop normal branch convergence wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "docs/scripts/audit" / script)], cwd=ROOT, check=True)


def main() -> int:
    run("audit_topic13_uet_o2_one_loop_convergence.py")
    run("sync_topic13_uet_o2_one_loop_convergence.py")
    print("PASS_TOPIC13_UET_O2_ONE_LOOP_CONVERGENCE_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
