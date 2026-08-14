"""Keep the Berut Figure 3 binary-identity sync in the wave runner."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / "docs/scripts/audit/run_topic13_berut_figure3_binary_identity_wave.py"


def main() -> int:
    text = RUNNER.read_text(encoding="utf-8-sig")
    if "'sync_topic13_berut_figure3_binary_identity.py'" in text:
        print("BERUT_BINARY_SYNC_ALREADY_IN_RUNNER")
        return 0
    anchor = "        'sync_topic13_berut_source_package_availability.py',\n"
    if anchor not in text:
        raise SystemExit("Berut binary runner anchor not found")
    text = text.replace(
        anchor,
        anchor + "        'sync_topic13_berut_figure3_binary_identity.py',\n",
        1,
    )
    RUNNER.write_text(text, encoding="utf-8")
    print("PATCHED_BERUT_BINARY_SYNC_RUNNER_ORDER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

