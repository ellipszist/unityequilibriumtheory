# Knowledge API and GraphQL Plan

This document defines the planned interface split for the UET knowledge system.

GraphQL should be added as a structured query and admin layer. It should not
replace the vector store, the embedding worker, the canonical research
documents, or MCP tools.

## Interface split

| Interface | Primary user | Best for | Should not do |
| :-- | :-- | :-- | :-- |
| REST | Web app and simple clients | Auth, quota, health checks, simple search calls | Become the only structured knowledge browser |
| MCP | AI agents | Simple tool calls for retrieval and topic lookup | Expose overly complex admin workflows |
| GraphQL | Web app, installer, admin UI, power users | Structured topic/document/index queries | Become the source of truth for research claims |
| Direct database access | Services only | Storage and internal queries | Be required for normal users or AI agents |

## GraphQL responsibilities

GraphQL should make the knowledge system inspectable:

- which documents are indexed
- which topics have indexed content
- which files are stale
- which ingest jobs ran
- which embedding model and index version are active
- which source file a search result came from
- whether a result is from current, stale, deleted, or historical content

## Initial schema sketch

This is a planning sketch, not a locked implementation contract.

```graphql
type Topic {
  id: ID!
  title: String
  status: String
  readiness: String
  controllingBlocker: String
  documents: [Document!]!
}

type Document {
  id: ID!
  sourcePath: String!
  sourceKind: String!
  topicId: String
  fileHash: String
  status: DocumentStatus!
  indexedAt: String
  chunkCount: Int!
  chunks(limit: Int = 20): [Chunk!]!
}

type Chunk {
  id: ID!
  documentId: ID!
  chunkIndex: Int!
  headingPath: String
  text: String!
  chunkHash: String!
  embeddingModel: String
  embeddingDim: Int
}

type IngestRun {
  id: ID!
  mode: String!
  startedAt: String!
  finishedAt: String
  status: IngestStatus!
  changedFiles: Int!
  embeddedChunks: Int!
  reusedChunks: Int!
  failedFiles: Int!
}

type SearchResult {
  document: Document!
  chunk: Chunk!
  score: Float
  snippet: String!
}

enum DocumentStatus {
  ACTIVE
  STALE
  DELETED
  IGNORED
  FAILED
}

enum IngestStatus {
  RUNNING
  SUCCEEDED
  PARTIAL
  FAILED
}
```

## Initial queries

```graphql
type Query {
  topics(status: String, readiness: String): [Topic!]!
  topic(id: ID!): Topic
  documents(topicId: String, status: DocumentStatus): [Document!]!
  document(path: String!): Document
  staleDocuments: [Document!]!
  ingestRuns(limit: Int = 20): [IngestRun!]!
  searchKnowledgeBase(query: String!, topK: Int = 8, topicId: String): [SearchResult!]!
}
```

## Initial mutations

```graphql
type Mutation {
  enqueueIngest(paths: [String!]!): IngestRun!
  enqueueChangedIngest: IngestRun!
  forceReindex(paths: [String!]!, reason: String!): IngestRun!
  markDocumentIgnored(path: String!, reason: String!): Document!
}
```

Forced reindex operations should require a reason because they can invalidate
large parts of the index.

## Optional subscriptions

Subscriptions are useful later, but they are not required for the first stable
version.

```graphql
type Subscription {
  ingestRunUpdated(id: ID!): IngestRun!
  knowledgeIndexChanged: IngestRun!
}
```

## MCP tool shape

MCP should stay small and practical. Candidate tools:

| Tool | Purpose |
| :-- | :-- |
| `search_knowledge_base` | Semantic search across indexed UET content |
| `search_physics` | Physics/math-focused search when the index supports it |
| `get_document` | Retrieve a source document or selected chunks |
| `list_topics` | List indexed topic identifiers and titles |
| `get_topic_status` | Return status reconstructed from canonical metadata, not from search prose alone |
| `kb_status` | Report index version, model, stale count, and last ingest run |

## Safety rules

- GraphQL search results must include source paths.
- Search snippets must not be treated as claim verification.
- Topic status should come from `docs/meta/`, `docs/topics/README.md`, and local
  topic evidence, not from vector similarity alone.
- Stale documents must be visible to users and AI agents.
- The API should distinguish historical context from current project state.
- The API should expose the embedding model and index version used for a result.

## Implementation order

1. Confirm one canonical database schema for documents, chunks, ingest runs, and
   index versions.
2. Implement or repair incremental ingestion against PostgreSQL + pgvector.
3. Expose minimal REST/MCP status and search endpoints.
4. Add GraphQL read queries for topics, documents, stale documents, and ingest
   runs.
5. Add GraphQL ingest mutations after the ingest queue is stable.
6. Add subscriptions only when a real UI needs live ingest progress.
## Current priority

GraphQL is parked until the personal knowledge-base layer is useful.

The first implementation should focus on local status, changed-file ingest, and
search. GraphQL becomes useful later when a web app, installer, dashboard, or
external admin surface actually needs structured queries.
