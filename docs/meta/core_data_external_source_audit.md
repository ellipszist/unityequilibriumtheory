# Core Data External Source Audit

Scope: topics `0.5`, `0.6`, `0.7`, `0.8`, `0.10`, `0.13`, `0.22`, and `0.26`.

This audit separates local working data from externally verifiable scientific data. A file
inside `Data/` is not enough. A topic becomes data-credible only when the source, URL/DOI,
license, local path, preprocessing step, hash, and verification role are recorded.

## Executive Finding

The weakest area is particle physics (`0.5-0.8`). These topics contain many useful working
files, but several `Download_*` scripts currently write embedded values rather than fetching
machine-readable upstream data. The next data-hardening wave should prioritize PDG/PDGLive,
PDG API or SQLite, HEPData, CERN Open Data, NuFIT, Fermilab Muon g-2, and AME/IAEA/AMDC
sources.

## Topic Ranking

| Topic | Current local data | Main weakness | Priority external sources |
| :-- | :-- | :-- | :-- |
| `0.5_Nuclear_Binding_Hadrons` | AME2020 JSON, PDG quark JSON, alpha/beta/hadron helper files | Mixed local/manual tables; AME downloader exists but output/provenance is not frozen in manifest | AME2020/AMDC/IAEA, PDG 2024/2025 API, NNDC/NuDat, HEPData QCD/hadron datasets |
| `0.6_Electroweak_Physics` | Electroweak CSV, PDG electroweak JSON, LHC Higgs JSON, W-mass helpers | `Download_Electroweak.py` embeds values instead of downloading from PDG/CERN/HEPData | PDG API, CERN/LEP EWWG records, HEPData W/Z/Higgs measurements, ATLAS/CMS public results |
| `0.7_Neutrino_Physics` | NuFit v5.2 CSV, PMNS JSON, KATRIN JSON, oscillation helpers | NuFit file is embedded; should update to NuFIT 6.0 and lock DOI/version | NuFIT 6.0, KATRIN, Super-K/T2K/NOvA/IceCube public data where available |
| `0.8_Muon_g2_Anomaly` | Muon g-2 CSV/JSON and helper module | Values are embedded; latest 2025 Fermilab final result should be added as a versioned source | Fermilab/DOE 2025 final result, PRL/Journal article, HEPData if available, Muon g-2 public pages |
| `0.10_Fluid_Dynamics_Chaos` | Internal benchmark configs/results | Good internal benchmark hygiene, but limited external fluid validation | Johns Hopkins Turbulence Database, NASA CFD validation cases, ERCOFTAC/standard CFD benchmarks |
| `0.13_Thermodynamic_Bridge` | Berut/Landauer/Cattaneo working JSON | Needs source-locked experimental thermodynamics data and raw extraction notes | Berut 2012 supplementary data, Landauer references, NIST constants, experimental heat/entropy datasets |
| `0.22_Biophysics_Origin_of_Life` | CHB-MIT/seizure/local biology working files | Domain appears mixed; biomedical provenance is not normalized | PhysioNet CHB-MIT with license, NCBI/ENA/PDB where biology mechanism requires it |
| `0.26_Cosmic_Dynamic_Frame` | Cosmicflows subset, Pioneer anomaly CSV, Laniakea JSON | Very important conceptually; current subset/source linkage is under-specified | Cosmicflows-3/4, Laniakea paper data, NASA/JPL Pioneer anomaly references, CMB dipole/frame references |

## Particle Physics Data Package Target

The particle topics should share one source-locked package instead of each topic maintaining
hand-entered constants independently.

| Package | Required fields | Used by |
| :-- | :-- | :-- |
| `pdg_particle_properties` | particle id/name, mass, width, lifetime, charge, source edition, PDG id, uncertainty, URL/API record, hash | `0.5`, `0.6`, `0.7`, `0.8` |
| `pdg_standard_model_constants` | alpha_em, alpha_s, G_F, sin2theta, mW, mZ, mH, uncertainties, edition | `0.5`, `0.6`, `0.8` |
| `ame2020_nuclear_masses` | isotope, Z, N, mass excess, binding energy, uncertainty, source URL, local raw file hash | `0.5`, `0.16` |
| `lhc_electroweak_measurements` | measurement name, experiment, energy, luminosity, value, uncertainty, HEPData record, DOI | `0.6`, `0.17` |
| `nufit_neutrino_global_fit` | version, ordering, theta12/theta13/theta23, dm2 values, delta_cp, ranges, DOI | `0.7` |
| `muon_g2_world_average` | experiment, run, a_mu, uncertainty, theory comparator, source DOI/URL, version | `0.8` |

## Data Quality Gates

1. `local working copy`: file exists in repo, but source and hash are incomplete.
2. `source referenced`: URL/DOI exists, but raw download and preprocessing are not reproducible.
3. `source locked`: raw file can be downloaded or manually placed from a named source; hash is recorded.
4. `benchmark linked`: verification script explicitly uses the source-locked file.
5. `reproducible data package`: manifest, hashes, license, preprocessing, and artifact are complete.

No topic should be upgraded above `source referenced` if the script writes embedded values and
does not fetch or verify an upstream file.

## Immediate Remediation Plan

1. Create a shared `docs/data/external/particle_physics/` package or equivalent metadata
   registry so `0.5-0.8` do not duplicate constants.
2. Replace embedded-value downloaders with honest fetchers or explicitly rename them as
   `write_reference_snapshot.py`.
3. Start with machine-readable PDG API/SQLite for particle masses and Standard Model constants.
4. Add NuFIT 6.0 as a versioned source for `0.7`.
5. Add Fermilab final Muon g-2 2025 result as a separate source version for `0.8`; preserve
   2021/2023 values as historical comparison rows.
6. Keep every future observational dataset under observer-frame notes: instrument, experiment,
   energy/regime, calibration assumptions, and whether the value is directly measured or
   model-inferred.

## Scientific Caution

The user-frame critique applies to data too: every external dataset must declare its
experimental or observer frame before being compared to UET equations. For particle physics,
that means collider energy, detector, luminosity, reconstruction assumptions, and Standard
Model fit assumptions. For cosmology, it means observer frame, epoch, light-delay, calibration
ladder, and model-inference assumptions.

