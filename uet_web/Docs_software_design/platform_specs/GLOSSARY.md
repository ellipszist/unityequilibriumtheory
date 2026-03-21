# UET v5.0 — Terminology Glossary & Standardization Guide

> **Related:** [[00__MASTER_BLUEPRINT_v5.0_FINAL]] · [[09__PLATFORM_ENERGY_UNITS]] · [[33__CREDIT_AND_SUBSCRIPTION_SPEC_v1]]

This document reconciles conflicting and overlapping terminology across the 35 platform specification documents. When writing new specs or updating existing ones, use the **Canonical Term** defined here.

---

## 1. Economic & Currency Terms

| Canonical Term | Also Known As | Source Docs | Resolution |
|---------------|--------------|-------------|------------|
| **Credits** | AEU, Axiomatic Energy Units, Platform Energy | Doc 09, 33 | Use **Credits** in user-facing context. "AEU" is the internal/theoretical name. Doc 33 is the canonical spec. |
| **UET Coin** | UET Token, UET Crypto | Doc 12, 14, 22 | Use **UET Coin** consistently. It is the on-chain asset backed by PoUW work. |
| **Negotiation Bonus** | Interaction Bonus | Doc 10 §7, Doc 12 §5 | Duplicated content. **Doc 10** is canonical reference. Remove from Doc 12 or replace with cross-reference. |
| **PoUW** | Proof of Useful Work | Doc 12, 14, 18 | Always expand on first use, then abbreviate. |
| **PoE** | Proof of Equilibrium | Doc 12, 14 | Always expand on first use, then abbreviate. |

---

## 2. Infrastructure & Architecture Terms

| Canonical Term | Also Known As | Source Docs | Resolution |
|---------------|--------------|-------------|------------|
| **Project** | Workspace, Room | Doc 15, 31 | Use **Project** for the main collaboration unit (Discord-like). It features Topic chats and an Obsidian-like file system. |
| **DEN** | Decentralized Educational Node | Doc 13 | Always expand on first use. |
| **Event Bus** | Event Spine, Flow Bus | Doc 05 | Use **Event Bus** for the message transport. "Flow" refers to Flow Control (the gatekeeper). |
| **Knowledge Sync** | KS Engine, Truth Harmonizer | Doc 07 | Use **Knowledge Sync** or **KS** as abbreviation. |

---

## 3. Layer & Tier Numbering

| Canonical Term | Also Known As | Source Docs | Resolution |
|---------------|--------------|-------------|------------|
| **L0–L5 (6-Tower Model)** | L0: API, L1: Flow, L2: Agent, L3: Knowledge, L4: Infra, L5: Economy | Doc 00, 23 | Use this layering in architecture diagrams. |
| **L1–L3 (Verification Layers)** | Verification Tiers | Doc 11 | This is a SEPARATE numbering for SLA verification only. Add prefix "SLA-L" to avoid confusion. |
| **4-Tier Roles** | Guest → Member → Power User → Admin | Doc 08 | Platform-level roles (see Role-Mapping doc). |
| **5-Layer Verification** | Syntax → Logic → Evidence → Consensus → Governance | Doc 11 | Verification pipeline layers. |

---

## 4. User-Facing Feature Names

| Canonical Term | Also Known As | Source Docs | Resolution |
|---------------|--------------|-------------|------------|
| **WorkChat** | Chat Studio, LibreChat | Doc 25, 35 | Use **WorkChat** everywhere. Note: Refers strictly to the AI chat interface. |
| **News** | Topics, Updates | Doc 35 §9 | Use **News** in navigation. |
| **Community** | Feed, Social Feed | Doc 29, 35 | Use **Community** for social updates, profiles, and friend group chats. |
| **Manual** | Docs, Documentation | Doc 07, 35 | Use **Manual** for platform guides. |
| **Install** | Home, Landing | Doc 35 | Use **Install** for the platform's entry or landing page. |
| **Topic** | Channel | Doc 31, 35 | Use **Topic** to refer to specific chat rooms inside a Project. |

---

## 5. Technology Names

| Canonical Term | What It Does | Source Docs |
|---------------|-------------|-------------|
| **Rocket.Chat** | Chat infrastructure (DM, channels, bots) | Doc 28, 30 |
| **LiveKit** | Real-time video/voice/screen sharing | Doc 28, 32 |
| **Hocuspocus** | Yjs CRDT server for collaborative editing | Doc 28, 31 |
| **Tiptap** | Rich text editor (built on ProseMirror + Yjs) | Doc 28, 31 |
| **LibreChat** | AI model gateway (multi-provider) | Doc 25, 28 |
| **OpenRouter** | LLM API aggregator | Doc 06, 25 |

---

## 6. Writing Rules

1. **First mention:** Always use full canonical term, optionally with abbreviation: "Axiomatic Energy Units (Credits)"
2. **Subsequent mentions:** Use abbreviation or short form: "Credits"
3. **Never mix terms:** Don't say "AEU" in one paragraph and "Credits" in the next within the same doc
4. **Link to this glossary:** When introducing a term that has known aliases, add: `(see [[GLOSSARY]])`

---

*Last updated: 2026-03-20 | Canonical for: all platform_specs documents*
