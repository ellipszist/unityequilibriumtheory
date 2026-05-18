"""
UET Neutrino Physics Test against NuFIT 6.0
===========================================
Checks UET-style neutrino parameters against an extracted official NuFIT 6.0 benchmark.
"""

from __future__ import annotations

import json
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
topic_dir = root_path / "docs" / "topics" / "0.7_Neutrino_Physics"
external_json = root_path / "docs" / "data" / "external" / "particle_physics" / "nufit" / "official" / "nufit_v60_parameters_extracted.json"
provenance_json = root_path / "docs" / "data" / "external" / "particle_physics" / "nufit" / "official" / "nufit_v60_provenance_validation.json"
katrin_json = root_path / "docs" / "data" / "external" / "particle_physics" / "katrin" / "katrin_latest_results_2025.json"
source_evidence_intake_json = topic_dir / "Data" / "03_Research" / "source_evidence_intake_stub.json"
source_evidence_readiness_json = topic_dir / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
branch_claim_gate_json = topic_dir / "Data" / "03_Research" / "branch_claim_gate.json"

engine_path = topic_dir / "Code" / "01_Engine"
if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

from Engine_Mixing_Neutrino import UETNeutrinoMixingSolver
from Engine_Neutrino import UETNeutrinoSolver


def load_nufit() -> dict:
    return json.loads(external_json.read_text(encoding="utf-8"))


def load_katrin() -> dict:
    return json.loads(katrin_json.read_text(encoding="utf-8"))


