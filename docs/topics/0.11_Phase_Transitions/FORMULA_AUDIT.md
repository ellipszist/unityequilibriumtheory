# Formula Audit: 0.11 Phase Transitions

## Scope

This registry covers the current phase-transition calculation paths: spectral
Cahn-Hilliard evolution, chemical potential, free-energy/order-parameter diagnostics, BEC
critical temperature, 3D Ising critical-exponent comparison, and competitor/test solvers. It
separates standard benchmark relations from UET heuristic projection claims and numerical
demonstrations.

## Formula Registry

| formula_id | relation | code surface | variables and units | constant_origin | proof_status | verification_role | failure_mode | next_hardening_step |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `PT-CH-EVOLUTION` | `dC/dt = M nabla^2(delta F/delta C)` | `Engine_Phase.step` | `C` dimensionless concentration/order field; `M` mobility proxy; `dt` simulation time step; grid units normalized | `checked_local_reference` Cahn-Hilliard form | `checked local numerical relation` | engine diagnostic | Numerical stability depends on grid, `dt`, `kappa`, and noise; visual domains are not a physical proof by themselves. | Add convergence sweep over grid size, seed, `dt`, and `kappa`. |
| `PT-FREE-ENERGY` | `F[C] = int [alpha/2 C^2 + gamma/4 C^4 + kappa/2 |grad C|^2] dV` | `Engine_Phase.compute_chemical_potential` comments and implementation | `alpha`, `gamma`, `kappa` dimensionless in normalized solver; `C` dimensionless | `topic_derived_relation` / Cahn-Hilliard benchmark structure | `heuristic bridge` | diagnostic | Solver uses normalized parameters, so physical material energy units are not established. | Document nondimensionalization and map to a material dataset if making physical claims. |
| `PT-CHEM-POTENTIAL` | `mu = alpha C + gamma C^3 - kappa nabla^2 C` | `Engine_Phase.compute_chemical_potential` | `mu` normalized potential; `C` dimensionless; `nabla^2` normalized grid operator | `checked_local_reference` | `checked local numerical relation` | engine diagnostic | Sign or FFT convention errors alter phase separation. | Add unit tests comparing FFT Laplacian to finite-difference reference. |
| `PT-SPECTRAL-UPDATE` | `C_new_hat = (C_hat - dt M k^2 NL_hat + noise_hat)/(1 + dt M kappa k^4)` | `Engine_Phase.step` | Fourier amplitudes dimensionless; `k` normalized wave number | `topic_derived_relation` from semi-implicit CH update | `checked local numerical relation` | engine diagnostic | Incorrect implicit denominator can create artificial stability or growth. | Record seed, initial condition, and spectral diagnostics in artifact. |
| `PT-ORDER-PARAMETER` | `order = mean(abs(C))` | `Engine_Phase.get_extra_metrics`; `Proof_Order_Parameter.py` | dimensionless order proxy | `topic_derived_relation` | `diagnostic proxy` | proof/test diagnostic | Threshold such as `order > 0.7` is simulation-specific, not universal phase-transition proof. | Calibrate threshold against known demixing simulations or mark as internal-only. |
| `PT-DOMAIN-COUNT` | zero-crossing count over sign of `C` | `Engine_Phase._count_domains` | count dimensionless | `topic_derived_relation` | `diagnostic proxy` | visualization/diagnostic | Sensitive to noise and grid resolution; not a robust domain morphology metric. | Replace or supplement with structure factor / correlation length. |
| `PT-BEC-TC` | `Tc = (hbar omega/k_B) * (N/zeta(3))^(1/3)` | `Engine_Phase.compute_bec_tc` | `omega` rad/s; `N` count; output K | `source_locked_physics_constant` plus standard trapped-BEC relation | `checked local benchmark relation` | diagnostic only | Not used by primary phase-transition gate; cannot support broad transition claims. | Add explicit BEC verifier if this becomes claim-bearing. |
| `PT-BETA-UET` | `beta_UET ~= 1/D_eff`; current data uses `0.333` | `Research_Critical_Exponents.py`; `critical_exponents.json` | `beta` dimensionless critical exponent | `heuristic_bridge` | `heuristic bridge with internal benchmark pass` | primary verifier gate | A close beta match does not derive `gamma`, `nu`, scaling relations, or full RG universality. | Extend verifier to `gamma`, `nu`, and scaling laws; source-lock benchmark references. |
| `PT-BETA-ERROR` | `relative_error = abs(beta_UET - beta_exp)/beta_exp * 100` | `Research_Critical_Exponents.py` | percent | `topic_derived_relation` | `identity` | primary verifier metric | If only beta is tested, README must not claim full phase-transition theory closure. | Keep claim to selected 3D Ising/liquid-gas beta exponent until broader gates exist. |

## Current Formula Boundary

