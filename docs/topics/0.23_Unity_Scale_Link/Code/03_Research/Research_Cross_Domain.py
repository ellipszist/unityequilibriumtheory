"""
Research: Cross-Domain Structural Scale-Link Check
==================================================
Topic: 0.23_Unity_Scale_Link
Folder: 03_Research

This verifier tests whether the same implemented Omega form can run across
normalized domain examples while keeping synthetic and source-backed evidence
separate.

Tests:
1. Galaxy-style kappa on synthetic neural fields
2. Local finance volatility versus synthetic neural interpretation
3. Fixed-parameter diagnostic with kappa=0.1
"""

import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import stats


def _bootstrap():
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

ROOT = ROOT_PATH
TOPIC_DIR = ROOT / "docs" / "topics" / "0.23_Unity_Scale_Link"
DATA_DIR = TOPIC_DIR / "data" / "03_Research"
if not DATA_DIR.exists():
    DATA_DIR = TOPIC_DIR / "Data" / "03_Research"

engine_file = TOPIC_DIR / "Code" / "01_Engine" / "Engine_Unity_Scale.py"
try:
    spec = importlib.util.spec_from_file_location("Engine_Unity_Scale", engine_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    UETUnityScaleEngine = getattr(module, "UETUnityScaleEngine")
except Exception as exc:
    print(f"Error loading Engine 0.23 Research: {exc}")
    sys.exit(1)

engine = UETUnityScaleEngine()

ARTIFACT_PATH = TOPIC_DIR / "Result" / "artifacts" / "0_23_unity_scale_link_verification.json"
DEPENDENCY_MANIFEST_PATH = DATA_DIR / "scale_dependency_manifest.json"
DATA_INPUTS = [
    DATA_DIR / "create_unified_data.py",
    DATA_DIR / "source_lock_manifest.json",
    DATA_DIR / "scale_dependency_manifest.json",
    DATA_DIR / "economy" / "Bitcoin_yahoo_real.csv",
    DATA_DIR / "economy" / "DowJones_yahoo_real.csv",
    DATA_DIR / "economy" / "EUR_USD_yahoo_real.csv",
    DATA_DIR / "economy" / "SP500_yahoo_real.csv",
    ROOT
    / "docs"
    / "data"
    / "external"
    / "finance"
    / "yahoo_snapshots"
    / "0_23_unity_scale_link"
    / "source_manifest.json",
    ROOT
    / "docs"
    / "topics"
    / "0.13_Thermodynamic_Bridge"
    / "Result"
    / "artifacts"
    / "0_13_thermodynamic_bridge_verification.json",
    ROOT
    / "docs"
    / "topics"
    / "0.5_Nuclear_Binding_Hadrons"
    / "Result"
    / "artifacts"
    / "0_5_nuclear_binding_hadrons_verification.json",
    ROOT
    / "docs"
    / "topics"
    / "0.6_Electroweak_Physics"
    / "Result"
    / "artifacts"
    / "0_6_electroweak_physics_verification.json",
    ROOT
    / "docs"
    / "topics"
    / "0.7_Neutrino_Physics"
    / "Result"
    / "artifacts"
    / "nufit_6_0_validation.json",
]
TEST_METRICS = {}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _input_identity():
    items = []
    for path in DATA_INPUTS:
        try:
            rel = path.relative_to(ROOT).as_posix()
        except ValueError:
            rel = str(path)
        if path.exists():
            items.append(
                {
                    "path": rel,
                    "sha256": _sha256(path),
                    "size_bytes": path.stat().st_size,
                }
            )
        else:
            items.append({"path": rel, "missing": True})
    return items


def _load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _build_scale_claim_gate(results, dependency_manifest, missing_inputs):
    dependency_chain = []
    if dependency_manifest:
        dependency_chain = dependency_manifest.get("dependency_chain", [])

    return {
        "schema_version": "1.0",
        "purpose": "Prevent scale-link and unity wording from outrunning source and dependency evidence.",
        "dependency_topics": [
            {
                "topic": item.get("topic"),
                "artifact": item.get("artifact"),
                "role": item.get("role"),
                "claim_class_ceiling": item.get("claim_class_ceiling"),
                "status_inheritance": item.get("status_inheritance"),
            }
            for item in dependency_chain
        ],
        "source_retrieval_log_status": {
            "finance_yahoo_snapshots": "source_manifest_present_but_original_query_logs_missing",
            "real_eeg_branch": "not_present",
            "synthetic_neural_branch": "simulation_only",
        },
        "fixed_parameter_falsification": {
            "status": "CONSTRAINT",
            "test_key": "universal_kappa",
            "current_result": results.get("universal_kappa"),
            "interpretation": (
                "A failed or unstable fixed-kappa branch is a useful blocker. It constrains the theory "
                "against universal fixed-parameter wording instead of counting as evidence for unity."
            ),
        },
        "branch_claim_policy": {
            "shared_omega_form": "model-shape diagnostic",
            "fixed_parameter_unity": "blocked unless held-out source-backed domains pass with one parameter contract",
            "scale_dependent_kappa": "hypothesis until upstream topic artifacts and uncertainties are mapped",
            "cross_domain_transfer": "simulation-only where synthetic neural or generated galaxy fields are used",
        },
        "paper_readiness": {
            "status": "BLOCKED",
            "blocking_conditions": [
                "missing declared inputs" if missing_inputs else "no missing declared inputs",
                "finance retrieval logs are absent",
                "real EEG source package is absent",
                "0.13 thermodynamic bridge remains a WARN dependency",
            ],
        },
    }


def _write_verification_artifact(results):
    passed = sum(1 for value in results.values() if value is True)
    input_identity = _input_identity()
    missing_inputs = [item["path"] for item in input_identity if item.get("missing")]
    dependency_manifest = _load_json(DEPENDENCY_MANIFEST_PATH)

    warnings = [
        "Finance snapshots now have local source metadata and hashes, but original Yahoo query logs/retrieval timestamps remain unavailable.",
        "Neural and galaxy fields are synthetic generator outputs, so cross-domain success is a model-shape result, not external replication.",
        "This topic depends on 0.13 Landauer/thermodynamic bridge limits and inherits its WARN/raw-table limitations.",
    ]
    if missing_inputs:
        warnings.append(f"Missing declared inputs: {missing_inputs}")
    if TEST_METRICS.get("galaxy_neural", {}).get("omega_seizure_std", 1.0) < 1e-12:
        warnings.append(
            "Synthetic seizure generator has near-zero variance; t-test significance is diagnostic only."
        )
    if TEST_METRICS.get("economy_neural", {}).get("same_ordering_as_synthetic_neural") is False:
        warnings.append(
            "Economy volatility ordering does not match the synthetic neural diagnostic under the fixed kappa benchmark."
        )
    scale_claim_gate = _build_scale_claim_gate(results, dependency_manifest, missing_inputs)

    status = "WARN" if passed > 0 and not missing_inputs else "FAIL"
    artifact = {
        "schema_version": "1.3",
        "topic": "0.23_Unity_Scale_Link",
        "command": ".venv\\Scripts\\python.exe docs\\topics\\0.23_Unity_Scale_Link\\Code\\03_Research\\Research_Cross_Domain.py",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "claim_class": "D",
        "inputs": input_identity,
        "metrics": TEST_METRICS,
        "thresholds": {
            "minimum_true_tests_for_nonfail": 1,
            "galaxy_neural_p_value_max": 0.001,
            "requires_external_source_lock_for_claim_class_above_C": True,
        },
        "test_results": {key: ("SKIP" if value is None else bool(value)) for key, value in results.items()},
        "dependency_manifest": dependency_manifest,
        "scale_claim_gate": scale_claim_gate,
        "evidence_lanes": {
            "source_backed_finance_snapshot": {
                "status": "WARN",
                "claim_class": "C - local source-referenced benchmark",
                "blocker": "Original Yahoo query logs and retrieval timestamps are not archived.",
            },
            "synthetic_neural_transfer": {
                "status": "SIMULATION_ONLY",
                "claim_class": "A/B - model-shape diagnostic",
                "blocker": "Replace or supplement with real EEG source package before external cross-domain claims.",
            },
            "fixed_universal_kappa": {
                "status": "CONSTRAINT",
                "claim_class": "negative/limiting evidence",
                "blocker": "One fixed parameter cannot be promoted as universal without held-out, source-backed domain passes.",
            },
        },
        "warnings": warnings,
        "interpretation": (
            "The run supports an exploratory structural scale-link check. It does not establish "
            "parameter unity, external prediction, or a proof of grand unification."
        ),
    }
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"\n[Artifact] Verification artifact written: {ARTIFACT_PATH}")
    print(f"[Artifact] Status: {status}")
    return artifact


