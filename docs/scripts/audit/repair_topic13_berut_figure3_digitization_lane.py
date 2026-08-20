"""Route the scoped Berut Figure 3c digitization lane through the full gate."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GATE = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> int:
    text = GATE.read_text(encoding="utf-8-sig")
    changed = False
    anchor = "'T13_BERUT_FIGURE3_REMOTE_BINARY_IDENTITY': 'berut_figure3_remote_binary_identity'"
    addition = anchor + ", 'T13_BERUT_FIGURE3_DIGITIZATION': 'berut_figure3_digitization'"
    if "T13_BERUT_FIGURE3_DIGITIZATION" not in text:
        if anchor not in text:
            raise SystemExit("Berut Figure 3 binary lane-map anchor not found")
        text = text.replace(anchor, addition, 1)
        changed = True

    route_anchor = (
        '            artifact["verification_status"]["eos_transport_kms_entropy"].pop(\n'
        '                "berut_figure3_remote_binary_identity", None\n'
        '            )\n'
    )
    route_addition = (
        '            digitization_lane = discovered_lane_integrations.get(\n'
        '                "berut_figure3_digitization"\n'
        '            )\n'
        '            if digitization_lane:\n'
        '                artifact["verification_status"]["source_package"][\n'
        '                    "berut_figure3_digitization"\n'
        '                ] = digitization_lane\n'
        '                artifact["verification_status"]["eos_transport_kms_entropy"].pop(\n'
        '                    "berut_figure3_digitization", None\n'
        '                )\n'
    )
    if "digitization_lane = discovered_lane_integrations.get" not in text:
        if route_anchor not in text:
            raise SystemExit("Berut Figure 3 source routing anchor not found")
        text = text.replace(route_anchor, route_anchor + route_addition, 1)
        changed = True

    closure_anchor = (
        '    if discovered_lane_integrations.get("ding_material_regime_boundary", {}).get('
        '"closure_level") == "CLOSED_FOR_LANE":\n'
    )
    closure_addition = (
        '    if discovered_lane_integrations.get("berut_figure3_digitization", {}).get('
        '"closure_level") == "CLOSED_FOR_LANE":\n'
        '        lane_closures.append("Berut Figure 3c marker transcription and '
        'figure-derived comparison boundary are closed for lane; raw numeric source, '
        'source-grade error bars, SI mapping, alpha, and external validation remain open")\n'
    )
    if "Berut Figure 3c marker transcription and figure-derived comparison boundary" not in text:
        if closure_anchor not in text:
            raise SystemExit("Topic 13 lane-closure insertion anchor not found")
        text = text.replace(closure_anchor, closure_addition + closure_anchor, 1)
        changed = True

    GATE.write_text(text, encoding="utf-8")
    print({"status": "PASS_BERUT_FIGURE3_DIGITIZATION_LANE_ROUTING", "changed": changed})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
