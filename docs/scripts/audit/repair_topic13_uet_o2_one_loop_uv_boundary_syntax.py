"""Repair the UV-boundary audit predicate without editing the audit by hand."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_uet_o2_one_loop_uv_boundary.py"
OLD = '        "phi_is_not_relabelled_as_temperature": "Phi": "action response input; not temperature" in json.dumps(branch_audit["major_result"]),\n'
NEW = '        "phi_is_not_relabelled_as_temperature": "action response input; not temperature" in json.dumps(branch_audit["major_result"]),\n'


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    if OLD not in text:
        raise SystemExit("expected malformed predicate was not found")
    TARGET.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("REPAIRED_TOPIC13_UET_O2_ONE_LOOP_UV_BOUNDARY_SYNTAX")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
