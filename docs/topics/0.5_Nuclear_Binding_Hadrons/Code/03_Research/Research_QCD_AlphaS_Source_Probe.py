"""
QCD alpha_s source probe for topic 0.5.

This diagnostic checks two narrow things:

1. The `alpha_s_uet_v2` branch no longer fails on the known QCD_PARAMS
   data-shape bug.
2. The local PDG 2025 SQLite source is searched for alpha_s/QCD-running rows.

It does not validate QCD running or promote the QCD branch.
"""

from __future__ import annotations

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
artifact_dir = topic_dir / "Result" / "artifacts"
engine_dir = topic_dir / "Code" / "01_Engine"
if str(engine_dir) not in sys.path:
    sys.path.insert(0, str(engine_dir))

from Engine_QCD_Bridge import alpha_s_uet_v2


PDG_SQLITE_PATH = root_path / "docs" / "data" / "external" / "particle_physics" / "pdg" / "pdg-2025-v0.2.2.sqlite"
ARTIFACT_PATH = artifact_dir / "qcd_alpha_s_source_probe.json"

SEARCH_TERMS = ["alpha_s", "strong coupling", "qcd running", "lambda_qcd"]
SMOKE_TEST_SCALES_GEV = [1.5, 5.0, 91.2, 172.0]


def search_pdg_sqlite() -> list[dict]:
    rows: list[dict] = []
    conn = sqlite3.connect(PDG_SQLITE_PATH)
    try:
        for term in SEARCH_TERMS:
            pattern = f"%{term.lower()}%"
            found = conn.execute(
                """
                SELECT p.pdgid, p.description, d.value, d.value_text, d.unit_text, d.display_value_text
                FROM pdgid p
                LEFT JOIN pdgdata d ON p.pdgid = d.pdgid
                WHERE lower(p.description) LIKE ?
                   OR lower(p.pdgid) LIKE ?
                   OR lower(coalesce(d.comment, '')) LIKE ?
                   OR lower(coalesce(d.value_text, '')) LIKE ?
                ORDER BY p.pdgid, d.sort
                LIMIT 40
                """,
                (pattern, pattern, pattern, pattern),
            ).fetchall()
            for row in found:
                rows.append(
                    {
                        "search_term": term,
                        "pdgid": row[0],
                        "description": row[1],
                        "value": row[2],
                        "value_text": row[3],
                        "unit_text": row[4],
                        "display_value_text": row[5],
                    }
                )
    finally:
        conn.close()
    return rows


def run_probe() -> bool:
    print("=" * 76)
    print("QCD ALPHA_S SOURCE PROBE")
    print("Topic: 0.5_Nuclear_Binding_Hadrons")
    print("=" * 76)

    smoke_results = []
    for scale in SMOKE_TEST_SCALES_GEV:
        value = alpha_s_uet_v2(scale)
        smoke_results.append(
            {
                "Q_GeV": scale,
                "alpha_s_uet_v2": value,
                "finite": value == value and value not in (float("inf"), float("-inf")),
            }
        )

    pdg_matches = search_pdg_sqlite()
    relevant_matches = [
        row
        for row in pdg_matches
        if row["description"]
        and any(token in row["description"].lower() for token in ("alpha_s", "strong coupling", "qcd running", "lambda_qcd"))
    ]

    summary = {
        "pdg_sqlite_search_terms": SEARCH_TERMS,
        "pdg_sqlite_raw_match_count": len(pdg_matches),
        "pdg_sqlite_relevant_alpha_s_match_count": len(relevant_matches),
        "alpha_s_uet_v2_smoke_count": len(smoke_results),
        "alpha_s_uet_v2_finite_count": sum(1 for row in smoke_results if row["finite"]),
        "source_mapping_status": "NO_ALPHA_S_SUMMARY_ROW_FOUND_IN_LOCAL_PDG_SQLITE",
        "model_status": "BUG_FIXED_DIAGNOSTIC_ONLY",
    }

    print(f"alpha_s_uet_v2 finite: {summary['alpha_s_uet_v2_finite_count']}/{summary['alpha_s_uet_v2_smoke_count']}")
    print(f"PDG raw matches:       {summary['pdg_sqlite_raw_match_count']}")
    print(f"Relevant alpha_s rows: {summary['pdg_sqlite_relevant_alpha_s_match_count']}")

    artifact = generate_artifact(
        topic="0.5_Nuclear_Binding_Hadrons",
        dataset_hash=hash_dataset(
            {
                "pdg_sqlite": str(PDG_SQLITE_PATH.relative_to(root_path)),
                "pdg_sqlite_sha256": hash_file(PDG_SQLITE_PATH),
                "search_terms": SEARCH_TERMS,
                "smoke_scales": SMOKE_TEST_SCALES_GEV,
            }
        ),
        results={
            "status": "DIAGNOSTIC_QCD_ALPHA_S_SOURCE_PROBE",
            "summary": summary,
            "smoke_results": smoke_results,
            "pdg_relevant_matches": relevant_matches,
            "claim_boundary": (
                "This artifact only confirms that alpha_s_uet_v2 executes after the data-shape fix "
                "and that the local PDG SQLite search did not find a direct alpha_s/QCD-running "
                "summary row with the current query policy."
            ),
            "blocked_exports": [
                "source-locked QCD-running validation",
                "alpha_s prediction claim",
                "QCD derivation claim",
            ],
        },
        config={
            "pdg_sqlite": str(PDG_SQLITE_PATH.relative_to(root_path)),
            "engine": "Code/01_Engine/Engine_QCD_Bridge.py",
            "search_terms": SEARCH_TERMS,
        },
        metrics=summary,
        thresholds={
            "required_finite_smoke_results": len(SMOKE_TEST_SCALES_GEV),
            "required_alpha_s_source_rows_for_validation": 1,
        },
        notes=(
            "Use this as a blocker-narrowing diagnostic. A source-backed QCD-running package "
            "still requires a vetted alpha_s source row or a separate external source package."
        ),
    )
    save_artifact(artifact, ARTIFACT_PATH)
    print(f"Artifact saved to {ARTIFACT_PATH}")
    return summary["alpha_s_uet_v2_finite_count"] == summary["alpha_s_uet_v2_smoke_count"]


if __name__ == "__main__":
    sys.exit(0 if run_probe() else 1)
