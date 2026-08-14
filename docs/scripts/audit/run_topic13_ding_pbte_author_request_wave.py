"""Run the bounded Ding PBTE author-request integration wave."""

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
    for relative in (
        "audit_topic13_ding_pbte_author_request.py",
        "sync_topic13_ding_pbte_author_request.py",
    ):
        result = run(relative)
        if result != 0:
            return result
    print("PASS_TOPIC13_DING_PBTE_AUTHOR_REQUEST_WAVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
