"""Audit whether funding flows can be joined to industry, labor, and physical resources.

The public macro package can identify aggregate funding channels, but it cannot
claim that a particular dollar paid for a particular labor/resource transformation.
This gate records which source-locked joins are present locally and which remain
missing or blocked.  It performs no imputation and no causal estimation.
"""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from economic_hardening_common import (
    ARTIFACT_DIR,
    BEA_1997_IO_ARTIFACT,
    BLS_IO_SOURCE_GATE_ARTIFACT,
    FED_Z1_FUNDING_MAPPING_ARTIFACT,
    RAW_ROOT,
    ROOT,
    sha256,
    utc_now,
    write_json,
)


ARTIFACT = ARTIFACT_DIR / "0_25_payer_resource_join_readiness.json"


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def _file_record(path: Path, role: str, status_if_present: str = "PASS") -> dict:
    exists = path.is_file()
    return {
        "role": role,
        "path": _relative(path) if exists else None,
        "exists": exists,
        "sha256": sha256(path) if exists else None,
        "status": status_if_present if exists else "MISSING",
    }


def _glob_record(directory: Path, pattern: str, role: str, status_if_present: str = "PASS") -> dict:
    files = sorted(path for path in directory.glob(pattern) if path.is_file()) if directory.exists() else []
    return {
        "role": role,
        "directory": _relative(directory),
        "pattern": pattern,
        "files": [_relative(path) for path in files],
        "hashes": { _relative(path): sha256(path) for path in files },
        "status": status_if_present if files else "MISSING",
    }


def _artifact_status(path: Path) -> dict:
    if not path.exists():
        return {"path": _relative(path), "exists": False, "status": "MISSING"}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        "path": _relative(path),
        "exists": True,
        "sha256": sha256(path),
        "status": payload.get("status", "UNKNOWN"),
        "controller_status": payload.get("controller_status"),
    }


def _xlsx_record(path: Path, role: str) -> dict:
    exists = path.is_file()
    sheets: list[str] = []
    valid = False
    if exists:
        try:
            with zipfile.ZipFile(path) as archive:
                workbook = archive.read("xl/workbook.xml").decode("utf-8", errors="replace")
                sheets = re.findall(r'<sheet[^>]+name="([^"]+)"', workbook)
                valid = bool(sheets)
        except (OSError, KeyError, zipfile.BadZipFile):
            valid = False
    digest = sha256(path) if exists else None
    manifest_path = path.parent / "source_manifest.json"
    manifest_exists = manifest_path.is_file()
    manifest_hash_matches = False
    if manifest_exists and digest:
        try:
            manifest_hash_matches = json.loads(manifest_path.read_text(encoding="utf-8")).get("sha256") == digest
        except (OSError, json.JSONDecodeError):
            manifest_hash_matches = False
    status = "PASS_WITH_BOUNDARY" if valid and manifest_hash_matches else ("WARN" if exists else "MISSING")
    return {
        "role": role,
        "path": _relative(path) if exists else None,
        "exists": exists,
        "sha256": digest,
        "sheet_names": sheets,
        "source_manifest": {
            "path": _relative(manifest_path) if manifest_exists else None,
            "exists": manifest_exists,
            "sha256": sha256(manifest_path) if manifest_exists else None,
            "hash_matches_data": manifest_hash_matches,
        },
        "status": status,
    }


