---
title: "C as a Relational Interaction Variable"
description: "Canonical ontology, physical correspondence, and observable mapping for the UET variable C."
status: "current ontology note; candidate correspondence, not a physical proof"
---

# C as a Relational Interaction Variable

## Status and purpose

This note records the current foundational meaning of `C` after reviewing the earlier UET
equation notes, the observation-as-past thought experiment, and the implemented equation
families.

The central correction is:

> `C` is an abstract relational variable for interaction and system behaviour. It is not
> universally mass, density, energy, information, a particle, or a tangible substance.

The word *interaction* is being used in the systems sense: a relation between degrees of
freedom, events, or subsystems that changes what can happen next. The relation is real in the
model, but it is not required to be an object that can be isolated and held in a container.

This is an ontology and research-order decision. It is not yet a derivation of a universal
physical observable for `C`.

## What the earlier material already contained

The idea was present in several earlier layers, but it was not consistently named or locked:

- the early equation analysis treats behaviour as requiring energy, leaving a record, and
  creating persistence pressure;
- the source--transmission--latency--observer material treats an observation as a received
  record of an earlier event rather than the event itself;
- the notation guide describes uppercase `C` as a dynamical coordination/communication
  variable;
- the legacy term-by-term notes use `C` for capacity, mass, density, concentration, and
  other lane-specific quantities.

These are not the same statement. The current rule is to preserve the interaction idea as the
foundational interpretation and treat mass, density, charge, order, and other quantities as
explicit downstream realizations. Older mappings remain useful provenance, but they cannot be
read as a universal definition of `C`.

Related source note: [Observation as Past Behavior](../../../core/THOUGHT_EXPERIMENT_OBSERVATION_PAST_BEHAVIOR.md).

## Ontology layers

The following layers must not be collapsed into one another:

| Layer | Symbol or object | Meaning | Current status |
| :-- | :-- | :-- | :-- |
| Relational model | `C` | coarse-grained coordinate for interaction/behavioural structure | foundational candidate ontology |
| Physical realization | `rho`, `n`, order parameter, stress, etc. | a lane-specific quantity mapped from or represented by `C` | must be declared per lane |
| Energy bookkeeping | `E`, `Omega`, free energy, heat, work | a quantity with its own balance law and units | not interchangeable with `C` |
| Observer record | `R = I_trace` or a measurement record | information calculated/received from completed physical change | derived observable unless a lane says otherwise |
| Space response | `Phi`, `Pi = d_t Phi` | an opt-in effective response variable in the matter--space candidate | not `C`, mass, metric, or trace |
| Standard physical object | `m`, `rho`, `q`, `T^{mu nu}` | mass, density, charge, and stress-energy | separate variables requiring correspondence |

The distinction is important because a number obtained by calculating an interaction is not
automatically a new substance. Likewise, a physical quantity that is useful in one application
does not become the definition of the abstract coordinate in every application.

## Relational definition of `C`

For a pair of interacting subsystems, the conceptual form is

$$
C_{ab} = {\cal I}(X_a, X_b; \Gamma_{ab}),
$$

where `X_a` and `X_b` are the states of the subsystems and `Gamma_ab` describes the relevant
channel, geometry, boundary, or coupling context. The functional `cal I` is intentionally
left open until a physical lane supplies a derivation and units.

For a continuum or coarse-grained model, `C(x,t)` represents the local aggregate of such
relations. It may encode how neighbouring states constrain, exchange with, or respond to one
another. It does not mean that the region contains a field of “interaction-stuff”.

The first correspondence baseline is therefore relational rather than material:

$$
\text{states and channels}
\longrightarrow
\text{interaction structure } C
\longrightarrow
\text{physical response and measurement record}.
$$

This is compatible with asking how two bodies are related in a Newtonian model and then asking
how finite signal propagation changes the observer's record. It does not replace Newtonian
mechanics or special relativity. Those theories provide standard comparison lanes and limiting
cases.

## What `C` is not

The following interpretations are not allowed without a new, explicit lane contract:

- `C` is not mass or baryonic mass density by definition;
- `C` is not energy, kinetic energy, or a conserved energy reservoir;
- `C` is not information or a memory store by definition;
- `C` is not a particle, anti-particle, metric tensor, ether, or new substance;
- `C` is not automatically the observer's record of what has already happened;
- `C` is not identical to `Phi` or to `R = I_trace`.

The statement that behaviour uses energy is a constraint on a physical realization and its
ledger. It does not turn the relational coordinate `C` into energy.

## Lane-specific physical correspondence

Every application must declare a mapping

$$
C \xrightarrow{\;M_ell\;} Q_ell
\xrightarrow{\;O_ell\;}
y_ell,
$$

where `Q_ell` is a standard-physics quantity for lane `ell` and `y_ell` is the observable
actually measured by an instrument or dataset.

Examples of permitted mappings are:

| Lane | Possible `Q_ell` | Observable | Required caution |
| :-- | :-- | :-- | :-- |
| Mass-density | `rho(x,t)` | mass profile, gravitational response, rotation curve | requires dimensional map and stress/gravity model |
| O(2) charge | `n(x,t)` | charge/current response | `C` is not automatically the Noether density; the map must be derived |
| Phase transition | order parameter or correlation field | structure factor, interface width, correlation length | diagnostic realization, not universal ontology |
| Heat transport | temperature, heat flux, entropy production | `T`, `q`, lag, phase, hysteresis | `C` must not be reported as heat without a unit contract |
| Relational observer | relative position/velocity or interaction observable | delayed signal, received state, inferred relation | observer record is not the underlying event |

