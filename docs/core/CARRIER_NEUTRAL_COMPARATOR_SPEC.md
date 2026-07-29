# Carrier-Neutral Comparator Contract

## Status

`BLOCKED / CONTRACT_ONLY / NO_UET_PARTICLE_DERIVATION`

This document defines the minimum comparison record for a photon lane, a
neutrino lane, and an electron-positron reaction lane. It does not choose a
universal carrier for UET and does not identify `I_trace`, `R_gen`, or `effect`
with any particle.

## Required lane record

Every lane must record:

- source interaction and source state,
- carrier identity or reaction-participant role,
- rest-mass status,
- energy-momentum ledger,
- charge/current and other relevant conservation laws,
- propagation law and causal speed,
- detector/receiver interaction,
- observable payload and units,
- falsification condition,
- source provenance and evidence status.

## Declared comparator roles

| Lane | Role in this program | Current status |
| --- | --- | --- |
| Photon | primary massless electromagnetic observation/signal-carrier baseline | standard comparator; UET derivation not established |
| Neutrino | weakly interacting carrier candidate with standard mass eigenstates | benchmark compatibility only; UET identity not established |
| Electron-positron | mass-bearing antiparticle reaction participant; annihilation product comparator | standard reaction comparator; not a universal carrier |

The phrase “mass-bearing phase continues in a carrier” is therefore a
candidate transition hypothesis. It can be tested only after a source
interaction, transition mechanism, and conservation ledger are specified. A
large speed or an observer record alone cannot derive a photon or erase rest
mass.

## Gate boundary

The contract remains `BLOCKED` while the matter-space core has a causal-support
failure, while the carrier-specific unit/detector maps are open, or while the
Topic 0.11 phase pilot is only simulation-only. The next valid work is a
source-locked comparator package, not parameter fitting or particle identity
promotion.
