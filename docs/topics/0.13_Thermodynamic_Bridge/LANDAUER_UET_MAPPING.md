# Landauer-to-UET Mapping

## Purpose

This file answers a narrow but important question:

What, exactly, does `0.13` currently show about a UET mapping to the Landauer lower bound?

It is intentionally stricter than legacy paper-draft language.

## Current status

`imported_constraint_not_noncircular_uet_derivation`

That means:

- the topic does support Landauer as a source-backed lower-bound constraint
- the topic does not yet support a non-circular UET derivation of that lower bound

## What the current code actually does

Current engine surface:

- `Code/01_Engine/Engine_Thermodynamics.py::get_landauer_limit`

Current relation used there:

```python
return k_B * T_K * np.log(2) * (self.params.beta / self.params.beta)
```

Current reading:

- the output is exactly the standard Landauer form
- a `beta` symbol appears in the path
- but `beta / beta` cancels algebraically
- so the current path does **not** expose a nontrivial UET-dependent scaling in this lane

## What is supported now

| Claim | Supported now? | Why |
| :-- | :-- | :-- |
| Landauer lower bound is reproduced numerically | yes | verifier matches exact-constant CODATA expression |
| measured summary values remain above the lower bound | yes, conservatively | current benchmark lane checks lower-bound non-violation |
| UET derives the lower bound from first principles | no | current path imports the standard formula directly |
| beta term adds tested thermodynamic structure in this lane | no | current engine expression cancels beta out |

## Evidence split

### Imported standard constraint

- `T13-004`
- `Research_Landauer.landauer_energy`
- current verifier artifact reports zero relative error against the exact-constant CODATA expression

This is good evidence for a constraint lane.

### UET-added structure

Current status:

- not established in this lane

Reason:

- no artifact currently distinguishes the imported lower bound from a genuinely UET-generated correction or derivation

## Forbidden overreads

- Do not say UET derives Landauer from first principles based on the current engine path.
- Do not treat the presence of the symbol `beta` as proof of a thermodynamic bridge.
- Do not treat perfect agreement with the standard formula as evidence that a UET-specific mechanism has been added.

## What would strengthen this next

1. State whether `beta` in this lane is meant to be a derived bridge coefficient, a normalization tag, or only a placeholder.
2. If this lane is only a boundary condition, document that explicitly and keep the claim at the constraint level.
3. If UET is supposed to add structure here, implement a nontrivial mapping that can be tested against the imported lower bound without circular reuse.

## Artifact link

The machine-readable version of this mapping status is:

- [landauer_uet_mapping.json](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/landauer_uet_mapping.json:1)

It should stay aligned with:

- [DERIVATION_MAP.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.13_Thermodynamic_Bridge/DERIVATION_MAP.md:1)
- [UNITS_CONTRACT.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.13_Thermodynamic_Bridge/UNITS_CONTRACT.md:1)
- [FORMULA_AUDIT.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.13_Thermodynamic_Bridge/FORMULA_AUDIT.md:1)
