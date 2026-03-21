Phase# UET v5.0 — Open-Source Stack Selection v1

> **Related:** [[25__WORKCHAT_AND_LIBRECHAT_BOUNDARY_v1]] · [[29__SOCIAL_FEED_AND_PROFILES_SPEC_v1]] · [[30__REALTIME_CHAT_AND_MESSAGING_SPEC_v1]] · [[31__WORKSPACE_AND_COLLABORATION_SPEC_v1]] · [[32__VIDEO_AND_VOICE_SPEC_v1]] · [[33__CREDIT_AND_SUBSCRIPTION_SPEC_v1]] · [[34__INTEGRATION_ARCHITECTURE_v1]]

## 1. Purpose
This document evaluates and selects open-source projects for each major platform feature area, providing a unified technology stack that minimizes custom development while maximizing feature completeness.

## 2. Selection Criteria
- **License**: Must be MIT, Apache 2.0, or similarly permissive (AGPL only if isolated)
- **Maturity**: Prefer projects with 3+ years of active development
- **Self-hostable**: Must support on-premise deployment
- **API-first**: Must expose REST or WebSocket APIs for integration
- **Active community**: Regular releases, responsive maintainers
- **TypeScript/Rust affinity**: Prefer stacks that align with our existing codebase

---

## 3. Evaluation Matrix

### 3.1 Real-time Chat & Workspace Platform

| Criteria | Rocket.Chat | Matrix (Element) | Stoat (ex-Revolt) | Mattermost |
|----------|-------------|------------------|--------------------|------------|
| License | MIT (community) | Apache 2.0 | AGPL-3.0 | MIT (community) |
| Language | TypeScript/Node | Python (Synapse) / Rust (Conduit) | Rust + TypeScript | Go + TypeScript |
| Discord-like UX | Partial (channels, DM) | Partial (rooms, spaces) | Very close clone | Slack-like |
| Roles & Permissions | Full RBAC | Room-level ACL | Server roles | Team/channel perms |
| Video/Voice Call | Built-in (Jitsi/LiveKit) | Element Call (beta) | Not yet | Built-in (plugin) |
| File Sharing | Yes | Yes | Basic | Yes |
| Federation | No (enterprise only) | Yes (core feature) | No | No |
| Bot/Integration API | REST + Realtime API | Matrix Client-Server API | REST API | REST + Webhook |
| Mobile Apps | iOS + Android | iOS + Android | Web only (beta) | iOS + Android |
| Docker Deploy | Yes | Yes | Yes | Yes |
| GitHub Stars | 42k+ | 12k+ (Element) | 9k+ | 31k+ |
| Maturity | 10+ years | 7+ years | 3 years (beta) | 8+ years |

**Decision: Rocket.Chat**
- Most mature all-in-one platform with channels, DM, roles, video, bots
- MIT community edition sufficient for our needs
- REST + Realtime API enables deep integration with UET backend
- Channels map directly to Discord-like workspace concept
- Built-in Jitsi/LiveKit integration for video calls

### 3.2 AI Chat Interface

| Criteria | LibreChat | Open WebUI | LobeChat | Custom (current) |
|----------|-----------|------------|----------|-----------------|
| License | MIT | MIT | MIT | N/A |
| Multi-provider | Yes (all major) | Yes | Yes | Single (OpenRouter) |
| MCP Support | Yes | Partial | No | No |
| Agents/Tools | Yes | Yes | Yes | Basic |
| File Upload | Yes | Yes | Yes | No |
| Artifacts | Yes | No | Yes | No |
| Auth System | Yes (OAuth, LDAP) | Yes | Basic | Via Rust API |
| Self-hosted | Docker | Docker | Docker | Custom |
| GitHub Stars | 22k+ | 70k+ | 55k+ | N/A |

**Decision: LibreChat (as parallel shell, Option B from spec 25)**
- MCP support aligns perfectly with UET MCP backend
- Agents + tools match our multi-agent architecture
- Keep UET Workchat for research-specific UX (source panel, physics workflows)
- LibreChat handles general AI chat, multi-model switching, conversation management

### 3.3 Video & Voice Communication

| Criteria | LiveKit | Jitsi Meet | OpenVidu | Daily.co |
|----------|---------|------------|----------|----------|
| License | Apache 2.0 | Apache 2.0 | Apache 2.0 | Proprietary |
| Language | Go (server) | Java + TypeScript | Java + TypeScript | N/A |
| WebRTC SFU | Yes | Yes | Yes | Yes |
| React SDK | Yes (@livekit/react) | Yes (lib-jitsi-meet) | Yes | Yes |
| Screen Share | Yes | Yes | Yes | Yes |
| Recording | Yes (Egress) | Yes (Jibri) | Yes | Yes |
| Self-hosted | Yes | Yes | Yes | Cloud only |
| Scalability | Excellent (distributed) | Good | Good | Excellent |
| Rocket.Chat Integration | Yes (native) | Yes (native) | No | No |
| GitHub Stars | 12k+ | 24k+ | 4k+ | N/A |

**Decision: LiveKit**
- Best performance and scalability (Go SFU)
- Native Rocket.Chat integration available
- Excellent React SDK for custom UI
- Recording via Egress service
- Can also be used standalone for UET-specific video features

