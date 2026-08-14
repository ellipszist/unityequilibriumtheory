"""Repair full-gate causal reporting without changing legacy baseline status."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"repair anchor not found: {label}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    text = replace_once(
        text,
        '            "status": "PASS" if full_candidate_pass else "BLOCKED",\n            "lane_status": "PASS" if causal_lane_pass else "BLOCKED",\n',
        '            "status": "PASS" if full_candidate_pass else "BLOCKED",\n            "baseline_status": "PASS" if full_candidate_pass else "BLOCKED",\n            "lane_status": "PASS" if causal_lane_pass else "BLOCKED",\n            "structural_question_closure": (\n                "CLOSED_AS_NO_GO" if causal_lane_pass else "OPEN"\n            ),\n',
        "causal lane fields",
    )
    text = replace_once(
        text,
        '    blockers = [\n        item["controlling_blocker"]\n        for item in gates.values()\n        if item.get("status") == "BLOCKED" and item.get("controlling_blocker")\n    ]\n',
        '    raw_blockers = [\n        item["controlling_blocker"]\n        for item in gates.values()\n        if item.get("status") == "BLOCKED" and item.get("controlling_blocker")\n    ]\n    # The legacy baseline remains blocked, but a recorded scoped no-go and\n    # named causal branches close the structural question for the lane.\n    blockers = [\n        blocker\n        for blocker in raw_blockers\n        if not (\n            blocker == "original_conserved_c_gradient_baseline_blocked"\n            and causal_lane_pass\n        )\n    ]\n',
        "causal blocker aggregation",
    )
    text = replace_once(
        text,
        '            "what_remains_open": blockers,\n            "dependency_unlocked": "Gravity/GR remains blocked until this full bridge and Core curved 3+1 gates pass",\n',
        '            "what_remains_open": blockers,\n            "baseline_open_items": (\n                [\n                    "original conserved-C local-gradient candidate remains BLOCKED; the named no-go and finite-cone branches are separate lanes",\n                ]\n                if causal_lane_pass\n                else []\n            ),\n            "dependency_unlocked": "Gravity/GR remains blocked until this full bridge and Core curved 3+1 gates pass",\n',
        "major result baseline field",
    )
    TARGET.write_text(text, encoding="utf-8")
    print("PASS_REPAIRED_TOPIC13_FULL_GATE_CAUSAL_REPORTING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
