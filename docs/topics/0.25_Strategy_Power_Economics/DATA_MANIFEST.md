# Data Manifest: Topic 0.25

## Data reality

This topic now contains two deliberately separated data classes:

1. a source-locked U.S. historical Book 1 package used by the new primary diagnostics;
2. legacy local market/economy working copies used only for descriptive integrity checks.

The Book 1 source gate is `PASS` (`15/15` required inputs). The raw provider files live under
`docs/data/external/economics/us_historical/<provider>/2026-07-12/`; normalized source subsets
and their hashes are described by `Data/03_Research/uet_us_economics_transform_manifest.json`.
Provider raw files may remain local-only because of terms or repository ignore rules. If a
required file is absent or its hash does not match the manifest, the panel gate must return
`WARN` and no model may silently proceed.

## Book 1 source map

| Source / series | Upstream URL | Frozen local path | Source unit | Runtime transformation | Role |
| :-- | :-- | :-- | :-- | :-- | :-- |
| FRED `M2SL` | https://fred.stlouisfed.org/series/M2SL | `docs/data/external/economics/us_historical/fred/2026-07-12/M2SL.csv` | billions USD, SA, monthly | December/end-of-year annual observation | primary `M` |
| FRED `GDPC1` | https://fred.stlouisfed.org/series/GDPC1 | `.../fred/2026-07-12/GDPC1.csv` | chained-dollar real GDP, quarterly | annual mean | `R` component |
| FRED `POP` | https://fred.stlouisfed.org/series/POP | `.../fred/2026-07-12/POP.csv` | thousands of persons, monthly | annual mean | per-capita denominator |
| FRED `UNRATE` | https://fred.stlouisfed.org/series/UNRATE | `.../fred/2026-07-12/UNRATE.csv` | percent, monthly | annual mean | `N` proxy |
| FRED `CPIENGSL`, `CPIAUCSL` | https://fred.stlouisfed.org/series/CPIENGSL | `.../fred/2026-07-12/` | CPI indexes, monthly | annual mean, log change | `N` and inflation |
| FRED `GDPDEF`, `TB3MS` | https://fred.stlouisfed.org/series/GDPDEF | `.../fred/2026-07-12/` | price index / percent | annual mean | robustness/context |
| FRED `OPHNFB`, `COMPRNFB` | https://fred.stlouisfed.org/series/OPHNFB | `.../fred/2026-07-12/` | BLS indexes, quarterly | annual mean | BLS wage comparator and `R` productivity |
| FRED `PAYEMS`, `CMDEBT` | https://fred.stlouisfed.org/series/PAYEMS | `.../fred/2026-07-12/` | thousands / billions USD | annual mean or end-of-year | per-worker and credit sensitivity |
| BEA Fixed Assets | https://www.bea.gov/itable/fixed-assets | `docs/data/external/economics/us_historical/bea/2026-07-12/bea_fixed_assets_annual.csv` | chain-type quantity indexes, 2017=100 | Table 1.2/2.8 extraction; per-worker proxies | `K` and `I` |
| EIA Table 1.3 | https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T01.03&freq=A | `docs/data/external/economics/us_historical/eia/2026-07-12/eia_primary_energy_annual.csv` | quadrillion Btu/year | annual `TETCBUS`; divide by population, rebase | `R` energy |
| EPI provider chart | https://data.epi.org/productivity/productivity_levels/line/year/national/real_dollars_per_hour_2024/productivity_pay | `docs/data/external/economics/us_historical/epi/2026-07-12/epi_productivity_pay.csv` | provider real-dollar-per-hour chart values | rebase both series to 1979=100 | wage construction |

The exact original filenames, bytes, SHA-256 hashes, retrieval vintage, per-input UTC retrieval
timestamp, coverage, terms, and benchmark roles are machine-recorded in
`uet_us_economics_source_manifest.json`; raw-to-normalized lineage is machine-recorded in
`uet_us_economics_transform_manifest.json`. The panel recomputes each required input hash and
returns `WARN` on any mismatch.

## Derived panel and artifacts

- `Data/03_Research/uet_us_macro_panel_1959_2024.csv`: normalized 66-row panel; committed
  research subset with hash in `uet_us_macro_panel_status.json`.
- `Result/artifacts/0_25_uet_economics_verification.json`: aggregate artifact; references
  source, transform, panel, formula, parameter, holdout, claim, and sub-artifact hashes.
- `Result/artifacts/0_25_uet_resource_equation_audit.json`: coefficients, rolling origins,
  aggregate and median RMSE, and block-bootstrap intervals.
- `Result/artifacts/0_25_stone_balloon_audit.json`: mismatch forecasts, regime summaries,
  baselines, bootstrap intervals, and asset-lane status.

## Legacy working-copy lane

`Data/03_Research/SP500_yahoo_real.csv`, `Gold_yahoo_real.csv`, `Bitcoin_yahoo_real.csv`,
`Data/Global_Economy_2024.json`, and `daily_economic_snapshot.json` remain local diagnostic
working copies. Their provenance gate is separate and incomplete; none is primary evidence for
the Book 1 panel. They support only row-count, Gini-range, return-volatility, and correlation
statistics.

## Provenance and unit rules

- Every input records source URL, terms, original filename, local path, preprocessing, unit,
  coverage, retrieval vintage, benchmark role, and SHA-256 where available.
- `R`, `N`, `K`, and `I` are dimensionless/indexed proxies only after the documented divisions,
  rebasing, logs, and training-window standardization.
- Missing values are rejected; no interpolation, forward filling, or silent imputation is used.
- A manifest is a provenance control, not external validation or causal evidence.

## Open data blockers

- EIA 1776-1945 source-mix export is absent.
- A source-locked heat-content table with a common physical basis is absent, so literal
  energy-density claims remain blocked.
- LBMA annual gold and a licensed S&P 500 total-return export are absent.
- Legacy market/economy working copies still lack complete upstream retrieval metadata.
