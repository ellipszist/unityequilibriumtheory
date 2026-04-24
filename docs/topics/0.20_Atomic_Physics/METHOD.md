# Method

## Problem target

This topic studies whether UET-style atomic models can reproduce selected spectral and multi-electron atomic benchmarks.

## Core components

### Engine components
- `Code/01_Engine/Engine_Atomic_Hydrogen.py`

### Proof-oriented components
- `Code/02_Proof/Proof_Hydrogen_Spectrum.py`

### Research and comparison components
- `Code/03_Research/Research_Atomic_ThreeBody.py`
- `Code/03_Research/Research_Multi_Electron.py`
- `Code/03_Research/Research_Rydberg_Validation.py`

## Variable framing

- Primary modeled quantities: energy levels, spectral-line positions, orbital-scale terms, and correction parameters

## Assumptions

- The current package is an internal atomic benchmark environment for selected hydrogen, helium, and related data.

## Domain of validity

- Selected atomic spectra and multi-electron comparisons represented in topic-local NIST-style files.

## Excluded cases

- A full QED derivation or universal many-body closure for all atoms.

## Parameter sensitivity note

- Approximation choices beyond simple atoms remain important in the current scripts.
