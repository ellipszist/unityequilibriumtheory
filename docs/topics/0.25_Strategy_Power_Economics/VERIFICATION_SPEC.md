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
| `Data/03_Research/source_lock_manifest.json` | binds market/economy/snapshot working copies to explicit provenance classes |

## Generated workflow artifacts

- `Data/03_Research/source_lock_manifest.json`
- `Data/03_Research/source_evidence_intake_stub.json`
- `Data/03_Research/source_evidence_readiness_matrix.json`
- `Data/03_Research/model_claim_gate.json`
- embedded `descriptive_diagnostic_gate` in `Result/artifacts/0_25_strategy_power_economics_verification.json`
- embedded `economics_claim_scope_gate` in `Result/artifacts/0_25_strategy_power_economics_verification.json`

## Current readiness snapshot

- SP500/Gold/Bitcoin metadata packages: each `5/6` complete; blocked only by missing retrieval date
- Global economy baseline package: `4/6` complete; blocked by missing upstream URL/DOI and retrieval date
- Daily snapshot feed: `5/6` complete; blocked by missing upstream URL/API

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
limitations. It must also include `economics_claim_scope_gate.controller_status`,
blocked export phrases, and machine-readable next blockers so integration
summaries cannot promote descriptive diagnostics into policy or market-prediction
claims.

## Interpretation

- `PASS`: local time series are long enough, Gini units are sane, and source
  URL/DOI provenance is recorded.
- `WARN`: diagnostic metrics are computable, but provenance or model-claim
  blockers remain.
- `FAIL`: required inputs cannot be parsed or core metrics cannot be computed.

This verifier does not test strategic superiority, Nash-equilibrium improvement,
policy causality, or global social stabilization.

`descriptive_diagnostic_gate.diagnostic_run_contract == PASS` means only that
the market row-count and Gini sanity diagnostics passed. If
`descriptive_diagnostic_gate.status == DESCRIPTIVE_WARN`, policy, prediction,
and strategic-superiority claims remain blocked by provenance and causal-design
gaps.

`economics_claim_scope_gate.controller_status == DESCRIPTIVE_DIAGNOSTIC_ONLY`
is the export controller for `0.0` and paper-facing summaries. It may allow
descriptive market/economy diagnostics, but it blocks market prediction,
strategic-superiority, Nash-equilibrium, policy-causality, and
social-stabilization claims until source locks, baselines, causal design, and
calibrated simulation comparators exist.

## Book 1 economics hardening command

```powershell
.\.venv\Scripts\python.exe docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Verify_UET_Economics_Hardening.py
```

Use `--refresh-sources` only when fetching the public FRED inputs. The verifier
writes `Result/artifacts/0_25_uet_economics_verification.json` plus source,
parameter, holdout, formula, and claim gates under `Data/03_Research/`.

`WARN` is the correct result while required source exports are missing. A completed
internal diagnostic remains Claim Class C; a passing run never authorizes claims
of causal fiat effects, a confirmed economic law, policy validation, or asset
superiority.
