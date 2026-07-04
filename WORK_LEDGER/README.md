# UET Repo Work Ledger

This folder is the repo-level operating ledger for all UET work, not only
research topics.

Use it to keep daily progress visible across:

- research topics and standards
- theory history and book writing
- Thailand policy proposals
- services, experiments, MCP, GraphQL, and tooling
- repository operations, GitHub Actions, manifests, and agent rules
- raw/private source handling decisions

The ledger answers one question: what work moved today, what can be published,
and what still needs a commit, push, PR, or manifest?

## Daily Files

Use one file per day under the year folder:

```text
WORK_LEDGER/2026/2026-07-04.md
```

Each completed section of work should add one short entry. If 10 entries exist
for unpushed work, stop expanding scope and make a checkpoint before continuing.

## Relationship To Other Logs

- `WORK_LEDGER/` records repo-wide daily operating history.
- Topic `UPDATE_LOG.md` files record research-state changes for that topic.
- Manifests record what was included, excluded, private, duplicated, or too large.
- Git commits and PRs are the durable public evidence that work actually moved.

Do not use this ledger to upgrade research claims or replace artifacts. Use it
to prevent work from disappearing into local-only branches.