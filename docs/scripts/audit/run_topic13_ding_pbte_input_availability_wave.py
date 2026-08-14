"""Run Topic 13 through the Ding PMC OA numeric-input availability wave."""

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
    base_wave = run("run_topic13_ding_pbte_mapping_wave.py")
    if base_wave != 0:
        return base_wave

    for relative in (
        "audit_topic13_ding_pbte_numeric_input_availability.py",
        "sync_topic13_ding_pbte_input_availability_into_energy_bridge.py",
        "sync_topic13_ding_pbte_input_availability_gate.py",
        "audit_major_result_closure.py",
        "sync_topic13_flux_branch_register.py",
        "sync_topic13_flux_phi_coupled_register.py",
        "sync_topic13_alpha_identifiability_register.py",
        "sync_topic13_dimensional_bridge_register.py",
        "sync_topic13_energy_response_register.py",
        "sync_topic13_ding_pbte_mapping_register.py",
        "sync_topic13_ding_pbte_input_availability_register.py",
        "sync_topic13_gatech_source_register.py",
        "sync_topic13_cp_cv_correction_register.py",
        "sync_topic13_gatech_volumetric_cp_no_go_register.py",
        "sync_uet_wave1_foundation_hash_cycle.py",
        "repair_wave1_major_result_hash_cycle.py",
        "audit_uet_research_room_wave1.py",
        "audit_uet_research_room_wave1_integrity.py",
        "audit_major_result_dependency_unlock.py",
    ):
        result = run(relative)
        if result != 0:
            return result
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
