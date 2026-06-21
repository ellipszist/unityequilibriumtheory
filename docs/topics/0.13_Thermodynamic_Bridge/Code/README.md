# Topic 0.13: Thermodynamic Bridge - Code

> [!WARNING]
> This file is a legacy code map, not the authority for current `0.13` claim scope.
> Current allowed wording is controlled by the topic root files and by
> `Result/artifacts/0_13_thermodynamic_bridge_verification.json`.
> Use this page to locate scripts, not to infer proof, closure, or final validation status.

## Current boundary

- Primary status authority:
  - `../README.md`
  - `../METHOD.md`
  - `../LIMITATIONS.md`
  - `../VERIFICATION_SPEC.md`
  - `../FORMULA_AUDIT.md`
  - `../Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Current strongest supported lane:
  - Landauer lower-bound consistency and standard thermodynamic-gravity identity checks
- Blocked or incomplete lanes:
  - UET bridge proof
  - source-normalized Landauer closure
  - external heat-transport validation
  - derived beta-bridge coefficient claim

## 5x4 structure

```text
Code/
  01_Engine/
    Engine_Thermodynamics.py
  02_Proof/
    Proof_Entropy_Max.py
  03_Research/
    Research_Landauer.py
    Research_Real_Data_Validation.py
    Research_Thermodynamic_Bridge.py
  04_Competitor/
    (currently empty)
```

## Script roles

### 01_Engine
- `Engine_Thermodynamics.py`: topic-local thermodynamic helper engine and proxy calculations.

### 02_Proof
- `Proof_Entropy_Max.py`: legacy proof-oriented script for the topic's entropy-mixing interpretation.

### 03_Research
- `Research_Landauer.py`: primary verifier and current status authority for lower-bound/formula-consistency lanes.
- `Research_Real_Data_Validation.py`: legacy cross-check script that mixes Landauer, black-hole, and Josephson diagnostics; useful only with current topic claim boundaries in mind.
- `Research_Thermodynamic_Bridge.py`: legacy integration script; not the current status authority for bridge-proof claims.

## Run commands

```powershell
python docs/topics/0.13_Thermodynamic_Bridge/Code/01_Engine/Engine_Thermodynamics.py
python docs/topics/0.13_Thermodynamic_Bridge/Code/02_Proof/Proof_Entropy_Max.py
python docs/topics/0.13_Thermodynamic_Bridge/Code/03_Research/Research_Landauer.py
python docs/topics/0.13_Thermodynamic_Bridge/Code/03_Research/Research_Real_Data_Validation.py
python docs/topics/0.13_Thermodynamic_Bridge/Code/03_Research/Research_Thermodynamic_Bridge.py
```

## Reading guidance

- Treat `Research_Landauer.py` as the main current verifier.
- Treat the other research scripts as legacy or diagnostic surfaces unless their outputs are explicitly re-threaded into the root documentation and verifier artifact.
- Do not use this file's existence as evidence that `0.13` has a closed first-principles thermodynamic bridge.
