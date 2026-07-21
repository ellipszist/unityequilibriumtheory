# UET GR Closed-Limit and Non-Closed Response Research Specification

> **Status:** `HYPOTHESIS / CANDIDATE PROGRAM`
> **Current claim class:** `A`
> **Current controlling blocker:** `covariant_parent_action_missing`
> **Program rule:** General relativity is the null/closed-response model. A
> non-zero UET response is an empirical alternative, not a conclusion assumed
> from the existence of the model.

## 1. Research question

Can UET be written as a generally covariant, causal, history-dependent
effective theory in which:

1. Einstein gravity is recovered exactly when exchange, dissipation, memory,
   and the additional space-response sector are switched off;
2. a non-closed effective matter-spacetime sector obeys an explicit covariant
   balance law;
3. matter amount can remain conserved even when matter stress-energy exchanges
   with the effective space-response sector;
4. the derived trace remains an observable of past dissipation and never acts
   as an independent source; and
5. data can distinguish a non-zero UET response from the exact GR null model
   without fitting and testing on the same evidence.

The program does **not** assume that the complete universe is thermodynamically
open to an exterior. Global closure remains unresolved until a boundary,
environment, or operational global balance definition exists.

## 2. Nested theory contract

The intended hierarchy is

```text
causal non-closed UET
    -- exchange, dissipation, and memory -> 0 -->
conservative covariant response theory
    -- epsilon_nc -> 0 and Phi -> Phi_* -->
Einstein general relativity
```

This reduction must be a continuous parameter limit. Deleting equations by
hand, cancelling unrelated fitted parameters, or taking a coefficient to
infinity does not count as GR recovery.

The nested hypotheses are

```text
H0: epsilon_nc = 0       -> Einstein GR
H1: epsilon_nc != 0      -> UET non-closed response candidate
```

The existence of `H1` does not establish that nature selects it. A physical
non-closed claim requires independent evidence that rejects or materially
outperforms `H0` after parameter penalties and holdout testing.

## 3. Closure taxonomy

| Closure level | Mathematical condition | Locked interpretation |
| --- | --- | --- |
| Matter amount | `nabla_mu N^mu = 0` | No creation or destruction of the declared matter-number current. |
| Matter stress-energy | `nabla_mu T_m^(mu nu) = Q^nu` | `Q = 0` means separately closed matter stress-energy; `Q != 0` means exchange with another modeled sector. |
| Total modeled balance | `nabla_mu (T_m + T_UET)^(mu nu) = 0` | Required by the covariant parent unless a separate global-nonconservation branch is explicitly opened. |
| GR closed-response limit | `epsilon_nc = 0` with open kernels disabled | The UET correction vanishes and the Einstein field equation remains. |
| Complete-universe closure | unresolved | No current artifact establishes an exterior, global reservoir, or global nonconservation law. |

Einstein's equations provide a local covariant balance through the contracted
Bianchi identity. That identity is not, by itself, a statement that arbitrary
curved spacetimes possess one globally conserved thermodynamic energy.

## 4. Ontology

| Symbol | Role | Independent physical state? | Claim boundary |
| --- | --- | --- | --- |
| `g_mu_nu` | spacetime metric | yes in the future gravity solver | Standard geometric variable. |
| `Psi_m` | relativistic matter variables | yes | Must be a scalar, spinor, gauge field, or fluid current with declared transformation law. |
| `N^mu` | matter-number current | derived from matter state | Used only in lanes where matter amount is meaningful. |
| `Phi` | effective space-response variable | yes in the candidate parent | A collective response degree of freedom; not information, antimatter, or a particle identification. |
| `Pi` | response rate in a 3+1 reduction | yes in reduced dynamics | Must be derived from the covariant state rather than inserted as a second ontology. |
| `Q^nu` | covariant exchange current | no; derived from coupled equations | Records transfer between modeled sectors, not missing energy. |
| `R` | derived trace observable | no | Retarded functional of a physical production source; no feedback edge is allowed. |
| `epsilon_nc` | nesting coupling | model parameter | `0` is exact GR. It is not a percentage of how open the universe is. |