- The strongest current result is a selected beta-exponent internal benchmark.
- Spectral Cahn-Hilliard simulation demonstrates a normalized mechanism but is not yet mapped
  to physical material units.
- Order emergence and symmetry-breaking language must remain model/diagnostic wording unless
  backed by broader exponent, morphology, and material-data gates.
## Wave 5 Spatial-Coupling Candidate Addendum

| formula_id | relation | code surface | variables and units | constant_origin | proof_status | verification_role | failure_mode | next_hardening_step |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `PT-UET-LEGACY-INFO` | `Omega_info = beta C I`; `dC/dt += -beta I` | `docs/core/uet_master_equation.py::information_coupling`; `information_dynamics_source` | `C` normalized order field; `I` normalized information field; units remain normalized/proxy in topic 0.11 | `heuristic_bridge` | `legacy local operator` | compatibility baseline | Local source can act without requiring mass/interface structure, so it can stay spatially blind. | Keep as legacy comparator only unless a derivation requires it. |
| `PT-UET-SPATIAL-INFO-CANDIDATE` | `Omega_info = 0.5 beta C^2 I`; `dC/dt += -beta C I` | `information_coupling(..., operator_mode="spatial_coupled_v1")`; `information_dynamics_source` | `C` normalized order field; `I` normalized information field; unit closure open | `heuristic_bridge` | `candidate heuristic bridge` | diagnostic gate input | Wrong coefficient/sign can create artificial damping or noise response without physical closure. | Derive or reject the multiplicative information term before stronger claims. |
| `PT-UET-SPATIAL-GAME-CANDIDATE` | `V_game = beta_U |grad C|^2`; dynamics candidate `F_game = c_kpz V_game` | `game_theory_potential`; `game_theory_force` | `grad C` normalized grid gradient; `beta_U` strategic boost; units proxy/open | `heuristic_bridge` | `candidate diagnostic-only` | spatial operator gate | Passing interface sensitivity does not imply RG closure or universality shift. | Add unit closure and compare against accepted interface-growth/scaling references. |
| `PT-SPATIAL-SCALING-GATE` | fit `log(<|C|>) = beta log(Tc-T)+b` for baseline, legacy, and spatial lanes | `Research_Spatial_Coupling_Scaling.py`; `0_11_spatial_coupling_scaling.json` | beta dimensionless; synthetic normalized TDGL grid | `topic_derived_relation` | `diagnostic artifact` | hardening gate | Current Wave 5 result remains near mean-field: baseline `0.4912`, legacy `0.5050`, spatial `0.5081`. | Keep universality claims blocked until `universality_shift_gate` passes with documented derivation. |
| `PT-SPATIAL-COEFFICIENT-SENSITIVITY` | sweep `spatial_information_coupling` and `spatial_game_coupling`; fit beta per case | `Research_Spatial_Coupling_Sensitivity.py`; `0_11_spatial_coupling_sensitivity.json` | beta dimensionless; reduced synthetic TDGL grid | `topic_derived_relation` | `diagnostic artifact` | blocker triage | Wave 6 found no tested coefficient-only case near 3D Ising beta; best beta `0.4729`, range `0.4729` to `0.5243`. | Stop treating coefficient strength as the likely repair; revise operator form or estimator. |
| `PT-CORRELATION-LENGTH-DIAGNOSTIC` | connected autocorrelation axis crossing proxy for `xi`; fit `xi ~ (Tc-T)^(-nu_proxy)` | `Research_Correlation_Length_Diagnostics.py`; `0_11_correlation_length_diagnostics.json` | `xi` grid units; `nu_proxy` dimensionless diagnostic | `topic_derived_relation` | `diagnostic artifact` | estimator gate | Wave 7 found weak spatial correlation growth: spatial `nu_proxy ~= 0.0324`, `xi_near/xi_far ~= 1.0668`. | Add finite-size/correlation-length-aware scaling before stronger universality claims. |

## Wave 5 Formula Boundary

The spatial-coupled operator is now available as an opt-in core candidate, but the current
scaling artifact does not support a claim that UET escapes mean-field behavior. The allowed
claim is limited to: a candidate spatial operator exists, its interface/zero-field gates pass,
and its current scaling result remains diagnostic-only.

## Wave 6 Coefficient Boundary

The coefficient sensitivity diagnostic narrows the blocker: changing the current candidate
coefficients alone did not shift the fitted beta exponent toward the 3D Ising target. The
allowed claim is limited to: coefficient-only tuning remains mean-field-like under the tested
grid, so the next hardening step needs a revised operator form, nonlocal/scale-dependent term,
or correlation-length-aware estimator.

## Wave 7 Estimator Boundary

The correlation-length diagnostic shows that the current synthetic temperature window does not
expose strong connected correlation-length growth. The allowed claim is limited to: beta-only
order-parameter fits are not enough for universality promotion, and the next hardening step
needs finite-size/correlation-length-aware scaling plus an operator form that separates from
baseline behavior.
