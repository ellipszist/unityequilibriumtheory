# UET v5.0 — Social Feed & Profiles Spec v1

## 1. Vision
An academic social feed where researchers share findings, discuss theories, and build reputation through verified contributions — not engagement farming.

---

## 2. Core Concepts

### 2.1 Knowledge Feed (not `Timeline'')
- Posts are academic in nature: research summaries, equation derivations, experimental results
- Content supports rich text (Markdown), LaTeX equations, images, and code blocks
- `Verified Insights'' badge for posts backed by PoUW verification
- Feed sorted by: relevance (default), recency, or trending

### 2.2 Academic Reputation
- Users gain reputation through verified contributions, not likes
- Reputation score visible on profile (maps to User.reputation in Prisma)
- High-reputation users get priority in feed ranking

---

## 3. Data Model (Prisma Extensions)

### 3.1 Existing Models (already in schema)
- `Post` (id, authorId, title, content, upvotes, tags, comments)
- `Comment` (id, postId, authorId, content, upvotes)
- `Tag` (id, name, posts)

### 3.2 New Models Required

`prisma
model Follow {
  id          String   @id @default(uuid())
  followerId  String
  followingId String
  createdAt   DateTime @default(now())
  follower    User     @relation(""Followers"", fields: [followerId], references: [id])
  following   User     @relation(""Following"", fields: [followingId], references: [id])
  @@unique([followerId, followingId])
  @@index([followingId])
}

model Media {
  id        String   @id @default(uuid())
  postId    String?
  userId    String
  url       String
  type      MediaType // IMAGE | VIDEO | DOCUMENT
  filename  String
  size      Int
  createdAt DateTime @default(now())
  post      Post?    @relation(fields: [postId], references: [id])
  user      User     @relation(fields: [userId], references: [id])
}

enum MediaType {
  IMAGE
  VIDEO
  DOCUMENT
}
`

### 3.3 User Model Extensions
Add to existing User model:
`prisma
model User {
  // ... existing fields
  displayName String?
  bio         String?  @db.Text
  avatarUrl   String?
  institution String?  // University/Lab affiliation
  website     String?
  followers   Follow[] @relation(""Following"")
  following   Follow[] @relation(""Followers"")
  media       Media[]
}
`

---

## 4. Pages & Routes

| Route | Page | Description |
|-------|------|-------------|
| `/feed` | Feed | Main social feed with infinite scroll |
| `/feed/new` | Create Post | Rich text editor (TiptapEditor) |
| `/profile/[userId]` | User Profile | Bio, posts, followers, activity |
| `/profile/edit` | Edit Profile | Update bio, avatar, institution |
| `/search` | Search | Search posts and users |

---

## 5. API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/feed` | Get feed (paginated, filtered) |
| GET | `/api/feed?tag=quantum` | Filter by tag |
| GET | `/api/feed?following=true` | Following-only feed |
| POST | `/api/posts` | Create post (existing) |
| PUT | `/api/posts/[id]` | Update post |
| DELETE | `/api/posts/[id]` | Delete post |
| POST | `/api/posts/[id]/upvote` | Upvote/downvote |
| GET | `/api/posts/[id]/comments` | Get comments |
| POST | `/api/posts/[id]/comments` | Add comment |
| GET | `/api/profile/[userId]` | Get user profile |
| PUT | `/api/profile` | Update own profile |
| POST | `/api/follow/[userId]` | Follow user |
| DELETE | `/api/follow/[userId]` | Unfollow user |
| POST | `/api/upload` | Upload media (returns URL) |

---

## 6. Feed Algorithm

### 6.1 Default Sort (Relevance)
`
score = upvotes * 1.0
      + comment_count * 0.5
      + author_reputation * 0.3
      + recency_decay(hours_old)
      + (is_verified ? 2.0 : 0.0)
      + (is_following_author ? 1.0 : 0.0)
`

### 6.2 Feed Modes
- **For You**: Relevance-sorted, personalized by follows + tags
- **Latest**: Chronological
- **Trending**: Highest engagement in last 24h
- **Following**: Only posts from followed users

---

## 7. Media Storage

### 7.1 Cloudflare R2 (Recommended)
- S3-compatible API
- Free egress (no bandwidth charges)
- `@aws-sdk/client-s3` for uploads
- Presigned URLs for direct browser upload

### 7.2 Upload Flow
1. Client requests presigned URL from `/api/upload`
2. Client uploads directly to R2
3. Server stores Media record in Prisma
4. Post references Media IDs

---

## 8. UI Components

### 8.1 FeedCard
- Author avatar + name + institution + timestamp
- Post title + content preview (truncated)
- Tag pills
- Upvote/downvote buttons + comment count
- Verified badge if applicable

### 8.2 PostComposer
- TiptapEditor (already exists) with extensions:
  - `@tiptap/extension-mathematics` for LaTeX
  - `@tiptap/extension-code-block-lowlight` for code
  - `@tiptap/extension-image` for inline images
- Tag selector (autocomplete from existing tags)
- Media upload dropzone

### 8.3 UserProfileCard
- Avatar, display name, institution
- Bio (truncated)
- Follower/following counts
- Follow/unfollow button
- Recent posts

---

## 9. Implementation Priority
1. User profile model extension + edit page
2. Feed page with infinite scroll (using existing Post model)
3. Upvote/downvote functionality
4. Comment system
5. Follow system + following-only feed
6. Media upload (R2)
7. Search
8. Feed algorithm optimization