# Service Status and Boundary

This directory is a source-only future-platform and experiment area. Its code
does not control research status and is not required for ordinary work in
`docs/`, `uet_history/`, or `thailand_proposals/`.

## Current classification

| Component | Status | Role when activated | Current rule |
| :-- | :-- | :-- | :-- |
| `uet_core/` | `future` | reusable Rust calculation primitives | no authority over `docs/core` status |
| `uet_kb/` | `future` | optional retrieval/MCP implementation | derived index only; source paths required |
| `uet_agents/` | `experimental` | optional orchestration and ingestion helpers | cannot promote claims or gates |
| `uet_api/` | `future` | future application/API access layer | no production deployment |
| `uet_build/` | `experimental` | build/tooling experiments | no research dependency without a gate |
| `uet_chain/` | `future` | ledger/chain prototype | not a live network |
| `uet_security/` | `future` | signing and hashing primitives | not a production security boundary |
| `uet_miner/` | `archive` | historical mining experiment | not part of current UET research execution |
| `uet_under_development/` | `future` | unfinished economic, governance, market, oracle modules | no activation or publication claim |

## Dependency rule

The allowed direction is:

```text
canonical sources -> optional index/access layer -> future clients
```

The reverse direction is prohibited: a service, index, agent, API, or GraphQL
response must not become the source of truth for a research claim, topic gate,
book state, or provenance record.

## Activation checklist

A component stays `future`, `experimental`, or `archive` until a scoped decision
records:

1. the repeated manual problem it solves
2. its input/output and provenance contract
3. its behavior when unavailable
4. its test boundary and regeneration path
5. the maintenance and compute cost compared with the manual workflow

Do not add GraphQL, public API, authentication, deployment, or vector-service
dependencies merely because the future architecture mentions them.
