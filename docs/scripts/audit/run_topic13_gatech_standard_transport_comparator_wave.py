"""Run and integrate the bounded Topic 13 standard comparator wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "docs/scripts/audit" / script)], cwd=ROOT, check=True)


def main() -> int:
    run("audit_topic13_gatech_standard_transport_comparator.py")
    run("sync_topic13_gatech_standard_transport_comparator.py")
    print("PASS_TOPIC13_GATECH_STANDARD_TRANSPORT_COMPARATOR_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
