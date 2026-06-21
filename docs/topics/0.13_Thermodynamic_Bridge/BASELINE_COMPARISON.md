# Baseline Comparison

## Baseline target

This topic does not have one single universal comparator. It has lane-specific baselines, and each lane must stay inside its own evidence class.

## Current comparator package

| Lane | Baseline or comparator | Source type | Current role |
| :-- | :-- | :-- | :-- |
| Landauer lower-bound lane | `E_min = k_B T ln 2` with exact SI constants plus selected source-referenced measured erasure values | exact identity + source-referenced benchmark working copies | primary acceptance lane |
| Thermodynamic-gravity identity lane | standard Bekenstein, Unruh, and Hawking relations | established theoretical identities | constraint/comparison lane only |
| Synthetic nonequilibrium lane | Cattaneo-style lag demo against instantaneous Fourier-style expectation | topic-local synthetic benchmark | exploratory simulation lane |
| Vacuum entropy-sink lane | no accepted external comparator yet | topic-local hypothesis sandbox | no acceptance role |

If no dedicated competitor script exists, the comparator is the source dataset or standard identity declared in `DATA_MANIFEST.md`, `FORMULA_AUDIT.md`, and the verification artifact.

## Comparison metrics

| Lane | Metrics | Current threshold role |
| :-- | :-- | :-- |
| Landauer lower-bound lane | `landauer_engine_vs_codata_relative_error`, `jun_2014_ratio_to_landauer_lower_bound` | hard gate in verifier |
| Thermodynamic-gravity identity lane | formula-consistency outputs for Bekenstein/Hawking entropy and Unruh/Hawking temperatures | diagnostic; not an acceptance gate for UET dynamics |
| Synthetic nonequilibrium lane | qualitative lag/hysteresis behavior | no external threshold yet |
| Vacuum entropy-sink lane | none accepted | hypothesis-only |

The current topic-level benchmark meaning comes only from the Landauer lower-bound lane.

## Acceptance boundary

- This file does not certify a final pass/fail result by itself.
- The authoritative gate is `Result/artifacts/0_13_thermodynamic_bridge_verification.json`.
- Current hard thresholds are:
  - `landauer_engine_vs_codata_relative_error <= 1e-12`
  - `jun_2014_ratio_to_landauer_lower_bound >= 1.0`
  - all three primary tests in the verifier must pass
- Even if those checks pass, the topic remains `WARN` while source-normalized row capture, uncertainty propagation, and UET-specific bridge derivation remain open.

## Claim boundary

- Allowed wording now:
  - `source-referenced internal benchmark`
  - `formula-consistency check`
  - `lower-bound consistency`
  - `simulation-only exploratory lane`
  - `UET bridge hypothesis`
- Not allowed from this baseline package:
  - `solved`
  - `verified UET bridge`
  - `exact information-energy equivalence`
  - `external thermodynamic validation`
  - `foundation complete`

## Next comparator upgrades

1. Replace topic-derived Berut/Jun/Peterson summaries with row-level source-normalized captures.
2. Add uncertainty-aware comparison rows so measured heat and black-hole mass inputs carry visible error bars into the outputs.
3. Decide whether the Cattaneo lane will be replaced by a real heat-transport dataset or permanently demoted to simulation-only support.
4. Keep the vacuum entropy-sink branch outside the baseline package unless it gains an independently motivated falsification workflow.
