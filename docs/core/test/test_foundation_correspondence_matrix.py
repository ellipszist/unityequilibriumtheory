"""Regression tests for the focused cross-topic correspondence matrix."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/audit/build_uet_foundation_correspondence_matrix.py"


def load_matrix_module():
    spec = importlib.util.spec_from_file_location("uet_correspondence_matrix", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load matrix module: {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_matrix_keeps_standard_baseline_open_bridge_and_conflict_distinct():
    matrix = load_matrix_module().build_matrix()
    rows = {row["matrix_id"]: row for row in matrix["rows"]}

    assert matrix["audit_status"] == "PASS"
    assert matrix["matrix_status"] == "BLOCKED"
    assert rows["T13-004"]["compatibility_status"] == "COMPATIBLE_STANDARD_IDENTITY"
    assert rows["EW-01"]["uet_derivation_status"] == "NOT_ESTABLISHED"
    assert rows["uet.legacy.master_potential"]["compatibility_status"] == "CONTRADICTION"
    assert rows["T01-001"]["special_case_status"] == "NOT_TESTABLE"