def load_economy_data():
    """Load the local S&P 500 snapshot for volatility diagnostics."""
    sp500_path = DATA_DIR / "economy" / "SP500_yahoo_real.csv"

    if not sp500_path.exists():
        print(f"  Warning: SP500 data not found: {sp500_path}")
        return None

    data = []
    with sp500_path.open("r", encoding="utf-8") as handle:
        lines = handle.readlines()
        header = lines[0].strip().split(",")

        close_idx = None
        for idx, column in enumerate(header):
            if "Close" in column or "Adj Close" in column:
                close_idx = idx
                break

        if close_idx is None:
            close_idx = 4

        for line in lines[1:]:
            parts = line.strip().split(",")
            try:
                if len(parts) > close_idx:
                    value = float(parts[close_idx])
                    if value > 0:
                        data.append(value)
            except ValueError:
                continue

    return np.array(data) if data else None


def generate_synthetic_galaxy_field(n: int = 100) -> np.ndarray:
    return engine.generate_field("galactic", n=n)


def generate_neural_field(state: str = "normal", n: int = 256) -> np.ndarray:
    return engine.generate_field("neural", state_regime=state, n=n)


def compute_omega(field: np.ndarray, kappa: float = 0.1, beta: float = 0.05) -> float:
    return engine.compute_omega(field, kappa=kappa, beta=beta)


