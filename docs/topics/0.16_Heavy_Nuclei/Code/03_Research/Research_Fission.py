"""
UET Research: Nuclear Fission Simulation
========================================
Topic: 0.16 Heavy Nuclei

Diagnostic fission check for:
    n + U-235 -> Ba-141 + Kr-92 + 3n + Energy

The current verifier checks an exothermic fission sanity range and an AME2020
U-235 binding checkpoint. Fragment binding energies are still produced by the
SEMF/UET bridge, so the artifact is WARN rather than a calibrated fission Q-value PASS.
"""

import importlib.util
import json
import platform
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path


def _bootstrap():
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return None


root_path = _bootstrap()
if root_path is None:
    print("CRITICAL: UET docs root not found")
    sys.exit(1)
TOPIC_DIR = root_path / "docs" / "topics" / "0.16_Heavy_Nuclei"
AME_HEAVY_PATH = TOPIC_DIR / "Data" / "03_Research" / "ame2020_heavy_nuclei.json"
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_16_heavy_nuclei_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
BRANCH_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "branch_claim_gate.json"


def load_engine():
    engine_file = TOPIC_DIR / "Code" / "01_Engine" / "Engine_Heavy_Nuclei.py"
    spec = importlib.util.spec_from_file_location("Engine_Heavy_Nuclei", engine_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "UETHeavyNucleiEngine")


