# UET v5.0 — Integration Architecture v1

> **Related:** [[28__OPEN_SOURCE_STACK_SELECTION_v1]] · [[30__REALTIME_CHAT_AND_MESSAGING_SPEC_v1]] · [[31__WORKSPACE_AND_COLLABORATION_SPEC_v1]] · [[32__VIDEO_AND_VOICE_SPEC_v1]] · [[33__CREDIT_AND_SUBSCRIPTION_SPEC_v1]] · [[27__PHASED_EXECUTION_PLAN_v1]]

## 1. Purpose
This document defines how all open-source services (Rocket.Chat, LiveKit, Hocuspocus, LibreChat) integrate with the existing UET backend (Rust API, Python Agent, Next.js, PostgreSQL) into a unified platform.

---

## 2. System Architecture Overview

`
                        ┌─────────────────────────────────────────────┐
                        │              REVERSE PROXY (Caddy/Nginx)    │
                        │   uet.app → Next.js                        │
                        │   uet.app/rc/ → Rocket.Chat                │
                        │   uet.app/meet/ → LiveKit                  │
                        │   uet.app/ai/ → LibreChat                  │
                        └──────────┬──────────────────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
    ┌─────┴─────┐           ┌──────┴──────┐          ┌─────┴─────┐
    │  Next.js  │           │ Rocket.Chat │          │ LibreChat │
    │  (3005)   │           │  (3200)     │          │  (3080)   │
    │           │           │             │          │           │
    │ - Feed    │           │ - DM        │          │ - Multi   │
    │ - Profile │           │ - Channels  │          │   model   │
    │ - Pricing │           │ - Files     │          │ - MCP     │
    │ - Account │           │ - Presence  │          │ - Agents  │
    │ - Docs    │           │ - Bots      │          │           │
    │ - Workchat│           │ - Webhooks  │          │           │
    └─────┬─────┘           └──────┬──────┘          └─────┬─────┘
          │                        │                        │
          │    ┌───────────────────┼─────────┐              │
          │    │                   │         │              │
    ┌─────┴────┴──┐    ┌──────────┴──┐  ┌───┴────────┐    │
    │  Rust API   │    │  LiveKit    │  │ Hocuspocus │    │
    │  (3001)     │    │  (7880)     │  │ (1234)     │    │
    │             │    │             │  │            │    │
    │ - Auth/JWT  │    │ - WebRTC   │  │ - Yjs CRDT │    │
    │ - OAuth     │    │ - SFU      │  │ - Collab   │    │
    │ - API keys  │    │ - Screen   │  │ - Persist  │    │
    │ - MCP       │    │ - Record   │  │            │    │
    │ - Proxy     │    │            │  │            │    │
    └─────┬───────┘    └────────────┘  └──────┬─────┘    │
          │                                    │          │
    ┌─────┴───────┐                     ┌──────┴──────────┴──┐
    │ Python Agent│                     │   PostgreSQL       │
    │  (8001)     │                     │   (5433)           │
    │             │                     │                    │
    │ - Semantic  │                     │ - Users, Auth      │
    │ - Executive │                     │ - Posts, Comments   │
    │ - Memory    │                     │ - Workspaces       │
    │ - LLM       │                     │ - Credits, Billing │
    └─────────────┘                     │ - Documents (Yjs)  │
                                        │ - Projects, Tasks  │
          ┌─────────────┐              │                    │
          │  MongoDB    │              └────────────────────┘
          │  (27017)    │
          │             │              ┌────────────────────┐
          │ - RC msgs   │              │  Cloudflare R2     │
          │ - RC files  │              │  (media storage)   │
          │ - RC users  │              │                    │
          └─────────────┘              │ - Avatars          │
                                       │ - Post images      │
                                       │ - Shared files     │
                                       │ - Recordings       │
                                       └────────────────────┘
`

---

## 3. Authentication Flow (Single Sign-On)

### 3.1 Auth Source of Truth: Rust API
The Rust API (uet_api) remains the central auth authority.

