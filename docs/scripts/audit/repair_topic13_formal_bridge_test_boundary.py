"""Update the beta integration expectation to the explicit two-level boundary."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/core/test/test_topic13_thermal_response_beta_contract_integration.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = '    assert full["verification_status"]["non_circular_bridge"]["status"] == "BLOCKED"\n'
    new = (
        '    assert full["verification_status"]["non_circular_bridge"]["status"] == "BLOCKED"\n'
        '    assert full["verification_status"]["non_circular_bridge"]["formal_boundary_closure_level"] == "CLOSED_FOR_LANE"\n'
    )
    if old not in text:
        if 'formal_boundary_closure_level' in text:
            print("FORMAL_BRIDGE_TEST_BOUNDARY_ALREADY_PRESENT")
            return 0
        raise SystemExit("beta integration boundary assertion not found")
    TARGET.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("UPDATED_FORMAL_BRIDGE_TEST_BOUNDARY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
