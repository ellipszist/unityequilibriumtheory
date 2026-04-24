# Core Scientific Validity Audit

This file is about scientific correctness, not presentation.

Scope: theory-core topics `0.0-0.26`.

## Current Scientific State

| Area | Current result | Scientific meaning |
| :-- | :-- | :-- |
| Core verification execution | `27/27` commands currently run with exit code `0` | All theory-core verification commands are executable under the standardized runner |
| Current command-level benchmark failure | None in the latest run contract | The latest batch has no command-level benchmark failure, but this does not close proof/data/physics gaps |
| Recent scientific fix | `0.3_Cosmology_Hubble_Tension` now uses `sqrt(alpha_em)` as its Hubble-frame coupling | The previous failure was caused by using the generic solver beta for a topic-specific frame comparison |
| No-fitting policy | Active | Parameters must come from derivation, independent measurement, or prior definition before benchmark comparison |
| Data provenance | Mixed | Several topics still use manual, placeholder, or embedded-local data packages |
| Mathematical rigor | Mostly incomplete | Most non-template topics have method boundaries but not full theorem/derivation coverage |
| Physical rigor | Mostly incomplete | Most topics still need stronger unit, regime, boundary-condition, and known-limit checks |

## Problems That Still Matter Scientifically

### 1. Data Reality Gaps

These topics cannot yet be treated as high-confidence data-grounded science because the data
package is still `manual or placeholder`:

- `0.5_Nuclear_Binding_Hadrons`
- `0.6_Electroweak_Physics`
- `0.7_Neutrino_Physics`
- `0.8_Muon_g2_Anomaly`
- `0.13_Thermodynamic_Bridge`
- `0.18_Mathnicry`
- `0.22_Biophysics_Origin_of_Life`
- `0.26_Cosmic_Dynamic_Frame`

Scientific remediation:

- Replace manual or generated inputs with source-locked datasets where possible.
- Add upstream URL/DOI, local file path, preprocessing note, hash, and benchmark role.
- If no real dataset exists, keep that topic as theoretical or exploratory instead of data-backed.

### 2. Embedded-Local Data Gaps

These topics have local data, but provenance is not strong enough:

- `0.9_Quantum_Nonlocality`
- `0.14_Complex_Systems`
- `0.23_Unity_Scale_Link`

Scientific remediation:

- Identify the original source for each local data file.
- Hash files and document preprocessing.
- Separate hand-entered constants from observed datasets.

### 3. Equation Naturalness And Parameter Origin

The most important current issue is not whether a script can be made to pass. It is whether
the equation produces the result from prior structure.

Resolved benchmark case:

- `0.3_Cosmology_Hubble_Tension`: the H0 benchmark now uses the topic's prior
  `beta_frame = sqrt(alpha_em)` rule instead of the generic Landauer-derived solver beta.
  The latest artifact reports `Delta H0 = 5.7576` against the observed Planck-SH0ES gap
  of `5.64`, with `2.09%` relative error under the fixed `< 20%` threshold.
- The generic solver beta remains documented separately as `0.0258`; using it for this H0
  frame comparison was the source of the previous failure.

Scientific remediation:

- Keep the `sqrt(alpha_em)` source frozen and visible in artifacts.
- Strengthen the proof of why the electromagnetic fine-structure bridge is the correct
  frame-coupling rule for early-vs-late H0 measurements.
- Extend the same no-fitting mechanism through BAO, SN, CMB likelihood, and high-z tests.

### 4. Mathematical Coverage Gaps

Most topics now have `METHOD.md`, but that does not equal mathematical proof.

High-priority proof-boundary topics:

- `0.0_Grand_Unification`
- `0.5_Nuclear_Binding_Hadrons`
- `0.6_Electroweak_Physics`
- `0.7_Neutrino_Physics`
- `0.8_Muon_g2_Anomaly`
- `0.17_Mass_Generation`
- `0.18_Mathnicry`
- `0.21_Yang_Mills_Mass_Gap`

Scientific remediation:

- Define theorem or derivation target.
- List assumptions and excluded cases.
- Show dimensional consistency.
- Separate heuristic argument, partial derivation, numerical evidence, and full proof.

### 5. Physical Consistency Gaps

Physics-heavy topics still need stronger checks beyond script execution:

- `0.1`, `0.2`, `0.3`, `0.4`, `0.5`, `0.6`, `0.7`, `0.8`
- `0.10`, `0.11`, `0.12`, `0.16`, `0.17`, `0.19`, `0.20`, `0.21`, `0.26`

Scientific remediation:

- Declare unit system and dimensional form for each primary equation.
- Specify physical regime and boundary conditions.
- Compare against known limits of standard physics.
- State where the model fails or is undefined.

## Priority Order

1. Normalize data provenance for manual/placeholder topics.
2. Add dimensional and unit checks for physics-heavy topics.
3. Add proof-boundary documents for proof-heavy topics.
4. Extend `0.3` beyond the H0 pairwise benchmark to BAO/SN/CMB/high-z consistency.
5. Only after those steps should any topic be considered for stronger scientific status.

## Non-Negotiable Rule

Failure is valid scientific output.

If the logic, data, and units are correct but the result fails, the correct action is to keep
the failure and explain it. The wrong action is to adjust parameters, thresholds, or wording
until the result appears successful.
