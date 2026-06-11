# UET Agent Operating Guide

This file is the root entrypoint for AI agents and collaborators working in this repository.

It does not replace the project standards. It tells an agent where truth lives, how to work
without inflating claims, and how to stay useful inside the actual UET workflow.

## Purpose

Use this file to orient quickly before editing code, rewriting docs, auditing a topic, or
answering research questions.

The repository already contains the full operating standard in
[`docs/topics/For Work/`](./docs/topics/For%20Work/). This guide is the short version for
day-to-day agent work.

## Project reality

- `docs/` is the main research codebase, documentation root, and GitHub Pages source.
- `docs/topics/` contains the numbered topic workspaces and the standards workspace.
- `docs/topics/For Work/` is the canonical operating manual for topic research work.
- `docs/meta/` and `docs/topics/README.md` are the preferred source of truth for current
  topic status, readiness, and claim restraint.
- Many files under `Result/`, `_Logs/`, generated reports, and audit outputs are artifacts,
  not the first place to make narrative decisions from memory.

## Default working style

This repository is often used for:

- auditing what is still weak, unclear, overstated, missing, or not yet standardized
- answering learning-oriented questions about how the repo works
- improving credibility, structure, verification discipline, and research legibility
- conducting topic research using the standards already documented in `For Work`

If the request is ambiguous, prefer:

1. inspect local evidence first
2. identify gaps, risks, or unclear claims
3. improve structure or wording conservatively
4. avoid promoting status unless the evidence clearly supports it

When work spans repeated repair passes, prefer a visible hardening loop:

1. package or confirm the current sources
2. regenerate one stable verifier artifact
3. add or tighten one machine-readable blocker gate
4. update the local topic docs to match the new blocker boundary
5. record the pass in the topic update log
6. commit the coherent change before starting the next wave

## Start here

Open these files first when you need repository-wide context:

1. [`README.md`](./README.md)
2. [`CONTRIBUTING.md`](./CONTRIBUTING.md)
3. [`docs/topics/README.md`](./docs/topics/README.md)
4. [`docs/topics/For Work/00_README.md`](./docs/topics/For%20Work/00_README.md)

Then choose the next standard by task.

## Reading order by task

### If the task is audit, cleanup, or credibility repair

1. [`docs/topics/For Work/01_Project_Research_Constitution.md`](./docs/topics/For%20Work/01_Project_Research_Constitution.md)
2. [`docs/topics/For Work/03_AI_Usage_and_Governance.md`](./docs/topics/For%20Work/03_AI_Usage_and_Governance.md)
3. [`docs/topics/For Work/04_Claim_and_Evidence_Rubric.md`](./docs/topics/For%20Work/04_Claim_and_Evidence_Rubric.md)
4. [`docs/topics/For Work/02_Project_Workflow_and_Lifecycle.md`](./docs/topics/For%20Work/02_Project_Workflow_and_Lifecycle.md)
5. [`docs/topics/For Work/18_Research_Hardening_Workflow.md`](./docs/topics/For%20Work/18_Research_Hardening_Workflow.md)

### If the task is topic building or refactoring

1. [`docs/topics/For Work/02_Project_Workflow_and_Lifecycle.md`](./docs/topics/For%20Work/02_Project_Workflow_and_Lifecycle.md)
2. [`docs/topics/For Work/10_Topic_Architecture_5x4.md`](./docs/topics/For%20Work/10_Topic_Architecture_5x4.md)
3. the relevant standards in `11-18`

### If the task is multi-wave hardening or progress reconstruction

1. [`docs/topics/For Work/18_Research_Hardening_Workflow.md`](./docs/topics/For%20Work/18_Research_Hardening_Workflow.md)
2. [`docs/topics/For Work/24_TEMPLATE_UPDATE_LOG.md`](./docs/topics/For%20Work/24_TEMPLATE_UPDATE_LOG.md)
3. the local topic `README.md`, `LIMITATIONS.md`, and `VERIFICATION_SPEC.md`

### If the task is mainly question answering or learning support

1. inspect the local files that already define the topic or workflow
2. answer from local evidence first, not memory
3. cite the exact file that acts as the current source of truth
4. say clearly when a conclusion is inference rather than an explicit repo statement

### If the task is repeated hardening, unblock work, or reconstruct progress

1. inspect the local topic package first
2. open [`docs/topics/For Work/18_Research_Hardening_Workflow.md`](./docs/topics/For%20Work/18_Research_Hardening_Workflow.md)
3. open [`docs/topics/For Work/24_TEMPLATE_UPDATE_LOG.md`](./docs/topics/For%20Work/24_TEMPLATE_UPDATE_LOG.md)
4. rebuild the current blocker chain from manifests, gates, and artifacts before changing prose

## Non-negotiable rules

- Do not let a topic outrun its evidence.
- Do not upgrade a fit into a prediction.
- Do not upgrade an internal rerun into external validation.
- Do not use hardcoded local paths when repository path helpers or relative structure should
  be used.
