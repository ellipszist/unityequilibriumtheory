"""
Download Real Superconductor Critical Temperature Data
=======================================================
Sources:
1. NIMS SuperCon Database (MatNavi)
2. UCI Machine Learning Database (Hamidieh)
3. MIT Experimental Data

References:
- McMillan equation: Tc = (Î˜D/1.45) * exp(-1.04(1+Î»)/(Î»-Î¼*(1+0.62Î»)))
- Allen-Dynes modification for strong coupling
- BCS theory for conventional superconductors

Updated: 2026-01-02
"""

import json
import os
from pathlib import Path
import platform
import sys
from datetime import datetime, timezone
from hashlib import sha256

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


TOPIC_DIR = Path("docs/topics/0.4_Superconductivity_Superfluids")
DATA_DIR = TOPIC_DIR / "Data" / "03_Research"
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_4_superconductivity_superfluids_verification.json"
SOURCE_LOCK_PATH = DATA_DIR / "source_lock_manifest.json"
COMPREHENSIVE_DATA_PATH = DATA_DIR / "comprehensive_superconductor_data.json"
ROW_PROVENANCE_PATH = DATA_DIR / "row_provenance_manifest.json"
NORMALIZATION_QUEUE_PATH = DATA_DIR / "row_normalization_queue.json"
NORMALIZATION_STATUS_PATH = DATA_DIR / "row_normalization_status.json"
NORMALIZATION_CANDIDATES_PATH = DATA_DIR / "row_normalization_candidates.json"
PROVISIONAL_NORMALIZED_PATH = DATA_DIR / "provisional_normalized_superconductors.json"
RESIDUAL_BLOCKER_PATH = DATA_DIR / "provisional_residual_blockers.json"
ROW_DOSSIER_PATH = DATA_DIR / "residual_blocker_row_dossiers.json"
FIELD_LOCK_MATRIX_PATH = DATA_DIR / "residual_blocker_field_lock_matrix.json"
PROXY_SENSITIVITY_PATH = DATA_DIR / "residual_blocker_proxy_sensitivity.json"
VANADIUM_PACKET_PATH = DATA_DIR / "vanadium_source_lock_packet.json"
A15_PACKET_PATH = DATA_DIR / "a15_external_resolution_packet.json"
VANADIUM_PATCH_PREVIEW_PATH = DATA_DIR / "vanadium_candidate_patch_preview.json"
A15_PATCH_PREVIEW_PATH = DATA_DIR / "a15_candidate_patch_preview.json"
ROW_EVIDENCE_INTAKE_PATH = DATA_DIR / "row_evidence_intake_stub.json"
ROW_EVIDENCE_READINESS_PATH = DATA_DIR / "row_evidence_readiness_matrix.json"
ROW_EVIDENCE_EXECUTION_QUEUE_PATH = DATA_DIR / "row_evidence_execution_queue.json"
ROW_EVIDENCE_SOURCE_REVIEW_PACKET_PATH = DATA_DIR / "row_evidence_source_review_packets.json"
ROW_EVIDENCE_DECISION_GATE_PATH = DATA_DIR / "row_evidence_decision_gate.json"
TOPIC_SOURCE_EVIDENCE_INTAKE_PATH = DATA_DIR / "source_evidence_intake_stub.json"
TOPIC_SOURCE_EVIDENCE_READINESS_PATH = DATA_DIR / "source_evidence_readiness_matrix.json"
TOPIC_BRANCH_CLAIM_GATE_PATH = DATA_DIR / "branch_claim_gate.json"
RAW_MCMILLAN_ROW_ELIGIBILITY_POLICY_PATH = (
    DATA_DIR / "raw_mcmillan_row_eligibility_policy.json"
)
ALLEN_DYNES_ARTIFACT_PATH = (
    TOPIC_DIR
    / "Result"
    / "artifacts"
    / "0_4_superconductivity_superfluids_allen_dynes_verification.json"
)
ROW_TARGET_DIR = Path(
    "docs/data/external/condensed_matter/superconductivity/row_resolution_targets"
)
VANADIUM_SOURCE_LOCK_DECISION_PATH = DATA_DIR / "vanadium_source_lock_decision.json"
VANADIUM_EXTERNAL_PACKET_PATHS = {
    "raw_page_capture_checklist": ROW_TARGET_DIR / "vanadium_raw_page_capture_checklist.json",
    "primary_page_capture_record": ROW_TARGET_DIR
    / "vanadium_primary_page_capture_record_20260516.json",
    "primary_capture_requirement_packet": ROW_TARGET_DIR
    / "vanadium_primary_capture_requirement_packet.json",
    "patch_block_decision": ROW_TARGET_DIR / "vanadium_patch_block_decision.json",
    "compatibility_review_packet": ROW_TARGET_DIR
    / "vanadium_compatibility_review_packet.json",
    "citation_integrity_report": ROW_TARGET_DIR / "vanadium_citation_integrity_report.json",
    "archive_dossier": ROW_TARGET_DIR / "vanadium" / "archive_dossier.json",
    "tc_text_capture_record": ROW_TARGET_DIR / "vanadium" / "tc_text_capture_record.json",
    "theta_text_capture_record": ROW_TARGET_DIR / "vanadium" / "theta_text_capture_record.json",
    "lambda_numeric_capture_record": ROW_TARGET_DIR
    / "vanadium"
    / "lambda_numeric_capture_record.json",
    "mu_star_numeric_capture_record": ROW_TARGET_DIR
    / "vanadium"
    / "mu_star_numeric_capture_record.json",
}

# Real experimental data from literature
# Sources: Kittel (Solid State Physics), Nature reviews, Physical Review Letters

SUPERCONDUCTOR_DATA = {
    "description": "Real experimental superconductor data with references",
    "sources": [
        "NIMS SuperCon Database",
        "MIT Junior Lab",
        "Kittel Solid State Physics 8th Ed",
        "McMillan (1968) Phys. Rev. 167, 331",
    ],
    "superconductors": [
        # ======= TYPE-I (Classical BCS) =======
        {
            "name": "Aluminum (Al)",
            "Tc_K": 1.175,
            "Tc_uncertainty": 0.002,
            "Theta_D_K": 428,
            "type": "Type-I",
            "lambda_ep": 0.43,  # Electron-phonon coupling
            "mu_star": 0.10,  # Coulomb pseudopotential
            "source": "McMillan 1968",
        },
        {
            "name": "Mercury (Hg)",
            "Tc_K": 4.15,
            "Tc_uncertainty": 0.01,
            "Theta_D_K": 72,
            "type": "Type-I",
            "lambda_ep": 1.6,
            "mu_star": 0.10,
            "source": "Onnes 1911 / Kittel",
        },
        {
            "name": "Lead (Pb)",
            "Tc_K": 7.19,
            "Tc_uncertainty": 0.02,
            "Theta_D_K": 105,
            "type": "Type-I",
            "lambda_ep": 1.55,
            "mu_star": 0.12,
            "source": "MIT Junior Lab",
        },
        {
            "name": "Vanadium (V)",
            "Tc_K": 5.36,
            "Tc_uncertainty": 0.13,
            "Theta_D_K": 380,
            "type": "Type-II",
            "lambda_ep": 0.80,
            "mu_star": 0.11,
            "source": "MIT Junior Lab",
        },
        {
            "name": "Niobium (Nb)",
            "Tc_K": 9.25,
            "Tc_uncertainty": 0.02,
            "Theta_D_K": 275,
            "type": "Type-II",
            "lambda_ep": 1.04,
            "mu_star": 0.12,
            "source": "Kittel / MIT",
        },
        {
            "name": "Tin (Sn)",
            "Tc_K": 3.72,
            "Tc_uncertainty": 0.01,
            "Theta_D_K": 200,
            "type": "Type-I",
            "lambda_ep": 0.72,
            "mu_star": 0.10,
            "source": "Kittel",
        },
        {
            "name": "Indium (In)",
            "Tc_K": 3.41,
            "Tc_uncertainty": 0.01,
            "Theta_D_K": 112,
            "type": "Type-I",
            "lambda_ep": 0.81,
            "mu_star": 0.10,
            "source": "Kittel",
        },
        # ======= A15 Compounds =======
        {
            "name": "Nb3Sn",
            "Tc_K": 18.3,
            "Tc_uncertainty": 0.2,
            "Theta_D_K": 280,
            "type": "A15",
            "lambda_ep": 1.8,
            "mu_star": 0.13,
            "source": "Matthias 1954",
        },
        {
            "name": "Nb3Ge",
            "Tc_K": 23.2,
            "Tc_uncertainty": 0.3,
            "Theta_D_K": 300,
            "type": "A15",
            "lambda_ep": 2.1,
            "mu_star": 0.13,
            "source": "Gavaler 1973",
        },
        # ======= MgB2 (Two-Gap) =======
        {
            "name": "MgB2",
            "Tc_K": 39.0,
            "Tc_uncertainty": 0.5,
            "Theta_D_K": 800,
            "type": "Two-Gap",
            "lambda_ep": 0.87,  # Weighted average
            "mu_star": 0.10,
            "source": "Nagamatsu 2001 Nature",
        },
        # ======= HIGH-Tc CUPRATES (Non-BCS) =======
        {
            "name": "YBCO (YBa2Cu3O7)",
            "Tc_K": 92.0,
            "Tc_uncertainty": 2.0,
            "Theta_D_K": 400,
            "type": "High-Tc Cuprate",
            "lambda_ep": None,  # Not applicable - different mechanism
            "mu_star": None,
            "source": "Wu 1987 PRL",
            "note": "Non-BCS mechanism",
        },
        {
            "name": "BSCCO-2223",
            "Tc_K": 110.0,
            "Tc_uncertainty": 2.0,
            "Theta_D_K": 400,
            "type": "High-Tc Cuprate",
            "lambda_ep": None,
            "mu_star": None,
            "source": "Maeda 1988",
            "note": "Non-BCS mechanism",
        },
    ],
    "formulas": {
        "BCS_weak_coupling": "Tc = 1.13 * Theta_D * exp(-1/Î»)",
        "McMillan_1968": "Tc = (Theta_D/1.45) * exp(-1.04*(1+Î»)/(Î»-Î¼*(1+0.62*Î»)))",
        "Allen_Dynes": "Tc = (f1*f2*Ï‰_log/1.2) * exp(-1.04*(1+Î»)/(Î»-Î¼*(1+0.62*Î»)))",
        "UET_extension": "Pending - need Information field coupling",
    },
}


