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
| Source-lock manifest | `Data/03_Research/source_lock_manifest.json` | topic-derived provenance map for market/economy/snapshot working copies | inherits per-target unit conventions | binds local data classes, benchmark roles, and shared Yahoo-style provider reference | present; improves provenance discipline but does not create archival upstream retrieval metadata |
| Source evidence intake stub | `Data/03_Research/source_evidence_intake_stub.json` | topic-generated intake sheet for unresolved market/economy/snapshot source metadata | mixed; each target declares its own expected unit basis | landing zone before data rewrites or claim upgrades | workflow control only; not evidence by itself |
| Source evidence readiness matrix | `Data/03_Research/source_evidence_readiness_matrix.json` | topic-generated readiness gate derived from the intake stub | n/a | tracks completeness of provenance capture | all five targets are now mapped as `partial`; remaining blockers are specific metadata gaps rather than blank placeholders |
| Model claim gate | `Data/03_Research/model_claim_gate.json` | topic-generated claim gate for diagnostic versus simulation lanes | n/a | controls allowed claim class per lane | workflow control only; cannot raise claim strength beyond descriptive diagnostics |
| Descriptive diagnostic gate | embedded in `Result/artifacts/0_25_strategy_power_economics_verification.json` | verifier-generated gate for market/economy diagnostics | n/a | separates row-count/Gini sanity from policy or prediction claims | Can pass only descriptive diagnostics; policy, prediction, and strategic claims remain blocked until provenance and causal baselines exist. |

## Hash Policy

The primary verifier records SHA-256 hashes for all primary inputs in
`Result/artifacts/0_25_strategy_power_economics_verification.json`.

## Data Use Boundary

These data support descriptive diagnostics: row counts, returns, volatility,
correlations, and Gini sanity. They do not by themselves support causal claims
about strategic superiority, social stabilization, or economic policy outcomes.

## Next Provenance Work

- Add exact retrieval dates for each Yahoo-style market time series.
- Add upstream World Bank/IMF URL or DOI and retrieval date for `Global_Economy_2024.json`.
- Add upstream URL or API description for `daily_economic_snapshot.json`.
- Replace local World Bank/IMF referenced JSON with source-locked tables and
  retrieval dates.
- Move raw upstream downloads to `docs/data/external/economics/...` when fetched;
  keep topic-derived normalized copies under this topic's `Data/` folder.
- Use `source_evidence_intake_stub.json` and `source_evidence_readiness_matrix.json`
  as the gate before editing working-copy data or upgrading claim language.

## Current Readiness Snapshot

- SP500 market metadata: `5/6` fields complete; missing `retrieval_date`
- Gold market metadata: `5/6` fields complete; missing `retrieval_date`
- Bitcoin market metadata: `5/6` fields complete; missing `retrieval_date`
- Global economy baseline: `4/6` fields complete; missing upstream `URL/DOI` and `retrieval_date`
- Daily snapshot feed: `5/6` fields complete; missing `upstream_url_or_api`
