"""Shared, dependency-light utilities for the Topic 0.25 economics hardening lane.

The helpers intentionally preserve raw source identity and make a missing source a
machine-readable blocker.  They must not manufacture historical observations.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import statistics
import sys
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable


def bootstrap_repo() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        # Documentation subtrees can themselves contain a ``docs`` directory.
        # The root operating guide prevents them from being mistaken for the repository root.
        if (parent / "AGENTS.md").is_file() and (parent / "docs" / "topics").is_dir():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    raise RuntimeError("Repository root with docs/topics was not found.")


ROOT = bootstrap_repo()
TOPIC = ROOT / "docs" / "topics" / "0.25_Strategy_Power_Economics"
DATA = TOPIC / "Data"
RESEARCH_DATA = DATA / "03_Research"
RAW_ROOT = ROOT / "docs" / "data" / "external" / "economics" / "us_historical"
ARTIFACT_DIR = TOPIC / "Result" / "artifacts"
SOURCE_MANIFEST = RESEARCH_DATA / "uet_us_economics_source_manifest.json"
SOURCE_READINESS = RESEARCH_DATA / "uet_us_economics_source_readiness.json"
FORMULA_GATE = RESEARCH_DATA / "uet_us_economics_formula_gate.json"
PARAMETER_POLICY = RESEARCH_DATA / "uet_us_economics_parameter_policy.json"
HOLDOUT_POLICY = RESEARCH_DATA / "uet_us_economics_holdout_policy.json"
CLAIM_GATE = RESEARCH_DATA / "uet_economics_claim_gate.json"
PANEL_PATH = RESEARCH_DATA / "uet_us_macro_panel_1959_2024.csv"
PANEL_STATUS = RESEARCH_DATA / "uet_us_macro_panel_status.json"
RESEARCH_REGISTER = RESEARCH_DATA / "uet_economics_research_register.json"
VARIABLE_DICTIONARY = RESEARCH_DATA / "uet_economics_variable_dictionary.json"
CAUSAL_DAG = RESEARCH_DATA / "uet_economics_causal_dag.json"
CLAIM_MATRIX = RESEARCH_DATA / "uet_economics_claim_matrix.json"
WARN_GATE_REGISTRY = RESEARCH_DATA / "uet_economics_warn_gate_registry.json"
MEASUREMENT_ARTIFACT = ARTIFACT_DIR / "0_25_uet_measurement_validity_audit.json"
WELFARE_SOURCE_MANIFEST = RAW_ROOT.parent.parent / "welfare" / "uet_us_welfare_source_manifest.json"
WELFARE_ARTIFACT = ARTIFACT_DIR / "0_25_uet_welfare_audit.json"
MONEY_CREDIT_ARTIFACT = ARTIFACT_DIR / "0_25_money_credit_inflation_audit.json"
GLOBAL_REPLICATION_ARTIFACT = ARTIFACT_DIR / "0_25_global_replication_readiness.json"
GLOBAL_WDI_PANEL_ARTIFACT = ARTIFACT_DIR / "0_25_global_wdi_panel.json"
GLOBAL_WDI_LOO_ARTIFACT = ARTIFACT_DIR / "0_25_global_wdi_leave_one_out.json"
GLOBAL_WDI_PPP_ARTIFACT = ARTIFACT_DIR / "0_25_global_wdi_ppp_comparison.json"


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def runtime_environment() -> dict[str, str]:
    return {"python": platform.python_version(), "platform": platform.platform()}


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: Path, default: dict | None = None) -> dict:
    if not path.exists():
        return {} if default is None else default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: object) -> float | None:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def annualise_fred(path: Path, method: str = "mean") -> dict[int, float]:
    """Convert a FRED CSV to annual observations without filling missing values."""
    values: dict[int, list[float]] = {}
    for row in read_csv(path):
        date = row.get("observation_date", "")
        value_columns = [key for key in row if key != "observation_date"]
        if len(date) < 4 or not value_columns:
            continue
        value = as_float(row[value_columns[0]])
        if value is None:
            continue
        values.setdefault(int(date[:4]), []).append(value)
    if method == "end":
        return {year: observations[-1] for year, observations in values.items()}
    return {year: statistics.fmean(observations) for year, observations in values.items()}


def source_path(manifest: dict, source_id: str) -> Path | None:
    for item in manifest.get("sources", []):
        if item.get("source_id") == source_id and item.get("local_path"):
            candidate = ROOT / item["local_path"]
            if candidate.exists():
                return candidate
    return None


def log_change(current: float | None, previous: float | None) -> float | None:
    if current is None or previous is None or current <= 0 or previous <= 0:
        return None
    return math.log(current / previous)


def rebased_index(value: float, base: float) -> float:
    if value <= 0 or base <= 0:
        raise ValueError("Index inputs must be positive.")
    return 100.0 * value / base


def arithmetic_mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        raise ValueError("Cannot calculate the mean of no values.")
    return statistics.fmean(values)


def standardize(value: float, mean: float, standard_deviation: float) -> float:
    if standard_deviation <= 0:
        return 0.0
    return (value - mean) / standard_deviation


def rmse(actual: list[float], predicted: list[float]) -> float | None:
    if not actual or len(actual) != len(predicted):
        return None
    return math.sqrt(arithmetic_mean([(a - p) ** 2 for a, p in zip(actual, predicted)]))


def median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    """Gaussian elimination for small, predeclared regression designs."""
    n = len(vector)
    augmented = [row[:] + [vector[index]] for index, row in enumerate(matrix)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("Regression design is singular.")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [item / scale for item in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [item - factor * basis for item, basis in zip(augmented[row], augmented[column])]
    return [augmented[row][-1] for row in range(n)]


def ols(features: list[list[float]], targets: list[float]) -> dict:
    if not features or len(features) != len(targets):
        raise ValueError("OLS needs equally sized feature and target rows.")
    width = len(features[0])
    if len(features) <= width:
        raise ValueError("OLS needs more observations than coefficients.")
    if any(len(row) != width for row in features):
        raise ValueError("OLS feature width is inconsistent.")
    xtx = [[0.0] * width for _ in range(width)]
    xty = [0.0] * width
    for row, target in zip(features, targets):
        for i in range(width):
            xty[i] += row[i] * target
            for j in range(width):
                xtx[i][j] += row[i] * row[j]
    coefficients = solve_linear_system(xtx, xty)
    predictions = [sum(coefficient * value for coefficient, value in zip(coefficients, row)) for row in features]
    residuals = [target - prediction for target, prediction in zip(targets, predictions)]
    mean_target = arithmetic_mean(targets)
    total_sum_squares = sum((target - mean_target) ** 2 for target in targets)
    residual_sum_squares = sum(residual * residual for residual in residuals)
    return {
        "coefficients": coefficients,
        "predictions": predictions,
        "residuals": residuals,
        "n": len(targets),
        "r_squared": None if total_sum_squares == 0 else 1.0 - residual_sum_squares / total_sum_squares,
        "residual_rmse": math.sqrt(residual_sum_squares / max(1, len(targets) - width)),
    }


def moving_block_bootstrap_interval(deltas: list[float], block_size: int = 3, draws: int = 1000) -> dict:
    """Deterministic moving-block bootstrap for forecast-error deltas.

    A negative interval means the first model has lower squared error than the
    comparator.  This is a diagnostic interval, not causal inference.
    """
    if len(deltas) < block_size:
        return {"status": "INSUFFICIENT_ROWS", "draws": 0, "lower": None, "upper": None, "mean": None}
    samples: list[float] = []
    n = len(deltas)
    for draw in range(draws):
        picked: list[float] = []
        cursor = (draw * 7 + 3) % n
        while len(picked) < n:
            for offset in range(block_size):
                picked.append(deltas[(cursor + offset) % n])
                if len(picked) == n:
                    break
            cursor = (cursor + block_size + 5) % n
        samples.append(arithmetic_mean(picked))
    samples.sort()
    lower = samples[max(0, int(0.025 * len(samples)) - 1)]
    upper = samples[min(len(samples) - 1, int(0.975 * len(samples)))]
    return {"status": "OK", "draws": draws, "block_size": block_size, "lower": lower, "upper": upper, "mean": arithmetic_mean(deltas)}


def source_file_metadata(path: Path) -> dict:
    return {
        "local_path": relative(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }


def download(url: str, destination: Path, timeout_seconds: int = 45) -> tuple[bool, str | None]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "UET-Topic-0.25-Research/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            destination.write_bytes(response.read())
        return True, None
    except Exception as error:  # noqa: BLE001 - the artifact needs the real download reason.
        return False, f"{type(error).__name__}: {error}"