- Do not hide important physics logic or derivation-critical behavior in vague helper code.
- Do not rewrite repository status using stale counts from older prose when canonical
  metadata exists.
- Do not smooth uncertainty away just because a polished sentence sounds better.

## Claim discipline

Use conservative wording unless the repository clearly supports something stronger.

Preferred wording includes:

- `hypothesis`
- `proposal`
- `model`
- `derived relation`
- `reproduced internally`
- `passes current internal benchmark`
- `externally replicated`
- `peer-reviewed result`

Treat words like `solved`, `verified`, `proved`, `exact`, and `production grade` as
restricted unless the relevant local evidence explicitly justifies them.

For claim wording, defer to:

- [`docs/topics/For Work/04_Claim_and_Evidence_Rubric.md`](./docs/topics/For%20Work/04_Claim_and_Evidence_Rubric.md)
- [`docs/UET_Documentation_Details/STANDARDS/documentation_style_guide.md`](./docs/UET_Documentation_Details/STANDARDS/documentation_style_guide.md)

## When editing a topic

Before changing a topic narrative, inspect the local topic package first. Prefer this order
when files exist:

1. topic `README.md`
2. `METHOD.md`
3. `LIMITATIONS.md`
4. `VERIFICATION_SPEC.md`
5. relevant `FORMULA_AUDIT.md`
6. code, data, and result artifacts

When editing, preserve the distinction between:

- theory and benchmark behavior
- derivation and calibration
- internal evidence and external evidence
- exploratory concept work and core-credibility work

## Verification mindset

When asked to review or improve work, default to a verification-first mindset:

- look for broken structure, missing provenance, unclear baselines, weak thresholds, missing
  limitations, and inflated claims
- prefer explicit metrics and named artifacts over adjectives
- treat generated figures and logs as outputs that should be explained by scripts and inputs
- if a topic status is unclear, consult `docs/topics/README.md` and the metadata in
  `docs/meta/` before summarizing it
- if a topic has gone through many waves, prefer reconstructing the state from the update log,
  verifier artifact, and blocker gates together rather than from prose memory alone
- if a topic is moving through repeated repair passes, use the hardening workflow and keep an
  update log so later reviewers can reconstruct what changed and why

## Git workflow

Use `git` actively so work does not sit uncommitted for too long.

- check `git status` before editing so you know whether the tree is already dirty
- do not revert or overwrite unrelated user changes
- keep commits scoped to the files and task you actually touched
- prefer small, meaningful commits over one large end-of-session dump
- when a unit of work is stable, commit it instead of letting it linger
- if the repository already contains unrelated changes, stage only the intended files
- write commit messages that describe the real change plainly, especially for audits,
  standards, verification, and claim-discipline work

Suggested commit cadence:

1. finish one coherent change
2. run the relevant quick verification or review pass
3. stage only the intended files
4. commit before starting the next distinct chunk

For multi-wave hardening, a good unit is:

1. one blocker narrowed
2. one manifest or gate added or tightened
3. one verifier rerun if the artifact schema changed
4. one short update-log entry
5. one scoped commit

## Agent behavior expectations

- Be useful for audits, critique, normalization, and learning support.
- Prefer local evidence over speculation.
- Keep summaries legible and restrained.
- If evidence is mixed, say so plainly.
- If you infer something, label it as an inference.
- If a file in `For Work` already governs the decision, follow it instead of inventing a new
  rule.
- If a topic is stuck, aim to make the blocker narrower and more machine-readable before trying
  to make the claim stronger.

## Quick routing

- Claim sounds too strong: open
  [`04_Claim_and_Evidence_Rubric.md`](./docs/topics/For%20Work/04_Claim_and_Evidence_Rubric.md)
- AI-generated wording needs review: open
  [`03_AI_Usage_and_Governance.md`](./docs/topics/For%20Work/03_AI_Usage_and_Governance.md)
- Topic structure is messy: open
  [`10_Topic_Architecture_5x4.md`](./docs/topics/For%20Work/10_Topic_Architecture_5x4.md)
- Data provenance is weak: open
  [`12_Data_Standard.md`](./docs/topics/For%20Work/12_Data_Standard.md)
- Result artifacts are unclear: open
  [`14_Result_Standard.md`](./docs/topics/For%20Work/14_Result_Standard.md)
- Formula origin or units are unclear: open
  [`17_Formula_Audit_Standard.md`](./docs/topics/For%20Work/17_Formula_Audit_Standard.md)
- The topic is stuck in repeated `FAIL` or `WARN` cycles: open
  [`18_Research_Hardening_Workflow.md`](./docs/topics/For%20Work/18_Research_Hardening_Workflow.md)
- You need a durable record of what changed across waves: open
  [`24_TEMPLATE_UPDATE_LOG.md`](./docs/topics/For%20Work/24_TEMPLATE_UPDATE_LOG.md)

## One-line principle

Use the agent as a careful research assistant, auditor, and systems organizer, not as the
final authority that upgrades evidence by confidence alone.
