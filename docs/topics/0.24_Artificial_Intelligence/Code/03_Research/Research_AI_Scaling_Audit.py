"""Topic 0.24 verification: AI scaling and sparsity audit.

This verifier is intentionally narrow. It checks the topic-local scaling-law and
MoE metadata package, records hashes, computes transparent benchmark diagnostics,
and refuses to treat the result as a proof of AI alignment or ethics.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import sys
from datetime import UTC, datetime
from pathlib import Path


def bootstrap_repo() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    raise RuntimeError("Repository root with docs/core was not found.")


ROOT = bootstrap_repo()
TOPIC = ROOT / "docs" / "topics" / "0.24_Artificial_Intelligence"
DATA = TOPIC / "Data"
ARTIFACT = TOPIC / "Result" / "artifacts" / "0_24_artificial_intelligence_verification.json"
SOURCE_EVIDENCE_INTAKE = DATA / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS = DATA / "03_Research" / "source_evidence_readiness_matrix.json"
MODEL_CLAIM_GATE = DATA / "03_Research" / "model_claim_gate.json"
SOURCE_LOCK_MANIFEST = DATA / "03_Research" / "source_lock_manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload


def find_source_target(source_lock: dict, suffix: str) -> dict:
    for item in source_lock.get("source_targets", []):
        if item.get("local_path", "").endswith(suffix):
            return item
    return {}


def fit_power_exponent(points: list[tuple[float, float]]) -> dict:
    """Fit loss ~= A * N^-alpha in log space."""
    xs = [math.log(p) for p, _ in points]
    ys = [math.log(loss) for _, loss in points]
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    denom = sum((x - x_mean) ** 2 for x in xs)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denom
    intercept = y_mean - slope * x_mean
    predictions = [math.exp(intercept + slope * x) for x in xs]
    rmse = math.sqrt(sum((pred - actual) ** 2 for pred, (_, actual) in zip(predictions, points)) / len(points))
    return {
        "alpha_fit": -slope,
        "intercept_log": intercept,
        "rmse_loss": rmse,
        "point_count": len(points),
    }


def read_gpt3_csv(path: Path) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            points.append((float(row["Parameters"]), float(row["Test_Loss"])))
    return points


def model_sparsity_table(moe_data: dict) -> list[dict]:
    rows = []
    for name, spec in moe_data["models"].items():
        total = float(spec["Total_Params"])
        active = float(spec["Active_Params"])
        rows.append(
            {
                "model": name,
                "type": spec["Type"],
                "total_params": total,
                "active_params": active,
                "active_fraction": active / total,
                "capacity_to_active_ratio": total / active,
                "context_window": spec["Context_Window"],
                "training_tokens": spec["Training_Tokens"],
                "source_note": spec["Note"],
            }
        )
    return rows


def build_source_evidence_intake_stub() -> dict:
    scaling = load_json(DATA / "03_Research" / "scaling_laws.json")
    moe_data = load_json(DATA / "03_Research" / "deepseek_moe_data.json")
    source_lock = load_json(SOURCE_LOCK_MANIFEST) if SOURCE_LOCK_MANIFEST.exists() else {}
    scaling_lock = find_source_target(source_lock, "Data/03_Research/scaling_laws.json")
    csv_lock = find_source_target(source_lock, "Data/GPT3_Scaling_Laws.csv")
    moe_lock = find_source_target(source_lock, "Data/03_Research/deepseek_moe_data.json")

    payload = {
        "schema_version": "1.0",
        "topic": "0.24_Artificial_Intelligence",
        "purpose": "Structured intake stub for upstream AI scaling and model-metadata evidence before data rewrites or stronger claims.",
        "instructions": [
            "Attach upstream URL, DOI, or arXiv identifier, local archive path, retrieval date, and extraction note before changing a working-copy dataset.",
            "Separate public metadata, estimated values, and proprietary assumptions explicitly.",
            "Do not treat this file as evidence by itself; it is an intake and tracking layer."
        ],
        "source_targets": [
            {
                "name": "Scaling-law source package",
                "priority": "immediate",
                "status": "partial",
                "evidence_fields": [
                    {
                        "field": "doi_or_arxiv_or_url",
                        "status": "complete" if scaling_lock.get("arxiv_id") or scaling_lock.get("url") or scaling.get("arxiv_id") or scaling.get("url") else "pending",
                        "value": scaling_lock.get("arxiv_id") or scaling_lock.get("url") or scaling.get("arxiv_id") or scaling.get("url", ""),
                    },
                    {
                        "field": "local_path",
                        "status": "complete",
                        "value": "docs/topics/0.24_Artificial_Intelligence/Data/03_Research/scaling_laws.json; docs/topics/0.24_Artificial_Intelligence/Data/03_Research/source_lock_manifest.json",
                    },
                    {
                        "field": "table_or_equation_identifier",
                        "status": "complete",
                        "value": "L(N) ~ (N_c / N)^alpha_N; L(D) ~ (D_c / D)^alpha_D; L(C) ~ (C_c / C)^alpha_C",
                    },
                    {
                        "field": "retrieval_date",
                        "status": "complete" if scaling_lock.get("retrieval_date") or scaling.get("retrieval_date") else "pending",
                        "value": scaling_lock.get("retrieval_date") or scaling.get("retrieval_date", ""),
                    },
                    {
                        "field": "unit_basis",
                        "status": "complete",
                        "value": scaling_lock.get("unit_system", "dimensionless exponents; parameters count; tokens count; PF-days"),
                    },
                    {
                        "field": "extraction_note",
                        "status": "complete",
                        "value": scaling_lock.get("source_note", scaling.get("source", "")),
                    },
                ],
            },
            {
                "name": "GPT-style scaling table provenance package",
                "priority": "high",
                "status": "partial",
                "evidence_fields": [
                    {
                        "field": "upstream_url_or_derivation_note",
                        "status": "complete",
                        "value": "Topic-local GPT-style working table used for a secondary log-log fit; not yet pinned to an upstream archival table.",
                    },
                    {
                        "field": "local_path",
                        "status": "complete",
                        "value": "docs/topics/0.24_Artificial_Intelligence/Data/GPT3_Scaling_Laws.csv",
                    },
                    {
                        "field": "row_origin_or_table_identifier",
                        "status": "complete",
                        "value": "5-row parameter/test-loss/FLOPs table embedded in GPT3_Scaling_Laws.csv",
                    },
                    {
                        "field": "retrieval_or_construction_date",
                        "status": "pending",
                        "value": "",
                    },
                    {
                        "field": "unit_basis",
                        "status": "complete",
                        "value": csv_lock.get("unit_system", "parameters; test loss; FLOPs"),
                    },
                    {
                        "field": "extraction_note",
                        "status": "complete",
                        "value": csv_lock.get("source_note", "Small topic-local table used only for internal alpha-fit consistency."),
                    },
                ],
            },
            {
                "name": "Model architecture metadata package",
                "priority": "high",
                "status": "partial",
                "evidence_fields": [
                    {
                        "field": "public_model_cards_or_urls",
                        "status": "pending",
                        "value": "",
                    },
                    {
                        "field": "local_path",
                        "status": "complete",
                        "value": "docs/topics/0.24_Artificial_Intelligence/Data/03_Research/deepseek_moe_data.json; docs/topics/0.24_Artificial_Intelligence/Data/03_Research/source_lock_manifest.json",
                    },
                    {
                        "field": "estimated_value_flags",
                        "status": "complete",
                        "value": "Estimated/proprietary row present: GPT-4-Turbo; public rows: Llama-3-70B, Llama-3-405B, DeepSeek-V3, Mixtral-8x7B",
                    },
                    {
                        "field": "retrieval_date",
                        "status": "pending",
                        "value": "",
                    },
                    {
                        "field": "unit_basis",
                        "status": "complete",
                        "value": moe_lock.get("unit_system", "total and active parameters; context window tokens; training tokens"),
                    },
                    {
                        "field": "extraction_note",
                        "status": "complete",
                        "value": moe_lock.get("source_note", moe_data.get("source", "")),
                    },
                ],
            },
        ],
        "claim_boundary": (
            "This intake stub is for source evidence capture only. Filling it does not by itself justify "
            "AI-law, alignment, ethics, or consciousness claim upgrades."
        ),
        "source_lock_dependencies": [target.get("local_path") for target in source_lock.get("source_targets", [])],
    }
    return write_json(SOURCE_EVIDENCE_INTAKE, payload)


def build_source_evidence_readiness_matrix(intake_stub: dict) -> dict:
    rows = []
    ready = 0
    blocked = 0
    for target in intake_stub["source_targets"]:
        pending_fields = [field["field"] for field in target["evidence_fields"] if field.get("status") != "complete"]
        fields_total = len(target["evidence_fields"])
        fields_complete = fields_total - len(pending_fields)
        row_ready = not pending_fields
        if row_ready:
            ready += 1
        else:
            blocked += 1
        rows.append(
            {
                "name": target["name"],
                "priority": target["priority"],
                "fields_total": fields_total,
                "fields_complete": fields_complete,
                "fields_pending": len(pending_fields),
                "pending_fields": pending_fields,
                "target_status": target.get("status", "pending"),
                "ready_for_source_review": row_ready,
                "blocking_reason": "" if row_ready else "One or more required evidence fields are still pending.",
            }
        )
    payload = {
        "schema_version": "1.0",
        "topic": "0.24_Artificial_Intelligence",
        "purpose": "Readiness matrix for AI scaling and model-metadata evidence before data edits or claim upgrades.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready,
            "targets_blocked_by_pending_evidence": blocked,
        },
        "readiness_rows": rows,
        "claim_boundary": (
            "This matrix is a workflow gate only. A target marked ready still requires actual source review before "
            "working-copy or claim changes."
        ),
    }
    return write_json(SOURCE_EVIDENCE_READINESS, payload)


def build_model_claim_gate() -> dict:
    payload = {
        "schema_version": "1.0",
        "topic": "0.24_Artificial_Intelligence",
        "purpose": "Claim gate for benchmark, heuristic, and exploratory AI lanes inside the topic.",
        "summary": {
            "lanes_total": 6,
            "accepted_now": 2,
            "blocked_for_strong_claims": 4,
        },
        "lanes": [
            {
                "lane": "Scaling-law benchmark",
                "status": "accepted_descriptive_only",
                "allowed_usage_now": "Internal exponent consistency benchmark from topic-local tables.",
                "blocker_to_stronger_claim": "Need source-locked scaling tables, extraction lineage, and broader benchmark replication."
            },
            {
                "lane": "Sparse architecture diagnostic",
                "status": "accepted_descriptive_only",
                "allowed_usage_now": "Active-parameter fraction comparison only.",
                "blocker_to_stronger_claim": "Need separated public versus estimated metadata and performance-normalized baselines."
            },
            {
                "lane": "alpha_N to kappa constant bridge",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Heuristic comparison only.",
                "blocker_to_stronger_claim": "Need a derived bridge or a verifier-backed proxy that clears the stated threshold."
            },
            {
                "lane": "Entropy-learning engine",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Implemented but not benchmark-validated.",
                "blocker_to_stronger_claim": "Need optimizer benchmark, seeds, baselines, and acceptance thresholds."
            },
            {
                "lane": "AI detective or cross-topic reasoning scripts",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Exploratory cross-topic tooling only.",
                "blocker_to_stronger_claim": "Need explicit dependency artifact and isolation from 0.1 galaxy-data credibility."
            },
            {
                "lane": "Alignment, ethics, consciousness, developmental AI",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Exploratory only.",
                "blocker_to_stronger_claim": "Need separate source-backed verifiers and claim-specific benchmarks."
            },
        ],
        "claim_boundary": "This gate cannot raise claim strength above the current internal scaling/sparsity benchmark evidence.",
    }
    return write_json(MODEL_CLAIM_GATE, payload)


def build_ai_claim_scope_gate(
    status: str,
    checks: dict,
    blockers: list[str],
    source_evidence_readiness: dict,
    model_claim_gate: dict,
) -> dict:
    source_summary = source_evidence_readiness.get("summary", {})
    model_summary = model_claim_gate.get("summary", {})
    return {
        "schema_version": "1.0",
        "topic": "0.24_Artificial_Intelligence",
        "controller_status": "SCALING_SPARSITY_BENCHMARK_ONLY",
        "controller_reason": (
            "The artifact supports only internal scaling-law and sparse-architecture diagnostics. "
            "Alignment, ethics, consciousness, universal intelligence, and kappa-law claims remain blocked."
        ),
        "claim_class": "C_internal_scaling_sparsity_benchmark",
        "allowed_claims_now": [
            {
                "claim": "The topic-local scaling and sparsity verifier ran and wrote an artifact.",
                "status": status,
                "artifact_role": "internal benchmark/run-contract",
                "source_evidence_readiness": "working_copy_source_referenced_not_full_archive",
            },
            {
                "claim": "MoE active-parameter fraction is lower than dense active fraction in the topic-local table.",
                "status": "PASS" if checks.get("moe_sparsity_ok") else "BLOCKED",
                "artifact_role": "architecture diagnostic",
                "source_evidence_readiness": "metadata_requires_source_normalization",
            },
            {
                "claim": "CSV scaling exponent is internally consistent with the stored alpha_N threshold.",
                "status": "PASS" if checks.get("csv_alpha_ok") else "BLOCKED",
                "artifact_role": "scaling diagnostic",
                "source_evidence_readiness": "topic_local_table_requires_lineage_review",
            },
        ],
        "blocked_claims": [
            {
                "claim": "UET derives a universal AI scaling law or alpha-kappa identity.",
                "status": "BLOCKED",
                "blocking_reason": "The alpha_N to kappa_macro bridge remains a heuristic and currently misses the provisional threshold.",
                "next_evidence_required": [
                    "derived alpha-kappa bridge",
                    "source-locked scaling corpus",
                    "threshold-clearing verifier artifact",
                ],
            },
            {
                "claim": "MoE sparsity validates intelligence, efficiency, safety, or alignment.",
                "status": "BLOCKED",
                "blocking_reason": "Active-parameter fraction is not a performance, safety, or alignment benchmark.",
                "next_evidence_required": [
                    "performance-normalized baseline",
                    "public/estimated metadata separation",
                    "task-level evaluation artifact",
                ],
            },
            {
                "claim": "UET proves AI alignment, ethics as physical law, consciousness, or developmental AI.",
                "status": "BLOCKED",
                "blocking_reason": "Those lanes have no source-backed verifier artifacts or claim-specific benchmarks.",
                "next_evidence_required": [
                    "alignment benchmark",
                    "ethics/decision criterion artifact",
                    "consciousness claim boundary and external evidence",
                ],
            },
        ],
        "blocked_export_phrases": [
            "AI alignment proved",
            "ethics as physical law verified",
            "machine consciousness validated",
            "universal intelligence law",
            "alpha equals kappa derived",
            "MoE proves efficient intelligence",
            "developmental AI solved",
        ],
        "machine_readable_next_blockers": [
            "alpha_kappa_bridge_heuristic_open",
            "scaling_source_archive_incomplete",
            "model_metadata_source_normalization_incomplete",
            "moe_sparsity_not_alignment_metric",
            "alignment_ethics_consciousness_verifiers_missing",
            "cross_topic_ai_detective_dependency_not_isolated",
        ],
        "gate_inputs": {
            "topic_status": status,
            "checks": checks,
            "blockers": blockers,
            "source_evidence_summary": source_summary,
            "model_claim_summary": model_summary,
        },
        "claim_boundary": (
            "0.24 may export only internal scaling/sparsity benchmark language. It must not export alignment, ethics, "
            "consciousness, universal-intelligence, alpha-kappa-law, or MoE-performance claims until separate gates close."
        ),
    }


def main() -> int:
    scaling_path = DATA / "03_Research" / "scaling_laws.json"
    moe_path = DATA / "03_Research" / "deepseek_moe_data.json"
    gpt3_path = DATA / "GPT3_Scaling_Laws.csv"

    scaling = load_json(scaling_path)
    moe_data = load_json(moe_path)
    csv_fit = fit_power_exponent(read_gpt3_csv(gpt3_path))
    source_evidence_intake = build_source_evidence_intake_stub()
    source_evidence_readiness = build_source_evidence_readiness_matrix(source_evidence_intake)
    model_claim_gate = build_model_claim_gate()

    alpha_n = float(scaling["constants"]["alpha_N"])
    alpha_c = float(scaling["constants"]["alpha_C"])
    kappa_macro = 0.1
    alpha_kappa_abs_delta = abs(alpha_n - kappa_macro)
    alpha_kappa_relative_delta = alpha_kappa_abs_delta / alpha_n
    csv_alpha_delta = abs(csv_fit["alpha_fit"] - alpha_n)

    sparsity_rows = model_sparsity_table(moe_data)
    dense_rows = [row for row in sparsity_rows if row["type"].lower().startswith("dense")]
    moe_rows = [row for row in sparsity_rows if "moe" in row["type"].lower()]
    min_dense_fraction = min(row["active_fraction"] for row in dense_rows)
    min_moe_fraction = min(row["active_fraction"] for row in moe_rows)

    thresholds = {
        "csv_alpha_delta_max": 0.20,
        "moe_active_fraction_must_be_below_dense": True,
        "alpha_kappa_relative_delta_warn_max": 0.25,
    }

    csv_alpha_ok = csv_alpha_delta <= thresholds["csv_alpha_delta_max"]
    moe_sparsity_ok = min_moe_fraction < min_dense_fraction
    alpha_kappa_ok = alpha_kappa_relative_delta <= thresholds["alpha_kappa_relative_delta_warn_max"]

    status = "PASS" if (csv_alpha_ok and moe_sparsity_ok and alpha_kappa_ok) else "WARN"
    blockers = []
    if not alpha_kappa_ok:
        blockers.append(
            "Kaplan alpha_N is not numerically close enough to the current kappa_macro=0.1 proxy to support a UET constant-identification claim."
        )
    if not csv_alpha_ok:
        blockers.append("Topic-local GPT3 CSV fit does not reproduce the stored alpha_N within the provisional threshold.")
    if not moe_sparsity_ok:
        blockers.append("MoE active-parameter fraction is not below the dense-model active fraction in the topic-local table.")
    checks = {
        "csv_alpha_ok": csv_alpha_ok,
        "moe_sparsity_ok": moe_sparsity_ok,
        "alpha_kappa_ok": alpha_kappa_ok,
    }
    ai_claim_scope_gate = build_ai_claim_scope_gate(
        status,
        checks,
        blockers,
        source_evidence_readiness,
        model_claim_gate,
    )

    artifact = {
        "schema_version": "1.1",
        "topic": "0.24_Artificial_Intelligence",
        "status": status,
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "command": "python docs/topics/0.24_Artificial_Intelligence/Code/03_Research/Research_AI_Scaling_Audit.py",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "claim_class": "C - internal scaling and sparsity benchmark",
        "formula_ids": [
            "AI24-SCALING-POWER-LAW",
            "AI24-UET-KAPPA-ALPHA-CHECK",
            "AI24-MOE-SPARSITY",
            "AI24-CSV-ALPHA-FIT",
        ],
        "inputs": [
            {
                "path": str(scaling_path.relative_to(ROOT)).replace("\\", "/"),
                "source": scaling.get("source", "unspecified"),
                "sha256": sha256(scaling_path),
            },
            {
                "path": str(moe_path.relative_to(ROOT)).replace("\\", "/"),
                "source": moe_data.get("source", "unspecified"),
                "sha256": sha256(moe_path),
            },
            {
                "path": str(gpt3_path.relative_to(ROOT)).replace("\\", "/"),
                "source": "topic-local GPT-3 scaling-law working table",
                "sha256": sha256(gpt3_path),
            },
            {
                "path": str(SOURCE_LOCK_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
                "source": "topic-derived AI source-lock manifest",
                "sha256": sha256(SOURCE_LOCK_MANIFEST),
            },
        ],
        "threshold": thresholds,
        "metrics": {
            "alpha_N_reference": alpha_n,
            "alpha_C_reference": alpha_c,
            "kappa_macro_proxy": kappa_macro,
            "alpha_kappa_abs_delta": alpha_kappa_abs_delta,
            "alpha_kappa_relative_delta": alpha_kappa_relative_delta,
            "csv_alpha_fit": csv_fit["alpha_fit"],
            "csv_alpha_delta": csv_alpha_delta,
            "csv_fit_rmse_loss": csv_fit["rmse_loss"],
            "min_dense_active_fraction": min_dense_fraction,
            "min_moe_active_fraction": min_moe_fraction,
        },
        "model_sparsity": sparsity_rows,
        "checks": checks,
        "blockers": blockers,
        "ai_claim_scope_gate": ai_claim_scope_gate,
        "source_evidence_intake_stub": {
            "path": str(SOURCE_EVIDENCE_INTAKE.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(SOURCE_EVIDENCE_INTAKE),
            "source_targets": [item["name"] for item in source_evidence_intake["source_targets"]],
            "claim_boundary": "This intake stub is for source evidence capture only. It does not authorize data or claim upgrades by itself.",
        },
        "source_evidence_readiness_matrix": {
            "path": str(SOURCE_EVIDENCE_READINESS.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(SOURCE_EVIDENCE_READINESS),
            "summary": source_evidence_readiness["summary"],
            "claim_boundary": "This readiness matrix is a workflow gate only. It tracks whether source evidence is still pending.",
        },
        "model_claim_gate": {
            "path": str(MODEL_CLAIM_GATE.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(MODEL_CLAIM_GATE),
            "summary": model_claim_gate["summary"],
            "claim_boundary": "This gate records diagnostic versus exploratory claim ceilings only. It cannot upgrade the topic beyond the current benchmark evidence.",
        },
        "limitations": [
            "This artifact audits topic-local scaling and architecture metadata only.",
            "It does not prove AI alignment, ethics as a physical law, consciousness, or universal intelligence dynamics.",
            "Several model metadata fields remain working-copy or estimated values and require upstream source normalization.",
        ],
    }

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")

    print("UET AI scaling/sparsity audit")
    print(f"  status: {status}")
    print(f"  alpha_N: {alpha_n:.6f}")
    print(f"  csv alpha fit: {csv_fit['alpha_fit']:.6f}")
    print(f"  |alpha_N - kappa| / alpha_N: {alpha_kappa_relative_delta:.3f}")
    print(f"  min dense active fraction: {min_dense_fraction:.4f}")
    print(f"  min MoE active fraction: {min_moe_fraction:.4f}")
    print(f"  artifact: {ARTIFACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
