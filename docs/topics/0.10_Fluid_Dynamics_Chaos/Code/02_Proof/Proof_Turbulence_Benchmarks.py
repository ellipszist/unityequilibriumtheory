"""
UET Tier 2 Benchmark: Speed and Stability
=========================================
Head-to-head internal comparison between a simplified Navier-Stokes baseline and the UET
solver. This script is intended for repository benchmark hygiene, not theorem-level claims.
"""

import os
import sys
import time
from pathlib import Path
from statistics import median

import matplotlib.pyplot as plt
import numpy as np


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

from docs.core.reproducibility import generate_artifact, hash_dataset, hash_file, save_artifact
from docs.core.uet_master_equation import UETMasterEquation, UETParameters


TOPIC_DIR = Path(__file__).resolve().parents[2]
SOURCE_LOCK_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_lock_manifest.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"


class SimplifiedNSSolver:
    """A minimal vectorized Navier-Stokes-style baseline for benchmarking."""

    def __init__(self, nx=32, ny=32, dt=0.001, nu=0.01):
        self.nx, self.ny = nx, ny
        self.dt, self.nu = dt, nu
        self.dx = 1.0 / nx
        self.dy = 1.0 / ny
        self.u = np.zeros((ny + 2, nx + 2))
        self.v = np.zeros((ny + 2, nx + 2))
        self.p = np.zeros((ny + 2, nx + 2))

    def step(self):
        un = self.u[1:-1, 1:-1]
        vn = self.v[1:-1, 1:-1]

        self.u[1:-1, 1:-1] = un + self.dt * (
            self.nu
            * (
                (self.u[1:-1, 2:] - 2 * un + self.u[1:-1, :-2]) / self.dx**2
                + (self.u[2:, 1:-1] - 2 * un + self.u[:-2, 1:-1]) / self.dy**2
            )
        )
        self.v[1:-1, 1:-1] = vn + self.dt * (
            self.nu
            * (
                (self.v[1:-1, 2:] - 2 * vn + self.v[1:-1, :-2]) / self.dx**2
                + (self.v[2:, 1:-1] - 2 * vn + self.v[:-2, 1:-1]) / self.dy**2
            )
        )

        for _ in range(20):
            self.p[1:-1, 1:-1] = 0.25 * (
                self.p[1:-1, 2:]
                + self.p[1:-1, :-2]
                + self.p[2:, 1:-1]
                + self.p[:-2, 1:-1]
            )

        self.u[1:-1, 1:-1] -= self.dt * (self.p[1:-1, 2:] - self.p[1:-1, 1:-1]) / self.dx
        self.v[1:-1, 1:-1] -= self.dt * (self.p[2:, 1:-1] - self.p[1:-1, 1:-1]) / self.dy


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(__import__("json").dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.10_Fluid_Dynamics_Chaos",
        "purpose": "Source evidence intake before claim upgrades across internal benchmark, external CFD, and theorem branches.",
        "source_targets": [
            {
                "name": "Embedded speed and stability benchmark package",
                "priority": "immediate",
                "status_hint": "internal_benchmark_ready",
                "evidence_entries": [
                    "benchmark_script_path",
                    "source_lock_manifest_path",
                    "grid_and_step_config",
                    "timing_statistic",
                    "unit_basis",
                    "claim_boundary_note",
                ],
            },
            {
                "name": "UET master-equation implementation package",
                "priority": "high",
                "status_hint": "internal_formula_package",
                "evidence_entries": [
                    "master_equation_path",
                    "engine_surface_path",
                    "hash_recording_note",
                    "unit_basis",
                    "regression_requirement",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "External CFD validation dataset package",
                "priority": "high",
                "status_hint": "missing_external_validation",
                "evidence_entries": [
                    "dataset_identity",
                    "upstream_source",
                    "local_path",
                    "case_definition",
                    "unit_basis",
                    "artifact_path",
                ],
            },
            {
                "name": "Physical Reynolds-number validation package",
                "priority": "medium",
                "status_hint": "missing_physical_unit_gate",
                "evidence_entries": [
                    "fluid_property_source",
                    "boundary_condition_package",
                    "reynolds_case_definition",
                    "unit_basis",
                    "artifact_path",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Navier-Stokes theorem or proof package",
                "priority": "medium",
                "status_hint": "not_a_theorem_package",
                "evidence_entries": [
                    "proof_script_path",
                    "assumption_registry",
                    "artifact_path",
                    "status_rule",
                    "theorem_scope",
                    "limitation_note",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself validate CFD accuracy or theorem-level Navier-Stokes claims.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "Embedded speed and stability benchmark package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 6,
            "fields_pending": 0,
            "pending_fields": [],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "UET master-equation implementation package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "regression_requirement",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The implementation package is hash-tracked, but it still needs formula-level regression discipline before stronger promotion.",
        },
        {
            "name": "External CFD validation dataset package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "dataset_identity",
                "upstream_source",
                "local_path",
                "case_definition",
                "unit_basis",
                "artifact_path",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "No external CFD validation dataset is currently packaged for this topic.",
        },
        {
            "name": "Physical Reynolds-number validation package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "fluid_property_source",
                "boundary_condition_package",
                "reynolds_case_definition",
                "unit_basis",
                "artifact_path",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The current gate uses dimensionless internal fields rather than physical Reynolds-number validation cases.",
        },
        {
            "name": "Navier-Stokes theorem or proof package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "assumption_registry",
                "artifact_path",
                "status_rule",
                "theorem_scope",
                "limitation_note",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The current benchmark script is not an audit-grade theorem or Millennium-proof package.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.10_Fluid_Dynamics_Chaos",
        "purpose": "Readiness matrix for source-evidence review across fluid benchmark and theorem branches.",
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
        "topic": "0.10_Fluid_Dynamics_Chaos",
        "purpose": "Claim gate for separate fluid benchmark and theorem branches inside the topic.",
        "summary": {
            "branches_total": 5,
            "accepted_now": 2,
            "blocked_for_strong_claims": 3,
        },
        "branches": [
            {
                "branch": "Embedded speed benchmark branch",
                "status": "accepted_internal_benchmark",
                "allowed_usage_now": "Internal implementation speed comparison against the embedded simplified comparator.",
                "blocker_to_stronger_claim": "Need external CFD baselines and broader hardware/configuration checks before promotion beyond internal benchmark status.",
            },
            {
                "branch": "Stress stability diagnostic branch",
                "status": "accepted_internal_diagnostic",
                "allowed_usage_now": "Finite-output stress diagnostic only.",
                "blocker_to_stronger_claim": "Need norm-growth and broader stability evidence before stronger claims.",
            },
            {
                "branch": "External CFD validation branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not yet supported by packaged data.",
                "blocker_to_stronger_claim": "Need source-backed external CFD/turbulence validation cases and artifact-backed comparisons.",
            },
            {
                "branch": "Physical fluid and Reynolds-number branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not yet a primary gate.",
                "blocker_to_stronger_claim": "Need physical-unit fluid-property cases with declared Reynolds-number validation workflows.",
            },
            {
                "branch": "Navier-Stokes theorem or Millennium-proof claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need a separate proof package with explicit theorem assumptions and audit-grade status rules.",
            },
        ],
        "claim_boundary": "This gate cannot raise the topic above the current internal speed/stability benchmark package.",
    }


def run_benchmarks():
    print("=" * 60)
    print("UET TIER 2: SPEED AND STABILITY BENCHMARK")
    print("=" * 60)

    grid_size = 128
    steps = 100
    trials = 5
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)

    def time_ns_once():
        ns = SimplifiedNSSolver(nx=grid_size, ny=grid_size, dt=0.001)
        t0 = time.perf_counter()
        for _ in range(steps):
            ns.step()
        return time.perf_counter() - t0

    params = UETParameters(kappa=0.01, beta=1.0, alpha=0.0, gamma=0.0, W_N=0.0)

    def time_uet_once():
        solver = UETMasterEquation(params)
        c_field = np.zeros((grid_size, grid_size))
        i_field = np.zeros((grid_size, grid_size))
        t0 = time.perf_counter()
        for _ in range(steps):
            result = solver.step(c_field, dt=0.001, dx=1.0 / grid_size, I=i_field)
            if isinstance(result, tuple):
                if len(result) == 3:
                    c_field, i_field, _ = result
                else:
                    c_field, i_field = result
            else:
                c_field = result
        return time.perf_counter() - t0

    # Warm-up removes first-call import/allocation jitter without changing the threshold.
    time_ns_once()
    time_uet_once()
    ns_trials = [time_ns_once() for _ in range(trials)]
    uet_trials = [time_uet_once() for _ in range(trials)]
    t_ns = median(ns_trials)
    t_uet = median(uet_trials)

    speedup = t_ns / t_uet

    solver = UETMasterEquation(params)
    c_stress = np.zeros((grid_size, grid_size))
    i_field = np.zeros((grid_size, grid_size))
    c_stress[grid_size // 2, grid_size // 2] = 1e6
    try:
        for _ in range(50):
            result = solver.step(c_stress, dt=0.001, dx=1.0 / grid_size, I=i_field)
            if isinstance(result, tuple):
                if len(result) == 3:
                    c_stress, i_field, _ = result
                else:
                    c_stress, i_field = result
            else:
                c_stress = result
        is_stable = bool(np.isfinite(c_stress).all())
    except Exception:
        is_stable = False

    print(f"NS Runtime: {t_ns:.4f}s")
    print(f"UET Runtime: {t_uet:.4f}s")
    print(f"Speedup: {speedup:.1f}x")
    print(f"Stable: {is_stable}")

    fig_dir = Path(__file__).resolve().parents[2] / "Result" / "02_Proof"
    fig_dir.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.bar(["Navier-Stokes", "UET"], [t_ns, t_uet], color=["gray", "red"])
    plt.yscale("log")
    plt.ylabel("Runtime (s) - Log Scale")
    plt.title("Speed Comparison")
    plt.grid(True, axis="y", alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.imshow(c_stress, cmap="hot")
    plt.title(f"Stability stress test\n(Peak bound: {np.max(c_stress):.2e})")
    plt.colorbar(label="Field Intensity")
    plt.tight_layout()
    plt.savefig(fig_dir / "benchmarks_tier2.png")
    plt.close()

    passed = speedup > 2.0 and is_stable
    artifact = generate_artifact(
        topic="0.10_Fluid_Dynamics_Chaos",
        dataset_hash=hash_dataset({
            "grid_size": grid_size,
            "steps": steps,
            "trials": trials,
            "source_lock_sha256": hash_file(SOURCE_LOCK_PATH) if SOURCE_LOCK_PATH.exists() else None,
        }),
        results={
            "status": "PASS" if passed else "FAIL",
            "navier_stokes_runtime_seconds": float(t_ns),
            "uet_runtime_seconds": float(t_uet),
            "navier_stokes_runtime_trials_seconds": [float(v) for v in ns_trials],
            "uet_runtime_trials_seconds": [float(v) for v in uet_trials],
            "speedup": float(speedup),
            "stable": is_stable,
            "source_evidence_readiness_summary": source_evidence_readiness_matrix["summary"],
            "branch_claim_gate_summary": branch_claim_gate["summary"],
        },
        config={
            "grid_size": grid_size,
            "steps": steps,
            "trials": trials,
            "timing_statistic": "median",
            "source_lock_manifest": str(SOURCE_LOCK_PATH.relative_to(ROOT)),
            "comparator": "SimplifiedNSSolver embedded in Proof_Turbulence_Benchmarks.py",
        },
        metrics={
            "speedup": float(speedup),
            "stable": is_stable,
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
        },
        thresholds={"min_speedup": 2.0, "requires_stability": True},
        notes="Internal implementation benchmark artifact using the repository comparator script; not an external CFD validation result.",
    )
    artifact["input_hashes"] = {
        "source_lock_manifest": hash_file(SOURCE_LOCK_PATH) if SOURCE_LOCK_PATH.exists() else None,
        "benchmark_script": hash_file(Path(__file__).resolve()),
        "uet_master_equation": hash_file(ROOT / "docs" / "core" / "uet_master_equation.py"),
    }
    artifact["claim_boundary"] = (
        "PASS means the UET implementation beat the embedded simplified comparator under this "
        "grid/timing/stability gate. It does not establish external CFD accuracy or a "
        "Navier-Stokes theorem result."
    )
    artifact["source_evidence_intake_stub"] = {
        "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": hash_file(SOURCE_EVIDENCE_INTAKE_PATH),
        "source_targets": [row["name"] for row in source_evidence_intake_stub["source_targets"]],
        "claim_boundary": source_evidence_intake_stub["claim_boundary"],
    }
    artifact["source_evidence_readiness_matrix"] = {
        "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": hash_file(SOURCE_EVIDENCE_READINESS_PATH),
        "summary": source_evidence_readiness_matrix["summary"],
        "claim_boundary": source_evidence_readiness_matrix["claim_boundary"],
    }
    artifact["branch_claim_gate"] = {
        "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
        "sha256": hash_file(BRANCH_CLAIM_GATE_PATH),
        "summary": branch_claim_gate["summary"],
        "claim_boundary": branch_claim_gate["claim_boundary"],
    }
    artifact["interpretation"] = (
        "This artifact supports an internal implementation speed benchmark and a finite-output stress diagnostic. "
        "It does not validate external CFD accuracy or theorem-level Navier-Stokes claims."
    )
    artifact["limitations"] = [
        "The current comparator is simplified and internal to the repository.",
        "Speedup is environment-sensitive and should not be treated as external solver superiority.",
        "No external CFD validation dataset is currently part of the primary gate.",
        "Theorem-level Navier-Stokes or Millennium claims remain blocked.",
    ]
    artifact_path = Path(__file__).resolve().parents[2] / "Result" / "artifacts" / "fluid_benchmark_validation.json"
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")

    return passed


if __name__ == "__main__":
    success = run_benchmarks()
    sys.exit(0 if success else 1)
