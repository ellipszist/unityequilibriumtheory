---
title: "UET Term Activation Rules"
description: "A practical rule set for deciding which UET terms should be active in a given system and why."
---

# UET Term Activation Rules

This note explains how the UET master functional should be used across different systems
without turning it into arbitrary term-picking.

The key idea is simple:

**UET is one core framework with multiple terms, but each term should be activated only when
the structure of the system justifies it.**

That is different from saying "use any term you want."

## Why this note exists

Without activation rules, a reader may misunderstand UET in one of two bad ways:

- as if every topic must always use all seven terms equally
- as if the author can switch terms on and off without scientific discipline

Both readings are wrong.

The intended use is:

1. define the system
2. define the state variables
3. define the information and flow variables
4. identify which physical or systemic structures are actually present
5. activate only the terms supported by those structures

## High-level rule

The UET master functional is a structured term system.

Each term has:

- a conceptual source
- an activation condition
- a deactivation condition
- a typical role in the model

So the equation is flexible across domains, but not unconstrained.

## Activation table

| Term | Formula element | Activate when | Deactivate or downweight when | Typical role | Main conceptual source |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Potential term | `V(C)` | the system has a meaningful equilibrium, stability cost, or disequilibrium measure | there is no defined state potential yet | leading structural term | thermodynamics, equilibrium thinking |
| Gradient term | `(\kappa / 2)|\nabla C|^2` | spatial or state variation matters and sharp transitions should cost something | the model has no meaningful gradient or no spatial/state field | leading or correction term depending on domain | field theory, geometry, smoothing/stiffness logic |
| Coupling term | `\beta C \cdot I` | information, entropy, structure, or signal content affects the state dynamics | no explicit information-like variable is defined | leading bridge term in information-sensitive topics | Landauer, information-thermodynamic thinking |
| Exchange term | `\gamma_J (J_{in} - J_{out}) \cdot C` | the system is open or semi-open and inflow/outflow changes behavior | the system is treated as closed over the relevant regime | leading term for open systems; correction otherwise | open-system thermodynamics |
| Persistence term | `W_N |\nabla \Omega|` | the topic needs a persistence, descent, action-like, or survival-pressure layer | no rigorous persistence interpretation is available for the topic | conceptual or correction term unless strongly derived | action logic, persistence, natural dynamics |
| Dynamic-interaction term | `\beta_U V_{game}` | multiple agents, sectors, or subsystems strategically interact or adapt to one another | the topic has no meaningful strategic or adaptive interaction layer | extension term, sometimes leading in socio-economic systems | dynamic games, adaptive interaction logic |
| Coherence term | `\lambda \sum (C_i - C_j)^2` | multiple layers or coupled subsystems must stay synchronized or partially unified | there is only one state layer or no meaningful coherence target | layer-coupling or correction term | unity/coherence principle, multi-scale coupling |

## Term-by-term rules

## 1. Potential term

### Use it when

- the system can be described by a stable, metastable, or target equilibrium state
- disequilibrium can be expressed as a cost
- the model needs a baseline state function

### Do not use it casually when

- no state variable is defined well enough to support a potential
- the equilibrium concept is only rhetorical, not mathematical

### Interpretation

This is usually the default structural term.

If a topic cannot even explain `V(C)`, the model is not ready.

## 2. Gradient term

### Use it when

- the state varies across space, scale, or a comparable ordered domain
- sharp transitions should be penalized
- the topic needs a smoothing or stiffness logic

### Do not use it casually when

- there is no meaningful gradient operator for the chosen state variable
- the system is being modeled as a lumped scalar with no internal structure

### Interpretation

This term is common in physics-like and field-like applications.

It often becomes essential in spatial models, continuum models, and layered systems.

## 3. Coupling term

### Use it when

- the topic explicitly defines an information-like variable `I`
- entropy, structure, signaling, uncertainty, or informational content changes the system state
- the theory is trying to express an information-energy bridge

### Do not use it casually when

- `I` is not defined clearly
- "information" is being used only as a metaphor

### Interpretation

This term is central to UET identity.

It is one of the strongest reasons UET is not just a standard equilibrium model.

## 4. Exchange term

### Use it when

- the system is open or semi-open
- environment coupling matters
- input and output flows alter the state trajectory

### Do not use it casually when

- the regime being studied is effectively closed
- inflow/outflow has not been defined operationally

