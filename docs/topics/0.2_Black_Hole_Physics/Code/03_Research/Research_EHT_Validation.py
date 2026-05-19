"""
UET Black Hole Physics Test
============================
Tests UET predictions against EHT data for:
- M87* black hole shadow
- Sgr A* black hole shadow
"""

import sys
from pathlib import Path

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


import sys
from pathlib import Path

# --- PATH SETUP (Must be FIRST) ---
from docs import ROOT_PATH

ROOT = ROOT_PATH

TOPIC_DIR = ROOT / "docs" / "topics" / "0.2_Black_Hole_Physics"
DATA_PATH = TOPIC_DIR / "Data"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"

# Core Imports
from docs.core.uet_glass_box import UETPathManager, UETMetricLogger
from docs.core.uet_parameters import G, C, M_SUN

pc_to_m = 3.085677581e16
c = C
M_sun = M_SUN

import json
import math
import numpy as np
import platform
from datetime import datetime, timezone
from hashlib import sha256


def load_eht_data():
    """Load EHT black hole data from master source."""
    with open(DATA_PATH / "03_Research" / "black_hole_data.json") as f:
        raw_data = json.load(f)

    # Transform list to dict for easy access
    data = {item["name"]: item for item in raw_data["supermassive"]}
    return data


def hash_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.2_Black_Hole_Physics",
        "purpose": "Source evidence intake before upgrading claims across EHT, GW, saturation-core, and CCBH black-hole branches.",
        "source_targets": [
            {
                "name": "EHT shadow benchmark package",
                "priority": "immediate",
                "status_hint": "working_copy_benchmark_with_real_source_labels",
                "evidence_entries": [
                    "working_copy_json_path",
                    "upstream_publication_package",
                    "observable_scope",
                    "unit_basis",
                    "hash_lock",
                    "benchmark_role",
                ],
            },
            {
                "name": "Image-domain and ray-tracing package",
                "priority": "high",
                "status_hint": "shadow_size_only_open",
                "evidence_entries": [
                    "image_domain_dataset",
                    "ray_tracing_artifact",
                    "geometry_scope",
                    "unit_basis",
                    "comparison_metric",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Saturation-core mechanism package",
                "priority": "high",
                "status_hint": "heuristic_core_scale_open",
                "evidence_entries": [
                    "core_scale_policy",
                    "internal_structure_artifact",
                    "observable_scope",
                    "unit_basis",
                    "failure_mode_note",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Gravitational-wave and ringdown package",
                "priority": "high",
                "status_hint": "secondary_lane_not_yet_primary_gated",
                "evidence_entries": [
                    "gw_dataset_paths",
                    "artifact_path",
                    "observable_scope",
                    "unit_basis",
                    "threshold_policy",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "CCBH cosmological coupling package",
                "priority": "medium",
                "status_hint": "blocked_external_data_branch",
                "evidence_entries": [
                    "shen_dataset_path",
                    "kormendy_dataset_path",
                    "external_cache_path",
                    "preprocessing_note",
                    "artifact_path",
                    "upgrade_requirement",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself validate singularity resolution, GR replacement, or CCBH cosmological coupling.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "EHT shadow benchmark package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "upstream_publication_package",
                "transcription_precision_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The EHT benchmark is still a topic-local working copy rather than a normalized upstream archive.",
        },
        {
            "name": "Image-domain and ray-tracing package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "image_domain_dataset",
                "ray_tracing_artifact",
                "geometry_scope",
                "unit_basis",
                "comparison_metric",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The current verifier checks only compact shadow-size agreement, not image-domain structure.",
        },
        {
            "name": "Saturation-core mechanism package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "core_scale_policy",
                "internal_structure_artifact",
                "observable_scope",
                "failure_mode_note",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The saturation-core path remains a heuristic diagnostic without a locked physical core scale.",
        },
        {
            "name": "Gravitational-wave and ringdown package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 2,
            "fields_pending": 4,
            "pending_fields": [
                "artifact_path",
                "observable_scope",
                "threshold_policy",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "GW/ringdown scripts exist, but they are not yet primary-gated with a declared artifact contract.",
        },
        {
            "name": "CCBH cosmological coupling package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "shen_dataset_path",
                "kormendy_dataset_path",
                "external_cache_path",
                "preprocessing_note",
                "artifact_path",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "CCBH remains blocked until its upstream datasets are archived in the shared external cache.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.2_Black_Hole_Physics",
        "purpose": "Readiness matrix for source-evidence review across black-hole benchmark and theory branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row has enough provenance structure for source review. It does not by itself upgrade black-hole or GR claims.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.2_Black_Hole_Physics",
        "purpose": "Claim gate for separate black-hole branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 2,
            "blocked_for_strong_claims": 4,
        },
        "branches": [
            {
                "branch": "EHT shadow-size benchmark branch",
                "status": "accepted_internal_benchmark_branch",
                "allowed_usage_now": "Accepted EHT shadow-size benchmark branch for M87* and Sgr A* under the compact shadow-size approximation.",
                "blocker_to_stronger_claim": "Need image-domain or ray-tracing validation before promoting beyond a size benchmark.",
            },
            {
                "branch": "Black-hole constant-and-geometry branch",
                "status": "accepted_gr_comparator_branch",
                "allowed_usage_now": "Accepted comparator branch for Schwarzschild-radius and GR-style shadow geometry bookkeeping.",
                "blocker_to_stronger_claim": "Comparator geometry does not validate a UET replacement for GR.",
            },
            {
                "branch": "Saturation-core singularity-resolution branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Heuristic diagnostic only.",
                "blocker_to_stronger_claim": "Need a locked physical core scale and a source-backed internal-structure artifact.",
            },
            {
                "branch": "Gravitational-wave and ringdown branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Secondary lane only.",
                "blocker_to_stronger_claim": "Need dedicated GW/ringdown artifacts with thresholds and source packages.",
            },
            {
                "branch": "CCBH cosmological coupling branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need archived Shen/Kormendy upstream data plus a runnable artifact in the repo.",
            },
            {
                "branch": "GR replacement or singularity-resolution claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need stronger theoretical closure and source-backed artifacts beyond the current EHT shadow benchmark.",
            },
        ],
        "claim_boundary": "This gate keeps the topic at EHT benchmark and comparator status, not black-hole theory closure.",
    }


def build_black_hole_claim_scope_gate(
    status: str,
    artifact_rows: list[dict],
    source_evidence_readiness_matrix: dict,
    branch_claim_gate: dict,
) -> dict:
    controller_status = "WARN" if status == "PASS" else "FAIL"
    max_relative_error = max(row["relative_error_percent"] for row in artifact_rows)
    return {
        "schema_version": "1.0",
        "topic": "0.2_Black_Hole_Physics",
        "controller_status": controller_status,
        "controller_reason": (
            "The compact EHT shadow-size benchmark passed, but export remains warning-gated because "
            "image-domain/ray-tracing, physical core-scale, GW/ringdown, CCBH, singularity, and GR-replacement branches are not primary-gated."
            if status == "PASS"
            else "One or more EHT shadow targets failed the declared 2-sigma benchmark gate."
        ),
        "claim_class": "C_eht_shadow_benchmark_only",
        "allowed_claims_now": [
            {
                "claim": "The compact 5.2 Rs shadow-size approximation matches the selected M87* and Sgr A* working-copy targets within the declared 2-sigma gates.",
                "status": status,
                "artifact_role": "primary EHT shadow-size benchmark",
                "metrics": {
                    "target_count": len(artifact_rows),
                    "max_relative_error_percent": max_relative_error,
                    "all_targets_within_2sigma": status == "PASS",
                },
                "source_evidence_readiness": "topic_working_copy_not_full_archive",
            },
            {
                "claim": "Schwarzschild radius and GR-style shadow geometry may be cited as comparator bookkeeping.",
                "status": "COMPARATOR_ONLY" if status == "PASS" else "BLOCKED",
                "artifact_role": "black-hole geometry comparator",
                "formula_role": "compact GR shadow approximation, not UET replacement dynamics",
                "source_evidence_readiness": "inherits_eht_working_copy",
            },
        ],
        "blocked_claims": [
            {
                "claim": "UET proves black-hole singularity resolution.",
                "status": "BLOCKED",
                "blocking_reason": "The saturation-core path is heuristic and lacks a locked physical core scale plus source-backed internal-structure artifact.",
                "next_evidence_required": [
                    "physical core-scale definition",
                    "internal-structure artifact",
                    "independent mathematical or numerical stability review",
                ],
            },
            {
                "claim": "UET replaces GR for black holes or validates full black-hole imaging.",
                "status": "BLOCKED",
                "blocking_reason": "The primary gate is a compact angular-size benchmark, not image-domain ray tracing or a GR replacement test.",
                "next_evidence_required": [
                    "ray-tracing artifact",
                    "image-domain EHT comparison",
                    "metric/baseline comparison against GR",
                ],
            },
            {
                "claim": "UET validates GW/ringdown or CCBH cosmological coupling.",
                "status": "BLOCKED",
                "blocking_reason": "GW/ringdown and CCBH branches lack archived upstream data, thresholds, and primary verifier artifacts.",
                "next_evidence_required": [
                    "GW/ringdown source package and thresholds",
                    "archived Shen/Kormendy upstream files",
                    "runnable CCBH artifact in the repository",
                ],
            },
        ],
        "blocked_export_phrases": [
            "black-hole singularity resolved",
            "GR replacement validated",
            "EHT image-domain validation",
            "ringdown validated",
            "CCBH cosmological coupling proven",
            "black-hole information problem solved",
        ],
        "source_evidence_summary": source_evidence_readiness_matrix["summary"],
        "branch_claim_gate_summary": branch_claim_gate["summary"],
        "machine_readable_next_blockers": [
            "eht_ray_tracing_artifact_missing",
            "physical_core_scale_missing",
            "internal_structure_artifact_missing",
            "gw_ringdown_artifact_missing",
            "ccbh_upstream_archive_missing",
            "gr_replacement_theory_gate_missing",
        ],
        "claim_boundary": (
            "A PASS artifact supports only selected EHT shadow-size benchmarking and comparator geometry. "
            "It does not prove singularity resolution, replace GR, validate image-domain EHT data, validate "
            "GW/ringdown physics, prove CCBH coupling, or solve black-hole information problems."
        ),
    }


# --- DELEGATE MATH TO ENGINE ---
# Local math removed: schwarzschild_radius, shadow_radius, angular_size_uas


def run_test():
    """Run black hole physics tests."""
    print("=" * 60)
    print("UET BLACK HOLE PHYSICS TEST")
    print("Data: Event Horizon Telescope (M87*, Sgr A*)")
    print("Data: Event Horizon Telescope (M87*, Sgr A*)")
    print("=" * 60)

    # Initialize Standard Logger
    # This automatically creates: /Result/{timestamp}_EHT_Validation/
    # Initialize Standard Logger (V2.1 Showcase)
    result_dir_base = UETPathManager.get_result_dir(
        topic_id="0.2", experiment_name="EHT_Validation", category="showcase"
    )
    logger = UETMetricLogger("EHT_Validation", topic_id="0.2", category="showcase")

    # Save Metadata
    logger.set_metadata(
        {
            "data_source": "Event Horizon Telescope (EHT)",
            "targets": ["M87*", "Sgr A*"],
            "method": "UET_Schwarzschild_Shadow",
            "parameters": {"G": G, "c": c},
        }
    )

    print(f"\\n📂 Logging detailed results to: {logger.run_dir}")

    data = load_eht_data()
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)
    results = []
    artifact_rows = []

    # Initialize Engine
    if "UETBlackHoleSolver" not in globals():
        import importlib.util

        topic_dir_path = Path(__file__).resolve().parent.parent.parent
        engine_path = topic_dir_path / "Code" / "01_Engine" / "Engine_BlackHole.py"
        if engine_path.exists():
            spec = importlib.util.spec_from_file_location("Engine_BlackHole", str(engine_path))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            UETBlackHoleSolver = mod.UETBlackHoleSolver
        else:
            print("CRITICAL: Engine not found")
            return False

    # Initialize with default params (Room Temp Landauer or Unitary)
    solver = UETBlackHoleSolver()

    # Test 1: M87* Shadow
    print("\n[1] M87* Black Hole Shadow")
    print("-" * 40)

    m87 = data["M87*"]
    M_m87 = m87["mass_solar"]
    d_m87 = m87["distance_Mpc"] * 1e6 * pc_to_m  # Mpc to m
    theta_obs = m87["shadow_uas"]
    theta_err = m87["shadow_error_uas"]

    r_s = solver.compute_schwarzschild_radius(M_m87)
    # Note: Engine returns Diameter for shadow
    d_shadow = solver.compute_shadow_diameter(r_s)
    theta_uet = solver.compute_angular_size_uas(d_shadow, d_m87)

    error = abs(theta_uet - theta_obs) / theta_obs * 100

    print(f"  Mass:     {M_m87:.1e} M☉")
    print(f"  Distance: {m87['distance_Mpc']} Mpc")
    print(f"  Observed: {theta_obs} ± {theta_err} μas")
    print(f"  UET:      {theta_uet:.1f} μas")
    print(f"  Error:    {error:.1f}%")

    passed = abs(theta_uet - theta_obs) <= 2 * theta_err  # 2σ
    results.append(("M87* Shadow", error, passed))
    artifact_rows.append(
        {
            "target": "M87*",
            "mass_solar": M_m87,
            "distance_m": d_m87,
            "observed_shadow_uas": theta_obs,
            "observed_error_uas": theta_err,
            "predicted_shadow_uas": theta_uet,
            "relative_error_percent": error,
            "within_2sigma": bool(passed),
        }
    )
    print(f"  {'✅ PASS' if passed else '❌ FAIL'}")

    # Test 2: Sgr A* Shadow
    print("\n[2] Sgr A* Black Hole Shadow")
    print("-" * 40)

    sgra = data["Sgr A*"]
    M_sgra = sgra["mass_solar"]
    d_sgra = sgra["distance_kpc"] * 1e3 * pc_to_m  # kpc to m
    theta_obs_sgra = sgra["shadow_uas"]
    theta_err_sgra = sgra["shadow_error_uas"]

    r_s_sgra = solver.compute_schwarzschild_radius(M_sgra)
    d_shadow_sgra = solver.compute_shadow_diameter(r_s_sgra)
    theta_uet_sgra = solver.compute_angular_size_uas(d_shadow_sgra, d_sgra)

    error_sgra = abs(theta_uet_sgra - theta_obs_sgra) / theta_obs_sgra * 100

    print(f"  Mass:     {M_sgra:.1e} M☉")
    print(f"  Distance: {sgra['distance_kpc']} kpc")
    print(f"  Observed: {theta_obs_sgra} ± {theta_err_sgra} μas")
    print(f"  UET:      {theta_uet_sgra:.1f} μas")
    print(f"  Error:    {error_sgra:.1f}%")

    passed_sgra = abs(theta_uet_sgra - theta_obs_sgra) <= 2 * theta_err_sgra
    results.append(("Sgr A* Shadow", error_sgra, passed_sgra))
    artifact_rows.append(
        {
            "target": "Sgr A*",
            "mass_solar": M_sgra,
            "distance_m": d_sgra,
            "observed_shadow_uas": theta_obs_sgra,
            "observed_error_uas": theta_err_sgra,
            "predicted_shadow_uas": theta_uet_sgra,
            "relative_error_percent": error_sgra,
            "within_2sigma": bool(passed_sgra),
        }
    )
    print(f"  {'✅ PASS' if passed_sgra else '❌ FAIL'}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed_count = sum(1 for _, _, p in results if p)
    total = len(results)

    for name, error, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}: {error:.1f}% error")

    print(f"\nResult: {passed_count}/{total} PASSED")
    print("=" * 60)
    artifact_status = "PASS" if passed_count == total else "FAIL"
    black_hole_claim_scope_gate = build_black_hole_claim_scope_gate(
        artifact_status,
        artifact_rows,
        source_evidence_readiness_matrix,
        branch_claim_gate,
    )

    artifact = {
        "schema_version": "1.1",
        "topic": "0.2_Black_Hole_Physics",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.2_Black_Hole_Physics/Code/03_Research/Research_EHT_Validation.py",
        "status": artifact_status,
        "claim_class": "C internal benchmark",
        "inputs": [
            {
                "path": str((DATA_PATH / "03_Research" / "black_hole_data.json").relative_to(TOPIC_DIR)),
                "sha256": hash_file(DATA_PATH / "03_Research" / "black_hole_data.json"),
                "role": "EHT shadow benchmark working copy",
            }
        ],
        "thresholds": {
            "per_target": "abs(predicted_shadow_uas - observed_shadow_uas) <= 2 * observed_error_uas"
        },
        "metrics": {
            "passed_targets": passed_count,
            "total_targets": total,
            "all_targets_within_2sigma": passed_count == total,
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
            "blocked_claim_exports": len(black_hole_claim_scope_gate["blocked_export_phrases"]),
        },
        "results": artifact_rows,
        "limitations": [
            "Uses compact GR shadow diameter approximation D_shadow = 5.2 Rs.",
            "Topic-local EHT data package is a working copy, not a fully normalized upstream archive.",
            "This artifact does not prove singularity resolution or a GR replacement.",
        ],
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy_version": np.__version__,
        },
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
    artifact["black_hole_claim_scope_gate"] = black_hole_claim_scope_gate
    artifact["interpretation"] = (
        "This artifact supports an EHT shadow-size benchmark branch and a bounded black-hole geometry comparator branch. "
        "It does not validate singularity resolution, GR replacement, or CCBH cosmological coupling."
    )
    artifact_path = TOPIC_DIR / "Result" / "artifacts" / "0_2_black_hole_physics_verification.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Artifact saved to {artifact_path}")

    # --- VISUALIZATION ---
    # Delegated to Code/05_Visualization/Vis_BlackHole_Signature.py
    print("  [Note] Run Vis_BlackHole_Signature.py for EHT shadow plots.")

    return passed_count == total

    # Save Final Report
    logger.log_step(
        step=1,
        time_val=1.0,
        omega=1.0,
        entropy=0.0,
        extra_metrics={"Passed": passed_count, "Total": total},
    )
    logger.save_report()

    return passed_count == total


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
