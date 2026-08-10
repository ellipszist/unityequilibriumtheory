# Book 1 Blueprint: The Origin of Wealth

> **Book ID:** `0.1_origin_of_wealth`
> **Section:** `section_economics_ai_energy`
> **Blueprint version:** `book1-economics-v2-research-reset`
> **Status:** `PROVISIONAL / IN_PROGRESS`
> **Evidence boundary:** hypotheses, definitions, and research architecture; not an economic law or policy validation

## Book promise

The book asks how societies convert labor, energy, materials, knowledge, capital, and institutional coordination into output, wealth, and welfare—and how money and credit allocate claims on that process. It preserves the original intuition that financial claims must ultimately interact with a real productive system, while refusing to treat money, physical energy, accounting value, and social power as the same quantity.

## Reader outcomes

After reading, the reader should be able to:

1. distinguish output, wealth, welfare, money, credit, payments, and physical throughput;
2. follow a payment from a funding channel as far as the available evidence permits;
3. understand why an accounting identity is not automatically a causal theory;
4. compare the Book's hypotheses with standard production, monetary, labor, and energy frameworks;
5. identify which historical claims are established, contested, or speculative;
6. see exactly what Book 1 hands to the AI analysis in Book 2 and the monetary-design tests in Book 3.

## Scientific contract

### Controlled ontology

| Symbol | Construct | Type | Typical unit |
| --- | --- | --- | --- |
| `Y` | real output/value added | flow | chained currency per time or quantity index |
| `W` | comprehensive wealth | stock | real currency or physical component vector |
| `Kp` | produced capital/infrastructure | stock/service | real currency stock or capital-service index |
| `H` | human and knowledge capital | stock/proxy | education, R&D stock, IP, or patent-quality measure |
| `L` | labor services | flow | hours or quality-adjusted hours |
| `E` | energy service/exergy | flow | joule, exergy unit, or service index per time |
| `X` | material/natural-resource throughput | flow | mass or volume per time |
| `A` | technology, institutions, organization | residual/state | declared index or estimated productivity |
| `C` | constraint or shock | event/exposure | shock-specific unit |
| `M^j` | declared money aggregate | stock | currency |
| `Cr` | credit/debt | stock or flow as labelled | currency or currency per time |
| `T` | transaction/expenditure | flow | currency per time |
| `P^{b,g}` | price index for basket `b`, group `g` | index | dimensionless |
| `F` | financing flows | flow | currency per time |

+`R=N+K+I` is retained only as `BOOK-HEURISTIC-001`, status `RETIRED_AS_IDENTITY`. The letters must not be reused as a hidden alternative ontology.

### Money-value decomposition

There is no single observed scalar called the value of money. Book 1 separates:

- internal basket purchasing power: `PP^{b,g}_t=P^{b,g}_0/P^{b,g}_t`;
- external exchange value: bilateral FX or real effective exchange rate;
- payment acceptance and use: transaction count/value by payment instrument;
- store-of-value performance: horizon-specific real returns and drawdowns;
- resource coverage: an exploratory scarcity diagnostic, never an observed value identity.

### Benchmark models

Production and growth accounting:

\[
\Delta\ln Q_{i,t}=\sum_{x\in\{K,L,E,M,S\}}\bar{s}_{x,i,t}\Delta\ln X_{x,i,t}+\Delta\ln A_{i,t}
\]

Production network and modelled resource footprint:

\[
x=(I-A)^{-1}f,\qquad q=B(I-A)^{-1}f
\]

Innovation under constraints:

\[
Innovation_{t+h}=g(C_t,H_t,R\&D_t,Kp_t,Finance_t,Institutions_t)+\epsilon_{t+h}
\]

Money accounting identity:

\[
M_tV_t=P_tY_t
\]

Infrastructure accumulation and social value:

\[
K^I_{t+1}=(1-\delta)K^I_t+I_t
\]

\[
NPV_{social}=-CapEx+\sum_h\frac{Benefits_h-O\&M_h-ExternalCosts_h}{(1+\rho)^h}+\frac{ResidualValue_T}{(1+\rho)^T}
\]

Exergy destruction, only with a declared system boundary and reference environment:

\[
B_{destroyed}=T_0S_{generated}
\]

## Chapter architecture

### Chapter 1 — What wealth is and is not

**Purpose:** separate real output, wealth stock, welfare, natural capital, liquidity, and financial claims.

**Owned claims:** `B1-C001`, `B1-C002`, `B1-C003`.

**Key questions:**

- What does GDP measure, and what does it omit?
- How do produced, human, natural, and financial assets differ?
- When is a service real output even without a tangible product?

**Boundary:** GDP may be incomplete as welfare; it is not therefore an illusion.

### Chapter 2 — The economy as an open production system

**Purpose:** explain how labor, capital, energy, materials, services, knowledge, and institutions transform inputs into outputs.

