# Formula Audit: Nuclear Binding Hadrons

## Scope

This registry covers the calculation paths that currently support topic `0.5`.
It separates source-backed benchmark gates from heuristic bridge terms and diagnostic-only
hadron/QCD scripts.

## Formula Registry

| formula_id | relation | code surface | variables and units | constant_origin | proof_status | verification_role | failure_mode | next_hardening_step |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `T05-SEMF-001` | `B = a_vol*A - a_surf*A^(2/3) - a_coul*Z*(Z-1)/A^(1/3) - a_asym*(N-Z)^2/A + delta`; total path adds entropy and Yukawa components separately | `Code/01_Engine/Engine_Nuclear_Binding.py`; `Data/03_Research/semf_coefficient_provenance_gate.json` | `A`, `Z`, `N` dimensionless counts; `B` MeV; coefficients in MeV; `delta` MeV; final `B/A` MeV per nucleon | `checked_local_reference` for SEMF coefficients; `heuristic_bridge` for UET entropy correction; `heuristic_bridge` for Yukawa add-on | `checked local` for selected heavy-nucleus benchmark; not first-principles | primary gate in `Research_Nuclear_Binding_SourceLocked.py`; parameter-free wording blocked by SEMF coefficient gate | Light nuclei can fail badly; additive correction may hide fitted/heuristic behavior if described too strongly. | Source-lock coefficient provenance and rerun the primary verifier so SEMF-only versus correction metrics become current artifact state. |
| `T05-COMP-001A` | `binding_energy_components(A,Z,beta_nuc)` returns SEMF, entropy, Yukawa, and total components | `Code/01_Engine/Engine_Nuclear_Binding.py`; `Code/03_Research/Research_Nuclear_Binding_SourceLocked.py` | component energies MeV; component `B/A` values MeV per nucleon; residuals percent | `checked_local_reference` for SEMF; `heuristic_bridge` for correction terms | `diagnostic decomposition` | current strict artifact decomposition lane for selected subset | The current heavy selected-subset artifact shows SEMF-only mean error lower than the total path after correction terms, so the correction lane cannot be described as an improvement. | Source-lock SEMF coefficients and define whether the Yukawa term is baseline physics, UET bridge, or a separate diagnostic lane. |
| `T05-YUKAWA-002` | `correction = 10.0 * exp(-mu*R) / R`, `mu = m_pion / hbar_c`, `R = r0*A^(1/3)` | `Code/01_Engine/Engine_Nuclear_Binding.py` | `m_pion` MeV; `hbar_c` MeV*fm; `R` fm; `mu` 1/fm; correction MeV-like before multiplication by `A` | `source_locked_physics_constant` for pion mass convention; `heuristic_bridge` for coefficient `10.0` and additive use | `heuristic bridge` | part of primary binding engine | The coefficient and additive placement can create apparent heavy-nucleus success while failing outside domain. | Record sensitivity of heavy-nucleus pass rate to the Yukawa coefficient and justify or demote the term. |
| `T05-PAIR-003` | `delta = +/- a_pair/sqrt(A)` for even-even / odd-odd nuclei | `Code/01_Engine/Engine_Nuclear_Binding.py` | `A` dimensionless; `delta` MeV; parity of `Z` and `N` dimensionless | `checked_local_reference` from SEMF convention | `checked local` | primary binding engine | Pairing convention affects small/light nuclei strongly and must not be treated as UET-specific derivation. | Document coefficient source and compare against SEMF-only baseline. |
| `T05-PROTON-RADIUS-004` | `r_p = 0.841 fm` | `Code/01_Engine/Engine_Nuclear_Binding.py` | `r_p` fm | `source_locked_benchmark_input` / benchmark anchor from muonic-hydrogen-style value | `benchmark anchor` | primary gate against `Data_Proton_Radius.json` | The engine returns the target-like value directly, so this is not an independent prediction. | Replace with derived relation or keep it labeled as benchmark-anchor compatibility only. |
| `T05-AME-GATE-005` | `relative_error = abs(predicted_BE/A - observed_BE/A) / observed_BE/A * 100` | `Code/03_Research/Research_Nuclear_Binding_SourceLocked.py` | `predicted_BE/A`, `observed_BE/A` MeV per nucleon; error percent | `source_locked_benchmark_input` from AME2020 raw-derived subset | `identity` for metric; source-backed benchmark gate for data | primary verifier threshold: heavy nuclei `A >= 16` under `15%`, proton radius under `5%` | Passing selected heavy nuclei does not imply full AME table pass. | Keep strict subset gate separate from full-table diagnostic in README and paper drafts. |
| `T05-FULLTABLE-006` | table-wide residual distribution over parsed AME2020 rows | `Code/03_Research/Research_Nuclear_Binding_FullTable_Diagnostic.py` | AME2020 parsed `A`, `Z`, `BE_keV`; derived `BE/A` MeV per nucleon; error percent | `source_locked_benchmark_input` from `docs/data/external/particle_physics/ame2020/mass_1.mas20` | `checked local` diagnostic | diagnostic-only artifact | Light nuclei show very weak behavior; using only selected subset can overstate robustness. | Use diagnostic artifact in limitations and decide whether a separate light-nuclei engine should own `A < 16`. |
| `T05-LIGHT-007` | deuteron: `(hbar_c*kappa)^2/(2*mu)`; triton/He3/He4 use overlap, Coulomb, and saturation factors | `Code/01_Engine/Engine_Light_Nuclei.py` | `hbar_c` MeV*fm; `kappa` 1/fm; `mu` MeV; binding MeV; factors dimensionless | `checked_local_reference` for constants; `heuristic_bridge` for overlap/saturation terms | `heuristic bridge` | diagnostic-only for light nuclei | Uses empirical-looking constants (`0.232`, `0.95`, `0.762`, `1.3`, `1.16`) and should not be merged into heavy-nucleus pass claims. | Source-lock constants or classify as fitted/heuristic; connect to separate verifier if retained. |
| `T05-HADRON-008` | meson/baryon mass as sum of constituent masses with constituent shift `DELTA_M_UET = 330*beta` | `Code/01_Engine/Engine_Hadron_Model.py`; `Data/03_Research/pdg_hadron_qcd_source_mapping_gate.json` | quark masses MeV/GeV depending on PDG row; hadron mass MeV; `beta` dimensionless | PDG 2025 records found but not integrated; `heuristic_bridge` for constituent shift and strangeness factor | `heuristic bridge` | diagnostic-only | Constituent shift can act as hidden benchmark anchor; scripts still use embedded snapshots even though PDG records are now mapped. | Generate a topic-local PDG-derived package and add a dedicated hadron-mass verifier artifact. |
| `T05-GMOR-009` | `m_pi = sqrt(abs(-(m_u+m_d)*condensate/F_pi^2))` | `Code/01_Engine/Engine_Hadron_Model.py` | `m_u`, `m_d`, `F_pi`, `sigma_qq` MeV; condensate MeV^3; result MeV | `checked_local_reference` from PDG/lattice-QCD-style constants | `checked local` | diagnostic-only | Constants are embedded and not yet tied to local source files/hashes. | Source-lock PDG/FLAG values or move this row to checked external benchmark status. |
| `T05-QCD-010` | `alpha_s(Q) = 1/(b0*ln(Q^2/Lambda^2))`; UET variants multiply or alter `Lambda` | `Code/01_Engine/Engine_QCD_Bridge.py`; `Data/03_Research/pdg_hadron_qcd_source_mapping_gate.json` | `Q`, `Lambda` GeV; `alpha_s` dimensionless; `n_f` active flavors | embedded PDG-like table; source-mapping gate records that alpha_s still needs a dedicated PDG query/package | `diagnostic blocked` | diagnostic-only | `alpha_s_uet_v2` currently treats a float as a dict (`QCD_PARAMS[...]["value"]`), so that branch is not reliable. | Fix the data shape bug, source-lock PDG alpha_s inputs, and define whether this is baseline QCD or a UET correction. |
| `T05-CONF-011` | proof script checks `0.9 < proton_mass_gev < 1.01` after hadron engine step | `Code/02_Proof/Proof_Color_Confinement.py` | proton mass GeV from diagnostic hadron model | `heuristic_bridge` | `diagnostic blocked` | diagnostic-only | Script returns `True` regardless of pass/fail print path, so it cannot certify confinement. | Make proof command return real pass/fail and label as diagnostic until derivation exists. |

