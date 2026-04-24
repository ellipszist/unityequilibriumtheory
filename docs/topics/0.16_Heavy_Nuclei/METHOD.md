# Method

## Problem target

This topic studies whether UET-style heavy-nuclei and fission models can reproduce selected high-mass nuclear benchmarks.

## Core components

### Engine components
- `Code/01_Engine/Engine_Fission_Solver.py`
- `Code/01_Engine/Engine_Heavy_Nuclei.py`

### Proof-oriented components
- `Code/02_Proof/Proof_Stability_Valley.py`

### Research and comparison components
- `Code/03_Research/Research_Fission.py`
- `Code/03_Research/Research_Heavy_Binding.py`
- `Code/03_Research/Research_Heavy_Nuclei.py`

## Variable framing

- Primary modeled quantities: binding energy, fission observables, stability-valley terms, and heavy-nuclei correction parameters

## Assumptions

- The topic uses selected heavy-nuclei and fission benchmarks rather than a universal nuclear-force derivation.

## Domain of validity

- Heavy nuclei, fission, and related mass-table comparisons represented in topic-local files.

## Excluded cases

- A complete first-principles theory for all nuclear stability and decay channels.

## Parameter sensitivity note

- Fit sensitivity remains important for high-mass tails and stability-valley behavior.
