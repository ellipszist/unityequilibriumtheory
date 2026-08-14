"""Keep the original full-candidate causal gate blocked while exposing lane closure."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = '            "status": "PASS" if causal_lane_pass else "BLOCKED",\n'
    new = (
        '            # The named lane may close without promoting the original\n'
        '            # full-candidate causal gate.\n'
        '            "status": "PASS" if full_candidate_pass else "BLOCKED",\n'
        '            "lane_status": "PASS" if causal_lane_pass else "BLOCKED",\n'
        '            "formal_no_go_closure": "CLOSED_AS_NO_GO" if formal_no_go_recorded else "OPEN",\n'
    )
    if old not in text:
        if new in text:
            print("TOPIC13_CAUSAL_GATE_STATUS_BOUNDARY_ALREADY_PRESENT")
            return 0
        raise SystemExit("causal gate status line not found")
    TARGET.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("ADDED_TOPIC13_CAUSAL_GATE_STATUS_BOUNDARY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
