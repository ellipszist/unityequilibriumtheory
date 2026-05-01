# Verification Spec

## Primary command

```powershell
python docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Research_Economic_Data_Audit.py
```

## Inputs

| Input | Role |
| :-- | :-- |
| `Data/03_Research/SP500_yahoo_real.csv` | S&P 500 market time-series working copy |
| `Data/03_Research/Gold_yahoo_real.csv` | gold futures market time-series working copy |
| `Data/03_Research/Bitcoin_yahoo_real.csv` | Bitcoin market time-series working copy |
| `Data/Global_Economy_2024.json` | population, GDP PPP, and Gini working copy |
| `Data/03_Research/daily_economic_snapshot.json` | local daily indicator snapshot |

## Metrics

| Metric | Meaning | Current threshold |
| :-- | :-- | :-- |
| `row_count` | usable close-price rows per market series | `>= 2500` |
| `annualized_volatility` | descriptive volatility from log returns | recorded, not pass/fail |
| `return_correlation` | descriptive cross-market Pearson correlation | recorded, not pass/fail |
| `gini_min/gini_max` | Gini index unit sanity | within `0..100` |
| source URL/DOI presence | provenance gate for economy/snapshot inputs | required for PASS |

## Artifact target

`Result/artifacts/0_25_strategy_power_economics_verification.json`

The artifact must include `status`, command, environment, formula IDs, input
hashes, market metrics, economy metrics, thresholds, checks, blockers, and
limitations.

## Interpretation

- `PASS`: local time series are long enough, Gini units are sane, and source
  URL/DOI provenance is recorded.
- `WARN`: diagnostic metrics are computable, but provenance or model-claim
  blockers remain.
- `FAIL`: required inputs cannot be parsed or core metrics cannot be computed.

This verifier does not test strategic superiority, Nash-equilibrium improvement,
policy causality, or global social stabilization.
