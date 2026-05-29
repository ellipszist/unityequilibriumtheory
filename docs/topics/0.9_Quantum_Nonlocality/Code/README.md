# Topic 0.9: Quantum Nonlocality - Code

This code layer contains quantum nonlocality engines, proof-oriented scripts, research
verifiers, and comparators. The current primary verifier is a source-referenced internal
CHSH summary benchmark. It does not reconstruct raw Bell event counts, derive a UET
nonlocality mechanism, replace standard quantum theory, or validate adjacent qubit,
double-slit, tunneling, DNA, or LC-unity branches.

## 5x4 Structure

```text
Code/
  01_Engine/
    Engine_Quantum.py              # diagnostic Tsirelson/tunneling engine
  02_Proof/
    Proof_Bell_Violation.py        # proof-oriented legacy note/script
  03_Research/
    Research_CHSH_Verification.py  # primary CHSH summary benchmark verifier
    Research_Bell_Inequality.py    # legacy/simulated CHSH path
    Research_Bell_Test.py          # simulated Bell-test path
    Research_Double_Slit.py        # adjacent quantum lane
    Research_DNA_Tunneling_Decay.py # adjacent quantum biology lane
    Research_Qubit_Mechanics.py    # adjacent qubit lane
  04_Competitor/
    Competitor_QM_Baseline.py      # standard quantum-mechanics comparator work
```

## Run Commands

```powershell
cd c:\Users\santa\Desktop\uet_harness

python docs/topics/0.9_Quantum_Nonlocality/Code/03_Research/Research_CHSH_Verification.py
python docs/topics/0.9_Quantum_Nonlocality/Code/01_Engine/Engine_Quantum.py
python docs/topics/0.9_Quantum_Nonlocality/Code/02_Proof/Proof_Bell_Violation.py
python docs/topics/0.9_Quantum_Nonlocality/Code/03_Research/Research_Bell_Test.py
python docs/topics/0.9_Quantum_Nonlocality/Code/03_Research/Research_Qubit_Mechanics.py
python docs/topics/0.9_Quantum_Nonlocality/Code/03_Research/Research_DNA_Tunneling_Decay.py
```

## Current Verification Status

Current authority: `../Result/artifacts/0_9_quantum_nonlocality_verification.json` and
`../VERIFICATION_SPEC.md`.

| Lane | Evidence | Current status | Claim boundary |
|:--|:--|:--|:--|
| CHSH summary benchmark | Hensen 2015 summary values | `PASS` | Source-referenced internal benchmark only |
| Raw Bell reconstruction | raw event counts / supplementary table package | `OPEN` | Not reconstructed locally |
| UET topology mechanism | topological-filament derivation | `BLOCKED` | No first-principles CHSH derivation artifact |
| Replacement-theory claim | comparison against standard nonlocality framework | `BLOCKED` | No replacement claim |
| Adjacent quantum lanes | qubit, double-slit, tunneling, DNA, LC-unity | `BLOCKED` for CHSH inheritance | Need separate source packages and verifiers |
| Claim-scope controller | `chsh_claim_scope_gate` | `CHSH_SUMMARY_ONLY_RAW_AND_MECHANISM_BLOCKED` | Export only the CHSH summary benchmark |

## Data Sources

- Hensen et al. 2015 CHSH working copy with DOI `10.1038/nature15759`
- External reference packages under `docs/data/external/quantum_nonlocality/`
- Raw Bell event counts or a supplementary-table reconstruction package are not yet locally
  archived and reconstructed.

## Engine / Proof Analysis

`Engine_Quantum.py` and `Proof_Bell_Violation.py` are useful mechanism-development surfaces,
but they do not override the primary artifact controller. The current evidence is a CHSH
summary benchmark, not a UET derivation of nonlocality.

## Claim Boundary

Allowed now:

- the recorded Hensen 2015 CHSH summary violates the local-realist bound under topic checks
- the stored quantum benchmark is consistent with the rounded Tsirelson value

Blocked now:

- raw Bell counts reconstructed
- UET proves nonlocality
- topological filament derivation verified
- standard quantum framework replaced
- qubit claims inherit CHSH PASS
- double-slit explained by CHSH
- tunneling validated by CHSH
- LC-unity quantum mechanism proved

## Key Formula

```text
S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
local realist bound: |S| <= 2
Tsirelson benchmark: 2 * sqrt(2)
```

See `../FORMULA_AUDIT.md` for formula roles, proof status, and failure modes.
