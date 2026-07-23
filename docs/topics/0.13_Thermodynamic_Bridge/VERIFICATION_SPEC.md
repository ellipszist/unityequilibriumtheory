# Verification Spec

- Primary command:
  - `.venv\Scripts\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Inputs:
  - `Data/03_Research/__init__.py`
  - `Data/03_Research/berut_2012.json`
  - `Data/03_Research/cattaneo_data.json`
  - `Data/03_Research/experimental_data.py`
  - `Data/03_Research/landauer_source_lock.json`
  - `docs/data/external/thermodynamics/landauer/berut_2012/source_record.json`
  - `docs/data/external/constants/codata/si_2019_exact_constants.json`
- Baseline:
  - Landauer exact-constant identity at 300 K.
  - Jun-style measured erasure cost must remain above the Landauer lower bound.
  - Bekenstein, Unruh, and Hawking relations are formula-consistency checks only.
  - Cattaneo synthetic heat-flux data is not part of the primary acceptance gate.
- Reported metrics:
  - `landauer_engine_vs_codata_relative_error`
  - `jun_2014_ratio_to_landauer_lower_bound`
  - `unruh_temperature_earth_g_K`
  - `hawking_temperature_solar_mass_K`
  - `bekenstein_hawking_entropy_solar_mass_planck_units`
  - input file SHA-256 identities and optional plot artifact status
- Fixed threshold:
  - `landauer_engine_vs_codata_relative_error <= 1e-12`
  - `jun_2014_ratio_to_landauer_lower_bound >= 1.0`
  - all three primary tests must return true
  - optional plot artifacts should render; plot failure downgrades artifact status to `WARN`
  - topic-derived Berut numeric rows keep this topic from claim class `A/B` until raw/supplemental table provenance is archived
- Artifact target:
  - Result/artifacts/0_13_thermodynamic_bridge_verification.json
- Interpretation:
  - Treat `PASS` as formula/lower-bound consistency only.
  - Treat `WARN` as scientifically usable for hardening but not paper-ready; the present WARN is expected while Berut numeric values remain topic-derived summaries.
  - Do not upgrade claim language to "solved", "verified UET", or "exact bridge" until source-locked external data, uncertainty propagation, and cross-topic dependency proof are complete.

## Core Thermodynamic Constraint Gate

Run:

```powershell
.venv\Scripts\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Core_Thermodynamic_Constraint_Gate.py
```

Artifact:

- `Result/artifacts/0_13_core_thermodynamic_constraint_gate.json`

Required interpretation:

- `foundation_constraint_export_gate`: only the Landauer lower bound and standard thermodynamic/gravity identities may pass as class-C constraints.
- `landauer_coefficient_non_derivation_gate`: Landauer must remain an imported bound and must not be used to derive `beta` or core transport coefficients.
- `cattaneo_simulation_control_gate`: the Cattaneo result must remain explicitly simulation-only and non-external.
- `trace_phi_observable_separation_gate`: normalized `Phi` and `R` must not be relabeled as thermal observables or feedback without a dimensional map.
- `row_controller_preservation_gate`: the Berut, Jun, Hong, and Peterson source-row blockers must remain unchanged by this dependency packet.
- `uet_bridge_derivation_gate`: remains `BLOCKED` until a non-circular derivation and proxy-to-SI mapping exist.
- `thermal_pilot_physical_gate`: remains `BLOCKED` while pre-arrival leakage or external-source readiness fails.
- `core_eos_transport_entropy_gate`: remains `BLOCKED` until charge EOS, covariant transport, entropy current, and dissipative-Bianchi completion are derived.
- `topic_promotion_gate`: remains `BLOCKED`; constraint exports and synthetic controls cannot promote the topic tier.

Current controlling blocker:

- `topic_0_13_constraint_only_eos_transport_entropy_bridge_missing`

