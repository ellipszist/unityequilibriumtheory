---
title: "Master Equation Stable Summary"
description: "A conservative technical entrypoint for the promoted UET master-equation structure."
---

# Master Equation Stable Summary

This note is the technical entrypoint for the currently promoted UET master-equation
structure.

It is intentionally conservative.

Its goal is to explain what the repository is currently treating as the most stable core
functional template, how to read its variables and terms, how it maps to the code, and where
formal closure is still incomplete.

It should be read together with the companion notes:

- [term-by-term-stable-summary.md](./term-by-term-stable-summary.md)
- [parameter-registry-stable-summary.md](./parameter-registry-stable-summary.md)
- [correspondence-and-reduction.md](./correspondence-and-reduction.md)
- [uet-term-activation-rules.md](./uet-term-activation-rules.md)

## Current promoted equation form

The most stable legacy form repeatedly carried forward in the repo is the following 7-term
functional:

$$
\Omega[C,I,J] =
\int d^3x \left[
V(C)
+ \frac{\kappa}{2}|\nabla C|^2
+ \beta C \cdot I
+ \gamma_J (J_{in} - J_{out}) \cdot C
+ W_N |\nabla \Omega|
+ \beta_U V_{game}
+ \lambda \sum (C_i - C_j)^2
\right]
$$

## What this equation is trying to do

The repository uses this functional as a candidate umbrella structure for describing:

- equilibrium and disequilibrium cost
- spatial or state variation cost
- information-energy coupling
- semi-open exchange with surroundings
- persistence or path-following drive
- strategic interaction in adaptive multi-agent systems
- coherence across coupled layers or subsystems

This does **not** imply that every topic implements all seven terms directly.

It does **not** imply that every term is already first-principles closed in the current
repository.

The stable claim is narrower:

**The 7-term functional is the main promoted legacy template for the intended UET core
structure.**

## Variable framing

The core variables should be read as structural placeholders whose operational meaning can
change by topic.

| Symbol | Generic technical role | Typical question a topic must answer |
| :-- | :-- | :-- |
| `C` | primary state or capacity-like field | What is the main state variable being evolved? |
| `I` | information-like, entropy-like, or hidden-structure field | What information-like quantity is coupled into the state? |
| `J` | flow or exchange layer | What is entering or leaving the system? |
| `\Omega` | total disequilibrium / action-like / cost functional | What quantity is being minimized, descended, or regulated? |

In the current repo, `C`, `I`, and `J` are **not** globally fixed to one physical meaning.
Each serious topic should declare its local mapping explicitly.

## Domain of integration and mathematical level

The promoted equation is written as a continuum functional over `d^3x`.

That should currently be read as the **default legacy presentation**, not as proof that every
implementation in the repo uses a fully continuous three-dimensional field theory.

Depending on the topic, the practical implementation may instead operate on:

- a 1D grid
- a 2D grid
- a reduced state vector
- a coarse scalar observable
- a subsystem-level metric bundle

So the current safe interpretation is:

- the legacy equation is a continuum-style template
- topic implementations may use reduced or discretized versions
- a topic should state clearly when it is using a reduced form rather than the full field form

## Units and dimensional status

A reader should be careful not to assume that the full promoted functional already has one
fully closed universal unit system across all topics.

Current technical posture:

| Element | Current status |
| :-- | :-- |
| `V(C)` | topic-dependent potential; unit meaning depends on the topic state choice |
| `\kappa` | gradient penalty / stiffness parameter; scale-sensitive in current interpretation |
| `\beta` | coupling term intended to connect information-like and capacity-like quantities |
| `\gamma_J` | exchange-rate factor for open or semi-open systems |
| `W_N` | persistence term with the softest formal closure |
| `\beta_U` | interaction or game-layer coefficient; strongest in higher-level adaptive systems |
| `\lambda` | coherence penalty across layers/subsystems |

The repo does contain topic- and code-level parameter conventions, but the public stable claim
should remain:

**full cross-domain dimensional closure is still incomplete and must be documented per topic or
per code surface.**

## The seven promoted terms

| Term | Symbol | Intended role | Current caution |
| :-- | :-- | :-- | :-- |
| Potential | `V(C)` | baseline energy or disequilibrium cost | depends on topic-level state definition |
| Gradient | `(\kappa / 2)|\nabla C|^2` | spatial memory / smoothing / inertia-like cost | scale dependence remains important |
| Coupling | `\beta C \cdot I` | information-energy interaction | `I` must be defined explicitly, not metaphorically |
| Exchange | `\gamma_J (J_{in} - J_{out}) \cdot C` | semi-open system exchange | not all topics need this term |
| Persistence | `W_N |\nabla \Omega|` | persistence / descent / action-like drive | conceptually important, formally soft |
| Dynamic interaction | `\beta_U V_{game}` | competition / coordination / adaptive interaction | mostly a systems-extension layer |
| Coherence | `\lambda \sum (C_i - C_j)^2` | cross-layer synchrony | requires explicit subsystem definitions |

