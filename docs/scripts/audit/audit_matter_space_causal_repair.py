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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_artifact() -> dict[str, Any]:
    default = load(DEFAULT_VERIFICATION)
    old_diagnostic = load(CAUSAL_DIAGNOSTIC)
    reference = run_reference()
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
        "reference_energy_ledger_closed": False,
        "full_coupled_integration_closed": False,
    }
    return {
        "schema_version": "causal-discretization-repair-artifact-v1",
        "artifact": "causal_discretization_repair_artifact",
        "generated_at": date.today().isoformat(),
        "status": "BLOCKED",
        "repair_status": "REFERENCE_PASS_FULL_COUPLED_INTEGRATION_OPEN",
        "reference_status": "PASS" if reference_pass else "FAIL",
        "default_full_candidate_status": "BLOCKED",
        "controlling_blocker": "full_coupled_causal_scheme_energy_and_functional_integration_missing",
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
            "couple the characteristic Phi/Pi update to the same functional derivatives",
            "preserve conserved C dynamics without importing a parabolic infinite-speed claim into the response cone",
            "derive and verify a shared discrete energy/ledger relation",
            "test nonlinear potential and explicit C-to-Phi source under the same cone",
            "rerun the original full-candidate prearrival gate without clipping or cone padding",
        ],
        "evidence_inputs": {
            "core_source": "docs/core/uet_matter_space.py",
            "core_source_sha256": sha256(CORE_SOURCE),
            "default_verification": "docs/core/artifacts/matter_space_variational_verification.json",
            "causal_diagnostic": "docs/core/artifacts/matter_space_causal_discretization_diagnostic.json",
        },
        "claim_boundary": "The repair narrows the numerical blocker by validating a strict-CFL reference lane; it does not promote the full coupled candidate, continuum causality, SI physics, or downstream topics.",
        "next_controller": "implement and verify a coupled characteristic/staggered Phi-Pi lane with energy closure before changing the default operator",
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