## Unit and Data Discipline

- AME2020 binding inputs are source-backed through `docs/data/external/particle_physics/ame2020/mass_1.mas20`.
- Strict pass/fail applies only to selected heavy nuclei (`A >= 16`) plus proton radius.
- Full-table AME2020 behavior is diagnostic; it is not a pass/fail proof of general nuclear binding.
- Hadron/QCD constants remain partly embedded snapshots and should not be reused as source-locked UET constants.
- SEMF coefficients and Yukawa constants are now tracked by `Data/03_Research/semf_coefficient_provenance_gate.json`; that gate blocks parameter-free and first-principles wording until a source package and term policy exist.
- PDG 2025 quark and several hadron mass records are now mapped in `Data/03_Research/pdg_hadron_qcd_source_mapping_gate.json`, but this is not yet verifier integration.

## Current Formula Status

- Primary nuclear-binding gate: `checked local` for selected heavy nuclei.
- Light nuclei: `heuristic bridge` / diagnostic.
- Proton radius: benchmark anchor, not independent prediction.
- Hadron and QCD bridge: diagnostic-blocked until source-backed data and verifier contracts are added.
- Confinement proof script: diagnostic-blocked; current return behavior is not a proof gate.

## Next Hardening Steps

1. Source-lock SEMF coefficients and decide whether the Yukawa term is baseline physics, UET bridge, or a separate diagnostic lane.
2. Generate a topic-local PDG-derived hadron/quark package from the mapping gate and add a dedicated verifier.
3. Fix `Engine_QCD_Bridge.alpha_s_uet_v2` data-shape bug and add PDG alpha_s source mapping before using it in any verifier.
4. Change `Proof_Color_Confinement.py` to return a real pass/fail status.
5. Add a dedicated light-nuclei verifier or keep `A < 16` explicitly outside the heavy-nucleus claim.
