# Data Manifest

Current data reality status: manifested real dataset for NIST/CODATA working copies used by the primary hydrogen-spectrum verifier.

## Primary Verifier Inputs

| Item | Local path | Bytes | SHA-256 | Source | DOI / URL | Units | Benchmark role | Provenance status |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- | :-- |
| NIST hydrogen spectrum working copy | `Data/03_Research/nist_hydrogen_spectrum.json` | 2224 | `f355dd9aa2ffb65eb53e1e5140fa48580fc760e67c596a41a38cfb9a0210a4e8` | NIST Atomic Spectra Database v5.11 | DOI `10.18434/T4W30F`; URL `https://physics.nist.gov/asd` | vacuum/air wavelength `nm`; frequency `THz`; energy `eV` | primary spectral-line benchmark | Source label and DOI/URL present; verifier records local SHA256. |
| CODATA atomic constants working copy | `Data/03_Research/codata_2018_atomic.json` | 1582 | `31c982eedd02900d8fb05c1b925d56fb3733ddae877ec304becff6465b9dbf31` | CODATA recommended values | DOI `10.1063/5.0064853` | `R_H`, `R_infinity` in m^-1; `a_0` m; energies/constants SI | primary constant benchmark | Source label and DOI present; verifier records local SHA256. |
| Hydrogen-like ion source package | `Data/03_Research/hydrogen_like_ion_spectrum.json` | 3406 | `a80872ec987970f0d12d84dcafce44074817649895117ffc3c9f6eb76ee2636f` | NIST He II handbook row; Li III paper row citing NIST; CODATA/NIST mass constants | NIST He URL; DOI `10.1088/2058-6272/abfea2`; CODATA DOI `10.1063/5.0064853` | wavelengths nm/A; masses kg/u | provisional selected hydrogen-like ion benchmark | He II is direct NIST handbook; Li III still needs direct ASD capture before non-provisional source-lock. |
| Hydrogen precision spectroscopy source package | `Data/03_Research/hydrogen_precision_spectroscopy_sources.json` | 2756 | `8172adc3f8c784ff37a0f13be3a380e9937baca80d4c84943d57b88b2807b5ab` | 1S-2S measurement, Lamb-shift summary, 21 cm reference | DOI `10.1103/PhysRevLett.107.203001`; source URLs recorded in JSON | Hz/MHz | precision source package | Source package plus nonrelativistic and leading Dirac 1S-2S baseline diagnostics; QED/recoil/proton-radius/hyperfine model and residual gate remain blocked. |
| Hydrogen Lamb-shift handoff source package | `Data/03_Research/hydrogen_lamb_shift_correction_sources.json` | 2540 | `f723593f9c4dd3d6b06193e032d5083405348572026a3e0b37e7ee7f18cee77a` | 1S Lamb-shift measurement record; NIST critical compilation for 2S Lamb-shift value | OSTI URL; NIST PDF URL recorded in JSON | MHz/Hz | empirical Lamb-shift handoff package | Empirical source handoff only; primary page spans, convention audit, QED decomposition, recoil, and proton-size model remain blocked. |
| Hydrogen 21 cm hyperfine source package | `Data/03_Research/hydrogen_hyperfine_21cm_sources.json` | 2314 | `0d0e59fa85646d2a3f70b0824befff7cde8faf3776e62d43a7557a95bc1862be` | NIST critical compilation; NASA hydrogen maser clock record | NIST PDF URL; NTRS URL recorded in JSON | Hz/MHz; m/cm | hyperfine source bookkeeping package | Source-lock and wavelength bookkeeping only; Fermi-contact Hamiltonian, magnetic moment convention, recoil/QED, and proton-structure model remain blocked. |
| Neutral helium source package | `Data/03_Research/helium_many_electron_sources.json` | 2747 | `1c53074cb3d70824505e1d0e2fbd248fe7d519c96b5d50838cb26ab3da117d06` | NIST Handbook of Basic Atomic Spectroscopic Data, strong lines of helium | URL `https://physics.nist.gov/PhysRefData/Handbook/Tables/heliumtable2_a.htm` | wavelengths nm/A; relative intensity | neutral helium / many-electron source package | Source package only; two-electron Hamiltonian, correlation treatment, term mapping, and residual gate remain blocked. |

## Secondary Inputs

