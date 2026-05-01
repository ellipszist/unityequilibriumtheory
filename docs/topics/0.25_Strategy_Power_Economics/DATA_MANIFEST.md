# Data Manifest

Current data reality status: `real source referenced`

The topic contains usable local economic and market working copies, but upstream
source identity is not yet archival enough for strong macroeconomic or policy
claims.

## Primary Inputs

| Dataset | Local path | Source | Unit convention | Benchmark role | Provenance status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| S&P 500 time series | `Data/03_Research/SP500_yahoo_real.csv` | Yahoo-style `^GSPC` working copy | index points, date, volume | market diagnostic input | local copy hashed by artifact; retrieval URL/date still needed |
| Gold time series | `Data/03_Research/Gold_yahoo_real.csv` | Yahoo-style `GC=F` working copy | USD/oz futures close, date, volume | market diagnostic input | local copy hashed by artifact; retrieval URL/date still needed |
| Bitcoin time series | `Data/03_Research/Bitcoin_yahoo_real.csv` | Yahoo-style `BTC-USD` working copy | USD close, date, volume | market diagnostic input | local copy hashed by artifact; retrieval URL/date still needed |
| Global economy baseline | `Data/Global_Economy_2024.json` | local World Bank/IMF referenced working copy | population count, GDP PPP USD, Gini 0-100 | economy sanity benchmark | source named but URL/DOI and exact table extraction missing |
| Daily economic snapshot | `Data/03_Research/daily_economic_snapshot.json` | `UET_FINANCIAL_GATEWAY` local snapshot | mixed: points, USD/oz, THB, percent | local indicator snapshot | no upstream URL/DOI; not paper-ready |

## Hash Policy

The primary verifier records SHA-256 hashes for all primary inputs in
`Result/artifacts/0_25_strategy_power_economics_verification.json`.

## Data Use Boundary

These data support descriptive diagnostics: row counts, returns, volatility,
correlations, and Gini sanity. They do not by themselves support causal claims
about strategic superiority, social stabilization, or economic policy outcomes.

## Next Provenance Work

- Add exact Yahoo query/download metadata for each market time series.
- Replace local World Bank/IMF referenced JSON with source-locked tables and
  retrieval dates.
- Move raw upstream downloads to `docs/data/external/economics/...` when fetched;
  keep topic-derived normalized copies under this topic's `Data/` folder.
