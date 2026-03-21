# 🔄 UET Flow & Event Spine (v5.0 — THE SYSTEM NERVOUS SYSTEM)

> **Related:** [[01__SYSTEM_CONTRACT_v5.0_CONSTITUTION]] · [[03__AGENT_ENGINE_v5.0_SPEC]] · [[10__SYSTEM_COORDINATION_v5.0_RULES]] · [[11__SLA_AND_VERIFICATION_v5.0_STABILITY]] · [[23__LATEST_PLATFORM_FLOW_v1]]

The Flow & Event Spine is the integration layer that guarantees the **Unity Mega-Platform** operates as a single, coherent mathematical entity. It combines **Flow Control (The Gatekeeper)** and the **Event Bus (The Communicator)** into a unified orchestration spine.

---

## 🛡️ 1. Flow Control: The Architecture of Trust
Flow Control governs every request before it reaches the reasoning or data layers.

### **1.1 The 4 Validation Layers**
1.  **INPUT LAYER**: Semantic/syntax sanitization and intent classification.
2.  **CONTEXT LAYER**: KB-version stability check (Block if Knowledge Sync is active).
3.  **PERMISSION LAYER**: Validation against the **Permission Matrix** (Axiomatic Trust).
4.  **SAFETY LAYER**: Loop detection and "Hallucination Guard" (Reflection check).

### **1.2 System Governor States**
- 🟢 **READY**: Normal operation.
- 🟡 **BUSY**: Resource throttling (rate limit active).
- 🔴 **LOCKDOWN**: Critical fault detected (Orphan vector or Version Sync failure).

---

## 📡 2. Event Bus: The Pulse of Synchronization
The Event Bus ensures all distributed components (Rust core, Agents, UI) are perfectly aligned.

### **2.1 Core Event Groups**
| Group | Key Events | Reaction |
| :--- | :--- | :--- |
| **Knowledge** | `KB_VERSION_UPDATED` | Immediate Cache Purge & Agent Reset |
| **Security** | `CONTRACT_VIOLATION` | Blacklist Agent |
| **Execution** | `AGENT_STEP_FINISH` | Audit Ledger Write |
| **System** | `SYSTEM_LOCKDOWN` | Global Halt |

### **2.2 Delivery Model: "Ordered Fanout"**
- **Strict FIFO**: Events must be delivered in the order they occurred.
- **Project Isolation**: Events are strictly bound to their `project_id`.
- **Atomic Persistence**: Every state-changing event is committed to the **Unity Ledger**.

---

## 🔄 3. State-Machine Logic (The Spine Loop)
1.  **ACTION RECEIVED** → Flow Control checks Governor State.
2.  **VALIDATION GATES** → If fail, emit `FLOW_ERROR` event and abort.
3.  **EXECUTION** → Engine performs task and emits `STEP_DONE` events.
4.  **STATE SYNC** → Event Bus broadcasts changes; RAG/Cache invalidate; Registry increments `kb_version`.

---

> [!IMPORTANT]
> **Deterministic Rollback**: Any failure in the Spine Loop triggers an immediate rollback to the last confirmed state in the **Axiomatic Registry**.
