# UET v5.0 — Role & Permission Mapping (Cross-Document Reconciliation)

> **Related:** [[08__PLATFORM_GOVERNANCE_v5.0_ROLES]] · [[19__DECENTRALIZED_GOVERNANCE_v5.0]] · [[31__WORKSPACE_AND_COLLABORATION_SPEC_v1]]

This document resolves the three overlapping role systems defined across Docs 08, 19, and 31 into a unified, layered permission model.

---

## 1. The Problem

Three documents define roles independently:

| Document | Scope | Roles Defined |
|----------|-------|--------------|
| **Doc 08** (Platform Governance) | Platform-wide | Guest → Member → Power User → Admin |
| **Doc 19** (Decentralized Governance) | On-chain/DAO | Voter → Delegate → Council → Guardian |
| **Doc 31** (Workspace Collaboration) | Per-workspace | Viewer → Member → Moderator → Owner |

These are NOT conflicting — they operate at **different scopes**. But without this mapping, implementers may confuse which role system applies where.

---

## 2. Unified Role Architecture (3 Layers)

```
┌─────────────────────────────────────────────────┐
│  Layer 1: PLATFORM ROLES (Doc 08)               │
│  Controls: Login, feature access, credit limits  │
│  Assigned by: Platform admin / registration       │
│  Roles: Guest → Member → Power User → Admin      │
├─────────────────────────────────────────────────┤
│  Layer 2: WORKSPACE ROLES (Doc 31)              │
│  Controls: Per-workspace permissions              │
│  Assigned by: Workspace owner                     │
│  Roles: Viewer → Member → Moderator → Owner       │
├─────────────────────────────────────────────────┤
│  Layer 3: GOVERNANCE ROLES (Doc 19)             │
│  Controls: Economic policy voting, proposals      │
│  Assigned by: Token weight + reputation           │
│  Roles: Voter → Delegate → Council → Guardian     │
└─────────────────────────────────────────────────┘
```

**A single user can hold roles at ALL three layers simultaneously.** For example:
- Platform: **Member** (standard access)
- Workspace A: **Owner** (full control)
- Workspace B: **Viewer** (read-only)
- Governance: **Delegate** (can vote on behalf of others)

---

## 3. Permission Matrix (Combined)

### 3.1 Platform-Level (Doc 08)

| Permission | Guest | Member | Power User | Admin |
|-----------|-------|--------|------------|-------|
| View public content | ✅ | ✅ | ✅ | ✅ |
| Create posts/comments | ❌ | ✅ | ✅ | ✅ |
| Use AI Workchat | ❌ | ✅ (limited credits) | ✅ (extended credits) | ✅ (unlimited) |
| Create workspaces | ❌ | ✅ (max 3) | ✅ (max 10) | ✅ (unlimited) |
| Access admin panel | ❌ | ❌ | ❌ | ✅ |
| Manage platform users | ❌ | ❌ | ❌ | ✅ |

### 3.2 Workspace-Level (Doc 31)

| Permission | Viewer | Member | Moderator | Owner |
|-----------|--------|--------|-----------|-------|
| View workspace content | ✅ | ✅ | ✅ | ✅ |
| Post messages/docs | ❌ | ✅ | ✅ | ✅ |
| Edit shared documents | ❌ | ✅ | ✅ | ✅ |
| Manage channels | ❌ | ❌ | ✅ | ✅ |
| Invite/remove members | ❌ | ❌ | ✅ | ✅ |
| Delete workspace | ❌ | ❌ | ❌ | ✅ |
| Transfer ownership | ❌ | ❌ | ❌ | ✅ |

### 3.3 Governance-Level (Doc 19)

| Permission | Voter | Delegate | Council | Guardian |
|-----------|-------|----------|---------|----------|
| Vote on proposals | ✅ | ✅ | ✅ | ✅ |
| Submit proposals | ❌ | ✅ | ✅ | ✅ |
| Vote with delegated power | ❌ | ✅ | ✅ | ✅ |
| Set economic parameters | ❌ | ❌ | ✅ | ✅ |
| Emergency veto | ❌ | ❌ | ❌ | ✅ |
| Audit smart contracts | ❌ | ❌ | ❌ | ✅ |

---

## 4. Implementation Notes

### 4.1 Storage Model
```
users table:
  platform_role: enum(guest, member, power_user, admin)

workspace_members table:
  user_id, workspace_id, workspace_role: enum(viewer, member, moderator, owner)

governance table:
  user_id, governance_role: enum(voter, delegate, council, guardian)
  token_weight: decimal
```

### 4.2 Permission Check Order
1. Check **platform role** first (blocks Guest from all workspace/governance actions)
2. Check **workspace role** for workspace-scoped actions
3. Check **governance role** for proposal/voting actions

### 4.3 Role Escalation Rules
- Platform: Only Admin can promote to Power User / Admin
- Workspace: Only Owner can promote to Moderator / Owner
- Governance: Token-weighted — automatic based on contribution

---

*Last updated: 2026-03-20 | Canonical for: reconciling Docs 08, 19, 31*