### 3.4 Collaborative Document Editing

| Criteria | Tiptap + Yjs | Liveblocks | Plate | Etherpad |
|----------|-------------|------------|-------|----------|
| License | MIT | Proprietary | MIT | Apache 2.0 |
| CRDT Backend | Yjs (Hocuspocus) | Managed | Yjs | OT (custom) |
| Rich Text | Excellent (ProseMirror) | Via Tiptap/Lexical | Good | Basic |
| LaTeX Support | Via extension | Via Tiptap | Possible | No |
| Real-time Collab | Via Hocuspocus server | Built-in | Via Yjs | Built-in |
| Self-hosted | Yes | Cloud only | Yes | Yes |
| Already in codebase | Yes (TiptapEditor.tsx) | No | No | No |

**Decision: Tiptap + Yjs + Hocuspocus**
- TiptapEditor component already exists in codebase
- Yjs CRDT is battle-tested for collaborative editing
- Hocuspocus is the official Tiptap collaboration backend (open-source)
- LaTeX support via @tiptap/extension-mathematics
- Zero migration cost — extend what we have

### 3.5 Social Feed & Content

| Criteria | Custom (Prisma) | Mastodon/ActivityPub | Discourse |
|----------|----------------|---------------------|-----------|
| License | N/A | AGPL | GPL |
| Academic Focus | Can customize | General social | Forum-style |
| Already in codebase | Post, Comment, Tag models exist | No | No |
| Integration Effort | Low (extend Prisma) | High (federation protocol) | Medium |
| LaTeX Support | Via TiptapEditor | Limited | Via plugin |

**Decision: Custom build on existing Prisma schema**
- Post/Comment/Tag models already exist and are wired to API routes
- Add Feed UI components, media upload, follow system
- Use Cloudflare R2 for media storage (S3-compatible, cheap)
- No need for heavy OSS framework for a feed — it's standard CRUD + UI

### 3.6 Credit & Subscription Billing

| Criteria | Stripe + Custom | LemonSqueezy | Paddle |
|----------|----------------|--------------|--------|
| Credit System | Must build | Must build | Must build |
| Subscription | Stripe Billing | Built-in | Built-in |
| One-time Purchase | Stripe Checkout | Built-in | Built-in |
| Tax Handling | Stripe Tax | Built-in | Built-in |
| Already in codebase | CheckoutForm component exists | No | No |

**Decision: Stripe + Custom credit model in Prisma**
- CheckoutForm.tsx already exists
- Prisma schema can easily add CreditBalance + CreditTransaction
- Middleware for AI usage metering
- Reference: Vercel's nextjs-subscription-payments template

### 3.7 Project Management (within Workspaces)

| Criteria | Custom (Prisma) | Huly | Plane |
|----------|----------------|------|-------|
| License | N/A | EPL-2.0 | AGPL |
| Already in codebase | Project + Task models exist | No | No |
| Integration | Native | Separate system | Separate system |
| Kanban | Must build UI | Built-in | Built-in |

**Decision: Custom build on existing Prisma schema**
- Project/Task models already exist
- Add Kanban UI component within workspaces
- Lighter weight than integrating a separate project management tool

---

## 4. Final Stack Summary

| Feature Area | Solution | Type | Integration Level |
|-------------|----------|------|-------------------|
| Chat & Workspace | **Rocket.Chat** | External service (Docker) | API integration + embedded UI |
| AI Chat | **LibreChat** | External service (Docker) | Parallel shell to UET AI backend |
| Video/Voice | **LiveKit** | External service (Docker) | SDK integration + Rocket.Chat native |
| Collab Editing | **Tiptap + Yjs + Hocuspocus** | Library + service | Extend existing TiptapEditor |
| Social Feed | **Custom (Next.js + Prisma)** | Built-in | Extend existing models |
| Credits/Billing | **Stripe + Custom Prisma** | Library + service | Extend existing CheckoutForm |
| Project Management | **Custom (Next.js + Prisma)** | Built-in | Extend existing models |
| Media Storage | **Cloudflare R2** | External service | S3-compatible SDK |

## 5. Docker Compose Addition (Target)

`yaml
services:
  # Existing
  postgres:       # PostgreSQL 15
  uet_api:        # Rust API (port 3001)
  uet_agents:     # Python Agent (port 8001)
  uet_web:        # Next.js (port 3005)
  
  # New services
  rocketchat:     # Rocket.Chat (port 3200)
  mongo:          # MongoDB for Rocket.Chat
  librechat:      # LibreChat (port 3080)
  livekit:        # LiveKit SFU (port 7880)
  hocuspocus:     # Yjs collab backend (port 1234)
`

## 6. Phased Adoption

| Phase | Services to Add | Effort |
|-------|----------------|--------|
| Phase 0 | None (fix existing) | 1-2 days |
| Phase 1 | None (custom feed on Prisma) | 1-2 weeks |
| Phase 2 | Rocket.Chat + MongoDB | 1-2 weeks |
| Phase 3 | Hocuspocus | 1 week |
| Phase 4 | LiveKit | 1 week |
| Phase 5 | Stripe (no new service) | 1 week |
| Optional | LibreChat | 1-2 days |