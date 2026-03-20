# UET Platform — UX/UI Design Standard v1.0

> **Scope:** All pages and components under `uet_web/src/`. Every new page or component MUST comply with this standard before merge.

---

## 1. Core Philosophy

| Principle | Rule |
|-----------|------|
| **Clarity** | One primary action per view. Remove visual noise. |
| **Performance** | No layout shift on load. Prefer CSS over JS animations. Lazy-load heavy panels. |
| **Consistency** | Every page uses `AppShell`. No custom navbars. No duplicate nav patterns. |
| **Accessibility** | All interactive elements keyboard-navigable. Min contrast ratio 4.5:1. |
| **Responsiveness** | Mobile-first. 1 panel → 2 panel → 3 panel as viewport grows. |

---

## 2. Layout System

### 2.1 Universal Shell — `AppShell`

**Every authenticated page wraps content in `<AppShell>`.**

```tsx
// ✅ Correct
export default function MyPage() {
  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">...</div>
    </AppShell>
  );
}

// ❌ Wrong — custom navbar
export default function MyPage() {
  return (
    <div>
      <header>...</header>  {/* NEVER do this */}
      ...
    </div>
  );
}
```

`AppShell` provides:
- Fixed top navbar (h-14) with logo, nav links, MenuPopover, Search, Messenger, Notifications, Profile
- Mobile bottom tab bar
- `flex flex-col h-screen` root so children fill remaining height

### 2.2 Three Panel Layout — `ThreePanelLayout`

Used for: **Feed**, **Profile**, **Post detail**, **Search**

```
┌──────────┬──────────────────┬──────────┐
│  Left    │     Center       │  Right   │
│ Profile/ │   Main content   │  Chat/   │
│ Context  │   (scrollable)   │  Info    │
│ 260px    │   flex-1         │  280px   │
└──────────┴──────────────────┴──────────┘
```

- Left/Right panels: collapsible, resizable via drag handle
- Center: always visible, `overflow-y-auto`
- Mobile: only center shown, tab bar switches panels

### 2.3 Sidebar Layout — `SidebarLayout`

Used for: **Messages**, **Workspaces**, **Docs**

```
┌────────┬──────────────────────────────┐
│ Side   │        Main Content          │
│ 240px  │        (flex-1)              │
│        │                             │
└────────┴──────────────────────────────┘
```

- Sidebar: collapsible on mobile (overlay), fixed on desktop
- Content: `overflow-y-auto`, `flex-1`

### 2.4 Three-Panel Vertical (Studio) — Custom Flex Row

Used for: **Workchat**

```
┌──────────┬──────────────────┬──────────┐
│  Source  │      Chat        │  Output  │
│  240px   │    flex-1        │  320px   │
│ shrink-0 │   min-w-0        │ shrink-0 │
└──────────┴──────────────────┴──────────┘
```

### 2.5 Bento Grid — `BentoGridLayout`

Used for: **Landing page features**, **News/Topics grid**, **Dashboard cards**

```
┌───────┬───────┬───────────────┐
│ Card  │ Card  │  Wide Card    │
│  1x1  │  1x1  │     2x1       │
├───────┴───────┼───────────────┤
│  Tall Card    │ Card  │ Card  │
│     1x2       │  1x1  │  1x1  │
└───────────────┴───────┴───────┘
```

---

## 3. Navigation Standard

### 3.1 Top Navbar (inside AppShell)

```
[Logo] [Feed] [Projects] [Workchat] [News]    [☰Menu] [🔍] [💬] [🔔] [👤]
```

- **Left:** Logo + brand name (hidden on mobile)
- **Center:** Primary nav links (max 4-5 items). Icons + label.
- **Right:** MenuPopover → Search → Messenger → Notifications → Profile

### 3.2 Nav Links (canonical list)

| Label | Route | Icon |
|-------|-------|------|
| Feed | `/feed` | Home |
| Projects | `/workspaces` | FolderKanban |
| Workchat | `/chat` | Sparkles |
| News | `/news` | Newspaper |

