"""
Diagnostic hadron-model check against the generated PDG source package.

This script is deliberately not a pass/fail validation gate. It verifies that
the hadron-model formula path can be driven by the source-linked PDG package
instead of embedded benchmark masses, then records the resulting residuals.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path


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
engine_dir = topic_dir / "Code" / "01_Engine"
if str(engine_dir) not in sys.path:
    sys.path.insert(0, str(engine_dir))

from Engine_Hadron_Model import (
    baryon_mass_uet,
    constituent_masses_from_current,
    extract_source_package_masses,
    load_pdg_reference_package,
    meson_mass_uet,
    pion_mass_gmor,
)


REFERENCE_PACKAGE_PATH = data_dir / "pdg_hadron_quark_reference_package.json"
ARTIFACT_PATH = artifact_dir / "hadron_model_source_package_diagnostic.json"

BARYON_COMPOSITIONS = {
    "proton": ("u", "u", "d"),
    "neutron": ("u", "d", "d"),
    "Lambda": ("u", "d", "s"),
    "Omega": ("s", "s", "s"),
}

MESON_COMPOSITIONS = {
    "omega": ("u", "d"),
    "phi": ("s", "s"),
}


def relative_error_percent(predicted: float, observed: float) -> float:
    return abs(predicted - observed) / observed * 100.0 if observed else 0.0


def summarize(errors: list[float]) -> dict:
    if not errors:
        return {
            "count": 0,
            "mean_error_percent": None,
            "median_error_percent": None,
            "max_error_percent": None,
        }
    return {
        "count": len(errors),
        "mean_error_percent": statistics.fmean(errors),
        "median_error_percent": statistics.median(errors),
        "max_error_percent": max(errors),
    }


def run_diagnostic() -> bool:
    print("=" * 76)
    print("UET HADRON MODEL SOURCE-PACKAGE DIAGNOSTIC")
    print("Data: generated PDG 2025 hadron/quark reference package")
    print("=" * 76)

    package = load_pdg_reference_package(REFERENCE_PACKAGE_PATH)
    quark_masses, hadron_masses = extract_source_package_masses(package)
    constituent_masses = constituent_masses_from_current(quark_masses)

    comparisons: list[dict] = []

    if "pion_pm" in hadron_masses:
        predicted = pion_mass_gmor(quark_masses)
        observed = hadron_masses["pion_pm"]
        comparisons.append(
            {
                "engine_label": "pion_pm",
                "formula_path": "GMOR",
                "observed_mass_mev": observed,
                "predicted_mass_mev": predicted,
                "relative_error_percent": relative_error_percent(predicted, observed),
                "source_package_backed": True,
            }
        )

    for label, quarks in MESON_COMPOSITIONS.items():
        if label not in hadron_masses:
            continue
        predicted = meson_mass_uet(quarks[0], quarks[1], constituent_masses=constituent_masses)
        observed = hadron_masses[label]
        comparisons.append(
            {
                "engine_label": label,
                "formula_path": "constituent_meson",
                "quark_content": list(quarks),
                "observed_mass_mev": observed,
                "predicted_mass_mev": predicted,
                "relative_error_percent": relative_error_percent(predicted, observed),
                "source_package_backed": True,
            }
        )

    for label, quarks in BARYON_COMPOSITIONS.items():
        if label not in hadron_masses:
            continue
        predicted = baryon_mass_uet(
            quarks[0],
            quarks[1],
            quarks[2],
            constituent_masses=constituent_masses,
        )
        observed = hadron_masses[label]
        comparisons.append(
            {
                "engine_label": label,
                "formula_path": "constituent_baryon",
                "quark_content": list(quarks),
                "observed_mass_mev": observed,
                "predicted_mass_mev": predicted,
                "relative_error_percent": relative_error_percent(predicted, observed),
                "source_package_backed": True,
            }
        )

    compared_labels = {row["engine_label"] for row in comparisons}
    source_labels = {record["engine_label"] for record in package["hadron_mass_records"]}
    unsupported_labels = sorted(source_labels - compared_labels)
    errors = [row["relative_error_percent"] for row in comparisons]
    summary = summarize(errors)
    summary.update(
        {
            "source_package_status": package["status"],
            "source_package_records_total": package["summary"]["records_total"],
            "source_package_records_found": package["summary"]["records_found"],
            "source_package_unit_mismatch_count": package["summary"]["unit_mismatch_count"],
            "compared_hadron_count": len(comparisons),
            "unsupported_source_labels": unsupported_labels,
            "model_status": "DIAGNOSTIC_ONLY",
        }
    )

    print(f"Source records found: {summary['source_package_records_found']}/{summary['source_package_records_total']}")
    print(f"Compared hadrons:     {summary['compared_hadron_count']}")
    print(f"Mean error:           {summary['mean_error_percent']:.2f}%")
    print(f"Max error:            {summary['max_error_percent']:.2f}%")
    if unsupported_labels:
        print(f"Unsupported labels:   {', '.join(unsupported_labels)}")

    artifact = generate_artifact(
        topic="0.5_Nuclear_Binding_Hadrons",
        dataset_hash=hash_dataset(
            {
                "reference_package": str(REFERENCE_PACKAGE_PATH.relative_to(root_path)),
                "reference_package_sha256": hash_file(REFERENCE_PACKAGE_PATH),
                "compared_labels": sorted(compared_labels),
            }
        ),
        results={
            "status": "DIAGNOSTIC_MODEL_SOURCE_PACKAGE",
            "summary": summary,
            "comparisons": comparisons,
            "claim_boundary": (
                "This artifact confirms that the diagnostic hadron-model comparison reads "
                "the generated PDG source package. It does not validate QCD running, "
                "confinement, or a first-principles hadron-mass derivation."
            ),
            "blocked_exports": [
                "hadron-mass validation claim",
                "QCD-running validation claim",
                "confinement proof claim",
            ],
        },
        config={
            "reference_package": str(REFERENCE_PACKAGE_PATH.relative_to(root_path)),
            "engine": "Code/01_Engine/Engine_Hadron_Model.py",
            "note": "Only formula paths with explicit current engine support are compared.",
        },
        metrics=summary,
        thresholds={
            "source_records_required_found": package["summary"]["records_total"],
            "allowed_unit_mismatches": 0,
            "validation_threshold_percent": None,
        },
        notes=(
            "Use this artifact as a source-package integration diagnostic only. "
            "The residuals are not configured as a pass/fail hadron-mass benchmark."
        ),
    )
    save_artifact(artifact, ARTIFACT_PATH)
    print(f"Artifact saved to {ARTIFACT_PATH}")
    return package["summary"]["records_missing"] == 0 and package["summary"]["unit_mismatch_count"] == 0


if __name__ == "__main__":
    sys.exit(0 if run_diagnostic() else 1)
