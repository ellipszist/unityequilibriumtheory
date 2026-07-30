# ADR 0001: Research First, Optional Platform Later

- Status: accepted for the current repository phase
- Date: 2026-07-30
- Scope: `services_and_experiments/`, `docs/knowledge_base/`, research workspaces

## Decision

The UET research workflow is the primary execution path. The code under
`services_and_experiments/` is retained as a future platform and experiment
area, but it is not a dependency of research, book writing, or policy work.

The repository source files, metadata, manifests, verifier artifacts, gates, and
update logs remain the controlling state. Knowledge-base indexes, MCP responses,
agents, APIs, and future GraphQL surfaces are derived or access layers only.

## Consequences

- A researcher must be able to work with services stopped or unavailable.
- `uet_core` is a reusable future-platform library, not the canonical research
  equation implementation or status authority.
- `uet_kb` may provide optional local retrieval, but an index must be
  regenerable from canonical sources and must expose source paths.
- `uet_agents` may orchestrate tasks, but it cannot decide claim strength,
  verifier status, or publication readiness.
- `uet_api` and GraphQL remain future interfaces until there is a stable client,
  schema, and a demonstrated use case.
- Platform CI and deployment must be explicitly opt-in while the platform is
  not active.

## Activation gate for a future service

Before a service becomes active, document the repeated problem it solves, its
input/output contract, provenance behavior, failure mode, test boundary, and
why maintenance costs less than the manual workflow it replaces.
