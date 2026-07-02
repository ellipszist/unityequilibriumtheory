# History Recovery Log

## 2026-07-02 - Incubator research history bridge

This repository previously had substantial research work recorded on `codex/incubator-local-cleanup` / PR #5, but that branch used a separate history root and was never merged into `main`.

This recovery records that branch as reachable repository history without replacing the current `main` tree. The merge uses the current `main` content as the controlling file state, while preserving the incubator branch ancestry for audit and contribution history.

What this does:

- connects the incubator research commits to the main repository history
- avoids reintroducing destructive deletions, raw asset drift, or duplicate path drift from the old branch
- keeps PR #10 as the current content recovery batch
- leaves detailed content reconciliation for later scoped recovery passes

What this does not do:

- it does not promote all old incubator files as current source of truth
- it does not re-enable deleted/raw `uet_history` assets as website input
- it does not replace topic manifests, gates, or update logs

Controlling state after this bridge:

- file tree: current `main`
- recovered ancestry: `codex/incubator-local-cleanup`
- content recovery reference: `LOCAL_RECOVERY_MANIFEST.md`
