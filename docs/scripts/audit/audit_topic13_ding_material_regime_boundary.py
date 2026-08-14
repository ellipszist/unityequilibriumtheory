"""Audit the explicit Ding/comparator material-regime boundary."""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / (
    "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/"
    "ding_graphite_material_regime_boundary_source_package.json"
)
OUT = ROOT / "docs/core/artifacts/t13_ding_material_regime_boundary_audit.json"
DING_RAW = ROOT / (
    "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/"
    "ding_2022_supplementary_information.pdf"
)
HUANG_AUDIT = ROOT / "docs/core/artifacts/t13_huang_2023_supplementary_payload_boundary_audit.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    package = json.loads(PACKAGE.read_text(encoding="utf-8-sig"))
    target = package["target"]
    comparators = package["comparators"]
    checks = {
        "package_target_identity_present": target["source_id"]
        == "ding_2022_natural_graphite_ttg_pbte_lane",
        "ding_raw_present": DING_RAW.is_file(),
        "ding_raw_hash_matches": DING_RAW.is_file()
        and digest(DING_RAW) == target["supplementary_sha256"],
        "ding_locator_and_characterization_present": "p. 11" in target["source_locator"]
        and target["reported_characterization"]["average_grain_area_um2"] > 0.0,
        "all_comparators_have_packages": all(
            bool(item.get("evidence_package")) and bool(item.get("regime_difference"))
            for item in comparators
        ),
        "all_comparators_explicitly_not_equivalent": all(
            item.get("equivalence_status") == "NOT_ESTABLISHED" for item in comparators
        ),
        "equivalence_rule_is_explicit": "material identity" in package[
            "mapping_contract"
        ]["equivalence_rule"],
        "equivalence_result_is_false": package["mapping_contract"]["equivalence_result"] is False,
        "huang_audit_present": HUANG_AUDIT.is_file(),
        "holdout_not_accessed": package["holdout_policy"]["xie_2026_accessed"] is False,
        "holdout_not_consumed": package["holdout_policy"]["xie_2026_source_data_consumed"] is False,
        "no_target_fit_or_alpha_fit": package["holdout_policy"]["target_curve_used"] is False
        and package["holdout_policy"]["alpha_Phi_K_fit_used"] is False,
    }
    passed = all(checks.values())
    status = (
        "PASS_SCOPED_DING_MATERIAL_REGIME_BOUNDARY_NO_GO"
        if passed
        else "FAIL_DING_MATERIAL_REGIME_BOUNDARY_AUDIT"
    )
    result = {
        "schema_version": "t13-ding-material-regime-boundary-audit-v1",
        "artifact": "t13_ding_material_regime_boundary_audit",
        "generated_at": date.today().isoformat(),
        "status": status,
        "major_result": {
            "major_result_id": "T13_DING_MATERIAL_REGIME_BOUNDARY",
            "topic": "0.13_Thermodynamic_Bridge",
            "closure_level": "CLOSED_FOR_LANE" if passed else "OPEN",
            "what_is_closed": [
                "Ding natural-graphite TTG specimen identity and supplementary grain characterization are source-locked",
                "MP48, NIST AXM-5Q1, BIPM Carbone Lorraine, IAEA manufactured-graphite, and Huang ribbon comparator identities are listed",
                "none of the archived comparator lanes is treated as equivalent to the Ding TTG/PBTE regime",
                "the material-equivalence rule is explicit and rejects silent comparator substitution",
            ],
            "equation_or_mapping": {
                "Ding_C_src": "C_src(T) = sum_mu c_mu(T) in the source PBTE response",
                "material_equivalence_rule": package["mapping_contract"]["equivalence_rule"],
                "result": "equivalence_result = false",
            },
            "units": {
                "Ding_C_src": "J m^-3 K^-1; numeric value remains open",
                "grain_area": "um^2",
                "temperature": "K",
            },
            "derivation_class": "source identity, morphology/state comparison, and scoped no-go boundary; no UET derivation",
            "observable": "Ding/comparator material-regime equivalence status",
            "data_role": "SOURCE_PROVENANCE_BOUNDARY_NOT_CALIBRATION",
            "evidence_artifacts": [
                {"path": rel(OUT)},
                {"path": rel(PACKAGE), "sha256": digest(PACKAGE)},
                {"path": rel(DING_RAW), "sha256": digest(DING_RAW) if DING_RAW.is_file() else None},
                {"path": rel(HUANG_AUDIT), "sha256": digest(HUANG_AUDIT) if HUANG_AUDIT.is_file() else None},
            ],
            "verification_status": status,
            "open_blockers": [
                "ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing",
                "same_grade_volumetric_cv_uncertainty_not_source_locked",
                "independent_alpha_Phi_K_missing",
            ]
            if passed
            else ["Ding material-regime boundary checks failed"],
            "dependency_unlocked": "Material-equivalence no-go only; comparator c_v/c_p lanes remain comparison-only and Ding C_src, alpha, transport, Core, Gravity, and Galaxy remain locked",
            "claim_boundary": "This is a scoped material-regime boundary, not a claim that the comparator physics is false and not a Ding C_src validation. It prevents silent substitution of different graphite grades, structures, or response contracts.",
        },
        "source": {
            "target": target,
            "comparators": comparators,
            "ding_raw_sha256_observed": digest(DING_RAW) if DING_RAW.is_file() else None,
            "package_path": rel(PACKAGE),
            "package_sha256": digest(PACKAGE),
        },
        "mapping_contract": package["mapping_contract"],
        "checks": checks,
        "holdout_accessed": False,
        "target_fit_performed": False,
        "numeric_alpha_Phi_K_emitted": False,
        "controlling_blocker": "material_regime_mapping_to_TTG_not_closed",
        "next_controller": "Obtain an explicit same-material/state/microstructure and PBTE response mapping or retain all comparator lanes as non-Ding comparison evidence.",
        "claim_boundary": "Source-locked material-regime no-go boundary only; no numeric Ding C_src, no independent alpha_Phi_K, and no Full Topic 13 closure.",
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "artifact": rel(OUT), "comparator_count": len(comparators), "equivalence_result": package["mapping_contract"]["equivalence_result"]}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
