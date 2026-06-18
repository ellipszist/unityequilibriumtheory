# Baseline Comparison

## Baseline target

- AME2020, PDG-derived topic files, proton-radius references, and topic-local competitor scripts.

## Current comparator package

- Comparator or reference scripts should be taken from topic-local Code/04_Competitor/ when present.
- If no dedicated competitor script exists, the baseline is the cited source dataset or reference model listed in DATA_MANIFEST.md.

## Comparison metrics

- strict-subset binding-energy residuals
- SEMF-only versus SEMF-plus-correction residuals for the strict subset
- table-wide AME2020 diagnostic residuals
- selected radius residuals
- mismatch against competitor baselines

## Acceptance boundary

- This file does not certify a final pass/fail result.
- Until the benchmark is rerun with a saved artifact, comparison language must remain internal benchmark comparison.
- The strict selected-subset artifact and the table-wide diagnostic artifact should be described separately.
- A future hardening pass must record the exact numeric threshold, generated artifact, timestamp, environment, and dataset hash.
- The 2026-06-17 strict artifact exposes SEMF decomposition metrics. In the heavy selected subset, SEMF-only mean error is about `0.86%`, while the total path after current correction terms is about `1.68%`.
- `Data/03_Research/semf_coefficient_provenance_gate.json`,
  `Data/03_Research/semf_coefficient_local_package.json`, and
  `Result/artifacts/semf_coefficient_provenance_diagnostic.json` now record the exact
  current engine constants with 0 gate mismatches. `Data/03_Research/semf_coefficient_source_candidates.json`
  and `Result/artifacts/semf_coefficient_source_candidate_audit.json` record one exact
  external source-candidate match, but still block parameter-free claims until a direct
  SEMF source record and Yukawa-term policy are source-locked.
- `Data/03_Research/pdg_hadron_qcd_source_mapping_gate.json` and `Data/03_Research/pdg_hadron_quark_reference_package.json` now source-link selected PDG 2025 quark/hadron mass records.
- `Result/artifacts/hadron_model_source_package_diagnostic.json` reads that package for 7 supported hadron labels, but records about `75.33%` mean error and `94.91%` max error, so hadron/QCD comparison remains diagnostic-blocked.
- `Result/artifacts/qcd_alpha_s_source_probe.json` smoke-tests `alpha_s_uet_v2` after the data-shape fix, but records `0` direct local PDG alpha_s/QCD-running source rows under the current query policy.
- `Result/artifacts/confinement_proof_gate_diagnostic.json` verifies that the proof script now has a real return contract, but the current narrow proton-mass consistency check fails and remains diagnostic-blocked.

## Claim boundary

- This baseline comparison can support only conservative wording such as matched selected benchmarks or internal comparison workflow.
- It does not support wording such as solved, verified, exact, unified, or production grade.