### 3.2 SSO Flow
`
User → Next.js Login Page
  → POST /api/auth/login (Rust API)
  → Returns: { access_token (JWT), refresh_token, user }
  → Store in localStorage

Next.js stores JWT → passes to all services:
  - Rust API: Authorization header
  - Python Agent: Authorization header
  - Rocket.Chat: Custom OAuth (JWT validated by Rust API)
  - LiveKit: Token generated server-side using JWT identity
  - Hocuspocus: Token passed in WebSocket connection
  - LibreChat: Custom OAuth or shared JWT
`

### 3.3 Rocket.Chat OAuth Configuration
`
OAuth Provider: Custom UET
  Token URL: http://uet_api:3001/api/auth/oauth/token
  Identity URL: http://uet_api:3001/api/auth/me
  Scope: openid profile email
  Merge Users: true (by email)
`

### 3.4 Service-to-Service Auth
For backend-to-backend calls (e.g., Next.js → Rocket.Chat API):
- Use Rocket.Chat admin token (stored as env var)
- Use LiveKit API key/secret (stored as env var)
- Use Hocuspocus shared secret for auth callback

---

## 4. Data Ownership

| Data Type | Storage | Owner |
|-----------|---------|-------|
| User identity, auth | PostgreSQL (Prisma) | Rust API |
| User profiles, follows | PostgreSQL (Prisma) | Next.js API |
| Posts, comments, tags | PostgreSQL (Prisma) | Next.js API |
| Chat messages, DMs | MongoDB | Rocket.Chat |
| Workspaces (metadata) | PostgreSQL (Prisma) | Next.js API |
| Workspace channels | Rocket.Chat (mapped) | Rocket.Chat |
| Documents (Yjs state) | PostgreSQL (Prisma) | Hocuspocus |
| Projects, tasks | PostgreSQL (Prisma) | Next.js API |
| Credits, billing | PostgreSQL (Prisma) | Next.js API |
| Wallets, transactions | PostgreSQL (Prisma) | Next.js API |
| AI sessions, memory | JSON file / PostgreSQL | Python Agent |
| Knowledge vectors | LanceDB | Python Agent |
| Media files | Cloudflare R2 | Next.js API |
| Video recordings | Cloudflare R2 | LiveKit Egress |
| AI conversations | LibreChat DB | LibreChat |

---

## 5. Docker Compose (Full Target)

`yaml
version: '3.8'

services:
  # ═══════════════ DATABASES ═══════════════
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: uet_platform
      POSTGRES_USER: uet
      POSTGRES_PASSWORD: 
    ports:
      - 5433:5432
    volumes:
      - pg_data:/var/lib/postgresql/data

  mongo:
    image: mongo:6
    volumes:
      - mongo_data:/data/db

  # ═══════════════ CORE SERVICES ═══════════════
  uet_api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - 3001:3001
    environment:
      DATABASE_URL: postgres://uet:@postgres:5432/uet_platform
    depends_on:
      - postgres

  uet_agents:
    build:
      context: .
      dockerfile: Dockerfile.agents
    ports:
      - 8001:8001
    environment:
      OPENROUTER_API_KEY: 

  uet_web:
    build:
      context: ./uet_web
      dockerfile: ../Dockerfile.web
    ports:
      - 3005:3000
    environment:
      DATABASE_URL: postgres://uet:@postgres:5432/uet_platform
      NEXT_PUBLIC_AGENT_URL: http://uet_agents:8001
      NEXT_PUBLIC_ROCKETCHAT_URL: http://localhost:3200
      NEXT_PUBLIC_LIVEKIT_URL: ws://localhost:7880
      STRIPE_SECRET_KEY: 
      NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: 
    depends_on:
      - postgres
      - uet_api
      - uet_agents

  # ═══════════════ COMMUNICATION ═══════════════
  rocketchat:
    image: registry.rocket.chat/rocketchat/rocket.chat:latest
    ports:
      - 3200:3000
    environment:
      MONGO_URL: mongodb://mongo:27017/rocketchat
      ROOT_URL: http://localhost:3200
      PORT: 3000
    depends_on:
      - mongo

  livekit:
    image: livekit/livekit-server:latest
    ports:
      - 7880:7880
      - 7881:7881
    volumes:
      - ./config/livekit.yaml:/etc/livekit.yaml
    command: --config /etc/livekit.yaml

  # ═══════════════ COLLABORATION ═══════════════
  hocuspocus:
    build:
      context: ./services/hocuspocus
    ports:
      - 1234:1234
    environment:
      DATABASE_URL: postgres://uet:@postgres:5432/uet_platform
    depends_on:
      - postgres

  # ═══════════════ AI (OPTIONAL) ═══════════════
  librechat:
    image: ghcr.io/danny-avila/librechat:latest
    ports:
      - 3080:3080
    environment:
      MONGO_URI: mongodb://mongo:27017/librechat
    depends_on:
      - mongo

volumes:
  pg_data:
  mongo_data:
`