**Owned claims:** `B1-C004`, `B1-C005`, `B1-C006`.

**Research backbone:** BEA–BLS KLEMS, BEA input-output accounts, EIA, USGS, Commodity Flow Survey, and USEEIO.

**Boundary:** input-output footprints are average/modelled supply-chain links, not observed causal paths from an individual payment.

### Chapter 3 — Constraints, knowledge, infrastructure, and innovation

**Purpose:** replace the additive `N+K+I` identity with testable, sign-ambiguous mechanisms.

**Owned claims:** `B1-C007`, `B1-C008`, `B1-C009`.

Constraints may stimulate search or destroy capacity. Knowledge uses multiple measures. Infrastructure is evaluated through services, utilization, depreciation, delays, externalities, and social/fiscal NPV.

### Chapter 4 — Money, payments, credit, and fiscal flows

**Purpose:** explain deposit creation, payment settlement, sectoral sources-and-uses, inflation transmission, and why money lineage is often unobservable.

**Owned claims:** `B1-C010` through `B1-C015`.

The “Stone in the Balloon” remains as a clearly labelled thought experiment: if a selected money aggregate doubles while real transactions, output, money demand, velocity, expectations, and all relative-price mechanisms are fixed, the identity implies a changed price level. Those assumptions do not hold automatically, so the metaphor is not a law or causal result.

Funding classifications are empirical, not moral binaries. Secured debt is not automatically productive; unsecured credit is not automatically unproductive.

### Chapter 5 — Productivity, wages, distribution, and cost of living

**Purpose:** distinguish mean and median pay, wages and compensation, output and consumer deflators, labor share, wealth distribution, housing burden, and household-specific purchasing power.

**Owned claims:** `B1-C016` through `B1-C020`.

EPI, BLS, BEA, CPS, CE, SCF/DFA, QCEW, and international sources remain separate constructions. The book must not attribute their divergence to fiat policy without an identified design.

### Chapter 6 — Firms, market power, SMEs, and time

**Purpose:** test upstream concentration, buyer power, markups, cost pass-through, firm size, entry/survival, wage formation, and leisure/time-use channels.

**Owned claims:** `B1-C021` through `B1-C025`.

SME shares require country/year/definition/denominator. Government can employ people directly; comparative policy claims must specify outcomes and counterfactuals. Leisure may raise market services, household production, or neither.

### Chapter 7 — Energy, materials, environment, and bounded history

**Purpose:** separate heat content, throughput, efficiency, useful energy, exergy, EROI, emissions, and natural-capital depletion; review historical claims with evidence tiers.

**Owned claims:** `B1-C026` through `B1-C032`.

Fire/cooking/storage/fuel collection are treated as potentially co-evolving. “Firewood was the first industry,” “the first war destroyed wood stores,” and “mathematics preceded speech to manage fuel” remain quarantined. Gold-standard and Great Depression history must include monetary contraction, banking crises, and international transmission rather than a single output/gold story.

“Profit is unpaid entropy” is retired as an identity. The testable replacement compares private financial returns with separately measured environmental and social externalities.

### Chapter 8 — What Book 1 establishes and hands off

**Purpose:** report supported, unsupported, and unresolved claims without prescribing the next books' conclusions.

Book 2 receives production, labor, ownership, market-power, welfare, and measurement definitions for evaluating AI divergence.

Book 3 receives design requirements and failure modes for any energy/resource monetary proposal: convertibility, oracle governance, volatility, procyclicality, liquidity, distribution, transition, legal authority, and attack resistance. Book 1 does not claim that Dynamic Energy Money is validated or inflation-free.

## Historical and policy quarantine

The following may appear only in boxed speculative interludes or research appendices until their specialist gates pass:

- firewood as the first industry or target of the first war;
- mathematics before spoken language;
- a single Nile origin for geometry;
- zero caused by one philosophical doctrine or transmitted principally by the Crusades;
- fiat money as the sole cause of wage divergence, asset ownership, or union decline;
- fertility decline as an intentional design of powerful groups;
- Singapore/Hong Kong motives inferred from gold-market status;
- Thailand labor tiers defined by nationality;
- a Balanced Market, Nash arrangement, or monetary peg as already superior.

## Evidence and wording boundary

Allowed language: `hypothesis`, `proposal`, `model`, `descriptive finding`, `accounting bridge`, `internally reproduced`, `did/did not outperform the declared baseline`.

Blocked without later evidence: `law`, `proved`, `fiat caused`, `validated peg`, `inflation-free`, `policy success`, `strategic superiority`, `universal equilibrium`.

## Entry and exit conditions

**Entry:** Section S02 is recorded; Topic 0.25 provides source-locked internal diagnostics.

**Exit:** Book 1 cannot lock at W05 until the systematic literature review, source digest, claim map, formula registry, contrary-evidence review, and Topic-to-Book version gate pass. Publication remains blocked until W10–W17 and human review.
