"""Regression checks for the row-complete F2 correspondence manifest."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3] / "docs/core"
ARTIFACT = ROOT / "artifacts/uet_topic_formula_correspondence_manifest.json"


def load() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def test_manifest_indexes_every_topic_formula_row() -> None:
    artifact = load()
    coverage = artifact["coverage"]
    assert artifact["audit_status"] == "PASS_WITH_EXPLICIT_BLOCKED_DISPOSITIONS"
    assert coverage["source_rows"] == 263
    assert coverage["manifest_rows"] == coverage["source_rows"]
    assert coverage["rows_missing_from_manifest"] == 0


def test_manifest_does_not_promote_lane_relations_or_observables() -> None:
    artifact = load()
    rows = artifact["rows"]
    coverage = artifact["coverage"]
    assert coverage["central_registry_exact_links"] == 0
    assert coverage["measurement_operator_declared_rows"] == len(rows)
    assert coverage["measurement_operator_open_rows"] == 0
    assert coverage["measurement_operator_placeholder_rows"] == len(rows) - 7
    assert coverage["measurement_operator_accepted_rows"] == 0
    assert coverage["measurement_operator_pending_rows"] == len(rows)
    assert coverage["measurement_operator_blocked_rows"] == len(rows)
    assert all(not row["central_registry_relation"]["exact_identity"] for row in rows)
    assert all(row["measurement_operator"]["status"] != "OPEN_UNRESOLVED" for row in rows)
    assert all(not row["measurement_operator"]["physical_closure"] for row in rows)
    placeholder_ids = {row["formula_id"] for row in rows if row["measurement_operator"]["kind"] == "row_level_observable_contract_placeholder"}
    assert len(placeholder_ids) == len(rows) - 7