def main() -> int:
    fed_z1_dir = RAW_ROOT / "fed_z1" / "2026-07-16"
    bls_io_dir = RAW_ROOT / "bls_io" / "2026-07-16"
    bea_dir = RAW_ROOT / "bea" / "2026-07-12"
    eia_dir = RAW_ROOT / "eia" / "2026-07-12"
    concordance_path = RAW_ROOT / "bea_io" / "2026-07-16" / "BEA-Industry-and-Commodity-Codes-and-NAICS-Concordance.xlsx"
    bea_benchmark = _artifact_status(BEA_1997_IO_ARTIFACT)
    benchmark_ready = bea_benchmark.get("status") == "PASS_WITH_BOUNDARY"

    evidence = {
        "funding_flows": {
            "status": "PASS_WITH_BOUNDARY",
            "artifact": _artifact_status(FED_Z1_FUNDING_MAPPING_ARTIFACT),
            "source": _file_record(fed_z1_dir / "z1_csv_files.zip", "Fed Z.1 sectoral transactions"),
            "boundary": "Aggregate sectoral channels and an accounting bridge are present; no payer-payee or project earmark is observed.",
        },
        "industry_input_output": {
            "status": "PASS_WITH_BOUNDARY" if benchmark_ready else "BLOCKED",
            "artifact": {
                "benchmark": bea_benchmark,
                "annual_bls_source_gate": _artifact_status(BLS_IO_SOURCE_GATE_ARTIFACT),
            },
            "source": _glob_record(bls_io_dir, "*", "BLS/BEA industry and commodity flows"),
            "boundary": "The 1997 BEA benchmark structure is source-locked and validated; the annual BLS/BEA flow lane remains unavailable and cannot be treated as a 1997-2024 panel.",
        },
        "bea_industry_accounts": {
            "status": "PASS_WITH_BOUNDARY" if benchmark_ready else "BLOCKED",
            "artifact": bea_benchmark,
            "source": _glob_record(bea_dir, "*input*output*", "BEA annual supply-use/input-output accounts"),
            "provider_access": {
                "official_page": "https://www.bea.gov/itable/input-output",
                "api_registration": "https://apps.bea.gov/api/signup/",
                "interactive_application": "https://apps.bea.gov/iTable/?Categories=Core&isURI=1&reqid=1602&step=2",
                "interactive_application_id": 52,
                "direct_backend_probe": {
                    "url": "https://apps.bea.gov/iTablecore/data/app/52",
                    "status_code": 500,
                    "table_rows_archived": False,
                    "anti_bot_bypass": False,
                },
                "status": "REGISTRATION_OR_INTERACTIVE_EXPORT_REQUIRED",
            },
            "boundary": "A source-locked 1997 benchmark is archived for structural validation; annual supply-use/input-output flow export still requires the BEA API or interactive application.",
        },
        "labor_industry_hours": {
            "status": "BLOCKED",
            "source": _glob_record(RAW_ROOT / "bls_labor" / "2026-07-16", "*", "BLS industry/occupation hours and labor input"),
            "boundary": "Aggregate productivity and employment proxies exist in the macro panel, but industry-level hours/occupations are not archived for concordance.",
        },
        "energy_throughput": {
            "status": "PASS_WITH_BOUNDARY",
            "source": _glob_record(eia_dir, "*.csv", "EIA energy throughput"),
            "boundary": "Energy throughput is available; it is not a complete material-extraction or project-level resource ledger.",
        },
        "material_quantities": {
            "status": "BLOCKED",
            "source": {
                "required_providers": ["USGS", "FAOSTAT", "EIA source-level extraction/environmental accounts"],
                "local_archives": [],
                "status": "MISSING",
            },
            "boundary": "No source-locked physical material quantity panel and industry concordance are present.",
        },
        "firm_project_payment_ledger": {
            "status": "BLOCKED",
            "source": {
                "required_providers": ["Census business microdata", "administrative ACH/card/invoice records"],
                "local_archives": [],
                "status": "MISSING",
            },
            "boundary": "Public aggregate accounts cannot identify which payer funded which purchase or project.",
        },
        "industry_concordance": {
            "status": "PASS_WITH_BOUNDARY" if concordance_path.is_file() else "BLOCKED",
            "source": _xlsx_record(concordance_path, "BEA industry and commodity codes / NAICS concordance"),
            "boundary": "The BEA code concordance is archived and hashed, but it does not itself provide payer, labor-hours, or physical-resource observations.",
        },
    }
    blocking = [name for name, item in evidence.items() if item["status"] in {"BLOCKED", "MISSING"}]
    payload = {
        "schema_version": "1.0",
        "topic": "0.25_Strategy_Power_Economics",
        "status": "BLOCKED" if blocking else "PASS_WITH_BOUNDARY",
        "controller_status": "PAYER_RESOURCE_JOIN_NOT_IDENTIFIED" if blocking else "PAYER_RESOURCE_JOIN_SOURCE_READY",
        "generated_at_utc": utc_now(),
        "coverage": {"requested": "sectoral funding -> industry use -> labor hours -> physical resources -> output/innovation", "no_imputation": True},
        "evidence": evidence,
        "blocking_components": blocking,
        "required_join": [
            "transaction or firm/project funding records",
            "industry/commodity input-output table",
            "industry labor hours and occupations",
            "source-level physical resource quantities",
            "versioned industry/commodity/labor/resource concordance",
        ],
        "claim_boundary": "This gate reports source/join readiness only. It does not infer payment-level provenance, funding shares, resource causality, or innovation causality.",
        "limitations": [
            "Operating surplus and net saving are accounting aggregates, not earmarked cash sources.",
            "Debt and equity liability transactions can include refinancing, redemptions, and repurchases.",
            "A complete public dataset linking every payment to a physical resource transformation is not present in the frozen package.",
        ],
    }
    write_json(ARTIFACT, payload)
    print("Payer-resource join readiness:", payload["status"], "blocking components", len(blocking))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
