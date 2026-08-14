"""Repair the bounded Ding lane runner so linked Wave 1 hashes refresh first."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/run_topic13_ding_fig1d_normalized_source_lane_wave.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = (
        '        "sync_major_result_wave1_contract.py",\n'
        '        "audit_major_result_dependency_unlock.py",\n'
        '        "audit_uet_research_room_wave1_integrity.py",\n'
    )
    new = (
        '        "sync_major_result_wave1_contract.py",\n'
        '        "sync_uet_wave1_foundation_hash_cycle.py",\n'
        '        "repair_wave1_major_result_hash_cycle.py",\n'
        '        "audit_uet_research_room_wave1.py",\n'
        '        "audit_major_result_dependency_unlock.py",\n'
        '        "audit_uet_research_room_wave1_integrity.py",\n'
    )
    if old not in text:
        if new in text:
            print("DING_LANE_WAVE_HASH_ORDER_ALREADY_PRESENT")
            return 0
        raise SystemExit("Ding lane runner command order not found")
    TARGET.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("REPAIRED_DING_LANE_WAVE_HASH_ORDER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
