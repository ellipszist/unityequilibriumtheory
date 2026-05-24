# 📉 Limitation: The Semi-Empirical Reality

> [!WARNING]
> **Legacy claim boundary:** This file is a concept, paper draft, bibliography note, or legacy analysis note from an earlier drafting pass.
> It is not the topic status authority and must not be used to claim QCD derivation, confinement proof,
> full AME2020-table pass, hadron-mass validation, light-nuclei closure, independent proton-radius prediction,
> complete strong-force theory, or Millennium-style closure. Current allowed claims are controlled by
> `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `FORMULA_AUDIT.md`, and
> `Result/artifacts/nuclear_binding_source_locked_validation.json`: selected heavy-nucleus subset and proton-radius benchmark-anchor checks only.

## The Problem
Calculating Nuclear Binding Energy explicitly from the UET Master Equation ($\Omega$) requires simulating the interaction of every quark and gluon in a non-perturbative regime. This is equivalent to "Lattice QCD" and is computationally impossible on a standard machine.

## Current Shortcut
Instead of solving the Master Equation for 56 nucleons (168 quarks), we use the **Semi-Empirical Mass Formula (SEMF / Weizsäcker)** as a baseline:

$$B/A \approx a_{vol} - a_{surf}A^{-1/3} - ...$$

We then apply a **UET Correction** to account for shell effects (Magic Numbers) which SEMF fails to predict:

$$UET\_Correction = \beta_{nuc} \frac{\ln A}{A}$$

## Honest Admission
The parameter **$\beta_{nuc} = 0.8$ Mev** is **NOT** derived from first principles (like $\ln 2$ or Planck Length).
- It is a **[CALIBRATED PARAMETER]**.
- It was determined by fitting the residuals of AME2020 data.

## Why is this Acceptable?
While `beta_nuc` is calibrated, its *form* ($\frac{\ln A}{A}$) is derived from UET's Information Entropy principle. This demonstrates that nuclear shell structure behaves like an "Information Field Resonance," even if we must calibrate the magnitude empirically.
