# Data Manifest

Current data reality status: `real source referenced`

The topic contains usable local economic and market working copies, but upstream
source identity is not yet archival enough for strong macroeconomic or policy
claims.

## Primary Inputs

| Dataset | Local path | Source | Unit convention | Bytes | SHA-256 | Benchmark role | Provenance status |
| :-- | :-- | :-- | :-- | --: | :-- | :-- | :-- |
| S&P 500 time series | `Data/03_Research/SP500_yahoo_real.csv` | Yahoo-style `^GSPC` working copy | index points, date, volume | 342,186 | `bc85614da6993c0edcf87ceb5bfd623003bad18b7b78f9b010bd8582a6252eeb` | market diagnostic input | local copy hashed by artifact; retrieval URL/date still needed |
| Gold time series | `Data/03_Research/Gold_yahoo_real.csv` | Yahoo-style `GC=F` working copy | USD/oz futures close, date, volume | 294,015 | `c558881407ce03cdf4dda12e57d972f620447d37be9750e953224502f3b940ba` | market diagnostic input | local copy hashed by artifact; retrieval URL/date still needed |
| Bitcoin time series | `Data/03_Research/Bitcoin_yahoo_real.csv` | Yahoo-style `BTC-USD` working copy | USD close, date, volume | 323,807 | `62a93ec47ffe98f7908a8c8b29ba9fa5a070fa611bb3cde5ae22bfb23ff9617a` | market diagnostic input | local copy hashed by artifact; retrieval URL/date still needed |
| Global economy baseline | `Data/Global_Economy_2024.json` | local World Bank/IMF referenced working copy | population count, GDP PPP USD, Gini 0-100 | 1,505 | `a3dd47fd7dadb6ce2ba6f4b634788a6dc782ea70b4f63d8222689c50eb8ba9d7` | economy sanity benchmark | source named but URL/DOI and exact table extraction missing |
| Daily economic snapshot | `Data/03_Research/daily_economic_snapshot.json` | `UET_FINANCIAL_GATEWAY` local snapshot | mixed: points, USD/oz, THB, percent | 729 | `f22483d6854d4c48039bf95d0f68b475b74e06860375c66b962e23a160fdd721` | local indicator snapshot | no upstream URL/DOI; not paper-ready |
| Source-lock manifest | `Data/03_Research/source_lock_manifest.json` | topic-derived provenance map for market/economy/snapshot working copies | inherits per-target unit conventions | 3,448 | `540f9bedafe6c04317482da3daedb8e6970fb0ed7347e1e6c9ae4762232dafe6` | binds local data classes, benchmark roles, and shared Yahoo-style provider reference | present; improves provenance discipline but does not create archival upstream retrieval metadata |
| Source evidence intake stub | `Data/03_Research/source_evidence_intake_stub.json` | topic-generated intake sheet for unresolved market/economy/snapshot source metadata | mixed; each target declares its own expected unit basis | 7,344 | `2de01fc979dc68868f18f24bf441620f55f3b31bf52914b2f5cfb0e1e88bf2b2` | landing zone before data rewrites or claim upgrades | workflow control only; not evidence by itself |
| Source evidence readiness matrix | `Data/03_Research/source_evidence_readiness_matrix.json` | topic-generated readiness gate derived from the intake stub | n/a | 2,602 | `4463d2303d8f5cec7ca413f3aef3b966017e3677d78dd151567def36bc54b81e` | tracks completeness of provenance capture | all five targets are now mapped as `partial`; remaining blockers are specific metadata gaps rather than blank placeholders |
| Model claim gate | `Data/03_Research/model_claim_gate.json` | topic-generated claim gate for diagnostic versus simulation lanes | n/a | 1,960 | `fa902d0d6d67cea9df2be2ad429123b2ef5a27099d23c00ff66aebf3c395591f` | controls allowed claim class per lane | workflow control only; cannot raise claim strength beyond descriptive diagnostics |
| Research_Economic_Data_Audit.py | `Code/03_Research/Research_Economic_Data_Audit.py` | topic verifier | n/a | 28,515 | `eb6e5ca4c385ff41ae6aaf3a1164655d84a25dbb8dc9bb74c4d4764477e3e71b` | regenerates descriptive diagnostics and claim-scope artifact | executable verifier; does not create prediction, policy, or strategy validation |
| Descriptive diagnostic gate artifact | `Result/artifacts/0_25_strategy_power_economics_verification.json` | verifier-generated gate for market/economy diagnostics | n/a | 12,755 | `89ec901da2c8b1546ca175931f3b7b98a1a162350207ad352466b81158c94ddc` | separates row-count/Gini sanity from policy or prediction claims | Can pass only descriptive diagnostics; policy, prediction, and strategic claims remain blocked until provenance and causal baselines exist. |

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
