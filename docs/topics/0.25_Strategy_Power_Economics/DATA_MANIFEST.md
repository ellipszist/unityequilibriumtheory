# Data Manifest: Topic 0.25

## Data reality

This topic now contains two deliberately separated data classes:

1. a source-locked U.S. historical Book 1 package used by the new primary diagnostics;
2. legacy local market/economy working copies used only for descriptive integrity checks.

The Book 1 U.S. source gate is PASS (15/15 required inputs). The long-term roadmap adds
global, welfare, credit, licensed asset, energy-density, and distributional lanes without
mixing them into the frozen baseline. The raw provider files live under
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
| Fed Z.1 `S11.1.i.a` | https://www.federalreserve.gov/releases/z1/ | `docs/data/external/economics/us_historical/fed_z1/2026-07-16/z1_csv_files.zip` | millions of dollars; annual transactions, NSA | select sectoral flow codes; freeze 1959-2024; no imputation | funding channels and accounting bridge |
| BLS Input-Output researcher ZIP | https://www.bls.gov/emp/data/input-output-matrix.htm | `docs/data/external/economics/us_historical/bls_io/2026-07-16/input-output.zip` (pending) | nominal and chain-weighted I-O matrices; provider coverage 1997-2024 | archive/hash/quality gate before parsing | payer-resource industry/commodity flow candidate |
| BEA 1997 benchmark I-O archives | https://www.bea.gov/industry/historical-benchmark-input-output-tables | `docs/data/external/economics/us_historical/bea_io/1997-benchmark/` | make/use: millions of dollars at producers prices; requirements: coefficients | ZIP member, code, table-reference, year, finite-value, and SHA-256 checks | one-year structural benchmark only; not annual payer/resource evidence |
| BEA industry/commodity/NAICS concordance | https://www.bea.gov/itable/input-output | `docs/data/external/economics/us_historical/bea_io/2026-07-16/BEA-Industry-and-Commodity-Codes-and-NAICS-Concordance.xlsx` | official code crosswalk workbook | ZIP structure/sheet check; SHA-256 lock | industry concordance only; no flow observations |
| BLS industry hours API | https://api.bls.gov/publicAPI/v2/timeseries/data/ | `docs/data/external/economics/us_historical/bls_labor/2026-08-01/` plus `Data/03_Research/bls_industry_hours_1987_2024.csv` | annual hours worked, millions of hours | predeclared NAICS4 candidate query; 11/202 returned with complete 1987-2024 rows (418); 16 other candidate batches quota-limited; no imputation | bounded labor-input diagnostic |
| USGS historical mineral statistics | https://www.usgs.gov/centers/national-minerals-information-center/historical-statistics-mineral-commodities-united | `docs/data/external/economics/us_historical/usgs_materials/2026-07-16/` plus `Data/03_Research/usgs_material_quantities_1900_2022.csv` | commodity-specific physical quantities | workbook XML extraction; national quantities only; no industry/project allocation | material-throughput diagnostic |
| SEC Company Facts | https://www.sec.gov/edgar/sec-api-documentation | `docs/data/external/economics/us_historical/sec_xbrl/2026-07-16/` plus `Data/03_Research/sec_public_firm_funding_proxy_2010_2024.csv` | annual 10-K reported USD facts | predeclared 10-firm sample; tag/unit/date validation; no imputation | firm funding-scale proxy |
| USAspending.gov federal awards | https://api.usaspending.gov/docs/endpoints | `docs/data/external/economics/us_historical/usaspending/2026-08-01/` plus `Data/03_Research/usaspending_doe_fy2024_transactions.csv` | current U.S. dollars; award obligations | fixed DOE FY2024 contract query, five pages/500 rows; no imputation; cached API wrappers and hashes | bounded public payer/recipient ledger; not settlement or financing-source evidence |
| Project payment ledger boundary | https://www.census.gov/topics/research/guidance/restricted-use-microdata/economic-data.html | `Result/artifacts/0_25_project_payment_ledger_gate.json` | invoice/transaction-level payer and purchase identity | records public-data restriction and approved access route | blocked provenance link |

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
- `Result/artifacts/0_25_payer_resource_join_readiness.json`: source/hash/readiness status for
  every link needed to connect funding flows to industry use, labor, physical resources, and
  project/output records.
- `Result/artifacts/0_25_usaspending_federal_project_ledger.json`: five-page DOE FY2024
  public-award transaction sample with source hashes and explicit non-settlement/non-financing
  boundary.

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

## Wave 3 welfare source package

The separate welfare manifest at docs/data/external/welfare/uet_us_welfare_source_manifest.json
archives FRED rent (CUSR0000SEHA), owners equivalent rent (CUSR0000SEHC), real median household
income (MEHOINUSA672N), and FHFA house-price index (USSTHPI). The audit freezes observations
through 2024, uses the common complete intersection without imputation, and keeps welfare
outcomes separate from aggregate GDP. Its source hashes are embedded in the aggregate artifact.

## Long-term source expansion contract

Wave 1 extends the manifest to FRED/H.6, BEA, BLS, EIA, FHFA, Census/Fed distributional
accounts, USPTO/PatsView, licensed LBMA/S&P/CRSP, and later WDI/OECD/ILOSTAT/IMF/BIS/WID.
Each new file must record provider, source URL, terms, release and retrieval timestamps,
as-of/revision vintage, original filename, local path, preprocessing, units, coverage,
benchmark role, and SHA-256. Global files are not eligible for pooling until the U.S. package
and PPP/exchange-rate policy are frozen.

## Open data blockers

- EIA 1776-1945 source-mix export is absent.
- A source-locked heat-content table with a common physical basis is absent, so literal
  energy-density claims remain blocked.
- LBMA annual gold and a licensed S&P 500 total-return export are absent.
- Legacy market/economy working copies still lack complete upstream retrieval metadata.
- Fed Z.1 sectoral flow mapping is complete for the frozen years, but payer/payee and
  natural-resource concordance data are not yet source-locked.
- BLS I-O archive is pending because the official endpoint returned Access Denied and the
  provider quality notice requires replacement-file validation.
- BLS industry-hours API archive is bounded (11 returned NAICS4 candidates, complete 1987-2024, 418 rows); 16 other candidate batches remain quota-limited and were not imputed.
- BEA code concordance and the 1997 benchmark I-O archives are source-locked and validated for
  structural use. The BEA annual I-O flow export still requires API registration or an interactive
  export and has not entered the primary panel.
- USAspending public-award lane is `PASS_WITH_BOUNDARY` for the fixed DOE FY2024 sample, but it does not identify bank settlement, private invoices, or tax/debt/money-creation financing.
- Payer-resource join gate is `BLOCKED`: BLS and USGS inputs now exist as bounded source packages, but they do not form a common industry/project join; the project payment ledger remains unavailable.