def load_provenance() -> dict:
    if not provenance_json.exists():
        return {
            "schema_validation_status": "MISSING",
            "manual_review_required": True,
            "problems": ["Run docs/scripts/data/validate_nufit_v60_provenance.py"],
        }
    return json.loads(provenance_json.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def uet_geometric_angles(solver: UETNeutrinoSolver) -> dict:
    """Return the current engine angle outputs.

    Earlier versions of this verifier used a benchmark-compatible local angle package.
    That made the benchmark pass less meaningful because it was not testing the engine
    path declared in the topic docs. The verifier now checks the live engine output.
    """
    theta12, theta23, theta13, delta_cp = solver.pmns_angles_geometric()
    return {
        "theta12_deg": float(theta12),
        "theta23_deg": float(theta23),
        "theta13_deg": float(theta13),
        "delta_cp_deg": float(delta_cp),
        "source": "Engine_Neutrino.UETNeutrinoSolver.pmns_angles_geometric",
    }


def in_range(value: float, lower: float, upper: float) -> bool:
    return bool(lower <= value <= upper)


def compare_to_variant(label: str, variant: dict, geometric: dict, runtime: dict) -> dict:
    params = variant["normal_ordering"]
    results = {}
    for key in ("theta12_deg", "theta23_deg", "theta13_deg"):
        ref = params[key]
        pred = geometric[key]
        results[key] = {
            "mode": "geometric_uet",
            "predicted": pred,
            "best_fit": ref["best_fit"],
            "within_3sigma": in_range(pred, ref["3sigma_min"], ref["3sigma_max"]),
            "distance_from_best_fit": abs(pred - ref["best_fit"]),
            "range_3sigma": [ref["3sigma_min"], ref["3sigma_max"]],
        }

    splittings = {
        "delta_m21_sq_1e5_eV2": runtime["dm21_sq"] * 1e5,
        "delta_m3l_sq_1e3_eV2": runtime["dm31_sq"] * 1e3,
    }
    for key, pred in splittings.items():
        ref = params[key]
        results[key] = {
            "mode": "runtime_benchmark_param",
            "predicted": pred,
            "best_fit": ref["best_fit"],
            "within_3sigma": in_range(pred, ref["3sigma_min"], ref["3sigma_max"]),
            "distance_from_best_fit": abs(pred - ref["best_fit"]),
            "range_3sigma": [ref["3sigma_min"], ref["3sigma_max"]],
        }
    return {"label": label, "results": results}


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.7_Neutrino_Physics",
        "purpose": "Source evidence intake before claim upgrades across neutrino benchmark and theory branches.",
        "source_targets": [
            {
                "name": "NuFIT 6.0 checked-transcription benchmark package",
                "priority": "immediate",
                "status_hint": "source_backed_ready_with_transcription_caveat",
                "evidence_entries": [
                    "official_pdf_path",
                    "extracted_json_path",
                    "provenance_validation_path",
                    "variant_scope",
                    "unit_basis",
                    "transcription_note",
                ],
            },
            {
                "name": "KATRIN 2025 absolute-mass benchmark package",
                "priority": "immediate",
                "status_hint": "source_backed_ready",
                "evidence_entries": [
                    "official_html_path",
                    "extracted_json_path",
                    "observable_scope",
                    "unit_basis",
                    "benchmark_role",
                    "extraction_note",
                ],
            },
            {
                "name": "Runtime mass-splitting benchmark package",
                "priority": "high",
                "status_hint": "benchmark_fed_runtime_layer",
                "evidence_entries": [
                    "engine_param_surface",
                    "nufit_reference_path",
                    "observable_scope",
                    "unit_basis",
                    "claim_boundary_note",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Live angle-bridge derivation package",
                "priority": "high",
                "status_hint": "accepted_benchmark_gate_with_derivation_gap",
                "evidence_entries": [
                    "engine_angle_surface",
                    "benchmark_reference_path",
                    "observable_scope",
                    "unit_basis",
                    "derivation_gap_note",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Hierarchy proxy and full-sector proof package",
                "priority": "medium",
                "status_hint": "blocked_theory_branch",
                "evidence_entries": [
                    "hierarchy_proxy_surface",
                    "proof_script_path",
                    "artifact_path",
                    "status_rule",
                    "topological_invariant_requirement",
                    "limitation_note",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself prove the neutrino sector.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "NuFIT 6.0 checked-transcription benchmark package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "KATRIN 2025 absolute-mass benchmark package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Runtime mass-splitting benchmark package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "derived_from_first_principles",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The runtime splittings are benchmark-fed parameters, not first-principles outputs.",
        },
        {
            "name": "Live angle-bridge derivation package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "field_equation_derivation",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The live angle branch passes the benchmark but still lacks a first-principles derivation.",
        },
        {
            "name": "Hierarchy proxy and full-sector proof package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "proof_script_path",
                "artifact_path",
                "status_rule",
                "topological_invariant_requirement",
                "limitation_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The hierarchy selector is still a proxy and there is no audit-grade full-sector proof package.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.7_Neutrino_Physics",
        "purpose": "Readiness matrix for source-evidence review across neutrino benchmark and theory branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row has enough provenance structure for source review. It does not itself upgrade a claim.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.7_Neutrino_Physics",
        "purpose": "Claim gate for separate neutrino branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 4,
            "blocked_for_strong_claims": 2,
        },
        "branches": [
            {
                "branch": "NuFIT benchmark data branch",
                "status": "accepted_source_backed_benchmark",
                "allowed_usage_now": "Source-backed NuFIT 6.0 compatibility benchmark with checked-transcription guard.",
                "blocker_to_stronger_claim": "Need machine parsing or independent double-entry if this benchmark is promoted further.",
            },
            {
                "branch": "Live angle bridge branch",
                "status": "accepted_benchmark_gate_with_derivation_gap",
                "allowed_usage_now": "Accepted live-angle benchmark compatibility branch.",
                "blocker_to_stronger_claim": "Need a derivation from UET field equations rather than a benchmark-gated heuristic bridge.",
            },
            {
                "branch": "Runtime mass-splitting branch",
                "status": "accepted_benchmark_fed_runtime_branch",
                "allowed_usage_now": "Accepted compatibility check for benchmark-fed runtime splittings only.",
                "blocker_to_stronger_claim": "Need first-principles mass-splitting outputs rather than benchmark-fed runtime parameters.",
            },
            {
                "branch": "Absolute-mass KATRIN branch",
                "status": "accepted_bounded_model_branch",
                "allowed_usage_now": "Accepted bounded compatibility branch under the official KATRIN limit.",
                "blocker_to_stronger_claim": "Need a fuller neutrino-mass derivation beyond the compact see-saw-style construction.",
            },
            {
                "branch": "Hierarchy proxy branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Diagnostic proxy only.",
                "blocker_to_stronger_claim": "Need a real topological invariant or comparable derived hierarchy selector.",
            },
            {
                "branch": "Full neutrino-sector proof claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need closure of angle, splitting, hierarchy, and mass-generation derivations together.",
            },
        ],
        "claim_boundary": "This gate cannot raise the topic above the current neutrino benchmark-compatibility package.",
    }


def build_neutrino_claim_scope_gate(
    overall: bool,
    geometric_pass: bool,
    splitting_pass: bool,
    katrin_pass: bool,
    provenance_pass: bool,
    source_evidence_readiness_matrix: dict,
    branch_claim_gate: dict,
) -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.7_Neutrino_Physics",
        "purpose": "Machine-readable controller separating NuFIT/KATRIN benchmark PASS from full neutrino-sector claims.",
        "controller_status": "WARN" if overall else "FAIL",
        "benchmark_compatibility_gate": {
            "status": "PASS" if overall else "FAIL",
            "claim_class": "C - internal source-backed benchmark compatibility package",
            "component_status": {
                "live_angle_gate": "PASS" if geometric_pass else "FAIL",
                "runtime_splitting_gate": "PASS" if splitting_pass else "FAIL",
                "absolute_mass_katrin_gate": "PASS" if katrin_pass else "FAIL",
                "nufit_provenance_guard": "PASS" if provenance_pass else "FAIL",
            },
            "supports": "The current live angle, benchmark-fed splitting, and absolute-mass branches satisfy the declared NuFIT/KATRIN gates.",
            "does_not_support": "A first-principles neutrino mass origin, hierarchy selector, PMNS derivation, or full neutrino-sector proof.",
        },
        "derivation_gate": {
            "status": "OPEN",
            "controller_role": "blocks promotion from benchmark compatibility to derived neutrino-sector theory",
            "required_evidence": [
                "field-equation derivation for live PMNS angle bridge",
                "first-principles mass-splitting outputs rather than benchmark-fed runtime parameters",
                "uncertainty-aware propagation across angle, splitting, and absolute-mass lanes",
            ],
        },
        "hierarchy_gate": {
            "status": "BLOCKED",
            "controller_role": "blocks hierarchy and full-sector closure exports",
            "required_evidence": [
                "topological invariant or comparable derived hierarchy selector",
                "dedicated verifier artifact for hierarchy claims",
                "source-backed baseline comparison for hierarchy alternatives",
            ],
        },
        "source_pipeline_gate": {
            "status": "PARTIAL",
            "controller_role": "blocks stronger source-readiness claims for the NuFIT layer",
            "required_evidence": [
                "machine parse or independent double-entry of NuFIT official table",
                "explicit review trail for checked transcription changes",
            ],
        },
        "blocked_exports": [
            "neutrino mass origin derived",
            "full PMNS matrix proved from UET",
            "mass hierarchy resolved",
            "full neutrino-sector closure",
            "unification evidence beyond benchmark constraint",
        ],
        "gate_inputs": {
            "source_evidence_summary": source_evidence_readiness_matrix["summary"],
            "branch_claim_summary": branch_claim_gate["summary"],
        },
        "promotion_rule": (
            "Only NuFIT/KATRIN benchmark compatibility can pass in this artifact. Stronger neutrino-sector claims "
            "require closed derivation, hierarchy, and source-pipeline gates."
        ),
    }


def run_test() -> bool:
    print("=" * 72)
    print("UET NEUTRINO PHYSICS TEST - NUFIT 6.0")
    print("Data: Official NuFIT 6.0 parameter-table benchmark")
    print("=" * 72)

    dataset = load_nufit()
    provenance = load_provenance()
    katrin = load_katrin()
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    write_json(source_evidence_intake_json, source_evidence_intake_stub)
    write_json(source_evidence_readiness_json, source_evidence_readiness_matrix)
    write_json(branch_claim_gate_json, branch_claim_gate)
    solver = UETNeutrinoMixingSolver()
    runtime = solver.NUFIT_PARAMS
    mass_solver = UETNeutrinoSolver()
    geometric = uet_geometric_angles(mass_solver)
    predicted_mass_eV = mass_solver.predict_neutrino_mass()
    katrin_limit_eV = katrin["data"]["mass_limit_eV_c2"]

    variants = dataset["variants"]
    comparisons = [
        compare_to_variant("ic19_without_sk_atm", variants["ic19_without_sk_atm"], geometric, runtime),
        compare_to_variant("ic24_with_sk_atm", variants["ic24_with_sk_atm"], geometric, runtime),
    ]

    print("\n[1] GEOMETRIC ANGLE CHECKS")
    print("-" * 72)
    print("| Variant | Parameter | UET | Best fit | 3sigma range | In range |")
    print("| :-- | :-- | --: | --: | :-- | :-- |")
    for comparison in comparisons:
        for key in ("theta12_deg", "theta23_deg", "theta13_deg"):
            row = comparison["results"][key]
            print(
                f"| {comparison['label']} | {key} | {row['predicted']:.3f} | {row['best_fit']:.3f} | "
                f"{row['range_3sigma'][0]:.3f} -> {row['range_3sigma'][1]:.3f} | {row['within_3sigma']} |"
            )

    print("\n[2] MASS-SPLITTING CHECKS")
    print("-" * 72)
    print("| Variant | Parameter | Runtime | Best fit | 3sigma range | In range |")
    print("| :-- | :-- | --: | --: | :-- | :-- |")
    for comparison in comparisons:
        for key in ("delta_m21_sq_1e5_eV2", "delta_m3l_sq_1e3_eV2"):
            row = comparison["results"][key]
            print(
                f"| {comparison['label']} | {key} | {row['predicted']:.3f} | {row['best_fit']:.3f} | "
                f"{row['range_3sigma'][0]:.3f} -> {row['range_3sigma'][1]:.3f} | {row['within_3sigma']} |"
            )

    print("\n[3] DIRECT MASS-LIMIT CHECK (KATRIN 2025)")
    print("-" * 72)
    print(f"Official KATRIN upper limit: < {katrin_limit_eV:.2f} eV/c^2")
    print(f"Current UET engine mass scale: {predicted_mass_eV:.6g} eV")
    katrin_pass = predicted_mass_eV < katrin_limit_eV
    print(f"KATRIN compatibility: {'PASS' if katrin_pass else 'FAIL'}")

    print("\n[4] NUFIT PROVENANCE GUARD")
    print("-" * 72)
    provenance_pass = provenance.get("schema_validation_status") == "PASS"
    print(f"Checked-transcription provenance status: {provenance.get('schema_validation_status')}")
    print(f"Manual review required: {provenance.get('manual_review_required')}")
    if provenance.get("problems"):
        print(f"Problems: {provenance['problems']}")
    print(f"Provenance guard: {'PASS' if provenance_pass else 'FAIL'}")

    geometric_pass = all(
        any(comparison["results"][key]["within_3sigma"] for comparison in comparisons)
        for key in ("theta12_deg", "theta23_deg", "theta13_deg")
    )
    splitting_pass = all(
        any(comparison["results"][key]["within_3sigma"] for comparison in comparisons)
        for key in ("delta_m21_sq_1e5_eV2", "delta_m3l_sq_1e3_eV2")
    )
    overall = geometric_pass and splitting_pass and katrin_pass and provenance_pass
    neutrino_claim_scope_gate = build_neutrino_claim_scope_gate(
        overall,
        geometric_pass,
        splitting_pass,
        katrin_pass,
        provenance_pass,
        source_evidence_readiness_matrix,
        branch_claim_gate,
    )
    failed_angles = [
        key
        for key in ("theta12_deg", "theta23_deg", "theta13_deg")
        if not any(comparison["results"][key]["within_3sigma"] for comparison in comparisons)
    ]

    print("\n[5] INTERPRETATION")
    print("-" * 72)
    print(
        "Angles are checked as live UET engine outputs against official NuFIT 6.0 ranges.\n"
        "Mass splittings are checked separately as runtime benchmark-fed parameters, not yet as\n"
        "first-principles derivations. The direct KATRIN mass-limit check is stricter: it probes\n"
        "the absolute mass-scale engine path rather than the oscillation benchmark layer."
    )
    print(f"\nRESULT: {'PASS' if overall else 'FAIL'}")

    artifact = generate_artifact(
        topic="0.7_Neutrino_Physics",
        dataset_hash=hash_dataset(
            {
                "source_locked_reference": str(external_json.relative_to(root_path)),
                "nufit_provenance": provenance,
                "theta12": geometric["theta12_deg"],
                "theta23": geometric["theta23_deg"],
                "theta13": geometric["theta13_deg"],
                "angle_source": geometric["source"],
                "dm21_sq": runtime["dm21_sq"],
                "dm31_sq": runtime["dm31_sq"],
                "katrin_limit_eV": katrin_limit_eV,
                "predicted_mass_eV": predicted_mass_eV,
            }
        ),
        results={
            "status": "PASS" if overall else "FAIL",
            "claim_class": "C internal benchmark gate" if overall else "model-hardening blocker",
            "geometric_angles": geometric,
            "runtime_benchmark_params": {"dm21_sq": runtime["dm21_sq"], "dm31_sq": runtime["dm31_sq"]},
            "absolute_mass_scale": {
                "predicted_mass_eV": predicted_mass_eV,
                "katrin_limit_eV_c2": katrin_limit_eV,
                "passes": katrin_pass,
            },
            "comparisons": comparisons,
            "nufit_provenance": provenance,
            "geometric_pass": geometric_pass,
            "splitting_pass": splitting_pass,
            "katrin_pass": katrin_pass,
            "provenance_pass": provenance_pass,
            "source_evidence_readiness_summary": source_evidence_readiness_matrix["summary"],
            "branch_claim_gate_summary": branch_claim_gate["summary"],
            "neutrino_claim_scope_status": neutrino_claim_scope_gate["controller_status"],
            "failure_analysis": {
                "failed_live_angle_gates": failed_angles,
                "model_action": (
                    "revise or derive the live geometric angle path before using this topic "
                    "as support for mass-generation or unity-scale claims"
                )
                if failed_angles
                else "no live angle failure in this run",
                "downstream_dependency_policy": {
                    "0.17_Mass_Generation": "may cite this artifact only as benchmark compatibility and inherits the derivation gap",
                    "0.23_Unity_Scale_Link": "may cite this artifact as a constraint, not as positive unification evidence",
                    "0.0_Grand_Unification": "must carry the benchmark-gated neutrino limitation until derivations are closed",
                },
            },
        },
        config={
            "source_locked_reference": str(external_json.relative_to(root_path)),
            "nufit_provenance_reference": str(provenance_json.relative_to(root_path)),
            "katrin_source_locked_reference": str(katrin_json.relative_to(root_path)),
            "note": "NuFIT 6.0 values are maintained as a checked-transcription JSON guarded by source hashes and schema validation; the KATRIN limit is extracted from the official 2025 KATRIN results page; angle checks use live Engine_Neutrino outputs.",
        },
        metrics={
            "engine_angles_all_within_any_3sigma": geometric_pass,
            "engine_angle_fail_count": len(failed_angles),
            "runtime_splittings_all_within_any_3sigma": splitting_pass,
            "predicted_mass_eV": predicted_mass_eV,
            "katrin_limit_eV_c2": katrin_limit_eV,
            "nufit_schema_validation_status": provenance.get("schema_validation_status"),
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
            "claim_scope_controller_status": neutrino_claim_scope_gate["controller_status"],
        },
        thresholds={
            "engine_angles_within_any_3sigma": True,
            "runtime_splittings_within_any_3sigma": True,
            "predicted_mass_less_than_katrin_limit": True,
        },
        notes=(
            "This test distinguishes live UET engine angle outputs from runtime benchmark-fed mass splittings. "
            "It also checks the direct absolute-mass engine path against the official 2025 KATRIN limit. "
            "A fail constrains downstream core-theory claims until the live geometric angle path is repaired."
        ),
    )
    artifact["source_evidence_intake_stub"] = {
        "path": str(source_evidence_intake_json.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(source_evidence_intake_stub),
        "source_targets": [row["name"] for row in source_evidence_intake_stub["source_targets"]],
        "claim_boundary": source_evidence_intake_stub["claim_boundary"],
    }
    artifact["source_evidence_readiness_matrix"] = {
        "path": str(source_evidence_readiness_json.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(source_evidence_readiness_matrix),
        "summary": source_evidence_readiness_matrix["summary"],
        "claim_boundary": source_evidence_readiness_matrix["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(branch_claim_gate_json.relative_to(topic_dir)).replace("\\", "/"),
        "sha256": hash_dataset(branch_claim_gate),
        "summary": branch_claim_gate["summary"],
        "claim_boundary": branch_claim_gate["claim_boundary"],
    }
    artifact["neutrino_claim_scope_gate"] = neutrino_claim_scope_gate
    artifact["interpretation"] = (
        "This artifact supports benchmark compatibility for source-backed NuFIT and KATRIN constraints, "
        "with accepted-but-caveated angle, splitting, and absolute-mass branches. It does not prove the full neutrino sector."
    )
    artifact["limitations"] = [
        "NuFIT remains a checked-transcription benchmark layer rather than a machine-parsed official table pipeline.",
        "Live angle and runtime splitting branches remain benchmark-compatible but not first-principles derived.",
        "The absolute-mass branch is bounded by KATRIN compatibility, not closed as a full mass-generation theory.",
        "Hierarchy proxy and full neutrino-sector proof claims remain blocked.",
    ]
    artifact_path = topic_dir / "Result" / "artifacts" / "nufit_6_0_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")
    return overall


if __name__ == "__main__":
    sys.exit(0 if run_test() else 1)
