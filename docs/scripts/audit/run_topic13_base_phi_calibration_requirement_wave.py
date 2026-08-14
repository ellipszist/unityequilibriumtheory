"""Run the Topic 13 base-Phi calibration-boundary hardening wave."""

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
    result = run("audit_topic13_base_phi_independent_calibration_requirement.py")
    if result != 0:
        return result
    return run("sync_topic13_base_phi_independent_calibration_requirement.py")


if __name__ == "__main__":
    raise SystemExit(main())
