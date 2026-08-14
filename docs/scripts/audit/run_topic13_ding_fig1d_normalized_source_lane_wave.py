"""Run and integrate the bounded Ding Fig. 1d normalized-source lane."""

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
        "audit_ding_2022_source_mapping.py",
        "audit_topic13_ding_fig1d_normalized_source_lane.py",
        "audit_topic13_full_bridge_gate.py",
        "sync_topic13_no_go_gate.py",
        "audit_major_result_closure.py",
        "sync_major_result_wave1_contract.py",
        "sync_uet_wave1_foundation_hash_cycle.py",
        "repair_wave1_major_result_hash_cycle.py",
        "audit_uet_research_room_wave1.py",
        "audit_major_result_dependency_unlock.py",
        "audit_uet_research_room_wave1_integrity.py",
    ):
        result = run(relative)
        if result != 0:
            return result
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
