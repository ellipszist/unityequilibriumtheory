"""Repair deterministic Oxford TGS provenance metadata and audit logic."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / (
    "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/"
    "oxford_tgs_figure1_source_package.json"
)
AUDIT = ROOT / "docs/scripts/audit/audit_topic13_oxford_tgs_comparator_provenance.py"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    package = json.loads(PACKAGE.read_text(encoding="utf-8-sig"))
    for record in package["raw_files"]:
        path = ROOT / record["local_path"]
        record["bytes"] = path.stat().st_size
        record["sha256"] = sha256(path)
    PACKAGE.write_text(json.dumps(package, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    text = AUDIT.read_text(encoding="utf-8-sig")
    old_header = 'mat_header = mat_path.read_bytes()[:8] if mat_path.is_file() else b""'
    new_header = 'mat_header = mat_path.read_bytes()[512:520] if mat_path.is_file() else b""'
    if old_header not in text:
        raise SystemExit("MAT header expression not found")
    text = text.replace(old_header, new_header, 1)
    old_claim = '"claim_boundary_is_explicit": "not a Ding PBTE numeric source" in package["claim_boundary"],'
    new_claim = (
        '"claim_boundary_is_explicit": '
        '"not a Ding PBTE numeric source" in package["major_result"]["claim_boundary"],'
    )
    if old_claim not in text:
        raise SystemExit("claim-boundary check not found")
    text = text.replace(old_claim, new_claim, 1)
    text = text.replace(
        '"mat_header_hex": mat_header.hex(),',
        '"mat_header_offset": 512,\n        "mat_header_hex": mat_header.hex(),',
        1,
    )
    AUDIT.write_text(text, encoding="utf-8")
    print("REPAIRED_OXFORD_TGS_PROVENANCE_METADATA_AND_HEADER_CHECK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
