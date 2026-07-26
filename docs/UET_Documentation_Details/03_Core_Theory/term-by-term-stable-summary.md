---
title: "Term-by-Term Stable Summary"
description: "Conservative interpretation of the major UET master-equation terms promoted from legacy notes."
---

# Term-by-Term Stable Summary

This note promotes the most reusable interpretive layer from the legacy term-by-term
material.

It focuses on what each term is *trying* to represent, not on claiming that every mapping is
already closed mathematically in the present repository.

Current ontology rule: `C` is an abstract relational variable for interaction and system
behaviour. Mass, density, charge, energy, information, and order are lane-specific mappings;
they are not universal meanings of `C`. See
[C as a Relational Interaction Variable](./relational-C-and-physical-mapping.md).

## Summary table

| Term | Formula element | Stable interpretation | Open caution |
| :-- | :-- | :-- | :-- |
| 1 | `V(C)` | baseline cost or preference over relational interaction structure | exact physical meaning and units depend on topic/domain |
| 2 | `(\kappa / 2)|\nabla C|^2` | cost of sharp variation of the relational coordinate across space/state | not automatically kinetic energy or viscosity |
| 3 | `\beta C · I` | coupling between the declared `C` sector and a second model sector | not a C-to-I conversion; the meaning of `I` must stay explicit |
| 4 | `\gamma_J (J_in - J_out) · C` | openness, inflow/outflow, exchange | not all topics use this layer equally |
| 5 | `W_N |\nabla \Omega|` | persistence or action-like drive toward a path | strongest conceptual term, weakest formal closure |
| 6 | `\beta_U V_game` | strategic interaction / competition / cooperation | mostly a higher-level systems extension |
| 7 | `\lambda \sum (C_i - C_j)^2` | coherence across layers or subsystems | needs explicit subsystem definitions in practice |

## 1. Potential term

### Formula

```text
V(C)
```

### Stable interpretation

This term acts like the cost of being away from a preferred or equilibrium configuration of the relational system state.

It is the clearest place where UET overlaps with familiar energy-functional thinking such as
Landau-Ginzburg style modeling, but the physical realization and units of `C` remain lane-specific.

### Safe statement

Use this term when the topic needs a baseline energy / stability / disequilibrium cost.

## 2. Gradient term

### Formula

```text
(\kappa / 2)|∇C|^2
```

### Stable interpretation

This term penalizes sharp gradients of the relational interaction coordinate.

In the legacy interpretation it carries ideas such as:

- spatial memory
- smoothing cost
- inertia-like resistance to abrupt change

### Safe statement

Use this term when the topic needs a cost for non-uniformity or sharp spatial/state
variation.

## 3. Coupling term

### Formula

```text
β C · I
```

### Stable interpretation

This is a coupling between the relational `C` sector and a second sector represented by `I`.
If a topic defines that second sector as information, entropy, or an observer record, the
coupling can be studied in that lane. The notation alone does not establish that `C` converts
into `I`, that information is a substance, or that `beta` has Landauer units.

### Safe statement

Use this term as a constitutive coupling only after the topic declares the meaning, units,
and observable mapping of `I`.

## 4. Exchange term

### Formula

```text
γ_J (J_in - J_out) · C
```

### Stable interpretation

This term was introduced to avoid treating interesting systems as perfectly closed.

It is the semi-open-system term:

- inflow
- outflow
- exchange with environment

### Safe statement

Use this term when the topic studies real systems that survive by exchange rather than
isolated conservation alone.

## 5. Natural-will term

### Formula

```text
W_N |∇Ω|
```

### Stable interpretation

In legacy language this term tries to capture persistence, survival pressure, or action-like
drive.

This is a meaningful part of the project’s conceptual identity, but it is also one of the
terms that needs the most caution in formal scientific wording.

### Safe statement

Treat this as a conceptual persistence term unless a topic provides a clearer derivation.

## 6. Game term

### Formula

```text
β_U V_game
```

### Stable interpretation

This term extends the framework into competition, coordination, or game-like interaction
between agents or subsystems.

It is more important for higher-level complex-system interpretations than for narrow
fundamental-physics derivations.

### Safe statement

Treat this as a systems-extension layer, not automatically as a core fundamental-physics
term for every topic.

## 7. Coherence term

### Formula

```text
λ Σ(C_i - C_j)^2
```

### Stable interpretation

This term penalizes mismatch between layers, subsystems, or coupled degrees of freedom.

It is the clearest formal expression of the “unity” side of UET.

### Safe statement

Use it when the topic explicitly defines multiple layers or subsystems whose coherence
matters.

## Practical reading rule

When reading UET topics, ask:

- which of the seven terms are actually active here?
- which are conceptual background only?
- which are benchmarked?
- which are still heuristic?

That question is more useful than assuming every topic implements the full legacy functional
in the same way.

## Legacy sources behind this note

- `LEGACY_REPORTS/01_Core_Theory/Term-by-Term.md`
- `LEGACY_REPORTS/01_Core_Theory/MASTER_EQUATION.md`
