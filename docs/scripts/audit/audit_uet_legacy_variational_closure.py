"""Audit exact variational closure of the legacy C/I implementation.

This audit does not change the legacy engine. It checks two implementation-level claims:
the coded derivative of V(C), and the sign of the I source implied by the declared
positive beta*C*I coupling under negative-gradient flow.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
MASTER_PATH = ROOT / "docs/core/uet_master_equation.py"
OUT = ROOT / "docs/core/artifacts/uet_legacy_variational_closure.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def potential_pair(master_text: str) -> dict[str, Any]:
    from docs.core.uet_master_equation import potential_V, potential_derivative
    from docs.core.uet_parameters import UETParameters

    params = UETParameters(alpha=1.0, gamma=0.025, C0=1.0)
    samples = np.array([-1.5, -0.75, 0.0, 0.5, 1.0, 1.5, 2.0], dtype=float)
    epsilon = 1.0e-6
    finite_difference = (
        potential_V(samples + epsilon, params) - potential_V(samples - epsilon, params)
    ) / (2.0 * epsilon)
    coded = potential_derivative(samples, params)
    residual = np.abs(finite_difference - coded)
    source_contract = {
        "potential_code": "diff = C_mag_sq - params.C0**2",
        "derivative_code": "diff = C - params.C0",
        "finite_difference_max_absolute_residual": float(np.max(residual)),
        "threshold": 1.0e-8,
        "samples": samples.tolist(),
    }
    status = "CONTRADICTION" if source_contract["finite_difference_max_absolute_residual"] > source_contract["threshold"] else "PASS"
    return {
        "finding_id": "legacy_potential_derivative_pair",
        "status": status,
        "declared_relation": "V(C)=alpha/2*(C^2-C0^2)^2+gamma/4*(C^2-C0^2)^4",
        "coded_relation": "dynamics uses alpha*(C-C0)+gamma*(C-C0)^3",
        "analytic_derivative": "2*C*(alpha*(C^2-C0^2)+gamma*(C^2-C0^2)^3)",
        "metrics": source_contract,
        "claim_boundary": "legacy comparator; not a closed variational gradient flow",
    }


def information_gradient_sign(master_text: str) -> dict[str, Any]:
    coupling_present = "return params.beta * np.sum(C * I) * volume" in master_text
    source_present = "source = params.beta * C" in master_text
    c_source_present = "return -params.beta * I" in master_text
    expected_i_source_sign = -1
    coded_i_source_sign = 1
    status = (
        "CONTRADICTION"
        if coupling_present and source_present and expected_i_source_sign != coded_i_source_sign
        else "NOT_ESTABLISHED"
    )
    return {
        "finding_id": "legacy_information_gradient_sign",
        "status": status,
        "declared_relation": "Omega_I contains +beta*C*I and dI/dt=-delta(Omega)/delta(I)",
        "coded_relation": "dI/dt=laplacian-kappa_I*I+beta*C",
        "expected_source_sign": expected_i_source_sign,
        "coded_source_sign": coded_i_source_sign,
        "c_source_sign_matches": c_source_present,
        "interpretation": "The I source sign is opposite to the negative functional gradient implied by the declared positive coupling. The C-side source has the opposite sign and therefore does not repair the I-side mismatch.",
        "claim_boundary": "legacy I dynamics is not a closed gradient-flow pair with the declared information coupling",
    }


def build_report() -> dict[str, Any]:
    master_text = MASTER_PATH.read_text(encoding="utf-8", errors="replace")
    findings = [potential_pair(master_text), information_gradient_sign(master_text)]
    blockers = [item["finding_id"] for item in findings if item["status"] == "CONTRADICTION"]
    return {
        "schema_version": "1.0",
        "artifact": "uet_legacy_variational_closure",
        "generated_at": date.today().isoformat(),
        "audit_status": "PASS",
        "closure_status": "BLOCKED" if blockers else "PASS_CONDITIONAL",
        "controlling_blockers": blockers,
        "equation_family": "uet.legacy.master_functional",
        "evidence_inputs": {"master_equation": rel(MASTER_PATH)},
        "findings": findings,
        "principle": "A dynamics implementation is variational only when every coupled state equation is the negative derivative of the same declared functional in the same unit and boundary lane.",
        "next_action": "Keep legacy behavior quarantined; either repair the functional/gradient pair or relabel the implementation as a non-variational comparator before using it as a foundation.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    try:
        report = build_report()
    except Exception as exc:  # pragma: no cover - surfaced as an audit failure
        print(f"audit_status=FAIL\nERROR: {exc}")
        return 1
    if not args.no_write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"audit_status={report['audit_status']}")
        print(f"closure_status={report['closure_status']}")
        print(f"controlling_blockers={','.join(report['controlling_blockers'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
