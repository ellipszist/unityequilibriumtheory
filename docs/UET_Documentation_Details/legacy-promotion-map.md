# Legacy Promotion Map

This file tracks which important ideas from `LEGACY_REPORTS` have already been promoted into
the main documentation layer, and which files should remain archive-first.

Its purpose is simple:

- stop readers from digging through the archive blindly
- preserve provenance from older documents
- separate stable theory summaries from older narrative or exploratory wording

## How to read this map

- `Promoted`: the legacy idea has been lifted into a current main-layer document
- `Summarized`: the legacy file is not copied directly, but its core idea was condensed into a
  newer stable summary
- `Archive-only`: keep for provenance, history, or deeper context, but do not treat as the
  primary current explanation

## Core theory files

| Legacy file | Current status | Main-layer destination | Note |
| :-- | :-- | :-- | :-- |
| `LEGACY_REPORTS/01_Core_Theory/MASTER_EQUATION.md` | Summarized | [03_Core_Theory/master-equation-stable-summary.md](./03_Core_Theory/master-equation-stable-summary.md) | Stable equation form promoted with more conservative wording |
| `LEGACY_REPORTS/01_Core_Theory/Term-by-Term.md` | Summarized | [03_Core_Theory/term-by-term-stable-summary.md](./03_Core_Theory/term-by-term-stable-summary.md) | Term meanings retained; hype and closure claims reduced |
| `LEGACY_REPORTS/01_Core_Theory/PARAMETER_REGISTRY.md` | Summarized | [03_Core_Theory/parameter-registry-stable-summary.md](./03_Core_Theory/parameter-registry-stable-summary.md) | Parameter logic preserved; provenance categories made clearer |
| `LEGACY_REPORTS/01_Core_Theory/THEORY_MAP.md` | Promoted | [03_Core_Theory/theory-lineage-and-sources.md](./03_Core_Theory/theory-lineage-and-sources.md) | Used to explain where the framework draws from |
| `LEGACY_REPORTS/01_Core_Theory/THREE_CORE_TERMS.md` | Summarized | [03_Core_Theory/term-by-term-stable-summary.md](./03_Core_Theory/term-by-term-stable-summary.md) | Folded into the clearer term-level explanation |
| `LEGACY_REPORTS/01_Core_Theory/SCALE_EQUATION.md` | Archive-only | [03_Core_Theory/dimensional-scaling.md](./03_Core_Theory/dimensional-scaling.md) | Related in theme, but not yet fully promoted as a direct stable summary |
| `LEGACY_REPORTS/01_Core_Theory/KAPPA_GUIDE.md` | Archive-only | [03_Core_Theory/parameter-registry-stable-summary.md](./03_Core_Theory/parameter-registry-stable-summary.md) | Important background for `kappa`, but still better treated as historical support |
| `LEGACY_REPORTS/01_Core_Theory/AXIOMATIC_BRIDGE.md` | Archive-only | [03_Core_Theory/axioms-and-principles.md](./03_Core_Theory/axioms-and-principles.md) | Conceptually related, but not yet rewritten as a stable promoted note |
| `LEGACY_REPORTS/01_Core_Theory/MATH_SPECIFICATION.md` | Archive-only | none yet | Candidate source for a future formal math note |
| `LEGACY_REPORTS/01_Core_Theory/SYMBOL_GLOSSARY.md` | Archive-only | none yet | Candidate source for a future glossary cleanup |
| `LEGACY_REPORTS/01_Core_Theory/SINGLE_SOURCE_OF_TRUTH.md` | Archive-only | none yet | Historical governance value, but not core theory-facing for new readers |

## Concept and origin files

| Legacy file | Current status | Main-layer destination | Note |
| :-- | :-- | :-- | :-- |
| `LEGACY_REPORTS/02_Concept/CONCEPTUAL_FRAMEWORK.md` | Promoted | [01_Introduction/origin-and-development.md](./01_Introduction/origin-and-development.md) | Core origin-story material lifted into the main introduction layer |
| `LEGACY_REPORTS/02_Concept/CONCEPTUAL_FOUNDATION.md` | Summarized | [03_Core_Theory/theory-lineage-and-sources.md](./03_Core_Theory/theory-lineage-and-sources.md) | Philosophical structure partly folded into theory lineage |
| `LEGACY_REPORTS/02_Concept/KEY_CONCEPTS.md` | Summarized | [03_Core_Theory/theory-lineage-and-sources.md](./03_Core_Theory/theory-lineage-and-sources.md) | Used as supporting language for the theory-source summary |
| `LEGACY_REPORTS/02_Concept/THEORY_OF_TIME_UET.md` | Archive-only | none yet | Important but specialized; not yet promoted into the current main path |
| `LEGACY_REPORTS/02_Concept/WHY_UNITY.md` | Archive-only | none yet | Useful historical framing, but not needed for first-pass reading |
| `LEGACY_REPORTS/02_Concept/AUTHOR_REFLECTION.md` | Archive-only | none yet | Personal reflection, not normative theory documentation |

