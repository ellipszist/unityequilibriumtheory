"""Run the complete Topic 13 closure wave and downstream dependency checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
COMMANDS = [
    "docs/scripts/audit/run_topic13_full_bridge_wave.py",
    "docs/scripts/audit/sync_uet_wave1_foundation_hash_cycle.py",
    "docs/scripts/audit/repair_wave1_major_result_hash_cycle.py",
    "docs/scripts/audit/audit_uet_research_room_wave1.py",
    "docs/scripts/audit/audit_uet_research_room_wave1_integrity.py",
    "docs/scripts/audit/audit_major_result_dependency_unlock.py",
]


def main() -> int:
    for relative in COMMANDS:
        completed = subprocess.run(
            [sys.executable, str(ROOT / relative)],
            cwd=ROOT,
            check=False,
        )
        if completed.returncode != 0:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