def test_galaxy_neural_transfer():
    print("\n[TEST 1] GALAXY-STYLE KAPPA ON SYNTHETIC NEURAL FIELDS")
    print("-" * 50)
    print("  NOTE: We use kappa=0.1 as a structural diagnostic parameter.")
    print("  Interpretation: generated field diagnostic only.")
    print("-" * 50)

    kappa_galaxy = 0.1
    beta_galaxy = 0.05
    print(f"  Using kappa={kappa_galaxy}, beta={beta_galaxy}")

    n_trials = 20
    omega_normal = []
    omega_seizure = []

    for _ in range(n_trials):
        omega_normal.append(compute_omega(generate_neural_field("normal"), kappa_galaxy, beta_galaxy))
        omega_seizure.append(compute_omega(generate_neural_field("seizure"), kappa_galaxy, beta_galaxy))

    omega_normal = np.array(omega_normal)
    omega_seizure = np.array(omega_seizure)
    t_stat, p_value = stats.ttest_ind(omega_normal, omega_seizure)

    print(f"\n  Omega(normal) = {np.mean(omega_normal):.3f} +/- {np.std(omega_normal):.3f}")
    print(f"  Omega(seizure) = {np.mean(omega_seizure):.3f} +/- {np.std(omega_seizure):.3f}")
    print(f"\n  t-statistic = {t_stat:.2f}")
    print(f"  p-value = {p_value:.2e}")

    TEST_METRICS["galaxy_neural"] = {
        "omega_normal_mean": float(np.mean(omega_normal)),
        "omega_normal_std": float(np.std(omega_normal)),
        "omega_seizure_mean": float(np.mean(omega_seizure)),
        "omega_seizure_std": float(np.std(omega_seizure)),
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "n_trials": n_trials,
        "kappa": kappa_galaxy,
        "beta": beta_galaxy,
        "data_role": "synthetic neural fields from engine generator",
    }

    passed = p_value < 0.001 and np.mean(omega_seizure) < np.mean(omega_normal)
    if passed:
        print("\n  PASS: synthetic seizure field has lower Omega than synthetic normal field")
    else:
        print("\n  FAIL: synthetic fields did not separate under this diagnostic")
    return passed


def test_economy_neural_correlation():
    print("\n[TEST 2] ECONOMY TO NEURAL ORDERING CHECK")
    print("-" * 50)

    kappa = 0.1
    beta = 0.05
    sp500 = load_economy_data()

    if sp500 is None or len(sp500) < 100:
        print("  Warning: skipping because SP500 data is unavailable")
        return None

    print(f"  Loaded {len(sp500)} SP500 data points")

    returns = np.diff(np.log(sp500))
    vol_window = 20
    rolling_vol = np.array([np.std(returns[idx : idx + vol_window]) for idx in range(len(returns) - vol_window)])

    vol_median = np.median(rolling_vol)
    high_vol_idx = np.where(rolling_vol > vol_median * 1.5)[0]
    low_vol_idx = np.where(rolling_vol < vol_median * 0.5)[0]

    omega_high = []
    omega_low = []
    window = 50

    for idx in high_vol_idx[:50]:
        if idx + window < len(sp500):
            omega_high.append(compute_omega(sp500[idx : idx + window], kappa, beta))

    for idx in low_vol_idx[:50]:
        if idx + window < len(sp500):
            omega_low.append(compute_omega(sp500[idx : idx + window], kappa, beta))

    if not omega_high or not omega_low:
        print("  Warning: not enough data for analysis")
        return None

    omega_high = np.array(omega_high)
    omega_low = np.array(omega_low)
    diff = float(np.mean(omega_high) - np.mean(omega_low))
    same_ordering_as_neural = diff < 0

    print(f"\n  Omega(high volatility) = {np.mean(omega_high):.3f} +/- {np.std(omega_high):.3f}")
    print(f"  Omega(low volatility) = {np.mean(omega_low):.3f} +/- {np.std(omega_low):.3f}")

    TEST_METRICS["economy_neural"] = {
        "sp500_points": int(len(sp500)),
        "omega_high_vol_mean": float(np.mean(omega_high)),
        "omega_high_vol_std": float(np.std(omega_high)),
        "omega_low_vol_mean": float(np.mean(omega_low)),
        "omega_low_vol_std": float(np.std(omega_low)),
        "high_vol_samples": int(len(omega_high)),
        "low_vol_samples": int(len(omega_low)),
        "kappa": kappa,
        "beta": beta,
        "omega_difference_high_minus_low": diff,
        "same_ordering_as_synthetic_neural": bool(same_ordering_as_neural),
        "data_role": "local SP500 snapshot compared to synthetic neural interpretation",
    }

    if same_ordering_as_neural:
        print("\n  Economy ordering matches the synthetic neural diagnostic.")
    else:
        print("\n  Economy ordering does NOT match the synthetic neural diagnostic.")
        print("  Neural diagnostic expects seizure-like disequilibrium to lower Omega.")
        print("  The current local finance snapshot shows the opposite direction.")

    return same_ordering_as_neural


