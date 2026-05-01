# Topic X.XX: [Topic Name]

## Purpose

[State what problem this topic exists to study.]

## When to use

- [New topic]
- [Topic normalization]
- [Readiness review]

## Workflow summary

```mermaid
flowchart LR
    A["Problem"] --> B["Method"]
    B --> C["Data and baseline"]
    C --> D["Results and artifact"]
    D --> E["Limitations and readiness"]
```

## Theory role diagram

Every topic README must include a topic-specific conceptual diagram. Replace this generic
diagram with the actual physical, mathematical, or computational role of the topic.

```mermaid
flowchart TD
    A["Upstream assumptions / constants"] --> B["Core mechanism or equation"]
    B --> C["Verifier / artifact"]
    C --> D["Supported claim class"]
    B --> E["Limitations / open bridge"]
```

## Topic matrix

| Field | Fill with |
| :-- | :-- |
| claim class | hypothesis, model, internal benchmark, external replication |
| baseline | comparator or published reference |
| artifact | result JSON or other reproducibility output |
| readiness | archived, draft, structured, reproducible internally, academic-ready |
| formula status | derived, heuristic bridge, source-locked constant, open |

## Evidence and dependency matrix

Every topic README must include a compact matrix that tells a later reader what makes the
topic strong and what still blocks it.

| Layer | Current status | Evidence path | Main blocker |
| :-- | :-- | :-- | :-- |
| Data | [source-backed / local / placeholder] | `[DATA_MANIFEST.md]` | [missing source/hash/unit/etc.] |
| Formula | [derived / heuristic / open] | `[FORMULA_AUDIT.md]` | [unit/proof/constant gap] |
| Verification | [PASS/WARN/FAIL/absent] | `[VERIFICATION_SPEC.md]`, `[Result/artifacts/...]` | [missing threshold/artifact/etc.] |
| Claim | [A/B/C/D/E] | `[README.md]`, `[METHOD.md]` | [overclaim/open bridge] |
| Dependency | [upstream/downstream topics] | [topic IDs or map] | [unverified dependency] |

## Problem

[Describe the exact scientific or engineering question.]

## Assumptions and scope

- [What is assumed?]
- [What is excluded?]
- [What is the claim boundary?]

## Data sources

- [Local path]
- [DOI or URL]
- [Provenance note]

## Method summary

- Engine: `[path]`
- Proof: `[path]`
- Research script: `[path]`
- Comparator: `[path]`

## Formula and unit registry

| Item | Value |
| :-- | :-- |
| Core relation | [formula or code path] |
| Variable definitions | [list] |
| Unit system | [SI / MeV / GeV / mixed with explicit conversions] |
| Source-locked constants | [list] |
| Heuristic bridges | [list or none] |
| Proof status | [identity / derived / heuristic / open] |

## Parameters and fitting status

- Fixed parameters: [list]
- Tunable parameters: [list]
- Fitting used: [Yes/No]
- If yes, explain where and why.

## Metrics and thresholds

- Metric: [name]
- Threshold: [value]
- Pass condition: [definition]

## Baselines

- [Comparator model or published benchmark]

## Limitations and open risks

- [Limitation 1]
- [Limitation 2]
- [Limitation 3]

## Reproducibility

- Command: `[command]`
- Artifact path: `[Result/artifacts/...json]`

## Current readiness status

Choose one:

- `Archived`
- `Draft`
- `Structured`
- `Reproducible internally`
- `Academic-ready`

## Checklist

- [ ] problem and scope are bounded
- [ ] README has a topic-specific conceptual diagram
- [ ] README has an evidence/status matrix
- [ ] assumptions and exclusions are explicit
- [ ] data and baseline are named
- [ ] formulas, units, and proof status are named
- [ ] metrics and thresholds are defined
- [ ] limitations and readiness are honest
