---
layout: article
title: "UET Topic 0.20: Atomic Physics"
description: "Hydrogen spectrum benchmark and atomic-model diagnostics within the Unity Equilibrium Theory framework."
---

# 0.20 Atomic Physics

> [!NOTE]
> **AI-Digest**: This topic currently has a source-backed hydrogen Rydberg benchmark using a NIST hydrogen spectrum working copy and CODATA `R_H`. It also has an explicit Bohr/de Broglie/Rydberg formula-bridge manifest that maps inherited standard atomic physics to UET dependencies (`0.13`, `0.6`, `0.17`, `0.23`) without upgrading those dependencies into a first-principles UET derivation. The current artifact now adds a rounded hydrogen n-level energy benchmark, a provisional selected hydrogen-like ion reduced-mass benchmark for He+ and Li2+, a precision spectroscopy source gate, nonrelativistic and leading Dirac 1S-2S baseline residual diagnostics, an empirical Lamb-shift handoff, and a neutral helium source gate. First-principles QED/recoil/proton-size/hyperfine residuals, neutral helium residuals, many-electron atoms, broad hydrogen-like ion coverage, and UET-derived `R_H` remain blocked.

![Status](https://img.shields.io/badge/Status-Hydrogen%20Benchmark-blue)
![Claim_Class](https://img.shields.io/badge/Claim%20Class-C%20Internal%20Benchmark-yellow)
![Verifier](https://img.shields.io/badge/Verifier-Artifact%20Required-blue)

## Research Role

Topic `0.20` is the atomic benchmark layer for UET. Its near-term job is to make hydrogen spectral formulas, constants, NIST data, and residual thresholds auditable before the theory uses atomic physics as evidence for broader information-channel claims.

## Conceptual Map

```mermaid
flowchart LR
    nist["NIST hydrogen spectrum"] --> rows["Balmer/Lyman vacuum wavelengths"]
    codata["CODATA R_H"] --> formula["Rydberg wavelength relation"]
    bridge["Bohr/de Broglie/Rydberg bridge manifest"] --> formula
    deps["0.13 / 0.6 / 0.17 / 0.23 dependency roles"] --> bridge
    rows --> verifier["Research_Rydberg_Validation.py artifact"]
    formula --> verifier
    verifier --> ions["Hydrogen-like ion checkpoint predictions"]
    verifier --> claim["Claim Class C: hydrogen spectrum benchmark"]

    levels["Hydrogen level data"] --> secondary["Secondary level-energy lane"]
    many["Three-body / multi-electron scripts"] --> open["Open: not primary evidence"]
    open --> deps["Inherited limitation for downstream topics"]
```

## Evidence and Status Matrix

| Layer | Current status | Evidence path | Claim allowed now | Blocker |
| :-- | :-- | :-- | :-- | :-- |
| Data | NIST/CODATA source-labeled working copies | `Data/03_Research/nist_hydrogen_spectrum.json`, `codata_2018_atomic.json` | Hydrogen line and constant inputs are inspectable with hashes. | Wavelength precision and source-transcription notes still need normalization. |
| Formula | Reviewed registry plus bridge manifest | `FORMULA_AUDIT.md`, `Data/03_Research/atomic_formula_bridge_manifest.json` | Photon transition, de Broglie standing wave, Bohr energy, Rydberg relation, and dependency roles are mapped. | UET derivation of `h`, `alpha`, `R_H`, transition operators, or the atomic Hamiltonian is not artifact-backed. |
| Verification | Runnable primary artifact | `Code/03_Research/Research_Rydberg_Validation.py` | Supports hydrogen-spectrum internal benchmark claims. | Many-electron and QED effects are outside the verifier. |
| Source evidence workflow | Structured provenance gate | `Data/03_Research/source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json` | source-review queue | Direct hydrogen level-table precision, direct Li III ASD capture, precision, and many-electron packages still need dedicated artifacts. |
| Branch claim gate | Structured claim ceiling | `Data/03_Research/branch_claim_gate.json` | benchmark-only claim control plus formula-bridge manifest branch | Hydrogen benchmark and bridge manifest do not promote full atomic-theory claims. |
| Hydrogen level energies | Rounded source-referenced benchmark | `Data/03_Research/hydrogen_spectra_data.json`, `hydrogen_level_energy_benchmark` in artifact | Selected `n=1..8` level rows pass ionization-energy anchored thresholds (`avg ~69 ppm`, `max ~118 ppm`). | Direct ASD per-level transcription precision and fine/QED splitting remain open. |
| Hydrogen-like ions | Provisional reduced-mass benchmark | `Data/03_Research/hydrogen_like_ion_spectrum.json`, `hydrogen_like_checkpoint` in artifact | Selected He+ and Li2+ rows pass reduced-mass hydrogenic thresholds (`avg ~76 ppm`, `max ~97 ppm`). | Li III still needs direct primary ASD capture; broad ion suite and fine-structure component policy remain open. |
| Precision spectroscopy | Source package plus baseline diagnostics | `Data/03_Research/hydrogen_precision_spectroscopy_sources.json`, `hydrogen_lamb_shift_correction_sources.json`, `precision_baseline_gate`, `precision_dirac_baseline_gate`, and `lamb_shift_handoff_gate` in artifact | 1S-2S, Lamb shift, and 21 cm hyperfine targets are organized; nonrelativistic, leading Dirac, and empirical Lamb-handoff residuals are computed. | Residuals step from `~22.99 GHz` to `~7.10 GHz` to `~10.32 MHz`; the final step is empirical handoff only, not QED/recoil/proton-size validation. |
| Neutral helium / many-electron | Source package only | `Data/03_Research/helium_many_electron_sources.json`, `helium_many_electron_gate` in artifact | Five He I visible target lines are organized for future many-electron artifacts. | No two-electron Hamiltonian/correlation model, term mapping, or residual gate yet. |
| Claim-scope gate | Artifact export controller | `atomic_claim_scope_gate` in artifact | blocks derivation/QED/many-electron overclaim | Hydrogen PASS remains topic-level `WARN` until precision and derivation branches are primary-gated. |
| Claims | Bounded to hydrogen benchmark | this README, `METHOD.md`, `LIMITATIONS.md` | May state that selected hydrogen lines match the standard Rydberg relation within declared thresholds. | Cannot claim full atomic theory or first-principles UET derivation. |
| Dependencies | Atomic constants/levels bridge | `0.6`, `0.17`, `0.21`, `0.23`, `0.0` | Downstream topics may cite the hydrogen benchmark with limitations. | Stronger claims need fine-structure/many-electron artifacts. |

## Primary Verification

```powershell
python docs/topics/0.20_Atomic_Physics/Code/03_Research/Research_Rydberg_Validation.py
```

Expected artifact:

- `Result/artifacts/0_20_atomic_physics_verification.json`

The artifact records dataset hashes, NIST/CODATA source IDs, line residuals, fitted slope, level-energy residuals, thresholds, formula-bridge manifest metadata, selected hydrogen-like ion benchmark rows, and limitations.
It must also record `atomic_claim_scope_gate`, which allows only hydrogen Rydberg benchmark, rounded hydrogen level-energy benchmark, formula-bridge-manifest, provisional selected He+/Li2+ reduced-mass benchmark language, precision-source-package language, nonrelativistic/Dirac 1S-2S baseline diagnostic language, empirical Lamb-handoff language, and neutral-helium-source-package language while blocking Rydberg derivation, broad hydrogen-like ion validation, QED correction validation, neutral helium residual validation, many-electron, and full atomic-theory claims.

## Key Files

- `FORMULA_AUDIT.md`: formula registry, units, constants, proof status, and failure modes.
- `DATA_MANIFEST.md`: NIST/CODATA working-copy provenance and benchmark roles.
- `VERIFICATION_SPEC.md`: primary command, thresholds, and artifact contract.
- `METHOD.md`: evidence lanes and dependency policy.
- `LIMITATIONS.md`: boundaries for derivation, QED, helium, and many-electron claims.
- `Data/03_Research/source_evidence_intake_stub.json`: provenance intake for hydrogen and future atomic lanes.
- `Data/03_Research/source_evidence_readiness_matrix.json`: readiness gate for source review.
- `Data/03_Research/branch_claim_gate.json`: branch-level claim ceiling.
- `Data/03_Research/atomic_formula_bridge_manifest.json`: Bohr/de Broglie/Rydberg dependency map connecting inherited formulas to UET topics without overclaiming derivation.
- `Data/03_Research/hydrogen_like_ion_spectrum.json`: source-referenced He+ and Li2+ rows for the provisional one-electron ion gate.
- `Data/03_Research/hydrogen_precision_spectroscopy_sources.json`: precision spectroscopy target package for future fine/Lamb/hyperfine artifacts.
- `Data/03_Research/hydrogen_lamb_shift_correction_sources.json`: empirical Lamb-shift source handoff for 1S-2S residual sizing.
- `Data/03_Research/helium_many_electron_sources.json`: neutral helium source targets and many-electron model requirements.
- `Code/01_Engine/Engine_Atomic_Hydrogen.py`: hydrogen engine and local Rydberg formula.
- `Code/03_Research/Research_Rydberg_Validation.py`: primary verifier.
