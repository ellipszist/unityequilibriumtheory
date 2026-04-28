"""Extract the source-locked Muon g-2 2025 experimental result from local HTML."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DOE_HTML = REPO_ROOT / "docs" / "data" / "external" / "particle_physics" / "muon_g2" / "doe_muon_g2_2025_press_release.html"
OUT_JSON = REPO_ROOT / "docs" / "data" / "external" / "particle_physics" / "muon_g2" / "fermilab_muon_g2_2025_experiment.json"


def parse_value(text: str) -> dict:
    pattern = re.compile(
        r"a<sub>μ</sub>\s*=\s*\(g-2\)/2 \(muon, experiment\)\s*=\s*"
        r"([0-9.\s]+)\s*\+-\s*([0-9.\s]+)\(stat\.\).*?\+-\s*([0-9.\s]+)\(syst\.\)",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError("Could not locate 2025 muon g-2 experimental value in DOE HTML")

    def clean_number(raw: str) -> float:
        return float(raw.replace(" ", ""))

    value = clean_number(match.group(1))
    stat = clean_number(match.group(2))
    syst = clean_number(match.group(3))
    combined = math.sqrt(stat**2 + syst**2)
    return {
        "a_mu_exp": value,
        "stat_error": stat,
        "syst_error": syst,
        "combined_error": combined,
    }


def main() -> int:
    text = DOE_HTML.read_text(encoding="utf-8", errors="replace")
    parsed = parse_value(text)
    payload = {
        "source": "DOE/Fermilab Muon g-2 final 2025 press release mirror",
        "source_file": str(DOE_HTML.relative_to(REPO_ROOT)),
        "published_date": "2025-06-03",
        "precision_ppb": 127,
        "data": parsed,
        "note": "This file records the experimental measurement only. Standard-Model comparison values must be tracked separately.",
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
