# Roadmap: Package Tier A → Evidence Grade A

## Status

Topic 0.25 is currently a standards-complete `Package Tier A` package with `Claim Class C`
and aggregate `WARN`. `Evidence Grade A` is a future target, not a current status. The
roadmap is U.S.-first and only opens the global lane after the U.S. measurement package is
stable. Strategy/Power/Nash/Social Stabilization remains a quarantined exploratory lane.

## Ten research waves

1. **Research constitution and preregistration:** register primary/secondary/exploratory
   hypotheses, outcomes, DAG, proxy families, holdout and no-imputation policy.
2. **U.S. source closure and vintage control:** lock FRED/H.6, BEA, BLS, EIA, FHFA, Census,
   Fed/SCF/DFA, USPTO/PatsView, and terms/release/hash/as-of metadata for each input.
3. **Measurement validity:** compare geometric, standardized-additive, and latent/PCA
   `R/N/K/I` families; test reliability, measurement error, invariance, double counting, and
   structural breaks.
4. **Cost of living and household welfare:** add CPI components, rent/OER, housing burden,
   real median wages/income, consumption baskets, and regional/state distributions.
5. **Money, credit, and inflation:** add broad money, velocity, bank/household/corporate/
   government credit, debt service, fiscal issuance, policy surprises, and separate
   descriptive from causal designs.
6. **Wage, productivity, and distribution:** reproduce EPI, compare BLS, add median/mean,
   labor share, quantiles, industry/hours controls, ILOSTAT/OECD robustness.
7. **Energy transition and literal density:** separate throughput, efficiency/productivity,
   and heat-content density; lock MJ/kg or equivalent basis and uncertainty.
8. **Markets, assets, and purchasing power:** acquire licensed S&P total-return/CRSP and
   LBMA data; compare real returns, drawdowns, rolling retention, and tracking error.
9. **Global replication:** build a 30+ economy, 20+ year common panel using WDI, OECD,
   ILOSTAT, IMF, BIS, WID, and historical robustness sources with PPP/exchange-rate lanes.
10. **Causal identification, external rerun, publication:** require pre-trends/placebos/
    negative controls/weak-IV checks, two independent designs, independent code rerun,
    replication report, and human review.

## Data and model contract

```text
raw provider archive
  → source manifest + release/revision/hash lock
  → canonical annual panel
  → unit/coverage/measurement gates
  → preregistered features
  → baseline + robustness + causal candidates
  → HAC/block-bootstrap uncertainty
  → independent replication artifact
  → claim gate and publication review
```

The current formulas are operational diagnostics:

- `Δln(R[t+3]) = α + βN N[t] + βK Δln(K[t]) + βI Δln(I[t]) + ε[t]`;
- `D[t] = Δln(M2[t]) − Δln(R[t])`;
- `gap[t] = ln(productivity[t]) − ln(compensation[t])`;
- welfare and asset paths are real, explicitly deflated, and separately reported.

## Source families

The U.S. package is anchored to [Federal Reserve/FRED](https://fred.stlouisfed.org/series/M2SL),
[BEA](https://www.bea.gov/data/gdp/gross-domestic-product),
[BLS](https://www.bls.gov/productivity/),
[EIA](https://www.eia.gov/totalenergy/data/annual/),
[FHFA](https://www.fhfa.gov/data/hpi),
[Census/Fed distributional accounts](https://www.federalreserve.gov/releases/z1/),
[USPTO/PatsView](https://www.uspto.gov/ip-policy/economic-research/patentsview),
[LBMA](https://www.lbma.org.uk/prices-and-data), and licensed [S&P/CRSP](https://www.spglobal.com/spdji/en/).
Global candidates are [World Bank WDI](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392),
[OECD](https://www.oecd.org/en/data/datasets/gdp-and-non-financial-accounts.html),
[ILOSTAT](https://ilostat.ilo.org/topics/labour-productivity/),
[IMF](https://data.imf.org/Datasets/CPI), [BIS](https://www.bis.org/statistics/dataportal/credit.htm),
and [WID](https://wid.world/methodology/), with Penn World Table/Maddison as historical
robustness rather than a replacement for official current accounts. Raw provider files belong
under docs/data/external/economics/us_historical/<provider>/<retrieval-vintage>/ or the later
global equivalent; topic-local normalized panels belong under Data/03_Research/.

## Evidence-grade acceptance

All twelve WARN gates are machine-readable in
[`uet_economics_warn_gate_registry.json`](Data/03_Research/uet_economics_warn_gate_registry.json).
Evidence Grade A requires critical source/unit/missingness/leakage gates to pass, stable
constructs across at least three operationalizations, two independent U.S. causal designs,
global 30+ economy robustness, a successful independent rerun, and human sign-off. Mixed or
negative results remain valid; they do not authorize stronger claims.
