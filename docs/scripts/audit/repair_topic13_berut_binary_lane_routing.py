"""Route the Figure 3 binary identity result to the source-package lane."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GATE = ROOT / 'docs/scripts/audit/audit_topic13_full_bridge_gate.py'


def main() -> int:
    text = GATE.read_text(encoding='utf-8-sig')
    changed = False
    lane_anchor = "'T13_BERUT_SOURCE_PACKAGE_AVAILABILITY_BOUNDARY': 'berut_source_package_availability_boundary'"
    lane_entry = ", 'T13_BERUT_FIGURE3_REMOTE_BINARY_IDENTITY': 'berut_figure3_remote_binary_identity'"
    if 'T13_BERUT_FIGURE3_REMOTE_BINARY_IDENTITY' not in text:
        if lane_anchor not in text:
            raise SystemExit('Berut source lane key anchor not found')
        text = text.replace(lane_anchor, lane_anchor + lane_entry, 1)
        changed = True

    route_anchor = '''        artifact["verification_status"]["eos_transport_kms_entropy"].pop(
            "berut_source_package_availability_boundary", None
        )
'''
    route_addition = '''        binary_lane = discovered_lane_integrations.get(
            "berut_figure3_remote_binary_identity"
        )
        if binary_lane:
            artifact["verification_status"]["source_package"][
                "berut_figure3_remote_binary_identity"
            ] = binary_lane
            artifact["verification_status"]["eos_transport_kms_entropy"].pop(
                "berut_figure3_remote_binary_identity", None
            )
'''
    if 'binary_lane = discovered_lane_integrations.get' not in text:
        if route_anchor not in text:
            raise SystemExit('Berut source routing block not found')
        text = text.replace(route_anchor, route_anchor + route_addition, 1)
        changed = True

    GATE.write_text(text, encoding='utf-8')
    print({'status': 'PASS_BERUT_FIGURE3_BINARY_LANE_ROUTING', 'changed': changed})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

