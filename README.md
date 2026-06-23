# Unity Equilibrium Theory Research Repository

This repository is the main research workspace for Unity Equilibrium Theory (UET).
It contains the active code, topic packages, verification artifacts, standards, and
documentation used to develop and audit the project.

This page is intentionally conservative. It is a repo entrypoint, not a claim upgrade.
For current topic status, follow the metadata and audit indexes inside `docs/`.

## What This Repository Is

- A research corpus centered in `docs/`, which serves as both the GitHub Pages source and the active codebase.
- A multi-topic workspace spanning theory-core physics topics, math-facing topics, and future concept branches.
- A standards-driven repo that now separates core evidence-bearing topics from exploratory application topics.

## What This Repository Is Not

- Not a certification that the theory is externally validated.
- Not a signal that every topic has reached the same level of auditability.
- Not an active cryptocurrency, mining network, or production platform implementation.

## Current Repo Baseline

The most current machine-readable repo summary is `docs/meta/topic_readiness.json`
(generated `2026-04-23`).

| Scope item | Current count |
| :-- | --: |
| Numbered topics | 42 |
| Core research topics | 27 |
| Future concept topics | 15 |
| Support workspaces | 2 |

Scope policy currently used in metadata:

- `0.0` through `0.26` are the theory-core research scope.
- `0.27` onward are future-concept or exploratory topics unless a later standards pass promotes them.
- `0.0_Grand_Unification` is treated as a foundation and integration layer, not as a blanket proof of all subordinate topics.

## Current Audit Snapshot

The repo no longer treats all topics as equally mature. Current public-facing summaries
should follow the audit tiers and status metadata rather than old badge language.

Current high-level picture from `docs/meta/topic_readiness.json` and `docs/meta/topic_executive_ranking.md`:

- Tier `A` structured core candidates currently include `0.1_Galaxy_Rotation_Problem`, `0.8_Muon_g2_Anomaly`, and `0.21_Yang_Mills_Mass_Gap`.
- Much of the theory-core remains Tier `B`: real research exists, but standardization, provenance, threshold stability, or claim-boundary work is still incomplete.
- `0.0_Grand_Unification` remains broad and integrative, so it should not be used as a shortcut around topic-level evidence.
- Topics `0.27+` should be treated as exploratory future concepts, not as current theory-confirmation evidence.

Some older prose indexes inside the repo still lag the latest machine-readable counts.
When counts or status summaries disagree, use the metadata in `docs/meta/` and the latest
topic-local artifacts before trusting older landing-page prose.

## Where Truth Lives

For repo-wide status or credibility questions, start here:

1. [`docs/topics/README.md`](./docs/topics/README.md) - conservative topic audit index
2. [`docs/meta/topic_readiness.json`](./docs/meta/topic_readiness.json) - machine-readable status baseline
3. [`docs/meta/topic_executive_ranking.md`](./docs/meta/topic_executive_ranking.md) - repo-wide execution priority
4. [`docs/meta/public_claim_risk_summary.md`](./docs/meta/public_claim_risk_summary.md) - pages whose wording currently outruns evidence
5. [`docs/topics/For Work/00_README.md`](./docs/topics/For%20Work/00_README.md) - standards workspace entrypoint

For repeated hardening or progress reconstruction, use:

- local topic `README.md`
- local `LIMITATIONS.md`
- local `VERIFICATION_SPEC.md`
- latest verifier artifact or blocker gate
- local `UPDATE_LOG.md` when the topic has gone through multiple waves

## Repository Structure

`docs/` is the working center of the repo.