**Removed from nav:** Docs, Topics (both live inside MenuPopover)

### 3.3 MenuPopover Sections

| Section | Items |
|---------|-------|
| Platform | News, Projects, Community, Messages |
| Tools | Workchat, Search, Notifications, Credits |
| More from UET | Documentation, GitHub, Developer API |

### 3.4 Mobile Bottom Tab Bar

Same 4 nav links, icon only, no label truncation.

---

## 4. Visual Design Tokens

### 4.1 Color System (CSS vars via Tailwind)

```
Background:     bg-background      (#fff / #0a0a0f dark)
Card surface:   bg-card            (white / #111 dark)
Muted surface:  bg-muted           (#f4f4f5 / #1a1a1a dark)
Border:         border-border      (#e4e4e7 / #27272a dark)
Primary:        text-primary       (#0d7a5f)
Muted text:     text-muted-foreground
```

### 4.2 Glassmorphism (use sparingly — hero sections, modals, popovers)

```css
/* Standard glass panel */
backdrop-blur-md
bg-white/80 dark:bg-black/80
border border-white/20 dark:border-white/10
shadow-2xl
```

```css
/* Subtle glass card */
bg-card/60 backdrop-blur-sm
border border-border
```

### 4.3 Typography Scale

| Use | Class |
|-----|-------|
| Page title | `text-2xl font-bold` |
| Section header | `text-lg font-semibold` |
| Card title | `text-sm font-semibold` |
| Body | `text-sm` |
| Caption / meta | `text-xs text-muted-foreground` |
| Mono (code, IDs) | `font-mono text-xs` |

### 4.4 Spacing Rhythm

- Panel padding: `p-4` or `px-4 py-6`
- Card padding: `p-4` (compact) or `p-5` (normal)
- Gap between cards: `gap-3` or `gap-4`
- Section gap: `space-y-6` or `space-y-8`

---

## 5. Component Patterns

### 5.1 Cards

```tsx
// Standard card
<div className="rounded-xl border border-border bg-card p-4 hover:border-primary/40 transition-colors">

// Glass card (hero/featured)
<div className="rounded-2xl border border-white/10 bg-card/60 backdrop-blur-sm p-5 shadow-lg">

// Bento card (grid)
<div className="rounded-2xl border border-border bg-card p-4 col-span-2 row-span-1">
```

### 5.2 Buttons

```tsx
// Primary CTA
<button className="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-sm font-semibold hover:bg-primary/90 transition-colors">

// Secondary / ghost
<button className="px-4 py-2 rounded-xl bg-muted text-foreground text-sm font-medium hover:bg-muted/80 transition-colors">

// Icon button (navbar)
<button className="w-9 h-9 rounded-full bg-muted/50 hover:bg-muted flex items-center justify-center transition-colors">
```

### 5.3 Popovers

All popovers:
- `rounded-2xl border border-border bg-card shadow-2xl z-50`
- `right-0` alignment when triggered from right-side navbar icons
- `max-h-[480px] overflow-y-auto` for scrollable content
- Close on outside click via `mousedown` listener on `document`
- Close on ESC key

### 5.4 Modals

All modals:
- Backdrop: `fixed inset-0 bg-black/60 backdrop-blur-sm z-[100]`
- Panel: `relative w-full max-w-lg bg-card rounded-2xl shadow-2xl`
- Header: centered title + close button top-right
- Lock body scroll: `document.body.style.overflow = 'hidden'` on open
- Restore on close/unmount

### 5.5 Form Inputs

```tsx
// Standard input
<input className="w-full px-3 py-2 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/60 focus:ring-1 focus:ring-primary/20 placeholder:text-muted-foreground transition-colors">

// Search input
<input className="w-full pl-9 pr-3 py-2 rounded-full bg-muted/50 text-xs outline-none focus:bg-muted placeholder:text-muted-foreground">
```

