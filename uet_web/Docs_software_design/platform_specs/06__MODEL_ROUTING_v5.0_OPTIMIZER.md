# 🎯 UET Model Routing (v5.0 — THE EXECUTION OPTIMIZER)

> **Related:** [[03__AGENT_ENGINE_v5.0_SPEC]] · [[05__FLOW_AND_EVENT_v5.0_SPINE]] · [[07__KNOWLEDGE_SYNC_v5.0_SPEC]] · [[25__WORKCHAT_AND_LIBRECHAT_BOUNDARY_v1]]

The Model Routing Engine v5.0 is the "Allocational Brain" of the Unity Mega-Platform. It dynamically directs every task to the most effective AI model based on complexity, cost, and safety requirements, ensuring hardware-agnostic intelligence.

---

## 🏛️ 1. Intelligent Model Routing (IMR) Pipeline
1.  **TASK CLASSIFICATION**: Determining depth (Fast, Deep, or Creative).
2.  **SIGNAL ANALYSIS**: Checking system health & provider latency via the **Event Bus**.
3.  **SCORING ENGINE**: Real-time calculation of the optimal model for the specific Intent.
4.  **ROUTING EXECUTION**: Dispatching the query to the chosen provider (Gemini, Claude, GPT).
5.  **NORMALIZATION**: Wrapping the output into the standard UET Unified JSON format.

---

## 🏗️ 2. The Model Pool (L0-L2)
- **L0 (Fast/Internal)**: Local LLMs or Small Flash models (e.g., Gemini Flash) for intent detection and normalization.
- **L1 (General/Professional)**: Mid-tier models (e.g., Gemini Pro, GPT-4o) for standard reasoning and RAG.
- **L2 (Deep/Axiomatic)**: High-reasoning models (e.g., Claude Opus, GPT-o1) for complex physics and system-level synthesis.

---

## 🛡️ 3. Routing Guardrails & Fallbacks
- **Cost Ceiling**: Automatic downgrade if the token budget for a project is exceeded.
- **Safety Over-ride**: If the **Flow Control** flags a request as "High Risk," it is routed only to audited "Safe-Tier" models.
- **Provider Failover**:
  ```
  Primary Fail (OpenAI) → Secondary (Anthropic) → Tertiary (Google) → Local (Ollama)
  ```

---

## 📤 4. Routing Contract (IMR v5.0)

### **Input Manifest**
```json
{
  "task_class": "Reasoning | Math | Coding",
  "priority": "Instant | Batch",
  "max_budget_tokens": 4000,
  "safety_tier": "Strict"
}
```

### **Routing Output**
```json
{
  "selected_model": "String",
  "route_reason": "String",
  "latency_estimate": "MS",
  "routing_id": "UUID"
}
```

---

> [!TIP]
> **Deterministic Routing**: Every routing decision is logged in the **Unity Ledger** to ensure that identical inputs are routed consistently for audit purposes.
