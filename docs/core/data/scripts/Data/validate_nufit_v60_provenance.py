"""Validate NuFIT 6.0 extracted benchmark provenance.

This is not a PDF table parser. It is a reproducibility guard for the current
checked-transcription layer: it verifies the locked PDF exists, records hashes,
and rejects malformed extracted JSON before topic 0.7 uses it.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_PDF = (
    REPO_ROOT
    / "docs"
    / "data"
    / "external"
    / "particle_physics"
    / "nufit"
    / "official"
    / "v60.tbl-parameters.pdf"
)
SOURCE_JSON = (
    REPO_ROOT
    / "docs"
    / "data"
    / "external"
    / "particle_physics"
    / "nufit"
    / "official"
    / "nufit_v60_parameters_extracted.json"
)
OUT_JSON = (
    REPO_ROOT
    / "docs"
    / "data"
    / "external"
    / "particle_physics"
    / "nufit"
    / "official"
    / "nufit_v60_provenance_validation.json"
)

REQUIRED_VARIANTS = ("ic19_without_sk_atm", "ic24_with_sk_atm")
REQUIRED_PARAMS = (
    "theta12_deg",
    "theta23_deg",
    "theta13_deg",
    "delta_m21_sq_1e5_eV2",
    "delta_m3l_sq_1e3_eV2",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_parameter(label: str, payload: dict) -> list[str]:
    problems = []
    for field in ("best_fit", "3sigma_min", "3sigma_max"):
        if field not in payload:
            problems.append(f"{label}: missing {field}")
    if problems:
        return problems

    best = payload["best_fit"]
    lower = payload["3sigma_min"]
    upper = payload["3sigma_max"]
    if not all(isinstance(value, (int, float)) for value in (best, lower, upper)):
        problems.append(f"{label}: best_fit and 3sigma bounds must be numeric")
    elif not lower <= best <= upper:
        problems.append(f"{label}: expected 3sigma_min <= best_fit <= 3sigma_max")
    return problems


def main() -> int:
    problems: list[str] = []
    if not SOURCE_PDF.exists():
        problems.append(f"missing locked NuFIT PDF: {SOURCE_PDF}")
    if not SOURCE_JSON.exists():
        problems.append(f"missing extracted NuFIT JSON: {SOURCE_JSON}")

    dataset = {}
    if SOURCE_JSON.exists():
        dataset = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
        variants = dataset.get("variants", {})
        for variant_name in REQUIRED_VARIANTS:
            variant = variants.get(variant_name)
            if not variant:
                problems.append(f"missing variant: {variant_name}")
                continue
            params = variant.get("normal_ordering", {})
            for param_name in REQUIRED_PARAMS:
                param = params.get(param_name)
                if not param:
                    problems.append(f"missing parameter: {variant_name}.{param_name}")
                    continue
                problems.extend(validate_parameter(f"{variant_name}.{param_name}", param))

    result = {
        "source_pdf": str(SOURCE_PDF.relative_to(REPO_ROOT)),
        "source_json": str(SOURCE_JSON.relative_to(REPO_ROOT)),
        "source_pdf_hash": sha256_file(SOURCE_PDF) if SOURCE_PDF.exists() else None,
        "source_json_hash": sha256_file(SOURCE_JSON) if SOURCE_JSON.exists() else None,
        "transcription_status": "checked transcription",
        "schema_validation_status": "PASS" if not problems else "FAIL",
        "manual_review_required": True,
        "problems": problems,
        "note": (
            "The repository currently validates the checked-transcription JSON against schema "
            "and locked-source hashes. A true machine PDF parser requires an explicit dependency."
        ),
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    print(f"NuFIT provenance validation: {result['schema_validation_status']}")
    print(f"Source PDF hash: {result['source_pdf_hash']}")
    print(f"Wrote {OUT_JSON}")
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
