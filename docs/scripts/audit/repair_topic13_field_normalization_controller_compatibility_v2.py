"""Repair the variable-based controller assignment in the field-normalization sync."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SYNC = ROOT / "docs/scripts/audit/sync_topic13_covariant_field_normalization_into_gates.py"
FULL = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/topic13_full_thermodynamic_bridge_core_ready_gate.json"
UMBRELLA = "dimensional_phi_energy_anchor_or_independent_alpha_calibration_missing"
DETAIL = "physical_field_normalization_observable_and_SI_coefficient_provenance_or_independent_alpha_calibration_missing"


def main() -> int:
    source = SYNC.read_text(encoding="utf-8-sig")
    old_controller = f'controller = "{DETAIL}"'
    new_controller = f'controller = "{UMBRELLA}"\n    controller_detail = "{DETAIL}"'
    if old_controller in source:
        source = source.replace(old_controller, new_controller)
    elif new_controller not in source:
        raise SystemExit("expected field-normalization controller variable was not found")
    old_assignment = 'full["controlling_blocker"] = controller\n'
    new_assignment = 'full["controlling_blocker"] = controller\n    full["controlling_blocker_detail"] = controller_detail\n'
    if old_assignment in source and new_assignment not in source:
        source = source.replace(old_assignment, new_assignment)
    elif new_assignment not in source:
        raise SystemExit("expected full-gate controller assignment was not found")
    SYNC.write_text(source, encoding="utf-8")

    gate = json.loads(FULL.read_text(encoding="utf-8-sig"))
    gate["controlling_blocker"] = UMBRELLA
    gate["controlling_blocker_detail"] = DETAIL
    FULL.write_text(json.dumps(gate, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print("PASS_REPAIRED_T13_FIELD_NORMALIZATION_CONTROLLER_COMPATIBILITY_V2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
