# No-Fitting Core Policy

## Purpose

The theory-core scope `0.0-0.26` must not be upgraded by tuning parameters to make a target
benchmark pass.

The goal is not to make outputs look good. The goal is to test whether the model's quantities
follow from prior definitions, independently specified physical quantities, or explicit
derivations.

## Rule

For core-theory evidence:

- A parameter must be derived, measured independently, or specified before the target
  benchmark is evaluated.
- A target-informed fit may be recorded only as a diagnostic, sensitivity study, or rejected
  alternative.
- A fitted value cannot be used as evidence that the equation is natural, derived, or
  physically explanatory.
- If a topic needs fitting to pass, the honest status is `Tier B` or lower until a no-fitting
  derivation exists.

## Allowed Evidence Types

| Evidence type | Can support scientific validity? | Condition |
| :-- | :-- | :-- |
| Prior derivation | yes | Variables, assumptions, and domain of validity are documented before benchmark comparison |
| Independent measurement | yes | Source and uncertainty are documented in the data manifest |
| Out-of-sample prediction | yes | Config is frozen before target evaluation |
| Fitted parameter | no | May be used only as diagnostic or calibration note |
| Post-hoc threshold change | no | Must not be used to convert failure into pass |

## Current Application

`0.3_Cosmology_Hubble_Tension` currently fails because the default beta explains only part of
the Planck-SH0ES H0 gap. Computing the beta that would force a match is useful diagnostic
information, but it is not an acceptable explanation of the physics.
