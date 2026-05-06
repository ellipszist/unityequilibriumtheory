"""
UET Casimir Effect Test
========================
Topic: 0.12 - Vacuum Energy
"""

import sys
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import platform

# --- ROBUST UET BOOTSTRAP ---
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
from pathlib import Path
current_path = Path(__file__).resolve()
root_path = ROOT_PATH
import sys
from pathlib import Path

# --- ROBUST PATH FINDER (5x4 Grid Standard) ---


# Engine Import (Dynamic)
try:
    import importlib.util

    engine_file = (
        root_path
        / "docs"
        / "topics"
        / "0.12_Vacuum_Energy_Casimir"
        / "Code"
        / "01_Engine"
        / "Engine_Vacuum.py"
    )
    spec = importlib.util.spec_from_file_location("Engine_Vacuum", engine_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    UETVacuumEngine = getattr(module, "UETVacuumEngine")
except Exception as e:
    print(f"Error loading Engine: {e}")
    sys.exit(1)

import json
import math
import numpy as np






# Standardized UET Root Path
TOPIC_DIR = root_path / "docs" / "topics" / "0.12_Vacuum_Energy_Casimir"
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_12_vacuum_energy_casimir_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"

def load_casimir_data():
    """Load Mohideen & Roy 1998 Data."""
    # Try multiple standard locations
    candidates = [
        root_path
        / "docs"
        / "topics"
        / "0.12_Vacuum_Energy_Casimir"
        / "Code"
        / "03_Research"
        / "mohideen_1998_casimir.json",
        root_path
        / "docs"
        / "topics"
        / "0.12_Vacuum_Energy_Casimir"
        / "Data"
        / "03_Research"
        / "mohideen_1998_casimir.json",
        current_path.parent / "mohideen_1998_casimir.json",
    ]

    for path in candidates:
        if path.exists():
            with open(path, "r") as f:
                return json.load(f), path

    raise FileNotFoundError("Data not found (checked standard locations)")


def file_sha256(path):
    digest = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_artifact(artifact):
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.12_Vacuum_Energy_Casimir",
        "purpose": "Source evidence intake before upgrading claims across the Casimir benchmark, geometry sensitivity, and vacuum-energy bridge branches.",
        "source_targets": [
            {
                "name": "Mohideen/Roy primary benchmark package",
                "priority": "immediate",
                "status_hint": "working_copy_benchmark_with_real_source_label",
                "evidence_entries": [
                    "working_copy_json_path",
                    "upstream_url_or_doi",
                    "transcription_note",
                    "observable_scope",
                    "unit_basis",
                    "benchmark_role",
                ],
            },
            {
                "name": "Geometry and radius sensitivity package",
                "priority": "high",
                "status_hint": "benchmark_assumption_open",
                "evidence_entries": [
                    "dataset_radius_field",
                    "model_radius_policy",
                    "sensitivity_artifact_path",
                    "geometry_scope",
                    "unit_basis",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Finite-conductivity correction package",
                "priority": "high",
                "status_hint": "heuristic_model_component",
                "evidence_entries": [
                    "formula_registry_entry",
                    "clipping_policy",
                    "material_parameter_source",
                    "sensitivity_artifact_path",
                    "failure_mode_note",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Secondary Casimir dataset package",
                "priority": "medium",
                "status_hint": "not_yet_primary_gated",
                "evidence_entries": [
                    "secondary_dataset_paths",
                    "upstream_source_package",
                    "normalization_note",
                    "artifact_path",
                    "claim_boundary_note",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Vacuum-energy and cosmology bridge package",
                "priority": "medium",
                "status_hint": "blocked_theory_branch",
                "evidence_entries": [
                    "dark_energy_anchor_source",
                    "cosmology_dataset_package",
                    "bridge_derivation_note",
                    "downstream_dependency_map",
                    "artifact_path",
                    "upgrade_requirement",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself validate a vacuum-energy or dark-energy theory.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "Mohideen/Roy primary benchmark package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "upstream_url_or_doi",
                "transcription_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The primary benchmark is a topic-local working copy with a real source label, but the upstream archival pointer and transcription audit are not yet frozen.",
        },
        {
            "name": "Geometry and radius sensitivity package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 2,
            "fields_pending": 4,
            "pending_fields": [
                "model_radius_policy",
                "sensitivity_artifact_path",
                "geometry_scope",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The current verifier uses a 200 um model radius against a 196 um dataset radius without a dedicated sensitivity artifact.",
        },
        {
            "name": "Finite-conductivity correction package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 3,
            "fields_pending": 3,
            "pending_fields": [
                "material_parameter_source",
                "sensitivity_artifact_path",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The finite-conductivity correction remains heuristic and clipped, without an independent sensitivity package.",
        },
        {
            "name": "Secondary Casimir dataset package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "upstream_source_package",
                "normalization_note",
                "artifact_path",
                "claim_boundary_note",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "Secondary Casimir datasets exist only as local working copies and are not yet primary-gated.",
        },
        {
            "name": "Vacuum-energy and cosmology bridge package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "dark_energy_anchor_source",
                "cosmology_dataset_package",
                "bridge_derivation_note",
                "downstream_dependency_map",
                "artifact_path",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The dark-energy anchor is not derived from the Casimir benchmark and there is no cosmology bridge artifact yet.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.12_Vacuum_Energy_Casimir",
        "purpose": "Readiness matrix for source-evidence review across Casimir benchmark and vacuum-energy bridge branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row has enough provenance structure for source review. It does not by itself upgrade vacuum-energy claims.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.12_Vacuum_Energy_Casimir",
        "purpose": "Claim gate for separate Casimir and vacuum-energy branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 2,
            "blocked_for_strong_claims": 4,
        },
        "branches": [
            {
                "branch": "Sphere-plate Casimir benchmark branch",
                "status": "accepted_internal_benchmark_branch",
                "allowed_usage_now": "Accepted sphere-plate Casimir benchmark compatibility branch under the current Mohideen/Roy working dataset.",
                "blocker_to_stronger_claim": "Need source-normalized archival inputs and geometry sensitivity closure before promoting the branch further.",
            },
            {
                "branch": "Boundary-force mechanism branch",
                "status": "accepted_mechanism_diagnostic_branch",
                "allowed_usage_now": "Accepted boundary-force mechanism branch for vacuum-boundary behavior only.",
                "blocker_to_stronger_claim": "Need broader material, radius, and correction sensitivity packages before using it as generalized vacuum evidence.",
            },
            {
                "branch": "Finite-conductivity correction branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Heuristic correction only.",
                "blocker_to_stronger_claim": "Need independent parameter sourcing and sensitivity artifacts beyond the clipped correction path.",
            },
            {
                "branch": "Secondary Casimir dataset branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported as a primary benchmark branch.",
                "blocker_to_stronger_claim": "Need source-locked secondary datasets and separate verifier artifacts.",
            },
            {
                "branch": "Vacuum-energy or dark-energy bridge branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need a real bridge derivation and cosmology-grade datasets rather than an observed-like anchor.",
            },
            {
                "branch": "Cosmological-constant solution claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need a dedicated cosmology artifact and cross-topic closure beyond the Casimir benchmark.",
            },
        ],
        "claim_boundary": "This gate keeps the topic at Casimir benchmark and mechanism-diagnostic status, not vacuum-energy closure.",
    }


def run_test():
    engine = UETVacuumEngine()
    print("=" * 70)
    print("UET CASIMIR EFFECT TEST")
    print("Data: Mohideen & Roy 1998")
    print("=" * 70)

    try:
        data, data_path = load_casimir_data()
    except FileNotFoundError as e:
        artifact = {
            "schema_version": "1.1",
            "topic": "0.12_Vacuum_Energy_Casimir",
            "status": "FAIL",
            "claim_class": "E - blocked, missing primary dataset",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "command": "python docs/topics/0.12_Vacuum_Energy_Casimir/Code/03_Research/Research_Casimir.py",
            "failure_reason": str(e),
        }
        write_artifact(artifact)
        print(f"FAIL: {e}")
        return False

    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)

    measurements = data["measurements"]
    separations = [m["d_nm"] for m in measurements]
    # Convert pN -> nN (1 pN = 0.001 nN)
    forces_exp = [abs(m["F_measured_pN"]) * 1e-3 for m in measurements]

    print("\n[1] CASIMIR FORCE MEASUREMENTS")
    print("-" * 50)
    print("| Separation (nm) | F_exp (nN) | F_UET (nN) | Error |")
    print("|:----------------|:-----------|:-----------|:------|")

    results = []
    rows = []
    for d, F_exp in zip(separations, forces_exp):
        F_uet = engine.calculate_physical_casimir_force(d, radius_um=200.0)
        error = abs(abs(F_uet) - F_exp) / F_exp * 100 if F_exp > 0 else 0
        print(f"| {d:15} | {F_exp:10.4f} | {F_uet:10.4f} | {error:5.1f}% |")
        results.append(error)
        rows.append(
            {
                "separation_nm": d,
                "experimental_force_nN": F_exp,
                "model_force_nN": F_uet,
                "absolute_model_force_nN": abs(F_uet),
                "relative_error_percent": error,
            }
        )

    avg_error = sum(results) / len(results)
    max_error = max(results)
    threshold = {
        "average_relative_error_percent_max": 10.0,
        "max_relative_error_percent_max": 15.0,
    }

    print(f"\nAverage Error: {avg_error:.1f}%")
    print(f"Max Error: {max_error:.1f}%")
    passed = (
        avg_error <= threshold["average_relative_error_percent_max"]
        and max_error <= threshold["max_relative_error_percent_max"]
    )
    status = "PASS" if passed else "FAIL"
    print(f"\n{status} - UET Casimir Validation")

    # --- PLOTTING FOR SHOWCASE ---
    try:
        import matplotlib.pyplot as plt

        # Get Standard Showcase Path
        from docs.core.uet_glass_box import UETPathManager

        output_dir = UETPathManager.get_result_dir(
            topic_id="0.12", experiment_name="Casimir_Validation", category="showcase"
        )

        plt.figure(figsize=(10, 6))
        plt.loglog(separations, forces_exp, "ro", label="Exp: Mohideen (1998)")
        plt.loglog(
            separations,
            [
                abs(f)
                for f in [engine.calculate_physical_casimir_force(d, 200.0) for d in separations]
            ],
            "b-",
            label="UET Prediction",
        )

        plt.xlabel("Separation d (nm)")
        plt.ylabel("Casimir Force F (nN)")
        plt.title(f"Vacuum Energy Validation: UET vs Experiment (Err: {avg_error:.1f}%)")
        plt.grid(True, which="both", ls="-", alpha=0.5)
        plt.legend()

        output_path = output_dir / "Casimir_Validation_Plot.png"
        plt.savefig(output_path, dpi=300)
        print(f"📸 Showcase Image Saved: {output_path}")

    except Exception as e:
        print(f"⚠️ Could not generate plot: {e}")

    artifact = {
        "schema_version": "1.1",
        "topic": "0.12_Vacuum_Energy_Casimir",
        "status": status,
        "claim_class": "C - source-backed internal benchmark for Casimir force only",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.12_Vacuum_Energy_Casimir/Code/03_Research/Research_Casimir.py",
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "inputs": [
            {
                "path": str(data_path.relative_to(root_path)).replace("\\", "/"),
                "sha256": file_sha256(data_path),
                "source": data.get("paper", "Mohideen & Roy, PRL 81, 4549 (1998)"),
                "geometry": data.get("geometry", "sphere-plate"),
                "material": data.get("material", "gold"),
                "sphere_radius_um_dataset": data.get("sphere_radius_um"),
                "sphere_radius_um_model": 200.0,
            }
        ],
        "formula_ids": [
            "VAC-SPHERE-PFA",
            "VAC-FINITE-CONDUCTIVITY",
        ],
        "threshold": threshold,
        "metrics": {
            "average_relative_error_percent": avg_error,
            "max_relative_error_percent": max_error,
            "point_count": len(rows),
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
        },
        "results": rows,
        "limitations": [
            "This artifact validates the topic-local sphere-plate Casimir benchmark only.",
            "It does not validate the dark-energy anchor or solve the cosmological-constant problem.",
            "The engine uses a clipped finite-conductivity correction and a 200 um model radius against a 196 um dataset radius.",
        ],
    }
    artifact["source_evidence_intake_stub"] = {
        "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(source_evidence_intake_stub, sort_keys=True).encode("utf-8")).hexdigest(),
        "source_targets": [row["name"] for row in source_evidence_intake_stub["source_targets"]],
        "claim_boundary": source_evidence_intake_stub["claim_boundary"],
    }
    artifact["source_evidence_readiness_matrix"] = {
        "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(source_evidence_readiness_matrix, sort_keys=True).encode("utf-8")).hexdigest(),
        "summary": source_evidence_readiness_matrix["summary"],
        "claim_boundary": source_evidence_readiness_matrix["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": sha256(json.dumps(branch_claim_gate, sort_keys=True).encode("utf-8")).hexdigest(),
        "summary": branch_claim_gate["summary"],
        "claim_boundary": branch_claim_gate["claim_boundary"],
    }
    artifact["interpretation"] = (
        "This artifact supports a Casimir benchmark branch and a bounded boundary-force mechanism branch. "
        "It does not validate a vacuum-energy bridge or solve the cosmological-constant problem."
    )
    write_artifact(artifact)
    print(f"Artifact written: {ARTIFACT_PATH}")

    return passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
