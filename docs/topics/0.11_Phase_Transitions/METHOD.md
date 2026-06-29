# Method

## Problem target

This topic studies whether UET-style transition rules can reproduce selected critical-point and order-parameter benchmarks.

## Core components

### Engine components
- `Code/01_Engine/Engine_Phase.py`

### Proof-oriented components
- `Code/02_Proof/Proof_Order_Parameter.py`

### Research and comparison components
- `Code/03_Research/Research_Critical_Exponents.py`
- `Code/03_Research/Research_Spatial_Coupling_Scaling.py`
- `Code/03_Research/Research_Spatial_Coupling_Sensitivity.py`
- `Code/03_Research/Research_Correlation_Length_Diagnostics.py`
- `Code/03_Research/Research_Finite_Size_Scaling_Diagnostics.py`
- `Code/03_Research/Research_Critical_Window_Relaxation_Diagnostics.py`
- `Code/03_Research/Research_Operator_Form_Requirement_Gate.py`
- `Code/03_Research/Research_Spatial_Coupled_V2_Diagnostic.py`
- `Code/03_Research/Research_Spatial_Coupled_V2_Component_Ablation.py`
- `Code/03_Research/Research_Model_C_Conserved_Order_Diagnostic.py`
- `Code/03_Research/Research_Conserved_Order_Core_Candidate.py`
- `Code/03_Research/Research_Conserved_Order_Numerics_Gap.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_Core_Candidate.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_Scaling.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_Window_Repair.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_Spinodal_Window.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_Seed_Margin.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_Finite_Size_Replication.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_L16_Relaxation_Repair.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_L16_Estimator_Sensitivity.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_L16_Structure_Factor_Estimator.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_Structure_Factor_Multigrid_Calibration.py`
- `Code/03_Research/Research_Conserved_Order_Spectral_Structure_Factor_L20_Probe.py`
- `Code/03_Research/Research_Structure_Factor_Acceptance_Rule_Gate.py`
- `Code/03_Research/Research_Structure_Factor_Estimator_Reconciliation_Gate.py`
- `Code/03_Research/Research_Structure_Factor_Calibration_Source_Support_Gate.py`
- `Code/03_Research/Research_Structure_Factor_Source_Manifest_Gate.py`
- `Code/03_Research/test_05_phase_demixing.py`
- `Code/03_Research/test_phase_transitions.py`

## Variable framing

- Primary modeled quantities: critical temperature, order parameter, critical exponents, and transition-scale quantities
- Formula registry: see `FORMULA_AUDIT.md` for the distinction between selected exponent benchmarks, normalized Cahn-Hilliard dynamics, order-parameter diagnostics, and future material-data gates.

## Assumptions

