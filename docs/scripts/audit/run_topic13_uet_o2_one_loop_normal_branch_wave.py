"""Run and integrate the action-derived O(2) one-loop normal branch wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "docs/scripts/audit" / script)], cwd=ROOT, check=True)


def main() -> int:
    run("audit_topic13_uet_o2_one_loop_normal_branch.py")
    run("sync_topic13_uet_o2_one_loop_normal_branch.py")
    print("PASS_TOPIC13_UET_O2_ONE_LOOP_NORMAL_BRANCH_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
