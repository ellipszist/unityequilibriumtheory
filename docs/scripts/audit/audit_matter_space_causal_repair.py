"""Package the causal discretization repair result without promoting the full operator."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docs.scripts.audit.audit_matter_space_causal_reference import run_reference  # noqa: E402

DEFAULT_VERIFICATION = ROOT / "docs/core/artifacts/matter_space_variational_verification.json"
CAUSAL_DIAGNOSTIC = ROOT / "docs/core/artifacts/matter_space_causal_discretization_diagnostic.json"
CORE_SOURCE = ROOT / "docs/core/uet_matter_space.py"
OUTPUT = ROOT / "docs/core/artifacts/causal_discretization_repair_artifact.json"
REFERENCE_ENERGY = ROOT / "docs/core/artifacts/matter_space_causal_reference_energy_verification.json"
CAUSAL_DISCRETE_GRADIENT = ROOT / "docs/core/artifacts/matter_space_causal_discrete_gradient_verification.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_artifact() -> dict[str, Any]:
    default = load(DEFAULT_VERIFICATION)
    old_diagnostic = load(CAUSAL_DIAGNOSTIC)
    reference = run_reference()
    reference_energy = load(REFERENCE_ENERGY)
    causal_discrete_gradient = load(CAUSAL_DISCRETE_GRADIENT)
    reference_pass = (
        reference["status"] == "PASS"
        and reference["metrics"]["prearrival_max_outside_discrete_cone"] == 0.0
        and reference["metrics"]["prearrival_target_abs"] == 0.0
        and reference["metrics"]["arrival_target_abs"] > 0.0
    )
    checks = {
        "reference_compact_support": reference_pass,
        "reference_uses_strict_cfl": reference["reference_cfl"] == 1.0 if "reference_cfl" in reference else reference["time_step"]["cfl"] == 1.0,
        "default_full_candidate_remains_blocked": default["metrics"]["prearrival_leakage"]["gate"] == "FAIL",
        "old_diagnostic_classifies_numerical_domain_failure": old_diagnostic["classification"] == "NUMERICAL_DOMAIN_OF_DEPENDENCE_EXCEEDS_DECLARED_CONE",
        "no_clipping_or_cone_padding": True,
        "reference_energy_ledger_closed": reference_energy["audit_status"] == "PASS",
        "causal_discrete_gradient_partial_closure": causal_discrete_gradient["partial_closure_status"] == "PASS",
        "full_coupled_integration_closed": False,
    }
    return {
        "schema_version": "causal-discretization-repair-artifact-v1",
        "artifact": "causal_discretization_repair_artifact",
        "generated_at": date.today().isoformat(),
        "status": "BLOCKED",
        "repair_status": "REFERENCE_AND_PHI_PASS_C_SHARED_INTEGRATION_OPEN",
        "reference_status": "PASS" if reference_pass else "FAIL",
        "default_full_candidate_status": "BLOCKED",
        "controlling_blocker": "matter_C_shared_ledger_integration_missing",
        "checks": checks,
        "default_candidate": {
            "artifact": "docs/core/artifacts/matter_space_variational_verification.json",
            "prearrival_leakage_fraction": default["metrics"]["prearrival_leakage"]["value"],
            "threshold": default["metrics"]["prearrival_leakage"]["threshold"],
            "gate": default["metrics"]["prearrival_leakage"]["gate"],
        },
        "reference_lane": {
            "scope": "linearized_space_response_with_frozen_C",
            "scheme": "centered_second_order_damped_recurrence",
            "required_cfl": 1.0,
            "metrics": reference["metrics"],
            "config": reference["config"],
            "time_step": reference["time_step"],
            "claim_boundary": "compact-support numerical control only; not full nonlinear matter-space verification",
        },
        "integration_requirements": [
            "integrate the verified causal Phi/Pi discrete-gradient substep with a changing-C update",
            "preserve conserved C dynamics without importing a parabolic infinite-speed claim into the response cone",
            "derive and verify a shared discrete energy/ledger relation for the full coupled scheme",
            "extend compact-support and ledger tests from frozen-C to changing-C inputs",
            "rerun the original full-candidate prearrival gate without clipping or cone padding",
        ],
        "evidence_inputs": {
            "core_source": "docs/core/uet_matter_space.py",
            "core_source_sha256": sha256(CORE_SOURCE),
            "default_verification": "docs/core/artifacts/matter_space_variational_verification.json",
            "causal_diagnostic": "docs/core/artifacts/matter_space_causal_discretization_diagnostic.json",
            "reference_energy_verification": "docs/core/artifacts/matter_space_causal_reference_energy_verification.json",
            "causal_discrete_gradient_verification": "docs/core/artifacts/matter_space_causal_discrete_gradient_verification.json",
        },
        "claim_boundary": "The repair narrows the numerical blocker by validating a strict-CFL reference and a nonlinear frozen-C Phi/Pi lane; it does not promote the changing-C full candidate, continuum causality, SI physics, or downstream topics.",
        "next_controller": "integrate the changing-C matter step with the causal Phi-Pi substep and one shared ledger before changing the default operator",
    }


def main() -> int:
    artifact = build_artifact()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"repair_status={artifact['repair_status']}")
    print(f"reference_status={artifact['reference_status']}")
    print(f"controlling_blocker={artifact['controlling_blocker']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
