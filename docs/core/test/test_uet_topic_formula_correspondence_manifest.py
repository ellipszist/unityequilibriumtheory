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
    assert artifact["audit_status"] == "PASS_WITH_OPEN_ROW_MAPPINGS"
    assert coverage["source_rows"] == 263
    assert coverage["manifest_rows"] == coverage["source_rows"]
    assert coverage["rows_missing_from_manifest"] == 0


def test_manifest_does_not_promote_lane_relations_or_observables() -> None:
    artifact = load()
    rows = artifact["rows"]
    coverage = artifact["coverage"]
    assert coverage["central_registry_exact_links"] == 0
    assert coverage["measurement_operator_declared_rows"] == 7
    assert coverage["measurement_operator_open_rows"] == len(rows) - 7
    assert coverage["measurement_operator_blocked_rows"] == len(rows)
    assert all(not row["central_registry_relation"]["exact_identity"] for row in rows)
    mapped_ids = {row["formula_id"] for row in rows if row["measurement_operator"]["status"] != "OPEN_UNRESOLVED"}
    assert mapped_ids == {
        "PT-ORDER-PARAMETER",
        "PT-CONSERVED-ORDER-SPECTRAL-L16-STRUCTURE-FACTOR-ESTIMATOR",
        "PT-CONSERVED-ORDER-SPECTRAL-STRUCTURE-FACTOR-MULTIGRID",
        "T13-010",
        "T13-013",
        "T13-014",
        "T13-015",
    }
