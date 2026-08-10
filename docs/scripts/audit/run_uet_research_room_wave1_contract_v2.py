"""Run the Wave 1 contract builder with a Markdown-aware snapshot wrapper."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docs.scripts.audit import build_uet_research_room_wave1_contract as builder  # noqa: E402


ORIGINAL_SNAPSHOT = builder.snapshot


def markdown_snapshot(path: Path, selectors: tuple[str, ...] = ()) -> dict:
    if path.suffix.lower() in {".md", ".txt"}:
        text = path.read_text(encoding="utf-8")
        return {
            "path": path.relative_to(ROOT).as_posix(),
            "present": True,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "summary": {"required_report_headings_present": all(f"{key}:" in text for key in ("STATUS", "WHAT_CHANGED", "EQUATION_OR_MAPPING", "VERIFICATION", "CONTROLLING_BLOCKER", "NEXT_ACTION", "CLAIM_BOUNDARY"))},
        }
    return ORIGINAL_SNAPSHOT(path, selectors)


builder.snapshot = markdown_snapshot
raise SystemExit(builder.main())