```text
uet_harness/
|-- docs/
|   |-- core/                   # Core equations, shared parameters, common logic
|   |-- meta/                   # Repo-wide audit metadata and claim-risk summaries
|   |-- scripts/                # Runners, audit helpers, tooling
|   |-- topics/                 # Numbered topic packages plus support workspaces
|   |   |-- 0.0_Grand_Unification/
|   |   |-- 0.1_Galaxy_Rotation_Problem/
|   |   |-- ...
|   |   |-- 0.39_Bio_Smart_City/
|   |   |-- For Work/           # Canonical standards workspace
|   |   `-- General/            # Shared support workspace
|   `-- UET_Documentation_Details/
|-- .github/
|-- CONTRIBUTING.md
|-- LICENSE
`-- README.md
```

Each numbered topic generally follows the repo's topic architecture, with code, data,
result artifacts, references, and local documentation living inside the topic folder.
In practice, topics still vary in how fully they have been normalized to the standards.

## Topic Scope Map

### Theory-core research scope

The current credibility core for this phase is `0.0-0.26`. These topics determine the
scientific maturity of the repo more than the later application-oriented branches do.

Representative examples:

- `0.1_Galaxy_Rotation_Problem`
- `0.3_Cosmology_Hubble_Tension`
- `0.8_Muon_g2_Anomaly`
- `0.10_Fluid_Dynamics_Chaos`
- `0.20_Atomic_Physics`
- `0.21_Yang_Mills_Mass_Gap`

### Future-concept scope

Topics `0.27+` are currently exploratory unless explicitly promoted by a later standards pass.
They may contain simulations, design work, or proposal logic, but they should not be used as
theory-confirmation evidence by default.

Examples:

- `0.28_Material_Synthesis`
- `0.31_SpaceTime_Propulsion`
- `0.34_Information_Centric_Nanofabrication`
- `0.36_Orbital_Manufacturing`
- `0.39_Bio_Smart_City`

## Research Standards

The canonical operating manual for topic work is:

- [`docs/topics/For Work/00_README.md`](./docs/topics/For%20Work/00_README.md)

Important standards referenced throughout the repo:

- [`01_Project_Research_Constitution.md`](./docs/topics/For%20Work/01_Project_Research_Constitution.md)
- [`02_Project_Workflow_and_Lifecycle.md`](./docs/topics/For%20Work/02_Project_Workflow_and_Lifecycle.md)
- [`03_AI_Usage_and_Governance.md`](./docs/topics/For%20Work/03_AI_Usage_and_Governance.md)
- [`04_Claim_and_Evidence_Rubric.md`](./docs/topics/For%20Work/04_Claim_and_Evidence_Rubric.md)
- [`17_Formula_Audit_Standard.md`](./docs/topics/For%20Work/17_Formula_Audit_Standard.md)
- [`18_Research_Hardening_Workflow.md`](./docs/topics/For%20Work/18_Research_Hardening_Workflow.md)

Core rules that govern this repo:

- Do not let a topic outrun its evidence.
- Do not upgrade an internal fit into external validation.
- Do not present future-concept topics as if they already carry theory-core credibility.
- Prefer machine-readable gates, verifier artifacts, and update logs over memory-based summaries.

## Running The Repo

This repo is used as a Python research workspace rather than a root-level packaged product.

Typical setup:

```powershell
git clone https://github.com/unityequilibrium/UnityEquilibriumTheory.git
cd UnityEquilibriumTheory
. .\.venv\Scripts\Activate.ps1
pip install -r docs\requirements_ingest.txt
```

Common entrypoints:

- `python docs/topics/run_all_tests.py`
- `python docs/topics/run_full_verification.py`

Before treating the output of either runner as a public-facing status summary, compare it
against the topic-local verification specs and the repo metadata in `docs/meta/`.

## Notes On Historical Drift

Older root-level prose in this project often used stronger wording such as `solved`,
`verified`, or broad dashboard counts that no longer match the standardized audit view.
That drift is one reason the repo now keeps dedicated audit metadata and claim-risk summaries.

If you are updating docs, prefer:

1. metadata and topic artifacts first
2. standards workspace second
3. narrative cleanup afterward

## Quick Links

- [Topic audit index](./docs/topics/README.md)
- [Topic readiness metadata](./docs/meta/topic_readiness.json)
- [Executive ranking](./docs/meta/topic_executive_ranking.md)
- [Public claim risk summary](./docs/meta/public_claim_risk_summary.md)
- [Contributing guide](./CONTRIBUTING.md)

## License

Released under the [MIT License](./LICENSE).
