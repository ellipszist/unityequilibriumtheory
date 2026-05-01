# Method

## Problem target

This topic studies whether UET-style condensate and pairing ideas can reproduce selected superconducting or superfluid benchmark behavior.

## Core components

### Engine components
- `Code/01_Engine/Engine_Superconductivity.py`

### Proof-oriented components
- `Code/02_Proof/Proof_Cooper_Pairing.py`

### Research and comparison components
- `Code/03_Research/Experiment_Superconductor_Data.py`
- `Code/03_Research/Research_Hydrides.py`
- `Code/03_Research/Research_Plasma.py`

## Variable framing

- Primary modeled quantities: critical temperature, order-parameter-like quantities, coupling terms, and material descriptors
- Formula registry: see `FORMULA_AUDIT.md` for the distinction between McMillan/Allen-Dynes baseline formulas, calibrated material inputs, heuristic UET coherence terms, and superfluid/plasma diagnostics.

## Assumptions

- The current scripts behave like phenomenological internal models tied to selected materials and curated datasets.

## Domain of validity

- Selected superconducting materials, hydrides, and related transition benchmarks.

## Excluded cases

- A microscopic many-body derivation for all superconductors or a universal superfluid theory.

## Parameter sensitivity note

- Material selection and calibration choices still affect reported fits.
- The current primary verifier is the raw McMillan baseline because it produces a simple auditable artifact from the topic-local working-copy table.
- The verifier now includes an inverse-McMillan diagnostic: holding `Theta_D_K` and `mu_star` fixed, it solves for the `lambda_ep` that would reproduce the observed `Tc`. This identifies whether the current row-level coupling package is over- or under-driving the baseline.
- The Allen-Dynes/UET engine must be promoted through a separate verifier that reports per-material residuals and labels calibrated inputs before it can support stronger claims.
- The source-lock layer now pins McMillan 1968, Allen-Dynes 1975, and NIMS SuperCon provenance records, but this is not the same as row-level upstream normalization.

## Dependency policy

- `0.11_Phase_Transitions` may reference this topic only as a condensate/transition benchmark dependency until the formula and data gates are stronger.
- `0.13_Thermodynamic_Bridge` may use superfluid entropy or condensation-energy notes only with explicit unit conventions.
- `0.0_Grand_Unification` should treat UET coherence terms here as heuristic bridge terms, not proof-level support.

## Next model-hardening experiment

1. Build a row-level material table where each `Tc`, phonon-temperature proxy, `lambda`, and `mu_star` value has a source row or explicit literature citation.
2. Use the inverse-McMillan audit to flag rows where the declared `lambda_ep` strongly disagrees with the coupling implied by the observed `Tc`.
3. Run the raw McMillan gate against the normalized table without inverse calibration.
4. Run a separate Allen-Dynes/UET candidate gate with labels for source-locked, calibrated, and heuristic inputs.
5. Require a held-out material split before promoting any prediction-strength language.
