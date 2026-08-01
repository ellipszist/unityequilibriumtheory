# Method: Book 1 Economics Diagnostic Lane

## Scope and theory status

Book 1 supplies hypotheses, not a closed economic theory. The conceptual relation `R = N + K + I`
links resource-capacity change to necessity/constraint, knowledge, and infrastructure. The
money-value idea is tested as a mismatch between monetary growth and a measured resource-capacity
proxy. The Stone-in-the-Balloon, energy-density, and wage-productivity statements are kept as
separate falsifiable lanes.

All four lanes are internal, descriptive, and non-causal. The formulas are registered as
`heuristic bridge` or `topic-derived relation`, never as first-principles economic identities.

## Long-term research architecture

The current method is the U.S. diagnostic baseline in a ten-wave path toward Evidence Grade A.
The preregistered hypotheses, outcomes, and holdout policy live in RESEARCH_REGISTER.md; variable
definitions, the causal DAG, and the claim matrix are separate contracts. The 12-gate registry
is controlling: source/revision/license/unit/measurement/missingness/leakage, baseline, causal,
external, and publication WARNs cannot be hidden by an aggregate average. Strategy, Power, Nash,
and Social Stabilization remain quarantined from core economics evidence.

## Population, period, and source package

- Country: United States.
- Frequency: annual.
- Coverage: 1959-2024, frozen at retrieval vintage `2026-07-12`.
- Panel: `66` complete rows; no silent imputation.
- Sources: FRED/H.6 and BLS series, BEA Fixed Assets Tables 1.2/2.8, EIA Table 1.3,
  a versioned EPI Data Library chart export, the BLS public industry-hours API, official USGS
  mineral quantity workbooks, SEC Company Facts, and a restricted-data project-ledger gate.
- Source identity: `Data/03_Research/uet_us_economics_source_manifest.json` and
  `uet_us_economics_transform_manifest.json`.

## Proxy construction

### Resource capacity `R`

Each component is rebased to 1959=100 and combined as an equal-weight geometric mean:

1. real GDP per capita from `GDPC1 / POP`;
2. nonfarm-business output per hour from `OPHNFB`;
3. primary energy consumption per capita from EIA `TETCBUS / POP`.

The result is dimensionless and intentionally proxy-based. It is not a national wealth stock
and not a direct measurement of the Book's theoretical `R`.

### Necessity / constraint `N`

`N` is the equal-weight mean of training-window standardized CPI-energy inflation and the
unemployment rate. Standardization is recomputed using only data available at each rolling
forecast origin. This is an explicit diagnostic proxy for constraint, not biological necessity.

### Knowledge `K`

`K` is BEA nonresidential intellectual-property product investment's chain-type quantity index
(2017=100), divided by total nonfarm employees. The index is not treated as a dollar-valued
investment series. Utility patents per capita remain a declared robustness extension and are
not silently substituted in the primary run.

### Infrastructure `I`

`I` is the geometric mean of BEA nonresidential tangible fixed-asset and government fixed-asset
chain-type quantity indexes (2017=100), each divided by total nonfarm employees. It is an
indexed infrastructure proxy, not a dollar-valued capital stock.

## Verification lanes

1. **Resource engine:** estimate `Delta ln R[t+3]` on `N[t]`, `Delta ln K[t]`, and
   `Delta ln I[t]`; report one- and five-year sensitivities. `K` and `I` have expected
   positive associations in the diagnostic, while `N` has no predeclared sign.
2. **Stone-in-the-Balloon:** define `D[t] = Delta ln M2[t] - Delta ln R[t]`; compare one-,
   three-, and five-year inflation forecasts with inflation autoregression, money-growth-only,
   and quantity-style baselines. Summaries split 1959-1970 and 1974-2024, excluding 1971-1973.
3. **Pegged-stone asset lane:** requires exact LBMA gold and licensed S&P 500 total-return
   exports. The current lane is blocked; no Yahoo price-only substitution is allowed.
