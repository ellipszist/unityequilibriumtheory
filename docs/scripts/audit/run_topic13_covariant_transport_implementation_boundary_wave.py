"""Run and integrate the Topic 13 covariant transport boundary wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "docs/scripts/audit" / script)], cwd=ROOT, check=True)


def main() -> int:
    run("audit_topic13_covariant_transport_implementation_boundary.py")
    run("sync_topic13_covariant_transport_implementation_boundary.py")
    print("PASS_TOPIC13_COVARIANT_TRANSPORT_IMPLEMENTATION_BOUNDARY_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
