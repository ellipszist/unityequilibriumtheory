# Unity Equilibrium Theory Research Repository

This repository is now organized as a research-first workspace.

The active source of truth is `docs/`. Platform prototypes, application code,
runtime experiments, build outputs, and deployment scaffolding have been moved
out of the main view so the repository is easier to study and maintain.

## Current Structure

```text
uet_harness/
  docs/                    Active UET research, theory, evidence, validation, data, and reports.
  uet_history/             Historical notes and prior UET writing archive retained at root.
  .github/                 Repository automation and GitHub metadata.
  .venv/                   Local Python environment. Recreate if needed; do not treat as source.
  CITATION.cff             Citation metadata.
  CONTRIBUTING.md          Contribution notes.
  LICENSE                  License.
```

## Rules

- Do not mix platform app development back into this repository root.
- Do not modify or reorganize `docs/` during platform cleanup work.
- Non-research platform/prototype material has been moved outside this repo.
- `docs/` and `uet_history/` should not be used as dumping grounds for platform app code.
- If the platform is revived later, create a separate repository with a proper product spec, UX/UI design package, implementation roadmap, and engineering ownership.

## Research Entry Points

- `docs/README.md`
- `docs/core/README.md`
- `docs/topics/README.md`
- `docs/UET_Documentation_Details/README.md`

## Platform Status

The platform effort is paused. Existing platform/application work has been
archived because it did not yet represent the intended super-app architecture.
Future platform work should begin from professional product documentation and a
separate implementation repository, not from the archived prototypes.

Local archive path from this cleanup:

```text
C:\Users\santa\Desktop\uet_non_research_archive_2026-04-27
```