4. **Energy lane:** the postwar EIA throughput series is ready for the panel. The historical
   1776-1945 transition and literal fuel-energy-density claim remain blocked pending a common
   heat-content basis and conversion audit.
5. Wage lane: reproduce the versioned EPI chart construction, then report BLS OPHNFB/
   COMPRNFB separately. Differences are source/vintage/construction findings, not evidence of
   fiat causality.
6. Measurement-validity lane: compare three declared R, N, K, and I families, report pairwise
   index correlations and coefficient-sign stability, and leave missing patent data as a
   blocker rather than imputing it.
7. Welfare lane: use source-locked rent, OER, real median household income, and house-price
   series to report household pressure separately from GDP. The lane is descriptive and does
   not infer policy or fiat causality.
8. **Funding-source flow:** use Fed Z.1 S11.1.i.a to map sectoral outflows (compensation,
   taxes, interest, dividends, and transfers) and funding channels (net saving, debt, and
   equity transactions) into a rounded accounting bridge to capital formation. This identifies
   aggregate channels, not the payer of an individual purchase or the physical resource and
   labor transformation behind an investment.
9. **Payer-resource input-output source:** the BLS 1997-2024 matrix remains reserved for a later
   annual industry/commodity flow join; its source gate records the provider quality notice and access
   failure. A separate BEA 1997 benchmark archive is validated only as a one-year structural check,
   not as a time series or primary annual panel.

10. **Funding mix audit:** compute same-year and 0-2-year lead correlations between Z.1 net
   saving, debt, loans, and equity-liability transactions and capital formation, plus payment-flow
   scale relative to gross value added. Ratios are signed net-flow diagnostics and are not summed
   or labeled as earmarked funding shares.
11. **BEA benchmark structural check:** validate the source-locked 1997 make/use, direct-requirements, and total-requirements tables, including code crosswalk, table references, units, and finite-value checks. The benchmark is explicitly not a time series and cannot identify payer provenance.

12. **Payer-resource join readiness:** audit the required chain `funding -> industry use -> labor
   hours -> physical resource quantities -> output/innovation`. The gate records local archive
   identity and hashes for each link, rejects missing or unverified joins, and does not infer a
   project funding share from aggregate accounts.

13. **Industry labor-hours:** query only the official BLS public API for predeclared four-digit
   NAICS candidates. Returned rows are annual hours worked (millions of hours), coverage is
   recorded per code, and absent codes remain missing. The current archive contains 418 rows for
   11 returned series complete over 1987-2024; the source artifact remains `WARN` because the
   202-code candidate universe was not fully returned. The join gate may use this bounded subset,
   but it is not a complete labor ledger.
14. **Physical materials:** parse source-locked USGS historical workbooks for declared
   commodities. Quantities are national production/consumption observations on the provider's
   commodity-specific basis. They are not allocated to BEA industries, firms, or projects.
15. **Firm funding proxy:** extract annual SEC 10-K Company Facts for a predeclared nonfinancial
   sample. Profit and operating-cash-flow-to-capex ratios, plus signed debt transactions, are
   scale diagnostics. A ratio is not a financing share because refinancing, cash balances,
   equity issuance/repurchase, and timing are not fully observed.
16. **Project payment ledger gate:** record the public-data boundary and restricted-use route for
   invoice/transaction-level payer and purchase records. The gate is deliberately `BLOCKED` until
   approved microdata access and a reproducible ledger are available.

## Evaluation and uncertainty

Rolling-origin forecasts start in 2000. Every transformation and coefficient is fitted only
on data available at each origin. The primary horizon is three years; one and five years are
sensitivities. The predictive-candidate rule was declared before the run: at least 10% lower
median rolling-origin RMSE than every named baseline and a 95% block-bootstrap interval for
squared-error differences below zero. A candidate signal would still leave Claim Class C in
place; the current result is false for every tested horizon.

## What the method does not identify

The design is not a causal estimate of fiat money, the 1971-1973 monetary regime transition,
policy effects, asset superiority, or social stabilization. It is a source-locked diagnostic
architecture that reports both mixed and negative results.
