# Book 1 Research Specification

> **Version:** `BOOK1-RS-V3`
> **Status:** `IN_PROGRESS`
> **Blueprint:** `book1-economics-v2-research-reset`
> **Topic implementation:** `docs/topics/0.25_Strategy_Power_Economics`

## Primary research questions

1. Do physical inputs, labor, capital services, knowledge, and institutions explain output and productivity in ways consistent with standard KLEMS and production-network accounts?
2. Do predeclared UET-inspired variables add out-of-sample information beyond those standards?
3. How should internal purchasing power, external exchange value, payment use, and store-of-value performance be measured separately?
4. Through which monetary, credit, fiscal, and supply channels do identified shocks affect prices, output, wages, assets, and distribution?
5. What can public data observe about payer, funding source, expenditure, labor, and physical-resource transformation—and where is lineage unobservable?
6. How do productivity, compensation, labor share, inequality, market power, household baskets, and time use relate?
7. Which energy and historical claims survive unit closure, source appraisal, contrary evidence, and specialist review?

## Formula registry contract

### Retired heuristic

`BOOK-HEURISTIC-001: R=N+K+I` is a narrative mnemonic only. It has no unit closure and must not be fitted or described as a wealth equation.

### Production benchmark

`EC25-PRODUCTION-KLEMS`:

\[
\Delta\ln Q_{i,t}=\sum_x \bar s_{x,i,t}\Delta\ln X_{x,i,t}+\Delta\ln A_{i,t}
\]

### Innovation family

`EC25-INNOVATION-CONSTRAINT`:

\[
Innovation_{t+h}=g(C_t,H_t,R\&D_t,Kp_t,Finance_t,Institutions_t)+\epsilon_{t+h}
\]

The sign of `C` is not constrained.

### Purchasing power

`EC25-MONEY-PP`:

\[
PP^{b,g}_t=P^{b,g}_0/P^{b,g}_t
\]

### Monetary identity and empirical candidate

`EC25-MONEY-IDENTITY: MV=PY` is an ex-post identity when velocity is defined residually. Causal work uses identified shocks and must not treat observed M2 growth as exogenous.

### Production network

`EC25-IO-FOOTPRINT`:

\[
x=(I-A)^{-1}f,\qquad q=B(I-A)^{-1}f
\]

### Funding sources and uses

Firm:

\[
InternalCash+NetDebt+NetEquity+Transfers=Investment+WorkingCapital+Payouts+\Delta Cash+Residual
\]

Household and government accounts use corresponding declared sector identities. Individual-dollar lineage requires a tagged ledger.

### Infrastructure and exergy

Infrastructure capital accumulation, social NPV, fiscal NPV, and debt service are separate calculations. Exergy destruction uses `B_destroyed=T0*S_generated` only with SI units and declared boundaries.

## Evidence architecture

`L0` official macro → `L1` sector accounting → `L2` public partial transactions → `L3` restricted matched microdata → `L4` tagged payment/invoice/resource ledger.

Each result is labelled `OBSERVED`, `ACCOUNTING_INFERRED`, `MODEL_ALLOCATED`, or `UNOBSERVED`.

## Evaluation policy

- U.S.-first; annual macro baseline remains frozen at 1959–2024.
- No silent imputation in primary evidence.
- Transformations are fitted using training information only.
- Exact metrics are named correctly; RMSE is the square root of mean squared error.
- Moving-block bootstrap samples blocks with replacement using a recorded seed.
- Baselines include appropriate autoregressive, standard production, expectations/slack, and no-change models by lane.
- Multiple testing is controlled within predeclared claim families.
- Causal language requires pre-trends, placebo/negative controls, sensitivity checks, and two identification strategies with materially different assumptions.

## Permanent claim boundaries

A negative result is publishable. An internal rerun is not external validation. A modelled footprint is not transaction lineage. A successful forecast is not causal identification. A project or monetary design remains a proposal until independently evaluated.
