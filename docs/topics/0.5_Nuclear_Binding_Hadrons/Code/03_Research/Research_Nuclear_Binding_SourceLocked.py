"""
UET Nuclear Binding Test against source-backed local datasets
=============================================================
Uses the topic's AME2020 extracted JSON subset and proton-radius reference JSON.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path


def _bootstrap():
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
from docs.core.reproducibility import generate_artifact, hash_dataset, save_artifact


root_path = ROOT_PATH
topic_dir = root_path / "docs" / "topics" / "0.5_Nuclear_Binding_Hadrons"
data_dir = topic_dir / "Data" / "03_Research"
engine_path = topic_dir / "Code" / "01_Engine"
if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

from Engine_Nuclear_Binding import UETNuclearBindingEngine


AME_JSON = data_dir / "Data_AME2020_Binding_RawSubset.json"
AME_FULL_JSON = data_dir / "Data_AME2020_Binding_FullParsed.json"
AME_MANIFEST_JSON = data_dir / "Data_AME2020_Benchmark_Manifest.json"
PROTON_RADIUS_JSON = data_dir / "Data_Proton_Radius.json"
PDG_QUARKS_JSON = data_dir / "Data_PDG_Quarks_2024.json"
SOURCE_EVIDENCE_INTAKE_PATH = data_dir / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = data_dir / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = data_dir / "branch_claim_gate.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def binding_per_nucleon(be_kev: float, a: int) -> float:
    return (be_kev / 1000.0) / a


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.5_Nuclear_Binding_Hadrons",
        "purpose": "Source evidence intake before data normalization or claim upgrades across nuclear, hadron, and QCD branches.",
        "source_targets": [
            {
                "name": "AME2020 raw table and validation subset package",
                "priority": "immediate",
                "status_hint": "source_backed_ready",
                "evidence_entries": [
                    "raw_source_path",
                    "derived_subset_path",
                    "benchmark_manifest_path",
                    "parsed_table_count",
                    "gate_definition",
                    "extraction_note",
                ],
            },
            {
                "name": "Proton radius benchmark package",
                "priority": "high",
                "status_hint": "source_backed_ready",
                "evidence_entries": [
                    "benchmark_file_path",
                    "source_identity",
                    "benchmark_variant",
                    "unit_basis",
                    "comparison_role",
                    "extraction_note",
                ],
            },
            {
                "name": "PDG quark-mass source package",
                "priority": "high",
                "status_hint": "pending_external_source_lock",
                "evidence_entries": [
                    "doi_or_url",
                    "local_path",
                    "table_or_review_identifier",
                    "retrieval_date",
                    "unit_basis",
                    "extraction_note",
                ],
            },
            {
                "name": "QCD running benchmark package",
                "priority": "high",
                "status_hint": "pending_qcd_branch_hardening",
                "evidence_entries": [
                    "benchmark_identity",
                    "local_path",
                    "source_reference",
                    "unit_basis",
                    "parameter_note",
                    "bug_status_note",
                ],
            },
            {
                "name": "Confinement proof gate package",
                "priority": "medium",
                "status_hint": "pending_proof_gate_fix",
                "evidence_entries": [
                    "proof_script_path",
                    "return_contract_note",
                    "benchmark_identity",
                    "status_rule",
                    "artifact_path",
                    "limitation_note",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance work only. It does not authorize stronger strong-force or hadron claims by itself.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "AME2020 raw table and validation subset package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Proton radius benchmark package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "PDG quark-mass source package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "doi_or_url",
                "local_path",
                "table_or_review_identifier",
                "retrieval_date",
                "extraction_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "Working-copy source label exists, but the PDG package is not yet source-locked to an upstream record in this topic.",
        },
        {
            "name": "QCD running benchmark package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "local_path",
                "source_reference",
                "unit_basis",
                "parameter_note",
                "bug_status_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The QCD branch still has unresolved source-lock work and an open alpha_s_uet_v2 data-shape bug.",
        },
        {
            "name": "Confinement proof gate package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 2,
            "fields_pending": 4,
            "pending_fields": [
                "benchmark_identity",
                "status_rule",
                "artifact_path",
                "limitation_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The proof script still returns True instead of enforcing an audit-grade pass/fail contract.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.5_Nuclear_Binding_Hadrons",
        "purpose": "Readiness matrix for source-evidence review across nuclear binding, hadron, and QCD lanes.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row means the topic has enough local provenance structure for source review. It does not itself upgrade a claim.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.5_Nuclear_Binding_Hadrons",
        "purpose": "Claim gate for separate nuclear, hadron, and QCD branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 2,
            "blocked_for_strong_claims": 4,
        },
        "branches": [
            {
                "branch": "Heavy-nucleus binding subset branch",
                "status": "accepted_run_contract_only",
                "allowed_usage_now": "Source-backed heavy-nucleus subset benchmark for A >= 16 only.",
                "blocker_to_stronger_claim": "Need clearer SEMF-versus-UET decomposition and broader validation before promoting to a general nuclear-binding claim.",
            },
            {
                "branch": "Proton radius benchmark branch",
                "status": "accepted_benchmark_anchor_only",
                "allowed_usage_now": "Benchmark-anchor compatibility check only.",
                "blocker_to_stronger_claim": "Need a derived radius relation rather than an anchor-like returned value.",
            },
            {
                "branch": "Light nuclei branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Diagnostic/excluded lane only.",
                "blocker_to_stronger_claim": "Need a dedicated light-nuclei verifier and source-backed treatment of empirical constants.",
            },
            {
                "branch": "Hadron mass branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Diagnostic hadron-model lane only.",
                "blocker_to_stronger_claim": "Need source-locked quark/hadron inputs and a dedicated verifier artifact.",
            },
            {
                "branch": "QCD running branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Open diagnostic branch only.",
                "blocker_to_stronger_claim": "Need source-backed QCD benchmarks and a fix for the alpha_s_uet_v2 data-shape bug.",
            },
            {
                "branch": "Confinement proof branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not audit-grade at present.",
                "blocker_to_stronger_claim": "Need a real pass/fail proof gate and a defensible derivation benchmark.",
            },
        ],
        "claim_boundary": "This gate cannot raise the topic above the current heavy-nucleus subset benchmark plus proton-radius anchor compatibility.",
    }


def run_test() -> bool:
    print("=" * 72)
    print("UET NUCLEAR BINDING TEST - SOURCE-BACKED AME2020")
    print("Data: AME2020 table-wide parse + raw-derived subset + proton radius")
    print("=" * 72)

    ame = load_json(AME_JSON)
    full_ame = load_json(AME_FULL_JSON)
    manifest = load_json(AME_MANIFEST_JSON)
    proton = load_json(PROTON_RADIUS_JSON)
    pdg_quarks = load_json(PDG_QUARKS_JSON)
    engine = UETNuclearBindingEngine()
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()

    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)

    print("\n[1] BINDING ENERGY CHECKS")
    print("-" * 72)
    print("| Nucleus | A | Z | Obs BE/A | UET BE/A | Error | Heavy-nucleus gate |")
    print("| :-- | --: | --: | --: | --: | --: | :-- |")

    comparisons = {}
    errors = []
    heavy_errors = []
    light_excluded = []
    heavy_pass = True
    heavy_count = 0
    for symbol, row in ame["data"].items():
        a = row["A"]
        z = row["Z"]
        obs = binding_per_nucleon(row["BE_keV"], a)
        pred = engine.binding_energy_per_nucleon(a, z)
        err = abs(pred - obs) / obs * 100 if obs else 0.0
        heavy_gate = a >= 16
        if heavy_gate:
            heavy_count += 1
            heavy_pass = heavy_pass and (err < 15.0)
            heavy_errors.append(err)
        else:
            light_excluded.append(symbol)
        errors.append(err)
        comparisons[symbol] = {
            "A": a,
            "Z": z,
            "observed_be_per_a_mev": obs,
            "predicted_be_per_a_mev": pred,
            "relative_error_percent": err,
            "heavy_nucleus_gate": heavy_gate,
            "passes": (err < 15.0) if heavy_gate else None,
        }
        print(
            f"| {symbol} | {a} | {z} | {obs:.3f} | {pred:.3f} | {err:.2f}% | "
            f"{'PASS' if comparisons[symbol]['passes'] else ('SKIP' if not heavy_gate else 'FAIL')} |"
        )

    print("\n[2] PROTON RADIUS CHECK")
    print("-" * 72)
    rp_pred = engine.compute_proton_radius()
    rp_obs = proton["data"]["prad_2019_fm"]["value"]
    rp_err = abs(rp_pred - rp_obs) / rp_obs * 100 if rp_obs else 0.0
    rp_pass = rp_err < 5.0
    print(f"UET proton radius: {rp_pred:.6f} fm")
    print(f"PRad 2019:         {rp_obs:.6f} fm")
    print(f"Relative error:    {rp_err:.3f}%")
    print(f"Gate (<5%):        {'PASS' if rp_pass else 'FAIL'}")

    overall = heavy_pass and rp_pass and heavy_count > 0
    print(f"\nRESULT: {'PASS' if overall else 'FAIL'}")

    error_distribution = {
        "mean_error_percent": statistics.fmean(errors) if errors else None,
        "median_error_percent": statistics.median(errors) if errors else None,
        "max_error_percent": max(errors) if errors else None,
        "heavy_mean_error_percent": statistics.fmean(heavy_errors) if heavy_errors else None,
        "heavy_median_error_percent": statistics.median(heavy_errors) if heavy_errors else None,
        "heavy_max_error_percent": max(heavy_errors) if heavy_errors else None,
    }
    worst_cases = sorted(
        [
            {
                "symbol": symbol,
                "A": row["A"],
                "Z": row["Z"],
                "relative_error_percent": row["relative_error_percent"],
                "heavy_nucleus_gate": row["heavy_nucleus_gate"],
            }
            for symbol, row in comparisons.items()
        ],
        key=lambda item: item["relative_error_percent"],
        reverse=True,
    )[:5]

    print("\n[3] COVERAGE SUMMARY")
    print("-" * 72)
    print(f"AME2020 parsed rows with BE/A: {full_ame['parsed_table_count']}")
    print(f"Validation subset rows:        {len(ame['data'])}")
    print(f"Light diagnostic exclusions:   {len(light_excluded)}")
    print(f"Heavy-gate max error:          {error_distribution['heavy_max_error_percent']:.2f}%")

    artifact = generate_artifact(
        topic="0.5_Nuclear_Binding_Hadrons",
        dataset_hash=hash_dataset(
            {
                "ame_json": str(AME_JSON.relative_to(root_path)),
                "ame_full_json": str(AME_FULL_JSON.relative_to(root_path)),
                "ame_manifest_json": str(AME_MANIFEST_JSON.relative_to(root_path)),
                "proton_radius_json": str(PROTON_RADIUS_JSON.relative_to(root_path)),
                "pdg_quarks_json": str(PDG_QUARKS_JSON.relative_to(root_path)),
                "ame_subset_keys": sorted(ame["data"].keys()),
                "parsed_table_count": full_ame["parsed_table_count"],
            }
        ),
        results={
            "status": "PASS" if overall else "FAIL",
            "binding_comparisons": comparisons,
            "coverage": {
                "parsed_table_count": full_ame["parsed_table_count"],
                "validation_subset_count": len(ame["data"]),
                "excluded_light_cases": light_excluded,
                "skipped_no_binding_count": full_ame.get("skipped_no_binding_count"),
                "manifest": manifest,
            },
            "error_distribution": error_distribution,
            "worst_cases": worst_cases,
            "proton_radius": {
                "predicted_fm": rp_pred,
                "observed_fm": rp_obs,
                "relative_error_percent": rp_err,
                "passes": rp_pass,
            },
            "heavy_nuclei_all_pass": heavy_pass,
            "source_evidence_readiness_summary": source_evidence_readiness_matrix["summary"],
            "branch_claim_gate_summary": branch_claim_gate["summary"],
        },
        config={
            "binding_reference": str(AME_JSON.relative_to(root_path)),
            "full_table_reference": str(AME_FULL_JSON.relative_to(root_path)),
            "benchmark_manifest": str(AME_MANIFEST_JSON.relative_to(root_path)),
            "proton_radius_reference": str(PROTON_RADIUS_JSON.relative_to(root_path)),
            "pdg_quarks_reference": str(PDG_QUARKS_JSON.relative_to(root_path)),
            "note": "AME2020 input now has a table-wide parsed layer. The current pass/fail gate still uses a selected validation subset plus coverage metrics.",
        },
        metrics={
            "heavy_nuclei_all_pass": heavy_pass,
            "proton_radius_relative_error_percent": rp_err,
            "parsed_table_count": full_ame["parsed_table_count"],
            "validation_subset_count": len(ame["data"]),
            "excluded_count": len(light_excluded),
            "mean_error_percent": error_distribution["mean_error_percent"],
            "median_error_percent": error_distribution["median_error_percent"],
            "max_error_percent": error_distribution["max_error_percent"],
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
        },
        thresholds={
            "heavy_nucleus_binding_error_percent_max": 15.0,
            "proton_radius_relative_error_percent_max": 5.0,
        },
        notes="This verifier reads a raw-derived AME2020 subset plus source-backed proton-radius data, and now records source-evidence and branch-claim workflow gates.",
    )
    artifact["source_evidence_intake_stub"] = {
        "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(source_evidence_intake_stub),
        "source_targets": [row["name"] for row in source_evidence_intake_stub["source_targets"]],
        "claim_boundary": source_evidence_intake_stub["claim_boundary"],
    }
    artifact["source_evidence_readiness_matrix"] = {
        "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(source_evidence_readiness_matrix),
        "summary": source_evidence_readiness_matrix["summary"],
        "claim_boundary": source_evidence_readiness_matrix["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(branch_claim_gate),
        "summary": branch_claim_gate["summary"],
        "claim_boundary": branch_claim_gate["claim_boundary"],
    }
    artifact["interpretation"] = (
        "This artifact supports a source-backed heavy-nucleus subset benchmark and a proton-radius "
        "anchor-compatibility check. It does not validate light nuclei, hadron masses, QCD running, "
        "or confinement claims as audit-grade passes."
    )
    artifact["limitations"] = [
        "The strict pass/fail gate applies only to selected heavy nuclei plus proton-radius compatibility.",
        "Light nuclei remain diagnostic and can fail badly outside the liquid-drop validation regime.",
        "The proton-radius path is still benchmark-anchor behavior, not an independent prediction.",
        "Hadron-mass, QCD-running, and confinement-proof branches remain blocked for strong claims.",
    ]
    artifact_path = topic_dir / "Result" / "artifacts" / "nuclear_binding_source_locked_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")
    return overall


if __name__ == "__main__":
    sys.exit(0 if run_test() else 1)
