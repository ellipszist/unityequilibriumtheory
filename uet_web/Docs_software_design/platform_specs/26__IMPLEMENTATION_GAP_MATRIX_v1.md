# UET v5.0 — Implementation Gap Matrix v1

> **Related:** [[23__LATEST_PLATFORM_FLOW_v1]] · [[27__PHASED_EXECUTION_PLAN_v1]] · [[24__AI_AGENT_MEMORY_ARCHITECTURE_v1]]

This matrix compares the current codebase with the target v5.0 platform specifications so that implementation can proceed in a controlled and phased manner.

---

## 1. Status Key
- **Implemented**: present in a usable form.
- **Partial**: present, but below target architecture.
- **Missing**: specified but not materially implemented.
- **Deferred**: intentionally postponed to a later phase.

---

## 2. Core Gap Matrix

| Domain | v5.0 Target | Current State | Gap | Priority | Recommended Phase |
|---|---|---|---|---|---|
| Workchat UX | research studio with deterministic backend flow | usable prototype in `uet_web` | Partial | High | 1-2 |
| Flow Control | 4-layer validation governor | minimal local handling | Missing | High | 2 |
| Agent Engine | Planner-Executor-Reflector + Execution Graph | single-path semantic engine | Missing | High | 2-3 |
| RAG Engine | version-safe vector + graph evidence pipeline | simple chunk matching | Missing | High | 3 |
| Knowledge Sync | diff/chunk/embed/vector/registry pipeline | direct ingest to local JSON state | Missing | High | 3 |
| Model Routing | tiered routing with fallback and audit | fixed OpenRouter call for formatting | Partial | Medium | 2-3 |
| Memory Architecture | working/semantic/episodic/procedural separation | partial semantic persistence only | Missing | High | 2 |
| Rust Core Integration | stable API + data-backed orchestration | Rust bridge exists but startup depends on DB | Partial | High | 4 |
| Audit / Ledger | execution trace and proof recording | minimal local trace | Missing | Medium | 4-5 |
| MCP / External Connectivity | universal access via MCP/API | partial API surface | Partial | Medium | 4-5 |
| Social / Room Layer | academic collaboration platform | mostly spec-level | Deferred | Low | 5+ |
| Economy / PoUW | verified commit layer | UI hints and conceptual wiring only | Deferred | Low | 5+ |

---

## 3. Current Code Mapping

| Code Area | Role Today | Limitation |
|---|---|---|
| `uet_web/src/components/workchat/*` | local product-facing research chat prototype | not yet backed by full Flow/RAG/Agent separation |
| `uet_agents/semantic_engine.py` | local semantic retrieval and response composition | not a full agent engine or versioned retriever |
| `uet_agents/api_server.py` | thin FastAPI bridge | no executive router or structured memory interfaces |
| `uet_api/src/agent.rs` | Rust-to-Python proxy path | still downstream of DB-sensitive Rust startup |
| `uet_api/src/main.rs` | route registration and app startup | database required before local API becomes useful |

---

## 4. Gap Interpretation

### High-Priority Gaps
- explicit architecture docs for latest flow,
- central executive / memory system,
- backend contract cleanup,
- retrieval and ingestion structure.

### Medium-Priority Gaps
- model routing formalization,
- audit and trace capture,
- stable Rust reintegration path.

### Lower-Priority Gaps
- full economic commitment path,
- social room system,
- broader decentralized mesh features.

---

## 5. Phase Rule
- **Phase 1**: close understanding gaps with docs and diagrams.
- **Phase 2**: close backend architecture gaps.
- **Phase 3**: close retrieval and sync gaps.
- **Phase 4**: close integration and infrastructure gaps.
- **Phase 5**: expand into platform-scale social/economic features.

---

## 6. Success Criteria for This Matrix
A feature should move from **Partial** or **Missing** only when:
- a clear contract exists,
- a real code path exists,
- the path is stable enough to be the default development route,
- the behavior is understandable from `platform_specs` without relying on historical documents.
