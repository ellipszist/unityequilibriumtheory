# Update Log: 0.11 Phase Transitions

## Wave: Spatial-Coupling Coefficient Sensitivity (Wave 6)

**What changed:**
- Added `Research_Spatial_Coupling_Sensitivity.py` to test whether coefficient-only tuning of the current `spatial_coupled_v1` operator can move beta away from mean-field.
- Added machine-readable artifact `Result/artifacts/0_11_spatial_coupling_sensitivity.json` and CSV `Result/gl_spatial_coupling_sensitivity_stats.csv`.
- Updated topic docs to treat coefficient-only tuning as a blocked repair path rather than a likely route to a universality shift.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupling_Sensitivity.py`

**Which blocker narrowed:**
- Narrowed `universality_shift_gate` into `coefficient_only_spatial_operator_still_mean_field`.
- The sensitivity artifact tested 20 coefficient cases and found beta range `0.4729` to `0.5243`; best beta was `0.4729`, with zero cases near the 3D Ising reference under the declared tolerance.

**Next controlling blocker:**
- Coefficient tuning is not enough. The next wave needs a revised operator form, nonlocal/scale-dependent term, or correlation-length-aware estimator before rerunning stronger scaling claims.

**Current topic-level status after wave:**
- The spatial candidate remains diagnostic-only. No RG closure, universality-class shift, or phase-transition-solution claim is supported.

---
## Wave: Core GL Limit Verifier Stabilization (Wave 5 follow-up)

**What changed:**
- Made `verify_ginzburg_landau_limit()` deterministic and explicitly pure-GL: seeded RNG, disabled UET extras (`W_N`, exchange, viscosity, inertia), and used enough integration time for the local potential to relax toward the `C0` minimum.
- Did not change the core dynamics operator or promote the spatial-coupled candidate claim.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/core/uet_master_equation.py`
- `.\.venv\Scripts\python.exe docs/core/test/test_spatial_coupling.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Critical_Exponents.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupling_Scaling.py`

**Which blocker narrowed:**
- Narrowed the residual core self-test blocker: `Ginzburg-Landau limit` changed from `FAIL - Final V about 0.5212` to `PASS - Initial V=0.5242; Final V=0.0001`.
- The Wave 5 spatial artifact still records `engine_alignment_gate == PASS`, `spatial_operator_gate == PASS`, and `universality_shift_gate == BLOCKED`.

**Next controlling blocker:**
- `universality_shift_gate` remains the controlling topic blocker. Current beta estimates remain near mean-field: baseline `0.4912`, legacy local UET `0.5050`, spatial-coupled candidate `0.5081`.

**Current topic-level status after wave:**
- Core verifier hygiene improved, but the phase-transition dynamics claim remains diagnostic-only. No RG closure, universality-class shift, or phase-transition-solution claim is supported.

---
## Wave: Spatial-Coupling Candidate Gate (Wave 5)

