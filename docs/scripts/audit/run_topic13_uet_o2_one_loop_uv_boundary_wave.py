"""Run and integrate the thermal one-loop UV-boundary wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "docs/scripts/audit" / script)], cwd=ROOT, check=True)


def main() -> int:
    run("audit_topic13_uet_o2_one_loop_uv_boundary.py")
    run("sync_topic13_uet_o2_one_loop_uv_boundary.py")
    print("PASS_TOPIC13_UET_O2_ONE_LOOP_UV_BOUNDARY_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
