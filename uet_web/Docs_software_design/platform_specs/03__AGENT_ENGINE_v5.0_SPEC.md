# 🧠 UET Agent Engine (v5.0 — THE REASONING CORE)

> **Related:** [[04__RAG_ENGINE_v5.0_SPEC]] · [[05__FLOW_AND_EVENT_v5.0_SPINE]] · [[06__MODEL_ROUTING_v5.0_OPTIMIZER]] · [[24__AI_AGENT_MEMORY_ARCHITECTURE_v1]] · [[01__SYSTEM_CONTRACT_v5.0_CONSTITUTION]] · [[23__LATEST_PLATFORM_FLOW_v1]]

The Agent Engine v5.0 is the "Central Brain" of the Unity Mega-Platform, responsible for interpreting evidence, executing complex reasoning, and orchestrating multi-agent collaboration with absolute determinism.

---

## 🏛️ 1. Architecture: The ReAct Loop (v5.0)
UET Agents operate within a strict **Planner-Executor-Reflector** cycle:

1.  **PLAN (Intent Module)**: Analyze query goal, select Agent Profile, and generate an **Execution Graph**.
2.  **QUERY (RAG Engine)**: Retrieve "Axiomatic Proofs" (EvidenceSet) from the UKG.
3.  **EXECUTE (Action Layer)**: Run the Execution Graph steps (Tool calls, API, sub-agents).
4.  **REFLECT (Reflector Module)**: Validate results against the **System Constitution** and detect potential loops.

---

## 🕸️ 2. Execution Graph & Orchestration
Instead of linear scripts, v5.0 uses a **Directed Acyclic Graph (DAG)** to control flows:
- **Nodes**: Specific tasks (e.g., `RAG_NODE`, `CALC_NODE`, `REASON_NODE`).
- **Edges**: Conditional logic based on step results.
- **Explainability**: Every node transition is logged in the **Execution Trace** for total auditability.

---

## 👥 3. Multi-Agent Ecosystem (State Isolation)
v5.0 enforces strict **Separation of Concerns**:
- **Planner Agent**: The Architect.
- **Research Agent**: The deep-diving RAG specialist.
- **Physics Agent**: The `uet_core` math specialist.
- **Governance Agent**: The security/permission gatekeeper.
- **Isolation**: Each agent has its own memory boundary; communication only occurs via the **Event Bus**.

---

## 🛡️ 4. The Safety Layer (The Fortress)
- **Deterministic Guard**: If Input A + Evidence B results in anything other than Output C, the run is invalidated.
- **Loop Detection**: Automated abort if repeating reasoning patterns are detected within N steps.
- **Permission Firewall**: No agent can execute a tool that exceeds their user-level **Access Matrix**.
- **Zero-Stale Check**: Refuse to reason if `kb_version` is not the absolute latest recorded in the Ledger.

---

## 📥 5. Input/Output Contract

### **Input Template**
```json
{
  "task_id": "UUID",
  "intent": "ASK | TASK | RESEARCH",
  "evidence_set": "Evidence[]",
  "agent_profile": "Profile_ID",
  "safety_tier": "Strict | Relaxed"
}
```

### **Output Template**
```json
{
  "answer": "String",
  "reasoning_trace": "Log[]",
  "axiom_links": "Axiom_ID[]",
  "next_step": "Graph_Node | null"
}
```

---

> [!CAUTION]
> **Reasoning Hallucination**: Hallucinations are categorized as a "System Critical Failure." Agents that fail the Reflection phase are automatically blacklisted from the current session.
