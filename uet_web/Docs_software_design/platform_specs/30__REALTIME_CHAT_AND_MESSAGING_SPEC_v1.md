# UET v5.0 — Real-time Chat & Messaging Spec v1

## 1. Vision
Person-to-person and group messaging for academic collaboration, powered by Rocket.Chat as the communication backbone with deep integration into the UET platform.

---

## 2. Why Rocket.Chat

### 2.1 Key Capabilities We Get for Free
- Direct messaging (1-on-1)
- Group channels (public + private)
- File sharing in chat
- Message threading
- User presence (online/offline/away)
- Push notifications (mobile + desktop)
- Message search
- Emoji reactions
- Message pinning and starring
- Admin panel for moderation
- REST API + Realtime API (WebSocket)
- OAuth integration (share auth with UET)
- Video/voice call integration (Jitsi or LiveKit)

### 2.2 What We Don't Need to Build
- WebSocket server infrastructure
- Message persistence and delivery guarantees
- Read receipts
- Typing indicators
- File upload handling within chat
- Moderation tools
- Mobile push notification infrastructure

---

## 3. Deployment Architecture

### 3.1 Docker Services
`yaml
rocketchat:
  image: registry.rocket.chat/rocketchat/rocket.chat:latest
  restart: always
  environment:
    MONGO_URL: mongodb://mongo:27017/rocketchat
    ROOT_URL: http://localhost:3200
    PORT: 3200
    OVERWRITE_SETTING_Show_Setup_Wizard: completed
    # OAuth with UET
    OVERWRITE_SETTING_Accounts_OAuth_Custom_UET_enabled: true
    OVERWRITE_SETTING_Accounts_OAuth_Custom_UET_url: http://uet_api:3001
  ports:
    - 3200:3200
  depends_on:
    - mongo

mongo:
  image: mongo:6
  restart: always
  volumes:
    - mongo_data:/data/db
`

### 3.2 Authentication Integration
Rocket.Chat supports custom OAuth providers. UET Rust API becomes the OAuth server:

1. User logs into UET Platform (Next.js → Rust API)
2. When accessing chat, UET redirects to Rocket.Chat with OAuth token
3. Rocket.Chat validates token against UET API
4. Single sign-on: one login for both UET and chat

**OAuth Flow:**
`
UET Login → Rust API issues JWT → Rocket.Chat OAuth validates JWT → Session created
`

---

## 4. Integration Patterns

### 4.1 Embedded Chat (Recommended for MVP)
Embed Rocket.Chat within UET Next.js pages using iframe or Rocket.Chat's embedded layout:

`	sx
// components/chat/EmbeddedChat.tsx
export function EmbeddedChat({ channel }: { channel: string }) {
  return (
    <iframe
      src={${ROCKETCHAT_URL}/channel/?layout=embedded}
      className="w-full h-full border-0"
    />
  );
}
`

### 4.2 API Integration (For Custom Features)
Use Rocket.Chat REST API for programmatic actions:

| Action | API Endpoint |
|--------|-------------|
| Create channel | POST /api/v1/channels.create |
| Send message | POST /api/v1/chat.sendMessage |
| Get DMs | GET /api/v1/dm.list |
| Create DM | POST /api/v1/dm.create |
| User presence | GET /api/v1/users.getPresence |
| Search messages | GET /api/v1/chat.search |
| Upload file | POST /api/v1/rooms.upload |

### 4.3 Webhook Integration
Rocket.Chat webhooks notify UET of events:
- New message in monitored channel → trigger AI agent response
- User mentions @uet-agent → route to Python agent
- File shared → index in knowledge base

---

## 5. Channel Structure for Academic Platform

### 5.1 Default Channels (Auto-created)
| Channel | Purpose | Access |
|---------|---------|--------|
| #general | Platform-wide announcements | Public, read-only for non-admins |
| #research | General research discussion | Public |
| #help | Platform support | Public |
| #ai-chat | AI agent interaction channel | Public |

### 5.2 Topic Channels (Auto-generated from research_uet/topics)
| Channel | Purpose |
|---------|---------|
| #topic-quantum-mechanics | QM research discussion |
| #topic-astrophysics | Astrophysics research |
| #topic-fluid-dynamics | Fluid dynamics research |
| ... (one per UET topic) | |

### 5.3 Workspace Channels (User-created)
- Created when a user starts a Workspace (spec 31)
- Private by default
- Roles inherited from workspace membership

---

## 6. UET AI Bot Integration

### 6.1 Rocket.Chat Bot User
Create a bot user `uet-agent` that responds in channels:

`
User: @uet-agent What is the kappa parameter in UET?
Bot:  [Queries Python Agent API → Returns response with sources]
`

### 6.2 Bot Architecture
`
Rocket.Chat Webhook → UET Bot Service (Node.js) → Python Agent API (port 8001)
                                                  → Response back to channel
`

### 6.3 Bot Capabilities
- Answer UET research questions (via SemanticEngine)
- Search knowledge base
- Summarize documents
- Run UET calculations
- Post AI-generated research summaries to channels

---

## 7. Notification System

### 7.1 In-Platform Notifications
Rocket.Chat provides built-in notifications for:
- Direct messages
- @mentions
- Channel activity
- File shares

### 7.2 UET-Specific Notifications (Custom)
Add to UET Next.js via Rocket.Chat API polling or WebSocket:
- New follower (from social feed)
- Post upvotes/comments
- Task assignments (from workspaces)
- Credit balance warnings
- AI processing complete

### 7.3 Notification Bell Component
`	sx
// components/NotificationBell.tsx
// Polls Rocket.Chat /api/v1/subscriptions.read
// + UET /api/notifications for platform-specific notifications
`

---

## 8. Data Flow

`
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  UET Next.js │────▶│  Rocket.Chat │────▶│  MongoDB     │
│  (UI shell)  │     │  (port 3200) │     │  (messages)  │
│              │     │              │     │              │
│  /messages   │     │  REST API    │     │              │
│  /channels   │     │  WebSocket   │     │              │
│  embedded    │     │  Webhooks    │     │              │
└──────────────┘     └──────┬───────┘     └──────────────┘
                            │
                     ┌──────┴───────┐
                     │  UET Bot     │
                     │  Service     │
                     │  (webhooks)  │
                     └──────┬───────┘
                            │
                     ┌──────┴───────┐
                     │ Python Agent │
                     │ (port 8001)  │
                     └──────────────┘
`

---

## 9. Pages & Routes

| Route | Description |
|-------|-------------|
| /messages | DM inbox (embedded Rocket.Chat) |
| /messages/[userId] | Direct message with specific user |
| /channels | Browse public channels |
| /channels/[name] | View specific channel |

---

## 10. Implementation Steps

1. Add Rocket.Chat + MongoDB to docker-compose.yml
2. Configure OAuth integration with UET Rust API
3. Create EmbeddedChat component
4. Set up default channels
5. Create UET AI bot user + webhook integration
6. Add /messages and /channels routes to Next.js
7. Add notification bell component
8. Configure topic-based auto-channels