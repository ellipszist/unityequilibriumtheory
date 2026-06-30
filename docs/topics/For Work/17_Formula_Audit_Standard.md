# Formula Audit Standard

This guide defines how UET topics must document formulas, constants, units, and proof
status before scientific wording is promoted.

## Purpose

Make every important calculation auditable.

A reviewer should be able to answer:

- what is being computed
- which variables are used
- what units they carry
- where each constant came from
- whether the relation is derived, heuristic, benchmark-fed, or still open

## When to use

Use this file when:

- a topic contains scientific equations or calculation paths
- a constant appears in code without an obvious provenance trail
- a topic moves from draft notes into a structured topic
- AI or humans are rewriting method sections
- a bug suggests a unit mismatch or hidden assumption

## Workflow summary

```mermaid
flowchart TD
    A["Inspect engine and verifier code"] --> B["List main formulas"]
    B --> C["Record variables, units, conversions"]
    C --> D["Label each constant origin"]
    D --> E["Assign proof status"]
    E --> F["Link formula entries to METHOD, README, and verifier"]
    F --> G{"Any open gap left?"}
    G -->|Yes| H["Write limitation and keep status conservative"]
    G -->|No| I["Promote as structured formula package"]
```

## Formula audit matrix

| Field | Required question |
| :-- | :-- |
| `formula_id` | what calculation path is this entry tracking? |
| `relation` | what exact formula or pseudo-formula is used? |
| `variables` | what does each symbol mean physically and mathematically (e.g., continuous field, tensor, scalar)? |
| `units` | what units must each dimensional quantity use? |
| `unit_closure_status` | does the dimensional analysis balance exactly (Closed), use proxy units (Proxy), or remain unproven (Open)? |
| `conversion_steps` | where do units change and how? |
| `constant_origin` | source-locked constant, derived term, heuristic bridge, or benchmark anchor? |
| `proof_status` | identity, derived, checked local, heuristic, or open? |
| `verification_role` | gate, benchmark input, diagnostic-only, or exploratory? |
| `failure_mode` | what breaks if this term is wrong? |
| `next_hardening_step` | what would improve scientific confidence next? |

## Standard proof-status vocabulary

| Status | Meaning |
| :-- | :-- |
| `identity` | algebraic identity or exact definition |
| `source-locked constant` | externally sourced constant with declared provenance |
| `derived` | relation is derived inside current topic logic and documented |
| `checked local` | locally curated reference checked against a source |
| `heuristic bridge` | structured bridge term exists but is not yet first-principles closed |
| `benchmark anchor` | fixed benchmark value used for comparison or normalization |
| `open` | topic still lacks a justified derivation or provenance path |

## Allowed constant-origin classes

| Class | Use when |
| :-- | :-- |
| `source_locked_physics_constant` | PDG, CODATA, NuFIT, DOE, or equivalent upstream value |
| `source_locked_benchmark_input` | externally published comparator used in verification |
| `topic_derived_relation` | relation produced by topic logic and documented in METHOD |
| `checked_local_reference` | local package checked against a source but not directly machine-mapped |
| `heuristic_bridge` | bridge/correction factor exists but still needs derivation |
| `benchmark_anchor` | fixed value used to stabilize a comparison layer |
| `open_placeholder` | unresolved term that must not be hidden |

## Minimum output for a structured topic

At minimum, a topic with scientific code should have:

- `METHOD.md`
- `VERIFICATION_SPEC.md`
- `LIMITATIONS.md`
- `FORMULA_AUDIT.md` or an equivalent dedicated formula registry

## Required entry pattern

Every important formula entry should state:

1. the calculation path
2. the variables and their exact physical/mathematical meaning
3. the unit system
4. the unit closure status (Dimensional Analysis)
5. the conversion steps
6. the origin class of constants
7. the proof status
8. the verification role
9. the current limitation

## Example decision table

| Situation | Allowed label | Not allowed |
| :-- | :-- | :-- |
| PDG mass copied into engine | `source-locked constant` | `derived` |
| local reference cross-checked manually | `checked local` | `source-locked constant` |
| correction factor exists with physical story but no derivation | `heuristic bridge` | `proved` |
| baseline value normalizes a decay relation | `benchmark anchor` | `fundamental constant` |
| formula has unresolved unit path | `open` with limitation | silent omission |

## Key rules

- No important formula should remain undocumented once a topic is `Structured`.
- Units must be explicit whenever dimensional quantities appear.
- Unit closure (Dimensional Analysis) must balance, or the status must explicitly be marked as `Open`.
- Variables must have clear mathematical and physical definitions, not just casual prose.
- Hidden benchmark anchors are not allowed.
- Heuristic bridges are allowed only when labeled honestly.
- A formula registry must map back to real code or artifacts.

## Common failure modes

- a constant is treated like a derivation because it gives good output
- units are implicit in code comments but not written in docs
- a benchmark anchor is mistaken for a first-principles constant
- README language sounds stronger than the formula registry supports
- AI turns a desired mechanism into a pseudo-derivation without exposing the gap

## Checklist

- [ ] main formulas are listed explicitly
- [ ] variables are defined mathematically and physically
- [ ] units are defined and Unit Closure is verified
- [ ] conversion steps are written down
- [ ] constants are labeled by origin class
- [ ] proof status is assigned honestly
- [ ] each important formula has a failure mode and next hardening step