- The topic is currently a phenomenological comparison package tied to selected critical-point datasets.
- The primary verifier also writes `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, and `branch_claim_gate.json` so selected beta compatibility stays separate from wider universality claims.

## Domain of validity

- Selected fluids and materials transition benchmarks represented in topic-local files.

## Excluded cases

- A general renormalization-group derivation for all transition classes.

## Parameter sensitivity note

- Critical exponents and fit settings remain dependent on the chosen benchmark subset.
- The current primary verifier is deliberately narrow: it checks only the beta critical exponent for a 3D Ising/liquid-gas benchmark.
- The Wave 5 spatial-coupling verifier is a dynamics diagnostic gate; it currently keeps universality-shift claims blocked.
- The Wave 6 coefficient sensitivity verifier narrows the blocker further: coefficient-only tuning remains mean-field-like, so the next repair needs operator-form or estimator revision.
- The Wave 7 correlation-length verifier checks whether the simulation window exposes critical correlation growth; it currently blocks beta-only universality promotion.
- The Wave 8 finite-size verifier checks multi-grid xi/L and Binder-style proxy behavior; it currently blocks universality promotion because xi/L stays small and the spatial lane does not separate from baseline.
- The Wave 9 critical-window relaxation verifier checks whether closer-to-Tc temperatures and longer runs fix the small-xi blocker; it currently shows the window extension is still local.
- The Wave 10 operator-form requirement verifier aggregates Waves 5-9 and blocks claim upgrades until a revised opt-in operator demonstrates nonlocal, conserved, or scale-dependent correlation growth and baseline separation.
- The Wave 11 v2 diagnostic tests the first such opt-in candidate using core-engine screened memory and conserved interface/game helpers; it currently blocks claim upgrades because correlation growth and lane separation did not appear.
- The Wave 12 v2 component-ablation verifier separates information-only, game-only, full, short-memory, and long-memory profiles; it currently shows no tested v2 component improves correlation length over baseline.
- The Wave 13 Model C verifier uses `Engine_Phase.py` to test conserved order-parameter dynamics as a different operator family; it currently supports Model C as a mechanism repair direction while leaving finite-size scaling and core integration open.
- The Wave 14 core-candidate verifier tests `conserved_order_v1` inside `uet_master_equation.py`; it currently confirms opt-in availability, legacy compatibility, and mass conservation, while blocking the explicit core path on mechanism response.
- The Wave 15 numerics-gap verifier compares Wave 13 spectral Cahn-Hilliard settings with the Wave 14 explicit core candidate; it currently blocks coefficient-only repair and requires a spectral or semi-implicit conserved-order core path before rerunning scaling claims.
- The Wave 16 spectral-core verifier tests `conserved_order_spectral_v1` inside `uet_master_equation.py` against the existing topic spectral engine; it passes implementation/mechanism bridge gates and moves the next blocker to finite-size/exponent scaling.
- The Wave 17 spectral-scaling verifier runs a normalized 3D finite-size sweep for `conserved_order_spectral_v1`; it passes stability and coverage gates but blocks universality promotion on `xi/L` window and beta-exponent gates.
- The Wave 18 window-repair verifier separates relaxation/window-only repairs from kappa sensitivity and requires `xi/L` gains to preserve order-parameter signal before they count as scaling evidence.
- The Wave 19 spinodal-window verifier finds a single-grid order-preserving `xi/L` candidate but keeps claim upgrades blocked until seed-margin and finite-size replication pass.
- The Wave 20 seed-margin verifier extends the same normalized window to `4000` steps and passes the target seed-margin gate at `L=16`; claim upgrades remain blocked until multi-grid finite-size replication passes.
- The Wave 21 finite-size replication verifier reruns the target window across `L=8,12,16` and both Wave 20 plus fresh seed sets; it blocks promotion because `L=16` is not robust under fresh seeds.
- The Wave 22 `L=16` relaxation-repair verifier tests whether longer single-grid relaxation fixes the fresh-seed margin; it blocks relaxation-only repair and points the next work toward estimator/window-scaling design.
- The Wave 23 `L=16` estimator-sensitivity verifier tests whether the current axis-autocorrelation crossing threshold controls the fresh-seed margin; it finds the gate is threshold-sensitive, so the next work needs estimator derivation/calibration before any non-default threshold can be accepted.
- The Wave 24 `L=16` structure-factor verifier adds a threshold-free RMS length proxy; it confirms long-wavelength structure in the same fields but flags domain-scale risk, so the next work is multi-grid calibration rather than accepting a single-grid estimator.
- The Wave 25 structure-factor multi-grid verifier confirms the margin replicates across grid/seed cases, but blocks calibration because the estimator remains near the domain scale, especially at smaller grids.
- The Wave 26 L20 verifier shows the largest-grid `xi/L` can fall below the domain-scale warning threshold, but blocks claim use because a source-backed or derived acceptance rule is still missing.
- The Wave 27 acceptance-rule verifier defines a topic-derived preflight rule and keeps exponent use blocked because the current gridset fails domain-scale exclusion, absolute-length consistency, and estimator-reconciliation gates.
- The Wave 28 estimator-reconciliation verifier shows the structure-factor/axis-lower ratio is stable but uncalibrated, and both estimators show declining absolute length from L16 to L20.
- The Wave 29 source-support verifier scans the local reference package and blocks calibration acceptance until primary second-moment/finite-size estimator sources are packaged with formula boundaries.
- The Wave 30 source-manifest verifier packages primary estimator-source metadata but keeps formula extraction and calibration acceptance blocked.
- The Wave 31 formula-boundary verifier extracts the source-family second-moment estimator relation and blocks claim use of the current RMS inverse-k proxy.
- The Wave 32 lowest-mode candidate verifier implements that source-family relation on the existing L16/L20 fields and blocks replacement because the single-snapshot conserved-order lane lacks a valid `S(0)` susceptibility observable.
- Cahn-Hilliard simulations should be treated as normalized mechanism diagnostics until seed, grid, morphology, and material-unit gates are added.

## Dependency policy

- `0.4_Superconductivity_Superfluids` may reuse this topic's transition language only as a mechanism analogy until material-specific gates exist.
- `0.13_Thermodynamic_Bridge` may reference critical behavior only with the selected-exponent limitation.
- `0.0_Grand_Unification` should index this topic as a selected benchmark plus normalized mechanism model, not a full universality proof.
