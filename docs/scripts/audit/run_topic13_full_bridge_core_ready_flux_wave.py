"""Run the Topic 13 wave including the named conserved flux branch."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
COMMANDS = [
    "run_topic13_full_bridge_wave.py",
    "sync_topic13_source_package_hash.py",
    "audit_matter_space_conserved_flux_telegraph.py",
    "sync_topic13_flux_branch_gate.py",
    "audit_major_result_closure.py",
    "sync_topic13_flux_branch_register.py",
    "sync_uet_wave1_foundation_hash_cycle.py",
    "repair_wave1_major_result_hash_cycle.py",
    "audit_uet_research_room_wave1.py",
    "audit_uet_research_room_wave1_integrity.py",
    "audit_major_result_dependency_unlock.py",
]


def main() -> int:
    for relative in COMMANDS:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "docs/scripts/audit" / relative)],
            cwd=ROOT,
            check=False,
        )
        if completed.returncode != 0:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