### Interpretation

This term matters for real systems that survive through exchange, not isolation.

It often becomes important in biology, economics, fluid systems, and cosmological inference.

## 5. Persistence term

### Use it when

- the topic explicitly needs a persistence, continuation, descent, or action-like drive
- the model needs to explain why the system tends to keep moving along a path

### Do not use it casually when

- the topic has no rigorous interpretation of this term
- the term is being used only to make a story sound deeper

### Interpretation

This term is part of the conceptual identity of UET, but it is also one of the most
formally delicate.

In current usage it should usually be treated conservatively unless a topic derives it more
cleanly.

## 6. Dynamic-interaction term

### Use it when

- multiple agents or subsystems strategically affect each other
- adaptive response matters
- the model includes competition, coordination, bargaining, or multi-actor adjustment

### Do not use it casually when

- the topic is a single-field physical system with no strategic interaction layer
- the interaction is purely mechanical and does not need an adaptive structure

### Interpretation

This term is better described as a dynamic-interaction extension than as "game theory in
full."

Its role is strongest in complex systems, socio-economic systems, and any topic where the
behavior of one part changes in response to another part's behavior.

## 7. Coherence term

### Use it when

- the system has multiple layers, sectors, scales, or subsystems
- mismatch between those layers should carry a cost
- the model needs a formal expression of unity, coherence, or synchrony

### Do not use it casually when

- there is only one relevant state layer
- the model never defines what `C_i` and `C_j` actually are

### Interpretation

This is the clearest mathematical expression of the "Unity" side of Unity Equilibrium
Theory.

It should not be used unless the coupled subsystems are named explicitly.

## Leading terms versus correction terms

Not all active terms must play the same role.

For each topic, the author should say which terms are:

- `leading`
- `secondary`
- `correction`
- `conceptual only`

That prevents the false impression that every UET model is the full seven-term functional in
equal strength.

## Minimum documentation rule for any topic

If a topic uses UET seriously, it should say:

1. which terms are active
2. why they are active
3. which terms are inactive
4. whether each active term is leading or corrective
5. what variables are assigned to `C`, `I`, `J`, and any subsystem indices

Without that, the implementation is underexplained.

## Domain examples

## Physics-heavy topic

Typical active set:

- `V(C)`
- `(\kappa / 2)|\nabla C|^2`
- `\beta C \cdot I`

Sometimes also:

- `\gamma_J (J_{in} - J_{out}) \cdot C`

Usually weaker unless derived carefully:

- `W_N |\nabla \Omega|`
- `\beta_U V_{game}`

Possible when multiple sectors are coupled:

- `\lambda \sum (C_i - C_j)^2`

## Open complex system

Typical active set:

- `V(C)`
- `\beta C \cdot I`
- `\gamma_J (J_{in} - J_{out}) \cdot C`
- `\lambda \sum (C_i - C_j)^2`

Potentially important:

- `\beta_U V_{game}`

## Socio-economic or adaptive system

Typical active set:

- `V(C)`
- `\beta C \cdot I`
- `\gamma_J (J_{in} - J_{out}) \cdot C`
- `\beta_U V_{game}`
- `\lambda \sum (C_i - C_j)^2`

Gradient term may still matter if the model has a spatial or network geometry.

## Safe conclusion

UET should be read as:

- one core framework
- with multiple structured terms
- activated by system properties
- not by arbitrary author preference

That is the mathematical discipline needed to keep the theory flexible without making it
vague.

## Related notes

- [master-equation-stable-summary.md](./master-equation-stable-summary.md)
- [term-by-term-stable-summary.md](./term-by-term-stable-summary.md)
- [parameter-registry-stable-summary.md](./parameter-registry-stable-summary.md)
- [correspondence-and-reduction.md](./correspondence-and-reduction.md)
- [../04_User_Guides/how-to-use-uet-as-a-system-equation.md](../04_User_Guides/how-to-use-uet-as-a-system-equation.md)

## Legacy sources behind this note

- `LEGACY_REPORTS/01_Core_Theory/MASTER_EQUATION.md`
- `LEGACY_REPORTS/01_Core_Theory/Term-by-Term.md`
- `LEGACY_REPORTS/01_Core_Theory/THREE_CORE_TERMS.md`
- `LEGACY_REPORTS/03_Evidence/DOMAIN_MAPPING.md`
