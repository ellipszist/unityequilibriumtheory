# Research Register — Topic 0.25 Economics

This register is the preregistration contract for the long-term move from `Package Tier A`
to `Evidence Grade A`. It does not promote the topic: the current public boundary remains
`Claim Class C` and `DESCRIPTIVE_DIAGNOSTIC_ONLY`.

The machine-readable source of truth is
[`uet_economics_research_register.json`](Data/03_Research/uet_economics_research_register.json).

## Locked design

- **Scope:** United States first, annual 1959–2024 frozen vintage `2026-07-12`; global
  replication is a later wave and cannot be pooled into the U.S. baseline.
- **Primary outcomes:** resource-capacity index `R`, CPI-U inflation, and real median
  disposable income. Housing, wages, energy, and assets are secondary lanes.
- **Primary diagnostic hypotheses:** the indexed `R/N/K/I` relation and the
  monetary-resource mismatch. Neither is a causal estimate.
- **Selection rule:** proxy/model choices are fixed before holdout results; transformations
  are fitted only at each rolling-origin date; primary evidence has no imputation.
- **Strategy quarantine:** strategy, power, Nash, and social-stabilization notes are
  exploratory and excluded from the core economics evidence package until intervention data,
  measured outcomes, identification, and independent replication exist.

## Ten-wave sequence

| Wave | Focus | Current state | Exit condition |
|---:|---|---|---|
| 0 | Research constitution and preregistration | In progress | No post-hoc proxy/model selection |
| 1 | U.S. source closure and vintage control | In progress | Identity, release, terms, hash, coverage, and revision fields complete |
| 2 | Measurement validity of `R/N/K/I` | Planned | Three proxy families and measurement-error sensitivity |
| 3 | Cost-of-living and household welfare | Planned | Real welfare and burden outcomes separate from GDP |
| 4 | Money, credit, and inflation | Planned | Money definitions, credit measures, baselines, causal candidates separated |
| 5 | Wage, productivity, and distribution | Planned | EPI/BLS/ILOSTAT constructions remain separate and decomposed |
| 6 | Energy transition and literal density | Planned | Common heat-content basis and uncertainty locked |
| 7 | Markets, assets, and purchasing power | Planned | Licensed total-return/asset provenance closes or lane is quarantined |
| 8 | Global replication | Planned | 30+ economies, common coverage, PPP policy, leave-one-out checks |
| 9 | Causal identification, external rerun, publication | Planned | Two independent designs, independent rerun, human review |

## Current decision rule

The topic remains at `Package Tier A` only. A controlling WARN gate is not averaged away:
the evidence-grade aggregate stays `WARN` until source/revision/license/unit/measurement,
missingness/leakage, baseline, causal, external, and publication requirements are actually
closed. A negative or mixed result is a valid research result and does not justify stronger
wording.