def save_data(
    output_dir="docs/topics/0.4_Superconductivity_Superfluids/Data/03_Research",
):
    """Save real superconductor data to JSON."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_path = Path(output_dir) / "real_superconductor_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(SUPERCONDUCTOR_DATA, f, indent=2, ensure_ascii=False)

    print(f"âœ… Saved: {output_path}")
    print(f"   {len(SUPERCONDUCTOR_DATA['superconductors'])} superconductors")
    return output_path


def mcmillan_tc(theta_D, lambda_ep, mu_star=0.10):
    """
    McMillan equation for critical temperature.

    Tc = (Theta_D / 1.45) * exp(-1.04(1+Î») / (Î» - Î¼*(1+0.62Î»)))

    Valid for: Î» < 1.5 (weak to intermediate coupling)
    """
    import numpy as np

    if lambda_ep is None or lambda_ep <= mu_star * (1 + 0.62 * lambda_ep):
        return None  # Not applicable

    exponent = -1.04 * (1 + lambda_ep) / (lambda_ep - mu_star * (1 + 0.62 * lambda_ep))
    return (theta_D / 1.45) * np.exp(exponent)


def inverse_mcmillan_lambda(theta_D, target_tc, mu_star=0.10, low=0.05, high=5.0):
    """Find lambda_ep that reproduces target_tc for the declared theta_D and mu_star."""
    if target_tc <= 0 or theta_D <= 0:
        return None

    threshold = mu_star / max(1 - 0.62 * mu_star, 1e-12)
    low = max(low, threshold + 1e-6)
    lo_val = mcmillan_tc(theta_D, low, mu_star)
    hi_val = mcmillan_tc(theta_D, high, mu_star)
    if lo_val is None or hi_val is None or target_tc < lo_val or target_tc > hi_val:
        return None

    for _ in range(100):
        mid = (low + high) / 2
        mid_val = mcmillan_tc(theta_D, mid, mu_star)
        if mid_val is None:
            low = mid
        elif mid_val < target_tc:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def test_mcmillan():
    """Test McMillan equation against real data."""
    import numpy as np

    print("=" * 70)
    print("ðŸ”¬ McMillan Equation Test (Real Data)")
    print("=" * 70)

    results = []
    rows = []
    skipped_rows = []
    for sc in SUPERCONDUCTOR_DATA["superconductors"]:
        if sc.get("lambda_ep") is None:
            skipped_rows.append(
                {
                    "name": sc["name"],
                    "type": sc["type"],
                    "reason": "missing lambda_ep or non-BCS row for raw McMillan baseline",
                    "source": sc.get("source", "unknown"),
                }
            )
            continue

        tc_pred = mcmillan_tc(sc["Theta_D_K"], sc["lambda_ep"], sc.get("mu_star", 0.10))
        if tc_pred is None:
            continue

        tc_obs = sc["Tc_K"]
        error = abs(tc_pred - tc_obs) / tc_obs * 100
        signed_error_percent = (tc_pred - tc_obs) / tc_obs * 100
        lambda_required = inverse_mcmillan_lambda(
            sc["Theta_D_K"],
            tc_obs,
            sc.get("mu_star", 0.10),
        )
        lambda_delta = None if lambda_required is None else sc["lambda_ep"] - lambda_required
        lambda_ratio = None if not lambda_required else sc["lambda_ep"] / lambda_required
        status = "âœ…" if error < 20 else "âš ï¸"

        print(
            f"{sc['name']:20} | Tc_obs={tc_obs:6.2f}K | Tc_McM={tc_pred:6.2f}K | Î»={sc['lambda_ep']:.2f} | Err={error:5.1f}% {status}"
        )
        results.append(error)
        rows.append(
            {
                "name": sc["name"],
                "type": sc["type"],
                "Tc_observed_K": tc_obs,
                "Tc_mcmillan_K": float(tc_pred),
                "Theta_D_K": sc["Theta_D_K"],
                "lambda_ep": sc["lambda_ep"],
                "lambda_required_for_observed_tc": None if lambda_required is None else float(lambda_required),
                "lambda_delta_vs_required": None if lambda_delta is None else float(lambda_delta),
                "lambda_ratio_vs_required": None if lambda_ratio is None else float(lambda_ratio),
                "mu_star": sc.get("mu_star", 0.10),
                "relative_error_percent": float(error),
                "signed_error_percent": float(signed_error_percent),
                "within_20_percent": bool(error < 20),
                "source": sc.get("source", "unknown"),
            }
        )

    avg_err = np.mean(results)
    print("-" * 70)
    print(f"Average Error: {avg_err:.1f}%")
    return float(avg_err), rows, skipped_rows


def hash_file(path: Path) -> str | None:
    return sha256(path.read_bytes()).hexdigest() if path.exists() else None


def load_source_lock() -> dict:
    if not SOURCE_LOCK_PATH.exists():
        return {
            "status": "MISSING",
            "path": str(SOURCE_LOCK_PATH),
            "external_source_records": [],
            "derived_inputs": [],
        }
    return json.loads(SOURCE_LOCK_PATH.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def source_record_hashes(source_lock: dict) -> list[dict]:
    hashes = []
    for record_path in source_lock.get("external_source_records", []):
        path = Path(record_path)
        hashes.append(
            {
                "path": record_path,
                "sha256": hash_file(path),
                "status": "present" if path.exists() else "missing",
            }
        )
    return hashes


def build_raw_mcmillan_row_eligibility_report(
    rows: list[dict], skipped_rows: list[dict]
) -> dict:
    included_rows = []
    branch_migration_candidates = []
    for row in rows:
        policy_rule = (
            "raw_inputs_present"
            if row["type"] in ["Type-I", "Type-II"]
            else "formula_family_caveat_is_not_exclusion"
        )
        included_rows.append(
            {
                "name": row["name"],
                "type": row["type"],
                "source": row["source"],
                "policy_rule": policy_rule,
                "raw_gate_status": (
                    "within_threshold" if row["within_20_percent"] else "failed_threshold"
                ),
                "relative_error_percent": row["relative_error_percent"],
            }
        )
        if row["type"] in ["A15", "Two-Gap"] or row["name"] == "Vanadium (V)":
            branch_migration_candidates.append(
                {
                    "name": row["name"],
                    "type": row["type"],
                    "candidate_status": "review_candidate_only",
                    "current_raw_gate_membership": "included",
                    "reason": (
                        "Formula-family or convention caveat exists, but no "
                        "source-labeled alternate branch verifier has migrated this row."
                    ),
                }
            )

    return {
        "schema_version": "1.0",
        "policy": {
            "path": str(RAW_MCMILLAN_ROW_ELIGIBILITY_POLICY_PATH),
            "sha256": hash_file(RAW_MCMILLAN_ROW_ELIGIBILITY_POLICY_PATH),
            "status": (
                "present"
                if RAW_MCMILLAN_ROW_ELIGIBILITY_POLICY_PATH.exists()
                else "missing"
            ),
        },
        "summary": {
            "included_rows": len(included_rows),
            "skipped_rows": len(skipped_rows),
            "excluded_rows": 0,
            "branch_migration_candidates": len(branch_migration_candidates),
            "policy_executable_in_this_artifact": True,
            "metrics_changed_by_policy": False,
        },
        "included_rows": included_rows,
        "skipped_rows": [
            {
                "name": row["name"],
                "type": row["type"],
                "source": row["source"],
                "policy_rule": "missing_raw_coupling_inputs_or_declared_non_bcs",
                "reason": row["reason"],
            }
            for row in skipped_rows
        ],
        "excluded_rows": [],
        "branch_migration_candidates": branch_migration_candidates,
        "claim_boundary": (
            "This report makes row membership auditable. It does not exclude rows, "
            "migrate rows, change raw-gate metrics, or upgrade claims."
        ),
    }


def normalize_material_name(name: str) -> str:
    normalized = name.lower()
    for token in [" (al)", " (hg)", " (pb)", " (v)", " (nb)", " (sn)", " (in)"]:
        normalized = normalized.replace(token, "")
    normalized = normalized.replace(" ", "").replace("-", "").replace("_", "")
    return normalized


def analyze_failures(avg_err: float, rows: list[dict]) -> dict:
    failed_rows = [row for row in rows if not row["within_20_percent"]]
    worst_rows = sorted(
        rows,
        key=lambda row: row["relative_error_percent"],
        reverse=True,
    )[:5]
    return {
        "model_gate_status": "PASS" if avg_err <= 20.0 and not failed_rows else "FAIL",
        "primary_failure_reason": (
            "Raw McMillan benchmark exceeds the fixed average and per-material 20 percent error gates."
            if failed_rows
            else "No model-gate failure detected."
        ),
        "failed_material_count": len(failed_rows),
        "worst_materials": [
            {
                "name": row["name"],
                "relative_error_percent": row["relative_error_percent"],
                "type": row["type"],
                "source": row["source"],
            }
            for row in worst_rows
        ],
        "interpretation": "This is evidence that the current raw parameter package is not an accepted prediction gate; it is not evidence against every UET superconductivity mechanism.",
    }


def parameter_mismatch_summary(rows: list[dict]) -> dict:
    lambda_rows = [
        row for row in rows if row.get("lambda_required_for_observed_tc") is not None
    ]
    overestimated = [
        row for row in lambda_rows if row["lambda_ep"] > row["lambda_required_for_observed_tc"]
    ]
    underestimated = [
        row for row in lambda_rows if row["lambda_ep"] < row["lambda_required_for_observed_tc"]
    ]
    largest_abs_delta = sorted(
        lambda_rows,
        key=lambda row: abs(row["lambda_delta_vs_required"]),
        reverse=True,
    )[:5]
    return {
        "diagnostic": "inverse McMillan lambda audit",
        "interpretation": (
            "Holding theta_D and mu_star fixed, lambda_required_for_observed_tc is the "
            "coupling needed to reproduce observed Tc. Large deltas identify row-level "
            "parameter mismatch or missing Allen-Dynes/material-specific physics."
        ),
        "rows_with_inverse_solution": len(lambda_rows),
        "lambda_overestimated_count": len(overestimated),
        "lambda_underestimated_count": len(underestimated),
        "largest_lambda_mismatches": [
            {
                "name": row["name"],
                "lambda_ep": row["lambda_ep"],
                "lambda_required_for_observed_tc": row["lambda_required_for_observed_tc"],
                "lambda_delta_vs_required": row["lambda_delta_vs_required"],
                "relative_error_percent": row["relative_error_percent"],
            }
            for row in largest_abs_delta
        ],
    }


def error_bias_summary(rows: list[dict]) -> dict:
    signed_errors = [row["signed_error_percent"] for row in rows]
    overpredicted = [row for row in rows if row["signed_error_percent"] > 0]
    underpredicted = [row for row in rows if row["signed_error_percent"] < 0]
    return {
        "mean_signed_error_percent": sum(signed_errors) / len(signed_errors) if signed_errors else None,
        "median_signed_error_percent": sorted(signed_errors)[len(signed_errors) // 2] if signed_errors else None,
        "overpredicted_count": len(overpredicted),
        "underpredicted_count": len(underpredicted),
        "interpretation": (
            "Positive signed error means the raw McMillan package overpredicts Tc. "
            "A strong positive bias indicates the current lambda/theta/mu row package is systematically too hot."
        ),
    }


def summarize_group(rows: list[dict], field: str) -> list[dict]:
    summary = {}
    for row in rows:
        key = row[field]
        group = summary.setdefault(
            key,
            {
                "group": key,
                "materials_tested": 0,
                "materials_within_20_percent": 0,
                "relative_error_sum": 0.0,
                "signed_error_sum": 0.0,
            },
        )
        group["materials_tested"] += 1
        group["materials_within_20_percent"] += int(row["within_20_percent"])
        group["relative_error_sum"] += row["relative_error_percent"]
        group["signed_error_sum"] += row["signed_error_percent"]

    result = []
    for key, group in summary.items():
        tested = group["materials_tested"]
        result.append(
            {
                field: key,
                "materials_tested": tested,
                "materials_within_20_percent": group["materials_within_20_percent"],
                "average_relative_error_percent": group["relative_error_sum"] / tested,
                "mean_signed_error_percent": group["signed_error_sum"] / tested,
            }
        )
    return sorted(result, key=lambda item: item["average_relative_error_percent"], reverse=True)


def build_cross_dataset_comparison(rows: list[dict]) -> dict:
    comprehensive = load_json(COMPREHENSIVE_DATA_PATH)
    if not comprehensive:
        return {
            "status": "missing_comprehensive_dataset",
            "path": str(COMPREHENSIVE_DATA_PATH),
            "matched_rows": [],
            "priority_rows": [],
        }

    comprehensive_map = {
        normalize_material_name(item["name"]): item
        for item in comprehensive.get("superconductors", [])
    }
    matched_rows = []
    for row in rows:
        match = comprehensive_map.get(normalize_material_name(row["name"]))
        if not match:
            continue

        omega_log = match.get("omega_log_K")
        theta_d = row["Tc_observed_K"] and row.get("Tc_observed_K")
        lambda_gap = None
        if match.get("lambda_ep") is not None and row.get("lambda_ep") is not None:
            lambda_gap = row["lambda_ep"] - match["lambda_ep"]

        mu_gap = None
        if match.get("mu_star") is not None and row.get("mu_star") is not None:
            mu_gap = row["mu_star"] - match["mu_star"]

        matched_rows.append(
            {
                "name": row["name"],
                "raw_gate_type": row["type"],
                "raw_gate_source": row["source"],
                "raw_theta_D_K": row.get("Theta_D_K"),
                "comprehensive_omega_log_K": omega_log,
                "raw_lambda_ep": row["lambda_ep"],
                "comprehensive_lambda_ep": match.get("lambda_ep"),
                "lambda_gap_raw_minus_comprehensive": lambda_gap,
                "raw_mu_star": row["mu_star"],
                "comprehensive_mu_star": match.get("mu_star"),
                "mu_star_gap_raw_minus_comprehensive": mu_gap,
                "relative_error_percent": row["relative_error_percent"],
            }
        )

    priority_rows = sorted(
        matched_rows,
        key=lambda item: (
            abs(item["lambda_gap_raw_minus_comprehensive"])
            if item["lambda_gap_raw_minus_comprehensive"] is not None
            else -1
        ),
        reverse=True,
    )[:5]
    return {
        "status": "matched" if matched_rows else "no_overlap_found",
        "comprehensive_dataset_hash": hash_file(COMPREHENSIVE_DATA_PATH),
        "matched_row_count": len(matched_rows),
        "matched_rows": matched_rows,
        "priority_rows": priority_rows,
        "interpretation": (
            "This comparison is an internal provenance drift check between the raw McMillan gate table "
            "and the topic's broader comprehensive package. Large lambda gaps identify rows that need "
            "source normalization before any stronger superconductivity claim."
        ),
    }


def cross_package_lambda_substitution_audit(rows: list[dict]) -> dict:
    comprehensive = load_json(COMPREHENSIVE_DATA_PATH)
    if not comprehensive:
        return {
            "status": "missing_comprehensive_dataset",
            "path": str(COMPREHENSIVE_DATA_PATH),
        }

    comprehensive_map = {
        normalize_material_name(item["name"]): item
        for item in comprehensive.get("superconductors", [])
    }
    audited_rows = []
    raw_errors = []
    substituted_errors = []

    for row in rows:
        match = comprehensive_map.get(normalize_material_name(row["name"]))
        if not match or match.get("lambda_ep") is None:
            continue

        substituted_mu_star = match.get("mu_star", row["mu_star"])
        substituted_tc = mcmillan_tc(
            row["Theta_D_K"],
            match["lambda_ep"],
            substituted_mu_star,
        )
        if substituted_tc is None:
            continue

        substituted_error = abs(substituted_tc - row["Tc_observed_K"]) / row["Tc_observed_K"] * 100
        error_delta = substituted_error - row["relative_error_percent"]
        raw_errors.append(row["relative_error_percent"])
        substituted_errors.append(substituted_error)
        audited_rows.append(
            {
                "name": row["name"],
                "raw_relative_error_percent": row["relative_error_percent"],
                "substituted_relative_error_percent": float(substituted_error),
                "error_delta_percent": float(error_delta),
                "raw_lambda_ep": row["lambda_ep"],
                "substituted_lambda_ep": match["lambda_ep"],
                "raw_mu_star": row["mu_star"],
                "substituted_mu_star": substituted_mu_star,
                "interpretation": (
                    "Negative error_delta_percent means the comprehensive-package substitution improves "
                    "the raw gate for this row under the same Theta_D_K."
                ),
            }
        )

    improved_rows = [item for item in audited_rows if item["error_delta_percent"] < 0]
    worsened_rows = [item for item in audited_rows if item["error_delta_percent"] > 0]
    return {
        "status": "matched" if audited_rows else "no_overlap_found",
        "matched_row_count": len(audited_rows),
        "raw_average_relative_error_percent": (
            sum(raw_errors) / len(raw_errors) if raw_errors else None
        ),
        "substituted_average_relative_error_percent": (
            sum(substituted_errors) / len(substituted_errors) if substituted_errors else None
        ),
        "rows_improved_by_substitution": len(improved_rows),
        "rows_worsened_by_substitution": len(worsened_rows),
        "largest_improvements": sorted(
            improved_rows,
            key=lambda item: item["error_delta_percent"],
        )[:5],
        "largest_worsenings": sorted(
            worsened_rows,
            key=lambda item: item["error_delta_percent"],
            reverse=True,
        )[:5],
        "audited_rows": audited_rows,
        "claim_boundary": (
            "This is an internal sensitivity diagnostic only. It does not prove that the comprehensive "
            "package is source-correct; it only tests whether row drift is a major part of the raw-gate failure."
        ),
    }


def write_row_provenance_manifest(rows: list[dict], skipped_rows: list[dict]) -> dict:
    comparison = build_cross_dataset_comparison(rows)
    substitution_audit = cross_package_lambda_substitution_audit(rows)
    manifest = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Row-level provenance and drift tracker for the raw McMillan gate table.",
        "raw_gate_input_hash": hash_file(DATA_DIR / "real_superconductor_data.json"),
        "comprehensive_input_hash": hash_file(COMPREHENSIVE_DATA_PATH),
        "tested_rows": [
            {
                "name": row["name"],
                "type": row["type"],
                "source": row["source"],
                "lambda_ep": row["lambda_ep"],
                "mu_star": row["mu_star"],
                "relative_error_percent": row["relative_error_percent"],
                "source_status": "working_copy_cited_row",
            }
            for row in rows
        ],
        "skipped_rows": skipped_rows,
        "cross_dataset_comparison": comparison,
        "cross_package_lambda_substitution_audit": substitution_audit,
        "claim_boundary": (
            "This manifest improves row-level auditability but does not certify that any material row "
            "is normalized to an upstream authoritative table."
        ),
    }
    ROW_PROVENANCE_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def build_row_normalization_queue(rows: list[dict], row_provenance_manifest: dict) -> dict:
    substitution = row_provenance_manifest["cross_package_lambda_substitution_audit"]
    substitution_map = {
        item["name"]: item for item in substitution.get("audited_rows", [])
    }
    queue_rows = []

    for row in rows:
        sub = substitution_map.get(row["name"])
        if not sub:
            continue

        lambda_required = row.get("lambda_required_for_observed_tc")
        lambda_delta_required = row.get("lambda_delta_vs_required")
        priority_score = abs(sub["error_delta_percent"]) + row["relative_error_percent"]
        queue_rows.append(
            {
                "name": row["name"],
                "type": row["type"],
                "source": row["source"],
                "priority_score": float(priority_score),
                "priority_band": "immediate"
                if priority_score >= 100
                else "high"
                if priority_score >= 50
                else "medium",
                "current_relative_error_percent": row["relative_error_percent"],
                "signed_error_percent": row["signed_error_percent"],
                "raw_theta_D_K": row["Theta_D_K"],
                "raw_lambda_ep": row["lambda_ep"],
                "comprehensive_lambda_ep": sub["substituted_lambda_ep"],
                "lambda_required_for_observed_tc": lambda_required,
                "lambda_gap_raw_minus_comprehensive": (
                    None if sub["substituted_lambda_ep"] is None else row["lambda_ep"] - sub["substituted_lambda_ep"]
                ),
                "lambda_gap_raw_minus_required": lambda_delta_required,
                "raw_mu_star": row["mu_star"],
                "comprehensive_mu_star": sub["substituted_mu_star"],
                "substituted_relative_error_percent": sub["substituted_relative_error_percent"],
                "error_delta_percent": sub["error_delta_percent"],
                "normalization_target": (
                    "Verify row-level lambda_ep, theta_D/phonon proxy, and mu_star against source-backed literature or upstream table."
                ),
                "why_this_row_first": (
                    "Large internal package drift and large projected error reduction under substitution."
                ),
            }
        )

    queue_rows = sorted(queue_rows, key=lambda item: item["priority_score"], reverse=True)
    queue = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Actionable row-normalization queue derived from the current McMillan FAIL artifact.",
        "generated_from": {
            "artifact_path": str(ARTIFACT_PATH),
            "row_provenance_manifest_path": str(ROW_PROVENANCE_PATH),
            "raw_gate_input_hash": row_provenance_manifest.get("raw_gate_input_hash"),
            "comprehensive_input_hash": row_provenance_manifest.get("comprehensive_input_hash"),
        },
        "summary": {
            "rows_in_queue": len(queue_rows),
            "immediate_rows": sum(1 for item in queue_rows if item["priority_band"] == "immediate"),
            "high_rows": sum(1 for item in queue_rows if item["priority_band"] == "high"),
            "medium_rows": sum(1 for item in queue_rows if item["priority_band"] == "medium"),
        },
        "queue_rows": queue_rows,
        "claim_boundary": (
            "This queue prioritizes row normalization work. It does not by itself upgrade the scientific claim status of the topic."
        ),
    }
    NORMALIZATION_QUEUE_PATH.write_text(json.dumps(queue, indent=2), encoding="utf-8")
    return queue


def build_row_normalization_status(
    normalization_queue: dict, row_provenance_manifest: dict
) -> dict:
    comparison_map = {
        item["name"]: item
        for item in row_provenance_manifest["cross_dataset_comparison"].get("matched_rows", [])
    }
    status_rows = []
    for item in normalization_queue["queue_rows"]:
        comparison = comparison_map.get(item["name"], {})
        status_rows.append(
            {
                "name": item["name"],
                "priority_band": item["priority_band"],
                "source_status": "unverified_working_copy_row",
                "normalization_status": "pending_external_row_check",
                "current_row_package": {
                    "source_label": item["source"],
                    "theta_D_K": item["raw_theta_D_K"],
                    "lambda_ep": item["raw_lambda_ep"],
                    "mu_star": item["raw_mu_star"],
                },
                "internal_comparison_package": {
                    "source_label": "comprehensive_superconductor_data.json",
                    "omega_log_K": comparison.get("comprehensive_omega_log_K"),
                    "lambda_ep": item["comprehensive_lambda_ep"],
                    "mu_star": item["comprehensive_mu_star"],
                },
                "diagnostic_targets": {
                    "lambda_required_for_observed_tc": item["lambda_required_for_observed_tc"],
                    "raw_minus_comprehensive_lambda": item["lambda_gap_raw_minus_comprehensive"],
                    "raw_minus_required_lambda": item["lambda_gap_raw_minus_required"],
                    "projected_error_if_substituted_percent": item["substituted_relative_error_percent"],
                },
                "external_source_targets": [
                    "docs/data/external/condensed_matter/superconductivity/mcmillan_1968/source_record.json",
                    "docs/data/external/condensed_matter/superconductivity/nims_supercon/source_record.json",
                ],
                "next_actions": [
                    "Find an explicit upstream or literature row for Tc, phonon-temperature proxy, lambda_ep, and mu_star.",
                    "Record whether Theta_D_K or omega_log_K is the physically appropriate comparison target for this row.",
                    "Update the raw working-copy row only after the source path and unit convention are declared.",
                ],
                "why_priority": item["why_this_row_first"],
            }
        )

    ledger = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Operational status ledger for row-level superconductivity normalization work.",
        "generated_from": {
            "row_normalization_queue_path": str(NORMALIZATION_QUEUE_PATH),
            "row_provenance_manifest_path": str(ROW_PROVENANCE_PATH),
        },
        "summary": {
            "rows_pending_external_row_check": len(status_rows),
            "immediate_rows": sum(1 for row in status_rows if row["priority_band"] == "immediate"),
            "high_rows": sum(1 for row in status_rows if row["priority_band"] == "high"),
            "medium_rows": sum(1 for row in status_rows if row["priority_band"] == "medium"),
        },
        "status_rows": status_rows,
        "claim_boundary": (
            "This ledger is a work-control artifact. It organizes row normalization tasks but does not validate any source row by itself."
        ),
    }
    NORMALIZATION_STATUS_PATH.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    return ledger


def build_row_normalization_candidates(normalization_status: dict) -> dict:
    candidate_rows = []
    for row in normalization_status["status_rows"]:
        diagnostic = row["diagnostic_targets"]
        current = row["current_row_package"]
        comparison = row["internal_comparison_package"]

        required_lambda = diagnostic.get("lambda_required_for_observed_tc")
        comparison_lambda = comparison.get("lambda_ep")
        current_lambda = current.get("lambda_ep")

        comparison_vs_required_gap = None
        if comparison_lambda is not None and required_lambda is not None:
            comparison_vs_required_gap = comparison_lambda - required_lambda

        if comparison_vs_required_gap is not None and abs(comparison_vs_required_gap) <= 0.08:
            recommendation_class = "internal_consensus_candidate"
            recommended_lambda = comparison_lambda
            candidate_reason = (
                "Comprehensive-package lambda and inverse-required lambda are closely aligned."
            )
        elif comparison_lambda is not None and required_lambda is not None:
            recommendation_class = "needs_external_resolution"
            recommended_lambda = None
            candidate_reason = (
                "Comprehensive-package lambda and inverse-required lambda still disagree materially."
            )
        else:
            recommendation_class = "insufficient_internal_overlap"
            recommended_lambda = None
            candidate_reason = "Internal comparison package does not provide a stable candidate."

        candidate_rows.append(
            {
                "name": row["name"],
                "priority_band": row["priority_band"],
                "recommendation_class": recommendation_class,
                "current_lambda_ep": current_lambda,
                "comparison_lambda_ep": comparison_lambda,
                "inverse_required_lambda_ep": required_lambda,
                "comparison_minus_required_lambda": comparison_vs_required_gap,
                "recommended_lambda_ep": recommended_lambda,
                "current_mu_star": current.get("mu_star"),
                "comparison_mu_star": comparison.get("mu_star"),
                "recommended_mu_star": (
                    comparison.get("mu_star")
                    if recommendation_class == "internal_consensus_candidate"
                    else None
                ),
                "projected_error_if_comparison_package_used_percent": diagnostic.get(
                    "projected_error_if_substituted_percent"
                ),
                "candidate_reason": candidate_reason,
                "claim_boundary": (
                    "This candidate is for internal row normalization triage only. "
                    "Do not promote it to a source-backed value until an upstream row or literature table is attached."
                ),
            }
        )

    candidates = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Internal candidate pack for row-level normalization decisions before external row checks are completed.",
        "summary": {
            "rows_total": len(candidate_rows),
            "internal_consensus_candidates": sum(
                1 for row in candidate_rows if row["recommendation_class"] == "internal_consensus_candidate"
            ),
            "rows_needing_external_resolution": sum(
                1 for row in candidate_rows if row["recommendation_class"] == "needs_external_resolution"
            ),
            "rows_with_insufficient_internal_overlap": sum(
                1
                for row in candidate_rows
                if row["recommendation_class"] == "insufficient_internal_overlap"
            ),
        },
        "candidate_rows": candidate_rows,
        "claim_boundary": (
            "This file is an internal triage layer. It helps prioritize which rows may have a stable local candidate, "
            "but it does not replace external source normalization."
        ),
    }
    NORMALIZATION_CANDIDATES_PATH.write_text(json.dumps(candidates, indent=2), encoding="utf-8")
    return candidates


def build_provisional_normalized_table(
    rows: list[dict], normalization_candidates: dict
) -> dict:
    candidate_map = {
        item["name"]: item for item in normalization_candidates.get("candidate_rows", [])
    }
    provisional_rows = []
    for row in rows:
        candidate = candidate_map.get(row["name"])
        if not candidate:
            continue

        if candidate["recommendation_class"] == "internal_consensus_candidate":
            lambda_value = candidate["recommended_lambda_ep"]
            mu_value = (
                candidate["recommended_mu_star"]
                if candidate["recommended_mu_star"] is not None
                else row["mu_star"]
            )
            normalization_class = "provisional_internal_consensus"
        else:
            lambda_value = row["lambda_ep"]
            mu_value = row["mu_star"]
            normalization_class = "unresolved_kept_raw"

        provisional_rows.append(
            {
                "name": row["name"],
                "type": row["type"],
                "Tc_K": row["Tc_observed_K"],
                "Theta_D_K": row["Theta_D_K"],
                "lambda_ep": lambda_value,
                "mu_star": mu_value,
                "source": row["source"],
                "normalization_class": normalization_class,
                "candidate_basis": candidate["recommendation_class"],
            }
        )

    table = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Provisional normalized table for internal sensitivity testing only.",
        "rows": provisional_rows,
        "claim_boundary": (
            "This table is not a source-backed normalized dataset. It is an internal sensitivity package "
            "built from candidate rows to estimate how much the FAIL depends on row-level parameter drift."
        ),
    }
    PROVISIONAL_NORMALIZED_PATH.write_text(json.dumps(table, indent=2), encoding="utf-8")
    return table


def evaluate_rows(rows: list[dict]) -> dict:
    evaluated = []
    skipped = []
    errors = []

    for row in rows:
        lambda_ep = row.get("lambda_ep")
        mu_star = row.get("mu_star", 0.10)
        theta_d = row.get("Theta_D_K")
        tc_obs = row.get("Tc_observed_K", row.get("Tc_K"))
        if lambda_ep is None or theta_d is None or tc_obs is None:
            skipped.append({"name": row.get("name", "unknown"), "reason": "missing evaluation inputs"})
            continue

        tc_pred = mcmillan_tc(theta_d, lambda_ep, mu_star)
        if tc_pred is None:
            skipped.append({"name": row.get("name", "unknown"), "reason": "mcmillan returned none"})
            continue

        error = abs(tc_pred - tc_obs) / tc_obs * 100
        errors.append(error)
        evaluated.append(
            {
                "name": row["name"],
                "Tc_observed_K": tc_obs,
                "Tc_mcmillan_K": float(tc_pred),
                "relative_error_percent": float(error),
                "within_20_percent": bool(error <= 20.0),
            }
        )

    return {
        "rows": evaluated,
        "skipped": skipped,
        "average_relative_error_percent": (sum(errors) / len(errors)) if errors else None,
        "materials_within_20_percent": sum(1 for row in evaluated if row["within_20_percent"]),
        "materials_tested": len(evaluated),
    }


def build_provisional_residual_blockers(
    raw_rows: list[dict], normalization_candidates: dict, provisional_evaluation: dict
) -> dict:
    raw_map = {row["name"]: row for row in raw_rows}
    candidate_map = {
        row["name"]: row for row in normalization_candidates.get("candidate_rows", [])
    }
    blocker_rows = []

    for row in provisional_evaluation.get("rows", []):
        raw_row = raw_map.get(row["name"], {})
        candidate = candidate_map.get(row["name"], {})
        provisional_error = row.get("relative_error_percent")
        raw_error = raw_row.get("relative_error_percent")
        error_reduction = None
        if provisional_error is not None and raw_error is not None:
            error_reduction = raw_error - provisional_error

        if row.get("within_20_percent"):
            resolution_class = "provisional_pass_only"
            next_gate = "Requires upstream row lock before raw table can be changed."
        else:
            resolution_class = "residual_blocker_after_provisional"
            if candidate.get("recommendation_class") == "needs_external_resolution":
                next_gate = "External row resolution required before any normalization decision."
            else:
                next_gate = "Borderline residual; verify theta/omega proxy choice and source row."

        blocker_rows.append(
            {
                "name": row["name"],
                "type": raw_row.get("type"),
                "source": raw_row.get("source"),
                "raw_relative_error_percent": raw_error,
                "provisional_relative_error_percent": provisional_error,
                "error_reduction_percent": error_reduction,
                "within_20_percent_after_provisional": row.get("within_20_percent"),
                "candidate_basis": candidate.get("recommendation_class"),
                "recommended_lambda_ep": candidate.get("recommended_lambda_ep"),
                "inverse_required_lambda_ep": candidate.get("inverse_required_lambda_ep"),
                "resolution_class": resolution_class,
                "next_gate": next_gate,
            }
        )

    blocker_rows.sort(
        key=lambda item: (
            0 if item["resolution_class"] == "residual_blocker_after_provisional" else 1,
            -(item.get("provisional_relative_error_percent") or 0.0),
        )
    )

    manifest = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Residual blocker map after provisional internal-consensus substitutions.",
        "summary": {
            "rows_total": len(blocker_rows),
            "rows_passing_after_provisional": sum(
                1 for row in blocker_rows if row["within_20_percent_after_provisional"]
            ),
            "rows_still_blocking_after_provisional": sum(
                1
                for row in blocker_rows
                if row["resolution_class"] == "residual_blocker_after_provisional"
            ),
            "rows_requiring_external_resolution_after_provisional": sum(
                1
                for row in blocker_rows
                if row["resolution_class"] == "residual_blocker_after_provisional"
                and row["candidate_basis"] == "needs_external_resolution"
            ),
        },
        "blocker_rows": blocker_rows,
        "claim_boundary": (
            "This manifest is a residual-blocker decomposition for workflow control. "
            "It does not authorize replacement of the raw benchmark table."
        ),
    }
    RESIDUAL_BLOCKER_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def build_residual_blocker_row_dossiers(
    residual_blockers: dict, row_provenance_manifest: dict
) -> dict:
    matched_rows = {
        row["name"]: row
        for row in row_provenance_manifest["cross_dataset_comparison"].get("matched_rows", [])
    }
    dossiers = []

    for row in residual_blockers.get("blocker_rows", []):
        if row.get("resolution_class") != "residual_blocker_after_provisional":
            continue

        matched = matched_rows.get(row["name"], {})
        if row["name"] in {"Nb3Sn", "Nb3Ge"}:
            blocker_family = "A15 unresolved strong-coupling row"
            unit_question = (
                "Confirm whether the retained phonon proxy for the benchmark row should be Debye temperature "
                "(Theta_D_K) or log-phonon frequency (omega_log_K) before touching lambda_ep."
            )
            source_priority = "external_resolution_required"
        else:
            blocker_family = "Borderline conventional row"
            unit_question = (
                "Check whether Theta_D_K is the correct benchmark proxy for this row or whether omega_log_K "
                "should replace it in the source-normalized comparison."
            )
            source_priority = "borderline_source_lock_required"

        dossiers.append(
            {
                "name": row["name"],
                "blocker_family": blocker_family,
                "source_label": row.get("source"),
                "type": row.get("type"),
                "resolution_class": row.get("resolution_class"),
                "source_priority": source_priority,
                "raw_package": {
                    "relative_error_percent": row.get("raw_relative_error_percent"),
                    "theta_D_K": matched.get("raw_theta_D_K"),
                    "lambda_ep": matched.get("raw_lambda_ep"),
                    "mu_star": matched.get("raw_mu_star"),
                },
                "internal_candidate_package": {
                    "provisional_relative_error_percent": row.get("provisional_relative_error_percent"),
                    "recommended_lambda_ep": row.get("recommended_lambda_ep"),
                    "comparison_lambda_ep": matched.get("comprehensive_lambda_ep"),
                    "comparison_mu_star": matched.get("comprehensive_mu_star"),
                    "comparison_omega_log_K": matched.get("comprehensive_omega_log_K"),
                },
                "inverse_required_lambda_ep": row.get("inverse_required_lambda_ep"),
                "unit_decision_question": unit_question,
                "external_source_targets": [
                    "docs/data/external/condensed_matter/superconductivity/mcmillan_1968/source_record.json",
                    "docs/data/external/condensed_matter/superconductivity/allen_dynes_1975/source_record.json",
                    "docs/data/external/condensed_matter/superconductivity/nims_supercon/source_record.json",
                ],
                "required_row_fields": [
                    "Tc_K or Tc_exp_K with cited row source",
                    "phonon proxy field and unit basis (Theta_D_K or omega_log_K)",
                    "lambda_ep with row citation",
                    "mu_star with row citation or declared benchmark convention",
                ],
                "decision_gate": row.get("next_gate"),
                "claim_boundary": (
                    "This dossier is a row-resolution work packet. It narrows what must be checked next, "
                    "but it does not certify any material row until an upstream or literature row is attached."
                ),
            }
        )

    dossier_manifest = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Row-resolution dossiers for the residual blockers that remain after the provisional sensitivity pass.",
        "summary": {
            "dossiers_total": len(dossiers),
            "external_resolution_required": sum(
                1 for row in dossiers if row["source_priority"] == "external_resolution_required"
            ),
            "borderline_source_lock_required": sum(
                1 for row in dossiers if row["source_priority"] == "borderline_source_lock_required"
            ),
        },
        "row_dossiers": dossiers,
        "claim_boundary": (
            "These dossiers organize row-level follow-up work. They are not source-backed corrections."
        ),
    }
    ROW_DOSSIER_PATH.write_text(json.dumps(dossier_manifest, indent=2), encoding="utf-8")
    return dossier_manifest


def build_residual_blocker_field_lock_matrix(row_dossiers: dict) -> dict:
    matrix_rows = []
    for dossier in row_dossiers.get("row_dossiers", []):
        source_priority = dossier.get("source_priority")
        has_candidate_lambda = dossier["internal_candidate_package"].get("recommended_lambda_ep") is not None

        if source_priority == "external_resolution_required":
            phonon_proxy_status = "requires_external_row"
            lambda_status = "requires_external_row"
            mu_star_status = "requires_external_row"
        else:
            phonon_proxy_status = "proxy_choice_open"
            lambda_status = "internal_consensus_only" if has_candidate_lambda else "requires_external_row"
            mu_star_status = "working_copy_retained"

        matrix_rows.append(
            {
                "name": dossier["name"],
                "source_priority": source_priority,
                "field_lock_status": {
                    "Tc_observed": "working_copy_cited_but_row_unlocked",
                    "phonon_proxy": phonon_proxy_status,
                    "lambda_ep": lambda_status,
                    "mu_star": mu_star_status,
                },
                "current_values": {
                    "Tc_relative_error_percent": dossier["raw_package"].get("relative_error_percent"),
                    "theta_D_K": dossier["raw_package"].get("theta_D_K"),
                    "comparison_omega_log_K": dossier["internal_candidate_package"].get("comparison_omega_log_K"),
                    "raw_lambda_ep": dossier["raw_package"].get("lambda_ep"),
                    "candidate_lambda_ep": dossier["internal_candidate_package"].get("recommended_lambda_ep"),
                    "inverse_required_lambda_ep": dossier.get("inverse_required_lambda_ep"),
                    "mu_star": dossier["raw_package"].get("mu_star"),
                },
                "unlock_requirements": {
                    "Tc_observed": "Attach explicit upstream or literature row identity for the reported Tc value.",
                    "phonon_proxy": dossier.get("unit_decision_question"),
                    "lambda_ep": (
                        "Attach cited row-level lambda_ep value and confirm it matches the chosen phonon proxy convention."
                    ),
                    "mu_star": (
                        "Either attach a row-level mu_star citation or declare the benchmark convention used for this material family."
                    ),
                },
                "next_decision_gate": dossier.get("decision_gate"),
            }
        )

    matrix = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Field-level lock matrix for residual superconductivity blocker rows.",
        "summary": {
            "rows_total": len(matrix_rows),
            "rows_requiring_external_row": sum(
                1 for row in matrix_rows if row["source_priority"] == "external_resolution_required"
            ),
            "rows_with_proxy_choice_open": sum(
                1
                for row in matrix_rows
                if row["field_lock_status"]["phonon_proxy"] == "proxy_choice_open"
            ),
            "rows_with_internal_consensus_lambda_only": sum(
                1
                for row in matrix_rows
                if row["field_lock_status"]["lambda_ep"] == "internal_consensus_only"
            ),
        },
        "matrix_rows": matrix_rows,
        "claim_boundary": (
            "This matrix is a field-level workflow aid. It tracks what is still unlocked in each residual row, "
            "but it does not certify any field as upstream-verified."
        ),
    }
    FIELD_LOCK_MATRIX_PATH.write_text(json.dumps(matrix, indent=2), encoding="utf-8")
    return matrix


def build_residual_blocker_proxy_sensitivity(row_dossiers: dict) -> dict:
    proxy_rows = []
    for dossier in row_dossiers.get("row_dossiers", []):
        raw = dossier["raw_package"]
        candidate = dossier["internal_candidate_package"]
        theta_d = raw.get("theta_D_K")
        omega_log = candidate.get("comparison_omega_log_K")
        lambda_ep = candidate.get("recommended_lambda_ep")
        mu_star = candidate.get("comparison_mu_star")

        if theta_d is None or omega_log is None or lambda_ep is None or mu_star is None:
            continue

        tc_obs = None
        if raw.get("relative_error_percent") is not None and theta_d is not None:
            pass

        # Recover observed Tc from the internal candidate package via provisional error carrier data.
        # The raw dossier does not store Tc directly, so use the inverse-required lambda and current fields only
        # for comparative proxy sensitivity on the same row.
        theta_prediction = mcmillan_tc(theta_d, lambda_ep, mu_star)
        omega_prediction = mcmillan_tc(omega_log, lambda_ep, mu_star)

        tc_observed = None
        inverse_required = dossier.get("inverse_required_lambda_ep")
        if inverse_required is not None and theta_d is not None:
            tc_observed = mcmillan_tc(theta_d, inverse_required, mu_star)

        theta_error = None
        omega_error = None
        preferred_proxy = "undetermined"
        if tc_observed is not None and theta_prediction is not None and omega_prediction is not None:
            theta_error = abs(theta_prediction - tc_observed) / tc_observed * 100
            omega_error = abs(omega_prediction - tc_observed) / tc_observed * 100
            preferred_proxy = "omega_log_K" if omega_error < theta_error else "Theta_D_K"

        proxy_rows.append(
            {
                "name": dossier["name"],
                "source_priority": dossier["source_priority"],
                "recommended_lambda_ep": lambda_ep,
                "mu_star": mu_star,
                "theta_D_K": theta_d,
                "omega_log_K": omega_log,
                "tc_reference_from_inverse_required_K": tc_observed,
                "theta_proxy_prediction_K": theta_prediction,
                "omega_log_proxy_prediction_K": omega_prediction,
                "theta_proxy_relative_error_percent": theta_error,
                "omega_log_proxy_relative_error_percent": omega_error,
                "preferred_proxy_under_internal_sensitivity": preferred_proxy,
                "interpretation": (
                    "Internal-only proxy sensitivity check under the same lambda_ep and mu_star. "
                    "This does not choose the authoritative proxy without source-backed row context."
                ),
            }
        )

    manifest = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Internal proxy sensitivity comparison for residual blocker rows.",
        "summary": {
            "rows_compared": len(proxy_rows),
            "rows_preferring_omega_log_K_under_internal_sensitivity": sum(
                1 for row in proxy_rows if row["preferred_proxy_under_internal_sensitivity"] == "omega_log_K"
            ),
            "rows_preferring_theta_D_K_under_internal_sensitivity": sum(
                1 for row in proxy_rows if row["preferred_proxy_under_internal_sensitivity"] == "Theta_D_K"
            ),
        },
        "proxy_rows": proxy_rows,
        "claim_boundary": (
            "This proxy comparison is internal sensitivity only. It helps prioritize proxy checks "
            "but does not establish the authoritative field convention for any material row."
        ),
    }
    PROXY_SENSITIVITY_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def build_vanadium_source_lock_packet(
    row_dossiers: dict, field_lock_matrix: dict, proxy_sensitivity: dict
) -> dict | None:
    dossier = next(
        (row for row in row_dossiers.get("row_dossiers", []) if row.get("name") == "Vanadium (V)"),
        None,
    )
    field_lock = next(
        (row for row in field_lock_matrix.get("matrix_rows", []) if row.get("name") == "Vanadium (V)"),
        None,
    )
    proxy_row = next(
        (row for row in proxy_sensitivity.get("proxy_rows", []) if row.get("name") == "Vanadium (V)"),
        None,
    )
    if not dossier or not field_lock or not proxy_row:
        return None

    packet = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "material": "Vanadium (V)",
        "purpose": "Focused source-lock packet for the remaining borderline superconductivity blocker row.",
        "status_summary": {
            "source_priority": dossier["source_priority"],
            "decision_gate": dossier["decision_gate"],
            "raw_relative_error_percent": dossier["raw_package"]["relative_error_percent"],
            "provisional_relative_error_percent": dossier["internal_candidate_package"][
                "provisional_relative_error_percent"
            ],
        },
        "current_row_package": dossier["raw_package"],
        "candidate_row_package": {
            "recommended_lambda_ep": dossier["internal_candidate_package"]["recommended_lambda_ep"],
            "comparison_lambda_ep": dossier["internal_candidate_package"]["comparison_lambda_ep"],
            "comparison_mu_star": dossier["internal_candidate_package"]["comparison_mu_star"],
            "comparison_omega_log_K": dossier["internal_candidate_package"]["comparison_omega_log_K"],
            "inverse_required_lambda_ep": dossier["inverse_required_lambda_ep"],
        },
        "field_lock_status": field_lock["field_lock_status"],
        "proxy_sensitivity": {
            "preferred_proxy_under_internal_sensitivity": proxy_row[
                "preferred_proxy_under_internal_sensitivity"
            ],
            "theta_proxy_relative_error_percent": proxy_row["theta_proxy_relative_error_percent"],
            "omega_log_proxy_relative_error_percent": proxy_row["omega_log_proxy_relative_error_percent"],
        },
        "recommended_next_actions": [
            "Lock the cited Tc row identity first so later field choices reference the same material record.",
            "Start proxy verification from Theta_D_K because internal sensitivity currently favors it over omega_log_K for this row.",
            "Check whether the cited lambda_ep value near 0.6 belongs to the same proxy convention and material condition.",
            "Retain mu_star = 0.11 as a working benchmark convention unless a row-specific citation overrides it.",
        ],
        "external_source_targets": dossier["external_source_targets"],
        "claim_boundary": (
            "This packet is a workflow aid for the Vanadium row only. "
            "It does not certify the row as source-locked until the cited fields are attached."
        ),
    }
    VANADIUM_PACKET_PATH.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    return packet


def build_a15_external_resolution_packet(
    row_dossiers: dict, field_lock_matrix: dict
) -> dict | None:
    dossier_map = {
        row["name"]: row
        for row in row_dossiers.get("row_dossiers", [])
        if row.get("name") in {"Nb3Sn", "Nb3Ge"}
    }
    field_map = {
        row["name"]: row
        for row in field_lock_matrix.get("matrix_rows", [])
        if row.get("name") in {"Nb3Sn", "Nb3Ge"}
    }
    if len(dossier_map) != 2 or len(field_map) != 2:
        return None

    rows = []
    for name in ("Nb3Sn", "Nb3Ge"):
        dossier = dossier_map[name]
        field_lock = field_map[name]
        rows.append(
            {
                "name": name,
                "status_summary": {
                    "decision_gate": dossier["decision_gate"],
                    "raw_relative_error_percent": dossier["raw_package"]["relative_error_percent"],
                    "provisional_relative_error_percent": dossier["internal_candidate_package"][
                        "provisional_relative_error_percent"
                    ],
                },
                "current_row_package": dossier["raw_package"],
                "internal_comparison_package": {
                    "comparison_lambda_ep": dossier["internal_candidate_package"]["comparison_lambda_ep"],
                    "comparison_mu_star": dossier["internal_candidate_package"]["comparison_mu_star"],
                    "comparison_omega_log_K": dossier["internal_candidate_package"]["comparison_omega_log_K"],
                    "inverse_required_lambda_ep": dossier["inverse_required_lambda_ep"],
                },
                "field_lock_status": field_lock["field_lock_status"],
                "required_row_fields": dossier["required_row_fields"],
                "unit_decision_question": dossier["unit_decision_question"],
            }
        )

    packet = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "material_family": "A15 residual blockers",
        "purpose": "Focused external-resolution packet for the two remaining A15 blocker rows.",
        "status_summary": {
            "rows_total": 2,
            "source_priority": "external_resolution_required",
            "shared_decision_gate": "External row resolution required before any normalization decision.",
        },
        "row_packets": rows,
        "recommended_next_actions": [
            "Lock cited Tc row identities for both A15 materials before changing any parameter values.",
            "Resolve whether the row should be benchmarked with Theta_D_K or omega_log_K from the cited source context.",
            "Do not substitute lambda_ep from internal comparison packages until a row-level citation supports the chosen proxy convention.",
            "Treat mu_star as unresolved until a row citation or an explicit family-level benchmark convention is attached.",
        ],
        "external_source_targets": [
            "docs/data/external/condensed_matter/superconductivity/mcmillan_1968/source_record.json",
            "docs/data/external/condensed_matter/superconductivity/allen_dynes_1975/source_record.json",
            "docs/data/external/condensed_matter/superconductivity/nims_supercon/source_record.json",
        ],
        "claim_boundary": (
            "This packet is a workflow aid for the A15 blocker pair only. "
            "It does not certify either row as source-locked until row-level evidence is attached."
        ),
    }
    A15_PACKET_PATH.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    return packet


def build_vanadium_candidate_patch_preview(
    vanadium_source_lock_packet: dict | None,
) -> dict | None:
    if not vanadium_source_lock_packet:
        return None

    current = vanadium_source_lock_packet["current_row_package"]
    candidate = vanadium_source_lock_packet["candidate_row_package"]
    proxy = vanadium_source_lock_packet["proxy_sensitivity"]

    preview = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "material": "Vanadium (V)",
        "purpose": "Candidate working-copy patch preview pending source confirmation.",
        "current_working_row": {
            "theta_D_K": current["theta_D_K"],
            "lambda_ep": current["lambda_ep"],
            "mu_star": current["mu_star"],
        },
        "proposed_if_source_confirms": {
            "theta_D_K": current["theta_D_K"],
            "lambda_ep": candidate["recommended_lambda_ep"],
            "mu_star": current["mu_star"],
        },
        "projected_gate_impact": {
            "raw_relative_error_percent": vanadium_source_lock_packet["status_summary"][
                "raw_relative_error_percent"
            ],
            "projected_relative_error_percent": vanadium_source_lock_packet["status_summary"][
                "provisional_relative_error_percent"
            ],
            "preferred_proxy_under_internal_sensitivity": proxy[
                "preferred_proxy_under_internal_sensitivity"
            ],
        },
        "change_policy": {
            "fields_safe_to_patch_if_confirmed": ["lambda_ep"],
            "fields_to_hold_constant_until_source_confirms": ["theta_D_K", "mu_star"],
            "fields_that_must_be_attached_to_row_evidence_first": [
                "Tc_observed identity",
                "lambda_ep citation compatible with chosen phonon proxy",
            ],
        },
        "claim_boundary": (
            "This is a patch preview only. It must not be applied to the working copy until "
            "row-level evidence confirms the proposed field values and proxy convention."
        ),
    }
    VANADIUM_PATCH_PREVIEW_PATH.write_text(json.dumps(preview, indent=2), encoding="utf-8")
    return preview


def build_a15_candidate_patch_preview(
    a15_external_resolution_packet: dict | None,
) -> dict | None:
    if not a15_external_resolution_packet:
        return None

    row_previews = []
    for row in a15_external_resolution_packet.get("row_packets", []):
        row_previews.append(
            {
                "name": row["name"],
                "current_working_row": row["current_row_package"],
                "proposed_if_source_confirms": None,
                "projected_gate_impact": {
                    "raw_relative_error_percent": row["status_summary"]["raw_relative_error_percent"],
                    "projected_relative_error_percent": row["status_summary"][
                        "provisional_relative_error_percent"
                    ],
                },
                "change_policy": {
                    "fields_safe_to_patch_if_confirmed": [],
                    "fields_blocked_until_external_row_resolution": [
                        "theta_D_K or omega_log_K selection",
                        "lambda_ep",
                        "mu_star",
                    ],
                    "fields_that_must_be_attached_to_row_evidence_first": [
                        "Tc_observed identity",
                        "phonon proxy field and unit basis",
                        "lambda_ep row citation",
                        "mu_star row citation or family convention",
                    ],
                },
                "why_no_patch_preview_yet": (
                    "Internal comparison values exist, but the row still requires explicit external resolution "
                    "before any candidate patch can be proposed honestly."
                ),
            }
        )

    preview = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "material_family": "A15 residual blockers",
        "purpose": "Conditional patch preview showing why the A15 rows are not yet patchable.",
        "status_summary": a15_external_resolution_packet["status_summary"],
        "row_previews": row_previews,
        "claim_boundary": (
            "This is a blocked patch preview only. It exists to show why no honest row edit can be applied yet "
            "for the A15 pair without external row evidence."
        ),
    }
    A15_PATCH_PREVIEW_PATH.write_text(json.dumps(preview, indent=2), encoding="utf-8")
    return preview


def build_row_evidence_intake_stub(
    vanadium_source_lock_packet: dict | None,
    a15_external_resolution_packet: dict | None,
) -> dict:
    a15_rows = {}
    if a15_external_resolution_packet:
        a15_rows = {
            row["name"]: row for row in a15_external_resolution_packet.get("row_packets", [])
        }

    vanadium_current = (
        vanadium_source_lock_packet.get("current_row_package", {})
        if vanadium_source_lock_packet
        else {}
    )
    vanadium_candidate = (
        vanadium_source_lock_packet.get("candidate_row_package", {})
        if vanadium_source_lock_packet
        else {}
    )
    stub = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Structured intake stub for future row-level evidence before any working-copy edits are applied.",
        "instructions": [
            "Fill one evidence entry per material row and per source artifact.",
            "Do not overwrite working-copy values from this file directly.",
            "Attach source path, source type, field-level value, unit basis, and extraction note first.",
            "Only after evidence review should a row patch preview be promoted into an actual data edit.",
        ],
        "materials": [
            {
                "name": "Vanadium (V)",
                "source_priority": (
                    vanadium_source_lock_packet["status_summary"]["source_priority"]
                    if vanadium_source_lock_packet
                    else "borderline_source_lock_required"
                ),
                "recommended_starting_point": (
                    "Check the Tc row identity and Theta_D_K-backed lambda_ep citation first."
                ),
                    "evidence_entries": [
                        {
                            "field": "Tc_observed",
                            "status": "working_copy_context_present",
                            "source_type": "working_copy_row_packet",
                            "source_path_or_doi": str(VANADIUM_PACKET_PATH),
                            "original_row_identifier": "MIT Junior Lab cited row identity still unlocked",
                            "extracted_value": 5.36,
                            "unit_basis": "K",
                            "extraction_note": "Working-copy Tc is present in the Vanadium packet, but the cited upstream/literature row still needs to be attached.",
                        },
                        {
                            "field": "Theta_D_K",
                            "status": "working_copy_context_present",
                            "source_type": "working_copy_row_packet",
                            "source_path_or_doi": str(VANADIUM_PACKET_PATH),
                            "original_row_identifier": "raw benchmark row with proxy choice still open",
                            "extracted_value": vanadium_current.get("theta_D_K"),
                            "unit_basis": "K",
                            "extraction_note": "Theta_D_K is present in the working row, but source review must confirm whether Debye temperature is the correct proxy for this material row.",
                        },
                        {
                            "field": "lambda_ep",
                            "status": "working_copy_context_present",
                            "source_type": "working_copy_row_packet",
                            "source_path_or_doi": str(VANADIUM_PACKET_PATH),
                            "original_row_identifier": "raw benchmark row plus internal candidate comparison",
                            "extracted_value": {
                                "raw_lambda_ep": vanadium_current.get("lambda_ep"),
                                "candidate_lambda_ep": vanadium_candidate.get("recommended_lambda_ep"),
                                "inverse_required_lambda_ep": vanadium_candidate.get("inverse_required_lambda_ep"),
                            },
                            "unit_basis": "dimensionless",
                            "extraction_note": "Internal packet narrows the likely lambda range, but the cited row value is not source-locked yet.",
                        },
                        {
                            "field": "mu_star",
                            "status": "working_copy_context_present",
                            "source_type": "working_copy_row_packet",
                            "source_path_or_doi": str(VANADIUM_PACKET_PATH),
                            "original_row_identifier": "working benchmark convention",
                            "extracted_value": vanadium_current.get("mu_star"),
                            "unit_basis": "dimensionless",
                            "extraction_note": "Current packet retains mu_star as a working convention until a row-specific citation is attached.",
                        },
                    ],
                },
                {
                "name": "Nb3Sn",
                "source_priority": "external_resolution_required",
                "recommended_starting_point": "Resolve Tc row identity and phonon proxy convention before any parameter patching.",
                    "evidence_entries": [
                        {
                            "field": "Tc_observed",
                            "status": "working_copy_context_present",
                            "source_type": "working_copy_row_packet",
                            "source_path_or_doi": str(A15_PACKET_PATH),
                            "original_row_identifier": "Matthias 1954 cited row identity still unlocked",
                            "extracted_value": 18.3,
                            "unit_basis": "K",
                            "extraction_note": "Working-copy Tc is known, but the exact source row still needs to be attached before patch review.",
                        },
                        {
                            "field": "Theta_D_K_or_omega_log_K",
                            "status": "proxy_unresolved",
                            "source_type": "working_copy_and_internal_comparison",
                            "source_path_or_doi": str(A15_PACKET_PATH),
                            "original_row_identifier": "A15 proxy convention unresolved",
                            "extracted_value": {
                                "raw_theta_D_K": a15_rows.get("Nb3Sn", {}).get("current_row_package", {}).get("theta_D_K"),
                                "comparison_omega_log_K": a15_rows.get("Nb3Sn", {}).get("internal_comparison_package", {}).get("comparison_omega_log_K"),
                            },
                            "unit_basis": "K",
                            "extraction_note": "Both Debye and omega_log proxy candidates are known internally, but the source-backed proxy convention for Nb3Sn is unresolved.",
                        },
                        {
                            "field": "lambda_ep",
                            "status": "working_copy_context_present",
                            "source_type": "working_copy_and_internal_comparison",
                            "source_path_or_doi": str(A15_PACKET_PATH),
                            "original_row_identifier": "raw row plus internal comparison candidate",
                            "extracted_value": {
                                "raw_lambda_ep": a15_rows.get("Nb3Sn", {}).get("current_row_package", {}).get("lambda_ep"),
                                "comparison_lambda_ep": a15_rows.get("Nb3Sn", {}).get("internal_comparison_package", {}).get("comparison_lambda_ep"),
                                "inverse_required_lambda_ep": a15_rows.get("Nb3Sn", {}).get("internal_comparison_package", {}).get("inverse_required_lambda_ep"),
                            },
                            "unit_basis": "dimensionless",
                            "extraction_note": "Internal comparison narrows the disagreement, but no external row has yet certified the lambda value.",
                        },
                        {
                            "field": "mu_star",
                            "status": "working_copy_context_present",
                            "source_type": "working_copy_row_packet",
                            "source_path_or_doi": str(A15_PACKET_PATH),
                            "original_row_identifier": "family-level working convention",
                            "extracted_value": a15_rows.get("Nb3Sn", {}).get("current_row_package", {}).get("mu_star"),
                            "unit_basis": "dimensionless",
                            "extraction_note": "Current A15 packet keeps mu_star as a working convention; a row-specific citation is still required.",
                        },
                    ],
                },
            {
                "name": "Nb3Ge",
                "source_priority": "external_resolution_required",
                "recommended_starting_point": "Resolve Tc row identity and phonon proxy convention before any parameter patching.",
                    "evidence_entries": [
                        {
                            "field": "Tc_observed",
                            "status": "working_copy_context_present",
                            "source_type": "working_copy_row_packet",
                            "source_path_or_doi": str(A15_PACKET_PATH),
                            "original_row_identifier": "Gavaler 1973 cited row identity still unlocked",
                            "extracted_value": 23.2,
                            "unit_basis": "K",
                            "extraction_note": "Working-copy Tc is known, but the exact source row still needs to be attached before patch review.",
                        },
                        {
                            "field": "Theta_D_K_or_omega_log_K",
                            "status": "proxy_unresolved",
                            "source_type": "working_copy_and_internal_comparison",
                            "source_path_or_doi": str(A15_PACKET_PATH),
                            "original_row_identifier": "A15 proxy convention unresolved",
                            "extracted_value": {
                                "raw_theta_D_K": a15_rows.get("Nb3Ge", {}).get("current_row_package", {}).get("theta_D_K"),
                                "comparison_omega_log_K": a15_rows.get("Nb3Ge", {}).get("internal_comparison_package", {}).get("comparison_omega_log_K"),
                            },
                            "unit_basis": "K",
                            "extraction_note": "Both Debye and omega_log proxy candidates are known internally, but the source-backed proxy convention for Nb3Ge is unresolved.",
                        },
                        {
                            "field": "lambda_ep",
                            "status": "working_copy_context_present",
                            "source_type": "working_copy_and_internal_comparison",
                            "source_path_or_doi": str(A15_PACKET_PATH),
                            "original_row_identifier": "raw row plus internal comparison candidate",
                            "extracted_value": {
                                "raw_lambda_ep": a15_rows.get("Nb3Ge", {}).get("current_row_package", {}).get("lambda_ep"),
                                "comparison_lambda_ep": a15_rows.get("Nb3Ge", {}).get("internal_comparison_package", {}).get("comparison_lambda_ep"),
                                "inverse_required_lambda_ep": a15_rows.get("Nb3Ge", {}).get("internal_comparison_package", {}).get("inverse_required_lambda_ep"),
                            },
                            "unit_basis": "dimensionless",
                            "extraction_note": "Internal comparison narrows the disagreement, but no external row has yet certified the lambda value.",
                        },
                        {
                            "field": "mu_star",
                            "status": "working_copy_context_present",
                            "source_type": "working_copy_row_packet",
                            "source_path_or_doi": str(A15_PACKET_PATH),
                            "original_row_identifier": "family-level working convention",
                            "extracted_value": a15_rows.get("Nb3Ge", {}).get("current_row_package", {}).get("mu_star"),
                            "unit_basis": "dimensionless",
                            "extraction_note": "Current A15 packet keeps mu_star as a working convention; a row-specific citation is still required.",
                        },
                    ],
                },
        ],
        "claim_boundary": (
            "This intake file is for evidence collection only. Filling it does not by itself authorize "
            "a row edit or claim upgrade."
        ),
    }
    ROW_EVIDENCE_INTAKE_PATH.write_text(json.dumps(stub, indent=2), encoding="utf-8")
    return stub


def build_row_evidence_readiness_matrix(row_evidence_intake_stub: dict) -> dict:
    readiness_rows = []
    for material in row_evidence_intake_stub.get("materials", []):
        entries = material.get("evidence_entries", [])
        pending_fields = [entry["field"] for entry in entries if entry.get("status") != "complete"]
        context_fields = [
            entry["field"] for entry in entries if entry.get("status") not in {"pending", "complete"}
        ]
        ready_for_patch = len(pending_fields) == 0
        readiness_rows.append(
            {
                "name": material["name"],
                "source_priority": material["source_priority"],
                "recommended_starting_point": material["recommended_starting_point"],
                "fields_total": len(entries),
                "fields_complete": sum(1 for entry in entries if entry.get("status") == "complete"),
                "fields_with_working_context": sum(
                    1 for entry in entries if entry.get("status") not in {"pending", "complete"}
                ),
                "fields_pending": len(pending_fields),
                "pending_fields": pending_fields,
                "context_only_fields": context_fields,
                "ready_for_patch_review": ready_for_patch,
                "blocking_reason": (
                    None
                    if ready_for_patch
                    else "Evidence intake still has pending fields; patch review must stay blocked."
                ),
            }
        )

    matrix = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Readiness matrix for row-level evidence before patch review.",
        "summary": {
            "rows_total": len(readiness_rows),
            "rows_ready_for_patch_review": sum(
                1 for row in readiness_rows if row["ready_for_patch_review"]
            ),
            "rows_blocked_by_pending_evidence": sum(
                1 for row in readiness_rows if not row["ready_for_patch_review"]
            ),
        },
        "readiness_rows": readiness_rows,
        "claim_boundary": (
            "This matrix is an evidence-readiness control layer only. "
            "A row marked ready still requires human or scripted source review before editing."
        ),
    }
    ROW_EVIDENCE_READINESS_PATH.write_text(json.dumps(matrix, indent=2), encoding="utf-8")
    return matrix


def build_row_evidence_execution_queue(
    row_evidence_intake_stub: dict, row_evidence_readiness_matrix: dict
) -> dict:
    materials_by_name = {
        material["name"]: material for material in row_evidence_intake_stub.get("materials", [])
    }
    queue_rows = []
    for row in row_evidence_readiness_matrix.get("readiness_rows", []):
        material = materials_by_name.get(row["name"], {})
        entries = material.get("evidence_entries", [])
        primary_targets = [entry["field"] for entry in entries if entry.get("status") != "complete"][:2]
        source_paths = sorted(
            {
                entry.get("source_path_or_doi")
                for entry in entries
                if entry.get("source_path_or_doi")
            }
        )
        if row["name"] == "Vanadium (V)":
            queue_class = "borderline_single_row_source_lock"
            next_action = "Attach Tc row identity plus Theta_D_K-backed lambda_ep citation from one compatible source row."
        else:
            queue_class = "a15_external_resolution_pair"
            next_action = "Resolve Tc row identity and phonon proxy convention before accepting any lambda_ep or mu_star patch."

        queue_rows.append(
            {
                "name": row["name"],
                "source_priority": row["source_priority"],
                "queue_class": queue_class,
                "fields_total": row["fields_total"],
                "fields_complete": row["fields_complete"],
                "fields_with_working_context": row["fields_with_working_context"],
                "pending_fields": row["pending_fields"],
                "primary_evidence_targets": primary_targets,
                "context_only_fields": row["context_only_fields"],
                "candidate_source_packets": source_paths,
                "next_action": next_action,
                "ready_for_patch_review": row["ready_for_patch_review"],
                "claim_boundary": (
                    "This queue is for evidence collection sequencing only. "
                    "It does not authorize a working-copy edit."
                ),
            }
        )

    priority_rank = {
        "borderline_source_lock_required": 0,
        "external_resolution_required": 1,
    }
    queue_rows.sort(key=lambda item: (priority_rank.get(item["source_priority"], 99), item["name"]))

    queue = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Execution queue for the next row-evidence collection pass before any patch review.",
        "summary": {
            "rows_total": len(queue_rows),
            "rows_with_working_context": sum(
                1 for row in queue_rows if row["fields_with_working_context"] > 0
            ),
            "rows_ready_for_patch_review": sum(
                1 for row in queue_rows if row["ready_for_patch_review"]
            ),
            "top_priority_row": queue_rows[0]["name"] if queue_rows else None,
        },
        "queue_rows": queue_rows,
        "claim_boundary": (
            "This queue sequences evidence work only. "
            "Source-complete review is still required before any row edit."
        ),
    }
    ROW_EVIDENCE_EXECUTION_QUEUE_PATH.write_text(json.dumps(queue, indent=2), encoding="utf-8")
    return queue


def build_row_evidence_source_review_packets(
    row_evidence_intake_stub: dict, row_evidence_execution_queue: dict
) -> dict:
    materials_by_name = {
        material["name"]: material for material in row_evidence_intake_stub.get("materials", [])
    }
    review_rows = []
    for queue_row in row_evidence_execution_queue.get("queue_rows", []):
        material = materials_by_name.get(queue_row["name"], {})
        source_review_fields = []
        for entry in material.get("evidence_entries", []):
            source_review_fields.append(
                {
                    "field": entry["field"],
                    "current_status": entry.get("status"),
                    "working_context_value": entry.get("extracted_value"),
                    "working_context_note": entry.get("extraction_note"),
                    "required_source_fields": [
                        "source_title_or_doi",
                        "table_or_figure_identifier",
                        "row_locator",
                        "extracted_value",
                        "unit_basis",
                        "compatibility_note_with_working_copy",
                    ],
                    "review_stub": {
                        "source_title_or_doi": None,
                        "table_or_figure_identifier": None,
                        "row_locator": None,
                        "extracted_value": None,
                        "unit_basis": None,
                        "compatibility_note_with_working_copy": None,
                        "review_status": "pending_source_attachment",
                    },
                }
            )

        review_rows.append(
            {
                "name": queue_row["name"],
                "source_priority": queue_row["source_priority"],
                "queue_class": queue_row["queue_class"],
                "next_action": queue_row["next_action"],
                "candidate_source_packets": queue_row["candidate_source_packets"],
                "primary_evidence_targets": queue_row["primary_evidence_targets"],
                "source_review_fields": source_review_fields,
                "claim_boundary": (
                    "These review packets are structured attachment templates only. "
                    "They do not certify any field until a real source row is attached and reviewed."
                ),
            }
        )

    packets = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Structured source-review packets for attaching real row evidence field by field.",
        "summary": {
            "rows_total": len(review_rows),
            "top_priority_row": review_rows[0]["name"] if review_rows else None,
            "fields_requiring_source_attachment": sum(
                len(row["source_review_fields"]) for row in review_rows
            ),
        },
        "review_rows": review_rows,
        "claim_boundary": (
            "These packets formalize the next source-review pass only. "
            "They do not authorize a row patch or claim upgrade."
        ),
    }
    ROW_EVIDENCE_SOURCE_REVIEW_PACKET_PATH.write_text(
        json.dumps(packets, indent=2), encoding="utf-8"
    )
    return packets


def build_row_evidence_decision_gate(row_evidence_source_review_packets: dict) -> dict:
    decision_rows = []
    for row in row_evidence_source_review_packets.get("review_rows", []):
        if row["name"] == "Vanadium (V)":
            gate_questions = [
                "Does one source row identify the observed Tc value unambiguously?",
                "Does the same source family support Theta_D_K as the active phonon proxy for this row?",
                "Is the cited lambda_ep compatible with that same proxy convention?",
                "Can mu_star remain the working convention, or does the source row specify a different convention?",
            ]
        else:
            gate_questions = [
                "Does one source row identify the observed Tc value unambiguously?",
                "Is the row benchmark based on Theta_D_K, omega_log_K, or another phonon proxy convention?",
                "Is the cited lambda_ep extracted under the same proxy convention as the chosen row?",
                "Is mu_star explicitly given, or must it be carried as a declared family convention?",
            ]

        decision_rows.append(
            {
                "name": row["name"],
                "source_priority": row["source_priority"],
                "queue_class": row["queue_class"],
                "gate_questions": gate_questions,
                "required_gate_status": {
                    "row_identity_locked": False,
                    "proxy_convention_locked": False,
                    "unit_basis_checked": False,
                    "field_compatibility_checked": False,
                    "eligible_for_patch_review": False,
                },
                "current_decision": "blocked_pending_source_review",
                "claim_boundary": (
                    "This decision gate is a review-control layer only. "
                    "It records what must be true before patch review can even begin."
                ),
            }
        )

    decision_gate = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Decision gate for determining whether attached row evidence is strong enough to enter patch review.",
        "summary": {
            "rows_total": len(decision_rows),
            "rows_eligible_for_patch_review": sum(
                1 for row in decision_rows if row["required_gate_status"]["eligible_for_patch_review"]
            ),
            "rows_blocked_pending_source_review": sum(
                1 for row in decision_rows if row["current_decision"] == "blocked_pending_source_review"
            ),
            "top_priority_row": decision_rows[0]["name"] if decision_rows else None,
        },
        "decision_rows": decision_rows,
        "claim_boundary": (
            "This gate cannot promote a row by itself. "
            "It exists to prevent source attachments from being mistaken for approved patches."
        ),
    }
    ROW_EVIDENCE_DECISION_GATE_PATH.write_text(
        json.dumps(decision_gate, indent=2), encoding="utf-8"
    )
    return decision_gate


def build_topic_source_evidence_intake_stub() -> dict:
    stub = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Source evidence intake before claim upgrades across superconductivity benchmark and theory branches.",
        "source_targets": [
            {
                "name": "Raw McMillan benchmark package",
                "priority": "immediate",
                "status_hint": "working_copy_benchmark_with_external_records",
                "evidence_entries": [
                    "working_copy_table_path",
                    "source_lock_manifest_path",
                    "benchmark_role_note",
                    "unit_basis",
                    "row_normalization_dependency",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Allen-Dynes or comprehensive parameter package",
                "priority": "high",
                "status_hint": "topic_local_comprehensive_package",
                "evidence_entries": [
                    "comprehensive_dataset_path",
                    "upstream_source_record",
                    "row_normalization_status",
                    "unit_basis",
                    "held_out_validation_requirement",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Conventional-row normalization evidence package",
                "priority": "high",
                "status_hint": "in_progress_row_resolution",
                "evidence_entries": [
                    "row_evidence_intake_path",
                    "row_evidence_readiness_path",
                    "vanadium_packet_path",
                    "a15_packet_path",
                    "source_review_status",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "High-Tc and hydride benchmark package",
                "priority": "medium",
                "status_hint": "not_primary_gated",
                "evidence_entries": [
                    "dataset_identity",
                    "upstream_source_record",
                    "mechanism_scope",
                    "unit_basis",
                    "artifact_path",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "UET coherence or relativistic correction package",
                "priority": "medium",
                "status_hint": "heuristic_branch",
                "evidence_entries": [
                    "formula_surface",
                    "parameter_origin_note",
                    "held_out_test_artifact",
                    "unit_basis",
                    "calibration_status",
                    "upgrade_requirement",
                ],
            },
        ],
        "claim_boundary": (
            "This intake stub organizes provenance and branch-upgrade work only. "
            "It does not itself turn the superconductivity topic into a predictive theory."
        ),
    }
    TOPIC_SOURCE_EVIDENCE_INTAKE_PATH.write_text(json.dumps(stub, indent=2), encoding="utf-8")
    return stub


def build_topic_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "Raw McMillan benchmark package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "row_normalization_dependency",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The raw gate is runnable, but row-level provenance normalization is still incomplete and the benchmark remains FAIL.",
        },
        {
            "name": "Allen-Dynes or comprehensive parameter package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 3,
            "fields_pending": 3,
            "pending_fields": [
                "row_normalization_status",
                "held_out_validation_requirement",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The comprehensive package exists, but it is still a topic-local package without source-backed row normalization and held-out validation.",
        },
        {
            "name": "Conventional-row normalization evidence package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 4,
            "fields_pending": 2,
            "pending_fields": [
                "source_review_status",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The row-evidence workflow is in place, but the remaining Vanadium and A15 source checks are still pending.",
        },
        {
            "name": "High-Tc and hydride benchmark package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 1,
            "fields_pending": 5,
            "pending_fields": [
                "upstream_source_record",
                "mechanism_scope",
                "unit_basis",
                "artifact_path",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "High-Tc and hydride branches are present in data files but are not yet part of a primary gated benchmark package.",
        },
        {
            "name": "UET coherence or relativistic correction package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 2,
            "fields_pending": 4,
            "pending_fields": [
                "parameter_origin_note",
                "held_out_test_artifact",
                "calibration_status",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The correction terms remain heuristic and do not yet have a held-out validation artifact.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    matrix = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Readiness matrix for source-evidence review across superconductivity benchmark and theory branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": (
            "A ready row has enough provenance structure for source review. "
            "It does not itself upgrade a claim."
        ),
    }
    TOPIC_SOURCE_EVIDENCE_READINESS_PATH.write_text(json.dumps(matrix, indent=2), encoding="utf-8")
    return matrix


def build_topic_branch_claim_gate() -> dict:
    allen_dynes_artifact = load_json(ALLEN_DYNES_ARTIFACT_PATH)
    allen_dynes_status = (
        allen_dynes_artifact.get("model_gate_status")
        if allen_dynes_artifact
        else "artifact_missing"
    )
    allen_dynes_strict_summary = (
        allen_dynes_artifact.get("strict_source_locked_summary", {})
        if allen_dynes_artifact
        else {}
    )
    gate = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "purpose": "Claim gate for separate superconductivity benchmark and theory branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 2 if allen_dynes_status == "PASS" else 1,
            "blocked_for_strong_claims": 4 if allen_dynes_status == "PASS" else 5,
            "raw_mcmillan_topic_gate": "controls_topic_level_status",
            "allen_dynes_branch_gate": allen_dynes_status,
        },
        "branches": [
            {
                "branch": "Raw McMillan baseline branch",
                "status": "accepted_failure_diagnostic_only",
                "allowed_usage_now": "Internal baseline diagnostic and blocker decomposition only.",
                "blocker_to_stronger_claim": "Need row-level source normalization and a passing or better-bounded benchmark package before promotion.",
            },
            {
                "branch": "Row-normalized conventional superconductors branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "In-progress source-normalization workflow only.",
                "blocker_to_stronger_claim": "Need completed row evidence, normalized inputs, and rerun benchmark results.",
            },
            {
                "branch": "Allen-Dynes Nb3Sn smoke-test branch",
                "status": (
                    "accepted_branch_smoke_test_only"
                    if allen_dynes_status == "PASS"
                    else "blocked_pending_branch_artifact"
                ),
                "artifact_path": str(ALLEN_DYNES_ARTIFACT_PATH),
                "artifact_sha256": hash_file(ALLEN_DYNES_ARTIFACT_PATH),
                "strict_source_locked_summary": allen_dynes_strict_summary,
                "allowed_usage_now": (
                    "Separate Nb3Sn Allen-Dynes smoke-test branch only; not topic-level PASS."
                    if allen_dynes_status == "PASS"
                    else "Model formulation and future benchmark path only."
                ),
                "blocker_to_stronger_claim": "Need broader source-locked coverage and held-out rows before any topic-level upgrade.",
            },
            {
                "branch": "UET coherence or relativistic correction branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Heuristic bridge only.",
                "blocker_to_stronger_claim": "Need parameter-origin clarity and out-of-sample validation.",
            },
            {
                "branch": "High-Tc and hydride branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Future hardening target only.",
                "blocker_to_stronger_claim": "Need separate source-backed gates and mechanism-appropriate benchmarks.",
            },
            {
                "branch": "Universal superconductivity theory claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by the current evidence package.",
                "blocker_to_stronger_claim": "Need successful source-backed validation across conventional and non-BCS regimes plus theory closure.",
            },
        ],
        "claim_boundary": (
            "This gate cannot raise the topic above the current baseline-diagnostic status "
            "while the raw McMillan artifact remains FAIL."
        ),
    }
    TOPIC_BRANCH_CLAIM_GATE_PATH.write_text(json.dumps(gate, indent=2), encoding="utf-8")
    return gate


def build_vanadium_source_lock_decision(rows: list[dict]) -> dict:
    loaded_packets = {
        name: load_json(path)
        for name, path in VANADIUM_EXTERNAL_PACKET_PATHS.items()
    }
    patch_decision = loaded_packets.get("patch_block_decision") or {}
    compatibility_packet = loaded_packets.get("compatibility_review_packet") or {}
    primary_page_capture = loaded_packets.get("primary_page_capture_record") or {}
    primary_packet = loaded_packets.get("primary_capture_requirement_packet") or {}
    archive_dossier = loaded_packets.get("archive_dossier") or {}
    raw_row = next((row for row in rows if row.get("name") == "Vanadium (V)"), {})

    archive_targets = archive_dossier.get("archive_targets", [])
    fields_closed_by_primary_capture = set(
        primary_page_capture.get("source_lock_effect", {}).get(
            "fields_closed_by_this_record", []
        )
    )
    pending_archive_fields = [
        target.get("field")
        for target in archive_targets
        if target.get("status") != "complete"
        and target.get("field") not in fields_closed_by_primary_capture
        and not (
            target.get("field") == "Theta_D_K"
            and "Theta_D_K_or_proxy_context" in fields_closed_by_primary_capture
        )
    ]
    compatibility_summary = compatibility_packet.get("compatibility_summary", {})
    field_review = compatibility_packet.get("field_review", [])
    fields_primary_page_confirmed = compatibility_summary.get(
        "fields_primary_page_confirmed", []
    )
    patch_blocked = patch_decision.get("current_decision") == "blocked_do_not_apply_preview"
    if patch_blocked:
        source_lock_state = "PATCH_BLOCKED"
    elif pending_archive_fields:
        source_lock_state = "MORE_SOURCE_REQUIRED"
    else:
        source_lock_state = "PATCH_ALLOWED"

    decision = {
        "schema_version": "1.0",
        "topic": "0.4_Superconductivity_Superfluids",
        "material": "Vanadium (V)",
        "purpose": "Machine-readable Vanadium source-lock decision for the raw McMillan gate.",
        "decision": source_lock_state,
        "working_row_mutated": False,
        "raw_mcmillan_row_status": "unchanged_due_to_source_lock_blocker",
        "current_working_row": {
            "Tc_observed_K": raw_row.get("Tc_observed_K"),
            "Theta_D_K": raw_row.get("Theta_D_K"),
            "lambda_ep": raw_row.get("lambda_ep"),
            "mu_star": raw_row.get("mu_star"),
            "relative_error_percent": raw_row.get("relative_error_percent"),
            "source": raw_row.get("source"),
        },
        "external_capture_reference": compatibility_packet.get(
            "external_capture_reference", {}
        ),
        "primary_page_capture": {
            "path": str(VANADIUM_EXTERNAL_PACKET_PATHS["primary_page_capture_record"]),
            "sha256": hash_file(
                VANADIUM_EXTERNAL_PACKET_PATHS["primary_page_capture_record"]
            ),
            "status": primary_page_capture.get(
                "source_lock_effect", {}
            ).get("citation_integrity_gate"),
            "fields_closed_by_this_record": sorted(fields_closed_by_primary_capture),
            "fields_not_closed_by_this_record": primary_page_capture.get(
                "source_lock_effect", {}
            ).get("fields_not_closed_by_this_record", []),
        },
        "field_decisions": [
            {
                "field": item.get("field"),
                "compatibility_status": item.get("compatibility_status"),
                "working_value": item.get("working_value"),
                "external_value": item.get("external_value"),
                "alternative_external_value": item.get("alternative_external_value"),
                "review_note": item.get("review_note"),
            }
            for item in field_review
        ],
        "source_lock_blockers": {
            "pending_archive_fields": pending_archive_fields,
            "fields_primary_page_confirmed": fields_primary_page_confirmed,
            "fields_requiring_primary_page_confirmation": compatibility_summary.get(
                "fields_requiring_primary_page_confirmation", []
            ),
            "fields_requiring_convention_review": compatibility_summary.get(
                "fields_requiring_convention_review", []
            ),
            "blocked_preview_fields": patch_decision.get("blocked_preview_fields", []),
            "why_blocked": patch_decision.get("why_blocked", []),
        },
        "primary_capture_requirements": {
            "target": primary_packet.get("primary_source_target", {}),
            "required_elements": primary_packet.get(
                "required_primary_capture_elements", []
            ),
            "success_condition": primary_packet.get("success_condition"),
        },
        "safe_interim_policy": patch_decision.get(
            "safe_interim_policy",
            {
                "keep_working_row_unchanged": True,
                "allow_patch_preview_for_execution": False,
            },
        ),
        "packet_inputs": {
            name: {
                "path": str(path),
                "sha256": hash_file(path),
                "status": "present" if path.exists() else "missing",
            }
            for name, path in VANADIUM_EXTERNAL_PACKET_PATHS.items()
        },
        "claim_boundary": (
            "This decision records why Vanadium cannot be patched yet. Primary Tc "
            "and Theta/proxy context are now confirmed, but lambda_ep and mu_star "
            "remain convention-conflicted. It does not authorize any working-row "
            "edit and does not reduce the raw McMillan FAIL."
        ),
    }
    VANADIUM_SOURCE_LOCK_DECISION_PATH.write_text(
        json.dumps(decision, indent=2), encoding="utf-8"
    )
    return decision


def build_evidence_lanes(
    *,
    status: str,
    avg_err: float,
    rows: list[dict],
    skipped_rows: list[dict],
    failure_analysis: dict,
    provisional_normalized_table: dict,
    provisional_evaluation: dict,
    row_evidence_readiness_matrix: dict,
    row_evidence_decision_gate: dict,
    vanadium_source_lock_decision: dict,
) -> dict:
    allen_dynes_artifact = load_json(ALLEN_DYNES_ARTIFACT_PATH)
    raw_failed_rows = [row for row in rows if not row["within_20_percent"]]
    row_eligibility_report = build_raw_mcmillan_row_eligibility_report(
        rows, skipped_rows
    )
    return {
        "schema_version": "1.0",
        "raw_mcmillan_gate": {
            "lane_role": "primary topic gate",
            "model_gate_status": status,
            "row_eligibility_summary": row_eligibility_report["summary"],
            "claim_class": (
                "internal baseline diagnostic"
                if status == "PASS"
                else "model-baseline blocker"
            ),
            "thresholds": {
                "average_relative_error_percent_max": 20.0,
                "per_material_relative_error_percent_max": 20.0,
            },
            "metrics": {
                "average_relative_error_percent": avg_err,
                "materials_tested": len(rows),
                "materials_within_20_percent": sum(
                    1 for row in rows if row["within_20_percent"]
                ),
                "failed_material_count": len(raw_failed_rows),
                "materials_skipped_from_raw_mcmillan_gate": len(skipped_rows),
            },
            "worst_materials": failure_analysis["worst_materials"],
            "blocker_reason": failure_analysis["primary_failure_reason"],
            "claim_boundary": (
                "This lane controls the topic-level benchmark status. It remains FAIL "
                "until the fixed average and per-material gates are met without hiding rows."
            ),
        },
        "provisional_normalized_sensitivity": {
            "lane_role": "internal sensitivity only",
            "model_gate_status": "NON_GATING",
            "metrics": {
                "average_relative_error_percent": provisional_evaluation[
                    "average_relative_error_percent"
                ],
                "materials_tested": provisional_evaluation["materials_tested"],
                "materials_within_20_percent": provisional_evaluation[
                    "materials_within_20_percent"
                ],
                "rows": len(provisional_normalized_table["rows"]),
            },
            "claim_class": "sensitivity analysis only",
            "claim_boundary": (
                "This lane can identify row-package drift, but it cannot replace or "
                "override the raw McMillan gate because its substitutions are not "
                "fully source-backed."
            ),
        },
        "allen_dynes_nb3sn_smoke_test": {
            "lane_role": "separate branch gate",
            "artifact_path": str(ALLEN_DYNES_ARTIFACT_PATH),
            "artifact_sha256": hash_file(ALLEN_DYNES_ARTIFACT_PATH),
            "model_gate_status": (
                allen_dynes_artifact.get("model_gate_status")
                if allen_dynes_artifact
                else "MISSING_ARTIFACT"
            ),
            "strict_source_locked_summary": (
                allen_dynes_artifact.get("strict_source_locked_summary", {})
                if allen_dynes_artifact
                else {}
            ),
            "claim_class": "source-labeled branch smoke test",
            "claim_boundary": (
                "This PASS, when present, is limited to the Nb3Sn Allen-Dynes "
                "smoke-test rows. It does not change the raw McMillan artifact or "
                "promote the full superconductivity topic."
            ),
        },
        "row_resolution_handoff": {
            "lane_role": "source-lock and patch-review control",
            "model_gate_status": "NON_GATING",
            "vanadium_decision": {
                "path": str(VANADIUM_SOURCE_LOCK_DECISION_PATH),
                "sha256": hash_file(VANADIUM_SOURCE_LOCK_DECISION_PATH),
                "decision": vanadium_source_lock_decision["decision"],
                "working_row_mutated": vanadium_source_lock_decision[
                    "working_row_mutated"
                ],
                "source_lock_blockers": vanadium_source_lock_decision[
                    "source_lock_blockers"
                ],
            },
            "row_evidence_readiness_summary": row_evidence_readiness_matrix["summary"],
            "row_evidence_decision_summary": row_evidence_decision_gate["summary"],
            "next_priority": "Vanadium lambda_ep and mu_star convention review, then Nb3Ge source-lock pass.",
            "next_priority_after_wave_2": (
                "Vanadium lambda_ep/mu_star convention review; do not patch "
                "Tc/Theta alone without a coherent row package."
            ),
            "claim_boundary": (
                "This lane can authorize future review work only. No row patch is "
                "allowed until the decision gate changes from blocked to eligible."
            ),
        },
    }


def write_artifact(output_path: Path, avg_err: float, rows: list[dict], skipped_rows: list[dict]) -> None:
    data_path = DATA_DIR / "real_superconductor_data.json"
    source_lock = load_source_lock()
    row_eligibility_report = build_raw_mcmillan_row_eligibility_report(
        rows, skipped_rows
    )
    topic_source_evidence_intake_stub = build_topic_source_evidence_intake_stub()
    topic_source_evidence_readiness_matrix = build_topic_source_evidence_readiness_matrix()
    topic_branch_claim_gate = build_topic_branch_claim_gate()
    failure_analysis = analyze_failures(avg_err, rows)
    row_provenance_manifest = write_row_provenance_manifest(rows, skipped_rows)
    normalization_queue = build_row_normalization_queue(rows, row_provenance_manifest)
    normalization_status = build_row_normalization_status(
        normalization_queue, row_provenance_manifest
    )
    normalization_candidates = build_row_normalization_candidates(normalization_status)
    provisional_normalized_table = build_provisional_normalized_table(
        rows, normalization_candidates
    )
    provisional_evaluation = evaluate_rows(provisional_normalized_table["rows"])
    provisional_residual_blockers = build_provisional_residual_blockers(
        rows, normalization_candidates, provisional_evaluation
    )
    residual_blocker_row_dossiers = build_residual_blocker_row_dossiers(
        provisional_residual_blockers, row_provenance_manifest
    )
    residual_blocker_field_lock_matrix = build_residual_blocker_field_lock_matrix(
        residual_blocker_row_dossiers
    )
    residual_blocker_proxy_sensitivity = build_residual_blocker_proxy_sensitivity(
        residual_blocker_row_dossiers
    )
    vanadium_source_lock_packet = build_vanadium_source_lock_packet(
        residual_blocker_row_dossiers,
        residual_blocker_field_lock_matrix,
        residual_blocker_proxy_sensitivity,
    )
    a15_external_resolution_packet = build_a15_external_resolution_packet(
        residual_blocker_row_dossiers,
        residual_blocker_field_lock_matrix,
    )
    vanadium_candidate_patch_preview = build_vanadium_candidate_patch_preview(
        vanadium_source_lock_packet
    )
    a15_candidate_patch_preview = build_a15_candidate_patch_preview(
        a15_external_resolution_packet
    )
    row_evidence_intake_stub = build_row_evidence_intake_stub(
        vanadium_source_lock_packet,
        a15_external_resolution_packet,
    )
    row_evidence_readiness_matrix = build_row_evidence_readiness_matrix(
        row_evidence_intake_stub
    )
    row_evidence_execution_queue = build_row_evidence_execution_queue(
        row_evidence_intake_stub,
        row_evidence_readiness_matrix,
    )
    row_evidence_source_review_packets = build_row_evidence_source_review_packets(
        row_evidence_intake_stub,
        row_evidence_execution_queue,
    )
    row_evidence_decision_gate = build_row_evidence_decision_gate(
        row_evidence_source_review_packets
    )
    vanadium_source_lock_decision = build_vanadium_source_lock_decision(rows)
    status = failure_analysis["model_gate_status"]
    evidence_lanes = build_evidence_lanes(
        status=status,
        avg_err=avg_err,
        rows=rows,
        skipped_rows=skipped_rows,
        failure_analysis=failure_analysis,
        provisional_normalized_table=provisional_normalized_table,
        provisional_evaluation=provisional_evaluation,
        row_evidence_readiness_matrix=row_evidence_readiness_matrix,
        row_evidence_decision_gate=row_evidence_decision_gate,
        vanadium_source_lock_decision=vanadium_source_lock_decision,
    )
    artifact = {
        "schema_version": "1.4",
        "topic": "0.4_Superconductivity_Superfluids",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.4_Superconductivity_Superfluids/Code/03_Research/Experiment_Superconductor_Data.py",
        "status": status,
        "run_status": "PASS",
        "model_gate_status": status,
        "blocker_class": "model-baseline failure" if status == "FAIL" else None,
        "claim_class": "C internal baseline diagnostic" if status == "PASS" else "model-baseline blocker",
        "inputs": [
            {
                "path": str(data_path),
                "sha256": hash_file(data_path),
                "role": "raw McMillan superconductivity benchmark working copy",
                "data_class": "topic-local working copy generated from in-script rows",
            },
            {
                "path": str(COMPREHENSIVE_DATA_PATH),
                "sha256": hash_file(COMPREHENSIVE_DATA_PATH),
                "role": "cross-dataset provenance drift comparator",
                "data_class": "topic-local broader superconductivity package",
            },
        ],
        "source_lock": {
            "path": str(SOURCE_LOCK_PATH),
            "sha256": hash_file(SOURCE_LOCK_PATH),
            "external_source_records": source_record_hashes(source_lock),
            "derived_inputs": source_lock.get("derived_inputs", []),
        },
        "source_evidence_intake_stub": {
            "path": str(TOPIC_SOURCE_EVIDENCE_INTAKE_PATH),
            "sha256": hash_file(TOPIC_SOURCE_EVIDENCE_INTAKE_PATH),
            "source_targets": [row["name"] for row in topic_source_evidence_intake_stub["source_targets"]],
            "claim_boundary": topic_source_evidence_intake_stub["claim_boundary"],
        },
        "source_evidence_readiness_matrix": {
            "path": str(TOPIC_SOURCE_EVIDENCE_READINESS_PATH),
            "sha256": hash_file(TOPIC_SOURCE_EVIDENCE_READINESS_PATH),
            "summary": topic_source_evidence_readiness_matrix["summary"],
            "claim_boundary": topic_source_evidence_readiness_matrix["claim_boundary"],
        },
        "branch_claim_gate": {
            "path": str(TOPIC_BRANCH_CLAIM_GATE_PATH),
            "sha256": hash_file(TOPIC_BRANCH_CLAIM_GATE_PATH),
            "summary": topic_branch_claim_gate["summary"],
            "claim_boundary": topic_branch_claim_gate["claim_boundary"],
        },
        "raw_mcmillan_row_eligibility_policy": row_eligibility_report["policy"],
        "row_eligibility": row_eligibility_report,
        "thresholds": {
            "average_relative_error_percent_max": 20.0,
            "per_material_relative_error_percent_max": 20.0,
        },
        "metrics": {
            "average_relative_error_percent": avg_err,
            "materials_tested": len(rows),
            "materials_within_20_percent": sum(1 for row in rows if row["within_20_percent"]),
            "materials_skipped_from_raw_mcmillan_gate": len(skipped_rows),
            "materials_excluded_from_raw_mcmillan_gate": row_eligibility_report[
                "summary"
            ]["excluded_rows"],
            "branch_migration_candidates": row_eligibility_report["summary"][
                "branch_migration_candidates"
            ],
            "source_targets_ready_for_review": topic_source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": topic_source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": topic_branch_claim_gate["summary"]["accepted_now"],
        },
        "evidence_lanes": evidence_lanes,
        "vanadium_source_lock_decision": {
            "path": str(VANADIUM_SOURCE_LOCK_DECISION_PATH),
            "sha256": hash_file(VANADIUM_SOURCE_LOCK_DECISION_PATH),
            "decision": vanadium_source_lock_decision["decision"],
            "working_row_mutated": vanadium_source_lock_decision["working_row_mutated"],
            "raw_mcmillan_row_status": vanadium_source_lock_decision[
                "raw_mcmillan_row_status"
            ],
            "source_lock_blockers": vanadium_source_lock_decision[
                "source_lock_blockers"
            ],
            "claim_boundary": vanadium_source_lock_decision["claim_boundary"],
        },
        "failure_analysis": failure_analysis,
        "parameter_mismatch_audit": parameter_mismatch_summary(rows),
        "error_bias_audit": error_bias_summary(rows),
        "type_summary": summarize_group(rows, "type"),
        "source_summary": summarize_group(rows, "source"),
        "row_provenance_manifest": {
            "path": str(ROW_PROVENANCE_PATH),
            "sha256": hash_file(ROW_PROVENANCE_PATH),
            "cross_dataset_comparison": row_provenance_manifest["cross_dataset_comparison"],
            "cross_package_lambda_substitution_audit": row_provenance_manifest[
                "cross_package_lambda_substitution_audit"
            ],
        },
        "row_normalization_queue": {
            "path": str(NORMALIZATION_QUEUE_PATH),
            "sha256": hash_file(NORMALIZATION_QUEUE_PATH),
            "summary": normalization_queue["summary"],
            "top_rows": normalization_queue["queue_rows"][:5],
        },
        "row_normalization_status": {
            "path": str(NORMALIZATION_STATUS_PATH),
            "sha256": hash_file(NORMALIZATION_STATUS_PATH),
            "summary": normalization_status["summary"],
        },
        "row_normalization_candidates": {
            "path": str(NORMALIZATION_CANDIDATES_PATH),
            "sha256": hash_file(NORMALIZATION_CANDIDATES_PATH),
            "summary": normalization_candidates["summary"],
        },
        "provisional_normalized_table": {
            "path": str(PROVISIONAL_NORMALIZED_PATH),
            "sha256": hash_file(PROVISIONAL_NORMALIZED_PATH),
            "summary": {
                "rows": len(provisional_normalized_table["rows"]),
                "internal_consensus_rows": sum(
                    1
                    for row in provisional_normalized_table["rows"]
                    if row["normalization_class"] == "provisional_internal_consensus"
                ),
                "unresolved_rows": sum(
                    1
                    for row in provisional_normalized_table["rows"]
                    if row["normalization_class"] == "unresolved_kept_raw"
                ),
            },
            "sensitivity_evaluation": provisional_evaluation,
            "claim_boundary": (
                "This provisional evaluation is an internal sensitivity check only and must not replace the raw-gate artifact."
            ),
        },
        "provisional_residual_blockers": {
            "path": str(RESIDUAL_BLOCKER_PATH),
            "sha256": hash_file(RESIDUAL_BLOCKER_PATH),
            "summary": provisional_residual_blockers["summary"],
            "top_rows": provisional_residual_blockers["blocker_rows"][:5],
            "claim_boundary": (
                "This residual-blocker map is a workflow decomposition only. "
                "It does not convert provisional substitutions into source-backed rows."
            ),
        },
        "residual_blocker_row_dossiers": {
            "path": str(ROW_DOSSIER_PATH),
            "sha256": hash_file(ROW_DOSSIER_PATH),
            "summary": residual_blocker_row_dossiers["summary"],
            "top_rows": residual_blocker_row_dossiers["row_dossiers"][:3],
            "claim_boundary": (
                "These row dossiers are execution packets only. They help focus source checks "
                "but do not authorize editing the raw benchmark rows without upstream evidence."
            ),
        },
        "residual_blocker_field_lock_matrix": {
            "path": str(FIELD_LOCK_MATRIX_PATH),
            "sha256": hash_file(FIELD_LOCK_MATRIX_PATH),
            "summary": residual_blocker_field_lock_matrix["summary"],
            "top_rows": residual_blocker_field_lock_matrix["matrix_rows"][:3],
            "claim_boundary": (
                "This field-lock matrix is a workflow control layer only. "
                "It tracks unresolved fields but does not certify them as source-backed."
            ),
        },
        "residual_blocker_proxy_sensitivity": {
            "path": str(PROXY_SENSITIVITY_PATH),
            "sha256": hash_file(PROXY_SENSITIVITY_PATH),
            "summary": residual_blocker_proxy_sensitivity["summary"],
            "top_rows": residual_blocker_proxy_sensitivity["proxy_rows"][:3],
            "claim_boundary": (
                "This proxy-sensitivity layer is internal only. "
                "It does not decide the authoritative phonon proxy without source-backed row evidence."
            ),
        },
        "vanadium_source_lock_packet": (
            {
                "path": str(VANADIUM_PACKET_PATH),
                "sha256": hash_file(VANADIUM_PACKET_PATH),
                "status_summary": vanadium_source_lock_packet["status_summary"],
                "proxy_sensitivity": vanadium_source_lock_packet["proxy_sensitivity"],
                "claim_boundary": (
                    "This is a focused execution packet for the Vanadium row only. "
                    "It does not certify the row without attached source evidence."
                ),
            }
            if vanadium_source_lock_packet
            else None
        ),
        "a15_external_resolution_packet": (
            {
                "path": str(A15_PACKET_PATH),
                "sha256": hash_file(A15_PACKET_PATH),
                "status_summary": a15_external_resolution_packet["status_summary"],
                "claim_boundary": (
                    "This is a focused execution packet for the A15 blocker pair only. "
                    "It does not certify either row without attached source evidence."
                ),
            }
            if a15_external_resolution_packet
            else None
        ),
        "vanadium_candidate_patch_preview": (
            {
                "path": str(VANADIUM_PATCH_PREVIEW_PATH),
                "sha256": hash_file(VANADIUM_PATCH_PREVIEW_PATH),
                "projected_gate_impact": vanadium_candidate_patch_preview["projected_gate_impact"],
                "claim_boundary": (
                    "This is a patch preview only. It does not authorize changing the working row "
                    "without source confirmation."
                ),
            }
            if vanadium_candidate_patch_preview
            else None
        ),
        "a15_candidate_patch_preview": (
            {
                "path": str(A15_PATCH_PREVIEW_PATH),
                "sha256": hash_file(A15_PATCH_PREVIEW_PATH),
                "status_summary": a15_candidate_patch_preview["status_summary"],
                "claim_boundary": (
                    "This is a blocked patch preview only. It explains why the A15 rows cannot be edited "
                    "honestly yet without external row evidence."
                ),
            }
            if a15_candidate_patch_preview
            else None
        ),
        "row_evidence_intake_stub": {
            "path": str(ROW_EVIDENCE_INTAKE_PATH),
            "sha256": hash_file(ROW_EVIDENCE_INTAKE_PATH),
            "materials": [item["name"] for item in row_evidence_intake_stub["materials"]],
            "claim_boundary": (
                "This intake stub is for evidence capture only. "
                "It does not authorize working-copy edits by itself."
            ),
        },
        "row_evidence_readiness_matrix": {
            "path": str(ROW_EVIDENCE_READINESS_PATH),
            "sha256": hash_file(ROW_EVIDENCE_READINESS_PATH),
            "summary": row_evidence_readiness_matrix["summary"],
            "claim_boundary": (
                "This readiness matrix is a workflow gate only. "
                "It tracks whether evidence fields are still pending before patch review."
            ),
        },
        "row_evidence_execution_queue": {
            "path": str(ROW_EVIDENCE_EXECUTION_QUEUE_PATH),
            "sha256": hash_file(ROW_EVIDENCE_EXECUTION_QUEUE_PATH),
            "summary": row_evidence_execution_queue["summary"],
            "top_rows": row_evidence_execution_queue["queue_rows"][:3],
            "claim_boundary": (
                "This execution queue sequences evidence collection only. "
                "It does not authorize working-copy edits."
            ),
        },
        "row_evidence_source_review_packets": {
            "path": str(ROW_EVIDENCE_SOURCE_REVIEW_PACKET_PATH),
            "sha256": hash_file(ROW_EVIDENCE_SOURCE_REVIEW_PACKET_PATH),
            "summary": row_evidence_source_review_packets["summary"],
            "top_rows": row_evidence_source_review_packets["review_rows"][:2],
            "claim_boundary": (
                "These source-review packets are attachment templates only. "
                "They do not certify a field until a real source row is reviewed."
            ),
        },
        "row_evidence_decision_gate": {
            "path": str(ROW_EVIDENCE_DECISION_GATE_PATH),
            "sha256": hash_file(ROW_EVIDENCE_DECISION_GATE_PATH),
            "summary": row_evidence_decision_gate["summary"],
            "top_rows": row_evidence_decision_gate["decision_rows"][:2],
            "claim_boundary": (
                "This decision gate is a review-control layer only. "
                "It does not authorize a row patch or claim upgrade by itself."
            ),
        },
        "skipped_rows": skipped_rows,
        "results": rows,
        "limitations": [
            "This is a raw McMillan baseline check, not a UET first-principles prediction.",
            "Several lambda_ep and mu_star values are literature/curated working-copy inputs.",
            "High-Tc cuprates with non-BCS mechanisms are skipped by this baseline.",
            "The source-lock manifest records formula and dataset provenance targets, but raw NIMS MDR files are not yet mirrored.",
        ],
        "interpretation": (
            "This artifact supports a raw-baseline failure diagnostic only. "
            "It does not certify row-normalized conventional superconductivity prediction, "
            "Allen-Dynes/UET held-out performance, or universal superconductivity claims."
        ),
        "next_model_hardening_tasks": [
            "Use the inverse-McMillan lambda audit to identify which row-level lambda_ep/Theta_D inputs need upstream normalization.",
            "Normalize row-level material inputs against upstream records or explicit literature tables.",
            "Add a separate Allen-Dynes/UET engine verifier with calibrated-input labels and held-out materials.",
            "Replace broad pass/fail claims in code docs with artifact-linked model-gate status.",
        ],
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Artifact saved to {output_path}")


if __name__ == "__main__":
    # Save data
    save_data()

    # Test McMillan
    print()
    avg_error, result_rows, skipped_rows = test_mcmillan()
    write_artifact(ARTIFACT_PATH, avg_error, result_rows, skipped_rows)

