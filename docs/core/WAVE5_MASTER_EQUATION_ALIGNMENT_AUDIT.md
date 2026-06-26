# Wave 5 Master Equation Alignment Audit

**Status:** alignment audit for the Wave 5 spatial-coupling candidate. This file treats
`docs/core/00_inbox/` as intake evidence, not as canonical proof.

## Intake Evidence

- `docs/core/00_inbox/raw chat.md`: identifies the concern that the current math translates
  the UET space/information/game explanation into local additive terms.
- `docs/core/00_inbox/UET_Master_Equation_Analysis.md`: proposes multiplicative
  information coupling and gradient/interface-sensitive game coupling as candidate repairs.

## Controlling Blocker

`spatially_blind_engine_operator`

The legacy engine and historical 0.11 scaling scripts can add information/game terms without
forcing those terms to depend on spatial structure. That is enough to shift diagnostics, but it
does not by itself establish a universality-class change.

## Code Alignment Matrix

| Concern | Legacy behavior | Wave 5 candidate behavior | Current evidence boundary |
| :-- | :-- | :-- | :-- |
| Information coupling | `beta * C * I` in Omega; C dynamics source `-beta * I` | opt-in `0.5 * beta * C^2 * I`; C dynamics source `-beta * C * I` | heuristic bridge; unit closure still open |
| Game term | `V_game = beta_U * C^2` in Omega; no explicit legacy game force in `dynamics_step_complete` | opt-in `V_game = beta_U * |grad C|^2`; KPZ-style dynamics force from the same core helper | interface diagnostic only |
| Engine default | legacy local mode | unchanged unless `operator_mode="spatial_coupled_v1"` is selected | backward-compatible pilot |
| Phase-transition claim | selected beta JSON projection can pass | dynamics scaling must pass a separate gate | no RG/universality promotion yet |

## Wave 5 Artifact Result

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_spatial_coupling_scaling.json`

- `engine_alignment_gate`: `PASS`
- `spatial_operator_gate`: `PASS`
- `universality_shift_gate`: `BLOCKED`
- beta estimates: baseline `0.4912`, legacy local UET `0.5050`, spatial-coupled candidate `0.5081`

## Core Self-Test Follow-Up

The core script now reports all A11 limit checks as passing after the GL limit verifier was
made deterministic and isolated from UET extras:

- command: `.\.venv\Scripts\python.exe docs/core/uet_master_equation.py`
- `Ginzburg-Landau limit`: `PASS - Initial V=0.5242; Final V=0.0001`

This is verifier hygiene evidence only. It does not change the Wave 5 physics boundary or the
blocked universality-shift gate.

## Current Boundary

The Wave 5 candidate fixes the narrow implementation blocker that spatial operators were not
available in the core engine. It does not fix the physics blocker: the current candidate still
fits near mean-field behavior and does not shift toward the 3D Ising beta exponent.

## Next Hardening Step

Keep the spatial-coupled operator as an opt-in diagnostic candidate. The next wave should either
revise the candidate operator or add a stronger derivation/unit-closure package before rerunning
scaling claims.
