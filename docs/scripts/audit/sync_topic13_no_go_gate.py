"""Attach the scoped conserved-C no-go assessment to the Topic 13 gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GATE = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/topic13_full_thermodynamic_bridge_core_ready_gate.json"
NO_GO = ROOT / "docs/core/artifacts/conserved_c_finite_cone_no_go_assessment.json"


def main() -> int:
    gate = json.loads(GATE.read_text(encoding="utf-8-sig"))
    no_go = json.loads(NO_GO.read_text(encoding="utf-8-sig"))
    no_go_path = NO_GO.relative_to(ROOT).as_posix()
    no_go_hash = hashlib.sha256(NO_GO.read_bytes()).hexdigest()
    causal = gate["verification_status"]["causal_full_candidate_or_formal_no_go_branch"]
    causal["formal_no_go_recorded"] = no_go["status"] == "NO_GO_FOR_DECLARED_CONSERVED_CATTANEO_LOCAL_GRADIENT_CLASS"
    causal["no_go_scope"] = no_go["proof_scope"]
    causal["no_go_artifact"] = {"path": no_go_path, "sha256": no_go_hash}
    causal["named_finite_cone_branch_pass"] = False
    causal["controlling_blocker"] = "named_finite_cone_branch_or_explicit_regularization_missing"
    gate["controlling_blocker"] = "named_finite_cone_branch_or_explicit_regularization_missing"
    gate["major_result"]["what_is_closed"].append("scoped structural no-go assessment for the declared conserved-C local-gradient class")
    gate["major_result"]["what_remains_open"] = [
        "named finite-cone branch or explicit conserved-C regularization",
        *[item for item in gate["major_result"]["what_remains_open"] if item != "formal_conserved_C_no_go_or_explicit_regularization_missing"],
    ]
    gate["evidence_artifacts"].append({"path": no_go_path, "sha256": no_go_hash, "summary": {"status": no_go["status"], "proof_scope": no_go["proof_scope"]}})
    GATE.write_text(json.dumps(gate, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": gate["status"], "controlling_blocker": gate["controlling_blocker"], "no_go_status": no_go["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
