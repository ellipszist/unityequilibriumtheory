"""Point the new integration test at the detailed request-state field."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TEST = ROOT / "docs/core/test/test_topic13_ding_pbte_author_request_integration.py"
OLD = 'assert energy["pbte_numeric_input_availability"]["author_request_route"] == "REQUEST_PACKAGE_READY_NOT_SENT"'
NEW = 'assert energy["pbte_numeric_input_availability"]["author_request_package"]["request_state"] == "REQUEST_PACKAGE_READY_NOT_SENT"'


def main() -> int:
    text = TEST.read_text(encoding="utf-8")
    if OLD in text:
        TEST.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
        print("PATCHED_AUTHOR_REQUEST_INTEGRATION_TEST_STATE_FIELD")
    else:
        print("AUTHOR_REQUEST_INTEGRATION_TEST_STATE_FIELD_ALREADY_PATCHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
