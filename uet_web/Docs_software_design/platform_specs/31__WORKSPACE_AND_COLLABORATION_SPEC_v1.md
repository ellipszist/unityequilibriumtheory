# UET v5.0 — Workspace & Collaboration Spec v1

## 1. Vision
Discord-like workspaces for research teams — channels, roles, shared documents, task boards, and AI assistants — built on Rocket.Chat channels + Tiptap collaborative editing.

---

## 2. Workspace Concept

### 2.1 What is a Workspace?
A Workspace is a dedicated collaboration space for a research team, lab, or project. It maps to a **Rocket.Chat Team** (or channel group) with additional UET-specific features.

### 2.2 Workspace Components
| Component | Implementation | Description |
|-----------|---------------|-------------|
| Text Channels | Rocket.Chat channels | Real-time chat per topic/department |
| Voice Channels | LiveKit rooms | Voice/video communication |
| Shared Documents | Tiptap + Yjs (Hocuspocus) | Google Docs-like collaborative editing |
| Task Board | Custom Prisma (Project/Task) | Kanban board for project management |
| File Storage | Cloudflare R2 | Shared files and research data |
| AI Assistant | Python Agent bot | Per-workspace AI with workspace context |
| Member Management | Rocket.Chat roles + Prisma | Invite, roles, permissions |

---

## 3. Data Model

### 3.1 Prisma Models (UET-side)

`prisma
model Workspace {
  id            String   @id @default(uuid())
  name          String
  description   String?  @db.Text
  avatarUrl     String?
  ownerId       String
  rocketChatId  String?  @unique  // Rocket.Chat team/channel group ID
  isPublic      Boolean  @default(false)
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt

  owner         User              @relation(""WorkspaceOwner"", fields: [ownerId], references: [id])
  members       WorkspaceMember[]
  documents     Document[]
  projects      Project[]         // Existing model, now linked to workspace
}

model WorkspaceMember {
  id          String        @id @default(uuid())
  workspaceId String
  userId      String
  role        WorkspaceRole @default(MEMBER)
  joinedAt    DateTime      @default(now())

  workspace   Workspace @relation(fields: [workspaceId], references: [id], onDelete: Cascade)
  user        User      @relation(fields: [userId], references: [id])
  @@unique([workspaceId, userId])
}

enum WorkspaceRole {
  OWNER
  ADMIN
  MEMBER
  GUEST
}

model Document {
  id          String   @id @default(uuid())
  workspaceId String
  title       String
  yjsDocId    String   @unique  // Yjs document ID for Hocuspocus
  createdById String
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  workspace   Workspace @relation(fields: [workspaceId], references: [id], onDelete: Cascade)
  createdBy   User      @relation(fields: [createdById], references: [id])
}
`

### 3.2 Existing Models to Link
`prisma
model Project {
  // Add:
  workspaceId String?
  workspace   Workspace? @relation(fields: [workspaceId], references: [id])
}
`

---

## 4. Workspace Creation Flow

`
1. User clicks ""Create Workspace""
2. UET creates Workspace record in Prisma
3. UET calls Rocket.Chat API: POST /api/v1/teams.create
4. Rocket.Chat returns team ID → stored as rocketChatId
5. Default channels created: #general, #random, #announcements
6. Hocuspocus document space initialized
7. User redirected to workspace page
`

---

## 5. Channel Types

### 5.1 Text Channels (Rocket.Chat)
- Map 1:1 to Rocket.Chat channels within a team
- Created via Rocket.Chat API
- Embedded in UET UI via iframe or custom component

### 5.2 Voice Channels (LiveKit)
- Created as LiveKit rooms with workspace prefix
- Room name format: `ws-{workspaceId}-voice-{channelName}`
- Persistent rooms that users can join/leave
- See spec 32 for details

### 5.3 Document Channels
- Each document is a Tiptap + Yjs collaborative editor
- Connected to Hocuspocus backend
- Document ID: `ws-{workspaceId}-doc-{documentId}`
- See section 7 for details

---

## 6. Role & Permission System

### 6.1 Role Hierarchy
`
OWNER  → Full control (delete workspace, manage all)
ADMIN  → Manage channels, members, documents
MEMBER → Read/write in channels, edit documents
GUEST  → Read-only in designated channels
`

### 6.2 Permission Matrix

