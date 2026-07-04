# UET Work Log

This folder records daily operating checkpoints for work that spans major UET
workspaces.

Use one file per day, named like `2026-07-04.md`.

Each completed work section should add a short entry with:

- timestamp or section label
- workspace or topic touched
- files or artifact groups changed
- verifier, audit, or review run, if any
- what remains uncommitted, private, or unsafe to publish
- next commit or push action

This log does not replace topic-level `UPDATE_LOG.md` files. Topic logs describe
research state changes. This folder tracks daily repository work so progress
does not sit invisible in local branches.

After 10 entries for unpushed work, stop expanding scope and make a checkpoint:
inspect status, stage only intended files, commit the safe unit, and push or open
a draft PR. If publishing is blocked, record the blocker here before continuing.