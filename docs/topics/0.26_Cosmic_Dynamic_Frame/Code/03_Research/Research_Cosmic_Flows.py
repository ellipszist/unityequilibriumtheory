"""
UET Cosmic Flow Research
========================
Topic: 0.26 Cosmic Dynamic Frame

Primary verifier: load the topic-local Laniakea landmark working copy, render a
3D flow-map artifact, and write a machine-readable provenance/status artifact.
This is a visualization/provenance gate, not a cosmological model proof.
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

from docs.core.uet_glass_box import UETPathManager


TOPIC_DIR = ROOT / "docs" / "topics" / "0.26_Cosmic_Dynamic_Frame"
ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_26_cosmic_dynamic_frame_verification.json"
SOURCE_EVIDENCE_INTAKE_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS_PATH = TOPIC_DIR / "Data" / "03_Research" / "source_evidence_readiness_matrix.json"
DEPENDENCY_CLAIM_GATE_PATH = TOPIC_DIR / "Data" / "03_Research" / "dependency_claim_gate.json"
DATA_INPUTS = [
    TOPIC_DIR / "Data" / "03_Research" / "Laniakea_Flows.json",
    TOPIC_DIR / "Data" / "03_Research" / "source_lock_manifest.json",
    TOPIC_DIR / "Data" / "Cosmicflows_3_Subset.csv",
    TOPIC_DIR / "Data" / "Download_Cosmic_Data.py",
    TOPIC_DIR / "Data" / "Pioneer_Anomaly_Data.csv",
    ROOT / "docs" / "data" / "external" / "cosmology" / "laniakea" / "tully_2014" / "source_record.json",
    ROOT / "docs" / "data" / "external" / "cosmology" / "cosmicflows" / "cosmicflows3" / "source_record.json",
    ROOT / "docs" / "data" / "external" / "spacecraft" / "pioneer_anomaly" / "anderson_2002" / "source_record.json",
]


def _load_json_if_exists(path: Path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _find_source_target(source_lock: dict, suffix: str):
    for item in source_lock.get("derived_inputs", []):
        if item.get("local_path", "").endswith(suffix):
            return item
    return {}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _input_identity():
    items = []
    for path in DATA_INPUTS:
        rel = path.relative_to(ROOT).as_posix()
        if path.exists():
            items.append({"path": rel, "sha256": _sha256(path), "size_bytes": path.stat().st_size})
        else:
            items.append({"path": rel, "missing": True})
    return items


def load_flows():
    path = TOPIC_DIR / "Data" / "03_Research" / "Laniakea_Flows.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing Data: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _build_source_evidence_intake_stub():
    source_lock = _load_json_if_exists(TOPIC_DIR / "Data" / "03_Research" / "source_lock_manifest.json")
    laniakea_source = _load_json_if_exists(ROOT / "docs" / "data" / "external" / "cosmology" / "laniakea" / "tully_2014" / "source_record.json")
    cosmicflows_source = _load_json_if_exists(ROOT / "docs" / "data" / "external" / "cosmology" / "cosmicflows" / "cosmicflows3" / "source_record.json")
    pioneer_source = _load_json_if_exists(ROOT / "docs" / "data" / "external" / "spacecraft" / "pioneer_anomaly" / "anderson_2002" / "source_record.json")
    laniakea_lock = _find_source_target(source_lock, "Data/03_Research/Laniakea_Flows.json")
    cosmicflows_lock = _find_source_target(source_lock, "Data/Cosmicflows_3_Subset.csv")
    pioneer_lock = _find_source_target(source_lock, "Data/Pioneer_Anomaly_Data.csv")

    payload = {
        "schema_version": "1.0",
        "topic": "0.26_Cosmic_Dynamic_Frame",
        "purpose": "Structured intake stub for external-source evidence before data rewrites or dynamic-frame claim upgrades.",
        "instructions": [
            "Attach upstream DOI or URL, local archive path, frame metadata, and extraction notes before changing working-copy values.",
            "Record whether each dataset is observed, reconstructed, inferred, or baseline-comparator material.",
            "Do not treat this intake file as evidence by itself; it is a workflow landing zone."
        ],
        "source_targets": [
            {
                "name": "Laniakea raw or reconstruction table package",
                "priority": "immediate",
                "status": "partial",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "complete", "value": laniakea_source.get("doi_url", "")},
                    {"field": "local_path", "status": "complete", "value": laniakea_lock.get("local_path", "")},
                    {"field": "original_file_name", "status": "pending", "value": ""},
                    {"field": "reference_frame", "status": "complete", "value": laniakea_source.get("unit_convention", {}).get("coordinate_frame", "")},
                    {"field": "velocity_or_position_unit_basis", "status": "complete", "value": "distance: Mpc; velocity: km/s"},
                    {"field": "extraction_note", "status": "complete", "value": laniakea_lock.get("preprocessing", "")},
                ],
            },
            {
                "name": "Cosmicflows-3 subset extraction package",
                "priority": "immediate",
                "status": "partial",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "complete", "value": cosmicflows_source.get("doi_url", "")},
                    {"field": "local_path", "status": "complete", "value": cosmicflows_lock.get("local_path", "")},
                    {"field": "original_file_name", "status": "pending", "value": ""},
                    {"field": "observer_frame_and_distance_calibration", "status": "complete", "value": cosmicflows_source.get("unit_convention", {}).get("frame", "")},
                    {"field": "subset_selection_rule", "status": "pending", "value": ""},
                    {"field": "extraction_note", "status": "complete", "value": cosmicflows_lock.get("preprocessing", "")},
                ],
            },
            {
                "name": "Pioneer anomaly residual or telemetry package",
                "priority": "high",
                "status": "partial",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "complete", "value": pioneer_source.get("doi_url", "")},
                    {"field": "local_path", "status": "complete", "value": pioneer_lock.get("local_path", "")},
                    {"field": "original_file_name", "status": "pending", "value": ""},
                    {"field": "residual_or_telemetry_identifier", "status": "complete", "value": "Distance_AU / Anomaly_Accel_m_s2 / Error_m_s2 working table"},
                    {"field": "unit_basis", "status": "complete", "value": "acceleration: m s^-2; distance: AU"},
                    {"field": "extraction_note", "status": "complete", "value": pioneer_lock.get("preprocessing", "")},
                ],
            },
            {
                "name": "Pioneer thermal-recoil competitor baseline",
                "priority": "high",
                "status": "pending",
                "evidence_fields": [
                    {"field": "doi_or_url", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "pending", "value": ""},
                    {"field": "baseline_model_identifier", "status": "pending", "value": ""},
                    {"field": "reported_acceleration_or_heat_budget", "status": "pending", "value": ""},
                    {"field": "unit_basis", "status": "pending", "value": ""},
                    {"field": "extraction_note", "status": "pending", "value": ""},
                ],
            },
        ],
        "claim_boundary": (
            "This intake stub supports source capture only. Filling it does not by itself justify dynamic-frame, "
            "dark-matter replacement, or Pioneer-drag claim upgrades."
        ),
        "source_lock_dependencies": source_lock.get("external_source_records", []),
    }
    return _write_json(SOURCE_EVIDENCE_INTAKE_PATH, payload)


def _build_source_evidence_readiness_matrix(intake_stub: dict):
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
        "topic": "0.26_Cosmic_Dynamic_Frame",
        "purpose": "Readiness matrix for source evidence before data edits or claim upgrades.",
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
    return _write_json(SOURCE_EVIDENCE_READINESS_PATH, payload)


def _build_dependency_claim_gate():
    dependencies = [
        {
            "topic": "0.1_Galaxy_Rotation_Problem",
            "artifact_path": "docs/topics/0.1_Galaxy_Rotation_Problem/Result/artifacts/galaxy_rotation_validation.json",
            "upstream_status": "WARN",
            "allowed_usage_now": "Dependency reference only for future residual-link design; not evidence that 0.26 explains galaxy rotation.",
            "inherited_limitations": [
                "0.1 benchmark currently reports high residual error and zero pass rate under current galaxy gate.",
                "0.26 cannot borrow stronger credibility than the SPARC-linked benchmark currently supports."
            ],
        },
        {
            "topic": "0.23_Unity_Scale_Link",
            "artifact_path": "docs/topics/0.23_Unity_Scale_Link/Result/artifacts/0_23_unity_scale_link_verification.json",
            "upstream_status": "WARN",
            "allowed_usage_now": "Cross-scale dependency note only; exploratory logic must remain below direct cosmology-fit claims.",
            "inherited_limitations": [
                "0.23 remains exploratory and partly synthetic.",
                "Dynamic-frame claims cannot be promoted through scale-link language alone."
            ],
        },
        {
            "topic": "0.0_Grand_Unification",
            "artifact_path": "docs/topics/0.0_Grand_Unification/Result/artifacts/0_0_grand_unification_verification.json",
            "upstream_status": "WARN",
            "allowed_usage_now": "Integration-index dependency only; not a proof layer for 0.26.",
            "inherited_limitations": [
                "0.0 is an integration index and inherits open topic limitations.",
                "0.26 cannot treat 0.0 as a stronger external validation channel."
            ],
        },
    ]
    payload = {
        "schema_version": "1.0",
        "topic": "0.26_Cosmic_Dynamic_Frame",
        "purpose": "Dependency gate for inherited claim limits across core topics.",
        "summary": {
            "dependencies_total": len(dependencies),
            "dependencies_with_warn_status": sum(1 for item in dependencies if item["upstream_status"] == "WARN"),
            "dependencies_with_pass_status": sum(1 for item in dependencies if item["upstream_status"] == "PASS"),
        },
        "dependencies": dependencies,
        "claim_boundary": (
            "This dependency gate records inherited limits from linked core topics. It cannot raise the claim class "
            "above the weakest relevant upstream evidence."
        ),
    }
    return _write_json(DEPENDENCY_CLAIM_GATE_PATH, payload)


def _write_artifact(metrics, figure_path):
    inputs = _input_identity()
    source_evidence_intake_stub = _build_source_evidence_intake_stub()
    source_evidence_readiness_matrix = _build_source_evidence_readiness_matrix(source_evidence_intake_stub)
    dependency_claim_gate = _build_dependency_claim_gate()
    missing = [item["path"] for item in inputs if item.get("missing")]
    status = "WARN" if figure_path and not missing else "FAIL"
    artifact = {
        "schema_version": "1.1",
        "topic": "0.26_Cosmic_Dynamic_Frame",
        "command": ".venv\\Scripts\\python.exe docs\\topics\\0.26_Cosmic_Dynamic_Frame\\Code\\03_Research\\Research_Cosmic_Flows.py",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "claim_class": "D",
        "inputs": inputs,
        "metrics": metrics,
        "figure_artifact": str(figure_path.relative_to(TOPIC_DIR)) if figure_path else None,
        "source_evidence_intake_stub": {
            "path": str(SOURCE_EVIDENCE_INTAKE_PATH.relative_to(ROOT)).replace("/", "\\"),
            "sha256": _sha256(SOURCE_EVIDENCE_INTAKE_PATH),
            "source_targets": [item["name"] for item in source_evidence_intake_stub["source_targets"]],
            "claim_boundary": "This intake stub is for source evidence capture only. It does not authorize data or claim upgrades by itself.",
        },
        "source_evidence_readiness_matrix": {
            "path": str(SOURCE_EVIDENCE_READINESS_PATH.relative_to(ROOT)).replace("/", "\\"),
            "sha256": _sha256(SOURCE_EVIDENCE_READINESS_PATH),
            "summary": source_evidence_readiness_matrix["summary"],
            "claim_boundary": "This readiness matrix is a workflow gate only. It tracks whether source evidence is still pending.",
        },
        "dependency_claim_gate": {
            "path": str(DEPENDENCY_CLAIM_GATE_PATH.relative_to(ROOT)).replace("/", "\\"),
            "sha256": _sha256(DEPENDENCY_CLAIM_GATE_PATH),
            "summary": dependency_claim_gate["summary"],
            "claim_boundary": "This dependency gate records inherited claim limits only. It cannot upgrade the dynamic-frame claim class.",
        },
        "warnings": [
            "Laniakea/Cosmicflows/Pioneer source records are pinned, but raw tables, frame metadata, and preprocessing are not archived.",
            "This verifier checks data loading and flow-map generation, not a cosmological model fit.",
            "Cosmicflows/Pioneer files are hashed for provenance but are not used by this primary visualization gate.",
        ],
        "interpretation": (
            "The artifact supports an exploratory dynamic-frame visualization. It does not establish "
            "dark-matter replacement, toroidal cosmology, or Pioneer-drag physics."
        ),
    }
    if missing:
        artifact["warnings"].append(f"Missing declared inputs: {missing}")
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"\n[Artifact] Verification artifact written: {ARTIFACT_PATH}")
    print(f"[Artifact] Status: {status}")
    return artifact


def run_viz():
    print("=" * 60)
    print("UET COSMIC FLOW VISUALIZATION")
    print("Data: Laniakea topic-local working copy")
    print("=" * 60)

    output_dir = UETPathManager.get_result_dir(
        topic_id="0.26", experiment_name="Laniakea_Flow", category="showcase"
    )

    data = load_flows()
    landmarks = data["landmarks"]
    names = [item["name"] for item in landmarks]
    coords = np.array([item["coords"] for item in landmarks])
    types = [item["type"] for item in landmarks]

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")
    colors = {
        "Observer": "blue",
        "Attractor": "red",
        "Major Attractor": "darkred",
        "Repeller (Void)": "cyan",
        "Filament": "green",
        "Local Hub": "orange",
    }

    used_labels = set()
    for name, coord, kind in zip(names, coords, types):
        label = kind if kind not in used_labels else ""
        used_labels.add(kind)
        ax.scatter(coord[0], coord[1], coord[2], c=colors.get(kind, "gray"), s=160, label=label)
        ax.text(coord[0], coord[1], coord[2] + 5, name, fontsize=9)

    flow_names = ["Dipole Repeller", "Milky Way (Local Group)", "Great Attractor (Norma)", "Shapley Concentration"]
    has_flow_path = all(name in names for name in flow_names)
    if has_flow_path:
        path_coords = coords[[names.index(name) for name in flow_names]]
        ax.plot(path_coords[:, 0], path_coords[:, 1], path_coords[:, 2], "k--", linewidth=1, alpha=0.5)

    ax.set_xlabel("SGX (Mpc)")
    ax.set_ylabel("SGY (Mpc)")
    ax.set_zlabel("SGZ (Mpc)")
    ax.set_title("Laniakea Supercluster: Topic-Local Cosmic Flow Map")
    ax.legend()

    save_path = output_dir / "Laniakea_Flow_Map.png"
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Showcase image saved: {save_path}")

    metrics = {
        "landmark_count": int(len(landmarks)),
        "coordinate_frame": "supergalactic Mpc",
        "landmark_types": sorted(set(types)),
        "velocity_magnitudes_km_s": [item["velocity_mag"] for item in landmarks if "velocity_mag" in item],
        "has_flow_path": bool(has_flow_path),
    }
    artifact = _write_artifact(metrics, save_path if save_path.exists() else None)
    print("Result: flow-field map generated as exploratory visualization.")
    return artifact["status"] != "FAIL"


if __name__ == "__main__":
    raise SystemExit(0 if run_viz() else 1)