If a lane cannot state `Q_ell`, its units, and `O_ell`, it is `BLOCKED` for fitting or physical
claim. It may remain a normalized mathematical or conceptual experiment.

## Reading the legacy functional with the new ontology

The historical template is

$$
\Omega[C,I,J] = \int d^3x\,\left[
V(C)+\frac{\kappa}{2}|\nabla C|^2+\beta C I
+\gamma_J(J_{in}-J_{out})C+W_N|\nabla\Omega|
+\beta_U V_{game}+\lambda\sum(C_i-C_j)^2
\right].
$$

Under the current ontology:

1. `V(C)` is a cost or preference over interaction structure. It is not physical energy until
   the lane supplies units and an energy derivation.
2. `kappa |grad C|^2 / 2` penalizes spatial variation of the relational coordinate. It is not
   automatically kinetic energy, viscosity, or energy consumed by motion.
3. `beta C I` is a coupling term between two declared model sectors. It does not prove that
   `C` converts into `I`, that matter becomes information, or that information is a new
   reservoir.
4. `J_in - J_out` is a boundary/exchange term only when `J` has been defined as a flux with
   the appropriate units and boundary law.
5. `W_N`, `V_game`, and the coherence term are constitutive or systems extensions unless a
   topic derives them and identifies observables.

The equation therefore describes a relational system model. It does not, by its notation
alone, identify what the relational coordinate is made of.

## Condition, constraint, and necessity

The conceptual argument that motivated this interpretation contains three different claims.
They must be kept separate:

### Condition: behaviour involves energy exchange or use

For a chosen physical lane, a change, interaction, or behaviour must be associated with a work,
heat, chemical, field, or other energy ledger. A useful abstract bookkeeping form is

$$
E_{available}(t+\Delta t)
= E_{available}(t) - W_{behaviour} + J_{in} - J_{out},
\qquad W_{behaviour}\geq 0,
$$

with the understanding that energy is transferred or redistributed rather than simply
destroyed. This is a modelling condition, not a proof that every abstract change has one
universal scalar energy cost.

### Constraint: persistence requires available resources

If a system exhausts the resource or free-energy budget that supports its allowed transitions,
it cannot continue the same class of behaviour. The precise stopping criterion depends on the
lane, boundary conditions, and dissipation model. It must not be silently identified with
`Omega` or with the value of `C`.

### Necessity: shared behaviour can reduce persistence cost

The proposal that systems are selected toward coordinated or shared behaviour is a systems and
evolution hypothesis: coordination may reduce the cost of maintaining a viable state or preserve
usable potential for longer. It requires an explicit population/selection or multi-agent model.
It is not automatically derived from the seven-term functional, from the second law alone, or
from the symbol `C`.

This separation prevents a conceptual statement from being mistaken for a completed physical
derivation.

## Relation to observation and “past”

The observation thought experiment adds a separate measurement layer:

1. a physical interaction occurs;
2. the interaction changes a propagating carrier or local record;
3. an observer receives and processes that record later;
4. the observer's calculated information refers to the received past event, not necessarily
   the full present state of the source.

This supports a finite-signal/observer mapping question. It does not mean that every physical
trace is merely subjective, and it does not make `C` equal to `I_trace`. The underlying event,
its physical response, and the observer's record must remain separate in the model.

## Equation-family boundaries in the repository

The current implementation has several lanes that must not be read as one completed universal
equation:

| Implementation lane | What it can mean | What it cannot claim |
| :-- | :-- | :-- |
| `legacy_variational_v1` | normalized C/I functional and derivative closure under its declared contract | universal physical identity of `C` or `I` |
| `matter_space_coupled_v1` | opt-in candidate where `C`, `Phi`, and `Pi` are physical state variables for a specific normalized realization | a mass equation or derivation of spacetime itself |
| `spacetime_trace_v1` | derived causal history observable from a declared source history | a new substance or feedback field by default |
| relational observer toy lane | delayed record and two-body correspondence baseline | replacement of Newtonian or relativistic dynamics |

The `matter_space_coupled_v1` lane is therefore a possible physical realization of a chosen
`C` field, not the foundational definition of `C`. Before using it for mass or galaxy work, a
mass-density mapping must be declared and tested separately.

## Required research order

Future equation work must follow this order:

1. lock the meaning of the relational variable and its pair/continuum representation;
2. construct a two-body relational baseline against Newtonian mechanics;
3. define the finite-signal observation operator and distinguish event from received record;
4. choose one physical lane and derive its mapping from `C` to a standard quantity;
5. close units, variational derivatives, symmetries, conservation, and limiting cases;
6. verify numerical behaviour and reproducibility;
7. define the observable operator and data provenance;
8. only then calibrate, hold out, compare externally, and make a claim.

The dependency is intentionally one-way: a successful simulation of a normalized `C` field
does not by itself establish mass, information, gravity, or a new physical substance.

## Current claim boundary

- `C` as a relational interaction coordinate: **current ontology proposal**.
- `C` as a particular mass, density, charge, or order variable: **lane-specific and open**.
- behaviour requiring an energy ledger: **physical modelling condition; mapping open**.
- persistence/coordination pressure: **systems hypothesis; not derived globally**.
- observation as a record of a past event: **conceptual/standard correspondence baseline**.
- a universal UET physical equation: **not established**.
