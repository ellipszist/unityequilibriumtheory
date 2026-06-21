# Peterson Branch Identity Policy

## Purpose

This file narrows the remaining `0.13` quantum-Landauer blocker one step beyond
`composite source conflict`.

The branch is not only unresolved.
Current evidence is now strong enough to separate the incompatible candidate
families behind the legacy local `Peterson 2018` label:

- `Peterson` authorship points to a `2016` NMR-based quantum thermodynamics paper
- the trapped-ion / single-atom quantum-Landauer narrative points to a different
  `2018` PRL paper
- the currently stored Nature Physics DOI points to a mesoscopic entropy paper
  that matches neither the trapped-ion system nor the Peterson-led authorship

So the next useful policy is not to keep treating `Peterson 2018` as if it were
one fuzzy paper.
The next useful policy is to demote that local label and keep the branch generic
until one exact paper is selected.

## Current authority

- Machine-readable artifact:
  `Data/03_Research/peterson_branch_identity_policy.json`
- Supporting files:
  - `PETERSON_2018_SOURCE_CONFLICT.md`
  - `docs/data/external/thermodynamics/landauer/peterson_2018/source_record.json`
  - `Data/03_Research/row_closure_matrix.json`
  - `Data/03_Research/source_evidence_intake_stub.json`

## Candidate-family split

### 1. Peterson-led quantum thermodynamics paper

- upstream paper:
  `Experimental demonstration of information to energy conversion in a quantum system at the Landauer limit`
- publication:
  `Proc. R. Soc. A 472, 20150813 (2016)`
- DOI:
  `10.1098/rspa.2015.0813`
- why it matters:
  this is the current strongest fit to the local `Peterson` authorship cue
- why it is not the same as the current local runtime branch:
  it is `2016`, not `2018`, and its reported setup is an NMR-based quantum system
  rather than the trapped-ion single-atom narrative

### 2. Trapped-ion quantum-Landauer paper

- upstream paper:
  `Single-Atom Demonstration of the Quantum Landauer Principle`
- publication:
  `Phys. Rev. Lett. 120, 210601 (2018)`
- DOI:
  `10.1103/PhysRevLett.120.210601`
- why it matters:
  this is the current strongest fit to the local trapped-ion / first-quantum-Landauer
  narrative
- why it is not the same as the current local Peterson cue:
  the authorship does not match the local Peterson label

### 3. Nature Physics entropy-measurement paper

- upstream paper:
  `Direct entropy measurement in a mesoscopic quantum system`
- publication:
  `Nature Physics 14, 1083-1086 (2018)`
- DOI:
  `10.1038/s41567-018-0250-5`
- why it matters:
  this is the current strongest fit to the local DOI only
- why it is not the same as the local runtime narrative:
  it does not match the trapped-ion single-atom narrative and does not resolve
  the Peterson-led authorship cue either

## Policy

- Do not use the local label `Peterson 2018` as if it identifies one paper.
- Do not let the branch enter row capture, uncertainty propagation, or benchmark
  language under that label.
- Treat the current runtime entry as a generic unresolved quantum-Landauer
  placeholder only.
- Only after one exact paper is chosen may the branch re-enter row-level closure
  work.

## Minimum closure rule after this policy

The branch may move forward only when the topic package has:

1. one exact upstream paper identity
2. one matching DOI or official URL
3. one original file or table identity
4. one row-level value capture with unit convention
5. one explicit mapping from that row into the runtime branch

## Claim boundary

This policy narrows the Peterson blocker by separating the incompatible source
families behind the local label.
It does not yet identify the final benchmark paper, capture any row-level value,
or close uncertainty propagation.