| Action | OWNER | ADMIN | MEMBER | GUEST |
|--------|-------|-------|--------|-------|
| Delete workspace | Yes | No | No | No |
| Invite members | Yes | Yes | No | No |
| Remove members | Yes | Yes | No | No |
| Create channels | Yes | Yes | Yes | No |
| Delete channels | Yes | Yes | No | No |
| Send messages | Yes | Yes | Yes | No |
| Create documents | Yes | Yes | Yes | No |
| Edit documents | Yes | Yes | Yes | No |
| Create tasks | Yes | Yes | Yes | No |
| Assign tasks | Yes | Yes | No | No |
| Manage roles | Yes | Yes | No | No |
| View content | Yes | Yes | Yes | Yes |

### 6.3 Sync with Rocket.Chat Roles
- Workspace roles map to Rocket.Chat team roles
- UET is the source of truth; Rocket.Chat roles are synced via API

---

## 7. Collaborative Documents (Tiptap + Yjs)

### 7.1 Architecture
`
Browser (TiptapEditor + Yjs)
    │
    ▼ WebSocket
Hocuspocus Server (port 1234)
    │
    ▼ Persistence
PostgreSQL (via Hocuspocus extension)
`

### 7.2 Hocuspocus Configuration
`	ypescript
// hocuspocus.config.ts
import { Server } from '@hocuspocus/server'
import { Database } from '@hocuspocus/extension-database'

const server = Server.configure({
  port: 1234,
  extensions: [
    new Database({
      fetch: async ({ documentName }) => {
        // Load from PostgreSQL
        const doc = await prisma.document.findUnique({
          where: { yjsDocId: documentName }
        })
        return doc?.content || null
      },
      store: async ({ documentName, state }) => {
        await prisma.document.update({
          where: { yjsDocId: documentName },
          data: { content: state }
        })
      }
    })
  ],
  async onAuthenticate({ token, documentName }) {
    // Verify user has access to this workspace's document
    const user = await verifyToken(token)
    const doc = await prisma.document.findUnique({
      where: { yjsDocId: documentName },
      include: { workspace: { include: { members: true } } }
    })
    if (!doc.workspace.members.find(m => m.userId === user.id)) {
      throw new Error('Unauthorized')
    }
  }
})
`

### 7.3 TiptapEditor Extensions for Collaboration
`	ypescript
import Collaboration from '@tiptap/extension-collaboration'
import CollaborationCursor from '@tiptap/extension-collaboration-cursor'
import { HocuspocusProvider } from '@hocuspocus/provider'

const provider = new HocuspocusProvider({
  url: 'ws://localhost:1234',
  name: ws--doc-,
  token: userToken,
})

const editor = new Editor({
  extensions: [
    StarterKit,
    Mathematics,  // LaTeX
    Collaboration.configure({ document: provider.document }),
    CollaborationCursor.configure({ provider }),
  ]
})
`

---

## 8. Task Board (Kanban)

### 8.1 Reuse Existing Models
Project and Task models already exist in Prisma. Add workspace linkage:
- `Project.workspaceId` links to workspace
- Task statuses map to Kanban columns: TODO → IN_PROGRESS → IN_REVIEW → DONE
- `Task.bountyAmount` for UET credit rewards

### 8.2 UI Component
- DnD Kanban board (reuse existing SortableList component pattern)
- Each task card shows: title, assignee avatar, bounty amount, priority
- Click to expand: full description, comments, attachments

---

## 9. Pages & Routes

| Route | Description |
|-------|-------------|
| /workspaces | List all workspaces (joined + public) |
| /workspaces/new | Create workspace form |
| /workspaces/[id] | Workspace home (channels sidebar + main area) |
| /workspaces/[id]/channels/[name] | Text channel (embedded Rocket.Chat) |
| /workspaces/[id]/voice/[name] | Voice channel (LiveKit) |
| /workspaces/[id]/docs | Document list |
| /workspaces/[id]/docs/[docId] | Collaborative document editor |
| /workspaces/[id]/tasks | Kanban task board |
| /workspaces/[id]/settings | Workspace settings, members, roles |

---

## 10. Invite System

### 10.1 Invite Link
`
https://uet-platform.com/invite/{inviteCode}
`
- Generates unique code linked to workspace
- Configurable: expiry, max uses, auto-role assignment

### 10.2 Email Invitation
- Send email via existing email service (Rust API)
- Include workspace name, inviter name, join link

---

## 11. Implementation Steps

1. Add Workspace/WorkspaceMember/Document Prisma models
2. Link Project model to Workspace (optional workspaceId)
3. Create workspace CRUD API routes
4. Integrate Rocket.Chat team creation on workspace create
5. Build workspace layout page with channel sidebar
6. Add Hocuspocus to docker-compose
7. Extend TiptapEditor with Collaboration + Cursor extensions
8. Build document list and editor pages
9. Build Kanban task board UI
10. Add invite system (links + email)
11. Sync roles between UET Prisma and Rocket.Chat