"""Repair canonical Topic 13 generators so lane results survive rebuilds."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
FULL_GATE = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
REGISTER = ROOT / "docs/scripts/audit/audit_major_result_closure.py"

LANE_KEY_BY_ID = {
    "T13_UET_O2_ONE_LOOP_NORMAL_BRANCH": "uet_o2_one_loop_normal_branch",
    "T13_UET_O2_ONE_LOOP_CONVERGENCE": "uet_o2_one_loop_convergence",
    "T13_UET_O2_ONE_LOOP_THERMAL_UV_BOUNDARY": "uet_o2_one_loop_uv_boundary",
    "T13_UET_O2_CONDENSATE_GOLDSTONE_IDEAL_LANE": "uet_o2_condensate_goldstone_ideal_lane",
    "T13_UET_O2_CONDENSATE_FLUCTUATION_SPECTRUM": "uet_o2_condensate_fluctuation_spectrum",
    "T13_STANDARD_O2_FINITE_TEMPERATURE_NORMAL_COMPARATOR": "standard_o2_finite_temperature_normal_comparator",
    "T13_COVARIANT_TRANSPORT_IMPLEMENTATION_BOUNDARY": "covariant_transport_implementation_boundary",
    "T13_GATECH_STANDARD_TRANSPORT_COMPARATOR": "standard_graphite_transport_comparator",
    "T13_PHYSICAL_KUBO_COEFFICIENT_PROVENANCE_GATE": "physical_kubo_coefficient_provenance",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def repair_full_gate() -> None:
    text = FULL_GATE.read_text(encoding="utf-8-sig")
    old_controller = '    source_fit_forbidden = bool(source_gate.get("policy", {}).get("holdout_may_be_used_for_tuning") is False)\n'
    new_controller = old_controller + '''
    previous_gate = json.loads(OUT.read_text(encoding="utf-8-sig")) if OUT.is_file() else {}
    previous_transport = previous_gate.get("verification_status", {}).get("eos_transport_kms_entropy", {})
    preserved_lane_integrations = {
        key: value
        for key, value in previous_transport.items()
        if key not in {
            "status",
            "constraint_gate_status",
            "transport_contract_status",
            "physical_coefficient_evidence",
            "finite_temperature_completion",
            "full_SK_KMS_completion",
            "controlling_blocker",
        }
    }
    discovered_lane_integrations = {}
    for artifact_root in (ROOT / "docs/core/artifacts", ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts"):
        for artifact_path in sorted(artifact_root.rglob("*.json")):
            try:
                candidate = json.loads(artifact_path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                continue
            major = candidate.get("major_result")
            if not isinstance(major, dict):
                continue
            result_id = major.get("major_result_id")
            if result_id not in LANE_KEY_BY_ID:
                continue
            key = LANE_KEY_BY_ID[result_id]
            discovered_lane_integrations[key] = {
                "major_result_id": result_id,
                "status": candidate.get("status", major.get("verification_status", "OPEN")),
                "closure_level": major.get("closure_level", "OPEN"),
                "data_role": major.get("data_role", "artifact-reported"),
                "audit": {
                    "path": rel(artifact_path),
                    "sha256": sha256(artifact_path),
                    "summary": {
                        "status": candidate.get("status"),
                        "major_result_id": result_id,
                        "closure_level": major.get("closure_level"),
                    },
                },
                "controlling_blocker": candidate.get("controlling_blocker", major.get("open_blockers", [None])[0]),
                "claim_boundary": major.get("claim_boundary", "artifact-reported boundary"),
            }
    previous_major = previous_gate.get("major_result", {})
'''
    text = replace_once(text, old_controller, new_controller, "full-gate lane discovery")

    old_write = '    OUT.parent.mkdir(parents=True, exist_ok=True)\n'
    new_write = '''    artifact["verification_status"]["eos_transport_kms_entropy"].update(discovered_lane_integrations)
    artifact["verification_status"]["eos_transport_kms_entropy"].update(preserved_lane_integrations)
    artifact["major_result"]["what_is_closed"] = list(dict.fromkeys([
        *artifact["major_result"].get("what_is_closed", []),
        *previous_major.get("what_is_closed", []),
    ]))
    artifact["major_result"]["what_remains_open"] = list(dict.fromkeys([
        *artifact["major_result"].get("what_remains_open", []),
        *previous_major.get("what_remains_open", []),
    ]))
    existing_evidence_paths = {item.get("path") for item in artifact.get("evidence_artifacts", [])}
    for item in previous_gate.get("evidence_artifacts", []):
        if isinstance(item, dict) and item.get("path") not in existing_evidence_paths:
            artifact["evidence_artifacts"].append(item)
            existing_evidence_paths.add(item.get("path"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
'''
    text = replace_once(text, old_write, new_write, "full-gate lane preservation")
    FULL_GATE.write_text(text, encoding="utf-8")


def repair_register() -> None:
    text = REGISTER.read_text(encoding="utf-8-sig")
    marker = '    artifact = {\n'
    discovery = '''    discovered_entries: list[dict[str, Any]] = []
    discovered_ids: set[str] = set()
    for artifact_root in (ROOT / "docs/core/artifacts", ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts"):
        for artifact_path in sorted(artifact_root.rglob("*.json")):
            if artifact_path.resolve() == T13.resolve():
                continue
            try:
                candidate = load(artifact_path.relative_to(ROOT))
            except (OSError, json.JSONDecodeError, ValueError):
                continue
            major = candidate.get("major_result")
            if not isinstance(major, dict):
                continue
            result_id = major.get("major_result_id")
            if not isinstance(result_id, str) or not result_id or result_id in discovered_ids:
                continue
            if any(item.get("major_result_id") == result_id for item in entries):
                continue
            discovered_ids.add(result_id)
            artifact_evidence = {
                "path": rel(artifact_path),
                "sha256": sha256(artifact_path),
                "summary": {
                    "status": candidate.get("status"),
                    "major_result_id": result_id,
                    "closure_level": major.get("closure_level"),
                },
            }
            discovered_entries.append({
                "major_result_id": result_id,
                "topic": major.get("topic", "0.13_Thermodynamic_Bridge"),
                "closure_level": major.get("closure_level", "OPEN"),
                "what_is_closed": major.get("what_is_closed", []),
                "equation_or_mapping": major.get("equation_or_mapping", {}),
                "units": major.get("units", {}),
                "derivation_class": major.get("derivation_class", "artifact-reported"),
                "observable": major.get("observable", "artifact-reported"),
                "data_role": major.get("data_role", "artifact-reported"),
                "evidence_artifacts": [artifact_evidence],
                "verification_status": major.get("verification_status", candidate.get("status", "OPEN")),
                "open_blockers": major.get("open_blockers", major.get("what_remains_open", [])),
                "dependency_unlocked": major.get("dependency_unlocked", "none"),
                "claim_boundary": major.get("claim_boundary", "artifact-reported boundary"),
            })
    entries.extend(discovered_entries)
'''
    text = replace_once(text, marker, discovery + marker, "registry artifact discovery")
    REGISTER.write_text(text, encoding="utf-8")


def main() -> int:
    repair_full_gate()
    repair_register()
    print("REPAIRED_TOPIC13_CANONICAL_GENERATOR_LANE_PRESERVATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
