"""
Diagnostic pass/fail contract for the legacy confinement proof script.

This artifact narrows the old blocker where Proof_Color_Confinement.py returned
True regardless of the printed result. It does not prove color confinement.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _bootstrap() -> Path | None:
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


from docs import ROOT_PATH
from docs.core.reproducibility import generate_artifact, hash_dataset, hash_file, save_artifact


root_path = ROOT_PATH
topic_dir = root_path / "docs" / "topics" / "0.5_Nuclear_Binding_Hadrons"
proof_path = topic_dir / "Code" / "02_Proof" / "Proof_Color_Confinement.py"
artifact_path = topic_dir / "Result" / "artifacts" / "confinement_proof_gate_diagnostic.json"


def load_proof_module():
    spec = importlib.util.spec_from_file_location("Proof_Color_Confinement", proof_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load proof module: {proof_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_diagnostic() -> bool:
    print("=" * 76)
    print("CONFINEMENT PROOF GATE DIAGNOSTIC")
    print("Topic: 0.5_Nuclear_Binding_Hadrons")
    print("=" * 76)

    module = load_proof_module()
    result = module.evaluate_confinement()
    return_contract_ok = module.prove_confinement() == result["passed"]

    summary = {
        "proof_script_status": result["status"],
        "return_contract_ok": return_contract_ok,
        "proton_mass_gev": result["proton_mass_gev"],
        "threshold_min_gev": result["threshold_min_gev"],
        "threshold_max_gev": result["threshold_max_gev"],
        "claim_status": "DIAGNOSTIC_ONLY_NOT_FORMAL_PROOF",
    }

    print(f"Proof script status: {summary['proof_script_status']}")
    print(f"Return contract OK:  {summary['return_contract_ok']}")
    print(f"Proton mass:         {summary['proton_mass_gev']:.6f} GeV")

    artifact = generate_artifact(
        topic="0.5_Nuclear_Binding_Hadrons",
        dataset_hash=hash_dataset(
            {
                "proof_script": str(proof_path.relative_to(root_path)),
                "proof_script_sha256": hash_file(proof_path),
                "threshold_min_gev": result["threshold_min_gev"],
                "threshold_max_gev": result["threshold_max_gev"],
            }
        ),
        results={
            "status": "DIAGNOSTIC_CONFINEMENT_PROOF_GATE",
            "summary": summary,
            "claim_boundary": result["claim_boundary"],
            "blocked_exports": [
                "formal confinement proof",
                "QCD derivation claim",
                "hadron-mass validation claim",
            ],
        },
        config={
            "proof_script": str(proof_path.relative_to(root_path)),
            "engine": "Code/01_Engine/Engine_Hadron_Model.py",
            "note": "This checks proof-script pass/fail behavior only.",
        },
        metrics=summary,
        thresholds={
            "return_contract_required": True,
            "formal_proof_required_for_claim": True,
        },
        notes=(
            "The old unconditional True return blocker is narrowed. A defensible "
            "derivation benchmark is still required before any confinement proof claim."
        ),
    )
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to {artifact_path}")
    return return_contract_ok


if __name__ == "__main__":
    sys.exit(0 if run_diagnostic() else 1)
