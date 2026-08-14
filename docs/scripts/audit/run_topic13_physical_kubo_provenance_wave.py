"""Run the Topic 13 physical Kubo provenance gate wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT_DIR = ROOT / "docs/scripts/audit"


def run(relative: str) -> int:
    completed = subprocess.run([sys.executable, str(AUDIT_DIR / relative)], cwd=ROOT, check=False)
    return completed.returncode


def main() -> int:
    for relative in (
        "audit_topic13_physical_kubo_coefficient_provenance.py",
        "sync_topic13_physical_kubo_coefficient_provenance.py",
    ):
        result = run(relative)
        if result != 0:
            return result
    print("PASS_TOPIC13_PHYSICAL_KUBO_PROVENANCE_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
