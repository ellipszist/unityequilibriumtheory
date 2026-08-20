# Data Manifest

Current data reality status: "real source referenced with topic-derived working copies"

External-source audit status: `Berut/CODATA source records pinned; raw experimental table archive still open`.

Priority remediation:

- Archive or machine-transcribe Berut 2012 experimental Landauer-principle raw/supplementary values.
- Extend the CODATA/NIST constants record beyond exact SI constants if measured constants become acceptance gates.
- Separate historical theoretical references from experimental datasets used in verification.
- See `docs/meta/core_data_external_source_audit.md` for the cross-topic data-hardening plan.

| Item | Local path | Source | Unit convention | Bytes | SHA-256 | Benchmark role | Provenance status |
|:--|:--|:--|:--|--:|:--|:--|:--|
| Ding 2022 PMC OA numeric-input availability | `Data/03_Research/ding_2022_pbte_numeric_input_availability_package.json`; `Data/03_Research/raw/ding_2022_pmc_s3_inventory.xml`; `Data/03_Research/raw/ding_2022_supplementary_information.pdf`; `Data/03_Research/raw/ding_2022_supplementary_materials_2.pdf`; `Data/03_Research/raw/ding_2022_supplementary_materials_3.pdf`; `docs/core/artifacts/t13_ding_pbte_numeric_input_availability_audit.json` | PMC OA API, complete `PMC8755757.1/` S3 prefix, object metadata, full text, and all three supplementary PDFs captured/reviewed 2026-08-15 | source inventory only; required `C_src` units J m^-3 K^-1 | 3780 inventory bytes | inventory `6f86e82611321053b3afd9b548f6e4a314ef03fd753ab2706775e2bc8c551672`; package `7d660de4a984e313b60df545642fa1743da8921cdedeaf5908297f6c13d8e961`; audit `2811cfd9ef4f0218cc5696a1a7ce5a4591a4a8012c28dad118a5b6171b3b67fa` | Source acquisition decision; no calibration consumed | `PASS_SCOPED_OA_NUMERIC_INPUT_AVAILABILITY_NO_GO`; all supplementary archive records are hash-verified, but the official OA route still lacks reproducible PBTE numeric inputs while author request or independent reproduction remains open. |
| Ding 2022 PBTE energy-temperature source mapping | `Data/03_Research/ding_2022_pbte_energy_temperature_source_package.json`; `Data/03_Research/raw/ding_2022_supplementary_information.pdf`; `docs/core/artifacts/t13_ding_pbte_energy_temperature_mapping_audit.json` | Ding et al., Nature Communications 13, 285 (2022), Supplementary pp.3-5, Eqs. S1-S10; DOI `10.1038/s41467-021-27907-z`; PMC `PMC8755757` | `g_mu` and `Delta_u_ph` J m^-3; `C_src` J m^-3 K^-1; `Delta_Tq` K | 1893976 raw bytes | PDF `a50c1a6347775de72f705f4395507d3136cbf4e5cadfb6638caca2876c52b8f7`; package `9f6b8d31ba2d7a6e56d6a323581bc6aecb91c6d0e61064d62a3972ee0e2c0d6f`; audit `32d132bb695d62f52be337ce0cced4c57c43df13ea96b082c6f9ee416d0aed73` | Derived standard-PBTE formula and TTG-observable mapping; no numeric calibration or holdout consumption | `PASS_SOURCE_FORMULA_MAPPING_NUMERIC_C_OPEN`; numeric `C_src(T)`, convergence/uncertainty, `e0`, and base `Phi` mapping remain open. |
| Georgia Tech graphite c_p source and dependency no-go | `Data/03_Research/gatech_gen3csp_graphite_source_package.json`; `docs/core/artifacts/t13_gatech_volumetric_cp_independence_audit.json` | Georgia Tech Gen3 CSP graphite page, uncertainty method, and archived `Graphite.xlsx` row A3:G3 | `c_p` J g^-1 K^-1; D mm^2 s^-1; k W m^-1 K^-1; assumed density g cm^-3 | 11234 raw bytes | raw `baa7f6181fa3d5521fc594cb2c832308927bc77dbac89c43b373bc304eaa6900`; package `2635be1d91f35c9be6fd36d14a9e4d04384f158dd90340b59c5d7fa3f277bd51`; audit `7e9e858548cac1843c6bf5d405aeb192226ea79ef69a7dd5c3dc1e55d3cf8c6e` | Independent `c_p` source anchor and source-dependency audit; no calibration consumed | `PASS_SOURCE_CP_95CI_CV_OPEN` plus `PASS_SCOPED_SOURCE_INDEPENDENCE_NO_GO`; reported k is derived from D, c_p, and assumed density, so direct volumetric `c_v` or independent same-grade inputs remain required. |
| Matter-space second-sound source package | `Data/03_Research/matter_space_second_sound_source_package.json` | Metadata anchors: Ding et al. 2022 DOI `10.1038/s41467-021-27907-z`; Huberman et al. 2019 DOI `10.1126/science.aav3548`; McNelly et al. 1970 DOI `10.1103/PhysRevLett.24.100`; Xie et al. 2026 DOI `10.1038/s41467-026-70807-3` | Source-reported K, micrometre, time/TTG context; no local numeric rows | 5973 | `118ddf77864d74fe1c662e447af41705e544cfae4a8523cbe802560b6d4279f6` | Future external second-sound intake; 2026 graphite source locked as holdout | `BLOCKED`: metadata only, no local raw numeric source, extraction uncertainty, preprocessing, or dimensional `Phi` observable map; no fitting allowed. |
| Thermal source review and observable map | `Data/03_Research/matter_space_thermal_source_review.json`; `THERMAL_SOURCE_OBSERVABLE_MAPPING_SPEC.md` | Primary Nature source pages for Ding 2022 and Xie 2026; DOI/URL and section locators recorded | normalized TTG dimensionless; calibrated quasi-temperature K; heat flux/entropy units not active | generated | recorded in readiness artifact | Defines the standard quasi-temperature TTG operator and the UET normalized candidate operator | `PASS_WITH_BLOCKED_DIMENSIONAL_AND_DATA_LANES`: external identities reviewed, but local numeric package and `alpha_Phi_K` remain missing. |
| Thermal observable-map readiness artifact | `Result/artifacts/matter_space_thermal_observable_map_readiness.json` | Generated by `docs/scripts/audit/audit_thermal_source_observable_mapping.py` | dimensionless normalized operator; K only after independent calibration | generated | records source-package and source-review hashes | Machine-readable source/data/unit gate | `DEFINITION_ONLY / SIMULATION_ONLY`; not an external validation artifact. |
| Matter-space thermal preregistration | `Data/03_Research/matter_space_thermal_preregistration.json` | Topic-local locked synthetic protocol | normalized only | 2486 | `f0cb51e720c8c4813973d4227566373b9f3c473308346974e048f49056792fcd` | Locks controls, parameter grid, seed, thresholds, and holdout policy before the initial run | Workflow control; no external numeric inputs and no parameter fitting. |
| Matter-space numerical amendment 001 | `Data/03_Research/matter_space_thermal_numerical_amendment_001.json` | Post-diagnostic record linked to the failed locked-`dt` artifact hash | normalized `dt` only | 1377 | `a30b639531fda62983b380051b4ca86c791cda772b0440b3113c5ca7daf5f85e` | Discloses the numerical refinement used for the ledger gate | Not blind preregistration; changes only `dt`, with physics parameters and thresholds unchanged. |
| Matter-space thermal control artifact | `Result/artifacts/matter_space_thermal_control.json` | Generated by `Research_Matter_Space_Thermal_Control.py`; hashes preregistration, amendment, source package, core dependency, CSV, and figures | normalized only; `Phi` and `R` have no SI observable identity | 10757 | `2480561487165ce0a5c7f98ff5302d120cea23afb59679845cc7631c2b22f1d9` | Five-way synthetic comparator and internal ledger/causal diagnostic | `SIMULATION_ONLY / FAIL`: pre-arrival leakage and external-source gates remain failed; not external validation. |
| package marker | `Data/03_Research/__init__.py` | Topic-local package marker | n/a | 37 | `814f2a4f940ffae9d721f3dba46fb6c16d15a856819844b1531bbc9b50befe62` | Allows import of topic data package | Local infrastructure file. |
| Landauer working copy | `Data/03_Research/berut_2012.json` | Berut et al. 2012 Nature, DOI `10.1038/nature10872`; manually copied summary values | `T_K` kelvin; `kT_ln2_J` joule; measured heat joule | 319 | `76e0218ac3944ead0399d501d39c3e335d781a0f503647c4ebb4707ae2e77500` | Lower-bound consistency check for `E_min = k_B T ln 2` | Source-labeled, but not an archival raw/supplement copy. |
| Landauer source record | `docs/data/external/thermodynamics/landauer/berut_2012/source_record.json` | Nature article page and DOI `10.1038/nature10872` checked on 2026-04-30, preview-surface-inspected on 2026-06-16, exact Figure 3 preview locator mapped on 2026-06-21, and official Figure 3 PPT route download-tested on 2026-06-22 | source metadata; heat units declared as J or kT in topic-derived data | 8560 | `2333b9595ba0a4623162c373c7be8a5dac658892eb672fb630c2f9b22418aa38` | Upstream provenance anchor for Landauer lower-bound benchmark | External source record present; the currently visible Nature surface now exposes the official Figure 3 PPT route, binary identity, embedded raster candidates, a digitization protocol, automated panel-frame candidates, and semantic asset review selecting `jpeg_2`, but Berut remains below source-normalized row status until the relevant quantitative panel is selected, axis ticks and point/curve selections are mapped, and numeric transcription or a stronger source-data surface is attached. |
| Jun source record | `docs/data/external/thermodynamics/landauer/jun_2014/source_record.json` | Jun et al. 2014 PRL, DOI `10.1103/PhysRevLett.113.190601` | source metadata; runtime energy conversion must be explicit | 3575 | `ebbbb3990f545440bd1e020cace361ca1ee6f867b45c18dba469d47bdc4663a1` | Source identity anchor for the feedback-trap Landauer branch | Source record plus local arXiv transcription; it records the source-facing `0.71 +/- 0.03 kT` asymptotic-work summary, which the verifier converts into a first-pass Jun interval; the legacy `0.028 eV` runtime row is demoted to legacy context outside active Jun logic, while final PRL parity/APS access for the captured Table I/Figure 4 fit target remains open. |
| Jun source-summary locator | `Data/03_Research/jun_2014_source_summary_locator.json` | Topic-generated locator for Jun et al. 2014 arXiv/PRL source-summary surface | kT summary quantity plus eV runtime conversion boundary | 3046 | `2b50f39cbc292c115f8206b44e4ebd8e3882957e96f9403bf1cc16a8f25f35d8` | Captures Table 1/Figure 4/Eq. (3) as the fit target for the active Jun summary interval | Workflow/control artifact only; closes generic summary-target identity and now points to the local transcription artifact, but leaves final PRL parity/APS access resolution and row-level normalization open. |
| Jun source-summary transcription | `Data/03_Research/jun_2014_source_summary_transcription.json` | Topic-generated local transcription of arXiv:1408.5089 page-4 Table I/Figure 4 summary surface | kT source summary plus runtime eV conversion boundary | 4133 | `ec9fc90a2b59ab9501e73fe55ed87b0fdcd12fdf74b2195bc3b91bebeb90aa83` | Captures the active full-erasure `0.71 +/- 0.03 kT` row as local machine-readable source-summary evidence | Workflow/control artifact only; closes local arXiv transcription for the active summary row but leaves final PRL parity/APS access resolution open. |
| Hong candidate source record | `docs/data/external/thermodynamics/landauer/hong_2016/source_record.json` | Hong et al. 2016 Science Advances candidate branch; Crossref confirms the DOI metadata anchor and an accessible same-author arXiv precursor now exposes primary-facing numeric text, but a direct final article-page archive is still not stored locally | source metadata; candidate identifiers include `DOI 10.1126/sciadv.1501492`, `PMID 26998519`, `PMCID PMC4795654`; the accessible precursor exposes both `6.09 +/- 1.43 zJ (~0.0380 eV)` and `4.2 +/- 0.9 zJ (~0.0262 eV)` candidate quantities, while both publisher page/PDF routes remain access-blocked by `403`/Cloudflare challenge | 8053 | `a3449e0610cdf3ebe9204a3172514c560c6d480908f48c030064d94fb241b337` | Candidate alternate source identity for the legacy nanomagnetic-memory runtime row | Source-record staging artifact; machine-readable bibliographic metadata is anchored and one primary-facing precursor surface is now visible, while the topic now provisionally prefers the `4.2 +/- 0.9 zJ` target. Final-source confirmation and the legacy-row policy still remain open. |
| Hong Crossref metadata snapshot | `docs/data/external/thermodynamics/landauer/hong_2016/crossref_work_record.json` | Crossref work record for DOI `10.1126/sciadv.1501492`, fetched on `2026-06-15` | Crossref JSON metadata; includes DOI, title, authors, container, article number, and publisher resource URL | 10893 | `25b24a37a62f7ed5da51694ce256cbb0593829c6332b351c3ea2fc72579969e5` | Local machine-readable bibliographic anchor for the Hong candidate branch | Metadata snapshot only; does not replace a direct archived publisher page or close numeric/uncertainty extraction. |
| Peterson branch source-resolution record | `docs/data/external/thermodynamics/landauer/peterson_2018/source_record.json` | Candidate quantum-Landauer branch; direct Crossref checks now show the local runtime surface is composite rather than tied to one exact paper | source metadata, Crossref-verified candidate DOI metadata, and candidate DOI list | 5261 | `E549F9D90CFD1D38C6CCE9A1B6D767FDB597ECB2D26EC46AD075DEF7D4F89BB8` | Prevents the local Peterson branch from being treated as source-locked prematurely | Source identity conflict record only; cannot be used as a gate until one paper identity is chosen and row-level capture is attached. |
| SI exact constants record | `docs/data/external/constants/codata/si_2019_exact_constants.json` | NIST/CODATA exact SI defining constants record; primary reference URL `https://physics.nist.gov/constants` | SI; `k_B` J K^-1, `e` C, `h` J s, `c` m s^-1 | 1346 | `dcced6d840f4f4fbcea90128061ab7a528be04e1b37917893dbf4a28934b3560` | Constant provenance for Landauer and related formula checks | External source record present; not a full CODATA table. |
| Measured constants source record | `docs/data/external/constants/codata/measured_constants_2022_source_record.json` | CODATA 2022 / NIST constants portal provenance anchor for non-exact constants such as `G` | SI | 1730 | `7b526619e09c6e7d95a532e19dedb05c90b693216be56d4167a5d641aabfc4b9` | Uncertainty provenance anchor for measured constants used in gravity-adjacent diagnostics | Source record plus direct local CODATA 2022 G extract; broader measured-constant table archival and systematic terms still open. |
| CODATA 2022 measured constants extract | `docs/data/external/constants/codata/codata_2022_measured_constants_extract.json` | NIST/CODATA 2022 complete ASCII constants listing, checked 2026-06-21 | SI; `G` in m^3 kg^-1 s^-2 plus supporting `G_over_hbar_c` row | 1517 | `4a8c8c8b343d00bf94039c2833a383cb382ce17f5ce9c2a21f3001d6f38946a6` | Direct numeric extraction anchor for measured-constant uncertainty in gravity-context rows | External numeric extract present for `G`; broader CODATA table archival and systematic astrophysical terms remain open. |
| LIGO/Virgo source record | `docs/data/external/gravity/ligo_black_hole_mergers/source_record.json` | GW150914-led merger-mass provenance anchor | source masses in `M_sun`; runtime conversion to kg must be explicit | 1373 | `70f556e9231f3488a35226d9f363094a35a34510731e48abec97b74cf7b9c55f` | Provenance anchor for black-hole area/entropy context | Source record only; row-level archival capture and propagated uncertainty still open. |
| EHT source record | `docs/data/external/gravity/eht_black_hole_masses/source_record.json` | M87* and Sgr A* mass provenance anchor | source masses in `M_sun`; runtime conversion to kg must be explicit | 1423 | `c1f1ca9e6a8de48d0ca6580c504d2b8a2cbf4da5bfe2381e308bccc234facf21` | Provenance anchor for black-hole shadow/mass context | Source record only; object-level machine-readable capture and propagated uncertainty still open. |
| Landauer source-lock package | `Data/03_Research/landauer_source_lock.json` | Topic-derived package linking Berut and CODATA records to local working copies | SI; local rows declare kT/eV/solar-mass exceptions where used | 2046 | `2d5c6a16e86cdc105a6f6153ff0d1d19f213bbef681d25363eb094a668f0c1e7` | Connects verifier inputs to upstream source records | Improves provenance but does not replace raw data archive; explicitly retains WARN until raw/supplement extraction exists. |
| Source evidence intake stub | `Data/03_Research/source_evidence_intake_stub.json` | Topic-generated intake sheet for unresolved external-source packages | Mixed; each target declares its own expected unit basis | 16113 | `91ffcd183dfaead47cca1432a2d7c8edadd040755f1bfc4d2fadc15b73f74889` | Landing zone for DOI/URL/local path/row-level evidence before data rewrites or claim upgrades | Workflow control only; does not itself upgrade claim strength or data reality status; the current Hong target records two preprint-level candidate quantities, visible intervals, and a provisional preference for the `4.2 +/- 0.9 zJ` target while still keeping final-source confirmation and the legacy-row policy open; the current Jun target now records legacy-row demotion and source-summary identity as the active controller. |
| Source evidence readiness matrix | `Data/03_Research/source_evidence_readiness_matrix.json` | Topic-generated readiness gate derived from the intake stub | n/a | 3743 | `72a836c3c03dadd4f0579980042920e7af6b249258bb8fc8eb8aa023983b2e38` | Shows which external source targets are still blocked by missing evidence fields | Workflow control only; records completeness, not scientific validation; the Berut row now carries an official Figure 3 PPT route, binary identity, embedded raster inventory, digitization protocol, automated panel-frame candidates, and semantic asset review but remains blocked by selected-panel tick mapping, selected point/curve coordinates, and numeric capture, the Hong row remains blocked because final-source confirmation and the legacy-row policy are still open, and the Jun row remains blocked by final PRL parity/APS access for the locally transcribed source-summary surface after legacy-row demotion. |
| Row closure matrix | `Data/03_Research/row_closure_matrix.json` | Topic-generated row-by-row closure map joining source and uncertainty blockers | mixed by row; each row declares its own current surface and blocker type | 10888 | `3d391bcbb0792728cb006a24fdb5115b000c8dc2edc6daa9be7a83b90c6b2b70` | Narrows the remaining blocker chain so row-level closure can proceed without broad prose assumptions | Workflow/control artifact only; does not itself close any row; the current matrix now declares that Berut has moved beyond locator/source-route/raster-asset/protocol/asset-role choice into `berut_figure_3_quantitative_panel_tick_mapping_required`, Jun now moves to `jun_final_prl_parity_or_aps_access_resolution_required` after local Table I/Figure 4 transcription, and Hong remains at final-source confirmation plus explicit replace/remove action for the demoted legacy row. |
| Landauer row contract | `Data/03_Research/landauer_row_contract.json` | Topic-generated minimum closure contract for the current Berut, Jun, and Hong Landauer rows | mixed by row; each row declares runtime value, unit basis, and minimum closure fields | 6345 | `0B24BBFF3217038493352CA59B514E116E744B2DED65E14232FD6916C9294697` | Narrows the main benchmark lane to the most actionable row-level closure targets | Workflow/control artifact only; does not itself close any row. |
| Berut provenance gap | `Data/03_Research/berut_2012_provenance_gap.json` | Topic-generated Berut-specific provenance blocker note for the strongest current Landauer row | J at runtime; summary row only until source table mapping is archived | `runtime-generated` | `see verifier-adjacent governance artifacts` | Narrows the primary Landauer row to one row-level provenance problem | Workflow/control artifact only; does not itself close the Berut row. |
| Berut source surface note | `Data/03_Research/berut_2012_source_surface_note.json` | Topic-generated note recording what the currently visible Nature source surface exposes for Berut 2012 | preview-level figure labels and access state | 2037 | `16002f6bc966d7f5a3c59fefa546859383dbfff4c354fafae164f08962f09f7a` | Narrows the Berut row-locator blocker from a generic missing-table statement to a preview-surface characterization | Workflow/control artifact only; does not itself close the Berut row. |
| Berut transcription-policy blocker | `Data/03_Research/berut_2012_transcription_policy_blocker.json` | Topic-generated policy blocker stating that the repo now selects one explicit conservative Berut normalization path while the accessible source surface remains figure-level | policy choice plus deferred alternatives for supplementary or machine-transcribed closure | 2774 | `AE88EDDC6BEC6A4CCFE52849D5A5B47CB275EE667D3624CC4A1784220CA7386C` | Narrows the Berut provenance workload from `which policy should we trust?` to one selected Figure 3 locator plus the remaining numeric-capture boundary under that policy | Workflow/control artifact only; does not itself close the Berut row. |
| Jun source-summary identity gap | `Data/03_Research/jun_2014_uncertainty_gap.json` | Topic-generated Jun-specific uncertainty blocker note for the pinned source-facing summary row | eV at runtime; source summary interval present, legacy row demoted, Table 1/Figure 4 locator captured; final-source parity still partial | 2640 | `8cc8a1de817a1c6dd8f1765f7367d54c556ab0c731313ef10041b280ffa93804` | Narrows the second Landauer row to final-source parity/local archival after Table 1/Figure 4 fit-target capture and legacy-row demotion | Workflow/control artifact only; does not itself close the Jun row. |
| Jun runtime mapping conflict | `Data/03_Research/jun_2014_runtime_mapping_conflict.json` | Topic-generated Jun-specific runtime-to-source mapping conflict note for the current runtime row | eV at runtime versus source-facing kT summary | 2917 | `2d7745727a4a68d69cfa4081f14fe4803a812df6d005261d4931d1a2d9bdd481` | Narrows the Jun blocker to one evidence-backed branch-identity and runtime-value mismatch problem | Workflow/control artifact only; does not itself close the Jun row, but it now records that the pinned Jun asymptotic-work quantity is numerically below the legacy `0.028 eV` runtime row under the current verifier baseline and that Jun may currently support only summary-layer interval use. |
| Hong lineage note | `Data/03_Research/hong_2016_source_lineage_note.json` | Topic-generated lineage note stating that the legacy `0.028 eV / 44% above limit` runtime wording may reflect a later nanomagnetic-memory branch and that the accessible same-author preprint now exposes Hong-side numeric candidates | legacy runtime eV row with mixed lineage risk | 3670 | `9ac0ded5169613adb350064f148c3a1d699193a1a7842622cd705d5c12cef137` | Prevents the legacy `0.028 eV` row from being overread as a clean `Jun 2014` benchmark quantity | Workflow/control artifact only; does not itself assign the row conclusively to `Hong 2016` or close `Jun 2014`. |
| Hong source acquisition blocker | `Data/03_Research/hong_2016_source_acquisition_blocker.json` | Topic-generated acquisition note stating that the staged Hong branch now has a confirmed Crossref DOI metadata anchor and an accessible same-author preprint precursor, while the final publisher page remains unarchived locally | alternate-source candidate with precursor surface present but final-source archive missing | 4254 | `9edc140a2d0be914087f44ca1b9ead15bd37878792bc15db74c2edb0b1a32033` | Prevents precursor-level source access from being mistaken for a closed final source package | Workflow/control artifact only; does not itself close the branch or reassign the row. |
| Hong numeric mismatch note | `Data/03_Research/hong_2016_numeric_mismatch_note.json` | Topic-generated numeric note stating that the staged Hong branch now exposes multiple candidate source-facing values, including one near `~0.026 eV` and another near `~0.038 eV`, without yet justifying the local `0.028 eV` runtime row | legacy runtime `0.028 eV` versus Hong-side preprint candidates | 4431 | `b9e30c08aa2cba5a0e80613421373ba990a206bb60c04c2a8574a2d17028e422` | Prevents source-family closure from being mistaken for numeric-row closure | Workflow/control artifact only; does not itself prove which number is correct or close the row. |
| Hong runtime target policy | `Data/03_Research/hong_2016_runtime_target_policy.json` | Topic-generated conservative policy selecting the current best-fit Hong-side quantity for the inherited `2016 / 44% above limit / ~0.026 eV` runtime narrative | source-facing zJ values explicitly converted to runtime eV | 3296 | `914b7c804fdb8abd244e66cd2083ceff7b98d1139fb5c13988755cfdbba25815` | Prevents the Hong branch from staying numerically ambiguous now that multiple source-facing candidates are visible | Workflow/control artifact only; provisionally prefers the `4.2 +/- 0.9 zJ (~0.0262 eV)` temperature-series mean, but does not itself close final-source confirmation or justify the local `0.028 eV` row. |
| Peterson source conflict | `Data/03_Research/peterson_2018_source_conflict.json` | Topic-generated Peterson-specific source-identity conflict note for the quantum-Landauer branch | source-resolution only; not a benchmark row | 4424 | `E65B74C43B5A8B98B11A21B0FF4C287BB604E81DEAA840947227C7522CF221BB` | Narrows the Peterson branch to a composite source-reference conflict before row capture | Workflow/control artifact only; does not itself close the Peterson branch. |
| Peterson branch identity policy | `Data/03_Research/peterson_branch_identity_policy.json` | Topic-generated policy separating the Peterson-led 2016, trapped-ion PRL 2018, and Nature Physics 2018 candidate families behind the legacy local label | source-resolution only; not a benchmark row | 2860 | `A7EA326FFDE554BF90F1309F91A8431304696E0CE8F88C5854E5E9AD1A8FD2D9` | Prevents the unsupported local `Peterson 2018` label from remaining an active benchmark identity | Workflow/control artifact only; keeps the branch generic until one exact paper is chosen. |
| Measured-constant uncertainty package | `Data/03_Research/measured_constant_uncertainty_package.json` | Topic-generated runtime policy package for measured-constant uncertainty in gravity-context rows | mixed SI constants and direct-G relative-uncertainty policy | 4624 | `bd6046402b3296d60afa0672ac98857f9b7a2271c1f6e9553500d975d6d91cd4` | Narrows the measured-constant blocker to direct CODATA 2022 G extraction and row policy | Workflow/control artifact only; threads direct `G` extraction into gravity-context combined intervals, but does not close systematic terms or object-level source-row capture. |
| Uncertainty preprocessing manifest | `Data/03_Research/uncertainty_preprocessing_manifest.json` | Topic-generated bridge from summary values to future propagated uncertainty outputs | Mixed by row; each row declares source and runtime units | 3883 | `4fd8f7b803454a509a1d9fb8b41058612b3aaa10c7a3e98db91c14871210a73c` | Narrowed worklist for source-normalized multi-row Landauer and black-hole uncertainty propagation | Partial scaffold only; does not yet produce propagated uncertainty in the primary physics outputs. |
| Uncertainty propagation summary | `Data/03_Research/uncertainty_propagation_summary.json` | Topic-generated propagated-interval artifact for Berut-summary and selected black-hole rows | Mixed by row; each row declares runtime inputs and propagated outputs | 9075 | `e98db62755f3971f61df25ac3bc8148a8b05be4bd68fb5227c38a3d50297e31b` | Makes current uncertainty support machine-readable without pretending the topic is fully source-normalized | Partial interval package only; Jun source-summary identity, systematic astrophysical terms, and raw-source row closure remain open. |
| Bridge derivation map | `Data/03_Research/bridge_derivation_map.json` | Topic-generated proof-boundary map for imported identities, UET proxies, and open bridge steps | n/a | 5823 | `d3a3c502f143164feedcb89f415a9d839b52e44f2b46a520d2104c96d7d8a579` | Prevents the topic from silently upgrading standard thermodynamic identities into claimed UET derivations | Boundary artifact only; open derivation steps remain open until separate artifacts close them. |
| Units contract | `Data/03_Research/units_contract.json` | Topic-generated symbol-to-unit contract separating SI observables from topic-local proxies | mixed declared layers; SI plus nondimensional proxy layer | 6832 | `eb23e9b043cc0e416a9b4648e7c775c0c0ff6c86b54bc7c0ddc643c02bd423da` | Prevents the topic from silently treating proxy engine outputs as physical thermodynamic observables | Boundary artifact only; no full proxy-to-SI bridge conversion is justified yet. |
| Landauer-UET mapping | `Data/03_Research/landauer_uet_mapping.json` | Topic-generated lane-specific map of what the current code can honestly claim about a UET relationship to the Landauer lower bound | n/a | 3118 | `1cfb04af048c755f35da4f08f6bc684c41e5cd2a8cf4194048ac020da60fe101` | Prevents direct reuse of the standard lower bound from being overstated as a non-circular UET derivation | Boundary artifact only; no nontrivial UET-added mapping is established in the current engine path. |
| Beta role clarification | `Data/03_Research/beta_role_clarification.json` | Topic-generated clarification of what current evidence supports about beta in the Landauer and bridge lanes | n/a | 3215 | `027ed60b5d15089ad91f0bb62589945592cb79a89b9f871e22a88fbd368a6a69` | Prevents beta symbol presence from being overstated as a derived bridge coefficient | Boundary artifact only; beta is present but not closed as a derived thermodynamic coefficient in the current verifier lane. |
| Berut transcription-policy decision | `Data/03_Research/berut_2012_transcription_policy_decision.json` | Topic-generated decision artifact selecting `figure_level_locator_capture` as the current conservative Berut provenance path | policy state only; no row-level numeric capture yet | 1705 | `EE5670C4CC2A4FACEBB81C48DB0F906204E4203574C1335F8C930A8DE51A5D8D` | Prevents Berut from remaining blocked by a fully open policy choice when the visible source surface already supports a narrower next move | Workflow/control artifact only; does not itself close the Berut row. |
| Berut figure-locator mapping | `Data/03_Research/berut_2012_figure_locator_mapping.json` | Topic-generated locator note attaching Figure 3 on the visible Nature preview surface to the current Berut topic-summary row with an explicit claim boundary | preview figure label plus runtime-summary mapping boundary | 2292 | `ED3607024CF822B2D4A5DA7D1DF6BE3FBB30FA33E5197201493D3EED8E10D548` | Narrows the Berut workload from locator choice to numeric-point capture or stronger-surface closure | Workflow/control artifact only; does not itself close the Berut row. |
| Berut Figure 3 PPT source route | `Data/03_Research/berut_2012_figure3_ppt_source_route.json` | Topic-generated route record for the official Nature/Springer Figure 3 PowerPoint file | figure-file route; no numeric row unit yet | 3865 | `13a886c8761e253e2f960a6e58b32cb42ea559c3f3cbdcc568ff71beab684e1b` | Captures the official Figure 3 file route and binary identity for the Berut source-normalization path | Workflow/control artifact only; download-tested route, embedded raster observation, inventory linkage, and protocol linkage are present, but accepted tick mapping, selected point/curve coordinates, numeric transcription, or a stronger source-data surface remains open. |
| Berut Figure 3 raster asset inventory | `Data/03_Research/berut_2012_figure3_raster_asset_inventory.json` | Topic-generated inventory of valid embedded raster assets in the official Nature/Springer Figure 3 PowerPoint file | raster asset metadata; no numeric row unit yet | 5601 | `207360859bd53744a57e5681a510fbc96ab0fc93bc7f167d32098e8e6a53ec7b` | Names primary digitization candidates for the Berut source-normalization path | Workflow/control artifact only; closes raster-asset identity and points to the digitization protocol, but leaves visual review, tick mapping, point/curve selection, and numeric transcription open. |
| Berut Figure 3 digitization protocol | `Data/03_Research/berut_2012_figure3_digitization_protocol.json` | Topic-generated digitization protocol selecting the first calibration candidate and required landmark fields for official Figure 3 raster transcription | digitization workflow metadata; no numeric row unit yet | 4978 | `87b3f0e84c8688b680fa7875b6b3f29a40c399fde8bb6955585cb5c4fec76a01` | Converts the Berut raster-candidate state into a controlled landmark-capture worklist | Workflow/control artifact only; closes protocol choice but leaves visual review, tick mapping, point/curve selection, and numeric transcription open. |
| Berut Figure 3 landmark candidate capture | `Data/03_Research/berut_2012_figure3_landmark_candidate_capture.json` | Topic-generated automated candidate pass over official Figure 3 embedded rasters | raster candidate coordinates; no numeric row unit yet | 4412 | `63b37cb5dc94757213db6a73a8b325b81b182a731dd83f09e57f78c368d995fd` | Narrows the Berut visual-search blocker to candidate panel-frame review | Workflow/control artifact only; records non-accepted panel-frame candidates and leaves selected-panel tick mapping, point/curve selection, and numeric transcription open. |
| Berut Figure 3 semantic asset review | `Data/03_Research/berut_2012_figure3_semantic_asset_review.json` | Topic-generated semantic role review using the author research page and local raster-candidate evidence | raster role metadata; no numeric row unit yet | 3063 | `38022aec606173fae4632bcdd14d12125bc8f26f6154ebeecc10da0672eccdd4` | Corrects the preferred quantitative digitization candidate from `jpeg_3` to `jpeg_2` | Workflow/control artifact only; selects the likely quantitative raster candidate but leaves selected-panel tick mapping, point/curve capture, and numeric transcription open. |
| Foundation claim gate | `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json` | Topic-generated dependency export gate derived from verifier metrics, evidence lanes, source-readiness rows, uncertainty status, derivation-boundary state, units-contract status, Landauer-UET mapping state, beta-role clarification state, and the active row-controller summary | n/a | 9197 | `4500f6eeb6915dc7dbf8f4813b5bf161ededebee08554eddb305f925ef921ab1` | Defines which `0.13` claims can be inherited by `0.23` and `0.0` and which theory-level claims remain blocked | Claim-inheritance control only; does not close source-lock, uncertainty, or UET derivation blockers; it now also exports the active `Berut/Jun/Hong/Peterson` row-controller chain directly. |
| Cattaneo synthetic benchmark | `Data/03_Research/cattaneo_data.json` | Synthetic Cattaneo-Vernotte heat-flux benchmark created in topic | `time_ps` ps; `heat_flux` proxy W/m^2-like value; `gradient` proxy K/m | 1356 | `69e4ce956633d1081b12ce6b83474c566093f37b6276177b2dd630024f7eaa89` | Hysteresis/lag simulation demo | Synthetic/proxy, not external evidence. |
| Experimental-data module | `Data/03_Research/experimental_data.py` | Manual literature summary for Berut/Jun/Hong/Peterson, LIGO/Virgo, EHT, Josephson/SI constants | SI constants; black-hole masses in solar mass/kg; entropy in Planck units | 13740 | `EB892105EC91A9F5BE0D00E93D43EC94FA3D02DFE031195DABD535C03F2481A1` | Formula-consistency and external-literature sanity checks | Source-labeled code module; Jun remains a mixed-lineage legacy summary context, Hong now carries explicit preprint-level candidate values plus a provisional preferred target, and Peterson now remains a demoted legacy placeholder until one exact paper identity is chosen. |
| Primary verifier | `Code/03_Research/Research_Landauer.py` | Topic verifier using the source-lock package, uncertainty artifact generation, derivation-boundary checks, units-contract generation, Landauer-UET mapping review, beta-role clarification, measured-constant runtime policy generation, Berut surface/policy workflow intake generation, Berut figure-locator mapping intake generation, Hong runtime-target policy intake generation, legacy-runtime-row policy intake generation, centralized row-controller export, and row-controller-aware claim-gate generation | SI inputs; emits J, eV, K, Planck-unit entropy plus workflow artifacts | 122254 | `fff7821696d504f847c744c1f25d6ebafe1110c24130c3687c5dc13165ab751a` | Writes machine-readable artifact and warning state | Code artifact, not a data source; listed here so manifest hashes match current verification input. |
| Verification artifact | `Result/artifacts/0_13_thermodynamic_bridge_verification.json` | Generated by `Research_Landauer.py` | n/a | `runtime-generated` | `see current file hash after rerun` | Machine-readable lane/status controller | Artifact stays `WARN`; Landauer/formula lanes pass, uncertainty intervals are still only partial, derivation boundary is mapped but still open, units are separated into SI and proxy layers, the Landauer lane is explicitly marked as an imported constraint, beta is explicitly not closed as a derived bridge coefficient, gravity-context rows expose both mass-only baseline intervals and mass-plus-direct-CODATA-2022-`G` combined intervals, the legacy `0.028 eV` row is now explicitly demoted to mixed-lineage context outside active Jun/Hong benchmark logic, the pinned Jun asymptotic-work quantity remains the main lower-bound metric, the staged Hong branch now provisionally prefers the `4.2 +/- 0.9 zJ (~0.0262 eV)` target while the next controller shifts to final-source confirmation plus explicit replace/remove action for the demoted legacy row, and the Berut lane now explicitly selects `figure_level_locator_capture`, attaches the official `Figure 3` PPT route plus embedded raster candidates and protocol, adds automated panel-frame candidates, and keeps accepted tick-mapping numeric-point-or-stronger-source-data closure open before stronger row-level normalization claims. |

