# Resource Selection Dynamic-Game Comparator

Status: CANDIDATE_NORMALIZED_DYNAMIC_SELECTION / SIMULATION_ONLY

This lane formalizes the persistence hypothesis as a non-agentic dynamical
selection comparator. It does not assign intention, consciousness, or a goal to
matter.

## State and interaction

Let p_i(t) be the normalized occupancy of interaction states. The interaction
matrix A_ij is an explicit normalized compatibility/payoff comparator. The
collective coordinate is derived from the interaction state:

    C_collective = sum_i,j p_i A_ij p_j

The state evolution is the standard replicator-style relation:

    dp_i/dt = p_i (f_i - sum_j p_j f_j)

with

    f_i = s sum_j A_ij p_j - w c_i

where s and w are declared normalized comparator weights and c_i is the
behavior-related cost of state i.

This relation is a constitutive/evolutionary-game comparator. It is not a
derivation that nature has an objective function.

## Resource ledger

    dE_available/dt =
        J_in - J_out - P_behavior - P_maintenance

    P_behavior = sum_i p_i c_i
    P_maintenance = sum_i p_i m_i

Persistence is defined only as the benchmark event

    t_persist = inf{t : E_available(t) <= E_sustain}

The ledger does not identify E_available with SI energy until a physical lane
maps the costs to work, heat, or entropy production.

## Research question

For identical initial resource and initial state distributions, do interaction
structures with greater collective compatibility and lower resource cost produce
longer persistence without adding an intentional optimizer?

The answer is a falsifiable comparator result. It is not evidence for universal
Darwinian, biological, cosmological, or particle dynamics.

## Required gates

- simplex preservation and non-negative probabilities
- ledger closure without clipping
- deterministic configuration and no fitting
- C is derived from interaction state, not relabelled mass
- persistence ordering survives dt refinement
- physical mapping to work, heat, or entropy remains open
