"""
UET Cosmology and Hubble Tension Comparison
===========================================
Internal comparison using published H0 reference values and the repository cosmology engine.
"""

import sys
import json
from pathlib import Path

def _bootstrap_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current.parent] + list(current.parents):
        if (parent / "docs" / "__init__.py").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    raise RuntimeError("Could not locate repository root containing docs package.")


_bootstrap_root()

from docs import ROOT_PATH
from docs.core.reproducibility import generate_artifact, hash_dataset, hash_file, save_artifact


root_path = ROOT_PATH
topic_path = root_path / "docs" / "topics" / "0.3_Cosmology_Hubble_Tension"
engine_path = topic_path / "Code" / "01_Engine"
if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

try:
    from Engine_Cosmology import UETCosmologyEngine
except ImportError as exc:
    print(f"CRITICAL SETUP ERROR: {exc}")
    sys.exit(1)


H0_PLANCK = 67.4
H0_PLANCK_UNCERTAINTY = 0.5
H0_SHOES = 73.04
H0_SHOES_UNCERTAINTY = 1.04
TENSION_SIGMA = 4.8
SOURCE_LOCK_PATH = topic_path / "Data" / "03_Research" / "source_lock_manifest.json"
SOURCE_EVIDENCE_INTAKE_PATH = topic_path / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = topic_path / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = topic_path / "Data" / "03_Research" / "branch_claim_gate.json"


