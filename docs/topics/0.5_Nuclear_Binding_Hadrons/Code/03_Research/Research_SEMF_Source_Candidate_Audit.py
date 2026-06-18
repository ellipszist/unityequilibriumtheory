"""
SEMF source-candidate audit for topic 0.5.

This script compares the locally packaged SEMF coefficients against an
externally observed source-candidate row. The candidate is useful because it
matches the engine's coefficient set, but it is not a direct source lock: the
observed web page is a tertiary index that attributes the row to Rohlf (1994).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


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
local_package_path = data_dir / "semf_coefficient_local_package.json"
candidate_package_path = data_dir / "semf_coefficient_source_candidates.json"
artifact_path = artifact_dir / "semf_coefficient_source_candidate_audit.json"

SOURCE_CANDIDATES = [
    {
        "candidate_id": "wikipedia_semf_coefficients_rohlf_attributed_2026_06_19",
        "source_type": "tertiary_web_index",
        "retrieved_date": "2026-06-19",
        "retrieved_url": "https://en.wikipedia.org/wiki/Semi-empirical_mass_formula",
        "observed_location": "coefficients table under the page section that discusses calculating coefficients",
        "attributed_source": {
            "author": "J. W. Rohlf",
            "title": "Modern Physics from alpha to Z0",
            "publisher": "John Wiley & Sons",
            "year": 1994,
            "isbn": "978-0471572701",
            "direct_source_record_status": "NOT_HELD_IN_TOPIC_PACKAGE",
        },
        "coefficients": {
            "a_vol": 15.75,
            "a_surf": 17.8,
            "a_coul": 0.711,
            "a_asym": 23.7,
            "a_pair": 11.18,
            "k_pair": -0.5,
        },
        "candidate_limitations": [
            "The observed web page is not the direct textbook page.",
            "The topic package does not yet contain a scan, DOI, archive page, or page-numbered source record for Rohlf 1994.",
            "The row can support a source-candidate match only, not source-locked coefficient provenance.",
        ],
    }
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def local_coefficients(package: dict[str, Any]) -> dict[str, float]:
    records: dict[str, float] = {}
    for row in package["semf_coefficients"]:
        records[row["symbol"]] = float(row["value"])
    records["k_pair"] = -0.5
    return records


def compare_candidate(local: dict[str, float], candidate: dict[str, Any]) -> dict[str, Any]:
    comparisons = []
    for symbol, candidate_value in candidate["coefficients"].items():
        local_value = local.get(symbol)
        matches = local_value is not None and abs(float(local_value) - float(candidate_value)) <= 1e-12
        comparisons.append(
            {
                "symbol": symbol,
                "local_value": local_value,
                "candidate_value": candidate_value,
                "matches": matches,
            }
        )
    return {
        "candidate_id": candidate["candidate_id"],
        "comparison_count": len(comparisons),
        "match_count": sum(1 for row in comparisons if row["matches"]),
        "mismatch_count": sum(1 for row in comparisons if not row["matches"]),
        "direct_source_record_status": candidate["attributed_source"]["direct_source_record_status"],
        "source_lock_status": "CANDIDATE_MATCH_NOT_SOURCE_LOCKED",
        "comparisons": comparisons,
    }


def build_candidate_package(local_package: dict[str, Any], audits: list[dict[str, Any]]) -> dict[str, Any]:
    exact_match_count = sum(1 for audit in audits if audit["mismatch_count"] == 0)
    return {
        "schema_version": "1.0",
        "topic": "0.5_Nuclear_Binding_Hadrons",
        "package_status": "SOURCE_CANDIDATE_MATCH_DIRECT_SOURCE_BLOCKED",
        "purpose": "Records external source candidates for the exact SEMF coefficient set used by the local engine.",
        "local_package": {
            "path": "Data/03_Research/semf_coefficient_local_package.json",
            "sha256": hash_file(local_package_path),
            "status": local_package["package_status"],
        },
        "summary": {
            "candidate_count": len(SOURCE_CANDIDATES),
            "exact_candidate_match_count": exact_match_count,
            "direct_source_records_locked": 0,
            "source_lock_status": "CANDIDATE_MATCH_NOT_SOURCE_LOCKED",
        },
        "source_candidates": SOURCE_CANDIDATES,
        "candidate_audits": audits,
        "required_to_close": [
            "Acquire or cite a direct, page-numbered Rohlf 1994 source record for the coefficient row, or replace the engine coefficients with a different directly sourced set.",
            "Record the SEMF coefficient fitting convention and uncertainty policy.",
            "Keep the Yukawa correction policy separate from SEMF coefficient provenance.",
        ],
        "blocked_usage": [
            "source-locked SEMF coefficient claim",
            "parameter-free nuclear-binding claim",
            "first-principles nuclear-binding derivation claim",
        ],
        "claim_boundary": (
            "The engine coefficient set has an exact external source-candidate match, but the topic "
            "does not yet hold the direct source record. Treat this as candidate provenance only."
        ),
    }


def run_audit() -> bool:
    print("=" * 76)
    print("SEMF SOURCE-CANDIDATE AUDIT")
    print("Topic: 0.5_Nuclear_Binding_Hadrons")
    print("=" * 76)

    local_package = load_json(local_package_path)
    local = local_coefficients(local_package)
    audits = [compare_candidate(local, candidate) for candidate in SOURCE_CANDIDATES]
    candidate_package = build_candidate_package(local_package, audits)
    write_json(candidate_package_path, candidate_package)

    summary = candidate_package["summary"]
    print(f"Candidates checked:         {summary['candidate_count']}")
    print(f"Exact candidate matches:    {summary['exact_candidate_match_count']}")
    print(f"Direct source records held: {summary['direct_source_records_locked']}")
    print(f"Package saved to:           {candidate_package_path}")

    artifact = generate_artifact(
        topic="0.5_Nuclear_Binding_Hadrons",
        dataset_hash=hash_dataset(
            {
                "local_package_path": str(local_package_path.relative_to(root_path)),
                "local_package_sha256": hash_file(local_package_path),
                "candidate_package_path": str(candidate_package_path.relative_to(root_path)),
                "candidate_ids": [candidate["candidate_id"] for candidate in SOURCE_CANDIDATES],
            }
        ),
        results={
            "status": "SOURCE_CANDIDATE_MATCH_DIRECT_SOURCE_BLOCKED",
            "summary": summary,
            "candidate_package_path": str(candidate_package_path.relative_to(topic_dir)).replace("\\", "/"),
            "candidate_package_sha256": hash_file(candidate_package_path),
            "candidate_audits": audits,
            "claim_boundary": candidate_package["claim_boundary"],
            "blocked_exports": candidate_package["blocked_usage"],
        },
        config={
            "method": "Compare locally packaged SEMF coefficients to manually recorded external source-candidate rows.",
            "local_package": str(local_package_path.relative_to(topic_dir)).replace("\\", "/"),
            "candidate_source_policy": "Candidate row is useful for narrowing provenance, but not direct-source evidence.",
        },
        metrics=summary,
        thresholds={
            "required_exact_candidate_match_count": 1,
            "required_direct_source_records_locked_for_source_lock": 1,
        },
        notes=(
            "This audit narrows the SEMF blocker to direct-source acquisition. "
            "It does not source-lock the coefficient set."
        ),
    )
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to:          {artifact_path}")
    return summary["exact_candidate_match_count"] >= 1


if __name__ == "__main__":
    sys.exit(0 if run_audit() else 1)