---

## 6. Page-by-Page Layout Map

| Route | Layout | Left Panel | Center | Right Panel |
|-------|--------|-----------|--------|-------------|
| `/` | Custom landing | — | Hero + Features | — |
| `/feed` | ThreePanelLayout | ProfilePanel | FeedCards | ChatFriendsPanel |
| `/post/[id]` | ThreePanelLayout | AuthorCard | PostDetail + Comments | RelatedPosts |
| `/profile/[userId]` | ThreePanelLayout | ProfileCard | Posts/Activity | Stats |
| `/search` | SidebarLayout | Filters | Results | — |
| `/messages` | SidebarLayout | Channels | EmbeddedChat | — |
| `/workspaces` | AppShell + grid | — | WorkspaceCards | — |
| `/workspaces/[id]` | SidebarLayout | Tabs (Docs/Tasks/Members) | Content | — |
| `/chat` | ThreePanelLayout (Studio) | SourcePanel | ChatPanel | OutputPanel |
| `/news` | AppShell + stack | — | News/Topics accordion | — |
| `/docs` | SidebarLayout | DocTree | DocContent | — |
| `/account` | AppShell | — | AccountForm | — |

---

## 7. Performance Rules

- **No layout shift:** Always define explicit dimensions for images (`width`/`height` or aspect ratio container)
- **Panel overflow:** Each panel must have `overflow-hidden` or `overflow-y-auto` — never let content bleed
- **Suspense:** Wrap async data fetches in `<Suspense fallback={<Skeleton />}>`
- **Animation:** Prefer `transition-colors`, `transition-opacity`, `transition-transform` (GPU-composited). Avoid JS-driven animations for layout
- **Font:** System font stack only — no Google Fonts HTTP calls
- **Bundle:** No barrel imports from `lucide-react` — import icons individually

---

## 8. Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Page component | PascalCase + "Page" suffix | `FeedPage`, `ChatPage` |
| Layout component | PascalCase + "Layout"/"Shell" | `AppShell`, `ThreePanelLayout` |
| UI component | PascalCase | `FeedCard`, `CreatePostModal` |
| Popover | PascalCase + "Popover" | `MenuPopover`, `ProfilePopover` |
| Panel | PascalCase + "Panel" | `SourcePanel`, `ProfilePanel` |
| API route | kebab-case folder | `/api/posts/[id]/comments` |

---

## 9. Route & Name Registry (Canonical)

| Display name | Route | Notes |
|-------------|-------|-------|
| Feed | `/feed` | Social research feed |
| Projects | `/workspaces` | Collaborative workspaces |
| **Workchat** | `/chat` | AI assistant — ONE name only |
| **News** | `/news` | Research topics & updates (was "Topics") |
| Messages | `/messages` | Rocket.Chat embedded |
| Docs | `/docs` | Documentation |
| Search | `/search` | Global search |
| Profile | `/profile/[userId]` | User profile |
| Account | `/account` | Settings / billing |

> ⚠️ **Rule:** A page has exactly ONE name. Do not mix "Workchat Studio", "Chat", "AI Chat" — pick the canonical name and use it everywhere (navbar, page title, MenuPopover, document title).

---

## 10. Checklist Before Merging a New Page

- [ ] Wraps in `<AppShell>` (no custom navbar)
- [ ] Uses one of the 4 layout patterns (ThreePanel / Sidebar / Studio / Grid)
- [ ] All panels have `overflow-hidden` / `overflow-y-auto`
- [ ] Mobile: layout collapses gracefully (no horizontal scroll)
- [ ] Page title matches canonical name from Route Registry (§9)
- [ ] No hardcoded colors — uses Tailwind design tokens
- [ ] No `console.log` left in production code
- [ ] TypeScript — no `any` unless strictly necessary with comment

---

*Last updated: 2026-03-20 | Author: Cascade AI | Version: 1.0*