## External Source Targets

| Source target | Required storage path | Current status |
|:--|:--|:--|
| Berut et al. 2012 Landauer data/supplement | `docs/data/external/thermodynamics/landauer/berut_2012/` | Source record stored; raw external file or machine-transcribed table still open. |
| Jun et al. 2014 nanomagnetic bit erasure | `docs/data/external/thermodynamics/landauer/jun_2014/` | DOI recorded in data module; raw external file not yet stored. |
| Peterson et al. 2018 quantum Landauer | `docs/data/external/thermodynamics/landauer/peterson_2018/` | DOI recorded in data module; raw external file not yet stored. |
| LIGO/Virgo event masses used for area theorem checks | `docs/data/external/gravity/ligo_black_hole_mergers/` | Manual summary only; mass uncertainty propagation open. |
| EHT black-hole mass observations | `docs/data/external/gravity/eht_black_hole_masses/` | Manual summary only; mass uncertainty propagation open. |
| CODATA/NIST constants | `docs/data/external/constants/codata/` | Exact SI constants source record stored; measured-constant uncertainty record still open. |

Repository note:

- This manifest was created during the repo standards pass and should be tightened further in a later provenance-normalization wave.
- Until raw/supplementary tables and measured-constant uncertainty records are frozen, treat the dataset package as a source-referenced internal benchmark rather than an archival release.

