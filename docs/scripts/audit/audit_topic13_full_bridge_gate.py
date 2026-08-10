"""Build the conservative full Topic 0.13 Core-ready closure gate.

This verifier composes existing evidence. It does not invent a calibration,
promote the selected frozen-C control, or consume the locked holdout.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/topic13_full_thermodynamic_bridge_core_ready_gate.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(rel_path: str) -> tuple[Path, dict[str, Any]]:
    path = ROOT / rel_path
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return path, value


def evidence(rel_path: str, value: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / rel_path
    return {
        "path": rel_path,
        "sha256": sha256(path),
        "summary": summary,
    }


def main() -> int:
    branch_path, branch = load(
        "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/thermal_wave1_branch_gate.json"
    )
    source_path, source_gate = load(
        "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/thermal_parameter_provenance_gate.json"
    )
    constraint_path, constraint = load(
        "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/0_13_core_thermodynamic_constraint_gate.json"
    )
    calibration_path, calibration = load("docs/core/artifacts/thermal_dimensional_calibration_contract.json")
    transport_path, transport = load("docs/core/artifacts/covariant_superfluid_transport_contract.json")
    transport_verification_path, transport_verification = load(
        "docs/core/artifacts/covariant_superfluid_transport_verification.json"
    )
    eos_path, eos = load("docs/core/artifacts/o2_finite_density_eos_verification.json")
    causal_path, causal = load("docs/core/artifacts/matter_space_causal_cone_compatibility.json")
    source_package_path, source_package = load(
        "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/matter_space_second_sound_source_package.json"
    )

    selected = branch.get("selected_causal_branch", {})
    full = branch.get("full_candidate_branch", {})
    measurement = branch.get("measurement_contract", {})
    source_contract = branch.get("source_contract", {})
    source_policy = source_gate.get("current_lane", {})
    constraint_gates = constraint.get("gates", {})
    source_status = source_contract.get("package", {}).get("status")
    alpha_status = measurement.get("alpha_Phi_K_status")
    holdout_not_consumed = bool(source_contract.get("holdout_consumed") is False)

    causal_no_go_evidence = bool(
        causal.get("continuum_diagnostic", {})
        .get("cattaneo_extension", {})
        .get("high_k_group_speed_is_unbounded")
    )
    full_candidate_pass = (
        full.get("gate") == "PASS"
        and float(full.get("prearrival_leakage_fraction", 1.0)) <= float(full.get("threshold", 1.0e-6))
    )
    branch_pass = (
        float(selected.get("prearrival_leakage_fraction", 1.0)) <= float(selected.get("threshold", 1.0e-6))
        and float(selected.get("arrival_target_abs", 0.0)) > 0.0
    )
    source_ready = source_status == "SOURCE_LOCKED_NUMERIC"
    alpha_ready = alpha_status in {"DERIVED", "EXTERNAL_INPUT"}
    bridge_derived = constraint_gates.get("uet_bridge_derivation_gate", {}).get("status") == "PASS"
    eos_transport_entropy_ready = (
        constraint_gates.get("core_eos_transport_entropy_gate", {}).get("status") == "PASS"
        and transport.get("status") == "PASS"
        and transport_verification.get("physical_coefficient_evidence") not in {"BLOCKED_NOT_PROVIDED", "OPEN"}
    )
    dimensional_map_ready = bool(calibration.get("open_calibration_record", {}).get("physical_mapping_ready"))
    source_fit_forbidden = bool(source_gate.get("policy", {}).get("holdout_may_be_used_for_tuning") is False)

    gates = {
        "causal_full_candidate_or_formal_no_go_branch": {
            "status": "PASS" if full_candidate_pass else "BLOCKED",
            "full_candidate_pass": full_candidate_pass,
            "selected_reference_pass": branch_pass,
            "formal_no_go_recorded": False,
            "structural_no_go_evidence_present": causal_no_go_evidence,
            "threshold": 1.0e-6,
            "no_clipping_or_padding": True,
            "controlling_blocker": "formal_conserved_C_no_go_or_explicit_regularization_missing",
        },
        "source_package": {
            "status": "PASS" if source_ready else "BLOCKED",
            "source_status": source_status,
            "source_ready_for_full_closure": source_ready,
            "provisional_source_present": bool(source_contract.get("provisional_source_present")),
            "numeric_fitting_allowed": bool(source_contract.get("numeric_fitting_allowed")),
            "controlling_blocker": "ttg_numeric_source_package_is_provisional" if not source_ready else None,
        },
        "alpha_Phi_K": {
            "status": "PASS" if alpha_ready else "BLOCKED",
            "status_recorded": alpha_status,
            "independent_calibration_or_derivation": alpha_ready,
            "uncertainty_status": measurement.get("uncertainty_status"),
            "controlling_blocker": "alpha_Phi_K_independent_calibration_missing" if not alpha_ready else None,
        },
        "non_circular_bridge": {
            "status": "PASS" if bridge_derived else "BLOCKED",
            "constraint_gate_status": constraint_gates.get("uet_bridge_derivation_gate", {}).get("status"),
            "landauer_non_derivation_gate": constraint_gates.get("landauer_coefficient_non_derivation_gate", {}).get("status"),
            "controlling_blocker": "non_circular_uet_bridge_and_beta_derivation_missing" if not bridge_derived else None,
        },
        "eos_transport_kms_entropy": {
            "status": "PASS" if eos_transport_entropy_ready else "BLOCKED",
            "constraint_gate_status": constraint_gates.get("core_eos_transport_entropy_gate", {}).get("status"),
            "transport_contract_status": transport.get("status"),
            "physical_coefficient_evidence": transport_verification.get("physical_coefficient_evidence"),
            "finite_temperature_completion": transport_verification.get("finite_temperature_two_fluid_completion"),
            "full_SK_KMS_completion": transport_verification.get("full_SK_KMS_completion"),
            "controlling_blocker": "eos_transport_kms_entropy_completion_missing" if not eos_transport_entropy_ready else None,
        },
        "dimensional_observable_map": {
            "status": "PASS" if dimensional_map_ready else "BLOCKED",
            "relation": "Delta_Tq = alpha_Phi_K * Delta_Phi",
            "physical_mapping_ready": dimensional_map_ready,
            "calibration_status": calibration.get("claim_status"),
            "controlling_blocker": "dimensional_phi_to_thermal_observable_map_missing" if not dimensional_map_ready else None,
        },
        "holdout_integrity": {
            "status": "PASS" if holdout_not_consumed and source_fit_forbidden else "FAIL",
            "holdout_consumed": not holdout_not_consumed,
            "numeric_fitting_disabled": source_fit_forbidden,
            "xie_2026_policy": source_contract.get("xie_2026_policy"),
        },
    }

    all_core_ready = all(item.get("status") == "PASS" for item in gates.values())
    blockers = [
        item["controlling_blocker"]
        for item in gates.values()
        if item.get("status") == "BLOCKED" and item.get("controlling_blocker")
    ]
    artifact = {
        "schema_version": "topic13-full-thermodynamic-bridge-core-ready-v1",
        "artifact": "topic13_full_thermodynamic_bridge_core_ready_gate",
        "generated_at": date.today().isoformat(),
        "status": "T13_FULL_THERMODYNAMIC_BRIDGE_CORE_READY" if all_core_ready else "BLOCKED_OPEN_T13_FULL_BRIDGE",
        "claim_promotion": False,
        "major_result": {
            "major_result_id": "T13_FULL_THERMODYNAMIC_BRIDGE",
            "closure_level": "CLOSED_FOR_CORE" if all_core_ready else "PARTIAL",
            "what_is_closed": [
                "standard TTG normalized measurement operator",
                "normalized Phi response operator",
                "frozen-C compact-support control branch",
                "constraint-only Landauer and standard thermodynamic identities",
            ],
            "what_remains_open": blockers,
            "dependency_unlocked": "Gravity/GR remains blocked until this full bridge and Core curved 3+1 gates pass",
        },
        "equation_or_mapping": {
            "standard": "y_TTG = Delta_Tq(t) / Delta_Tq(0)",
            "uet_normalized": "y_TTG^UET = Delta_Phi(t) / Delta_Phi(0)",
            "dimensional": "Delta_Tq = alpha_Phi_K * Delta_Phi",
        },
        "units": {
            "y_TTG": "dimensionless",
            "y_TTG_UET": "dimensionless",
            "alpha_Phi_K": "K per normalized Phi; open until independent record exists",
        },
        "derivation_class": "standard observable definition plus blocked UET bridge derivation",
        "observable": "source-defined quasi-temperature difference and normalized UET response",
        "data_role": {
            "source_package": source_status,
            "calibration": source_policy.get("alpha_Phi_K_status"),
            "holdout": "Xie 2026 metadata-only locked holdout",
        },
        "verification_status": gates,
        "controlling_blocker": blockers[0] if blockers else None,
        "next_action": "Close the causal branch/no-go record, independent alpha_Phi_K, source rows, non-circular bridge, and EOS/transport/KMS/entropy gates in order.",
        "claim_boundary": "Full Topic 13 is not Core-ready; current evidence supports normalized/internal controls and constraint exports only. No temperature prediction, external validation, or global UET closure is claimed.",
        "evidence_artifacts": [
            evidence(rel(branch_path), branch, {"status": branch.get("status"), "controlling_blocker": branch.get("controlling_blocker")}),
            evidence(rel(source_path), source_gate, {"alpha_Phi_K_status": source_policy.get("alpha_Phi_K_status"), "holdout_consumed": source_policy.get("2026_graphite_holdout_consumed")}),
            evidence(rel(constraint_path), constraint, {"status": constraint.get("status"), "controlling_blocker": constraint.get("controlling_blocker")}),
            evidence(rel(calibration_path), calibration, {"audit_status": calibration.get("audit_status"), "claim_status": calibration.get("claim_status")}),
            evidence(rel(transport_path), transport, {"status": transport.get("status"), "next_controller": transport.get("next_controller")}),
            evidence(rel(transport_verification_path), transport_verification, {"physical_coefficient_evidence": transport_verification.get("physical_coefficient_evidence"), "full_SK_KMS_completion": transport_verification.get("full_SK_KMS_completion")}),
            evidence(rel(eos_path), eos, {"audit_status": eos.get("audit_status"), "evidence_status": eos.get("evidence_status")}),
            evidence(rel(causal_path), causal, {"audit_status": causal.get("audit_status"), "structural_blocker": causal.get("structural_blocker")}),
            evidence(rel(source_package_path), source_package, {"status": source_package.get("status")}),
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": artifact["status"], "closure_level": artifact["major_result"]["closure_level"], "blockers": blockers, "artifact": rel(OUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