## Evidence and scientific posture files

| Legacy file | Current status | Main-layer destination | Note |
| :-- | :-- | :-- | :-- |
| `LEGACY_REPORTS/03_Evidence/CALIBRATION_DECLARATION.md` | Summarized | [03_Core_Theory/correspondence-and-reduction.md](./03_Core_Theory/correspondence-and-reduction.md) | Core anti-fake-calibration posture promoted in a more conservative form |
| `LEGACY_REPORTS/03_Evidence/DOMAIN_MAPPING.md` | Summarized | [04_User_Guides/how-to-use-uet-as-a-system-equation.md](./04_User_Guides/how-to-use-uet-as-a-system-equation.md) | System-to-variable mapping idea promoted in practical form |
| `LEGACY_REPORTS/03_Evidence/DATA_STANDARD.md` | Archive-only | none yet | Superseded in practice by newer standards work under `docs/topics/For Work` |
| `LEGACY_REPORTS/03_Evidence/DATA_SOURCE_MAP.md` | Archive-only | none yet | Useful history, but not a current top-layer source |
| `LEGACY_REPORTS/03_Evidence/GLOBAL_INTEGRITY_LEDGER.md` | Archive-only | none yet | Historical integrity framing, not a first-pass current doc |
| `LEGACY_REPORTS/03_Evidence/PREDICTIONS.md` | Archive-only | none yet | May inform future evidence summaries, but not yet promoted |
| `LEGACY_REPORTS/03_Evidence/PREDICTION_VS_SIMULATION.md` | Archive-only | none yet | Still useful context, not yet stable enough for promotion |

## Analysis files

| Legacy file | Current status | Main-layer destination | Note |
| :-- | :-- | :-- | :-- |
| `LEGACY_REPORTS/07_ANALYSIS/ANALYSIS_The_Stupid_Genius.md` | Summarized | [03_Core_Theory/correspondence-and-reduction.md](./03_Core_Theory/correspondence-and-reduction.md) | The reduction-back-to-known-theory logic was preserved |
| `LEGACY_REPORTS/07_ANALYSIS/ANALYSIS_Natural_Physics.md` | Archive-only | none yet | Still useful philosophical support, but not promoted yet |
| `LEGACY_REPORTS/07_ANALYSIS/ANALYSIS_Hubble_Tension.md` | Archive-only | none yet | Domain-specific and should stay topic-level rather than top-layer |
| `LEGACY_REPORTS/07_ANALYSIS/ANALYSIS_Dark_Matter.md` | Archive-only | none yet | Domain-specific historical analysis |
| `LEGACY_REPORTS/07_ANALYSIS/ANALYSIS_Dark_Energy.md` | Archive-only | none yet | Domain-specific historical analysis |
| `LEGACY_REPORTS/07_ANALYSIS/ANALYSIS_The_Vantage_Point.md` | Archive-only | none yet | Relevant to observer-frame thinking, but not yet promoted |

## Reading rule

If a reader is new to the project, they should prefer the promoted files first:

1. [README.md](./README.md)
2. [01_Introduction/origin-and-development.md](./01_Introduction/origin-and-development.md)
3. [03_Core_Theory/theory-lineage-and-sources.md](./03_Core_Theory/theory-lineage-and-sources.md)
4. [03_Core_Theory/master-equation-stable-summary.md](./03_Core_Theory/master-equation-stable-summary.md)
5. [03_Core_Theory/term-by-term-stable-summary.md](./03_Core_Theory/term-by-term-stable-summary.md)
6. [03_Core_Theory/parameter-registry-stable-summary.md](./03_Core_Theory/parameter-registry-stable-summary.md)
7. [03_Core_Theory/correspondence-and-reduction.md](./03_Core_Theory/correspondence-and-reduction.md)
8. [04_User_Guides/how-to-use-uet-as-a-system-equation.md](./04_User_Guides/how-to-use-uet-as-a-system-equation.md)

Only after that should they dive into `LEGACY_REPORTS` for provenance, variants, or historical
development.