### 2026-08-01 source equation registry

The thermal source review now includes a machine-readable registry for the
standard TTG source equations and the intermediate g_n -> Delta_Tq ->
y_TTG observable layer. This is provenance and correspondence control only;
it does not add local numeric rows or close the dimensional Phi mapping.

## Berut Source Package Availability Boundary (2026-08-12)

The current checkout audit records the Nature Figure 3/PPT route as a publisher
locator, but no official binary, raw table, or separately exposed source-data
package is stored locally. The two Berut JSON copies remain topic-derived
summary rows and are not calibration-eligible. See `docs/core/artifacts/t13_berut_source_package_availability_boundary.json` for the
source-surface scope, hashes, and next acquisition controller.

## Berut Figure 3 Remote Binary Identity

The official publisher Figure 3 route was download-tested on 2026-08-12. The remote binary is hash-pinned as e4bab6be849a093b7578bc52ce6df9be95dc25d83d51ecb718b4f798a37d50fa with 479744 bytes and four embedded raster identities. The binary is not stored in the repository; no numeric row is accepted until panel, axis, point, uncertainty, preprocessing, and row identity are recorded. See docs/core/artifacts/t13_berut_figure3_remote_binary_identity.json.

## Ding 2022 Public Supplementary Payload Boundary (2026-08-12)

The official PMC S3 inventory is pinned at
`docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/ding_2022_pmc_s3_inventory.xml`
with SHA-256 `6f86e82611321053b3afd9b548f6e4a314ef03fd753ab2706775e2bc8c551672`.
It contains 11 objects. The three MOESM supplementary objects are archived locally
as PDF bytes; no machine-readable numeric payload object for PBTE `C_src` was
identified.

| Object | Local path | Size | SHA-256 | Role |
|:--|:--|--:|:--|:--|
| MOESM1 | `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/ding_2022_supplementary_information.pdf` | 1,893,976 | `a50c1a6347775de72f705f4395507d3136cbf4e5cadfb6638caca2876c52b8f7` | methods/equations/figures |
| MOESM2 | `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/ding_2022_supplementary_materials_2.pdf` | 4,537,623 | `2f7d1d057df83b8d3408f65c833dad7542fca8b24aeec087e304842fa5aca6e7` | reviewer response |
| MOESM3 | `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/ding_2022_supplementary_materials_3.pdf` | 927,333 | `4405683b720a24437d64fe3429d409503fcc91bd33c1e8616a3252cc50d94c5f` | reporting summary |

The machine-readable boundary result is
`docs/core/artifacts/t13_ding_public_supplementary_payload_boundary_audit.json`
with SHA-256 `c4ff211ea6853511a90f9e57ede81940e816a0dd4f2c77dc9125aead0adef6ea`. This closes only the public supplementary
availability lane; the author-request or accepted PBTE reproduction route remains open.

## MP48 Harmonic Spectral C_src-like Cross-file Reproduction (2026-08-13)

The permitted MP48 archive now has a deterministic harmonic DOS cross-file reproduction
lane. The raw DOS, thermal-properties, and Phonopy metadata files remain source-locked;
the reproduction artifact is `docs/core/artifacts/t13_mp48_spectral_csrc_reproduction_audit.json` with SHA-256
`5b2c6332fb70c6ae98749d96051cc4dbbffa04d37eed8f90e09168d35c61c091`. The full Topic 13 gate consumes this as a source-package lane only;
the current full-gate hash is `af317db05b87a694502b5852ee14f6a90e3b094ead9bb521c88c6820efb03ad2`.

The calculation uses `C_src^DOS(T) = N_A integral[g(nu)c(nu,T)dnu]` and reports J K^-1
mol^-1 primitive-cell values at 200, 250, and 300 K. It is an internal cross-file
harmonic comparator, not Ding PBTE `C_src`, not an accepted Ding-regime reproduction,
and not a UET or alpha calibration. No Xie 2026 holdout, target curve, or fitted
coefficient was accessed.

## MP48 Named Phi_E Dimensional Comparator (2026-08-13)

The MP48 harmonic package now supports a named standard-physics energy-response
comparator. At the declared reference `T0=300 K`, the source-derived thermal energy
density is used as `e0(T0)` and the same-source harmonic volumetric heat capacity as
`c_v(T0)`, yielding the conditional relation `alpha_Phi_E_K=e0/c_v`.

The machine-readable artifact is
`docs/core/artifacts/t13_mp48_phi_e_dimensional_comparator_audit.json` with SHA-256
`46fad518feb670e7e3fe4faac47582f7a5e93b88985c53225d4da4e6fc7cde44`. The result emits no `alpha_Phi_K`: `Phi_E` is a named standard-physics
coordinate and the base UET `Phi -> Phi_E` map remains open. No target curve, fitting,
or Xie 2026 holdout was used.

## MP48 Force-constant Harmonic Reconstruction (2026-08-13)

The permitted MP48 archive now has a deterministic source-level harmonic
reconstruction lane. The raw force constants, Phonopy metadata, and summary
remain source-locked; the result artifact is
`docs/core/artifacts/t13_mp48_force_constant_harmonic_reconstruction_audit.json` with SHA-256 `3903fbbbc22476e1394305edd2c9ad3c948802d31a9a9c36c572b8eb395cedd1`.
The Topic 13 full gate consumes this as a source-package lane only; its current
hash is `f6005cb6225975168eaf9fdf41ff280a6a6c096c16b55129cc9a92fda01671fd`.

