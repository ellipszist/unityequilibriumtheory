"""Run the Berut Figure 3 remote-binary identity wave."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT_DIR = ROOT / 'docs/scripts/audit'


def run(relative: str) -> int:
    completed = subprocess.run(
        [sys.executable, str(AUDIT_DIR / relative)],
        cwd=ROOT,
        check=False,
    )
    return completed.returncode


def main() -> int:
    for relative in (
        'repair_topic13_berut_figure3_numeric_metadata.py',
        'audit_topic13_berut_source_package_availability.py',
        'audit_topic13_berut_figure3_binary_identity.py',
        'repair_topic13_berut_source_lane_key.py',
        'repair_topic13_berut_binary_lane_routing.py',
        'audit_topic13_full_bridge_gate.py',
        'sync_topic13_berut_source_package_availability.py',
        'sync_topic13_berut_figure3_binary_identity.py',
        'audit_major_result_dependency_unlock.py',
    ):
        result = run(relative)
        if result != 0:
            return result
    print('PASS_TOPIC13_BERUT_FIGURE3_BINARY_IDENTITY_WAVE')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

