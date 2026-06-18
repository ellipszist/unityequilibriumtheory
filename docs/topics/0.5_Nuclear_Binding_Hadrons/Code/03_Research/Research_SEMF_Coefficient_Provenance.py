"""
SEMF coefficient provenance diagnostic for topic 0.5.

This script extracts the SEMF and Yukawa constants from the current engine,
checks that the machine-readable SEMF gate matches the code surface, and writes
a local coefficient package. It does not source-lock the coefficients.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any


def _bootstrap() -> Path | None:
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return None


ROOT = _bootstrap()
if not ROOT:
    print("CRITICAL: UET docs root not found!")
    sys.exit(1)


from docs import ROOT_PATH
from docs.core.reproducibility import generate_artifact, hash_dataset, hash_file, save_artifact


root_path = ROOT_PATH
topic_dir = root_path / "docs" / "topics" / "0.5_Nuclear_Binding_Hadrons"
data_dir = topic_dir / "Data" / "03_Research"
artifact_dir = topic_dir / "Result" / "artifacts"
engine_path = topic_dir / "Code" / "01_Engine" / "Engine_Nuclear_Binding.py"
gate_path = data_dir / "semf_coefficient_provenance_gate.json"
package_path = data_dir / "semf_coefficient_local_package.json"
artifact_path = artifact_dir / "semf_coefficient_provenance_diagnostic.json"

SEMF_SYMBOLS = {
    "a_vol": ("volume", "MeV"),
    "a_surf": ("surface", "MeV"),
    "a_coul": ("coulomb", "MeV"),
    "a_asym": ("asymmetry", "MeV"),
    "a_pair": ("pairing", "MeV"),
}

CORRECTION_SYMBOLS = {
    "m_pion": ("pion mass convention", "MeV"),
    "hbar_c": ("conversion constant", "MeV fm"),
    "r0": ("nuclear radius scale", "fm"),
    "yukawa_prefactor": ("Yukawa additive prefactor", "MeV-like scale before per-nucleus multiplication"),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def numeric_constant(node: ast.AST) -> float | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        inner = numeric_constant(node.operand)
        return -inner if inner is not None else None
    return None


def extract_engine_constants(path: Path) -> dict[str, float]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    constants: dict[str, float] = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        value = numeric_constant(node.value)
        for target in node.targets:
            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self":
                if target.attr in SEMF_SYMBOLS or target.attr in ("m_pion", "hbar_c"):
                    if value is not None:
                        constants[target.attr] = value
            elif isinstance(target, ast.Name) and target.id == "r0":
                if value is not None:
                    constants["r0"] = value
            elif isinstance(target, ast.Name) and target.id == "correction":
                if isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.Mult):
                    left = numeric_constant(node.value.left)
                    right = numeric_constant(node.value.right)
                    if left is not None:
                        constants["yukawa_prefactor"] = left
                    elif right is not None:
                        constants["yukawa_prefactor"] = right

    return constants


def gate_records_by_symbol(gate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for key in ("coefficients", "correction_terms"):
        for record in gate.get(key, []):
            symbol = record.get("symbol")
            if symbol:
                records[symbol] = record
    return records


def compare_to_gate(constants: dict[str, float], gate: dict[str, Any]) -> list[dict[str, Any]]:
    gate_records = gate_records_by_symbol(gate)
    comparisons: list[dict[str, Any]] = []
    for symbol in list(SEMF_SYMBOLS) + list(CORRECTION_SYMBOLS):
        if symbol == "beta_nuc":
            continue
        gate_record = gate_records.get(symbol, {})
        gate_value = gate_record.get("value", gate_record.get("current_gate_value"))
        engine_value = constants.get(symbol)
        matches = (
            isinstance(gate_value, (int, float))
            and engine_value is not None
            and abs(float(gate_value) - float(engine_value)) <= 1e-12
        )
        comparisons.append(
            {
                "symbol": symbol,
                "engine_value": engine_value,
                "gate_value": gate_value,
                "matches_gate": matches,
                "gate_source_status": gate_record.get("source_status"),
            }
        )
    return comparisons


def build_local_package(constants: dict[str, float], gate: dict[str, Any], comparisons: list[dict[str, Any]]) -> dict[str, Any]:
    coefficients = []
    for symbol, (term, unit) in SEMF_SYMBOLS.items():
        coefficients.append(
            {
                "symbol": symbol,
                "term": term,
                "value": constants.get(symbol),
                "unit": unit,
                "source_status": "LOCAL_ENGINE_EXTRACTED_NOT_SOURCE_LOCKED",
                "source_note": "Extracted from Engine_Nuclear_Binding.py; no topic-local source record pins the exact coefficient set or edition.",
            }
        )

    corrections = []
    for symbol, (term, unit) in CORRECTION_SYMBOLS.items():
        status = "LOCAL_ENGINE_EXTRACTED_NOT_SOURCE_LOCKED"
        if symbol == "yukawa_prefactor":
            status = "LOCAL_ENGINE_EXTRACTED_HEURISTIC_BRIDGE"
        corrections.append(
            {
                "symbol": symbol,
                "term": term,
                "value": constants.get(symbol),
                "unit": unit,
                "source_status": status,
                "source_note": "Extracted from Engine_Nuclear_Binding.py; source record and uncertainty policy remain unresolved.",
            }
        )

    matches = [row["matches_gate"] for row in comparisons]
    return {
        "schema_version": "1.0",
        "topic": "0.5_Nuclear_Binding_Hadrons",
        "package_status": "LOCAL_PACKAGE_READY_SOURCE_GAP_BLOCKED",
        "purpose": "Local package of the exact SEMF and Yukawa constants currently used by Engine_Nuclear_Binding.py.",
        "code_surface": "Code/01_Engine/Engine_Nuclear_Binding.py",
        "code_surface_sha256": hash_file(engine_path),
        "gate_surface": "Data/03_Research/semf_coefficient_provenance_gate.json",
        "gate_surface_sha256": hash_file(gate_path),
        "summary": {
            "engine_constants_extracted": len(constants),
            "semf_coefficients_extracted": sum(1 for symbol in SEMF_SYMBOLS if constants.get(symbol) is not None),
            "correction_constants_extracted": sum(1 for symbol in CORRECTION_SYMBOLS if constants.get(symbol) is not None),
            "gate_comparison_count": len(comparisons),
            "gate_match_count": sum(1 for matched in matches if matched),
            "gate_mismatch_count": sum(1 for matched in matches if not matched),
            "source_record_locked": False,
        },
        "semf_coefficients": coefficients,
        "correction_terms": corrections,
        "gate_comparisons": comparisons,
        "claim_boundary": gate["claim_boundary"],
        "required_to_close": gate["required_to_close"],
        "blocked_usage": gate["blocked_usage"],
    }


def run_diagnostic() -> bool:
    print("=" * 76)
    print("SEMF COEFFICIENT PROVENANCE DIAGNOSTIC")
    print("Topic: 0.5_Nuclear_Binding_Hadrons")
    print("=" * 76)

    gate = load_json(gate_path)
    constants = extract_engine_constants(engine_path)
    comparisons = compare_to_gate(constants, gate)
    package = build_local_package(constants, gate, comparisons)
    write_json(package_path, package)

    mismatch_count = package["summary"]["gate_mismatch_count"]
    extracted_count = package["summary"]["engine_constants_extracted"]
    print(f"Engine constants extracted: {extracted_count}")
    print(f"Gate comparison count:      {package['summary']['gate_comparison_count']}")
    print(f"Gate mismatches:            {mismatch_count}")
    print(f"Package saved to:           {package_path}")

    artifact = generate_artifact(
        topic="0.5_Nuclear_Binding_Hadrons",
        dataset_hash=hash_dataset(
            {
                "engine_path": str(engine_path.relative_to(root_path)),
                "engine_sha256": hash_file(engine_path),
                "gate_path": str(gate_path.relative_to(root_path)),
                "gate_sha256": hash_file(gate_path),
                "package_path": str(package_path.relative_to(root_path)),
            }
        ),
        results={
            "status": "LOCAL_PACKAGE_READY_SOURCE_GAP_BLOCKED",
            "summary": package["summary"],
            "package_path": str(package_path.relative_to(topic_dir)).replace("\\", "/"),
            "package_sha256": hash_file(package_path),
            "gate_comparisons": comparisons,
            "claim_boundary": (
                "The current engine constants are locally packaged and matched against the SEMF gate, "
                "but the coefficient set is not source-locked. Parameter-free and first-principles "
                "nuclear-binding claims remain blocked."
            ),
            "blocked_exports": gate["blocked_usage"],
        },
        config={
            "engine": str(engine_path.relative_to(topic_dir)).replace("\\", "/"),
            "gate": str(gate_path.relative_to(topic_dir)).replace("\\", "/"),
            "method": "Python AST extraction of numeric constants from Engine_Nuclear_Binding.py.",
        },
        metrics=package["summary"],
        thresholds={
            "required_gate_mismatch_count": 0,
            "required_source_record_locked": True,
        },
        notes=(
            "This diagnostic narrows the SEMF blocker to an explicit source-record gap. "
            "It is not an external-source package and does not validate the SEMF coefficient values."
        ),
    )
    save_artifact(artifact, artifact_path)
    print(f"Artifact saved to:          {artifact_path}")
    return mismatch_count == 0 and extracted_count >= len(SEMF_SYMBOLS) + len(CORRECTION_SYMBOLS)


if __name__ == "__main__":
    sys.exit(0 if run_diagnostic() else 1)
