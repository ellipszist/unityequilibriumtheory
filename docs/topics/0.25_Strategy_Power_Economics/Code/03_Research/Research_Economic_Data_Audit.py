"""Topic 0.25 verification: economic data and market time-series audit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import statistics
import sys
from datetime import UTC, datetime
from pathlib import Path


def bootstrap_repo() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    raise RuntimeError("Repository root with docs/core was not found.")


ROOT = bootstrap_repo()
TOPIC = ROOT / "docs" / "topics" / "0.25_Strategy_Power_Economics"
DATA = TOPIC / "Data"
ARTIFACT = TOPIC / "Result" / "artifacts" / "0_25_strategy_power_economics_verification.json"
SOURCE_EVIDENCE_INTAKE = DATA / "03_Research" / "source_evidence_intake_stub.json"
SOURCE_EVIDENCE_READINESS = DATA / "03_Research" / "source_evidence_readiness_matrix.json"
MODEL_CLAIM_GATE = DATA / "03_Research" / "model_claim_gate.json"
SOURCE_LOCK_MANIFEST = DATA / "03_Research" / "source_lock_manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload


def find_source_target(source_lock: dict, suffix: str) -> dict:
    for item in source_lock.get("source_targets", []):
        if item.get("local_path", "").endswith(suffix):
            return item
    return {}


def load_yahoo_close(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        next(reader, None)  # ticker row
        next(reader, None)  # Date placeholder row
        close_index = header.index("Close")
        for raw in reader:
            if not raw or len(raw) <= close_index:
                continue
            try:
                close = float(raw[close_index])
            except ValueError:
                continue
            if math.isfinite(close) and close > 0:
                rows.append({"date": raw[0], "close": close})
    return rows


def returns(closes: list[float]) -> list[float]:
    return [math.log(b / a) for a, b in zip(closes, closes[1:]) if a > 0 and b > 0]


def pearson(a: list[float], b: list[float]) -> float | None:
    n = min(len(a), len(b))
    if n < 3:
        return None
    x = a[-n:]
    y = b[-n:]
    mx = sum(x) / n
    my = sum(y) / n
    vx = sum((v - mx) ** 2 for v in x)
    vy = sum((v - my) ** 2 for v in y)
    if vx <= 0 or vy <= 0:
        return None
    return sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / math.sqrt(vx * vy)


def series_metrics(name: str, path: Path) -> dict:
    rows = load_yahoo_close(path)
    closes = [row["close"] for row in rows]
    rets = returns(closes)
    annualized_volatility = statistics.pstdev(rets) * math.sqrt(252) if len(rets) > 1 else None
    total_return = closes[-1] / closes[0] - 1.0 if len(closes) > 1 else None
    return {
        "name": name,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha256(path),
        "row_count": len(rows),
        "first_date": rows[0]["date"] if rows else None,
        "last_date": rows[-1]["date"] if rows else None,
        "first_close": closes[0] if closes else None,
        "last_close": closes[-1] if closes else None,
        "total_return": total_return,
        "annualized_volatility": annualized_volatility,
        "returns": rets,
    }


def economy_metrics(path: Path) -> dict:
    data = load_json(path)
    economies = data.get("Economies", {})
    gini_values = [float(item["Gini"]) for item in economies.values() if "Gini" in item]
    gdp_values = [float(item["GDP_PPP_USD"]) for item in economies.values() if "GDP_PPP_USD" in item]
    pop_values = [float(item["Population"]) for item in economies.values() if "Population" in item]
    return {
        "source": data.get("Source", "unspecified"),
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha256(path),
        "economy_count": len(economies),
        "gini_min": min(gini_values) if gini_values else None,
        "gini_max": max(gini_values) if gini_values else None,
        "gdp_ppp_total_usd": sum(gdp_values),
        "population_total": sum(pop_values),
        "world_total": economies.get("World_Total", {}),
    }


def build_source_evidence_intake_stub() -> dict:
    source_lock = load_json(SOURCE_LOCK_MANIFEST) if SOURCE_LOCK_MANIFEST.exists() else {}
    shared_yahoo = source_lock.get("shared_external_reference", {})
    sp500_lock = find_source_target(source_lock, "Data/03_Research/SP500_yahoo_real.csv")
    gold_lock = find_source_target(source_lock, "Data/03_Research/Gold_yahoo_real.csv")
    bitcoin_lock = find_source_target(source_lock, "Data/03_Research/Bitcoin_yahoo_real.csv")
    economy_lock = find_source_target(source_lock, "Data/Global_Economy_2024.json")
    snapshot_lock = find_source_target(source_lock, "Data/03_Research/daily_economic_snapshot.json")

    provider_url = "https://finance.yahoo.com/"

    payload = {
        "schema_version": "1.0",
        "topic": "0.25_Strategy_Power_Economics",
        "purpose": "Structured intake stub for external-source evidence before economic data rewrites or stronger strategy/policy claims.",
        "instructions": [
            "Attach upstream URL or DOI, local archive path, retrieval date, and extraction note before changing a working-copy dataset.",
            "Record unit convention and symbol or ticker identity for each market or macroeconomic source.",
            "Do not treat this file as the evidence itself; it is an intake and tracking layer."
        ],
        "source_targets": [
            {
                "name": "SP500 Yahoo-style market download metadata",
                "priority": "immediate",
                "status": "partial",
                "evidence_fields": [
                    {"field": "ticker_or_symbol", "status": "complete", "value": sp500_lock.get("ticker", "^GSPC")},
                    {"field": "upstream_url_or_query", "status": "complete", "value": provider_url},
                    {"field": "local_path", "status": "complete", "value": sp500_lock.get("local_path", "")},
                    {"field": "retrieval_date", "status": "pending", "value": ""},
                    {"field": "unit_basis", "status": "complete", "value": sp500_lock.get("unit_system", "")},
                    {"field": "extraction_note", "status": "complete", "value": sp500_lock.get("source_note", "")},
                ],
            },
            {
                "name": "Gold Yahoo-style market download metadata",
                "priority": "immediate",
                "status": "partial",
                "evidence_fields": [
                    {"field": "ticker_or_symbol", "status": "complete", "value": gold_lock.get("ticker", "GC=F")},
                    {"field": "upstream_url_or_query", "status": "complete", "value": provider_url},
                    {"field": "local_path", "status": "complete", "value": gold_lock.get("local_path", "")},
                    {"field": "retrieval_date", "status": "pending", "value": ""},
                    {"field": "unit_basis", "status": "complete", "value": gold_lock.get("unit_system", "")},
                    {"field": "extraction_note", "status": "complete", "value": gold_lock.get("source_note", "")},
                ],
            },
            {
                "name": "Bitcoin Yahoo-style market download metadata",
                "priority": "immediate",
                "status": "partial",
                "evidence_fields": [
                    {"field": "ticker_or_symbol", "status": "complete", "value": bitcoin_lock.get("ticker", "BTC-USD")},
                    {"field": "upstream_url_or_query", "status": "complete", "value": provider_url},
                    {"field": "local_path", "status": "complete", "value": bitcoin_lock.get("local_path", "")},
                    {"field": "retrieval_date", "status": "pending", "value": ""},
                    {"field": "unit_basis", "status": "complete", "value": bitcoin_lock.get("unit_system", "")},
                    {"field": "extraction_note", "status": "complete", "value": bitcoin_lock.get("source_note", "")},
                ],
            },
            {
                "name": "Global economy baseline source package",
                "priority": "high",
                "status": "partial",
                "evidence_fields": [
                    {"field": "world_bank_or_imf_url_or_doi", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "complete", "value": economy_lock.get("local_path", "")},
                    {"field": "table_identifier", "status": "complete", "value": "Economies.World_Total, USA, China, Thailand, Norway, South_Africa"},
                    {"field": "retrieval_date", "status": "pending", "value": ""},
                    {"field": "unit_basis", "status": "complete", "value": economy_lock.get("unit_system", "")},
                    {"field": "extraction_note", "status": "complete", "value": economy_lock.get("source_note", "")},
                ],
            },
            {
                "name": "Daily economic snapshot upstream feed",
                "priority": "high",
                "status": "partial",
                "evidence_fields": [
                    {"field": "upstream_url_or_api", "status": "pending", "value": ""},
                    {"field": "local_path", "status": "complete", "value": snapshot_lock.get("local_path", "")},
                    {"field": "snapshot_timestamp_basis", "status": "complete", "value": "topic-local date stamp in daily_economic_snapshot.json"},
                    {"field": "indicator_mapping", "status": "complete", "value": "SET_INDEX points; GOLD_PRICE USD/oz; USD_THB THB; GDP_GROWTH_REALTIME percent"},
                    {"field": "unit_basis", "status": "complete", "value": snapshot_lock.get("unit_system", "")},
                    {"field": "extraction_note", "status": "complete", "value": snapshot_lock.get("source_note", "")},
                ],
            },
        ],
        "claim_boundary": (
            "This intake stub is for source evidence capture only. Filling it does not by itself justify "
            "strategic-superiority, policy-causality, or social-stabilization claim upgrades."
        ),
        "source_lock_dependencies": [target.get("local_path") for target in source_lock.get("source_targets", [])] + ([shared_yahoo.get("local_path")] if shared_yahoo.get("local_path") else []),
    }
    return write_json(SOURCE_EVIDENCE_INTAKE, payload)


def build_source_evidence_readiness_matrix(intake_stub: dict) -> dict:
    rows = []
    ready = 0
    blocked = 0
    for target in intake_stub["source_targets"]:
        pending_fields = [field["field"] for field in target["evidence_fields"] if field.get("status") != "complete"]
        fields_total = len(target["evidence_fields"])
        fields_complete = fields_total - len(pending_fields)
        row_ready = not pending_fields
        if row_ready:
            ready += 1
        else:
            blocked += 1
        rows.append(
            {
                "name": target["name"],
                "priority": target["priority"],
                "fields_total": fields_total,
                "fields_complete": fields_complete,
                "fields_pending": len(pending_fields),
                "pending_fields": pending_fields,
                "target_status": target.get("status", "pending"),
                "ready_for_source_review": row_ready,
                "blocking_reason": "" if row_ready else "One or more required evidence fields are still pending.",
            }
        )
    payload = {
        "schema_version": "1.0",
        "topic": "0.25_Strategy_Power_Economics",
        "purpose": "Readiness matrix for economic source evidence before data edits or claim upgrades.",
        "summary": {
            "source_targets_total": len(rows),
            "targets_ready_for_source_review": ready,
            "targets_blocked_by_pending_evidence": blocked,
        },
        "readiness_rows": rows,
        "claim_boundary": (
            "This matrix is a workflow gate only. A target marked ready still requires actual source review before "
            "working-copy or claim changes."
        ),
    }
    return write_json(SOURCE_EVIDENCE_READINESS, payload)


def build_model_claim_gate() -> dict:
    payload = {
        "schema_version": "1.0",
        "topic": "0.25_Strategy_Power_Economics",
        "purpose": "Claim gate for diagnostic, simulation, and policy lanes inside the topic.",
        "summary": {
            "lanes_total": 5,
            "accepted_now": 2,
            "blocked_for_strong_claims": 3,
        },
        "lanes": [
            {
                "lane": "Market time-series diagnostics",
                "status": "accepted_descriptive_only",
                "allowed_usage_now": "Descriptive returns, volatility, and correlations from local working copies.",
                "blocker_to_stronger_claim": "Need source-locked upstream download metadata and comparator baselines."
            },
            {
                "lane": "Economy baseline sanity",
                "status": "accepted_descriptive_only",
                "allowed_usage_now": "Population, GDP PPP, and Gini range sanity from the local working copy.",
                "blocker_to_stronger_claim": "Need source-locked macro tables and exact extraction lineage."
            },
            {
                "lane": "Daily snapshot context",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Local context only.",
                "blocker_to_stronger_claim": "Need upstream API/source record, timestamp basis, and indicator lineage."
            },
            {
                "lane": "Social power engine and 8-billion resonance scripts",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "Heuristic simulation proposal only.",
                "blocker_to_stronger_claim": "Need seeded deterministic verifier, calibration target, and real-world benchmark linkage."
            },
            {
                "lane": "Policy and strategic-superiority claims",
                "status": "blocked_for_strong_claims",
                "allowed_usage_now": "No superiority or causality claim.",
                "blocker_to_stronger_claim": "Need counterfactual baseline, policy outcome data, uncertainty, and explicit causal design."
            },
        ],
        "claim_boundary": "This gate cannot raise claim strength above descriptive diagnostics without new verifier-backed evidence.",
    }
    return write_json(MODEL_CLAIM_GATE, payload)


def build_descriptive_diagnostic_gate(checks: dict, blockers: list[str], source_readiness: dict) -> dict:
    diagnostic_checks = {
        "market_rows_ok": checks.get("market_rows_ok", False),
        "gini_range_ok": checks.get("gini_range_ok", False),
    }
    provenance_checks = {
        "snapshot_has_source_url": checks.get("snapshot_has_source_url", False),
        "economy_has_source_url": checks.get("economy_has_source_url", False),
    }
    diagnostic_pass = all(diagnostic_checks.values())
    provenance_pass = all(provenance_checks.values()) and source_readiness["summary"]["targets_blocked_by_pending_evidence"] == 0
    return {
        "gate": "descriptive_economic_diagnostic_gate",
        "status": "DESCRIPTIVE_WARN" if diagnostic_pass and not provenance_pass else ("PASS" if diagnostic_pass else "FAIL"),
        "diagnostic_run_contract": "PASS" if diagnostic_pass else "FAIL",
        "provenance_gate": "PASS" if provenance_pass else "OPEN",
        "diagnostic_checks": diagnostic_checks,
        "provenance_checks": provenance_checks,
        "blockers": blockers,
        "blocked_claim_classes": [
            "policy causality",
            "strategic superiority",
            "social stabilization",
            "market prediction",
            "game-theory improvement claim",
        ],
        "claim_boundary": "This gate can pass only descriptive market/economy diagnostics. Policy, prediction, and strategic claims remain blocked until upstream provenance, baselines, and causal design are present.",
    }


def build_economics_claim_scope_gate(
    status: str,
    checks: dict,
    blockers: list[str],
    source_readiness: dict,
    model_claim_gate: dict,
    descriptive_diagnostic_gate: dict,
) -> dict:
    return {
        "gate": "economics_claim_scope_gate",
        "controller_status": "DESCRIPTIVE_DIAGNOSTIC_ONLY",
        "controller_reason": (
            "The artifact supports internal market/economy data diagnostics only. "
            "Policy, prediction, social-stabilization, and strategic-superiority exports remain blocked."
        ),
        "claim_class": "C_internal_economic_data_diagnostic",
        "allowed_claims_now": [
            {
                "claim": "Local market series row-count and close-price parsing diagnostics ran.",
                "condition": "market_rows_ok is true",
                "status": "allowed" if checks.get("market_rows_ok") else "blocked",
            },
            {
                "claim": "Local Gini values satisfy the declared 0-100 unit sanity check.",
                "condition": "gini_range_ok is true",
                "status": "allowed" if checks.get("gini_range_ok") else "blocked",
            },
            {
                "claim": "Return volatility and correlation metrics are descriptive statistics over local working copies.",
                "condition": "artifact status is PASS or WARN",
                "status": "allowed" if status in {"PASS", "WARN"} else "blocked",
            },
        ],
        "blocked_claims": [
            {
                "claim": "UET predicts future market prices or macroeconomic outcomes.",
                "blocker": "No out-of-sample forecast protocol, baseline comparison, or uncertainty calibration is present.",
            },
            {
                "claim": "The social power engine proves strategic superiority or Nash-equilibrium improvement.",
                "blocker": "Simulation lanes are heuristic and lack calibrated game-theory comparators.",
            },
            {
                "claim": "The topic validates real-world policy causality or social stabilization.",
                "blocker": "No causal identification design, policy-outcome dataset, or intervention baseline is verifier-gated.",
            },
            {
                "claim": "Local gateway/economy working copies are archival macroeconomic evidence.",
                "blocker": "Upstream URL/API, retrieval date, and table lineage remain incomplete for at least one input lane.",
            },
        ],
        "blocked_export_phrases": [
            "UET predicts markets",
            "strategic superiority proved",
            "Nash equilibrium improved",
            "policy causality verified",
            "social stabilization achieved",
            "8-billion resonance validated",
            "world lease model proven",
            "economic law confirmed",
        ],
        "machine_readable_next_blockers": [
            "market_retrieval_dates_missing",
            "global_economy_upstream_url_or_doi_missing",
            "daily_snapshot_upstream_url_or_api_missing",
            "forecast_baseline_protocol_missing",
            "causal_policy_design_missing",
            "social_power_engine_calibration_missing",
        ],
        "gate_inputs": {
            "artifact_status": status,
            "checks": checks,
            "blockers": blockers,
            "source_targets_blocked": source_readiness["summary"]["targets_blocked_by_pending_evidence"],
            "model_gate_summary": model_claim_gate.get("summary", {}),
            "descriptive_gate_status": descriptive_diagnostic_gate.get("status"),
            "descriptive_provenance_gate": descriptive_diagnostic_gate.get("provenance_gate"),
        },
        "claim_boundary": (
            "0.25 may be cited as an internal economic-data diagnostic and provenance-hardening topic only. "
            "It must not be exported as a market predictor, policy engine, or validated strategy framework until "
            "source locks, forecast baselines, causal design, and calibrated simulation comparators are present."
        ),
    }


def main() -> int:
    series = [
        series_metrics("SP500", DATA / "03_Research" / "SP500_yahoo_real.csv"),
        series_metrics("Gold", DATA / "03_Research" / "Gold_yahoo_real.csv"),
        series_metrics("Bitcoin", DATA / "03_Research" / "Bitcoin_yahoo_real.csv"),
    ]
    economy = economy_metrics(DATA / "Global_Economy_2024.json")
    snapshot_path = DATA / "03_Research" / "daily_economic_snapshot.json"
    snapshot = load_json(snapshot_path)
    source_evidence_intake = build_source_evidence_intake_stub()
    source_evidence_readiness = build_source_evidence_readiness_matrix(source_evidence_intake)
    model_claim_gate = build_model_claim_gate()

    sp500 = next(item for item in series if item["name"] == "SP500")
    gold = next(item for item in series if item["name"] == "Gold")
    bitcoin = next(item for item in series if item["name"] == "Bitcoin")

    correlations = {
        "sp500_gold_return_corr": pearson(sp500["returns"], gold["returns"]),
        "sp500_bitcoin_return_corr": pearson(sp500["returns"], bitcoin["returns"]),
        "gold_bitcoin_return_corr": pearson(gold["returns"], bitcoin["returns"]),
    }

    thresholds = {
        "min_rows_per_market_series": 2500,
        "gini_range_min": 0.0,
        "gini_range_max": 100.0,
        "require_snapshot_source_url": True,
        "require_economy_source_url_or_doi": True,
    }

    checks = {
        "market_rows_ok": all(item["row_count"] >= thresholds["min_rows_per_market_series"] for item in series),
        "gini_range_ok": economy["gini_min"] is not None
        and economy["gini_max"] is not None
        and economy["gini_min"] >= thresholds["gini_range_min"]
        and economy["gini_max"] <= thresholds["gini_range_max"],
        "snapshot_has_source_url": "url" in snapshot or "URL" in snapshot or "doi" in snapshot or "DOI" in snapshot,
        "economy_has_source_url": "url" in economy["source"].lower() or "doi" in economy["source"].lower(),
    }

    blockers = []
    if not checks["market_rows_ok"]:
        blockers.append("At least one market time series is too short for the provisional history-length gate.")
    if not checks["gini_range_ok"]:
        blockers.append("Global economy Gini values fall outside the declared 0-100 unit convention.")
    if not checks["snapshot_has_source_url"]:
        blockers.append("daily_economic_snapshot.json has no upstream URL/DOI; source is a local gateway label.")
    if not checks["economy_has_source_url"]:
        blockers.append("Global_Economy_2024.json names World Bank/IMF references but does not record a URL/DOI.")

    status = "PASS" if all(checks.values()) else "WARN"
    descriptive_diagnostic_gate = build_descriptive_diagnostic_gate(checks, blockers, source_evidence_readiness)
    economics_claim_scope_gate = build_economics_claim_scope_gate(
        status,
        checks,
        blockers,
        source_evidence_readiness,
        model_claim_gate,
        descriptive_diagnostic_gate,
    )

    for item in series:
        item.pop("returns", None)

    artifact = {
        "schema_version": "1.2",
        "topic": "0.25_Strategy_Power_Economics",
        "status": status,
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "command": "python docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Research_Economic_Data_Audit.py",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "claim_class": "C - internal economic data integrity and market diagnostics benchmark",
        "formula_ids": [
            "EC25-LOG-RETURN",
            "EC25-ANNUALIZED-VOLATILITY",
            "EC25-RETURN-CORRELATION",
            "EC25-GINI-SANITY",
        ],
        "inputs": [
            {key: item[key] for key in ("name", "path", "sha256", "row_count", "first_date", "last_date")}
            for item in series
        ]
        + [
            {
                "name": "Global_Economy_2024",
                "path": economy["path"],
                "sha256": economy["sha256"],
                "source": economy["source"],
            },
            {
                "name": "daily_economic_snapshot",
                "path": str(snapshot_path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(snapshot_path),
                "source": snapshot.get("source", "unspecified"),
                "timestamp": snapshot.get("timestamp"),
            },
            {
                "name": "source_lock_manifest",
                "path": str(SOURCE_LOCK_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(SOURCE_LOCK_MANIFEST),
                "source": "topic-derived economic source-lock manifest",
            },
        ],
        "threshold": thresholds,
        "checks": checks,
        "blockers": blockers,
        "source_evidence_intake_stub": {
            "path": str(SOURCE_EVIDENCE_INTAKE.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(SOURCE_EVIDENCE_INTAKE),
            "source_targets": [item["name"] for item in source_evidence_intake["source_targets"]],
            "claim_boundary": "This intake stub is for source evidence capture only. It does not authorize data or claim upgrades by itself.",
        },
        "source_evidence_readiness_matrix": {
            "path": str(SOURCE_EVIDENCE_READINESS.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(SOURCE_EVIDENCE_READINESS),
            "summary": source_evidence_readiness["summary"],
            "claim_boundary": "This readiness matrix is a workflow gate only. It tracks whether source evidence is still pending.",
        },
        "model_claim_gate": {
            "path": str(MODEL_CLAIM_GATE.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(MODEL_CLAIM_GATE),
            "summary": model_claim_gate["summary"],
            "claim_boundary": "This gate records diagnostic versus simulation claim ceilings only. It cannot upgrade the topic beyond descriptive evidence.",
        },
        "descriptive_diagnostic_gate": descriptive_diagnostic_gate,
        "economics_claim_scope_gate": economics_claim_scope_gate,
        "market_metrics": series,
        "economy_metrics": economy,
        "correlations": correlations,
        "snapshot": snapshot,
        "limitations": [
            "This artifact validates local data integrity and descriptive market/economy diagnostics only.",
            "It does not prove strategic superiority, social stabilization, Nash-equilibrium improvement, or policy causality.",
            "Upstream provenance for the economy and daily snapshot data remains below archival standard.",
        ],
    }

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")

    print("UET 0.25 economic data audit")
    print(f"  status: {status}")
    for item in series:
        print(
            f"  {item['name']}: rows={item['row_count']}, range={item['first_date']}..{item['last_date']}, "
            f"vol={item['annualized_volatility']:.4f}"
        )
    print(f"  gini range: {economy['gini_min']}..{economy['gini_max']}")
    print(f"  artifact: {ARTIFACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
