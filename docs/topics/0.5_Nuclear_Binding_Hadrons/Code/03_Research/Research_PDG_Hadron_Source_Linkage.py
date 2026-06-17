"""
PDG source-linkage diagnostic for topic 0.5 hadron and quark mass inputs.

This script does not validate the hadron/QCD model. It checks whether the
downloaded PDG 2025 SQLite source can reproduce the source records named by
the topic-local mapping gate, then writes a generated reference package and a
diagnostic artifact.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path


def _bootstrap() -> Path | None:
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return None


ROOT = _bootstrap()
if not ROOT:
    print("CRITICAL: UET docs root not found!")
    sys.exit(1)


from docs import ROOT_PATH
from docs.core.reproducibility import generate_artifact, hash_dataset, hash_file, save_artifact


root_path = ROOT_PATH
topic_dir = root_path / "docs" / "topics" / "0.5_Nuclear_Binding_Hadrons"
data_dir = topic_dir / "Data" / "03_Research"
artifact_dir = topic_dir / "Result" / "artifacts"

MAPPING_GATE_PATH = data_dir / "pdg_hadron_qcd_source_mapping_gate.json"
REFERENCE_PACKAGE_PATH = data_dir / "pdg_hadron_quark_reference_package.json"
ARTIFACT_PATH = artifact_dir / "pdg_hadron_quark_source_linkage.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def fetch_pdg_row(conn: sqlite3.Connection, pdgid: str) -> dict | None:
    row = conn.execute(
        """
        SELECT pdgid, edition, value_type, value, value_text, error_positive,
               error_negative, unit_text, display_value_text
        FROM pdgdata
        WHERE pdgid = ?
        ORDER BY
          CASE value_type WHEN 'AC' THEN 0 WHEN 'V' THEN 1 WHEN 'FC' THEN 2 ELSE 3 END,
          sort
        LIMIT 1
        """,
        (pdgid,),
    ).fetchone()
    if row is None:
        return None
    keys = [
        "pdgid",
        "edition",
        "value_type",
        "value",
        "value_text",
        "error_positive",
        "error_negative",
        "unit_text",
        "display_value_text",
    ]
    return dict(zip(keys, row))


def normalize_record(record: dict, row: dict | None, kind: str) -> dict:
    output = dict(record)
    output["record_kind"] = kind
    output["source_query_status"] = "FOUND" if row else "MISSING"
    output["source_row"] = row
    if row:
        output["value_delta_vs_gate"] = (
            abs(float(row["value"]) - float(record["value"]))
            if row.get("value") is not None and record.get("value") is not None
            else None
        )
        output["unit_matches_gate"] = row.get("unit_text") == record.get("unit")
    return output


def run_linkage() -> bool:
    print("=" * 76)
    print("PDG HADRON/QUARK SOURCE LINKAGE DIAGNOSTIC")
    print("Topic: 0.5_Nuclear_Binding_Hadrons")
    print("=" * 76)

    gate = load_json(MAPPING_GATE_PATH)
    db_path = root_path / gate["source_database"]["local_path"]
    if not db_path.exists():
        raise FileNotFoundError(f"PDG SQLite source not found: {db_path}")

    conn = sqlite3.connect(db_path)
    quark_records = []
    hadron_records = []

    for record in gate["mapped_quark_mass_records"]:
        quark_records.append(normalize_record(record, fetch_pdg_row(conn, record["pdgid"]), "quark_mass"))

    for record in gate["mapped_hadron_mass_records"]:
        hadron_records.append(normalize_record(record, fetch_pdg_row(conn, record["pdgid"]), "hadron_mass"))

    conn.close()

    all_records = quark_records + hadron_records
    found_count = sum(1 for row in all_records if row["source_query_status"] == "FOUND")
    missing_count = len(all_records) - found_count
    unit_mismatch_count = sum(
        1 for row in all_records if row["source_query_status"] == "FOUND" and not row.get("unit_matches_gate")
    )

    package = {
        "schema_version": "1.0",
        "topic": "0.5_Nuclear_Binding_Hadrons",
        "source_database": {
            **gate["source_database"],
            "local_path": str(db_path.relative_to(root_path)),
            "sha256_actual": hash_file(db_path),
        },
        "status": "SOURCE_MAPPED_PACKAGE_READY_DIAGNOSTIC",
        "claim_boundary": (
            "This package source-locks selected PDG 2025 quark and hadron mass rows for diagnostic "
            "work only. It does not validate the hadron model, QCD running, or confinement branches."
        ),
        "quark_mass_records": quark_records,
        "hadron_mass_records": hadron_records,
        "unmapped_or_ambiguous_records": gate["unmapped_or_ambiguous_records"],
        "summary": {
            "records_total": len(all_records),
            "records_found": found_count,
            "records_missing": missing_count,
            "unit_mismatch_count": unit_mismatch_count,
            "qcd_alpha_s_mapping_status": "NOT_MAPPED",
            "hadron_model_integration_status": "NOT_INTEGRATED",
        },
    }
    write_json(REFERENCE_PACKAGE_PATH, package)

    artifact = generate_artifact(
        topic="0.5_Nuclear_Binding_Hadrons",
        dataset_hash=hash_dataset(
            {
                "mapping_gate": str(MAPPING_GATE_PATH.relative_to(root_path)),
                "pdg_sqlite_sha256": hash_file(db_path),
                "reference_package": package["summary"],
            }
        ),
        results={
            "status": "DIAGNOSTIC_SOURCE_LINKAGE",
            "package_path": str(REFERENCE_PACKAGE_PATH.relative_to(root_path)),
            "package_sha256": hash_file(REFERENCE_PACKAGE_PATH),
            "summary": package["summary"],
            "claim_boundary": package["claim_boundary"],
            "blocked_exports": [
                "source-locked hadron-mass validation",
                "source-locked QCD-running validation",
                "confinement validation",
            ],
        },
        config={
            "mapping_gate": str(MAPPING_GATE_PATH.relative_to(root_path)),
            "pdg_sqlite": str(db_path.relative_to(root_path)),
        },
        metrics=package["summary"],
        thresholds={
            "required_records_found_for_package": len(all_records),
            "allowed_unit_mismatches": 0,
        },
        notes=(
            "This artifact proves source-linkage for selected quark/hadron mass rows only. "
            "A separate model verifier must read the generated package before hadron/QCD claims can change."
        ),
    )
    save_artifact(artifact, ARTIFACT_PATH)

    print(f"Records found: {found_count}/{len(all_records)}")
    print(f"Unit mismatches: {unit_mismatch_count}")
    print(f"Package saved to {REFERENCE_PACKAGE_PATH}")
    print(f"Artifact saved to {ARTIFACT_PATH}")
    return missing_count == 0 and unit_mismatch_count == 0


if __name__ == "__main__":
    sys.exit(0 if run_linkage() else 1)
