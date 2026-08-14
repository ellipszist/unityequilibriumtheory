"""Add the Oxford TGS provenance lane to the canonical Topic 13 gate."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old_mapping = (
        "'T13_BERUT_SOURCE_PACKAGE_AVAILABILITY_BOUNDARY': 'berut_source_package_availability_boundary', "
        "'T13_BERUT_FIGURE3_REMOTE_BINARY_IDENTITY': 'berut_figure3_remote_binary_identity'}"
    )
    new_mapping = (
        "'T13_BERUT_SOURCE_PACKAGE_AVAILABILITY_BOUNDARY': 'berut_source_package_availability_boundary', "
        "'T13_BERUT_FIGURE3_REMOTE_BINARY_IDENTITY': 'berut_figure3_remote_binary_identity', "
        "'T13_OXFORD_TGS_COMPARATOR_PROVENANCE': 'oxford_tgs_comparator_provenance'}"
    )
    text = replace_once(text, old_mapping, new_mapping, "lane key mapping")

    anchor = "\n".join([
        '    berut_source_lane = discovered_lane_integrations.get(',
        '        "berut_source_package_availability_boundary"',
        '    )',
    ]) + "\n"
    addition = "\n".join([
        '    oxford_source_lane = discovered_lane_integrations.get(',
        '        "oxford_tgs_comparator_provenance"',
        '    )',
        '    if oxford_source_lane:',
        '        artifact["verification_status"]["source_package"][',
        '            "oxford_tgs_comparator_provenance"',
        '        ] = oxford_source_lane',
        '        artifact["verification_status"]["eos_transport_kms_entropy"].pop(',
        '            "oxford_tgs_comparator_provenance", None',
        '        )',
    ]) + "\n"
    text = replace_once(text, anchor, addition + anchor, "source lane placement")

    closure_anchor = "\n".join([
        '    if discovered_lane_integrations.get("ding_fig1d_normalized_source_lane", {}).get("closure_level") == "CLOSED_FOR_LANE":',
        '        lane_closures.append("permitted Ding Fig. 1d normalized-source lane is closed for lane without raw-author or alpha claims")',
    ]) + "\n"
    closure_addition = "\n".join([
        '    if discovered_lane_integrations.get("oxford_tgs_comparator_provenance", {}).get("closure_level") == "CLOSED_FOR_LANE":',
        '        lane_closures.append("Oxford TGS Figure 1 provenance archive is closed for lane without numeric-row or calibration promotion")',
    ]) + "\n"
    text = replace_once(text, closure_anchor, closure_anchor + closure_addition, "lane closure projection")

    evidence_anchor = '    mp48_package_path = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/mp48_independent_graphite_cv_source_package.json"\n'
    evidence_addition = "\n".join([
        '    oxford_package_path = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/oxford_tgs_figure1_source_package.json"',
        '    if oxford_package_path.is_file() and not any(',
        '        item.get("path") == rel(oxford_package_path)',
        '        for item in artifact.get("evidence_artifacts", [])',
        '        if isinstance(item, dict)',
        '    ):',
        '        artifact["evidence_artifacts"].append(',
        '            evidence(',
        '                rel(oxford_package_path),',
        '                {},',
        '                {"status": "PASS_OXFORD_TGS_PROVENANCE_ARCHIVE_LOCKED_EXTRACTION_PENDING", "data_role": "TRAINING/COMPARISON", "numeric_rows_emitted": 0},',
        '            )',
        '        )',
    ]) + "\n"
    text = replace_once(text, evidence_anchor, evidence_addition + evidence_anchor, "source evidence linkage")

    TARGET.write_text(text, encoding="utf-8")
    print("ADDED_OXFORD_TGS_PROVENANCE_LANE_TO_TOPIC13_FULL_GATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
