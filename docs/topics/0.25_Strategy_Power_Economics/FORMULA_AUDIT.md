# Formula Audit: 0.25_Strategy_Power_Economics

Review status: reviewed first-pass registry for the economic-data and market
diagnostics lane. Social-manifold, strategy, policy, and game-theory claims remain
heuristic until separate verifiers with falsifiable thresholds exist.

## Formula Registry

| formula_id | relation | code surface | variables and units | constant_origin | proof_status | verification_role | failure_mode | next_hardening_step |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `EC25-LOG-RETURN` | `r_t = ln(P_t / P_{t-1})` | `Research_Economic_Data_Audit.py`; Yahoo-style CSVs | `P_t` close price/index level in source unit; `r_t` dimensionless | source-referenced market CSV working copies | checked local diagnostic | primary market time-series metric | Missing dates, adjusted-vs-unadjusted mismatch, or bad price rows distort all downstream metrics | Add upstream download URL, retrieval date, ticker metadata, and adjusted-close policy. |
| `EC25-ANNUALIZED-VOLATILITY` | `sigma_ann = std(r_t) * sqrt(252)` | `Research_Economic_Data_Audit.py` | daily log returns dimensionless; annualized volatility dimensionless fraction/year | standard finance convention; 252 trading-day anchor | benchmark convention | primary descriptive risk metric | Bitcoin trades daily while equities/gold use trading days; common 252 factor is imperfect | Split asset-class calendars and document calendar convention. |
| `EC25-RETURN-CORRELATION` | `corr(r_x, r_y) = cov(r_x,r_y)/(sigma_x sigma_y)` | `Research_Economic_Data_Audit.py` | paired log returns, dimensionless | standard Pearson correlation | descriptive diagnostic | secondary cross-market diagnostic | Date alignment is currently tail-length based, not calendar-join based | Implement date-keyed joins before using correlations as evidence. |
| `EC25-GINI-SANITY` | `0 <= Gini <= 100` and economy row count | `Global_Economy_2024.json`; `Research_Economic_Data_Audit.py` | Gini index in 0-100 convention; GDP PPP in USD; population count | topic-local World Bank/IMF referenced working copy | source-referenced sanity check | primary economy-data integrity check | Source string names World Bank/IMF but no URL/DOI, retrieval date, or exact table | Replace with source-locked World Bank/IMF rows and hashes. |
| `EC25-OMEGA-RESOURCE-SPREAD` | `Omega = variance(resources)` or engine field spread proxy | `Engine_Power_Dynamics.py`; `Research_8_Billion_Resonance.py` | resources dimensionless simulation units; Omega dimensionless variance/proxy | topic-derived simulation heuristic | heuristic/open | excluded from primary verifier | Old artifact showed stabilizer scenario did not reduce inequality while README claimed PASS | Add deterministic seed, baseline scenario, threshold, and artifact table before any stability claim. |
| `EC25-WORLD-LEASE` | `lease_pool = fee_rate * sum(C_high)` then redistribute to `C_low` | `Engine_Power_Dynamics.py`; `Research_World_Lease_Comparison.py` | `C` resource field in dimensionless model units; `fee_rate` dimensionless | topic-derived policy simulation | heuristic/open | future policy simulator only | Policy terms are not calibrated to real tax/wealth-flow data | Calibrate against source-locked distribution data and policy baselines. |
| `EC25-SOCIAL-STABILIZER` | Type C/D agent rules from boldness/selfishness parameters | `Engine_Power_Dynamics.py`; `Proof_Social_Stability.py` | agent traits dimensionless; resources dimensionless | topic heuristic | heuristic/open | future social-manifold lane only | Agent taxonomy can encode desired outcome and overstate causality | Add parameter sweep, random seeds, out-of-sample scenarios, and external empirical anchor. |

## Claim Boundary

- Current accepted evidence supports only Claim Class C internal diagnostics for
  local economic data integrity and descriptive market metrics.
- It does not support claims that UET is better than Nash equilibrium, proves a
  world-stabilizing policy, or causally explains macroeconomic power.
- Social-manifold and strategy simulations may remain as model proposals, but
  must cite their own artifact and limitations before being promoted.

## Audit Link

- Core audit report: `docs/meta/core_research_hardening_audit.md`