The calculation reconstructs `D_ij(q)` from the 200-atom supercell force
constants, checks the primitive mapping, acoustic sum rule, pair symmetry,
Gamma acoustic modes, and a declared 5x5x2 q-grid. It is an internal harmonic
source comparator, not Ding PBTE `C_src`, not UET transport, and not an alpha
calibration. No Xie 2026 holdout, target curve, or fitted coefficient was used.

## NIST Graphite alpha_V Source Boundary (2026-08-13)

The official NIST SP 260-89 PDF is archived at
`docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/nist_sp260_89_graphite.pdf`.
The audit artifact is `docs/core/artifacts/t13_nist_graphite_alpha_v_source_boundary_audit.json` with SHA-256
`392bf8c98de925ea806a86392cbf440029a47e4e32173c2839cd04ff2cb553d5` and the current full-gate hash is `4cc6d5b68e7ee84710da6fb357ec7b4c640ca30182835200b84b2be41507e2a8`.

The lane evaluates the declared AXM-5Q1 length-expansion polynomial and reports
an explicit isotropic `alpha_V` comparator at 200, 225, 250, and 300 K. It is a
source boundary only: no `K_T`, Ding/HOPG material equivalence, volumetric
`c_v`, `alpha_Phi_K`, or Xie 2026 holdout claim is made.

## Bosak Graphite Elastic Bulk Comparator (2026-08-13)

The primary Bosak et al. IXS PDF is archived at
`docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/bosak_2007_graphite_elasticity.pdf`
with SHA-256 `5db6247c3dbf48dcbed70d749da96ca61816fe6fed480f32d80a947ead649d7d`. The source package is
`docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/bosak_2007_graphite_elastic_bulk_source_package.json`.
The audit artifact is `docs/core/artifacts/t13_graphite_elastic_bulk_modulus_source_audit.json`
with SHA-256 `65238edbfb66b57c6b3c0a06f95d8b3d28d6dc613df7b83d825332aff4a996af`.

The source reports the room-temperature single-crystal graphite tensor and
`B=36.4 +/- 1.1 GPa`; the audit independently reconstructs the hydrostatic
elastic comparator from the normal compliance block. This is not an isothermal
`K_T`, not a Ding/HOPG match, and not a UET calibration.

## Hanfland Graphite Isothermal K_T Source (2026-08-13)

The primary Hanfland et al. EOS PDF is archived at
`docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/hanfland_1989_graphite_equation_of_state.pdf`
with SHA-256 `300a6b03af667f71a27fc7c269e7a928af57d4b846bded25feaefa0e37b1089e`. The source package is
`docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/hanfland_1989_graphite_isothermal_kt_source_package.json`.
The audit artifact is `docs/core/artifacts/t13_graphite_isothermal_kt_source_audit.json`
with SHA-256 `63f0518c78febda473f89f8a0c3927d14b9d98a102dc560277bcd2a9daf8c0c4`.

The scalar row is the fixed-temperature 300 K ambient-pressure EOS input
`K_T=33.8 +/- 3.0 GPa`. It is source-locked as a declared standard comparator,
but material matching and same-state alpha_V/Cp/Cv remain open.

## IHEP TPG Anisotropic Alpha_V Comparator (2026-08-13)

The IHEP 2001-32 primary report is archived at
`docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/ihep_2001_32_tpg_thermal_expansion.pdf`
with SHA-256 `e9527b8dba9d3944a1a9298e9d516e501279b500586cf0179ec076b94fdd6f2e`. The source package is
`docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/ihep_2001_32_tpg_anisotropic_alpha_v_source_package.json`.
The audit artifact is `docs/core/artifacts/t13_tpg_anisotropic_alpha_v_source_audit.json`
with SHA-256 `f8ed02677b5ef1aede683cc2b191538722bda56b520d1d6ba5af024638504c68`.

The report supplies separate near-room-temperature in-plane and out-of-plane
TPG slopes. The audit computes the explicitly bounded family comparator
`alpha_V=2*alpha_a+alpha_c`; because the rows are not a same-specimen pair,
the result is not promoted to a same-state volumetric measurement or UET
calibration.

## Official Nelson-Riley Natural Graphite Alpha_V Comparator (2026-08-13)

The official Argonne/OSTI ANL-5524 report is archived at
`docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/argonne_anl_5524_graphite_thermal_expansion_table.pdf`
with SHA-256 `7e334a4c380c130773f6c34a6238f25a9c28e15c3a9c0e1f9aa3769647e98561`. The source package is
`docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/argonne_anl_5524_nelson_riley_alpha_v_source_package.json`.
The audit artifact is `docs/core/artifacts/t13_natural_graphite_nelson_riley_alpha_v_source_audit.json`
with SHA-256 `c20b42f64b9107459b555dfaddc5150028c39b5254e4791782161b2b9861b861`.

Table XIX reports the Nelson-Riley crystalline-graphite alpha_a interval and
alpha_c relation. The audit evaluates `alpha_V=2*alpha_a+alpha_c` at an
approximate room-temperature point but deliberately emits no statistical
uncertainty because the table does not provide one.

## MP48 Force-constant C_src Mesh-Convergence Boundary (2026-08-13)

The independent MP48 force-constant route was tested on `5x5x2`, `10x10x4`,
and `15x15x6` q-meshes. The machine-readable artifact is
`docs/core/artifacts/t13_mp48_force_constant_csrc_mesh_convergence_audit.json`
with SHA-256 `e7414905d99f4f412c0516d54024d584991e84f2797a4f20d3ec0215cfb39605`.

The maximum adjacent-mesh relative change is `0.513481935500736`, above the
declared `0.01` source-acceptance tolerance. This closes the convergence
question as a scoped no-go for this route; it does not turn MP48 into Ding
PBTE `C_src`, does not close the material-regime map, and does not emit
`alpha_Phi_K`. No target fit or Xie 2026 holdout access occurred.

## Huang 2023 Graphite Supplementary Source Boundary (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_HUANG_2023_SUPPLEMENTARY_PAYLOAD_BOUNDARY`.
WHAT_IS_ACTUALLY_CLOSED: The public supplementary PDF is archived with SHA-256 `aaf2f325ddc797e7c309132e65d69379e4223e049e7411e6c3dc04cba9e09b90`; 9 pages were reviewed and no machine-readable PBTE, mode-resolved `C_src`, or force-constant payload was accepted.
WHAT_REMAINS_OPEN: Numeric PBTE source, Ding material/regime mapping, base-Phi SI anchor, independent `alpha_Phi_K`, bridge/beta, and full thermal closure remain open.
DEPENDENCY_UNLOCKED: Independent Huang graphite comparator provenance only; no Ding source or downstream dependency unlock.
STATUS: `PASS_HUANG_PUBLIC_SUPPLEMENTARY_BOUNDARY_NO_NUMERIC_PBTE_PAYLOAD`; Full Topic 13 remains `BLOCKED_OPEN_T13_FULL_BRIDGE`.
WHAT_CHANGED: Added the raw PDF, source-boundary audit artifact, focused test, and full-gate/register links. Audit artifact SHA-256 `b7bf5b4c567d588a685be131e092e22af566f9068d73f5274961645a6ab18453`; full gate SHA-256 `888e2ff3cd23a2e4b1b4454b53039c76fd7b3a8083cb8dd6cf2427e7d25beaeb`.
EQUATION_OR_MAPPING: `y_TTG = Delta_Tq(t) / Delta_Tq(0)` is retained only as the comparator measurement layer; figure curves were not digitized.
VERIFICATION: Source hash and package boundary pass; no fit, no holdout access, and no alpha emission.
CONTROLLING_BLOCKER: `ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing`.
NEXT_ACTION: Use an authorized numeric PBTE payload or accepted same-regime reproduction; do not promote the PDF into `C_src`.
CLAIM_BOUNDARY: Provenance boundary/comparator only, not Ding source closure or Full Topic 13 closure.

## MP48 Finest-Pair Convergence Refinement (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` refinement; complete MP48 route remains blocked.
WHAT_IS_ACTUALLY_CLOSED: `20x20x8 -> 25x25x10` passes the unchanged `0.01` criterion at `0.006531457496264048`.
WHAT_REMAINS_OPEN: The full five-mesh route has maximum adjacent step `0.513481935500736`; the three-mesh fine tail still has `0.020163733436403874` at 100 K.
DEPENDENCY_UNLOCKED: Finest-pair diagnostic only; no Ding or downstream unlock.
STATUS: `BLOCKED_MP48_FORCE_CONSTANT_C_SRC_MESH_CONVERGENCE`; Full Topic 13 remains blocked.
WHAT_CHANGED: Canonical artifact now records five meshes, fine-tail status, and finest-pair status. Artifact SHA-256 `049e820564e532ba57eb5935086b0d6924253d6e4524b2b7b4cc29db69529158`; full gate SHA-256 `f0cb644215f356b0b2e6b925bbc8bfa0e9fa364a0c33275133fbe70fd0624c1e`.
EQUATION_OR_MAPPING: Harmonic Bose heat-capacity mesh sum only; no Ding relabeling.
VERIFICATION: `3 passed` focused and `176 passed, 625 deselected` Topic 13 regression; no holdout or fit.
CONTROLLING_BLOCKER: `mp48_force_constant_C_src_mesh_convergence_missing`.
NEXT_ACTION: Obtain accepted Ding-compatible PBTE source/reproduction with convergence and uncertainty.
CLAIM_BOUNDARY: Finest-pair diagnostic, not source closure or Full Topic 13 closure.

## NIST AXM-5Q1 Same-Grade Density Source Boundary (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_NIST_AXM5Q1_DENSITY_SOURCE_BOUNDARY`.
WHAT_IS_ACTUALLY_CLOSED: Table 1 specimen 103 is archived as `rho=1721 kg m^-3` at approximately 20 C by hydrostatic weighing, with source-stated estimated precision `+/-0.1%` retained as non-standard-uncertainty metadata.
WHAT_REMAINS_OPEN: Density uncertainty, direct volumetric `c_v`, `C_p`/`C_v` uncertainty, same-state alpha_V/K_T, and Ding mapping remain open.
DEPENDENCY_UNLOCKED: Same-grade density availability only; no downstream unlock.
STATUS: `PASS_SCOPED_NIST_AXM5Q1_DENSITY_SOURCE_BOUNDARY`; Full Topic 13 remains blocked.
WHAT_CHANGED: Added source package/audit/test and integrated full gate and major-result register. Artifact SHA-256 `7b33b0b2b51be34baa2ee11418d1c8cd389874cc8ceac3f3e3ef06fb8a655092`; full gate SHA-256 `2030316aacac4f654b4ead1b1b59d4c034e9cd38596bb3243f16e66f10c1b4f7`.
EQUATION_OR_MAPPING: Density supplies only the `rho` input to `c_p^V=rho*c_p`; no `c_v` is emitted.
VERIFICATION: Source/hash/unit/precision-boundary checks pass; no fit or holdout access.
CONTROLLING_BLOCKER: `density_uncertainty_not_source_locked`.
NEXT_ACTION: Source-lock a standard uncertainty or direct volumetric `c_v` route with same-state alpha_V/K_T.
CLAIM_BOUNDARY: Density availability boundary only, not Full Topic 13 closure.

## MP48 Deep Fine-Tail Mesh Convergence (2026-08-13)

The source-locked MP48 force-constant audit now includes seven meshes through `35x35x14`. The unchanged acceptance tolerance is `0.01` absolute relative adjacent-mesh step. The declared fine-tail `20x20x8` through `35x35x14` passes with maximum `0.00653145749584183`, while the complete route remains blocked at `0.5134819354919335` because the native/coarse transition is not converged. The audit artifact is `docs/core/artifacts/t13_mp48_force_constant_csrc_mesh_convergence_audit.json` with SHA-256 `3b7832a7c7562de91be77cba0291b8dd0fdf40819a90b46d75e95f0d9a56a133`; this is not Ding `C_src`, not a measurement uncertainty, and not an alpha calibration. Full-gate SHA-256 is `09ad63424a483a338346c43c2f2de1d0713ddabff15e1f80f586b9973e48e764` and downstream unlock remains false.

## BIPM Graphite Specific-Heat Comparator (2026-08-13)

Raw report: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/bipm_2006_01_graphite_specific_heat.pdf` (`2c491c94adb3f70f4b1ba915259f0a1d2f4788e072e99c8d34a87f964f69ce42`).
Source package: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/bipm_2006_01_graphite_specific_heat_source_package.json` (`ab120653076ac3d44e45235705ca505e923096be78078c1ee261dbe72bdea2c7`).
Audit: `docs/core/artifacts/t13_bipm_specific_heat_source_audit.json` (`6d71952c1ab294d3e391ca257abd49cde10c534f2265612561efacd4e2cc8a4d`).

The lane source-locks the report's sample-H mass-specific `c_p` and same-report
density, then computes a volumetric `c_p` comparator with uncertainty. It does
not emit `c_v`; `alpha_V`, `K_T`, and Ding material equivalence remain open.

## IAEA Manufactured-Graphite Table-Derived c_v Comparator (2026-08-13)

Raw handbook: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/iaea_graphite_handbook_2017.pdf` (`91e9d84e5d1828ab1028bf0e5fec0743fe1fb49e416b9e6305edf2f71a30a28a`).
Source package: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/iaea_graphite_handbook_constant_volume_source_package.json` (`568853f10f4ef1fc75b4ebed5851240ac8a94f05a5d72cf10af1a2d94bb62e09`).
Audit: `docs/core/artifacts/t13_iaea_graphite_constant_volume_source_audit.json` (`1af3c1c9e81a44b6837cad8d47651f92e167f613743a667e8d3c823cdaaf213c`).

Table 4.11 supplies a manufactured-graphite table-derived mass-specific
lattice `c_v` at 300 K. The probable error in `c_p` is retained as such;
because `c_w` and the density conversion lack source-grade uncertainty, this
lane does not emit volumetric `c_v` or calibration values.

## Ding/Comparator Material-Regime Boundary (2026-08-13)

Target supplementary source: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/ding_2022_supplementary_information.pdf` (`a50c1a6347775de72f705f4395507d3136cbf4e5cadfb6638caca2876c52b8f7`).
Package: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/ding_graphite_material_regime_boundary_source_package.json` (`c379002e67b4ee3f27e784999bf65f6becb4094f9f101be2360b528c0bfb6fc8`).
Audit: `docs/core/artifacts/t13_ding_material_regime_boundary_audit.json` (`64742790afda02aae657ceed146c6a88c235185066ff283f067ed52c376d14e0`).

