"""Add explicit top-level holdout and data-use fields to the causal audit."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_causal_branch_selection.py"
OLD = '        "checks": checks,\n        "controlling_blocker":'
NEW = '        "checks": checks,\n        "parameter_fitting_performed": False,\n        "source_rows_consumed": False,\n        "target_data_used": False,\n        "xie_2026_accessed": False,\n        "controlling_blocker":'


def main() -> int:
    content = TARGET.read_text(encoding="utf-8")
    if OLD in content:
        content = content.replace(OLD, NEW, 1)
    elif NEW not in content:
        raise SystemExit("expected causal audit report insertion point not found")
    TARGET.write_text(content, encoding="utf-8")
    print("PASS_REPAIRED_T13_CAUSAL_BRANCH_HOLDOUT_FIELDS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