**What changed:**
- Added an opt-in `spatial_coupled_v1` operator mode to the core master equation while preserving `legacy_local` as the default.
- Added candidate information coupling `0.5 beta C^2 I` and interface-sensitive game coupling through `|grad C|^2`.
- Added `Research_Spatial_Coupling_Scaling.py` to compare baseline TDGL, historical local UET, and the new spatial-coupled candidate.
- Added `docs/core/WAVE5_MASTER_EQUATION_ALIGNMENT_AUDIT.md` to map inbox claims to code behavior without treating inbox text as canonical proof.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/core/test/test_spatial_coupling.py`
- `.\.venv\Scripts\python.exe docs/core/uet_master_equation.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Critical_Exponents.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupling_Scaling.py`

**Which blocker narrowed:**
- Narrowed `spatially_blind_engine_operator`: the core engine now exposes an opt-in spatial candidate and the artifact records `engine_alignment_gate == PASS` and `spatial_operator_gate == PASS`.

**Next controlling blocker:**
- `universality_shift_gate` remains `BLOCKED`. The Wave 5 artifact estimates beta near mean-field: baseline `0.4912`, legacy local UET `0.5050`, spatial-coupled candidate `0.5081`, versus 3D Ising reference `0.3265`.

**Current topic-level status after wave:**
- Spatial operator availability is hardened, but the candidate remains diagnostic-only. No RG closure, universality-class shift, or phase-transition-solution claim is supported.

---
## Wave: Synthetic GL V4 Benchmark (Scaling Analysis & Critical Exponents)

**What changed:**
- Opening Wave 4 to move beyond energy convergence into New Physics verification.
- Implemented `simulate_uet_scaling.py` using a 3D grid ($16 \times 16 \times 16$) to properly reflect 3D system topology.
- Converted static parameter $a$ to temperature-dependent $a(T) = a_0 \frac{T - T_c}{T_c}$.
- Injected strict Langevin thermal noise to the baseline TDGL to allow proper phase fluctuations near $T_c$.
- Extracted the Order Parameter Exponent ($\beta$) via Log-Log linear regression.

**Which verifier was run:**
- `uv run --with numpy --with matplotlib --with pandas --with scipy docs/topics/0.11_Phase_Transitions/Code/simulate_uet_scaling.py`

**Which blocker narrowed:**
- Evaluated the hypothesis that UET modifies the universality class ($\beta \to 0.33$).
- Result: Baseline yielded $\beta \approx 0.5188$. Full UET yielded $\beta \approx 0.4983$.

**Next controlling blocker:**
- The UET terms ($\Phi_N$ and $V_{game}$) in their current mathematical form do **not** break the system out of the Mean-Field universality class. The theoretical claim that UET shifts universality to 3D Ising is currently refuted by empirical simulation.
- Theoretical derivation must be revised: Is the game-shift term modifying the $C^4$ scaling, or is it merely shifting the effective temperature $T_c$?

**Current topic-level status after wave:**
- Critical Exponent hypothesis failed empirical validation. UET remains in the Mean-Field class.

---

## Wave: Synthetic GL V3 Benchmark (Statistical Validation)

**What changed:**
- Added `simulate_uet_gl_v3.py` to scale the diagnostic to 100 seeds.
- Froze hyperparameters (`a`, `b`, `kappa`, `Gamma`, `mu_G`, `eta_U`, `phi_noise`, `Gamma_N`) before execution.
- Added Paired Difference ($E_{UET} - E_{Baseline}$) and Win Rate calculation logic.

**Which verifier was run:**
- `uv run --with numpy --with matplotlib --with pandas --with scipy docs/topics/0.11_Phase_Transitions/Code/simulate_uet_gl_v3.py`

**Which blocker narrowed:**
- Addressed the small sample size (5 seeds) caveat from V2.
- The V3 result over 100 seeds shows UET wins 60% of the time, with a paired difference mean of -0.000511 ± 0.002225 J.
- Internally measured a small effect-size signal, though variance remains high.

**Next controlling blocker:**
- The effect size (mean paired difference) is modest. We need to analyze whether the UET components can be calibrated to a broader physical scope, or if the transition rules need scaling analysis (e.g., studying critical exponents at the transition boundary rather than just final energy depths).

**Current topic-level status after wave:**
- UET passes the first synthetic GL smoke benchmark: the Full UET lane achieves a lower mean final GL energy and beats the TDGL baseline in 60% of seeds. However, this is not yet a formal benchmark pass due to effect size bounds.

---

## Wave: Synthetic GL V2 Benchmark

**What changed:**
- Added `simulate_uet_gl_v2.py` as a diagnostic artifact.
- Fixed unit leakage in $\Phi_N$ by introducing rate coefficient $\Gamma_N$ ($m^3/(J\cdot s)$).
- Implemented full $\Omega_{UET}$ energy tracking instead of just GL free energy.
- Added ablation lanes (Baseline, PhiN, Vgame, UET) and multi-seed statistical validation (5 seeds).

**Which verifier was run:**
- `uv run --with numpy --with matplotlib --with pandas docs/topics/0.11_Phase_Transitions/Code/simulate_uet_gl_v2.py`

**Which blocker narrowed:**
- Removed unit error blocker and eliminated conflated evidence by tracking the full functional.

**Current topic-level status after wave:**
- Smoke Test Pass with caveats.