def load_source_lock() -> dict:
    if not SOURCE_LOCK_PATH.exists():
        return {
            "status": "MISSING",
            "path": str(SOURCE_LOCK_PATH),
            "external_source_records": [],
            "derived_inputs": [],
        }
    return json.loads(SOURCE_LOCK_PATH.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def source_record_hashes(source_lock: dict) -> list[dict]:
    hashes = []
    for record_path in source_lock.get("external_source_records", []):
        path = root_path / record_path
        hashes.append(
            {
                "path": record_path,
                "sha256": hash_file(path) if path.exists() else None,
                "status": "present" if path.exists() else "missing",
            }
        )
    return hashes


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.3_Cosmology_Hubble_Tension",
        "purpose": "Source evidence intake before claim upgrades across scalar H0, bridge, high-z, and dark-energy branches.",
        "source_targets": [
            {
                "name": "Planck-SH0ES scalar H0 benchmark package",
                "priority": "immediate",
                "status_hint": "source_backed_ready",
                "evidence_entries": [
                    "planck_source_record",
                    "shoes_source_record",
                    "scalar_value_paths",
                    "unit_basis",
                    "benchmark_role",
                    "extraction_note",
                ],
            },
            {
                "name": "Fine-structure bridge constant package",
                "priority": "high",
                "status_hint": "source_backed_constant_with_derivation_gap",
                "evidence_entries": [
                    "constant_source_record",
                    "constant_surface",
                    "bridge_rule_note",
                    "unit_basis",
                    "no_fit_policy",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Redshift transition and high-z package",
                "priority": "high",
                "status_hint": "diagnostic_local_package",
                "evidence_entries": [
                    "jwst_local_path",
                    "source_provenance_note",
                    "z_crit_surface",
                    "unit_basis",
                    "diagnostic_role",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Dark-energy or vacuum-energy branch package",
                "priority": "medium",
                "status_hint": "open_problem_branch",
                "evidence_entries": [
                    "research_script_paths",
                    "failure_artifact_note",
                    "observable_scope",
                    "status_rule",
                    "benchmark_requirement",
                    "limitation_note",
                ],
            },
            {
                "name": "Full cosmology likelihood package",
                "priority": "medium",
                "status_hint": "not_implemented",
                "evidence_entries": [
                    "planck_chain_or_release_data",
                    "shoes_covariance_package",
                    "bao_sn_inputs",
                    "likelihood_code_path",
                    "artifact_path",
                    "limitation_note",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself resolve the Hubble tension or full cosmology pipeline.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "Planck-SH0ES scalar H0 benchmark package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Fine-structure bridge constant package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "independent_derivation",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The constant is source-backed, but the sqrt(alpha_em) bridge still lacks an external derivation or constraint package.",
        },
        {
            "name": "Redshift transition and high-z package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 2,
            "fields_pending": 4,
            "pending_fields": [
                "source_provenance_note",
                "z_crit_source_lock",
                "diagnostic_role",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The high-z layer is still a local diagnostic package and the redshift-transition scale is not yet source-locked.",
        },
        {
            "name": "Dark-energy or vacuum-energy branch package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 2,
            "fields_pending": 4,
            "pending_fields": [
                "failure_artifact_note",
                "status_rule",
                "benchmark_requirement",
                "limitation_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The dark-energy branch is still an open-problem lane and must stay separate from the scalar H0 benchmark.",
        },
        {
            "name": "Full cosmology likelihood package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "planck_chain_or_release_data",
                "shoes_covariance_package",
                "bao_sn_inputs",
                "likelihood_code_path",
                "artifact_path",
                "limitation_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "A full observational likelihood package is not implemented in this topic.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.3_Cosmology_Hubble_Tension",
        "purpose": "Readiness matrix for source-evidence review across cosmology benchmark and theory branches.",
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
        "topic": "0.3_Cosmology_Hubble_Tension",
        "purpose": "Claim gate for separate cosmology branches inside the topic.",
        "summary": {
            "branches_total": 5,
            "accepted_now": 1,
            "provisional_or_diagnostic": 1,
            "blocked_for_strong_claims": 3,
        },
        "branches": [
            {
                "branch": "Scalar H0 benchmark branch",
                "status": "accepted_source_backed_benchmark",
                "allowed_usage_now": "Source-backed scalar Planck-SH0ES gap benchmark only.",
                "blocker_to_stronger_claim": "Need uncertainty-aware likelihood or release-level data packaging before promotion beyond scalar benchmark status.",
            },
            {
                "branch": "Frame-coupling bridge branch",
                "status": "provisional_no_fit_bridge_with_derivation_gap",
                "allowed_usage_now": "Diagnostic no-fit coupling lane for the current scalar benchmark.",
                "blocker_to_stronger_claim": "Need derivation or independent external constraint for beta_frame = sqrt(alpha_em).",
            },
            {
                "branch": "High-z or redshift-transition branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Diagnostic-only high-z lane.",
                "blocker_to_stronger_claim": "Need source-locked JWST/high-z packaging and a verified transition-scale gate.",
            },
            {
                "branch": "Dark-energy or vacuum-energy branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Open-problem lane only.",
                "blocker_to_stronger_claim": "Need a separate artifact-backed benchmark or failure decomposition that does not piggyback on the H0 pass.",
            },
            {
                "branch": "Full cosmology resolution claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need a full Planck/BAO/SN/SH0ES likelihood pipeline and broader cosmology consistency checks.",
            },
        ],
        "claim_boundary": "This gate cannot raise the topic above the current internal scalar H0 benchmark package.",
    }


def build_hubble_claim_scope_gate(error: float, passed: bool, source_evidence_readiness_matrix: dict, branch_claim_gate: dict) -> dict:
    readiness_summary = source_evidence_readiness_matrix["summary"]
    branch_summary = branch_claim_gate["summary"]
    return {
        "schema_version": "1.0",
        "topic": "0.3_Cosmology_Hubble_Tension",
        "purpose": "Machine-readable controller separating scalar benchmark PASS from unresolved cosmology claims.",
        "controller_status": "WARN" if passed else "FAIL",
        "scalar_benchmark_gate": {
            "status": "PASS" if passed else "FAIL",
            "claim_class": "C - internal scalar published-value benchmark",
            "metric": "relative_error_percent",
            "value": float(error),
            "threshold": 20.0,
            "supports": "The fixed no-fit scalar H0 comparison lands inside the repository threshold.",
            "does_not_support": "A Planck/SH0ES likelihood replication, high-z prediction, dark-energy model, or universal cosmology resolution.",
        },
        "bridge_derivation_gate": {
            "status": "OPEN",
            "claim_class": "D - exploratory mechanism hypothesis",
            "controller_role": "blocks promotion of beta_frame = sqrt(alpha_em) from diagnostic bridge to derived cosmology relation",
            "required_evidence": [
                "derivation with units and assumptions",
                "independent external constraint or baseline comparison",
                "uncertainty-aware propagation through the H0 benchmark",
            ],
        },
        "full_likelihood_gate": {
            "status": "OPEN",
            "controller_role": "blocks resolved-Hubble-tension or full-cosmology claims",
            "required_inputs": [
                "Planck release-level likelihood or chain package",
                "SH0ES covariance or release-level likelihood package",
                "BAO/SN consistency package",
                "fixed model-vs-baseline threshold",
            ],
        },
        "blocked_exports": [
            "Hubble tension resolved",
            "validated full cosmology model",
            "dark-energy replacement",
            "high-z prediction confirmed",
            "derived beta_frame relation",
        ],
        "gate_inputs": {
            "source_evidence_summary": readiness_summary,
            "branch_claim_summary": branch_summary,
        },
        "promotion_rule": (
            "Only the scalar published-value benchmark can pass in this artifact. Stronger cosmology claims require "
            "a closed bridge derivation gate and a full likelihood/baseline gate."
        ),
    }


def run_test():
    """Run the repository Hubble-comparison benchmark."""
    print("=" * 70)
    print("UET COSMOLOGY - HUBBLE TENSION TEST")
    print("Data: Planck 2018 + SH0ES 2022")
    print("=" * 70)

    engine = UETCosmologyEngine()
    res = engine.solve_hubble_tension(H0_PLANCK, H0_SHOES)
    h0_early_uet = float(res["H0_early_uet"])
    h0_late_uet = float(res["H0_late_uet"])
    delta_h0_uet = float(res["Delta_H0"])
    beta = float(res["beta"])
    beta_source = str(res.get("beta_source", "unspecified"))
    solver_beta = float(res.get("solver_beta", beta))

    observed_delta = H0_SHOES - H0_PLANCK
    observed_delta_uncertainty = (H0_PLANCK_UNCERTAINTY**2 + H0_SHOES_UNCERTAINTY**2) ** 0.5
    error = abs(delta_h0_uet - observed_delta) / observed_delta * 100
    passed = error < 20
    source_lock = load_source_lock()
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    hubble_claim_scope_gate = build_hubble_claim_scope_gate(error, passed, source_evidence_readiness_matrix, branch_claim_gate)
    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)

    print(f"Planck 2018 (CMB): {H0_PLANCK} km/s/Mpc")
    print(f"SH0ES 2022 (local): {H0_SHOES} km/s/Mpc")
    print(f"Observed Delta H0: {observed_delta:.2f} km/s/Mpc")
    print(f"UET early value: {h0_early_uet:.2f} km/s/Mpc")
    print(f"UET late value: {h0_late_uet:.2f} km/s/Mpc")
    print(f"UET Delta H0: {delta_h0_uet:.2f} km/s/Mpc")
    print(f"Hubble frame beta: {beta:.4f} ({beta_source})")
    print(f"Generic solver beta: {solver_beta:.4e}")
    print(f"Relative error: {error:.1f}%")
    print(f"Status: {'PASS' if passed else 'FAIL'}")

    try:
        import matplotlib.pyplot as plt

        fig_dir = topic_path / "Result" / "artifacts"
        fig_dir.mkdir(parents=True, exist_ok=True)
        output_path = fig_dir / "hubble_tension_resolution.png"

        labels = ["Planck 2018", "SH0ES 2022", "UET late"]
        values = [H0_PLANCK, H0_SHOES, h0_late_uet]

        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=["#1f77b4", "#d62728", "#2ca02c"])
        plt.ylabel("Hubble Constant (km/s/Mpc)")
        plt.title("Repository Hubble Comparison")
        plt.ylim(60, 80)
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Plot saved to {output_path}")
    except Exception as exc:
        print(f"Visualization skipped: {exc}")

    artifact = generate_artifact(
        topic="0.3_Cosmology_Hubble_Tension",
        dataset_hash=hash_dataset(
            {
                "H0_PLANCK": H0_PLANCK,
                "H0_PLANCK_UNCERTAINTY": H0_PLANCK_UNCERTAINTY,
                "H0_SHOES": H0_SHOES,
                "H0_SHOES_UNCERTAINTY": H0_SHOES_UNCERTAINTY,
                "TENSION_SIGMA": TENSION_SIGMA,
                "source_lock_sha256": hash_file(SOURCE_LOCK_PATH) if SOURCE_LOCK_PATH.exists() else None,
            }
        ),
        results={
            "H0_early_uet": h0_early_uet,
            "H0_late_uet": h0_late_uet,
            "H0_planck_reference": H0_PLANCK,
            "H0_planck_uncertainty": H0_PLANCK_UNCERTAINTY,
            "H0_shoes_reference": H0_SHOES,
            "H0_shoes_uncertainty": H0_SHOES_UNCERTAINTY,
            "observed_delta_h0": observed_delta,
            "observed_delta_h0_uncertainty": observed_delta_uncertainty,
            "delta_h0_uet": delta_h0_uet,
            "delta_residual": delta_h0_uet - observed_delta,
            "hubble_frame_beta": beta,
            "hubble_frame_beta_source": beta_source,
            "generic_solver_beta": solver_beta,
            "status": "PASS" if passed else "FAIL",
            "source_evidence_readiness_summary": source_evidence_readiness_matrix["summary"],
            "branch_claim_gate_summary": branch_claim_gate["summary"],
            "hubble_claim_scope_status": hubble_claim_scope_gate["controller_status"],
        },
        config={
            "relative_error_threshold_percent": 20.0,
            "no_fitting_rule": "hubble_frame_beta is sqrt(ALPHA_EM), not optimized against H0 data",
            "source_lock_path": str(SOURCE_LOCK_PATH.relative_to(root_path)),
        },
        metrics={
        "relative_error_percent": float(error),
        "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
        "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
        "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
        "provisional_or_diagnostic_branches": branch_claim_gate["summary"]["provisional_or_diagnostic"],
    },
        thresholds={"max_relative_error_percent": 20.0},
        notes="Internal scalar H0-gap comparison artifact using published H0 reference values and source-lock records.",
    )
    artifact["input_hashes"] = {
        "source_lock_manifest": hash_file(SOURCE_LOCK_PATH) if SOURCE_LOCK_PATH.exists() else None,
        "source_records": source_record_hashes(source_lock),
    }
    artifact["source_lock"] = {
        "path": str(SOURCE_LOCK_PATH.relative_to(root_path)),
        "derived_inputs": source_lock.get("derived_inputs", []),
    }
    artifact["source_evidence_intake_stub"] = {
        "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(topic_path)).replace("\\", "/"),
        "sha256": hash_file(SOURCE_EVIDENCE_INTAKE_PATH),
        "source_targets": [row["name"] for row in source_evidence_intake_stub["source_targets"]],
        "claim_boundary": source_evidence_intake_stub["claim_boundary"],
    }
    artifact["source_evidence_readiness_matrix"] = {
        "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(topic_path)).replace("\\", "/"),
        "sha256": hash_file(SOURCE_EVIDENCE_READINESS_PATH),
        "summary": source_evidence_readiness_matrix["summary"],
        "claim_boundary": source_evidence_readiness_matrix["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(topic_path)).replace("\\", "/"),
        "sha256": hash_file(BRANCH_CLAIM_GATE_PATH),
        "summary": branch_claim_gate["summary"],
        "claim_boundary": branch_claim_gate["claim_boundary"],
    }
    artifact["hubble_claim_scope_gate"] = hubble_claim_scope_gate
    artifact["interpretation"] = (
        "This artifact supports a source-backed scalar H0 benchmark and a diagnostic no-fit frame-coupling bridge with a derivation gap. "
        "It does not validate high-z, dark-energy, or full cosmology likelihood claims."
    )
    artifact["limitations"] = [
        "The current pass is a scalar published-value benchmark, not a full cosmology pipeline replication.",
        "The sqrt(alpha_em) bridge remains a no-fit hypothesis rather than a closed derivation.",
        "High-z and dark-energy branches remain separate blocked lanes.",
        "Full cosmology resolution claims remain unsupported by the current evidence package.",
    ]
    artifact["claim_boundary"] = (
        "PASS means the scalar z=0 H0-gap benchmark is inside the fixed 20 percent gate; "
        "it is not a full Planck/SH0ES likelihood replication or a universal cosmology resolution."
    )
    artifact_path = topic_path / "Result" / "artifacts" / "hubble_comparison_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")

    return passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
