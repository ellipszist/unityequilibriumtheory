"""Run the Topic 13 wave through the named coupled C/Phi lane."""

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
    initial_wave = run("run_topic13_full_bridge_core_ready_flux_wave.py")
    if initial_wave != 0:
        return initial_wave

    coupled_audit = run("audit_matter_space_flux_phi_coupled.py")
    # Always sync the artifact, including a BLOCKED result, so the gate never
    # falls back to stale prose when this controller is not passing.
    for relative in (
        "sync_topic13_flux_phi_coupled_gate.py",
        "audit_major_result_closure.py",
        "sync_topic13_flux_phi_coupled_register.py",
        "sync_uet_wave1_foundation_hash_cycle.py",
        "repair_wave1_major_result_hash_cycle.py",
        "audit_uet_research_room_wave1.py",
        "audit_uet_research_room_wave1_integrity.py",
        "audit_major_result_dependency_unlock.py",
    ):
        result = run(relative)
        if result != 0:
            return result
    return coupled_audit


if __name__ == "__main__":
    raise SystemExit(main())