| Item | Local path | Bytes | SHA-256 | Source | Units | Role | Use policy |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- |
| Hydrogen level working copy | `Data/03_Research/hydrogen_spectra_data.json` | 688 | `cd3554bd19ef3f47b2469bc88d81e97497eda4b93b6f144b43ab2043c5fd0845` | topic-local rounded level package with NIST ionization-energy anchor | energy `eV` | rounded level-energy benchmark | Used by the primary artifact as a rounded `n=1..8` benchmark; direct per-level ASD precision remains pending. |
| NIST hydrogen visible CSV | `Data/NIST_Hydrogen_Visible.csv` | 3787 | `633f28187ef79e8502e9c89ed3099d25ebe5283027c9d0abe2fcd36ff04888b9` | NIST local visible-line copy | wavelength fields in CSV | engine demo input | Not used by the primary artifact. |
| NIST helium visible CSV | `Data/NIST_Helium_Visible.csv` | 3787 | `525f4b49a906ffa5b12bac3776f22aac1015e6468fba187589e5affc2b24ffc3` | NIST local visible-line copy | wavelength fields in CSV | future helium/many-electron lane | Excluded from current claim scope. |
| NIST downloader helper | `Data/Download_NIST.py` | 2301 | `9207378b83f9fa32ff32795d25e7ac900f943516c57106df05e2736495b0d03e` | topic-local helper | n/a | data/source helper script | Not upstream source. |
| Data helper script | `Data/03_Research/download_data.py` | 6466 | `c12cbe85556f5eaedc0dfa703b6ab5dad0c16e6b71a8a3ed12fe9580d57c9a19` | topic-local helper | n/a | data/source helper script | Not upstream source. |
| Reference helper script | `Data/03_Research/download_references.py` | 6756 | `6c502427cc1f9bfd7263726e8f8bfc252045378ab0ffad1802d2304e285675ee` | topic-local helper | n/a | reference helper script | Not upstream source. |
| Topic source evidence intake stub | `Data/03_Research/source_evidence_intake_stub.json` | 2573 | `ebed455ba75471ce9fd70eaf693a76d230cf9dc9ae6a83d534403a71a1ff85fc` | Generated by primary verifier | n/a | provenance workflow intake | Organizes source-review work before claim upgrades, including level-energy, hydrogen-like ion, precision source-lock, and neutral-helium source-lock. |
| Topic source evidence readiness matrix | `Data/03_Research/source_evidence_readiness_matrix.json` | 3101 | `13d0999298b98a7cfc5e9b975463e7a99b0c7eb98c8f6ae68dcae0b04d33d6d0` | Generated by primary verifier | n/a | source-review readiness gate | Hydrogen level-energy, hydrogen-like ion, precision, and neutral-helium source packages are ready for review; precision and many-electron model artifacts remain blocked. |
| Topic branch claim gate | `Data/03_Research/branch_claim_gate.json` | 3797 | `14ccf4df1fd0ae6dcd54af0ab3bb28f3c8dd54c638c81dd565dffc866c15f62d` | Generated by primary verifier | n/a | claim ceiling for hydrogen and future atomic branches | Prevents hydrogen benchmark, rounded level benchmark, formula bridge, selected ion benchmark, precision source package, and neutral-helium source package from inflating full atomic-theory claims. |
| Atomic formula bridge manifest | `Data/03_Research/atomic_formula_bridge_manifest.json` | 5858 | `2b63bb601e835800826ce88af4b43cf603d58e44f29d317da9a01d202cdbad39` | Generated by primary verifier | n/a | Bohr/de Broglie/Rydberg bridge manifest | Maps inherited standard formulas, nonrelativistic/Dirac/Lamb-handoff 1S-2S precision gaps, 21 cm source bookkeeping, and UET dependencies without claiming first-principles derivation. |
| Primary verifier script | `Code/03_Research/Research_Rydberg_Validation.py` | 71118 | `1680183e96c983cb8d16445507fefc046fc28a1632d0a86ee5fc2e32228fc5d2` | Topic-local verifier | n/a | hydrogen Rydberg benchmark verifier | Generates primary artifact, source gates, formula bridge, rounded level benchmark, selected ion benchmark, precision source gate, 1S-2S baseline gates, Lamb handoff gate, 21 cm source gate, and neutral-helium source gate. |
| Primary verifier artifact | `Result/artifacts/0_20_atomic_physics_verification.json` | 42681 | `6680403b5f97c7c4d767a6e85a66d38a34967a92269f4ef2a971523686be2713` | Generated by primary verifier | n/a | hydrogen Rydberg benchmark artifact | `PASS` for hydrogen, rounded level-energy, and provisional selected He+/Li2+ benchmark; nonrelativistic/Dirac/Lamb-handoff 1S-2S residuals and 21 cm source bookkeeping are computed but first-principles QED/hyperfine-incomplete; precision spectroscopy and neutral helium are source-ready/model-blocked; controller remains `WARN`. |

## Preprocessing

- Primary verifier uses vacuum wavelengths from the NIST hydrogen working copy.
- It computes the Rydberg geometric term from parsed transitions.
- It compares predicted vacuum wavelengths from CODATA `R_H` against NIST vacuum wavelengths.
- It writes a formula bridge manifest that records inherited photon, de Broglie, Bohr, hydrogenic, and Rydberg formula roles plus cross-topic UET dependencies.
- It compares rounded hydrogen `n=1..8` energy rows against the NIST ionization-energy anchored `E_n = -13.5984/n^2` relation.
- It computes selected He+ and Li2+ reduced-mass hydrogenic residuals against source-referenced EUV rows.
- It records 1S-2S, Lamb shift, and 21 cm hyperfine as precision source targets, then computes nonrelativistic, leading Dirac, empirical Lamb-handoff 1S-2S residuals, and 21 cm wavelength bookkeeping.
- It records neutral He I visible rows as many-electron source targets without computing neutral-helium residuals.
- Air wavelengths are preserved in the data but not used in the primary metric.
- Topic-level source-evidence and branch-claim gate files keep the accepted hydrogen benchmark separate from blocked precision and many-electron claims.

## Data Policy

- Raw external spectral source captures may later move to `docs/data/external/...`; this topic must still record exact local paths and hashes.
- Hydrogen benchmark, rounded level-energy benchmark, formula bridge, selected He+/Li2+ reduced-mass results, precision source package, 1S-2S baseline/handoff residual diagnostics, 21 cm source bookkeeping, and neutral-helium source package cannot be used as evidence for UET-derived `R_H`, broad hydrogen-like ion validation, neutral-helium residual validation, first-principles QED, hyperfine Hamiltonian correction, periodic-table spectra, or many-electron claims.
