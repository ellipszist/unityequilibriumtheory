"""Repair one generated-audit script expression after ACL-safe patching."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_ding_public_supplementary_payload_boundary.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")
    old = '''            "verification_status": result_status := (\n                "PASS_PUBLIC_SUPPLEMENTARY_PAYLOAD_BOUNDARY_NO_NUMERIC_C_SRC"\n                if passed\n                else "FAIL_PUBLIC_SUPPLEMENTARY_PAYLOAD_BOUNDARY_AUDIT"\n            ),'''
    new = '''            "verification_status": (\n                "PASS_PUBLIC_SUPPLEMENTARY_PAYLOAD_BOUNDARY_NO_NUMERIC_C_SRC"\n                if passed\n                else "FAIL_PUBLIC_SUPPLEMENTARY_PAYLOAD_BOUNDARY_AUDIT"\n            ),'''
    if text.count(old) != 1:
        raise SystemExit(f"expected one syntax target, found {text.count(old)}")
    TARGET.write_text(text.replace(old, new), encoding="utf-8")
    print(f"repaired {TARGET.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
