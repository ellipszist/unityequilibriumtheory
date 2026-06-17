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
SEMF_COEFFICIENT_GATE_PATH = data_dir / "semf_coefficient_provenance_gate.json"
PDG_HADRON_QCD_MAPPING_GATE_PATH = data_dir / "pdg_hadron_qcd_source_mapping_gate.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def binding_per_nucleon(be_kev: float, a: int) -> float:
    return (be_kev / 1000.0) / a


def relative_error_percent(predicted: float, observed: float) -> float:
    return abs(predicted - observed) / observed * 100 if observed else 0.0


def summarize_errors(errors: list[float]) -> dict:
    if not errors:
        return {
            "count": 0,
            "mean_error_percent": None,
            "median_error_percent": None,
            "max_error_percent": None,
        }
    return {
        "count": len(errors),
        "mean_error_percent": statistics.fmean(errors),
        "median_error_percent": statistics.median(errors),
        "max_error_percent": max(errors),
    }


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
                "status_hint": "source_exists_not_integrated",
                "evidence_entries": [
                    "doi_or_url",
                    "local_path",
                    "table_or_review_identifier",
                    "retrieval_date",
                    "unit_basis",
                    "extraction_note",
                    "source_mapping_gate",
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
            "fields_total": 7,
            "fields_complete": 5,
            "fields_pending": 2,
            "pending_fields": [
                "extraction_note",
                "verifier_integration",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "PDG 2025 SQLite exists and a source-mapping gate identifies quark and hadron records, but topic 0.5 hadron/QCD scripts still do not read that package.",
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
            "blocking_reason": "The QCD branch still has unresolved alpha_s source mapping and an open alpha_s_uet_v2 data-shape bug.",
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


def build_semf_coefficient_provenance_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.5_Nuclear_Binding_Hadrons",
        "purpose": "Machine-readable provenance gate for SEMF coefficients used by Engine_Nuclear_Binding.py.",
        "controller_status": "BLOCKED_FOR_PARAMETER_FREE_CLAIMS",
        "claim_boundary": (
            "The current nuclear-binding engine may be described as a checked-local SEMF baseline plus "
            "heuristic correction workflow. It must not be described as parameter-free or first-principles "
            "until the SEMF coefficient source package is locked."
        ),
        "code_surface": "Code/01_Engine/Engine_Nuclear_Binding.py",
        "coefficients": [
            {
                "symbol": "a_vol",
                "term": "volume",
                "value": 15.75,
                "unit": "MeV",
                "source_status": "checked_local_reference",
                "source_note": "Hardcoded in engine with only a broad Wapstra/Nuclear Physics A comment; no topic-local source record pins this exact value.",
            },
            {
                "symbol": "a_surf",
                "term": "surface",
                "value": 17.8,
                "unit": "MeV",
                "source_status": "checked_local_reference",
                "source_note": "Hardcoded in engine with only a broad Wapstra/Nuclear Physics A comment; no topic-local source record pins this exact value.",
            },
            {
                "symbol": "a_coul",
                "term": "coulomb",
                "value": 0.711,
                "unit": "MeV",
                "source_status": "checked_local_reference",
                "source_note": "Hardcoded in engine with only a broad Wapstra/Nuclear Physics A comment; no topic-local source record pins this exact value.",
            },
            {
                "symbol": "a_asym",
                "term": "asymmetry",
                "value": 23.7,
                "unit": "MeV",
                "source_status": "checked_local_reference",
                "source_note": "Hardcoded in engine with only a broad Wapstra/Nuclear Physics A comment; no topic-local source record pins this exact value.",
            },
            {
                "symbol": "a_pair",
                "term": "pairing",
                "value": 11.18,
                "unit": "MeV",
                "source_status": "checked_local_reference",
                "source_note": "Hardcoded in engine with only a broad Wapstra/Nuclear Physics A comment; no topic-local source record pins this exact value.",
            },
        ],
        "correction_terms": [
            {
                "symbol": "beta_nuc",
                "term": "UET entropy correction",
                "current_gate_value": 0.0,
                "unit": "dimensionless",
                "source_status": "disabled_in_current_strict_binding_subset",
                "source_note": "The primary strict binding gate calls binding_energy_components(beta_nuc=0.0), so this term is diagnostic-ready but not active in the saved strict benchmark until rerun.",
            },
            {
                "symbol": "yukawa_prefactor",
                "term": "Yukawa additive prefactor",
                "value": 10.0,
                "unit": "MeV-like scale before per-nucleus multiplication",
                "source_status": "heuristic_bridge",
                "source_note": "The coefficient and additive placement are not source-locked and require sensitivity review before any stronger mechanism claim.",
            },
            {
                "symbol": "r0",
                "term": "nuclear radius scale",
                "value": 1.25,
                "unit": "fm",
                "source_status": "checked_local_reference",
                "source_note": "Used in the Yukawa correction; source record and uncertainty policy are not yet pinned.",
            },
            {
                "symbol": "m_pion",
                "term": "pion mass convention",
                "value": 139.57,
                "unit": "MeV",
                "source_status": "checked_local_reference",
                "source_note": "Close to charged-pion mass convention, but not currently read from the downloaded PDG 2025 SQLite source.",
            },
            {
                "symbol": "hbar_c",
                "term": "conversion constant",
                "value": 197.33,
                "unit": "MeV fm",
                "source_status": "checked_local_reference",
                "source_note": "Rounded local constant; should be reconciled with shared constants policy before precision claims.",
            },
        ],
        "required_to_close": [
            "Create a source record or reference package that pins the exact SEMF coefficient set and edition used.",
            "Decide whether the Yukawa term is a baseline nuclear-physics correction, a UET bridge term, or a separate diagnostic lane.",
            "Add uncertainty or sensitivity policy for SEMF coefficients and heuristic correction terms.",
        ],
        "allowed_usage_now": [
            "Internal selected-subset benchmark with explicit SEMF baseline dependency.",
            "Diagnostic decomposition of SEMF-only versus SEMF-plus-correction behavior after verifier rerun.",
        ],
        "blocked_usage": [
            "parameter-free nuclear-binding claim",
            "first-principles derivation of nuclear binding",
            "general strong-force theory claim",
            "claim that UET alone explains the selected-subset pass without SEMF baseline support",
        ],
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


def build_nuclear_claim_scope_gate(
    overall: bool,
    error_distribution: dict,
    semf_decomposition: dict,
    semf_coefficient_gate: dict,
    source_evidence_readiness_matrix: dict,
    branch_claim_gate: dict,
    light_excluded: list[str],
) -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.5_Nuclear_Binding_Hadrons",
        "purpose": "Machine-readable controller separating strict selected-subset PASS from broader nuclear, hadron, QCD, and confinement claims.",
        "controller_status": "WARN" if overall else "FAIL",
        "heavy_subset_gate": {
            "status": "PASS" if overall else "FAIL",
            "claim_class": "C - internal source-backed selected-subset benchmark",
            "metric": "heavy_max_error_percent",
            "value": error_distribution["heavy_max_error_percent"],
            "threshold": 15.0,
            "supports": "The selected heavy-nucleus AME2020 subset satisfies the repository threshold.",
            "does_not_support": "A full AME2020-table pass, a light-nuclei model, QCD running, hadron masses, or confinement proof.",
        },
        "proton_radius_anchor_gate": {
            "status": "PASS" if overall else "FAIL",
            "claim_class": "C - benchmark-anchor compatibility check",
            "supports": "The current engine output is compatible with the proton-radius benchmark threshold.",
            "does_not_support": "An independently derived proton-radius prediction.",
        },
        "full_table_gate": {
            "status": "DIAGNOSTIC_ONLY",
            "controller_role": "blocks broad AME2020-table pass claims",
            "required_evidence": [
                "fixed full-table acceptance threshold",
                "heavy/light split metrics treated as separate gates",
                "uncertainty and data-quality policy for all parsed rows",
            ],
        },
        "semf_decomposition_gate": {
            "status": "PRESENT_DIAGNOSTIC",
            "controller_role": "prevents the selected-subset PASS from hiding the SEMF baseline contribution",
            "claim_class": "C - internal diagnostic decomposition",
            "supports": "The artifact reports SEMF-only and SEMF-plus-correction residuals for the selected subset.",
            "does_not_support": "A parameter-free UET derivation or a source-locked SEMF coefficient package.",
            "metrics": {
                "heavy_semf_only_mean_error_percent": semf_decomposition["heavy_semf_only"]["mean_error_percent"],
                "heavy_total_mean_error_percent": semf_decomposition["heavy_total"]["mean_error_percent"],
                "heavy_mean_error_delta_percent_points": semf_decomposition["heavy_mean_error_delta_percent_points"],
            },
            "still_required": [
                "source-locked SEMF coefficient provenance",
                "fixed rule for whether Yukawa is baseline physics or UET correction",
                "uncertainty and data-quality policy for all parsed rows",
            ],
            "coefficient_gate_status": semf_coefficient_gate["controller_status"],
        },
        "light_nuclei_gate": {
            "status": "EXCLUDED_FROM_PASS",
            "excluded_cases": light_excluded,
            "controller_role": "blocks using heavy-nucleus PASS as a light-nuclei claim",
        },
        "qcd_hadron_confinement_gate": {
            "status": "BLOCKED",
            "controller_role": "blocks QCD running, hadron mass, and confinement exports",
            "required_evidence": [
                "source-locked quark and hadron inputs",
                "fixed QCD-running benchmark with data-shape bug resolved",
                "dedicated hadron-mass verifier artifact",
                "audit-grade confinement proof pass/fail contract",
            ],
        },
        "blocked_exports": [
            "full AME2020 nuclear-binding pass",
            "light-nuclei validation",
            "general QCD derivation",
            "hadron mass model validation",
            "formal confinement proof",
            "complete strong-force theory",
        ],
        "gate_inputs": {
            "source_evidence_summary": source_evidence_readiness_matrix["summary"],
            "branch_claim_summary": branch_claim_gate["summary"],
            "semf_coefficient_status": semf_coefficient_gate["controller_status"],
        },
        "promotion_rule": (
            "Only the selected heavy-nucleus subset and proton-radius anchor compatibility can pass here. "
            "Full-table, light-nuclei, QCD, hadron, and confinement claims require separate closed gates."
        ),
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
    semf_coefficient_gate = build_semf_coefficient_provenance_gate()
    pdg_hadron_qcd_mapping_gate = load_json(PDG_HADRON_QCD_MAPPING_GATE_PATH)
    branch_claim_gate = build_branch_claim_gate()

    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(SEMF_COEFFICIENT_GATE_PATH, semf_coefficient_gate)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)

    print("\n[1] BINDING ENERGY CHECKS")
    print("-" * 72)
    print("| Nucleus | A | Z | Obs BE/A | UET BE/A | Error | Heavy-nucleus gate |")
    print("| :-- | --: | --: | --: | --: | --: | :-- |")

    comparisons = {}
    errors = []
    heavy_errors = []
    semf_errors = []
    heavy_semf_errors = []
    correction_deltas = []
    heavy_correction_deltas = []
    light_excluded = []
    heavy_pass = True
    heavy_count = 0
    for symbol, row in ame["data"].items():
        a = row["A"]
        z = row["Z"]
        obs = binding_per_nucleon(row["BE_keV"], a)
        components = engine.binding_energy_components(a, z, beta_nuc=0.0)
        pred = components["total_mev"] / a
        semf_pred = components["semf_mev"] / a
        entropy_pred = components["uet_entropy_mev"] / a
        yukawa_pred = components["yukawa_mev"] / a
        err = relative_error_percent(pred, obs)
        semf_err = relative_error_percent(semf_pred, obs)
        correction_delta = err - semf_err
        heavy_gate = a >= 16
        if heavy_gate:
            heavy_count += 1
            heavy_pass = heavy_pass and (err < 15.0)
            heavy_errors.append(err)
            heavy_semf_errors.append(semf_err)
            heavy_correction_deltas.append(correction_delta)
        else:
            light_excluded.append(symbol)
        errors.append(err)
        semf_errors.append(semf_err)
        correction_deltas.append(correction_delta)
        comparisons[symbol] = {
            "A": a,
            "Z": z,
            "observed_be_per_a_mev": obs,
            "semf_only_be_per_a_mev": semf_pred,
            "uet_entropy_correction_per_a_mev": entropy_pred,
            "yukawa_correction_per_a_mev": yukawa_pred,
            "predicted_be_per_a_mev": pred,
            "semf_only_relative_error_percent": semf_err,
            "relative_error_percent": err,
            "correction_error_delta_percent_points": correction_delta,
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
    semf_decomposition = {
        "semf_coefficient_status": "checked_local_reference_not_source_locked",
        "correction_policy": "Current selected-subset verifier calls binding_energy_components(beta_nuc=0.0); UET entropy is zero in this gate, while the Yukawa term remains an additive heuristic correction.",
        "all_semf_only": summarize_errors(semf_errors),
        "all_total": summarize_errors(errors),
        "heavy_semf_only": summarize_errors(heavy_semf_errors),
        "heavy_total": summarize_errors(heavy_errors),
        "all_mean_error_delta_percent_points": (
            statistics.fmean(correction_deltas) if correction_deltas else None
        ),
        "heavy_mean_error_delta_percent_points": (
            statistics.fmean(heavy_correction_deltas) if heavy_correction_deltas else None
        ),
        "yukawa_term_status": "heuristic_bridge_in_current_engine",
        "uet_entropy_term_status": "disabled_for_current strict binding subset because beta_nuc=0.0 in binding_energy_per_nucleon",
    }
    nuclear_claim_scope_gate = build_nuclear_claim_scope_gate(
        overall,
        error_distribution,
        semf_decomposition,
        semf_coefficient_gate,
        source_evidence_readiness_matrix,
        branch_claim_gate,
        light_excluded,
    )
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
            "semf_decomposition": semf_decomposition,
            "worst_cases": worst_cases,
            "proton_radius": {
                "predicted_fm": rp_pred,
                "observed_fm": rp_obs,
                "relative_error_percent": rp_err,
                "passes": rp_pass,
            },
            "heavy_nuclei_all_pass": heavy_pass,
            "source_evidence_readiness_summary": source_evidence_readiness_matrix["summary"],
            "semf_coefficient_gate_status": semf_coefficient_gate["controller_status"],
            "pdg_hadron_qcd_mapping_gate_status": pdg_hadron_qcd_mapping_gate["controller_status"],
            "branch_claim_gate_summary": branch_claim_gate["summary"],
            "nuclear_claim_scope_status": nuclear_claim_scope_gate["controller_status"],
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
            "heavy_semf_only_mean_error_percent": semf_decomposition["heavy_semf_only"]["mean_error_percent"],
            "heavy_total_mean_error_percent": semf_decomposition["heavy_total"]["mean_error_percent"],
            "heavy_mean_error_delta_percent_points": semf_decomposition["heavy_mean_error_delta_percent_points"],
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
            "semf_coefficient_gate_blocked": semf_coefficient_gate["controller_status"] != "PASS",
            "pdg_hadron_qcd_mapping_gate_blocked": pdg_hadron_qcd_mapping_gate["controller_status"] != "PASS",
            "claim_scope_controller_status": nuclear_claim_scope_gate["controller_status"],
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
    artifact["semf_coefficient_provenance_gate"] = {
        "path": str(SEMF_COEFFICIENT_GATE_PATH.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(semf_coefficient_gate),
        "controller_status": semf_coefficient_gate["controller_status"],
        "claim_boundary": semf_coefficient_gate["claim_boundary"],
    }
    artifact["pdg_hadron_qcd_source_mapping_gate"] = {
        "path": str(PDG_HADRON_QCD_MAPPING_GATE_PATH.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(pdg_hadron_qcd_mapping_gate),
        "controller_status": pdg_hadron_qcd_mapping_gate["controller_status"],
        "claim_boundary": pdg_hadron_qcd_mapping_gate["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(branch_claim_gate),
        "summary": branch_claim_gate["summary"],
        "claim_boundary": branch_claim_gate["claim_boundary"],
    }
    artifact["nuclear_claim_scope_gate"] = nuclear_claim_scope_gate
    artifact["interpretation"] = (
        "This artifact supports a source-backed heavy-nucleus subset benchmark and a proton-radius "
        "anchor-compatibility check. It does not validate light nuclei, hadron masses, QCD running, "
        "or confinement claims as audit-grade passes."
    )
    artifact["limitations"] = [
        "The strict pass/fail gate applies only to selected heavy nuclei plus proton-radius compatibility.",
        "Light nuclei remain diagnostic and can fail badly outside the liquid-drop validation regime.",
        "The proton-radius path is still benchmark-anchor behavior, not an independent prediction.",
        "The SEMF baseline versus correction decomposition is now reported, but SEMF coefficient provenance remains checked-local rather than source-locked.",
        "Hadron-mass, QCD-running, and confinement-proof branches remain blocked for strong claims.",
    ]
    artifact_path = topic_dir / "Result" / "artifacts" / "nuclear_binding_source_locked_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")
    return overall


if __name__ == "__main__":
    sys.exit(0 if run_test() else 1)
