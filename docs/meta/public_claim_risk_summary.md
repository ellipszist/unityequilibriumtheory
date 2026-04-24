# Public Claim Risk Summary

This summary tracks pages whose public wording is stronger than the current evidence package.

It is a triage tool, not a final scientific judgment. A flagged page is not automatically
wrong; it means the page currently communicates more certainty or completeness than the repo
audit can support.

## Repo-level risk

### `docs/topics/README.md`

High-risk issues detected in the previous landing page version:

- described the collection as `31 Pillars of Truth` even though the repo currently has `40` numbered topic directories
- used summary badges such as `150+ Scripts` and `Physics-Unified` without tying them to canonical metadata
- marked many topics as effectively passed or complete despite metadata and structure showing most are still `Draft`
- described a `Triple-Green` standard that the majority of topics do not satisfy in the current repo state
- mixed future concepts with theory-core topics in a way that overstated the current evidence-bearing scope of the project

## High-risk topic pages

These topic READMEs most clearly combine strong language with incomplete standards packaging:

| Topic | Why it is risky now |
| :-- | :-- |
| `0.5_Nuclear_Binding_Hadrons` | strong wording such as `solved`, `exact`, `PASS`, and `unified` appears before a standards-grade method package exists |
| `0.8_Muon_g2_Anomaly` | anomaly-resolution language is stronger than the current verification framing |
| `0.17_Mass_Generation` | claim language suggests stronger proof and certainty than the repo can currently audit |
| `0.18_Mathnicry` | proof-heavy language appears without a documented proof boundary or case-coverage package |
| `0.21_Yang_Mills_Mass_Gap` | structured topic, but public wording still risks overstatement relative to internal-only support |

## Medium-risk topic pages

These pages use badges or assertive wording that should be downgraded until standards migration
is complete:

- `0.0_Grand_Unification`
- `0.3_Cosmology_Hubble_Tension`
- `0.10_Fluid_Dynamics_Chaos`
- `0.11_Phase_Transitions`
- `0.12_Vacuum_Energy_Casimir`
- `0.14_Complex_Systems`
- `0.16_Heavy_Nuclei`
- `0.19_Gravity_GR`
- `0.25_Strategy_Power_Economics`
- `0.26_Cosmic_Dynamic_Frame`
- `0.30_Mega_Flora_Biotech`
- `0.31_SpaceTime_Propulsion`

Common pattern:

- pass badges or percentages appear without audit-grade verification specs
- `proof` wording appears without method boundary documentation
- application topics are presented as if they were already physics-validated research packages

## Audit policy for future rewrites

- do not use `Solved`, `Verified`, `exact`, `100%`, `PASS`, or `unified` unless the topic has a standards-grade evidence package that explicitly supports the term
- do not let badge language outrun `topic_readiness.json`
- when in doubt, downgrade to wording such as `internal benchmark`, `draft mechanism`, `research workflow`, or `exploratory topic`
- do not use topics `0.27-0.38` as evidence for the current theory-core until they are explicitly promoted out of `future_concept` scope
