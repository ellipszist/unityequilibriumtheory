"""Keep the formal bridge wave runner's generated hash links reproducible."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/run_topic13_formal_bridge_boundary_wave.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    marker = '    "docs/scripts/audit/audit_major_result_dependency_unlock.py",\n'
    additions = (
        '    "docs/scripts/audit/sync_uet_wave1_foundation_hash_cycle.py",\n'
        '    "docs/scripts/audit/repair_wave1_major_result_hash_cycle.py",\n'
    )
    if additions.strip() in text:
        print("FORMAL_BRIDGE_WAVE_HASH_ORDER_ALREADY_PRESENT")
        return 0
    if text.count(marker) != 1:
        raise SystemExit(f"formal bridge wave dependency marker count: {text.count(marker)}")
    TARGET.write_text(text.replace(marker, marker + additions, 1), encoding="utf-8")
    print("ADDED_FORMAL_BRIDGE_WAVE_HASH_ORDER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
