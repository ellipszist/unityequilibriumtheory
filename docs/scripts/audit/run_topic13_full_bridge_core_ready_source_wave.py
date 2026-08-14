"""Run Topic 13 through causal, source, alpha, and bridge controllers."""

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
    coupled_wave = run("run_topic13_full_bridge_core_ready_coupled_wave.py")
    if coupled_wave != 0:
        return coupled_wave

    source_audit = run("audit_ding_2022_source_mapping.py")
    alpha_audit = run("audit_topic13_alpha_phi_k_identifiability.py")
    if source_audit != 0 or alpha_audit != 0:
        return source_audit or alpha_audit

    for relative in (
        "audit_thermal_source_observable_mapping.py",
        "audit_thermal_source_provenance.py",
        "audit_uet_main_theory_dimensional_observable.py",
        "audit_topic13_dimensional_bridge_contract.py",
        "audit_topic13_gatech_graphite_source.py",
        "audit_topic13_cp_cv_correction.py",
        "audit_topic13_energy_response_bridge.py",
        "sync_topic13_gatech_source_into_energy_bridge.py",
        "sync_topic13_cp_cv_correction_into_energy_bridge.py",
        "sync_topic13_source_package_hash.py",
        "sync_topic13_ding_source_mapping_gate.py",
        "sync_topic13_alpha_identifiability_gate.py",
        "sync_topic13_dimensional_bridge_gate.py",
        "sync_topic13_energy_response_gate.py",
        "sync_topic13_gatech_source_gate.py",
        "sync_topic13_cp_cv_correction_gate.py",
        "audit_major_result_closure.py",
        "sync_topic13_flux_branch_register.py",
        "sync_topic13_flux_phi_coupled_register.py",
        "sync_topic13_alpha_identifiability_register.py",
        "sync_topic13_dimensional_bridge_register.py",
        "sync_topic13_energy_response_register.py",
        "sync_topic13_gatech_source_register.py",
        "sync_topic13_cp_cv_correction_register.py",
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
