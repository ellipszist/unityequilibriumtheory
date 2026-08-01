"""Build a row-complete, lane-specific F2 correspondence manifest.

The manifest indexes every topic formula row and records whether a relation to
the central registry is an exact link, a lane dependency/comparator relation,
or still open.  It never promotes a topic formula into a central identity.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "docs/core/artifacts/uet_full_correspondence_coverage.json"
REGISTRY = ROOT / "docs/core/artifacts/uet_equation_correspondence_registry.json"
OUTPUT = ROOT / "docs/core/artifacts/uet_topic_formula_correspondence_manifest.json"

LANES: dict[str, dict[str, Any]] = {
    "0.11": {"lane_id": "C_phase", "role": "pilot_comparator", "registry": ["uet.matter_space.omega", "uet.matter_space.physical_dynamics", "uet.matter_space.energy_ledger"]},
    "0.13": {"lane_id": "thermal_cattaneo_bridge", "role": "pilot_comparator", "registry": ["uet.thermal.observable_bridge", "uet.trace.derived_observable", "uet.matter_space.energy_ledger"]},
    "0.1": {"lane_id": "galaxy_rotation_candidate", "role": "downstream_application", "registry": ["uet.mass_density.correspondence_identifiability", "uet.relational.two_body_baseline"]},
    "0.26": {"lane_id": "gravity_orbit_cosmology", "role": "downstream_application", "registry": ["uet.gr.closed_limit", "uet.cosmological.open_system_trace"]},
    "0.7": {"lane_id": "neutrino_particle_deferred", "role": "deferred_particle", "registry": []},
    "0.5": {"lane_id": "particle_deferred", "role": "deferred_particle", "registry": []},
    "0.6": {"lane_id": "particle_deferred", "role": "deferred_particle", "registry": []},
    "0.9": {"lane_id": "particle_deferred", "role": "deferred_particle", "registry": []},
    "0.17": {"lane_id": "particle_deferred", "role": "deferred_particle", "registry": []},
    "0.20": {"lane_id": "particle_deferred", "role": "deferred_particle", "registry": []},
    "0.10": {"lane_id": "fluid_dynamics", "role": "downstream_application", "registry": ["uet.matter_space.physical_dynamics"]},
    "0.19": {"lane_id": "gravity_orbit_cosmology", "role": "downstream_application", "registry": ["uet.gr.closed_limit"]},
}


PILOT_OPERATOR_MAP: dict[str, dict[str, Any]] = {
    "PT-ORDER-PARAMETER": {
        "operator_id": "UET-0.11-C-PHASE-PERSISTENCE-PROXY",
        "status": "INTERNAL_DIAGNOSTIC_PROXY",
        "kind": "simulation_metric_proxy",
        "expression": "C_phase_persistence_proxy",
        "unit_lane": "normalized_only_v1",
        "source_artifacts": ["docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_matter_space_phase_coupling_diagnostic.json"],
        "physical_closure": False,
        "note": "The artifact reports a lane-specific persistence/compatibility proxy, not a universal physical observable or mass map.",
    },
    "PT-CONSERVED-ORDER-SPECTRAL-L16-STRUCTURE-FACTOR-ESTIMATOR": {
        "operator_id": "UET-0.11-STRUCTURE-FACTOR-XI-SF",
        "status": "DECLARED_DIAGNOSTIC_OPERATOR_WITH_TOPIC_GATE_OPEN",
        "kind": "formula_declared_structure_factor_diagnostic",
        "expression": "xi_sf = 2*pi / sqrt(sum(S(k) k^2) / sum(S(k)))",
        "unit_lane": "normalized_or_topic_specific",
        "source_artifacts": ["docs/topics/0.11_Phase_Transitions/FORMULA_AUDIT.md"],
        "physical_closure": False,
        "note": "The operator is indexed from the topic formula row; replicate, temporal-acquisition, and estimator acceptance gates remain open.",
    },
    "PT-CONSERVED-ORDER-SPECTRAL-STRUCTURE-FACTOR-MULTIGRID": {
        "operator_id": "UET-0.11-STRUCTURE-FACTOR-XI-SF",
        "status": "DECLARED_DIAGNOSTIC_OPERATOR_WITH_TOPIC_GATE_OPEN",
        "kind": "formula_declared_structure_factor_diagnostic",
        "expression": "xi_sf = 2*pi / sqrt(sum(S(k) k^2) / sum(S(k)))",
        "unit_lane": "normalized_or_topic_specific",
        "source_artifacts": ["docs/topics/0.11_Phase_Transitions/FORMULA_AUDIT.md"],
        "physical_closure": False,
        "note": "The operator is indexed from the topic formula row; multi-grid/seed replication does not establish universality.",
    },
    "T13-010": {
        "operator_id": "STANDARD-CATTANEO-Q-001",
        "status": "DECLARED_NORMALIZED_STANDARD_CONTROL",
        "kind": "analytical_control_operator",
        "expression": "tau*dq/dt + q = -k*grad(T)",
        "unit_lane": "normalized_comparator",
        "source_artifacts": ["docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/matter_space_thermal_control.json"],
        "physical_closure": False,
        "note": "Analytical Cattaneo control passes its synthetic residual/lag/phase gates; it is not external UET validation.",
    },
    "T13-013": {
        "operator_id": "TTG-QTEMP-001",
        "status": "DECLARED_NORMALIZED_STANDARD_OPERATOR",
        "kind": "normalized_standard_observable",
        "expression": "y_TTG(t;Lambda) = Delta_Tq(t;Lambda) / Delta_Tq(0;Lambda)",
        "unit_lane": "dimensionless_observable",
        "source_artifacts": ["docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/matter_space_thermal_observable_map_readiness.json"],
        "physical_closure": False,
        "note": "The normalized standard operator is declared; local numeric source and dimensional UET bridge remain blocked.",
    },
    "T13-014": {
        "operator_id": "TTG-QTEMP-001",
        "status": "CANDIDATE_NORMALIZED_UET_OPERATOR",
        "kind": "normalized_candidate_observable",
        "expression": "y_TTG^UET(t;Lambda) = Delta_Phi(t;Lambda) / Delta_Phi(0;Lambda)",
        "unit_lane": "normalized_candidate_only",
        "source_artifacts": ["docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/matter_space_thermal_observable_map_readiness.json"],
        "physical_closure": False,
        "note": "Candidate Phi operator only; no Phi-to-temperature identity or external fit is established.",
    },
    "T13-015": {
        "operator_id": "TTG-PHI-TO-QTEMP-BRIDGE-001",
        "status": "OPEN_CALIBRATION_DEPENDENT_BRIDGE",
        "kind": "dimensional_bridge_target",
        "expression": "Delta_Tq = alpha_Phi_K * Delta_Phi",
        "unit_lane": "SI_target_open",
        "source_artifacts": ["docs/topics/0.13_Thermodynamic_Bridge/Result/artifacts/matter_space_thermal_observable_map_readiness.json"],
        "physical_closure": False,
        "note": "alpha_Phi_K remains calibration-dependent and cannot be fit from the same holdout used for validation.",
    },
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def lane_for(topic_id: str) -> dict[str, Any]:
    return LANES.get(topic_id, {"lane_id": f"topic_{topic_id}_specific", "role": "topic_specific", "registry": []})


def build() -> dict[str, Any]:
    source = load(SOURCE)
    registry = load(REGISTRY)
    registry_ids = {entry.get("equation_id") for entry in registry.get("entries", [])}
    rows: list[dict[str, Any]] = []
    for row in source.get("rows", []):
        lane = lane_for(row["topic_id"])
        related = [entry_id for entry_id in lane["registry"] if entry_id in registry_ids]
        source_status = row.get("registry_link_status", "UNDECLARED")
        if source_status == "CENTRAL_REGISTRY_EXACT_MATCH":
            relation_kind = "EXACT_CENTRAL_REGISTRY_LINK"
        elif related:
            relation_kind = "LANE_DEPENDENCY_OR_COMPARATOR_ONLY"
        else:
            relation_kind = "NO_CENTRAL_REGISTRY_RELATION_DECLARED"
        pilot_operator = PILOT_OPERATOR_MAP.get(row["formula_id"])
        measurement_operator = pilot_operator or {
            "operator_id": f"O[{row['formula_id']}]",
            "status": "OPEN_UNRESOLVED",
            "kind": "formula_row_observable_operator_not_yet_declared",
            "declared_observable": row.get("observable_mapping"),
            "physical_closure": False,
            "note": "A row index is present for audit completeness; this is not a physical measurement map.",
        }
        rows.append(
            {
                "formula_id": row["formula_id"],
                "topic_id": row["topic_id"],
                "source": row.get("source"),
                "lane_id": lane["lane_id"],
                "lane_role": lane["role"],
                "central_registry_relation": {
                    "kind": relation_kind,
                    "entry_ids": related,
                    "exact_identity": False,
                    "basis": "topic/lane dependency or comparator target only; not a universal identity of C or any physical quantity",
                },
                "correspondence": {
                    "source_registry_link_status": source_status,
                    "standard_counterpart_status": row.get("standard_counterpart_status"),
                    "standard_counterpart": row.get("standard_counterpart"),
                    "unit_lane": row.get("unit_lane"),
                    "derivation_class_or_status": row.get("derivation_class_or_status"),
                    "symmetry_conservation_status": row.get("symmetry_conservation_status"),
                    "limiting_case_status": row.get("limiting_case_status"),
                },
                "measurement_operator": measurement_operator,
                "claim_ceiling": row.get("claim_ceiling"),
                "next_action": row.get("next_action"),
            }
        )
    exact = sum(item["central_registry_relation"]["kind"] == "EXACT_CENTRAL_REGISTRY_LINK" for item in rows)
    lane_related = sum(item["central_registry_relation"]["kind"] == "LANE_DEPENDENCY_OR_COMPARATOR_ONLY" for item in rows)
    open_relation = sum(item["central_registry_relation"]["kind"] == "NO_CENTRAL_REGISTRY_RELATION_DECLARED" for item in rows)
    operator_status_counts: dict[str, int] = {}
    for item in rows:
        status = item["measurement_operator"]["status"]
        operator_status_counts[status] = operator_status_counts.get(status, 0) + 1
    operator_open = operator_status_counts.get("OPEN_UNRESOLVED", 0)
    operator_declared = len(rows) - operator_open
    operator_blocked = sum(not item["measurement_operator"].get("physical_closure", False) for item in rows)
    return {
        "schema_version": "1.0",
        "artifact": "uet_topic_formula_correspondence_manifest",
        "generated_at": date.today().isoformat(),
        "audit_status": "PASS_WITH_OPEN_ROW_MAPPINGS",
        "matrix_status": "COMPLETE_ROW_INDEX_OPEN_CORRESPONDENCE_AND_OBSERVABLES",
        "purpose": "exhaustive F2 row index; lane routing and open mapping visibility, not derivation or physical validation",
        "source_artifact": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "central_registry": str(REGISTRY.relative_to(ROOT)).replace("\\", "/"),
        "coverage": {
            "source_rows": len(source.get("rows", [])),
            "manifest_rows": len(rows),
            "rows_missing_from_manifest": len(source.get("rows", [])) - len(rows),
            "central_registry_exact_links": exact,
            "lane_dependency_or_comparator_rows": lane_related,
            "rows_without_declared_central_relation": open_relation,
            "measurement_operator_records": len(rows),
            "measurement_operator_declared_rows": operator_declared,
            "measurement_operator_open_rows": operator_open,
            "measurement_operator_blocked_rows": operator_blocked,
            "measurement_operator_status_counts": operator_status_counts,
        },
        "claim_boundary": "Lane relation is not variable identity; an indexed operator is not an observable validation; open rows cannot promote downstream claims.",
        "rows": rows,
        "next_controller": "resolve open standard counterparts, units, derivation origins, and physical measurement operators lane by lane; do not promote topic rows into central identities",
    }


def main() -> int:
    artifact = build()
    OUTPUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"audit_status={artifact['audit_status']}")
    print(f"source_rows={artifact['coverage']['source_rows']}")
    print(f"manifest_rows={artifact['coverage']['manifest_rows']}")
    print(f"open_measurement_rows={artifact['coverage']['measurement_operator_open_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