def file_sha256(path):
    digest = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_ame_heavy():
    if not AME_HEAVY_PATH.exists():
        return None
    with open(AME_HEAVY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def find_ame_binding_mev(data, z, a):
    if not data:
        return None
    for row in data.get("heavy_nuclei", []):
        if row.get("Z") == z and row.get("A") == a:
            return row["binding_energy_keV"] / 1000.0
    return None


def write_artifact(artifact):
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def build_source_evidence_intake_stub() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.16_Heavy_Nuclei",
        "purpose": "Source evidence intake before upgrading claims across heavy-nuclei binding, fission, and stability branches.",
        "source_targets": [
            {
                "name": "AME2020 U-235 checkpoint package",
                "priority": "immediate",
                "status_hint": "source_labeled_working_copy",
                "evidence_entries": [
                    "working_copy_json_path",
                    "doi_or_upstream_archive",
                    "observable_scope",
                    "unit_basis",
                    "hash_lock",
                    "benchmark_role",
                ],
            },
            {
                "name": "Source-locked fragment mass package",
                "priority": "high",
                "status_hint": "missing_primary_fragment_lock",
                "evidence_entries": [
                    "ba141_source_row",
                    "kr92_source_row",
                    "fragment_mass_or_binding_fields",
                    "unit_basis",
                    "artifact_path",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Evaluated fission energy baseline package",
                "priority": "high",
                "status_hint": "missing_q_value_baseline",
                "evidence_entries": [
                    "evaluated_q_value_source",
                    "uncertainty_field",
                    "comparison_artifact",
                    "observable_scope",
                    "unit_basis",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Heavy-binding subset benchmark package",
                "priority": "high",
                "status_hint": "secondary_lane_not_yet_primary_gated",
                "evidence_entries": [
                    "subset_dataset_path",
                    "upstream_source_package",
                    "artifact_rows",
                    "unit_basis",
                    "threshold_policy",
                    "upgrade_requirement",
                ],
            },
            {
                "name": "Stability valley and island-of-stability package",
                "priority": "medium",
                "status_hint": "blocked_theory_branch",
                "evidence_entries": [
                    "shell_correction_package",
                    "decay_or_half_life_data",
                    "stability_artifact",
                    "cross_topic_dependency_map",
                    "observable_scope",
                    "upgrade_requirement",
                ],
            },
        ],
        "claim_boundary": "This intake stub organizes provenance and branch-upgrade work only. It does not itself validate a first-principles heavy-nuclei theory.",
    }


def build_source_evidence_readiness_matrix() -> dict:
    rows = [
        {
            "name": "AME2020 U-235 checkpoint package",
            "priority": "immediate",
            "fields_total": 6,
            "fields_complete": 5,
            "fields_pending": 1,
            "pending_fields": ["upstream_archive_freeze"],
            "ready_for_source_review": True,
            "blocking_reason": None,
        },
        {
            "name": "Source-locked fragment mass package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "ba141_source_row",
                "kr92_source_row",
                "fragment_mass_or_binding_fields",
                "unit_basis",
                "artifact_path",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "Ba-141 and Kr-92 fragment masses are not source-locked in the current verifier.",
        },
        {
            "name": "Evaluated fission energy baseline package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "evaluated_q_value_source",
                "uncertainty_field",
                "comparison_artifact",
                "observable_scope",
                "unit_basis",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The current verifier has no evaluated fission Q-value baseline beyond an exothermic sanity range.",
        },
        {
            "name": "Heavy-binding subset benchmark package",
            "priority": "high",
            "fields_total": 6,
            "fields_complete": 3,
            "fields_pending": 3,
            "pending_fields": [
                "artifact_rows",
                "threshold_policy",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "The heavy-binding subset exists as a secondary lane but is not yet promoted into primary artifact rows.",
        },
        {
            "name": "Stability valley and island-of-stability package",
            "priority": "medium",
            "fields_total": 6,
            "fields_complete": 0,
            "fields_pending": 6,
            "pending_fields": [
                "shell_correction_package",
                "decay_or_half_life_data",
                "stability_artifact",
                "cross_topic_dependency_map",
                "observable_scope",
                "upgrade_requirement",
            ],
            "ready_for_source_review": False,
            "blocking_reason": "There is no source-backed stability or half-life package for island-of-stability claims.",
        },
    ]
    ready_count = sum(1 for row in rows if row["ready_for_source_review"])
    return {
        "schema_version": "1.0",
        "topic": "0.16_Heavy_Nuclei",
        "purpose": "Readiness matrix for source-evidence review across heavy-nuclei binding and fission branches.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready_count,
            "targets_blocked_by_pending_evidence": len(rows) - ready_count,
        },
        "readiness_rows": rows,
        "claim_boundary": "A ready row has enough provenance structure for source review. It does not by itself upgrade heavy-nuclei or stability claims.",
    }


def build_branch_claim_gate() -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.16_Heavy_Nuclei",
        "purpose": "Claim gate for separate heavy-nuclei branches inside the topic.",
        "summary": {
            "branches_total": 6,
            "accepted_now": 2,
            "blocked_for_strong_claims": 4,
        },
        "branches": [
            {
                "branch": "U-235 binding checkpoint branch",
                "status": "accepted_source_backed_checkpoint_branch",
                "allowed_usage_now": "Accepted U-235 binding checkpoint branch against the AME2020 working copy.",
                "blocker_to_stronger_claim": "Need broader isotope coverage and independent derivation before promoting beyond a checkpoint branch.",
            },
            {
                "branch": "Exothermic fission sanity branch",
                "status": "accepted_sanity_diagnostic_branch",
                "allowed_usage_now": "Accepted exothermic sanity-check branch for bridge-derived fission energetics only.",
                "blocker_to_stronger_claim": "Need source-locked fragment masses and evaluated Q-value baselines before claiming calibrated fission prediction.",
            },
            {
                "branch": "Fragment-mass prediction branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need source-locked Ba-141 and Kr-92 fragment rows in the primary verifier.",
            },
            {
                "branch": "Evaluated fission-energy branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need an evaluated fission-energy baseline with uncertainty-aware thresholds.",
            },
            {
                "branch": "Heavy-binding generalization branch",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Secondary comparison only.",
                "blocker_to_stronger_claim": "Need dedicated artifact rows and threshold policy for the heavy-binding subset lane.",
            },
            {
                "branch": "Island-of-stability and full heavy-nuclei theory claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Not supported by current evidence.",
                "blocker_to_stronger_claim": "Need shell corrections, decay data, and stability artifacts beyond the current SEMF/UET bridge.",
            },
        ],
        "claim_boundary": "This gate keeps the topic at heavy-nuclei checkpoint and sanity-diagnostic status, not first-principles nuclear closure.",
    }


def build_heavy_nuclei_claim_scope_gate(
    status: str,
    energy_released: float,
    u235_error_percent: float | None,
    fragment_ame_present: bool,
    source_evidence_readiness_matrix: dict,
    branch_claim_gate: dict,
) -> dict:
    return {
        "schema_version": "1.0",
        "topic": "0.16_Heavy_Nuclei",
        "controller_status": status,
        "controller_reason": (
            "The U-235 checkpoint and exothermic fission sanity gates pass, but export remains WARN because "
            "Ba-141/Kr-92 fragment masses and evaluated fission-energy baselines are not source-locked."
            if status == "WARN"
            else "The fission sanity check failed the energy-release or U-235 binding checkpoint gate."
        ),
        "claim_class": "C_D_boundary_fission_sanity_only",
        "allowed_claims_now": [
            {
                "claim": "The SEMF/UET bridge matches the U-235 AME2020 working-copy binding checkpoint within the declared tolerance.",
                "status": "WARN" if u235_error_percent is not None else "FAIL",
                "artifact_role": "source-backed U-235 checkpoint",
                "metric": "u235_binding_error_percent",
                "metric_value": u235_error_percent,
                "threshold": "<= 2.0",
                "source_evidence_readiness": "u235_checkpoint_ready_for_review",
            },
            {
                "claim": "The bridge-derived U-235 fission channel is exothermic in the declared sanity range.",
                "status": status,
                "artifact_role": "internal fission sanity diagnostic",
                "metric": "energy_release_mev",
                "metric_value": energy_released,
                "threshold": "100.0 < Q < 250.0",
                "source_evidence_readiness": "fragment_masses_not_source_locked",
            },
        ],
        "blocked_claims": [
            {
                "claim": "UET validates the evaluated U-235 fission Q-value.",
                "status": "BLOCKED",
                "blocking_reason": "The verifier uses bridge-derived Ba-141/Kr-92 fragment binding estimates rather than source-locked fragment masses.",
                "next_evidence_required": [
                    "source-locked Ba-141 fragment row",
                    "source-locked Kr-92 fragment row",
                    "evaluated fission-energy baseline with uncertainties",
                ],
            },
            {
                "claim": "UET validates heavy-nuclei binding across a general isotope subset.",
                "status": "BLOCKED",
                "blocking_reason": "Secondary heavy-binding plots are not promoted into primary artifact rows with thresholds.",
                "next_evidence_required": [
                    "primary heavy-binding artifact rows",
                    "threshold policy",
                    "source-normalized isotope suite",
                ],
            },
            {
                "claim": "UET predicts the island of stability or full heavy-nuclei theory.",
                "status": "BLOCKED",
                "blocking_reason": "No source-backed shell-correction, half-life, decay-channel, or superheavy stability artifact is available.",
                "next_evidence_required": [
                    "shell-correction model audit",
                    "decay and half-life source package",
                    "superheavy stability benchmark artifact",
                ],
            },
        ],
        "blocked_export_phrases": [
            "U-235 fission Q-value validated",
            "fragment masses predicted",
            "heavy-nuclei theory proven",
            "island of stability predicted",
            "first-principles nuclear closure",
        ],
        "source_evidence_summary": source_evidence_readiness_matrix["summary"],
        "branch_claim_gate_summary": branch_claim_gate["summary"],
        "fragment_ame_present": fragment_ame_present,
        "machine_readable_next_blockers": [
            "ba141_fragment_mass_source_lock_missing",
            "kr92_fragment_mass_source_lock_missing",
            "evaluated_fission_q_baseline_missing",
            "heavy_binding_primary_artifact_rows_missing",
            "island_stability_artifact_missing",
        ],
        "claim_boundary": (
            "A WARN artifact supports only the U-235 binding checkpoint and exothermic fission sanity diagnostic. "
            "It does not validate evaluated fission energetics, fragment masses, broad heavy-binding systematics, "
            "island-of-stability claims, or first-principles nuclear closure."
        ),
    }


def run_fission_sim():
    print("=" * 60)
    print("UET RESEARCH: NUCLEAR FISSION DIAGNOSTIC (U-235)")
    print("=" * 60)

    engine_cls = load_engine()
    engine = engine_cls()
    source_evidence_intake_stub = build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = build_source_evidence_readiness_matrix()
    branch_claim_gate = build_branch_claim_gate()
    write_json(SOURCE_EVIDENCE_INTAKE_PATH, source_evidence_intake_stub)
    write_json(SOURCE_EVIDENCE_READINESS_PATH, source_evidence_readiness_matrix)
    write_json(BRANCH_CLAIM_GATE_PATH, branch_claim_gate)

    z_parent, a_parent = 92, 235
    z_frag1, a_frag1 = 56, 141
    z_frag2, a_frag2 = 36, 92

    be_parent = engine.compute_binding_energy(z_parent, a_parent)
    be_frag1 = engine.compute_binding_energy(z_frag1, a_frag1)
    be_frag2 = engine.compute_binding_energy(z_frag2, a_frag2)
    total_be_products = be_frag1 + be_frag2
    energy_released = total_be_products - be_parent

    ame_data = load_ame_heavy()
    u235_ame_binding_mev = find_ame_binding_mev(ame_data, z_parent, a_parent)
    u235_error_percent = None
    if u235_ame_binding_mev:
        u235_error_percent = abs(be_parent - u235_ame_binding_mev) / u235_ame_binding_mev * 100

    threshold = {
        "energy_release_mev_min": 100.0,
        "energy_release_mev_max": 250.0,
        "u235_binding_error_percent_max": 2.0,
        "fragment_ame_required_for_pass": True,
    }
    exothermic_gate = threshold["energy_release_mev_min"] < energy_released < threshold["energy_release_mev_max"]
    u235_gate = u235_error_percent is not None and u235_error_percent <= threshold["u235_binding_error_percent_max"]
    fragment_ame_present = False
    status = "WARN" if exothermic_gate and u235_gate else "FAIL"
    failure_reason = (
        "Exothermic range and U-235 binding checkpoint pass, but Ba-141/Kr-92 fragment AME masses are not used by this verifier."
        if status == "WARN"
        else "Fission sanity check failed the energy-release or U-235 binding checkpoint gate."
    )

    print(f"  Parent U-235 bridge BE: {be_parent:.1f} MeV")
    if u235_ame_binding_mev is not None:
        print(f"  AME2020 U-235 BE:       {u235_ame_binding_mev:.1f} MeV")
        print(f"  U-235 error:            {u235_error_percent:.2f}%")
    print(f"  Products bridge BE:     {total_be_products:.1f} MeV")
    print(f"  Energy released:        {energy_released:.1f} MeV")
    print(f"  Artifact status:        {status}")
    heavy_nuclei_claim_scope_gate = build_heavy_nuclei_claim_scope_gate(
        status,
        energy_released,
        u235_error_percent,
        fragment_ame_present,
        source_evidence_readiness_matrix,
        branch_claim_gate,
    )

    artifact = {
        "schema_version": "1.1",
        "topic": "0.16_Heavy_Nuclei",
        "status": status,
        "claim_class": "C/D boundary - internal fission sanity check with missing fragment provenance",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python docs/topics/0.16_Heavy_Nuclei/Code/03_Research/Research_Fission.py",
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "inputs": [
            {
                "path": str(AME_HEAVY_PATH.relative_to(root_path)).replace("\\", "/"),
                "sha256": file_sha256(AME_HEAVY_PATH) if AME_HEAVY_PATH.exists() else None,
                "source": "AME2020 heavy-nuclei working copy",
                "doi": ame_data.get("publication", {}).get("doi") if ame_data else None,
            }
        ],
        "formula_ids": [
            "HN16-SEMF-BINDING",
            "HN16-UET-SEMF-BRIDGE",
            "HN16-FISSION-Q-SANITY",
        ],
        "threshold": threshold,
        "metrics": {
            "parent": {"Z": z_parent, "A": a_parent, "binding_energy_mev": be_parent},
            "fragments": [
                {"Z": z_frag1, "A": a_frag1, "binding_energy_mev": be_frag1},
                {"Z": z_frag2, "A": a_frag2, "binding_energy_mev": be_frag2},
            ],
            "energy_release_mev": energy_released,
            "u235_ame_binding_mev": u235_ame_binding_mev,
            "u235_binding_error_percent": u235_error_percent,
            "exothermic_gate": exothermic_gate,
            "u235_binding_gate": u235_gate,
            "fragment_ame_present": fragment_ame_present,
            "source_targets_ready_for_review": source_evidence_readiness_matrix["summary"]["targets_ready_for_source_review"],
            "source_targets_blocked": source_evidence_readiness_matrix["summary"]["targets_blocked_by_pending_evidence"],
            "accepted_claim_branches": branch_claim_gate["summary"]["accepted_now"],
            "blocked_claim_exports": len(heavy_nuclei_claim_scope_gate["blocked_export_phrases"]),
        },
        "failure_reason": failure_reason,
        "limitations": [
            "The verifier uses SEMF/UET-bridge fragment binding estimates, not source-locked AME fragment masses.",
            "The result supports an internal fission sanity check only.",
            "It does not validate the Island of Stability or a first-principles heavy-nuclei theory.",
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
    artifact["heavy_nuclei_claim_scope_gate"] = heavy_nuclei_claim_scope_gate
    artifact["interpretation"] = (
        "This artifact supports a U-235 checkpoint branch and a bounded exothermic fission sanity branch. "
        "It does not validate source-locked fragment energetics or heavy-nuclei stability theory."
    )
    write_artifact(artifact)
    print(f"  Artifact written: {ARTIFACT_PATH}")
    return status in {"PASS", "WARN"}


if __name__ == "__main__":
    success = run_fission_sim()
    sys.exit(0 if success else 1)
