---
title: "Parameter Registry Stable Summary"
description: "Conservative summary of the legacy UET parameter layer and how it should be interpreted today."
---

# Parameter Registry Stable Summary

This note promotes the most stable parts of the legacy parameter-registry material into the
current documentation layer.

It is intentionally stricter than the historical registry.

## Why this note exists

The legacy registry is important because it shows the intended logic behind core parameters.

But some historical wording is too strong to be reused directly without review.

This summary keeps the useful structure:

- which parameters matter
- what role they play
- which ones were meant to be scale-dependent
- what the anti-fitting rule was supposed to mean

## Core parameters

| Symbol | Stable role | Legacy interpretation | Current caution |
| :-- | :-- | :-- | :-- |
| `κ` | gradient penalty / stiffness / smoothing cost | linked to geometry, bounds, and scale regime | should not be assumed universal across all domains |
| `β` | coupling strength between capacity-like and information-like terms | Landauer/information-energy link | topic-specific use must be documented clearly |
| `γ_J` | exchange-rate factor | semi-open thermodynamic exchange | often more structural than directly source-locked |
| `W_N` | persistence or action-like drive term | natural-will / descent-like drive | conceptually important, formally soft |
| `λ` | coherence coupling across layers | multi-layer sync / unity term | requires explicit subsystem meaning |

## Scale dependence

One of the most important legacy claims is that at least some UET parameters, especially
`κ`, are **scale-sensitive** rather than globally fixed.

That idea should be preserved.

The safe current wording is:

- different regimes may require different effective parameter layers
- those regime changes must be documented explicitly
- regime dependence must not be confused with ad hoc per-topic fitting

## The intended anti-fitting rule

The most valuable part of the old registry is the anti-fitting discipline.

The intended rule was roughly:

1. derive from first principles where possible
2. calibrate once on independent data where necessary
3. relate parameters across scales or domains where justified
4. do not quietly retune per benchmark just to make results look good

That principle still matters and should survive into current standards language.

## Safe modern interpretation

The current safe interpretation is:

- some parameters are best treated as source-locked physical constants
- some are topic runtime parameters
- some are scale-regime parameters
- some are still heuristic bridges and should be labeled that way

So the registry should be read as a **discipline of parameter handling**, not as proof that
every historical parameter value is already final.

## What should be carried forward

- parameter provenance matters
- scale dependence matters
- anti-fitting discipline matters
- parameter changes must be declared, not hidden

## What should not be carried forward without review

- old topic-by-topic status flags as if they still reflect the current repo
- claims that all values are already permanently settled
- claims that every parameter is already fully first-principles derived

## Reading rule for current topics

When reading a topic now, ask:

- is this value source-locked?
- is it a runtime topic parameter?
- is it a scale-regime choice?
- is it a benchmark anchor?
- is it still heuristic?

That is the bridge between the legacy registry and the current repo-first standards.

## Legacy source behind this note

- `LEGACY_REPORTS/01_Core_Theory/PARAMETER_REGISTRY.md`
