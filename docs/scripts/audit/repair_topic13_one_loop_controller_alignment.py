"""Align the one-loop integration controller with the audit blocker key."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SYNC = ROOT / "docs/scripts/audit/sync_topic13_uet_o2_one_loop_normal_branch.py"


def main() -> int:
    text = SYNC.read_text(encoding="utf-8")
    old = 'blocker = "vacuum_counterterm_and_interacting_finite_temperature_UET_completion_not_closed"'
    new = 'blocker = "vacuum_counterterm_and_renormalized_one_loop_response_not_closed"'
    if old not in text:
        raise SystemExit("one-loop sync controller string not found")
    SYNC.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("PATCHED_T13_ONE_LOOP_CONTROLLER_ALIGNMENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