The boundary records why ideal, manufactured, isotopically purified, and
fine-grained graphite comparators cannot be silently promoted to Ding's
natural-graphite TTG/PBTE regime. The lane closes the equivalence question as
not established; it does not create a numeric `C_src`.

## IAEA c_v Uncertainty and Volumetric Boundary (2026-08-13)

Raw handbook: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/iaea_graphite_handbook_2017.pdf` (`91e9d84e5d1828ab1028bf0e5fec0743fe1fb49e416b9e6305edf2f71a30a28a`).
Boundary package: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/iaea_graphite_cv_uncertainty_boundary_source_package.json` (`43c28e1bb5f33e7c10261e2d3a84a31c54b55fa8d2413f44c5c9e5461c3e6fd5`).
Audit: `docs/core/artifacts/t13_iaea_cv_uncertainty_boundary_audit.json` (`a51c4318a72603c521fd9c9aaa48f759a95054a9da00707427c59cd3abe34b3e`).

The handbook table is retained as a mass-specific manufactured-graphite
comparator. Its probable-error `Delta c_p` is not promoted to a standard
uncertainty for `c_v`, and no same-row uncertainty-grade density/thermoelastic
package is emitted for a volumetric conversion or Ding substitution.

## Phonix mp-47 Graphite Harmonic Comparator (2026-08-13)

Raw snapshot: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/phonix_mp47_graphite_summary_row.json` (`cea9711b09f455375a5f9182c295588b98d498fb09af4660af6fb7dce4fdaff1`).
Source package: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/phonix_mp47_graphite_source_package.json` (`f08bc1d0ac5142abb4f1916c0caaf79c89d3ef414979edfeef9365f4690c1b76`).
Audit: `docs/core/artifacts/t13_phonix_mp47_graphite_comparator_audit.json` (`57550435f987dff1a38601f20dfd94c3a43b1aca0af2aea8216320c2b0443130`).

The immutable Phonix `mp-47` summary row is retained as a graphite harmonic
comparison source. Its DOS is source-declared `a.u.` and no standard
uncertainty is supplied, so no unitful volumetric `c_v`, Ding `C_src`, or
alpha calibration is emitted. The material equivalence to Ding's natural
graphite TTG/PBTE sample remains explicitly unestablished.

## Oxford TGS Figure 1 Numeric Rows (2026-08-13)

Numeric rows: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/oxford_tgs_figure1_numeric_rows.csv.gz` (`6e67be5794ed10ebb81ca1ca5b513ee1232b64f6040d7413c81332cf61250454`; 20,020 rows).
Extraction manifest: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/oxford_tgs_figure1_numeric_rows_manifest.json` (`25c0d7110843f26383433cf995ff2a2aad743fd1badccff4d0501e0010fd9817`).
Audit: `docs/core/artifacts/t13_oxford_tgs_numeric_rows_audit.json` (`80020df66e0c03ceaf02a9e112f56308f4bf0ea753fe28a421e90dd4b487c8df`).

The rows preserve the Oxford source's Figure 1 time/intensity data and its
`yy1 - yy` subtraction at the selected map point. They are a comparison-only
source. Material/temperature identity, physical thermal units, Ding `C_src`,
and base-Phi calibration remain open.

## DeSorbo Ceylon Graphite Numeric Cp Comparator (2026-08-13)

Raw archive: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/nist_srd69_graphite_desorbo_1955.html` (`2e9955e1a176adc93ee152aceb390da67f561bf5ba0a4c741e9936a552f1dc1b`).
Source package: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/desorbo_1955_ceylon_graphite_cp_source_package.json` (`3bf9cebd1b3129f9b0f1cd66b49e16c2d7743059a207ed203048894abb6a746b`).
Audit: `docs/core/artifacts/t13_desorbo_ceylon_graphite_cp_audit.json` (`bccbb8f7d2895c8f4e5c86c53a39690ac739e8d621673ba109d1dc3ca795f399`).

The lane source-locks the NIST row attributed to DeSorbo 1955 Ceylon natural
graphite at 298.15 K. It preserves the reported accuracy boundary without
relabeling it as standard uncertainty and emits no volumetric c_v or alpha.

## Independent C_src Acceptance Contract (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_INDEPENDENT_C_SRC_ACCEPTANCE_CONTRACT`.
WHAT_IS_ACTUALLY_CLOSED: The source package now has an explicit acceptance contract separating raw-author Ding `C_src` from an accepted independent PBTE reproduction. Required fields include source identity/hash, raw payload, material/state mapping, mode-resolved response, SI units, uncertainty, convergence, independence, and holdout/fit audit.
WHAT_REMAINS_OPEN: Current acceptance is `BLOCKED`: Ding numeric author payload is absent and MP48 remains a harmonic ideal-graphite comparator, not a Ding-equivalent PBTE response.
DEPENDENCY_UNLOCKED: Source acceptance policy only; no Ding `C_src`, alpha, bridge, transport, Core, Gravity, or Galaxy unlock.
STATUS: `PASS_SCOPED_INDEPENDENT_C_SRC_ACCEPTANCE_CONTRACT`; full gate remains `BLOCKED_OPEN_T13_FULL_BRIDGE`.
WHAT_CHANGED: Added `docs/core/artifacts/t13_independent_csrc_acceptance_contract.json` (SHA-256 `447584738a9b5e676345b692570ac899c51b97e0950ddf2307c7a29efb0e8b68`) and linked it to the full gate (SHA-256 `ea02ea87e689e844ed8cf514843b1722a78ff8dc5cf638efce40b5cefac27c5e`).
EQUATION_OR_MAPPING: `C_src(T)=sum_mu c_mu(T)`; `Delta_Tq=Delta_u_ph/C_src`. Harmonic `c_v` and normalized TTG rows cannot satisfy this acceptance contract by relabeling.
VERIFICATION: The contract evaluates raw-author and independent routes as false, preserves no-fit/no-holdout rules, and focused acceptance tests pass. No synthetic source or numeric alpha is emitted.
CONTROLLING_BLOCKER: `ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing`.
NEXT_ACTION: Obtain an authorized Ding numeric package or a permitted same-regime PBTE reproduction with source-grade units, uncertainty, convergence, and material-state mapping.
CLAIM_BOUNDARY: This is a source-acceptance policy and candidate boundary only. It is not Ding validation, `C_src` evidence, `alpha_Phi_K`, or Full Topic 13 closure.

## Calorine/Zenodo NEP BTE Candidate Boundary (2026-08-13)

