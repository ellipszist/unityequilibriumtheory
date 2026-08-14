"""Preserve lane-specific integration details during full-gate discovery."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = (
        "    # Current source artifacts must override stale records from an older gate.\n"
        "    artifact[\"verification_status\"][\"eos_transport_kms_entropy\"].update(discovered_lane_integrations)\n"
    )
    new = (
        "    # Current source artifacts override stale fields, while lane-specific\n"
        "    # details emitted by a sync pass (for example fixed-background flags) are\n"
        "    # retained until the corresponding lane is synchronized again.\n"
        "    merged_lane_integrations = {}\n"
        "    for lane_key, discovered in discovered_lane_integrations.items():\n"
        "        previous = preserved_lane_integrations.get(lane_key, {})\n"
        "        merged = dict(previous) if isinstance(previous, dict) else {}\n"
        "        merged.update(discovered)\n"
        "        merged_lane_integrations[lane_key] = merged\n"
        "    artifact[\"verification_status\"][\"eos_transport_kms_entropy\"].update(merged_lane_integrations)\n"
    )
    if new not in text:
        if old not in text:
            raise SystemExit("lane discovery update anchor not found")
        text = text.replace(old, new, 1)
        TARGET.write_text(text, encoding="utf-8")
    print("PASS_REPAIRED_TOPIC13_FULL_GATE_LANE_DETAIL_MERGE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