## Activation rule

A key reading rule for the current repo is that the 7-term functional is **structured**, not
uniformly mandatory.

The question is not "does every topic use all seven terms?"

The better question is:

1. which terms are active here?
2. which terms are leading?
3. which are correction terms?
4. which are conceptual background only?

For practical activation guidance, see:

- [uet-term-activation-rules.md](./uet-term-activation-rules.md)

## Mapping to the codebase

The deepest implementation-side surfaces currently visible in the repo are:

- [docs/core/uet_master_equation.py](../../core/uet_master_equation.py)
- [docs/core/README.md](../../core/README.md)
- [docs/core/uet_parameters.py](../../core/uet_parameters.py)

Current code-side observations:

- the code implements a broader implementation form than the public root `README` sketch
- the code includes additional internal detail such as an information propagator, runtime
  parameter handling, and limit-case verification helpers
- some code comments and status language are stronger than the current conservative audit layer

So the safe relationship is:

- this note explains the promoted technical template
- `docs/core/` shows the current computational realization and its assumptions
- the two are related, but should not be treated as identical without checking the exact code path

## Mapping to audit and governance documents

For repo-first claim discipline, this note should also be read with:

- [docs/topics/0.0_Grand_Unification/FORMULA_AUDIT.md](../../topics/0.0_Grand_Unification/FORMULA_AUDIT.md)
- [docs/topics/0.0_Grand_Unification/METHOD.md](../../topics/0.0_Grand_Unification/METHOD.md)

Those files matter because they narrow the claim boundary:

- `0.0` is currently an integration layer, not a master proof layer
- the formula registry still treats the top-level omega-density sketch as open or symbolic
- topic-level and code-level claims must inherit subordinate limitations

## Derivation status

The repo should currently be read as having **mixed derivation status** across the master
functional.

| Layer | Current safe reading |
| :-- | :-- |
| Structural idea of a multi-term functional | stable legacy core idea |
| Term-by-term interpretation | stable enough to document conservatively |
| Parameter handling discipline | meaningful and important |
| Exact first-principles closure of every term | not yet established repo-wide |
| Universal topic-independent dimensional closure | not yet established repo-wide |
| Exact one-to-one implementation of the full 7-term form in every topic | not true |

## Correspondence and reduction requirement

A central scientific requirement for the master-equation story is not merely novelty but
reduction back to known physics where known physics is already successful.

That means any strong claim should eventually specify:

- the target theory being reduced to
- the regime or limit being taken
- the variable mapping
- the assumptions being switched off or simplified
- whether the reduction is exact, approximate, or heuristic

For the promoted discussion of that standard, see:

- [correspondence-and-reduction.md](./correspondence-and-reduction.md)

## Practical reading checklist

When using this equation in the current repo, ask the following before making a strong claim:

1. What are `C`, `I`, and `J` in this topic?
2. Which terms are active, and which are inactive?
3. Which parameters are source-locked, runtime-level, scale-regime, or heuristic?
4. Is the implementation continuum, discretized, reduced, or symbolic?
5. What artifact or verifier actually checks the claim?
6. Does the topic document a reduction or correspondence boundary?

If those six questions cannot be answered, the equation may still be conceptually useful, but
it is not yet fully audit-ready for a strong scientific claim.

## What should be considered stable

These points are stable enough to carry forward from legacy into current documentation:

- the theory was organized around a multi-term functional rather than a single isolated trick
- the project explicitly tried to combine thermodynamic, informational, geometric, and
  interaction layers in one structure
- the 7-term view shaped the way later topic work and implementations were interpreted

## What should still be treated cautiously

These points should **not** be overpromoted yet:

- that every term has already been fully derived from first principles
- that all parameter values in legacy notes remain canonical today
- that every topic in the repo implements the full 7-term form directly
- that a pass in an integration topic proves theory-level closure of all subordinate topics

## Related promoted notes

- [the-master-equation.md](./the-master-equation.md)
- [term-by-term-stable-summary.md](./term-by-term-stable-summary.md)
- [parameter-registry-stable-summary.md](./parameter-registry-stable-summary.md)
- [correspondence-and-reduction.md](./correspondence-and-reduction.md)
- [uet-term-activation-rules.md](./uet-term-activation-rules.md)

## Legacy sources behind this note

- `LEGACY_REPORTS/01_Core_Theory/MASTER_EQUATION.md`
- `LEGACY_REPORTS/01_Core_Theory/Term-by-Term.md`