`Phi = Phi_*` denotes an ordered reference, not empty or nonexistent space. The
word `ordered` becomes claim-bearing only after the parent theory demonstrates
a stable stationary point and defines an entropy current or equivalent
measurable ordering criterion.

## 5. Conservative covariant parent target

The first implementation uses a scalar response pilot because it is the
smallest covariant representation. It is not assumed to be the final dynamic
frame ontology.

In natural units (`c = hbar = 1`), use the candidate action

```text
S = integral sqrt(-g) [
      F_epsilon(Phi)/(2 kappa_E) (R_scalar - 2 Lambda)
      - epsilon_nc Z_Phi/2 (nabla Phi)^2
      - epsilon_nc U(Phi)
    ] d^4x
    + S_m[g, Psi_m]
```

with

```text
delta_Phi = Phi - Phi_*
F_epsilon = 1 + epsilon_nc xi_Phi delta_Phi^2
U(Phi) = rho_* + m_Phi^2/2 delta_Phi^2
                 + lambda_Phi/4 delta_Phi^4
```

Required coefficient policy:

- `epsilon_nc >= 0` and dimensionless;
- `Z_Phi > 0`;
- `m_Phi^2 >= 0`;
- `lambda_Phi > 0`;
- `xi_Phi` has mass dimension `-2`;
- `kappa_E` has mass dimension `-2`;
- `rho_*` has mass dimension `4`.

The equilibrium conditions

```text
F_epsilon(Phi_*) = 1
dF_epsilon/dPhi at Phi_* = 0
dU/dPhi at Phi_* = 0
```

prevent a hidden first-order curvature or fifth-force source at the ordered
reference. If `rho_* != 0`, the constant response is reported as

```text
Lambda_eff = Lambda + kappa_E epsilon_nc rho_*
```

rather than being described as missing energy.

The metric equation target is

```text
F G_mu_nu + Lambda F g_mu_nu
  + (g_mu_nu box - nabla_mu nabla_nu) F
  = kappa_E [T_m_mu_nu + epsilon_nc T_Phi_mu_nu]
```

where

```text
T_Phi_mu_nu = Z_Phi nabla_mu Phi nabla_nu Phi
              - g_mu_nu [Z_Phi/2 (nabla Phi)^2 + U(Phi)]
```

The first code wave is a tensor-formula evaluator and exact-limit verifier. It
is not a metric PDE solver, a curved-spacetime simulation, or a Bianchi proof.

## 6. GR closed-limit contract

The exact null limit is

```text
epsilon_nc -> 0
Q^nu -> 0
open influence kernel -> 0
Phi -> Phi_*
nabla Phi -> 0
Pi -> 0
```

and must yield

```text
G_mu_nu + Lambda g_mu_nu = kappa_E T_m_mu_nu
```

Required implementation properties:

- no division by `epsilon_nc`;
- arbitrary response inputs make no contribution when `epsilon_nc = 0`;
- the GR residual is identical component by component, not merely close after
  fitting;
- a constant equilibrium density is either zero or mapped explicitly to
  `Lambda_eff`;
- the GR limit remains valid before and after the later nonrelativistic
  reduction.

## 7. Non-closed causal extension target

Ordinary single-copy conservative variation is not sufficient for generic
retarded dissipation. The next parent layer will therefore use a causal
influence-functional or closed-time-path contract:

```text
S_eff[+, -] = S_cons[+] - S_cons[-] + S_IF[+, -]
```

The physical balance must take one of two explicit branches:

1. **Exchange-completed branch (primary):**
   `nabla T_m = Q`, `nabla T_UET = -Q`; the observed sector is non-closed while
   the modeled total remains Bianchi-consistent.
2. **Global-nonconservation branch (deferred/high risk):** requires an explicit
   boundary, external sector, broken diffeomorphism contract, or alternative
   geometry. It may not be inferred from branch 1.

The derived trace target is

```text
R(x) = integral G_ret(x, x') [nabla_mu s^mu](x') d^4x'
```

and remains outside the physical equation graph.

## 8. Reduction to the existing matter-space model

After the covariant and open-sector gates pass, a documented 3+1, weak-field,
slow-motion, and near-equilibrium reduction must recover the normalized
`matter_space_coupled_v1` structure or identify exactly why it does not.

