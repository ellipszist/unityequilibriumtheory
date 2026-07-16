# Formula Audit: 0.25 Strategy Power Economics

## Audit status

The current registry is a source-linked diagnostic registry. Book 1 relations are hypotheses
and heuristic bridges. No entry is a derived economic law. Every formula maps to a script and a
machine-readable artifact.

| Formula ID | Relation / code path | Variables and units | Origin / proof | Role and failure mode |
| :-- | :-- | :-- | :-- | :-- |
| `EC25-UET-RESOURCE-ENGINE` | Book concept `R = N + K + I`; operational regression `Delta ln R[t+3] = alpha + beta_N N[t] + beta_K Delta ln K[t] + beta_I Delta ln I[t] + epsilon[t]` in `Research_UET_Resource_Equation_Audit.py` | `R` is a 1959=100 geometric index of GDP/person, output/hour, and primary-energy/person; `N` is a training-window standardized proxy; `K` is a BEA IP-product quantity index (2017=100)/employee; `I` is a geometric mean of BEA fixed-asset quantity indexes (2017=100)/employee; all modeled changes are dimensionless log changes | heuristic bridge; no dimensional closure to the Book concept | temporal diagnostic. Proxy aggregation, endogeneity, and omitted variables prevent causal or identity interpretation. |
| `EC25-UET-MONETARY-RESOURCE-MISMATCH` | `D[t] = Delta ln M2[t] - Delta ln R[t]` in `Research_Stone_Balloon_Audit.py` | `M2` is FRED billions USD (December level); `R` is the dimensionless proxy index; `D` is dimensionless | topic-derived relation; heuristic diagnostic | inflation baseline comparator. Monetary endogeneity and omitted shocks prevent fiat-causality claims. |
| `EC25-UET-WAGE-PRODUCTIVITY-GAP` | `gap[t] = ln(productivity[t]) - ln(compensation[t])` in `Research_Wage_Productivity_Audit.py` | EPI provider chart indexes are rebased to 1979=100; BLS comparator indexes are source-specific; logs are dimensionless | source-locked benchmark input; construction-specific diagnostic | reproduces EPI and reports BLS separately. Different universes/deflators are not silently merged. |
| `EC25-UET-ENERGY-DENSITY` | energy-throughput source mix and literal heat-content definition gate in `Research_Energy_Density_Audit.py` | postwar EIA input is quadrillion Btu/year; literal density requires a common physical basis such as MJ/kg and declared treatment of non-combustion sources | open placeholder; not closed | descriptive energy lane only. Throughput is not fuel density and cannot establish a macro mechanism. |
| `EC25-LOG-RETURN` and legacy formulas | legacy market return/volatility/correlation formulas in `Research_Economic_Data_Audit.py` | source-unit prices become dimensionless log returns; annualization uses a documented 252-day convention | checked local diagnostic | separate legacy lane; incomplete upstream retrieval metadata remains a limitation. |

## Formula registry v2 and measurement gate

The formula IDs above remain the current operational contract. The long-term registry requires
at least three declared operationalizations for each R/N/K/I construct, reliability and
measurement-error checks, historical invariance, and structural-break sensitivity. The
machine-readable variable and formula architecture is embedded by the aggregate verifier; until
WARN_MEASUREMENT and WARN_UNIT close, R=N+K+I remains a heuristic bridge.

## Unit closure policy

The Book 1 resource engine is explicitly `Proxy`, not `Closed`: source quantities are divided
by population or employees, rebased, logged, and combined only to create dimensionless indexes.
No dollar-valued BEA series is claimed where the source provides a chain-type quantity index.
The monetary mismatch and wage-gap logs are dimensionless after positive-index checks.

## Constant and parameter policy

There are no source-locked physical constants in this lane. The 1959 base year, 3-year primary
horizon, 1/5-year sensitivities, 2000 rolling-origin start, 1971-1973 exclusion, equal weights,
and 10%/bootstrap candidate rule are declared benchmark parameters in
`uet_us_economics_parameter_policy.json` and `uet_us_economics_holdout_policy.json`.
They are not fitted to the holdout and do not imply a theoretical constant.

## Verification linkage

- Formula gate: `Data/03_Research/uet_us_economics_formula_gate.json`.
- Resource artifact: `Result/artifacts/0_25_uet_resource_equation_audit.json`.
- Stone artifact: `Result/artifacts/0_25_stone_balloon_audit.json`.
- Wage artifact: `Result/artifacts/0_25_wage_productivity_audit.json`.
- Aggregate export controller: Result/artifacts/0_25_uet_economics_verification.json.
- Long-term architecture: RESEARCH_ROADMAP_EVIDENCE_GRADE_A.md, VARIABLE_DICTIONARY.md,
  CAUSAL_DAG.md, and Data/03_Research/uet_economics_warn_gate_registry.json.