def test_fixed_parameter_diagnostic():
    print("\n[TEST 3] FIXED KAPPA DIAGNOSTIC ACROSS SELECTED EXAMPLES")
    print("-" * 50)

    kappa_unity = 0.1
    beta_unity = 0.05
    print(f"  Using only kappa={kappa_unity}, beta={beta_unity}")

    results = {}
    results["galaxy"] = compute_omega(generate_synthetic_galaxy_field(), kappa_unity, beta_unity)
    omega_neural_normal = compute_omega(generate_neural_field("normal"), kappa_unity, beta_unity)
    omega_neural_seizure = compute_omega(generate_neural_field("seizure"), kappa_unity, beta_unity)
    results["neural_normal"] = omega_neural_normal
    results["neural_seizure"] = omega_neural_seizure

    sp500 = load_economy_data()
    if sp500 is not None and len(sp500) >= 100:
        results["economy"] = compute_omega(sp500[:100], kappa_unity, beta_unity)

    print("\n  Omega values (all with kappa=0.1):")
    print("  " + "-" * 30)
    for domain, omega in results.items():
        print(f"  {domain:15s}: Omega = {omega:.4f}")

    passed_neural_ordering = omega_neural_seizure < omega_neural_normal
    if passed_neural_ordering:
        print("\n  Synthetic neural ordering: seizure < normal")
    else:
        print("\n  Synthetic neural ordering did not match the diagnostic expectation")

    TEST_METRICS["universal_kappa"] = {
        "kappa": kappa_unity,
        "beta": beta_unity,
        "omega_values": {key: float(value) for key, value in results.items()},
        "passed_neural_ordering": bool(passed_neural_ordering),
    }
    return passed_neural_ordering


def run_cross_domain_research():
    print("=" * 70)
    print("RESEARCH: Cross-Domain Structural Scale-Link Check")
    print("    Exploratory verifier with explicit source-lock limitations")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("PREMISE: the same Omega implementation should be auditable across")
    print("selected normalized examples without promoting parameter unity.")
    print("=" * 70)

    np.random.seed(23023)
    results = {
        "galaxy_neural": test_galaxy_neural_transfer(),
        "economy_neural": test_economy_neural_correlation(),
        "universal_kappa": test_fixed_parameter_diagnostic(),
    }

    print("\n" + "=" * 70)
    print("RESEARCH SUMMARY")
    print("=" * 70)

    passed = sum(1 for value in results.values() if value is True)
    total = sum(1 for value in results.values() if value is not None)
    print(f"\n  Tests passed: {passed}/{total}")

    if passed == total:
        print("\n  ALL EXPLORATORY CHECKS RAN")
        print("     Current evidence supports a structural scale-link hypothesis.")
    elif passed > 0:
        print("\n  PARTIAL SUCCESS")
        print("     Some structural diagnostics matched their expected ordering.")
    else:
        print("\n  TESTS FAILED")
        print("     Structural diagnostics need model/data hardening.")

    economy_alignment = TEST_METRICS.get("economy_neural", {}).get("same_ordering_as_synthetic_neural")
    if economy_alignment is True:
        economy_line = "- local finance ordering matches the synthetic neural diagnostic"
    elif economy_alignment is False:
        economy_line = "- local finance ordering does not match the synthetic neural diagnostic"
    else:
        economy_line = "- local finance ordering was unavailable"

    print(
        f"""
    KEY DIAGNOSTIC:

    Fixed kappa=0.1 currently produces:
    - synthetic neural ordering consistent with the topic diagnostic
    {economy_line}

    This remains exploratory structural evidence only. Parameter unity and
    external prediction remain open.
    """
    )

    print("=" * 70)
    print("RESEARCH RESULT: ARTIFACT WRITTEN")
    print("=" * 70)

    artifact = _write_verification_artifact(results)
    return artifact["status"] != "FAIL"


if __name__ == "__main__":
    success = run_cross_domain_research()
    sys.exit(0 if success else 1)