The present variables cannot be promoted directly:

- frame-dependent density `C` must map to a covariant matter scalar or current,
  such as a scalar pilot field or `n = sqrt(-N_mu N^mu)`;
- `Phi` and `Pi` must arise from the covariant response state;
- normalized coefficients require an explicit natural-unit and later SI map;
- the existing causal-leakage failure remains a blocker for physical
  propagation language.

## 9. Verification program

### Core gates

- symbolic GR closed-limit residual: exactly zero;
- deterministic numeric closed-limit residual: `<= 1e-12`;
- stable ordered reference and positive local Hessian;
- symmetric response stress tensor;
- action-density mass dimension: `4` in the natural-unit lane;
- metric-equation residual mass dimension: `2`;
- no hidden division by `epsilon_nc`;
- Bianchi/exchange balance: open until the causal sector exists;
- characteristic and ghost gates: open until PDE principal symbols exist;
- derived trace backreaction: forbidden.

### Gravity gates

After the parent passes: Minkowski, Schwarzschild/de Sitter/FLRW closed
solutions, Newtonian/PPN reduction, light bending, perihelion, Shapiro delay,
redshift, gravitational-wave propagation, equivalence principle, and
short-range constraints.

### Empirical model comparison

Every application compares the nested pair `epsilon_nc = 0` and
`epsilon_nc != 0`. Parameter policy and holdout rows are locked before the
claim-bearing run. A fit on the same rows used for evaluation is diagnostic
only.

## 10. Falsification rules

The program is reduced or rejected in a lane if:

- GR appears only after manual term deletion or singular parameter tuning;
- the metric equation violates its covariant balance identity;
- a propagating response has ghosts, gradient instability, or superluminal
  characteristics outside its declared EFT domain;
- the entropy or exchange ledger cannot close;
- the response works only when derived trace `R` is fed back;
- external constraints force `epsilon_nc = 0` in all independent lanes;
- a claimed effect disappears on holdout or under resolution refinement; or
- the formulation is observationally identical to an existing theory while
  retaining an unsupported novelty claim.

## 11. Topic dependency order

1. `docs/core` and topic `0.19`: covariant parent and GR closed limit.
2. Topics `0.10` and `0.13`: causal constitutive and thermodynamic controls.
3. Topic `0.11`: nonrelativistic internal diagnostic only.
4. Topics `0.12` and `0.23`: equilibrium-density, units, and cross-scale policy.
5. Topics `0.1` and `0.26`: galaxy and dynamic-frame tests after gravity gates.
6. Particle/Dirac topics: deferred until local Lorentz, spinor, current, and
   CPT contracts exist.

## 12. Claim boundary

Allowed now:

- `GR correspondence hypothesis`
- `candidate non-closed effective matter-spacetime sector`
- `implemented one-dimensional nonrelativistic prototype`
- `derived trace with no backreaction`

Blocked now:

- `the universe is proved open`
- `Einstein equations derived from UET`
- `UET is Lorentz invariant`
- `UET validates GR`
- `space response is antimatter, ether, or a particle`
- `dark matter replaced`

## 13. Primary comparison literature

- T. Jacobson, *Thermodynamics of Spacetime: The Einstein Equation of State*,
  <https://arxiv.org/abs/gr-qc/9504004>.
- C. Eling, R. Guedens, and T. Jacobson, *Non-equilibrium Thermodynamics of
  Spacetime*, <https://arxiv.org/abs/gr-qc/0602001>.
- C. R. Galley, *The Classical Mechanics of Non-conservative Systems*,
  <https://arxiv.org/abs/1210.2745>.
- M. Crossley, P. Glorioso, and H. Liu, *Effective Field Theory of Dissipative
  Fluids*, <https://arxiv.org/abs/1511.03646>.
- T. Harko et al., *f(R,T) gravity*, <https://arxiv.org/abs/1104.2669>.
- T. Jacobson and D. Mattingly, *Gravity with a Dynamical Preferred Frame*,
  <https://arxiv.org/abs/gr-qc/0007031>.

These are comparison frameworks and constraints on method choice. They are not
evidence that UET is correct.