---

## 6. API Gateway / Reverse Proxy

### 6.1 Production Routing (Caddy)
`
uet-platform.com {
  handle /api/*     { reverse_proxy uet_api:3001 }
  handle /agent/*   { reverse_proxy uet_agents:8001 }
  handle /rc/*      { reverse_proxy rocketchat:3000 }
  handle /meet/*    { reverse_proxy livekit:7880 }
  handle /collab/*  { reverse_proxy hocuspocus:1234 }
  handle /ai/*      { reverse_proxy librechat:3080 }
  handle             { reverse_proxy uet_web:3000 }
}
`

### 6.2 Development (localhost)
Each service runs on its own port — no reverse proxy needed.

---

## 7. Event Bus (Cross-Service Communication)

### 7.1 Webhook-Based (MVP)
| Event | Source | Target | Action |
|-------|--------|--------|--------|
| New message mentioning @uet-agent | Rocket.Chat | Python Agent | AI responds in channel |
| New workspace created | Next.js | Rocket.Chat | Create RC team |
| Member added to workspace | Next.js | Rocket.Chat | Add user to RC team |
| AI credit depleted | Next.js | Rocket.Chat | Notify user via DM |
| Video call started | LiveKit | Rocket.Chat | Post notification in channel |

### 7.2 Future: Redis Pub/Sub or NATS
If webhook latency becomes an issue, add a message broker:
- Redis Pub/Sub for simple events
- NATS for high-throughput event streaming

---

## 8. Environment Variables

### 8.1 Required (.env)
`ash
# Database
DB_PASSWORD=secure_password
DATABASE_URL=postgres://uet:@localhost:5433/uet_platform

# AI
OPENROUTER_API_KEY=sk-or-v1-...

# Stripe
STRIPE_SECRET_KEY=sk_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_...

# LiveKit
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=devsecret

# Rocket.Chat
ROCKETCHAT_ADMIN_TOKEN=...
ROCKETCHAT_URL=http://localhost:3200

# Cloudflare R2
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=uet-media

# Hocuspocus
HOCUSPOCUS_SECRET=shared_secret
`

---

## 9. Migration Strategy

### Phase 0: Fix Foundation (no new services)
- Fix auth env vars, user profiles, live data

### Phase 1: Social Feed (no new services)
- Extend Prisma schema, build feed UI

### Phase 2: Chat & Messaging (add Rocket.Chat + MongoDB)
- Deploy Rocket.Chat, configure OAuth SSO
- Embed chat in Next.js pages
- Create UET AI bot

### Phase 3: Workspaces (add Hocuspocus)
- Deploy Hocuspocus for collaborative editing
- Build workspace UI with channel sidebar
- Sync workspace membership with Rocket.Chat teams

### Phase 4: Video (add LiveKit)
- Deploy LiveKit server
- Add voice channels to workspaces
- Configure Rocket.Chat LiveKit integration

### Phase 5: Credits (no new services)
- Add Prisma credit models
- Wire Stripe, build billing pages
- Add usage metering middleware

### Optional: LibreChat
- Deploy alongside existing Workchat
- Evaluate as parallel AI chat shell