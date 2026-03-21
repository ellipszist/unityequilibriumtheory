# 🌍 39. Event Bus & Multi-Cloud Infrastructure (v1.0)

> **Related:** [[37__ENTERPRISE_AND_WEB3_INFRA_v1]], [[03__AGENT_ENGINE_v5.0_SPEC]]

This document finalizes the two missing pillars of the UET Infrastructure: reviving the deterministic `"Event Bus v3.0"` from legacy architectures, and defining a **Multi-Cloud Database Strategy** (AWS + Alternatives) heavily requested for enterprise risk management.

---

## 🚌 1. The Revived UET Event Bus (Powered by Kafka)

The legacy `EVENT_BUS_SYSTEM_v3.0` was a masterpiece of internal logic, designed to prevent race conditions across AI Agents. We are reviving this exact logic, but instead of custom in-memory queues, we will power it using **Apache Kafka** (or Redpanda) as the distributed backbone.

### The 4 Delivery Guarantees (From Legacy Docs)
1. **Idempotency:** Agents won't break if they receive the same event twice.
2. **Atomic Delivery:** An event reaches all target Agents or none.
3. **Strict Ordering:** `KB_VERSION_v1` *must* arrive before `KB_VERSION_v2`.
4. **Deterministic Reactions:** Every Agent responds the exact same way to a `SYSTEM_LOCKDOWN` event.

### The Topic Mapping (Kafka Topics)
The legacy queues map directly to modern Kafka Topics. ClickHouse will subscribe to *all* of these to write the Universal History Log.
- `uet.system.*` (System Health, Errors, Shutdowns, Overloads)
- `uet.flow.*` (Task Created, Started, Completed, Retry)
- `uet.agent.*` (Block Start, Action Call, Reasoning Step)
- `uet.rag.*` (Retrieve Start, Graph Expand, Rerank)
- `uet.ks.*` (Knowledge Sync, Node Update, Canonical Merge)

By utilizing Kafka, the event bus becomes fully async, distributed-ready, and capable of handling millions of global events per second.

---

## ⛅ 2. Multi-Cloud & High Availability Database Strategy

Relying on a single cloud provider is a critical risk vector. UET will employ a **hybrid multi-cloud strategy** to guarantee stability across geopolitical boundaries and provider outages.

### Primary Provider: AWS (Amazon Web Services)
AWS will serve as the heavy-lifting backbone due to its robust ecosystem:
- **Compute:** ECS/EKS for running the Rust `uet_core` Agent Swarms.
- **Storage:** Amazon S3 for storing PDFs, raw research files, and user avatars (serving as the primary cache before files are decentralized to IPFS).
- **Key Management:** AWS KMS (Key Management Service) acting as the cyber-vault for all encrypted Wallet Private Keys and internal system passwords.

### Secondary Providers (Risk Management & Specific Capabilities)
To avoid vendor lock-in, data will be replicated to specialized secondary providers:
- **ClickHouse Cloud / GCP:** The massive continuous Event Sourcing logs (The Universal History) will be housed in managed ClickHouse. Google Cloud (GCP) offers extremely cheap egress for heavy analytical workloads if separated from AWS.
- **VectorDB Ecosystem:** Pinecone, Qdrant Cloud, or Milvus will be used agnostically for RAG, maintaining isolated tenant vector spaces outside of the main AWS RDS environment.

### The 3-Tier Web3 Failover
1. **Tier 1 (Fast, Centralized):** AWS Redis (Working Memory) & AWS Aurora Postgres (Immediate Ledger).
2. **Tier 2 (Analytical, Sourcing):** ClickHouse (Episodic Memory / Event Sourcing logs).
3. **Tier 3 (Immutable, Decentralized):** Polkadot/Substrate Blockchain & IPFS. At the end of every temporal epoch, cryptographic proofs of the ClickHouse logs and S3 files are hashed and committed permanently to the Web3 networks. 

---

## 🔌 3. Frontend to Backend Network Pipes

To support the massive real-time event flow to Open-Source frontends (LobeChat, Rocket.Chat):
1. **Real-time Protocol:** **gRPC** and **WebSockets** will connect the Rust backend to the UI. HTTP is too slow for Agent reasoning streams.
2. **Global CDN:** **Cloudflare** will sit in front of the AWS API Gateway, caching static files (Docusaurus Manuals), routing WebSockets cleanly, and absorbing massive DDoS attacks against the UET platform.
3. **API Gateway:** Limits requests (Rate Limiting) mathematically according to the user's available Energy Units ($\Omega$).
