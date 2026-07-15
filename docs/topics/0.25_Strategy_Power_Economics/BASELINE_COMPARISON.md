# Baseline Comparison: Book 1 Economics Diagnostics

## Purpose

This document reports the latest source-locked internal comparisons. It is not a claim of
prediction, causal identification, policy validation, or asset superiority. Numeric values are
read from `Result/artifacts/0_25_uet_economics_verification.json` and its referenced sub-artifacts.

## Resource-engine rolling-origin results

The primary horizon is three years; one and five years are sensitivities. Improvement is
`1 - median(UET absolute forecast error) / median(baseline absolute forecast error)`. A positive
value favors the UET proxy. The predeclared candidate rule also requires every bootstrap upper
endpoint to be below zero and positive knowledge/infrastructure coefficients.

| Horizon | Origins | Median UET RMSE | Median constant-growth RMSE | Improvement vs constant | Improvement vs zero-growth | Candidate |
| --: | --: | --: | --: | --: | --: | :-- |
| 3 years | 22 | 0.02659 | 0.02315 | -14.9% | -6.4% | false |
| 1 year | 24 | 0.00811 | 0.00874 | +7.3% | +25.7% | false |
| 5 years | 20 | 0.04986 | 0.03508 | -42.1% | -21.3% | false |

The primary 3-year bootstrap interval for UET minus constant-growth squared error is
`[0.000212, 0.001242]`, above zero. The result therefore does not meet the candidate rule.

## Stone-in-the-Balloon inflation baselines

| Horizon | Median UET RMSE | AR improvement | Money-growth improvement | Quantity-style improvement | Candidate |
| --: | --: | --: | --: | --: | :-- |
| 3 years | 0.02260 | -67.0% | -12.3% | -3.3% | false |
| 1 year | 0.01812 | -107.5% | -1.5% | -10.3% | false |
| 5 years | 0.02148 | -87.6% | -15.7% | +2.8% | false |

The UET mismatch does not beat the autoregression at any horizon. Bootstrap intervals are
reported in the Stone artifact; the 5-year quantity-style point improvement is not a robust
candidate signal because its upper endpoint remains above zero.

## Wage construction comparison

| Source construction | Coverage | Productivity growth | Compensation growth | Gap (percentage points) |
| :-- | :-- | --: | --: | --: |
| Book quote (typical worker wording) | 1979-2021 | 64.6% | 17.3% | 47.3 |
| EPI versioned provider chart | 1979-2021 | 80.24% | 28.38% | 51.86 |
| BLS nonfarm-business comparator | 1979-2021 | 125.02% | 56.64% | 68.38 |

The differences are construction/vintage findings. They do not select a preferred result and
do not identify fiat policy as a cause.

## Regime and asset boundaries

The pre-1971 summary covers 1959-1970 (`n=11`) and the post-1973 summary covers 1974-2024
(`n=51`); 1971-1973 are excluded descriptively. The mean monetary-resource mismatch is
`0.04076` pre-1971 and `0.05298` post-1973; these are non-causal regime descriptions.

The pegged-stone asset lane is `BLOCKED` because exact LBMA annual gold and licensed S&P 500
total-return exports are absent. Yahoo price-only files remain excluded by design.

## Interpretation

The current evidence supports the statement that the predeclared UET proxies did not satisfy
the declared candidate criteria in this U.S. panel. It does not support an economic-law,
fiat-causality, policy, asset, or strategic conclusion.
