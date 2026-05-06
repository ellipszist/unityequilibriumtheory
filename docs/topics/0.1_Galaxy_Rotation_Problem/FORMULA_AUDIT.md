# Formula Audit: 0.1 Galaxy Rotation Problem

## Scope

This registry covers the current repository working-copy galaxy benchmark, the
UET galaxy engine mass and velocity relations, the local SPARC loader examples,
and the primary verifier metric. It does not claim that the topic closes the
dark-matter question for all galaxy classes.

## Formula Registry

| formula_id | relation | code surface | variables and units | constant_origin | proof_status | verification_role | failure_mode | next_hardening_step |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `GR-DATA-WORKING-COPY` | working-copy galaxy row with `R_kpc`, `v_obs`, `M_disk_Msun`, `R_disk_kpc` | `Data/03_Research/sparc_data.json`; `Research_Galaxy_Rotation.py` | `R_kpc` in kpc; `v_obs` in km/s; `M_disk_Msun` in solar masses; `R_disk_kpc` in kpc | `checked_local_reference` | `checked local` | primary benchmark input | One-point-per-galaxy working copy is not the full upstream SPARC curve package and can be mistaken for it. | Add source-lock metadata and record whether each row is a representative outer-curve point or another summary statistic. |
| `GR-DISK-ENCLOSED-MASS` | `M_disk(<r) = M_d * (1 - (1 + x) exp(-x))`, `x = r / R_d` | `Engine_Galaxy_V3.compute_velocity_at_radius` | `M_d` in solar masses; `r`, `R_d` in kpc; output mass in solar masses | `topic_derived_relation` using exponential-disk approximation | `derived` | primary engine relation | Wrong disk scale or radius convention shifts enclosed mass and all predicted velocities. | Tie `R_disk_kpc` to an explicit observational meaning and note whether it approximates scale length or effective radius. |
| `GR-BULGE-ENCLOSED-MASS` | `M_bulge(<r) = M_b` for `r >= 1`, else `M_b * r^3` | `Engine_Galaxy_V3.compute_velocity_at_radius` | `M_b` in solar masses; `r` in kpc; output mass in solar masses | `heuristic_bridge` | `heuristic bridge` | engine support term | The `1 kpc` transition and cubic inner scaling are heuristic and can distort compact galaxies. | Source-lock the bulge profile assumption or replace it with a documented profile family. |
| `GR-BARYON-DENSITY` | `rho_bar = M_bar(<r) / ((4/3) pi r^3)` | `Engine_Galaxy_V3._integrate_information_mass` | mass in solar masses; radius in kpc; density in solar-mass-per-kpc^3 | `topic_derived_relation` | `derived` | intermediate engine term | Hidden unit mismatch in `rho_pivot` makes the information scaling physically uninterpretable. | Explicitly record `RHO_UNITY` units in topic docs and verifier notes. |
| `GR-INFORMATION-RATIO` | `ratio = 1` if `rho_bar > rho_pivot`, else `(rho_bar / rho_pivot)^(-gamma)` | `Engine_Galaxy_V3._integrate_information_mass` | `rho_bar`, `rho_pivot` in common density units; `gamma` dimensionless | `heuristic_bridge` with `RHO_UNITY` and `GAMMA_UET` from central parameters | `heuristic bridge` | core UET scaling law in current engine | If `rho_pivot` or `gamma` are mis-specified, the apparent dark-component replacement can be entirely calibration-driven. | Link `RHO_UNITY` and `GAMMA_UET` to a dedicated derivation/dependency note. |
| `GR-INFORMATION-MASS` | `M_total = M_bar * (1 + (ratio - 1) * beta_galactic * 0.075)`; `M_I = max(0, M_total - M_bar)` | `Engine_Galaxy_V3._integrate_information_mass` | masses in solar masses; `beta_galactic` dimensionless | `heuristic_bridge` | `heuristic bridge` | primary engine contribution to missing-mass replacement | The hard-coded bridge factors `11.7` and `0.075` act like hidden calibration anchors. | Expose these as documented benchmark anchors with rationale and sensitivity tests. |
| `GR-VELOCITY-LAW` | `v(r) = sqrt(G_galactic * M_total(<r) / r)` | `Engine_Galaxy_V3.compute_velocity_at_radius` | `G_galactic` in galactic units; `M_total` in solar masses; `r` in kpc; output km/s | `source_locked_physics_constant` for `G_GALACTIC` plus topic-derived mass terms | `derived plus heuristic inputs` | primary predicted observable | Any inconsistency in mass units or `G_GALACTIC` units invalidates every benchmark result. | Add explicit unit line for `G_GALACTIC` in METHOD and verifier docs. |
| `GR-PRIMARY-METRIC` | `abs(v_pred - v_obs) / v_obs * 100` and average over processed rows | `Research_Galaxy_Rotation.py` | `v_pred`, `v_obs` in km/s; output percent | `topic_derived_metric` | `metric definition` | primary verifier gate | If the dataset contains only one representative radius per galaxy, average error is a summary-row benchmark, not a full curve fit. | Label the metric as a summary-point benchmark until full curve arrays are source-locked. |

## Current Formula Boundary

- The current verifier operates on a checked-in summary-row working copy, not the full
  upstream SPARC curve release.
- The engine contains explicit heuristic bridge terms and hidden benchmark anchors that
  must stay labeled as such.
- Current artifact status can support an internal benchmark statement only.
- A stronger galaxy-dynamics claim needs source-normalized curve arrays, competitor
  baseline artifacts, and explicit constant/unit provenance for `RHO_UNITY`,
  `GAMMA_UET`, and the galactic beta bridge factors.
