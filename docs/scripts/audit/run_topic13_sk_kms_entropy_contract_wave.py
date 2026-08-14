"""Run the formal Topic 13 SK/KMS/entropy contract wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT_DIR = ROOT / "docs/scripts/audit"


def main() -> int:
    for relative in (
        "audit_topic13_sk_kms_entropy_contract.py",
        "sync_topic13_sk_kms_entropy_contract.py",
    ):
        completed = subprocess.run(
            [sys.executable, str(AUDIT_DIR / relative)],
            cwd=ROOT,
            check=False,
        )
        if completed.returncode != 0:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
