# Topic Audit Inventory

This inventory is the audit-facing scoreboard for all `41` numbered topic directories under
`docs/topics`.

Legend:

- `Scope` = `core` or `future`
- `S` = structure
- `D` = data reality
- `V` = verification
- `M` = mathematical rigor
- `P` = physical rigor
- `C` = claim integrity
- Scores use `0-3` where `0 = missing` and `3 = standardized and auditable`

| Topic | Scope | Status | Tier | S | D | V | M | P | C | Data class | Key gap | Recommended next action |
| :-- | :-- | :-- | :-- | --: | --: | --: | --: | --: | --: | :-- | :-- | :-- |
| `0.0_Grand_Unification` | `core` | `Draft` | `C` | 1 | 0 | 1 | 1 | 1 | 1 | `no data path` | synthesis topic lacks standards root docs and manifested datasets | build the full root standards package before upgrading any claim language |
| `0.1_Galaxy_Rotation_Problem` | `core` | `Structured` | `A` | 3 | 3 | 2 | 2 | 2 | 2 | `manifested real dataset` | still internal benchmark scope rather than external replication | use as a normalization template for the next audit wave |
| `0.2_Black_Hole_Physics` | `core` | `Draft` | `B` | 2 | 2 | 1 | 1 | 1 | 1 | `real source referenced` | verification package and limitations are missing | define a verification spec with explicit metrics, thresholds, baseline, and artifact output |
| `0.3_Cosmology_Hubble_Tension` | `core` | `Structured` | `B` | 3 | 3 | 1 | 2 | 2 | 2 | `manifested real dataset` | latest Hubble artifact fails its stated threshold | keep structured status but rerun/fix only with honest metric improvement |
| `0.4_Superconductivity_Superfluids` | `core` | `Draft` | `B` | 2 | 2 | 1 | 1 | 1 | 1 | `real source referenced` | standards root docs are still missing | define a verification spec with explicit metrics, thresholds, baseline, and artifact output |
| `0.5_Nuclear_Binding_Hadrons` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 0 | `manual or placeholder` | risky wording and incomplete data provenance coexist | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.6_Electroweak_Physics` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 1 | `manual or placeholder` | benchmark packaging is weaker than the README tone | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.7_Neutrino_Physics` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 1 | `manual or placeholder` | proof boundary and data workflow are under-documented | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.8_Muon_g2_Anomaly` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 0 | `manual or placeholder` | strong anomaly language outruns the standards package | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.9_Quantum_Nonlocality` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 1 | `embedded local only` | local evidence exists without an audit-grade contract | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.10_Fluid_Dynamics_Chaos` | `core` | `Structured` | `B` | 3 | 3 | 2 | 2 | 2 | 2 | `manifested real dataset` | latest run passes, but previous run fell below the speedup threshold | require repeated-run stability before restoring Tier A |
| `0.11_Phase_Transitions` | `core` | `Draft` | `B` | 2 | 2 | 1 | 1 | 1 | 1 | `real source referenced` | topic has active inputs but no verification standard | define a verification spec with explicit metrics, thresholds, baseline, and artifact output |
| `0.12_Vacuum_Energy_Casimir` | `core` | `Draft` | `B` | 2 | 2 | 1 | 1 | 1 | 1 | `real source referenced` | evidence exists but is not standardized | define a verification spec with explicit metrics, thresholds, baseline, and artifact output |
| `0.13_Thermodynamic_Bridge` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 1 | `manual or placeholder` | data reality still looks partly manual | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.14_Complex_Systems` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 1 | `embedded local only` | topic is active but unnormalized | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.15_Cluster_Dynamics` | `core` | `Draft` | `B` | 2 | 2 | 1 | 1 | 1 | 1 | `real source referenced` | sources are visible, verification is not | define a verification spec with explicit metrics, thresholds, baseline, and artifact output |
| `0.16_Heavy_Nuclei` | `core` | `Draft` | `B` | 2 | 2 | 1 | 1 | 1 | 1 | `real source referenced` | methods remain implicit rather than packaged | define a verification spec with explicit metrics, thresholds, baseline, and artifact output |
| `0.17_Mass_Generation` | `core` | `Draft` | `B` | 2 | 2 | 1 | 1 | 1 | 0 | `real source referenced` | strong claim language is still present | define a verification spec with explicit metrics, thresholds, baseline, and artifact output |
| `0.18_Mathnicry` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 1 | `manual or placeholder` | proof files exist, but proof scope is undocumented | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.19_Gravity_GR` | `core` | `Draft` | `B` | 2 | 2 | 1 | 1 | 1 | 1 | `real source referenced` | topic needs method, baseline, and limitations docs | define a verification spec with explicit metrics, thresholds, baseline, and artifact output |
| `0.20_Atomic_Physics` | `core` | `Draft` | `B` | 2 | 2 | 1 | 1 | 1 | 1 | `real source referenced` | research assets exist but are not packaged for audit | define a verification spec with explicit metrics, thresholds, baseline, and artifact output |
| `0.21_Yang_Mills_Mass_Gap` | `core` | `Structured` | `A` | 3 | 3 | 2 | 2 | 2 | 1 | `manifested real dataset` | strongest math-facing candidate still needs more conservative public wording | downgrade public wording so it matches the current evidence package |
| `0.22_Biophysics_Origin_of_Life` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 2 | `manual or placeholder` | active topic with incomplete data provenance | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.23_Unity_Scale_Link` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 2 | `embedded local only` | scale-link narrative is ahead of the standards package | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.24_Artificial_Intelligence` | `core` | `Draft` | `B` | 2 | 2 | 1 | 1 | 1 | 3 | `real source referenced` | public wording is relatively controlled, but verification is still weak | define a verification spec with explicit metrics, thresholds, baseline, and artifact output |
| 0.25_Strategy_Power_Economics | core | Structured | A | 3 | 3 | 3 | 2 | 1 | 3 | source-locked U.S. historical panel | Package Tier A only; 12 Evidence Grade A WARN gates remain open and Claim Class C controls | close measurement/source/license/energy gates, then causal and independent replication |
| `0.26_Cosmic_Dynamic_Frame` | `core` | `Draft` | `B` | 2 | 1 | 1 | 1 | 1 | 1 | `manual or placeholder` | data workflow still contains manual signals | document real dataset provenance and convert data handling into a manifest-backed workflow |
| `0.27_Cold_Light_Hologram` | `future` | `Draft` | `D` | 2 | 1 | 1 | 1 | 1 | 1 | `embedded local only` | exploratory topic remains outside the current theory-core credibility scope | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.28_Material_Synthesis` | `future` | `Draft` | `D` | 2 | 2 | 1 | 1 | 1 | 1 | `real source referenced` | future-facing topic has partial assets but is not part of the current theory-core audit | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.29_Ocean_Recovery` | `future` | `Draft` | `D` | 2 | 1 | 1 | 1 | 1 | 1 | `embedded local only` | exploratory application topic should not be counted as theory-core evidence | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.30_Mega_Flora_Biotech` | `future` | `Draft` | `D` | 1 | 0 | 1 | 1 | 1 | 1 | `no data path` | code and concept exist, but this phase does not treat it as theory-core evidence | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.31_SpaceTime_Propulsion` | `future` | `Draft` | `D` | 2 | 1 | 1 | 1 | 1 | 1 | `embedded local only` | future integration topic still lacks an evidence package appropriate for the current theory-core audit | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.32_Micro_Nuclear_Fusion` | `future` | `Draft` | `D` | 2 | 2 | 1 | 1 | 1 | 1 | `real source referenced` | future engineering topic is outside the current theory-core credibility scope | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.33_Battery_Tech` | `future` | `Draft` | `D` | 2 | 1 | 1 | 1 | 1 | 1 | `synthetic/local baseline` | standardized package exists, but no empirical dataset or external validation is present | keep this topic explicitly exploratory and separate it from theory-core credibility |
| `0.34_Information_Centric_Nanofabrication` | `future` | `Draft` | `D` | 1 | 1 | 1 | 1 | 1 | 1 | `embedded local only` | future concept area still missing several core pillars and manifests | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.35_ICN_Digital_Automation` | `future` | `Draft` | `D` | 1 | 0 | 1 | 0 | 1 | 3 | `no data path` | infrastructure shell with minimal research packaging | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.36_Orbital_Manufacturing` | `future` | `Draft` | `D` | 1 | 0 | 0 | 1 | 1 | 1 | `no data path` | README-driven vision topic with no auditable verification path | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.37_Quantum_Photovoltaics` | `future` | `Draft` | `D` | 1 | 0 | 1 | 0 | 1 | 3 | `no data path` | early shell topic with minimal evidence assets | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.38_Bio_Synthetic_Integration` | `future` | `Draft` | `D` | 2 | 0 | 1 | 1 | 1 | 2 | `no data path` | application concept lacks manifested data and standardized proof boundaries | keep this topic explicitly exploratory until real datasets, standards docs, and verification outputs exist |
| `0.39_Bio_Smart_City` | `future` | `Draft` | `D` | 2 | 1 | 1 | 1 | 1 | 1 | `synthetic/local baseline` | standardized local package exists, but city-scale claims lack empirical and external validation | keep this topic explicitly exploratory and outside theory-core credibility |

## Immediate conclusions

- Only `3` topics currently qualify as `Tier A`: `0.1`, `0.21`, `0.25`
- Most of the current theory-core (`0.0-0.26`) sits in `Tier B`, meaning research assets exist but the standards migration is unfinished
- `0.0_Grand_Unification` remains the only `Tier C` topic inside the core scope because it is broad, theory-central, and under-packaged
- All topics `0.27-0.39` are intentionally held in `Tier D` for this phase so they do not distort the credibility signal of the core theory audit
