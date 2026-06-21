# Peterson 2018 Source Conflict

## Purpose

This file isolates the current `Peterson 2018` blocker inside the `0.13` quantum-Landauer branch.

The problem is not only that row-level values are missing.
The topic package currently contains a composite source-reference conflict:

- the local runtime module names `Peterson et al. Nature Physics (2018)` and uses DOI `10.1038/s41567-018-0250-5`
- Crossref for `10.1038/s41567-018-0250-5` resolves to `Direct entropy measurement in a mesoscopic quantum system`, a Nature Physics mesoscopic-entropy paper rather than a trapped-ion quantum-Landauer article
- Crossref for `10.1103/PhysRevLett.120.210601` resolves to `Single-Atom Demonstration of the Quantum Landauer Principle`, which matches the trapped-ion quantum-Landauer narrative but not the local Peterson authorship label

So the branch is not just missing a citation.
It currently mixes incompatible DOI, title, system, and authorship cues.

Until that composite conflict is resolved, the `Peterson` branch must remain outside promotion and gate logic.
Current evidence is also strong enough to demote the local `Peterson 2018` label itself:
it should no longer be treated as if it names one exact benchmark paper.

## Current authority

- Machine-readable artifact: `Data/03_Research/peterson_2018_source_conflict.json`
- Supporting files:
  - `docs/data/external/thermodynamics/landauer/peterson_2018/source_record.json`
  - `Data/03_Research/source_evidence_intake_stub.json`
  - `Data/03_Research/source_evidence_readiness_matrix.json`
  - `ROW_CLOSURE_MATRIX.md`

## Current runtime state

- local topic label: `Peterson et al. Nature Physics (2018)`
- local DOI in working data module: `10.1038/s41567-018-0250-5`
- local system description: `Trapped Ca-40 ion`
- local claim: `First quantum verification of Landauer principle`

## Current evidence state

- verified Nature Physics DOI target: `Direct entropy measurement in a mesoscopic quantum system`, `Nature Physics 14, 1083-1086 (2018)`, DOI `10.1038/s41567-018-0250-5`
- verified PRL DOI target: `Single-Atom Demonstration of the Quantum Landauer Principle`, `Physical Review Letters 120, 210601 (2018)`, DOI `10.1103/PhysRevLett.120.210601`
- verified Peterson-led paper identity from the official Proceedings of the Royal Society A article page: `Experimental demonstration of information to energy conversion in a quantum system at the Landauer limit`, `Proc. R. Soc. A 472, 20150813 (2016)`, DOI `10.1098/rspa.2015.0813`
- inference from these two primary metadata checks: the local runtime branch is currently composite, not source-locked

This last sentence is an inference from the DOI metadata checks above, not a direct statement by either publisher.

## Narrowed policy consequence

The branch no longer needs to be described only as `source identity unresolved`.

It can now be described more precisely:

- `Peterson` authorship is one candidate family
- the trapped-ion / single-atom quantum-Landauer paper is a different candidate family
- the current Nature Physics DOI is a third, non-matching candidate family

So the local label `Peterson 2018` should now be treated as a demoted legacy placeholder,
not as an active benchmark label awaiting only row capture.

## Minimum closure rule for this branch

Do not treat the `Peterson 2018` branch as source-identified unless the topic package has:

1. one exact upstream paper identity
2. one exact DOI or official URL matching the local narrative
3. one original file or table identity
4. one row-level value capture with unit convention
5. one explicit mapping from that source row into the local runtime branch

## Current claim boundary

While this conflict remains open, the `Peterson 2018` branch may support only:

- blocker navigation
- documentation that a quantum-Landauer lane was considered but is currently composite and not yet source-resolved

It must not support:

- source-locked quantum-Landauer validation
- row-level uncertainty propagation
- stronger wording than `source identity unresolved`

## Use rule

Use this file when selecting the next narrow hardening move for the `Peterson` branch.
It is a blocker-navigation note, not a promotion artifact.