Public route: [Calorine thermal-conductivity BTE tutorial](https://calorine.materialsmodeling.org/get_started/thermal_conductivity_bte.html), [Zenodo tutorial inputs](https://zenodo.org/records/21198312), and the underlying graphite NEP/DFT package at [Zenodo 7811021](https://zenodo.org/records/7811021).

The route is source-located as a candidate independent reproduction path. Its public inputs include `graphite-prim.xyz` (MD5 `76a98ce37aa503552a23883c4054f64a`) and `nep-C.txt` (MD5 `6196d0146f2314249bc2c8b9b743cad5`), while the tutorial generates `fc2/fc3` and uses a small `16x16x8` mesh with RTA. No deposited mode-resolved `C_src(T)` rows, source-grade uncertainty/convergence package, Ding natural-graphite defect-state mapping, or base-Phi SI anchor is imported. The route remains comparison/candidate-only.

Artifact: `docs/core/artifacts/t13_calorine_zenodo_nep_bte_candidate_boundary_audit.json` (SHA-256 `5cd20205444f2678bce2c9660d01ad9248e0ae0ad5466601b1fcded38c158e42`).

## Xie 2026 Holdout Access Control (2026-08-13)

Canonical audit: `docs/core/artifacts/t13_xie_2026_holdout_access_audit.json` (`c3185da0a233894d7f338138bbe6acee287194e1852a80e40b0b5f6f2134e21b`).

The current record is explicit that metadata/article identity was observed during
source discovery, while no numeric holdout payload, rows, curves, or source bytes
were consumed. The holdout was not used for fitting, tuning, calibration, threshold
adjustment, candidate selection, or claim promotion. The canonical access audit
replaces ambiguous interpretation of legacy boolean compatibility fields; Xie 2026
remains locked.

## NIMS Graphite LTC Route No-Go (2026-08-13)

The public [NIMS MDR lattice thermal conductivity collection](https://mdr.nims.go.jp/collections/0113dccc-ec45-42ed-86db-f455f9b63fb1?locale=en) was checked through its exact subject and full-text search routes. `C`, `Graphite`, `Carbon`, `graphite`, and `specimen:graphite` searches returned no record in that collection. The `carbon` full-text result set (349 records over 35 pages) contained no elemental-carbon formula `C` material record. A public API cross-check returned two `specimen:"graphite"` records, both in the unrelated `MDR XAFS DB` collection.

Artifact: `docs/core/artifacts/t13_nims_graphite_ltc_route_no_go.json` (SHA-256 `47814c603057bd8dede2cbebcf069e820ff389566612402f23997bd3acc529ff). This is a source-route no-go only; it does not produce `C_src`, replace Ding, or unlock `alpha_Phi_K`.

## Ding 2017 ACS Supplementary Payload Boundary (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_DING_2017_ACS_SUPPLEMENTARY_PAYLOAD_BOUNDARY`.
WHAT_IS_ACTUALLY_CLOSED: The official ACS Figshare supplementary PDF is source-locked by DOI, file identity, size, and SHA-256 `048b3ecfa9ccd02db0a0fc4ec14bb352f04275cf4e0216e689f0689d4ad0a6e5`; all 18 pages were reviewed and no machine-readable mode-resolved `C_src(T)`, raw force constants, uncertainty package, or convergence package was accepted.
WHAT_REMAINS_OPEN: Numeric Ding-compatible PBTE `C_src(T)`, source-grade uncertainty and convergence, material/state mapping, base-Phi SI anchor, and independent `alpha_Phi_K` remain open.
DEPENDENCY_UNLOCKED: Ding 2017 public supplementary provenance boundary only; no `C_src`, alpha, bridge, transport, Core, Gravity, or Galaxy unlock.
STATUS: `PASS_DING_2017_ACS_SUPPLEMENTARY_BOUNDARY_NO_MACHINE_READABLE_C_SRC`; Full Topic 13 remains `BLOCKED_OPEN_T13_FULL_BRIDGE`.
WHAT_CHANGED: Added the public supplementary PDF, source-boundary artifact `E2676E6E59BA412944D27057333ECE6B3AE827600A30125E63725390B176C8CB`, focused test, full-gate projection, and register/dependency links. Current full-gate hash is `53e9367b0bee2aed9d85c9a9a2c9d395360e417ab2b750ee9888800d32aaa22d`.
EQUATION_OR_MAPPING: The source Eq. 15 heat-current/thermal-conductivity expressions are retained as method context only. Topic 13 still requires `C_src(T)=sum_mu c_mu(T)` in `J m^-3 K^-1` and `Delta_Tq=Delta_u_ph/C_src`; no `Delta_Tq=alpha_Phi_K*Delta_Phi` calibration is emitted.
VERIFICATION: Source locator, Figshare file identity, MD5/SHA-256, page review, no-figure-digitization, no-fit, no-alpha, and no-holdout checks pass. Full gate remains at the same 10 blockers; focused source/regression tests pass (`8 passed`).
CONTROLLING_BLOCKER: `ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing`; independent `alpha_Phi_K` calibration and full bridge closure remain unresolved.
NEXT_ACTION: Obtain an authorized numeric Ding-compatible PBTE payload or accepted same-regime reproduction with mode-resolved rows, SI units, uncertainty, convergence, and material-state mapping. Do not promote this PDF or its figures to `C_src`.
CLAIM_BOUNDARY: This closes only the ACS public-supplementary payload boundary. It is not Ding `C_src` evidence, an independent alpha calibration, TTG prediction, external validation, Core closure, or global UET closure.

## Phi SI Anchor Public-Source Boundary (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_PHI_SI_ANCHOR_PUBLIC_SOURCE_BOUNDARY`.
WHAT_IS_ACTUALLY_CLOSED: The official Ding 2022 public route is bounded to article, supplementary, and figure-derived material; the captured package contains no paired base-`Phi` amplitude and SI thermal-response record. The corresponding-author route is specified but not executed, and the current normalized/action lanes retain a scale freedom.
WHAT_REMAINS_OPEN: An independent paired base-`Phi`/SI record, the base-`Phi` to `Phi_E` map, `e0`/`c_v` uncertainty inputs, and independent `alpha_Phi_K` remain open.
DEPENDENCY_UNLOCKED: Public-source and normalization boundary only; no `e0`, `alpha_Phi_K`, Full Topic 13, Core, Gravity, or transport unlock.
STATUS: `PASS_PUBLIC_SOURCE_BOUNDARY_NO_PAIRED_BASE_PHI_RECORD`; Full Topic 13 remains `BLOCKED_OPEN_T13_FULL_BRIDGE`.
WHAT_CHANGED: Added `docs/core/artifacts/t13_phi_si_anchor_public_source_boundary_audit.json` (SHA-256 `605245fa937cf5d2701a0afa0cc90a4f543052c4dd977066e1f3496bc12c50c5`), integrated it under the dimensional-observable map, synchronized the major-result register/dependency gate, and added a focused regression test.
EQUATION_OR_MAPPING: `Phi_E=s_material*Phi_base`; `alpha_Phi_K=(e0/c_v)*s_material`; `Delta_Tq=alpha_Phi_K*Delta_Phi_base`. No numeric `e0` or `alpha_Phi_K` is emitted.
VERIFICATION: Official Nature data-availability route, captured OA inventory, author-request manifest, candidate-search audit, and covariant normalization no-go are hash-linked. Full gate is `BLOCKED_OPEN_T13_FULL_BRIDGE` with the same 10 blockers; focused tests pass (`6 passed`); no fit, tuning, holdout use, or threshold change occurred.
CONTROLLING_BLOCKER: `independent_paired_base_Phi_amplitude_and_SI_observable_record_missing` and `alpha_Phi_K_independent_calibration_missing`.
NEXT_ACTION: Obtain an authorized paired base-`Phi`/SI record or derive a coefficient-provenance-backed action-to-SI map, then rerun the independent alpha audit. Do not use the normalized TTG curve or Xie 2026 holdout.
CLAIM_BOUNDARY: This closes only a public-source availability and scoped identifiability lane. It is not an `alpha_Phi_K` calibration, temperature prediction, external validation, Core closure, or global UET closure.

## Action-Derived Finite-Temperature O(2) Hartree Self-Energy (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_UET_O2_FINITE_T_SELF_ENERGY_HARTREE_LANE`.
Source/data role: no external source rows. This is an action-derived natural-unit calculation from `docs/core/uet_o2_finite_temperature_self_energy.py` and the existing O(2) finite-density action configuration.
Audit artifact: `docs/core/artifacts/t13_uet_o2_finite_temperature_self_energy_audit.json` (SHA-256 `ACB61CB97087F66C97FC5E278F183F9CF6262FA633596C86DD910C190B545B18`).
Required fields represented: declared equations, natural-unit lane, derivation class, observable, approximation boundary, convergence records, finite-difference check, analytic weak-coupling witness, source hashes, no-fit/no-holdout policy, and claim boundary.
WHAT_IS_ACTUALLY_CLOSED: Hartree thermal tadpole, self-consistent normal-branch mass gap, and implicit response derivative with quadrature/cutoff convergence.
WHAT_REMAINS_OPEN: No SI anchor, `alpha_Phi_K`, Ding `C_src`, physical Kubo coefficient, microscopic SK/KMS match, condensate/two-fluid completion, or entropy/transport closure is supplied by this lane.
STATUS: `PASS_ACTION_DERIVED_HARTREE_THERMAL_SELF_ENERGY`; Full Topic 13 remains `BLOCKED_OPEN_T13_FULL_BRIDGE`.
EQUATION_OR_MAPPING: `I_T(M^2;T,mu)=1/2 integral[(n_B(E-mu)+n_B(E+mu))/E] d^3k/(2*pi)^3`; `Pi_T=(N+2)*lambda*I_T`; `M^2=m_eff^2(Phi)+Pi_T`; `dM^2/dPhi=(d m_eff^2/dPhi)/(1-dPi_T/dM^2)`.
VERIFICATION: Gap residual, implicit finite difference, quadrature/cutoff convergence, weak-coupling high-temperature witness, ontology, and no-holdout checks pass. No synthetic external source or numeric alpha is emitted.
CONTROLLING_BLOCKER: `interacting_finite_temperature_self_energy_and_unique_microscopic_scheme_matching_missing`; independent `alpha_Phi_K` and source-compatible `C_src` remain open.
NEXT_ACTION: Close the microscopic finite-temperature scheme and physical SK/KMS/Kubo interface; preserve this record as internal action-derived evidence only.
CLAIM_BOUNDARY: Natural-unit O(2) Hartree lane only. It is not a physical transport measurement, SI map, alpha calibration, TTG prediction, external validation, or Full Topic 13 closure.
## Hartree Equilibrium Thermodynamic Consistency (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_UET_O2_HARTREE_EQUILIBRIUM_THERMODYNAMIC_LANE`.
Source/data role: no external source rows. This is an action-derived natural-unit equilibrium calculation from `docs/core/uet_o2_finite_temperature_hartree_thermodynamics.py`, the Hartree self-energy lane, and the declared O(2) finite-density action configuration.
Audit artifact: `docs/core/artifacts/t13_uet_o2_hartree_thermodynamic_consistency_audit.json` (SHA-256 `C0845D9D7C088B6D5D16623376C215B00AAE2810B6524A1ECFE0D1564016B443`).
Required fields represented: stationary functional, ontology, natural units, derivation class, equilibrium observables, approximation boundary, convergence records, pressure-derivative identities, Maxwell check, source hashes, no-fit/no-holdout policy, and claim boundary.
WHAT_IS_ACTUALLY_CLOSED: Stationary Hartree pressure, charge, entropy, and energy identities on the homogeneous normal branch.
WHAT_REMAINS_OPEN: No vacuum counterterm, unique microscopic finite-temperature scheme, condensate/two-fluid sector, physical Kubo/SK-KMS match, entropy-current transport, SI anchor, `alpha_Phi_K`, Ding `C_src`, or external validation is supplied.
STATUS: `PASS_ACTION_DERIVED_HARTREE_EQUILIBRIUM_THERMODYNAMICS`; Full Topic 13 remains `BLOCKED_OPEN_T13_FULL_BRIDGE`.
EQUATION_OR_MAPPING: `Omega_H=Omega_1+(m_eff^2-M^2)I_T+(N+2)*lambda*I_T^2/2`; at the gap, `p_H=p_1+(N+2)*lambda*I_T^2/2`, `n_H=n_1`, `s_H=s_1`, and `epsilon_H=-p_H+T*s_H+mu*n_H`.
VERIFICATION: Pressure-to-entropy, pressure-to-charge, Maxwell, energy, stationarity, convergence, and positive equilibrium finite-difference checks pass. Fixed-dressed-mass susceptibility/heat-capacity fields are explicitly kept separate from stationary finite-difference stability.
CONTROLLING_BLOCKER: `vacuum_counterterm_and_unique_microscopic_finite_temperature_scheme_matching_missing`; independent `alpha_Phi_K` and source-compatible `C_src` remain open.
NEXT_ACTION: Close the named finite-temperature renormalization scheme, then match physical SK/KMS/Kubo and dimensional `Phi` interfaces.
CLAIM_BOUNDARY: Equilibrium natural-unit Hartree lane only. It is not full EOS/transport/KMS/entropy closure, a physical measurement, SI map, alpha calibration, TTG prediction, external validation, or Full Topic 13 closure.

## Finite-Temperature Scheme Identifiability No-Go (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_AS_NO_GO` for `T13_UET_O2_FINITE_T_SCHEME_IDENTIFIABILITY_NO_GO`.
Source/data role: no external source rows. This is an internal algebraic structural audit of finite local counterterm ambiguity under the current O(2) reference conditions.
Audit artifact: `docs/core/artifacts/t13_uet_o2_finite_temperature_scheme_identifiability_no_go.json` (SHA-256 `AD00E5E1C0E2998536F82490FA56CF35022FCEC65717C2F65410A12F73FB06CA`).
Required fields represented: finite-local-counterterm equation, natural units, shared reference conditions, off-reference witnesses, ontology, source hashes, no-fit/no-holdout policy, and claim boundary.
WHAT_IS_ACTUALLY_CLOSED: The current second-order reference conditions do not identify a unique finite-temperature renormalization completion.
WHAT_REMAINS_OPEN: No physical counterterm, microscopic matching, full Hartree renormalized action, condensate/two-fluid sector, physical Kubo/SK-KMS, entropy-current transport, SI anchor, `alpha_Phi_K`, Ding `C_src`, or external validation is supplied.
STATUS: `PASS_SCOPED_NO_GO_FINITE_TEMPERATURE_SCHEME_IDENTIFIABILITY`; Full Topic 13 remains `BLOCKED_OPEN_T13_FULL_BRIDGE`.
EQUATION_OR_MAPPING: `Delta V_a(x)=a*(x-x_*)^3/Lambda_*^2`; it vanishes through second order at `x_*` but changes off reference.
VERIFICATION: Two witnesses share reference value/first/second derivatives and differ off reference; no source data or holdout used.
CONTROLLING_BLOCKER: `source_backed_or_declared_physical_finite_temperature_renormalization_scheme_missing`.
NEXT_ACTION: Declare/source-lock a physical finite-temperature renormalization scheme with microscopic matching, or retain Hartree approximation-only.
CLAIM_BOUNDARY: Structural no-go only; not physical EOS/transport/KMS/SI/alpha/Full Topic 13 closure.

## MP48 Fine-Tail Acceptance Policy Correction (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for the independent MP48 fine-tail convergence lane.
WHAT_IS_ACTUALLY_CLOSED: Seven meshes are evaluated; the complete three-pair fine tail passes unchanged tolerance `0.01` with maximum step `0.00653145749584183`. Coarse pre-asymptotic changes remain diagnostic, including route-wide maximum `0.5134819354919335`.
WHAT_REMAINS_OPEN: Ding material/mode-resolved `C_src`, source uncertainty, base-Phi energy mapping, `alpha_Phi_K`, and the rest of Full Topic 13 remain open.
STATUS: `PASS_MP48_FORCE_CONSTANT_C_SRC_MESH_CONVERGENCE`; Full Topic 13 remains `BLOCKED_OPEN_T13_FULL_BRIDGE`.
EQUATION_OR_MAPPING: Harmonic mesh sum only; no Ding relabeling and no alpha calibration.
VERIFICATION: Fine-tail completeness and convergence checks pass; no fit or Xie 2026 numeric holdout use.
CONTROLLING_BLOCKER: `Ding_material_regime_and_mode_resolved_C_src_acceptance_missing`.
NEXT_ACTION: Source-lock an accepted same-regime Ding/PBTE package with uncertainty.
CLAIM_BOUNDARY: Independent comparator lane only, not Ding validation or Full Topic 13 closure. Artifact SHA-256 `585ebc548e5354c2c4905af9b3efca5f9c9d1365527046d4103751ce7869b45d`.

## MP48 Acceptance Controller Synchronization (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for fine-tail convergence; `PARTIAL` for Full Topic 13.
WHAT_IS_ACTUALLY_CLOSED: `force_constant_mesh_pass=true` under unchanged fine-tail policy.
WHAT_REMAINS_OPEN: `material_equivalent_to_ding=false`, `mode_resolved_ding_c_src_ready=false`, and `accepted_for_full_topic13=false`; source, alpha, bridge, transport, and dimensional blockers remain.
STATUS: `PASS_MP48_FORCE_CONSTANT_C_SRC_MESH_CONVERGENCE`; Full Topic 13 `BLOCKED_OPEN_T13_FULL_BRIDGE`.
VERIFICATION: Acceptance guards and evidence hashes are synchronized; no holdout or fit path was used.
CONTROLLING_BLOCKER: `ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing`.
NEXT_ACTION: Obtain accepted same-regime Ding/PBTE evidence.
CLAIM_BOUNDARY: Internal comparator acceptance-policy synchronization only. Mesh artifact `585ebc548e5354c2c4905af9b3efca5f9c9d1365527046d4103751ce7869b45d`; acceptance contract `844e59159f2cff251043eedbdbcc1017d74146dedd927ad755bf687056a09463`; full gate `c189beba37a32ebcc06f15eb4ea39558dcadb36c74e3a469e7f4bdd640f62427`.

## MP48 Full-Gate Narrative Drift Repair (2026-08-13)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for harmonic fine-tail convergence; `PARTIAL` for Full Topic 13.
WHAT_IS_ACTUALLY_CLOSED: The full gate uses the current convergence-pass wording.
WHAT_REMAINS_OPEN: Ding-compatible `C_src`, material mapping, alpha, SI bridge, and physical transport closure.
STATUS: `PASS_MP48_FORCE_CONSTANT_C_SRC_MESH_CONVERGENCE`; Full Topic 13 `BLOCKED_OPEN_T13_FULL_BRIDGE`.
VERIFICATION: Obsolete no-go phrase absent; acceptance contract still rejects MP48 for Full Topic 13.
CONTROLLING_BLOCKER: `ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing`.
NEXT_ACTION: Obtain accepted same-regime PBTE evidence.
CLAIM_BOUNDARY: Narrative drift repair only. Full gate SHA `284664c485e308f6311d2f85443c83c0937dac7518c891854216244e0d05c8c2`.
## MP48 Temperature-Volume Uncertainty Boundary (2026-08-13)

MAJOR_RESULT_CLOSURE: CLOSED_FOR_LANE for T13_MP48_TEMPERATURE_VOLUME_UNCERTAINTY_BOUNDARY.
WHAT_IS_ACTUALLY_CLOSED: The MP48 room-temperature volume anchor and non-statistical display envelope are bounded to comparator use; they are not a source-grade temperature-resolved volumetric c_v uncertainty contract.
WHAT_REMAINS_OPEN: Temperature-resolved volume uncertainty, source statistical c_v uncertainty, Ding C_src/material mapping, alpha_Phi_K, and Full Topic 13 closure remain open.
DEPENDENCY_UNLOCKED: MP48 comparator-boundary reporting only; no downstream Core or Gravity unlock.
STATUS: PASS_SCOPED_MP48_TEMPERATURE_VOLUME_UNCERTAINTY_BOUNDARY_NO_GO; Full Topic 13 remains BLOCKED_OPEN_T13_FULL_BRIDGE.
WHAT_CHANGED: Added the boundary audit, full-gate projection, registry/dependency links, focused test, and wave note.
EQUATION_OR_MAPPING: C_v^vol(T) = C_v^mol,cell(T) / V_mol,cell(T); fixed room-temperature volume is an explicit comparator approximation.
VERIFICATION: temperature_resolved_volume_status is OPEN; source statistical uncertainty is NOT_REPORTED_BY_DEPOSIT; combined display envelope is NON_STATISTICAL_DISPLAY_ONLY; focused tests pass (8 passed); holdout remains unconsumed.
CONTROLLING_BLOCKER: temperature_resolved_graphite_volume_and_source_grade_c_v_uncertainty_missing.
NEXT_ACTION: Obtain a permitted same-state temperature-resolved volume source with uncertainty and rerun the contract.
CLAIM_BOUNDARY: Comparator source/uncertainty boundary only; not Ding C_src, alpha calibration, TTG prediction, external validation, or Core closure.
EVIDENCE_HASHES: boundary audit 9736291b43cc2723d2e6cdd73af007c9d606bf8322394ab5c2fcf1194e151f69; package 86f5d5015b5bd0172bc2bfae64271955c56470650bdb6b8459bb1280e5dbc3cf; full gate bb5094dcc9683e8d8641b4648bac7d653d701ad96881e9a94e7cfc4df914b637; register 326f7efd7bbe2822753012973d49565b29f3f97a96d69056be8baba836637e35; dependency e48de2a90d0919f485880797cc0b21a612c7691fb36f7da00d3725254d754506; integrity 8d11ee5d8f154c8c69e847767f28c95c9c4d8a9dddaf4b6a5b095f8dbe1e14f8.
## Graphite alpha_V/K_T Source Compatibility Boundary (2026-08-13)

MAJOR_RESULT_CLOSURE: CLOSED_FOR_LANE for T13_GRAPHITE_ALPHA_V_K_T_MATCHED_SOURCE_BOUNDARY.
WHAT_IS_ACTUALLY_CLOSED: The current source inventory cannot form a same-state, same-grade alpha_V/K_T pair with source-grade uncertainty for Cp-to-Cv correction.
WHAT_REMAINS_OPEN: Same-state alpha_V/K_T with uncertainty, density, Ding mapping, source-grade c_v uncertainty, alpha_Phi_K, and Full Topic 13 remain open.
DEPENDENCY_UNLOCKED: Current source-pair inventory boundary only; no downstream Core or Gravity unlock.
STATUS: PASS_SCOPED_GRAPHITE_ALPHA_V_K_T_MATCHED_SOURCE_BOUNDARY_NO_GO; Full Topic 13 remains BLOCKED_OPEN_T13_FULL_BRIDGE.
WHAT_CHANGED: Added the compatibility audit, full-gate projection, registry/dependency links, focused test, and wave note.
EQUATION_OR_MAPPING: c_p^V - c_v^V = T * alpha_V^2 * K_T; no numeric correction is emitted.
VERIFICATION: NIST K_T is absent; Hanfland same-state alpha_V is absent; Bosak is dynamic elastic; TPG is not same specimen/temperature; Nelson-Riley lacks row-level statistical uncertainty; focused tests pass (10 passed).
CONTROLLING_BLOCKER: same_grade_alpha_V_and_K_T_missing.
NEXT_ACTION: Obtain a permitted same-state source pair with uncertainty and Ding-regime mapping.
CLAIM_BOUNDARY: Source compatibility boundary only; not thermodynamic correction, Ding C_src, alpha calibration, TTG prediction, external validation, or Core closure.
EVIDENCE_HASHES: boundary audit 4a1148ba4ef81c2af07a2985b59ec18cc17d46f452b73176f3de2cb02ac3d30e; full gate 4ebeb1cde595179fcf717c2ceb46e5a84e8c6940f243c3a017403882fdf2a2dd; register 04ea35790f92edef0606bef6171c2b5b271cb0de3e9740f78188a390a2741fce; dependency 18aa1310753f611a5cc1305d257fe61df08d360fa13f15e7b9295a380eefe3f1; integrity 8d11ee5d8f154c8c69e847767f28c95c9c4d8a9dddaf4b6a5b095f8dbe1e14f8.
## Ding Alternate Public Dataset Boundary (2026-08-13)

MAJOR_RESULT_CLOSURE: CLOSED_FOR_LANE for T13_DING_ALTERNATE_PUBLIC_DATASET_DISCOVERY_BOUNDARY.
WHAT_IS_ACTUALLY_CLOSED: The current public candidate inventory is bounded. ISIS is a Bi2Te3/Graphite nanocomposite PDOS route and Caltech is a graphite c-axis mean-free-path route; neither supplies Ding-compatible mode-resolved volumetric C_src(T).
WHAT_REMAINS_OPEN: Authorized Ding numeric C_src or accepted same-regime reproduction, material mapping, source-grade uncertainty/convergence, alpha_Phi_K, and Full Topic 13 remain open.
DEPENDENCY_UNLOCKED: Public route inventory boundary only; no downstream Core, Gravity, transport, or Galaxy unlock.
STATUS: PASS_SCOPED_DING_ALTERNATE_PUBLIC_DATASET_BOUNDARY_NO_GO; Full Topic 13 remains BLOCKED_OPEN_T13_FULL_BRIDGE.
WHAT_CHANGED: Added the candidate package, audit, full-gate projection, registry/dependency links, focused test, and wave note.
EQUATION_OR_MAPPING: C_src(T)=sum_mu c_mu(T); Delta_Tq=Delta_u_ph/C_src(T). No numeric C_src or alpha is emitted.
VERIFICATION: ISIS public RAW/Nexus metadata and Caltech public MFP metadata are recorded, but neither route passes material/observable/regime acceptance; no payload import, fitting, or holdout use occurred.
CONTROLLING_BLOCKER: ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing.
NEXT_ACTION: Acquire an authorized Ding numeric package or accepted same-regime PBTE reproduction with mode-resolved rows and source-grade uncertainty.
CLAIM_BOUNDARY: Source-discovery boundary only; not C_src evidence, alpha calibration, TTG prediction, external validation, or Full Topic 13 closure.
EVIDENCE_HASHES: package 31ca12abb2fd3459891e3189e5b291bf5bcf110478bc9380cd153212e3841b81; boundary audit d2ba45e151b22319c0721ea48185a7b8d7969a37e411ef984beb352516d825e7; full gate e25e1d0e67b72f97f8f7edec7a89ba1ad4e3451b7b9b105149e6f87fc779cd98; register 88cb9fabd434dc7acfb452d41037fb156e6093674f8710f6e3a1ced2aff6fbcd; dependency d699292b2b95634913622e3c762437dfc750d58074d72fc64cf977fe9e352d6d; integrity 8d11ee5d8f154c8c69e847767f28c95c9c4d8a9dddaf4b6a5b095f8dbe1e14f8.
## Calorine/Zenodo PBTE numeric C_src reproduction (2026-08-14)

MAJOR_RESULT_CLOSURE: CLOSED_FOR_LANE for T13_CALORINE_ZENODO_NEP_BTE_NUMERIC_REPRODUCTION.
WHAT_IS_ACTUALLY_CLOSED: Public Calorine/Zenodo inputs are hashed and rerun through a fixed 4x4x2 force-constant state with 4x4x2, 6x6x3, 8x8x4, and 10x10x5 q meshes; the latest pair passes the declared candidate numerical preflight.
WHAT_REMAINS_OPEN: Ding material/state mapping, source-grade uncertainty, raw Ding C_src acceptance, alpha_Phi_K, UET bridge/beta, full transport/KMS/entropy, and Phi-to-observable calibration.
DEPENDENCY_UNLOCKED: Candidate C_src reproduction lane only; no downstream Core or application unlock.
STATUS: PASS_SCOPED_CALORINE_NUMERIC_C_SRC_REPRODUCTION; Full Topic 13 remains BLOCKED_OPEN_T13_FULL_BRIDGE.
WHAT_CHANGED: Added the source package, persistent summaries and HDF5 payloads, reproduction audit, full-gate projection, registry sync, and focused test.
EQUATION_OR_MAPPING: C_src(T) = [sum_q w_q sum_mu c_qmu(T)] / [sum_q w_q V_primitive]; output unit J m^-3 K^-1. No Phi, alpha_Phi_K, or holdout mapping is emitted.
VERIFICATION: Source hashes, units, force-constant identity, mesh comparison, no-fit, and no-holdout checks pass.
CONTROLLING_BLOCKER: ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing.
NEXT_ACTION: Close material/state and source-grade uncertainty gates before reconsidering full C_src acceptance.
CLAIM_BOUNDARY: Candidate reproduction only; not Ding-equivalent, not calibration, not prediction, and not Full Topic 13 closure.
EVIDENCE_HASHES: package 2672a3fe2d60e564c7e9c4eff17944f5db4d3ff62bc20be32960912fe48500ca; audit 822a736824feff7223a6290734eb21a3891950eaa16af39b3864a83ecd72f135; full gate 4638941a2d1387df91048905a255f4641a35b83fea753a0b52086d11120aaa07; register b5bf4ceef12b075474c784874dcfc5ef0519176edc694629eb57c92ebe437a7c; dependency 8f426f75c104912b68a086ef560f9a63ae9b4ec4e75ae9666ef829231f4caf1d.
### 2026-08-14 - Calorine provenance and state-uncertainty decomposition

MAJOR_RESULT_CLOSURE: CLOSED_FOR_LANE for T13_CALORINE_ISOTOPE_MASS_SENSITIVITY and T13_CALORINE_STATE_UNCERTAINTY_DECOMPOSITION.
WHAT_IS_ACTUALLY_CLOSED: Zenodo is recorded as the local byte source, GPUMD as the upstream NEP model origin, and record 7811021 as related but not the input source. NIST natural-carbon bounds were propagated through the mass-only C_src lane; the mesh numerical envelope and mass-only state envelope are reported separately.
WHAT_REMAINS_OPEN: Ding natural-graphite material/state equivalence, defect/morphology and isotope-scattering state, source-grade uncertainty, Ding C_src acceptance, alpha_Phi_K, UET bridge/beta, EOS/transport/KMS/entropy, and dimensional Phi mapping.
DEPENDENCY_UNLOCKED: Provenance and Calorine state-sensitivity lanes only; no full Topic 13 or downstream unlock.
STATUS: PASS_SCOPED_CALORINE_STATE_UNCERTAINTY_DECOMPOSITION; Full Topic 13 remains BLOCKED_OPEN_T13_FULL_BRIDGE.
WHAT_CHANGED: Corrected NEP provenance metadata, regenerated the source package and candidate boundary, added mass-only isotope sensitivity and uncertainty decomposition audits, and synchronized the acceptance/full-gate/registry artifacts.
EQUATION_OR_MAPPING: epsilon_mesh = 0.0023908135; natural-composition mass envelope = 0.0000511973; pure-isotope values are stress bounds only. No Phi, alpha_Phi_K, or holdout mapping is inferred.
VERIFICATION: No fit, target tuning, alpha_Phi_K calibration, threshold adjustment, clipping, padding, or Xie 2026 holdout access occurred. Acceptance remains false.
CONTROLLING_BLOCKER: material_regime_mapping_to_TTG_not_closed; source-grade uncertainty is not inferred from the reported envelopes.
NEXT_ACTION: Source-lock defect/morphology state and response contract, or retain Calorine as a non-Ding comparator; then reassess independent C_src acceptance.
CLAIM_BOUNDARY: Candidate provenance and sensitivity decomposition only; not Ding validation, source-grade uncertainty closure, UET Phi calibration, TTG prediction, or Full Topic 13 closure.
EVIDENCE_HASHES: candidate 5e4e0d42d6e70612eabce988b86ab10b628dea14d4270bf2364ad58f572d014b; isotope 5db4a9487f728e5275906a1d4514c154b02cee4854fadcc0ea45f3ac6d5a0221; uncertainty d1b7619f1f0040e1010eb561de5422d2063fb554055c15fd7f14186d4134e481; acceptance 880eb2cc94543f19fefae13ad8c64af820bb619d9c898cd4e1e710494519d281; full gate 8c3d550ca900d11ad5d6748e5aba4410bf5bead2f423d21d09b0b6b2db1bee33.
### 2026-08-14 - Calorine evidence-chain resynchronization

MAJOR_RESULT_CLOSURE: CLOSED_FOR_LANE evidence chain synchronized for T13_CALORINE_ZENODO_NEP_BTE_NUMERIC_REPRODUCTION, T13_CALORINE_ISOTOPE_MASS_SENSITIVITY, and T13_CALORINE_STATE_UNCERTAINTY_DECOMPOSITION.
WHAT_IS_ACTUALLY_CLOSED: The final reproduction, acceptance, full-gate, and registry hashes now point to the same corrected provenance and sensitivity artifacts.
WHAT_REMAINS_OPEN: Full Topic 13 remains blocked by Ding-compatible C_src acceptance, material/state mapping, source-grade uncertainty, alpha_Phi_K, bridge/beta, EOS/transport/KMS/entropy, and dimensional mapping.
DEPENDENCY_UNLOCKED: No new dependency; only lane-level evidence-chain consistency.
STATUS: PASS_SCOPED_EVIDENCE_CHAIN_RESYNCHRONIZATION.
WHAT_CHANGED: Refreshed full-gate and registry projections after the final source-package and uncertainty-audit regeneration.
EQUATION_OR_MAPPING: y_TTG = Delta_Tq(t) / Delta_Tq(0); Delta_Tq = alpha_Phi_K * Delta_Phi remains open. The reported C_src envelopes are comparator diagnostics only.
VERIFICATION: Full gate remains BLOCKED_OPEN_T13_FULL_BRIDGE; claim promotion is false; no fit, holdout read, threshold change, clipping, or padding occurred.
CONTROLLING_BLOCKER: ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing.
NEXT_ACTION: Continue with source-locked Ding-regime material/state and uncertainty closure.
CLAIM_BOUNDARY: Hash synchronization is not physical closure, external validation, alpha calibration, or Full Topic 13 closure.
EVIDENCE_HASHES: package fdca0fe6b387ecf7a731831f808b19504b9c58ebefe2d150261de37b4334f914; reproduction audit afc8fb0d9daea81c30a09b24f0aabd824cde1a85e662ea52880fadd42863de89; candidate 5e4e0d42d6e70612eabce988b86ab10b628dea14d4270bf2364ad58f572d014b; isotope 5db4a9487f728e5275906a1d4514c154b02cee4854fadcc0ea45f3ac6d5a0221; uncertainty d1b7619f1f0040e1010eb561de5422d2063fb554055c15fd7f14186d4134e481; acceptance 880eb2cc94543f19fefae13ad8c64af820bb619d9c898cd4e1e710494519d281; full gate 8c3d550ca900d11ad5d6748e5aba4410bf5bead2f423d21d09b0b6b2db1bee33; register 3a0d50fc687a99206ad97e98991f9cfdb84d86ea065a4fdbc1c191f5c24a5da8; dependency e968545313aa9324e70e16f5a501f0c66a422309935d549f72e160a487dadccc.
## Ding Public-Route Boundary Resynchronization (2026-08-14)
MAJOR_RESULT_CLOSURE: CLOSED_FOR_LANE for T13_DING_ALTERNATE_PUBLIC_DATASET_DISCOVERY_BOUNDARY.
WHAT_IS_ACTUALLY_CLOSED: Three public routes are now inventoried and rejected for Ding C_src: ISIS nanocomposite PDOS, Caltech c-axis MFP, and NIMS/MDR article/PDF-only graphite-ribbon record.
WHAT_REMAINS_OPEN: Ding numeric C_src or accepted same-regime reproduction, material/state mapping, source-grade uncertainty/convergence, alpha_Phi_K, and Full Topic 13 remain open.
DEPENDENCY_UNLOCKED: Public source-discovery boundary only; no downstream unlock.
STATUS: PASS_SCOPED_DING_ALTERNATE_PUBLIC_DATASET_BOUNDARY_NO_GO; Full Topic 13 remains BLOCKED_OPEN_T13_FULL_BRIDGE.
WHAT_CHANGED: Added NIMS/MDR metadata and synchronized the audit, full gate, closure register, dependency gate, and focused test.
EQUATION_OR_MAPPING: C_src(T)=sum_mu c_mu(T); Delta_Tq=Delta_u_ph/C_src(T). No numeric C_src or alpha is emitted.
VERIFICATION: NIMS/MDR exposes the article PDF and an author-request data route, not machine-readable PBTE inputs; no candidate payload, fit, calibration, or holdout was used.
CONTROLLING_BLOCKER: ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing.
NEXT_ACTION: Acquire an authorized Ding package or accepted same-regime PBTE reproduction with rows, units, state mapping, uncertainty, convergence, and permission.
CLAIM_BOUNDARY: Source-discovery boundary only; not C_src evidence, alpha calibration, TTG prediction, external validation, or Full Topic 13 closure.
EVIDENCE_HASHES: package e20e41acee2789b0705cd351df853b9a2790b1e2e1b03b70618dc6aa0af5b680; boundary 327957c98bdb9f2cfe4a26dd85c6f01feb182641e15e9a8f5656bd909111b9d1; full d11014f549e6493f968febc290c0993f60b7a18db6f72429a6cf479fc986d707.

## Berut Figure 3c Figure-Derived Digitization

The official publisher Figure 3c route is represented by a hash-pinned embedded
raster identity and a ten-row, figure-derived marker table. The rows use `tau` in
seconds and `<Q>` in `kT`; they are not raw experimental data and are not eligible
for calibration. See `docs/core/artifacts/t13_berut_figure3_digitization.json`.
## Lowitzer Graphite P-V-T Candidate Boundary (2026-08-17)

MAJOR_RESULT_CLOSURE: CLOSED_FOR_LANE for T13_GRAPHITE_ALPHA_V_K_T_MATCHED_SOURCE_BOUNDARY.
WHAT_IS_ACTUALLY_CLOSED: The Lowitzer et al. P-V-T publication is recorded as a relevant same-study candidate, but the accessible publisher record is abstract-only.
WHAT_REMAINS_OPEN: Full P-V-T rows, alpha_V/K_T row uncertainty, density uncertainty, Ding material mapping, and Cp-to-Cv closure remain open.
DEPENDENCY_UNLOCKED: Candidate-source screening only; no numeric correction, Ding C_src, alpha_Phi_K, transport, Core, Gravity, or Full Topic 13 unlock.
STATUS: PASS_SCOPED_GRAPHITE_ALPHA_V_K_T_MATCHED_SOURCE_BOUNDARY_NO_GO; Full Topic 13 remains BLOCKED_OPEN_T13_FULL_BRIDGE.
WHAT_CHANGED: Added the Lowitzer candidate package and extended the existing alpha_V/K_T source-compatibility audit.
EQUATION_OR_MAPPING: c_p^V - c_v^V = T * alpha_V^2 * K_T; no numeric correction is emitted.
VERIFICATION: Abstract scope is recorded; no machine-readable P-V-T rows, alpha_V rows, K_T rows, source-grade uncertainty, or Ding mapping are present; focused regression 2 passed.
CONTROLLING_BLOCKER: same_grade_alpha_V_and_K_T_missing.
NEXT_ACTION: Obtain the full permitted payload or retain the candidate as a source-search boundary.
CLAIM_BOUNDARY: Abstract-only candidate screen; not source-grade thermodynamic correction, calibration, prediction, or external validation.
SOURCE_PACKAGE: docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/lowitzer_2006_graphite_pvt_candidate_source_package.json
SOURCE_HASH: ef5e46d19cee679196093df802e21187ca39d5a50910b9a74727f53bf4062225


## Calorine-to-Ding Material-State Admission Boundary (2026-08-18)
- Package: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/t13_calorine_zenodo_nep_bte_reproduction_source_package.json` (SHA-256 `fdca0fe6b387ecf7a731831f808b19504b9c58ebefe2d150261de37b4334f914`).
- Controller: `docs/core/artifacts/t13_ding_material_regime_boundary_audit.json` (SHA-256 `700a1f8520521045d58717dc1be25390a783389c443af4e5507736ea0e5940d8`).
- Result: Calorine C4 volume/density, SI C_src rows, input hashes, convergence preflight, and NEP/RTA boundary are source-checked; equivalence to Ding remains `NOT_ESTABLISHED`.
- Boundary: no source-grade uncertainty, Ding C_src acceptance, Phi calibration, holdout access, or downstream unlock.

## Tohei Graphite alpha_V/B0 Table Comparator (2026-08-18)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_TOHEI_GRAPHITE_ALPHA_V_K_T_TABLE_COMPARATOR`.
WHAT_IS_ACTUALLY_CLOSED: Tohei et al. Table I is recorded with a primary-paper locator. It gives a same-calculation QHA graphite comparator at 300 K (`alpha_V=19.8e-6 K^-1`, `B0=28.7 GPa`) and separately cited experimental table values (`21.9e-6 K^-1`, `33.8 GPa`).
WHAT_REMAINS_OPEN: No row-level uncertainty is provided; the experimental values come from different cited references; Ding specimen/state equivalence and a source-grade Cp-to-Cv correction remain open.
DEPENDENCY_UNLOCKED: Comparator lane only; no Ding C_src, Phi calibration, transport, Core, Gravity, or Full Topic 13 unlock.
STATUS: `SOURCE_SCREENED_TABLE_COMPARATOR_NO_CLOSURE`.
WHAT_CHANGED: Added `tohei_2006_graphite_alpha_v_kt_table_comparator_source_package.json` and projected it through the existing matched alpha_V/K_T boundary audit.
EQUATION_OR_MAPPING: `c_p^V-c_v^V=T*alpha_V^2*K_T`; no numeric correction is emitted.
VERIFICATION: Package hash `7a8dfafd8c06145e08194505aeca933b6f90c27e184cf4db45b56d9375b140c9`; audit hash `7f16734e1f78d29154c1652feb3784290ce16923e772fb42230237ea07ab03f1`; focused regression `2 passed`; no fit or holdout access.
CONTROLLING_BLOCKER: `same_grade_alpha_V_and_K_T_missing`, specifically same-state uncertainty and Ding-regime mapping.
NEXT_ACTION: Acquire a permitted full P-V-T payload or direct volumetric c_v/same-state Cp source with units, uncertainty, specimen identity, and state mapping.
CLAIM_BOUNDARY: Source-traceable comparator only; not thermodynamic correction, Ding validation, UET calibration, TTG prediction, external validation, or Full Topic 13 closure.
SOURCE_PACKAGE: `docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/tohei_2006_graphite_alpha_v_kt_table_comparator_source_package.json`
SOURCE_HASH: `7a8dfafd8c06145e08194505aeca933b6f90c27e184cf4db45b56d9375b140c9`

## Thermodynamic Normal Component Lane (2026-08-18)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_UET_O2_THERMODYNAMIC_NORMAL_COMPONENT_LANE`.
WHAT_IS_ACTUALLY_CLOSED: The action-derived finite-temperature quasiparticle sector is recorded as a named thermodynamic normal component with branch coverage, thermodynamic derivatives, static momentum response, low-temperature suppression, and total-state stability checks.
WHAT_REMAINS_OPEN: Physical normal flow, retarded Kubo transport, SI `Phi` normalization, independent `alpha_Phi_K`, Ding-compatible `C_src`, and Full Topic 13 remain open.
DEPENDENCY_UNLOCKED: Natural-unit thermodynamic normal-component lane only; no physical transport, calibration, Core, Gravity, or external-validation dependency unlock.
STATUS: `PASS_ACTION_DERIVED_THERMODYNAMIC_NORMAL_COMPONENT_LANE`.
WHAT_CHANGED: Added the source-role record for the action-derived lane and linked its module, inherited two-fluid implementation, audit artifact, and regression test.
EQUATION_OR_MAPPING: `p_n=p_qp`; `n_n=partial_mu p_n`; `s_n=partial_T p_n`; `epsilon_n=-p_n+T*s_n+mu*n_n`; `chi_n=partial_mu n_n`; static response is not relabeled as physical Kubo data.
VERIFICATION: Artifact status passes with zero failed checks; no external numeric source, fit, target data, alpha calibration, threshold change, or Xie 2026 holdout access.
CONTROLLING_BLOCKER: `physical_normal_flow_component_or_retarded_kubo_match_missing`.
NEXT_ACTION: Obtain a state-matched physical normal-flow/retarded Kubo record with units and uncertainty, while preserving the natural-unit boundary.
CLAIM_BOUNDARY: Internal action-derived thermodynamic lane only; not a physical normal-fluid measurement, SI thermal observable, TTG prediction, external validation, or Full Topic 13 closure.

EVIDENCE:
- `docs/core/uet_o2_finite_temperature_normal_component.py`
- `docs/core/uet_o2_finite_temperature_two_fluid_response.py`
- `docs/core/artifacts/t13_uet_o2_thermodynamic_normal_component_audit.json`
- `docs/scripts/audit/audit_topic13_uet_o2_thermodynamic_normal_component.py`
- `docs/core/test/test_topic13_uet_o2_thermodynamic_normal_component.py`

## Condensed Relative-Flow Collision Kernel (2026-08-18)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_UET_O2_CONDENSED_RELATIVE_FLOW_COLLISION_KERNEL_LANE`.
WHAT_IS_ACTUALLY_CLOSED: A screened action-derived condensate contact channel and a symmetric positive-semidefinite relative-flow operator with a conserved common-flow mode are now source-recorded as internal natural-unit evidence.
WHAT_REMAINS_OPEN: Complete microscopic vertices, continuum-renormalized physical Kubo, complete two-fluid tensor, SI Phi map, alpha_Phi_K, Ding C_src, and Full Topic 13.
DEPENDENCY_UNLOCKED: Condensed relative-flow kernel lane only; no physical transport or downstream unlock.
STATUS: `PASS_ACTION_DERIVED_CONDENSED_RELATIVE_FLOW_COLLISION_LANE`.
WHAT_CHANGED: Added the module, verifier, artifact, regression, equation addendum, full-gate projection, and closure-register synchronization.
EQUATION_OR_MAPPING: `s_med=2*E_a*E_b*(1-cos(theta))`; `m_H^2=2*lambda*A_*^2`; `L_rel=Gamma_rel*((1,-1),(-1,1))`.
VERIFICATION: Zero failed checks; refinement change `1.0049400415447205e-05`; no source rows, fit, calibration, target, threshold adjustment, or holdout access.
CONTROLLING_BLOCKER: `continuum_renormalized_physical_Kubo_coefficient_missing`.
NEXT_ACTION: Complete microscopic condensed-channel and continuum matching, or source-lock a state-matched retarded correlator.
CLAIM_BOUNDARY: Internal natural-unit kernel only; not physical Kubo, SI calibration, TTG prediction, or Full Topic 13 closure.

EVIDENCE:
- `docs/core/uet_o2_condensed_relative_flow_collision.py` (SHA-256 `d311f7106787e92638ac6a8d3d48a5b4d0ea6dbd688d83a52b2be824dff82d21`)
- `docs/core/artifacts/t13_uet_o2_condensed_relative_flow_collision_audit.json` (SHA-256 `87baac fcca4d df10be4c17d42c14a8ed98780eed340a0984294c3041bd18a369`)

## Continuum Relative-Flow Kubo Lane (2026-08-18)

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE`
WHAT_IS_ACTUALLY_CLOSED: The action-derived screened contact response is integrated over `k in [0,infinity)` using a compactified radial coordinate, with explicit order and scale refinement records.
WHAT_REMAINS_OPEN: This lane has no external source rows. Loop-renormalized vertex provenance, physical Kubo units/uncertainty, SI `Phi` map, independent calibration, Ding `C_src`, and Full Topic 13 remain open.
DEPENDENCY_UNLOCKED: Internal continuum thermal response lane only; no external-validation or downstream unlock.
STATUS: `PASS_ACTION_DERIVED_CONTINUUM_RELATIVE_FLOW_KUBO_LANE`
WHAT_CHANGED: Added the action/equation implementation and verifier artifact. This is derived internal evidence, not a source package or calibration record.
EQUATION_OR_MAPPING: `k=Lambda*u/(1-u)`; `Lambda` is a natural-energy quadrature scale and is not a physical cutoff; the thermal Bose weights provide the convergent integration domain.
VERIFICATION: Audit has zero failed checks; no source rows, target data, fitting, calibration, synthetic replacement, or Xie 2026 holdout was consumed.
CONTROLLING_BLOCKER: `loop_renormalized_condensed_vertex_and_physical_kubo_match_missing`.
NEXT_ACTION: Add a source-locked or microscopically derived retarded correlator with state, units, uncertainty, locator, and hash; retain this lane as internal action-derived evidence.
CLAIM_BOUNDARY: No external data provenance is claimed by this lane, and no physical transport coefficient or `alpha_Phi_K` is emitted.
EVIDENCE_PATHS: `docs/core/uet_o2_continuum_relative_flow_kubo.py`; `docs/core/artifacts/t13_uet_o2_continuum_relative_flow_kubo_audit.json`; `docs/core/test/test_topic13_uet_o2_continuum_relative_flow_kubo.py`.
EVIDENCE_HASHES: module `70850509063f5adf4493a21ceea420c9f414e1605eea7220a00ce3549d0bca30`; audit `76b46ffe55399fa03b7ae0309352b1df5e6afb494397cecfa4b82a87e0d78813`.
## T13-114 - Condensed Loop-Renormalized Contact Vertex

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE`.
WHAT_IS_ACTUALLY_CLOSED: An action-derived finite thermal loop/contact-channel record and state-matched natural retarded response are archived with code and audit hashes.
WHAT_REMAINS_OPEN: There is no external numeric source row, independent physical vertex/Kubo anchor, SI unit conversion, source-grade physical uncertainty, `alpha_Phi_K`, or Ding `C_src` payload in this lane.
DEPENDENCY_UNLOCKED: Internal lane only; no physical Kubo, calibration, Core, Gravity, or external-validation dependency.
STATUS: `PASS_ACTION_DERIVED_CONDENSED_LOOP_RENORMALIZED_CONTACT_VERTEX_LANE`.
WHAT_CHANGED: Added `docs/core/uet_o2_condensed_loop_renormalized_vertex.py`, its audit artifact, focused test, and equation-registry addendum. The declared target/reference states and preprocessing are in the audit; no synthetic replacement data are used.
EQUATION_OR_MAPPING: `B_ab^R=B_ab^th(T,mu,Phi)-B_ab^th(T,mu,Phi_ref)`; `lambda_ab^R=lambda/(1+lambda*B_ab^R)`; `K_rel^natural=lim_(omega->0) Re G_R^rel(omega)`.
VERIFICATION: Code and artifact hashes are recorded in `RESEARCH_WAVE_2026-08-20_CONDENSED_LOOP_RENORMALIZED_VERTEX.md`; numerical uncertainty is quadrature-only (`3.500054507989025e-06`). Holdout access audit remains clean.
CONTROLLING_BLOCKER: `physical_Kubo_coefficient_record_missing` and `independent_physical_condensed_vertex_anchor_missing`.
NEXT_ACTION: Source-lock or microscopically derive an accepted state-matched coefficient record with units, locator, uncertainty, and hash; do not treat this internal record as external data.
CLAIM_BOUNDARY: No external provenance, physical Kubo, SI observable, alpha calibration, TTG prediction, or Full Topic 13 closure is claimed.
DATA_ROLE: `DERIVED` internal action-derived natural-unit result; not `CALIBRATION`, `TRAINING`, or `HOLDOUT` data.
SOURCE_PROVENANCE: no external numeric source consumed; source/origin is the existing repository O(2) action and declared condensed dispersion.