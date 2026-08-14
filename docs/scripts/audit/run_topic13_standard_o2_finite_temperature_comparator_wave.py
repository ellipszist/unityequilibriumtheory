"""Run and integrate the standard finite-temperature O(2) comparator wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "docs/scripts/audit" / script)], cwd=ROOT, check=True)


def main() -> int:
    run("audit_topic13_standard_o2_finite_temperature_comparator.py")
    run("sync_topic13_standard_o2_finite_temperature_comparator.py")
    print("PASS_TOPIC13_STANDARD_O2_FINITE_TEMPERATURE_COMPARATOR_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
