"""
UET Higgs Coupling Consistency Check
===================================
Topic: 0.17 Mass Generation

This script checks whether a topic-local Higgs coupling dataset stays close to
the Standard Model normalized baseline kappa = 1. It does not prove a new mass-
generation mechanism or replace the Higgs mechanism.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

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

current_path = Path(__file__).resolve()
TOPIC_DIR = current_path.parents[2]
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"
SOURCE_LOCK_MANIFEST_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_lock_manifest.json"
HIGGS_COUPLING_REFERENCE_PATH = ROOT / "docs" / "data" / "external" / "particle_physics" / "higgs" / "higgs_coupling_cms_2022_reference_package.json"
HIGGS_MASS_REFERENCE_PATH = ROOT / "docs" / "data" / "external" / "particle_physics" / "higgs" / "higgs_mass_combined_atlas_cms_2015_reference_package.json"
PDG_LEPTON_REFERENCE_PATH = ROOT / "docs" / "data" / "external" / "particle_physics" / "pdg" / "pdg_2024_leptons_reference_package.json"

try:
    from docs.core.uet_glass_box import UETMetricLogger, UETPathManager
except Exception as e:
    print(f"CRITICAL SETUP ERROR: {e}")
    sys.exit(1)


def load_data():
    file_path = TOPIC_DIR / "Data" / "03_Research" / "higgs_coupling_data.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _input_hashes():
    inputs = [
        TOPIC_DIR / "Data" / "03_Research" / "higgs_coupling_data.json",
        TOPIC_DIR / "Data" / "03_Research" / "higgs_mass_combined.json",
        TOPIC_DIR / "Data" / "03_Research" / "lepton_data.json",
        TOPIC_DIR / "Data" / "03_Research" / "pdg_2024_leptons.json",
        SOURCE_LOCK_MANIFEST_PATH,
        HIGGS_COUPLING_REFERENCE_PATH,
        HIGGS_MASS_REFERENCE_PATH,
        PDG_LEPTON_REFERENCE_PATH,
    ]
    records = []
    for path in inputs:
        try:
            display_path = str(path.relative_to(TOPIC_DIR)).replace("\\", "/")
        except ValueError:
            display_path = str(path.relative_to(ROOT)).replace("\\", "/")
        record = {
            "path": display_path,
            "loaded_by_primary_script": path.name == "higgs_coupling_data.json",
        }
        if path.exists():
            record.update(
                {
                    "status": "present",
                    "bytes": path.stat().st_size,
                    "sha256": _sha256(path),
                }
            )
        else:
            record["status"] = "missing"
        records.append(record)
    return records


def _load_json_if_exists(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _field(field, status, value):
    return {"field": field, "status": status, "value": value}


def _build_source_target_status():
    coupling_package = _load_json_if_exists(HIGGS_COUPLING_REFERENCE_PATH)
    higgs_mass_package = _load_json_if_exists(HIGGS_MASS_REFERENCE_PATH)
    lepton_package = _load_json_if_exists(PDG_LEPTON_REFERENCE_PATH)
    coupling_source_id = coupling_package.get("doi") or coupling_package.get("url", "") if coupling_package else ""
    return [
        {
            "name": "Higgs coupling table source package",
            "priority": "immediate",
            "status": "partial" if coupling_package else "pending",
            "evidence_fields": [
                _field("doi_or_url", "complete" if coupling_source_id else "pending", coupling_source_id),
                _field(
                    "local_path",
                    "complete" if coupling_package else "pending",
                    str(HIGGS_COUPLING_REFERENCE_PATH.relative_to(ROOT)).replace("\\", "/") if coupling_package else "",
                ),
                _field(
                    "table_or_figure_identifier",
                    "complete" if coupling_package else "pending",
                    coupling_package.get("table_identifier", "") if coupling_package else "",
                ),
                _field(
                    "retrieval_date",
                    "complete" if coupling_package else "pending",
                    coupling_package.get("retrieval_or_packaging_date", "") if coupling_package else "",
                ),
                _field(
                    "unit_basis",
                    "complete" if coupling_package else "pending",
                    json.dumps(coupling_package.get("unit_basis", {}), ensure_ascii=False) if coupling_package else "",
                ),
                _field(
                    "extraction_note",
                    "complete" if coupling_package else "pending",
                    coupling_package.get("extraction_note", "") if coupling_package else "",
                ),
            ],
        },
        {
            "name": "Combined Higgs mass reference package",
            "priority": "high",
            "status": "complete" if higgs_mass_package else "pending",
            "evidence_fields": [
                _field(
                    "doi_or_url",
                    "complete" if higgs_mass_package and higgs_mass_package.get("doi") else "pending",
                    higgs_mass_package.get("doi", "") if higgs_mass_package else "",
                ),
                _field(
                    "local_path",
                    "complete" if higgs_mass_package else "pending",
                    str(HIGGS_MASS_REFERENCE_PATH.relative_to(ROOT)).replace("\\", "/") if higgs_mass_package else "",
                ),
                _field(
                    "table_or_result_identifier",
                    "complete" if higgs_mass_package else "pending",
                    higgs_mass_package.get("result_identifier", "") if higgs_mass_package else "",
                ),
                _field(
                    "retrieval_date",
                    "complete" if higgs_mass_package else "pending",
                    higgs_mass_package.get("retrieval_or_packaging_date", "") if higgs_mass_package else "",
                ),
                _field(
                    "unit_basis",
                    "complete" if higgs_mass_package else "pending",
                    json.dumps(higgs_mass_package.get("unit_basis", {}), ensure_ascii=False) if higgs_mass_package else "",
                ),
                _field(
                    "extraction_note",
                    "complete" if higgs_mass_package else "pending",
                    higgs_mass_package.get("extraction_note", "") if higgs_mass_package else "",
                ),
            ],
        },
        {
            "name": "Normative lepton mass dataset choice",
            "priority": "high",
            "status": "complete" if lepton_package else "pending",
            "evidence_fields": [
                _field(
                    "normative_file_name",
                    "complete" if lepton_package else "pending",
                    "pdg_2024_leptons.json" if lepton_package else "",
                ),
                _field(
                    "doi_or_url",
                    "complete" if lepton_package and (lepton_package.get("doi") or lepton_package.get("url")) else "pending",
                    lepton_package.get("doi") or lepton_package.get("url", "") if lepton_package else "",
                ),
                _field(
                    "local_path",
                    "complete" if lepton_package else "pending",
                    str(PDG_LEPTON_REFERENCE_PATH.relative_to(ROOT)).replace("\\", "/") if lepton_package else "",
                ),
                _field(
                    "source_year_or_release",
                    "complete" if lepton_package else "pending",
                    "2024" if lepton_package else "",
                ),
                _field(
                    "unit_basis",
                    "complete" if lepton_package else "pending",
                    json.dumps(lepton_package.get("unit_basis", {}), ensure_ascii=False) if lepton_package else "",
                ),
                _field(
                    "extraction_note",
                    "complete" if lepton_package else "pending",
                    lepton_package.get("extraction_note", "") if lepton_package else "",
                ),
            ],
        },
        {
            "name": "Planck exponential ansatz parameter provenance",
            "priority": "medium",
            "status": "pending",
            "evidence_fields": [
                _field("parameter_reference", "pending", ""),
                _field("local_path", "pending", ""),
                _field("ansatz_version_or_script", "pending", ""),
                _field("mass_scale_definition", "pending", ""),
                _field("unit_basis", "pending", ""),
                _field("derivation_or_fit_note", "pending", ""),
            ],
        },
    ]


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _build_source_evidence_intake_stub():
    payload = {
        "schema_version": "1.0",
        "topic": "0.17_Mass_Generation",
        "purpose": "Structured intake stub for Higgs and lepton-branch source evidence before data rewrites or stronger mass-generation claims.",
        "instructions": [
            "Attach upstream DOI or URL, local archive path, table identifier, and extraction note before changing a working-copy dataset.",
            "Record the normative dataset choice explicitly when more than one lepton file exists.",
            "Do not treat this file as evidence by itself; it is an intake and tracking layer.",
        ],
        "source_targets": _build_source_target_status(),
        "claim_boundary": "This intake stub is for source evidence capture only. Filling it does not by itself justify Higgs-replacement, Koide-proof, or first-principles mass-generation claims.",
    }
    return _write_json(SOURCE_EVIDENCE_INTAKE_PATH, payload)


def _build_source_evidence_readiness_matrix(intake_stub):
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
                "ready_for_source_review": row_ready,
                "blocking_reason": "" if row_ready else "One or more required evidence fields are still pending.",
            }
        )
    payload = {
        "schema_version": "1.0",
        "topic": "0.17_Mass_Generation",
        "purpose": "Readiness matrix for branch-specific source evidence before data edits or claim upgrades.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready,
            "targets_blocked_by_pending_evidence": blocked,
        },
        "readiness_rows": rows,
        "claim_boundary": "This matrix is a workflow gate only. A target marked ready still requires actual source review before working-copy or claim changes.",
    }
    return _write_json(SOURCE_EVIDENCE_READINESS_PATH, payload)


def _build_branch_claim_gate():
    payload = {
        "schema_version": "1.0",
        "topic": "0.17_Mass_Generation",
        "purpose": "Claim gate for separate mass-generation branches inside the topic.",
        "summary": {
            "branches_total": 5,
            "accepted_now": 1,
            "blocked_for_strong_claims": 4,
        },
        "branches": [
            {
                "branch": "Higgs coupling consistency branch",
                "status": "accepted_run_contract_only",
                "allowed_usage_now": "Internal SM-normalized Higgs-coupling consistency benchmark only.",
                "blocker_to_stronger_claim": "Need uncertainty-aware upstream table mapping and stronger acceptance statistics.",
            },
            {
                "branch": "Koide and tau branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Diagnostic algebraic branch only.",
                "blocker_to_stronger_claim": "Need normative lepton dataset, tau uncertainty handling, and dedicated verifier artifact.",
            },
            {
                "branch": "Planck exponential ansatz branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Exploratory fitted or hypothesis branch only.",
                "blocker_to_stronger_claim": "Need explicit parameter provenance and derivation-versus-fit declaration.",
            },
            {
                "branch": "Mass hierarchy or mechanism claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Conceptual framing only.",
                "blocker_to_stronger_claim": "Need separate verifier lanes beyond Higgs consistency plus source-backed hierarchy benchmarks.",
            },
            {
                "branch": "Higgs replacement or new mechanism claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need first-principles derivation, independent predictive success, and external benchmark support.",
            },
        ],
        "claim_boundary": "This gate cannot raise claim strength above the current Higgs-coupling run-contract evidence.",
    }
    return _write_json(BRANCH_CLAIM_GATE_PATH, payload)


def write_verification_artifact(result):
    artifact_path = TOPIC_DIR / "Result" / "artifacts" / "0_17_mass_generation_verification.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    source_evidence_intake_stub = _build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = _build_source_evidence_readiness_matrix(source_evidence_intake_stub)
    branch_claim_gate = _build_branch_claim_gate()
    artifact = {
        "schema_version": "1.1",
        "topic": "0.17_Mass_Generation",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.17_Mass_Generation/Code/03_Research/Research_Higgs_Coupling.py",
        "status": result["status"],
        "passed_run_contract": result["status"] in {"PASS", "WARN"},
        "input_hashes": _input_hashes(),
        "source_evidence_intake_stub": {
            "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
            "sha256": _sha256(SOURCE_EVIDENCE_INTAKE_PATH),
            "source_targets": [item["name"] for item in source_evidence_intake_stub["source_targets"]],
            "claim_boundary": "This intake stub is for source evidence capture only. It does not authorize data or claim upgrades by itself.",
        },
        "source_evidence_readiness_matrix": {
            "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
            "sha256": _sha256(SOURCE_EVIDENCE_READINESS_PATH),
            "summary": source_evidence_readiness_matrix["summary"],
            "claim_boundary": "This readiness matrix is a workflow gate only. It tracks whether source evidence is still pending.",
        },
        "branch_claim_gate": {
            "path": str(BRANCH_CLAIM_GATE_PATH.relative_to(TOPIC_DIR)).replace("\\", "/"),
            "sha256": _sha256(BRANCH_CLAIM_GATE_PATH),
            "summary": branch_claim_gate["summary"],
            "claim_boundary": "This gate records branch-specific claim ceilings only. It cannot upgrade the topic beyond the current Higgs-coupling run-contract evidence.",
        },
        "metrics": {
            "particle_count": result["particle_count"],
            "average_abs_kappa_deviation": result["average_abs_kappa_deviation"],
            "max_abs_kappa_deviation": result["max_abs_kappa_deviation"],
        },
        "thresholds": {
            "average_abs_kappa_deviation_max": 0.2,
            "run_without_error": True,
            "artifact_written": True,
        },
        "interpretation": (
            "Internal Higgs-coupling consistency artifact against a topic-local "
            "SM-normalized kappa dataset. This does not prove a new mass-generation "
            "mechanism or replace the Higgs mechanism."
        ),
        "results": result,
    }
    artifact_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"   Artifact Saved: {artifact_path}")


def run_coupling_analysis():
    print("=" * 60)
    print("UET MASS GENERATION: HIGGS COUPLING CONSISTENCY CHECK")
    print("=" * 60)

    data = load_data()
    particles = data["particles"]

    names = []
    masses = []
    kappas = []
    uncertainties = []

    for particle in particles:
        names.append(particle["name"])
        masses.append(particle["mass_GeV"])
        kappas.append(particle["coupling_kappa_observed"])
        uncertainties.append(particle["uncertainty"])

    masses = np.array(masses)
    kappas = np.array(kappas)
    uncertainties = np.array(uncertainties)

    result_dir = UETPathManager.get_result_dir("0.17", "Higgs_Coupling", category="showcase")
    _logger = UETMetricLogger("Higgs_Coupling", topic_id="0.17", category="showcase")

    plt.figure(figsize=(10, 7))
    plt.errorbar(
        masses,
        kappas,
        yerr=uncertainties,
        fmt="o",
        capsize=5,
        ecolor="red",
        color="blue",
        label="LHC data working copy",
    )
    plt.axhline(
        y=1.0,
        color="k",
        linestyle="--",
        linewidth=2,
        label="SM-normalized baseline",
    )
    plt.xscale("log")
    plt.xlabel("Particle Mass (GeV)")
    plt.ylabel(r"Coupling Modifier $\kappa_F, \kappa_V$ (Observed / SM)")
    plt.title("Higgs Coupling vs Mass: Local Consistency Benchmark")
    plt.ylim(0.5, 1.5)
    plt.grid(True, which="both", alpha=0.3)

    for i, name in enumerate(names):
        plt.annotate(name, (masses[i], kappas[i]), xytext=(0, 10), textcoords="offset points", ha="center")

    save_path = result_dir / "Higgs_Coupling_Validation.png"
    plt.savefig(save_path, dpi=300)
    print(f"Showcase image saved: {save_path}")

    deviations = np.abs(kappas - 1.0)
    avg_dev = float(np.mean(deviations))
    max_dev = float(np.max(deviations))
    print(f"   Average deviation from SM-normalized baseline: {avg_dev:.3f}")

    result = {
        "status": "PASS" if avg_dev < 0.2 else "WARN",
        "particle_count": len(names),
        "average_abs_kappa_deviation": avg_dev,
        "max_abs_kappa_deviation": max_dev,
        "baseline": "SM-normalized kappa = 1.0",
        "particles": [
            {
                "name": names[i],
                "mass_GeV": float(masses[i]),
                "kappa_observed": float(kappas[i]),
                "uncertainty": float(uncertainties[i]),
                "abs_kappa_deviation": float(deviations[i]),
            }
            for i in range(len(names))
        ],
        "figure_path": str(save_path),
    }
    write_verification_artifact(result)

    if avg_dev < 0.2:
        print("PASS: Current local Higgs-coupling dataset stays close to the SM-normalized baseline.")
    else:
        print("WARNING: Significant deviation detected in the local Higgs-coupling benchmark.")
    return result


if __name__ == "__main__":
    result = run_coupling_analysis()
    sys.exit(0 if result["status"] in {"PASS", "WARN"} else 1)
