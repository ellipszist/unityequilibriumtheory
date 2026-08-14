"""Keep the legacy Ding route field stable while exposing the new request state."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SYNC = ROOT / "docs/scripts/audit/sync_topic13_ding_pbte_author_request.py"
OLD = 'energy["pbte_numeric_input_availability"]["author_request_route"] = "REQUEST_PACKAGE_READY_NOT_SENT"'
NEW = '''# Preserve the legacy route field for existing consumers; expose the
    # machine-readable request state in the adjacent package record.
    energy["pbte_numeric_input_availability"]["author_request_route"] = "OPEN_NOT_EXECUTED"'''


def main() -> int:
    text = SYNC.read_text(encoding="utf-8")
    if OLD in text:
        text = text.replace(OLD, NEW, 1)
        SYNC.write_text(text, encoding="utf-8")
        print("PATCHED_LEGACY_AUTHOR_REQUEST_ROUTE_FIELD")
    else:
        print("LEGACY_AUTHOR_REQUEST_ROUTE_FIELD_ALREADY_PATCHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
