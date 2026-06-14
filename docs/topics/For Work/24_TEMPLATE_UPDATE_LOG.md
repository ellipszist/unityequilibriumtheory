# UPDATE LOG: [Topic Name or Workstream]

> **Scope:** `[Topic path or standards workspace area]`
> **Owner:** `[Human, team, or AI collaborator]`
> **Purpose:** `[Why this log exists]`

## When to use

Use this log when a topic or standards area is being updated across multiple
passes and a reader needs a clean history of what changed, what was verified,
and what remains blocked.

## Log rules

- Log real work, not intentions alone.
- Record verifier or audit commands when they were actually run.
- Name blockers in the same language used by manifests or artifacts.
- Keep entries short and audit-friendly.
- Do not let this log replace canonical status in artifacts, manifests, or
  README files.
- One entry should usually correspond to one coherent hardening wave.
- The latest completed entry should tell a new reviewer what the next
  controlling blocker is without needing to inspect git history first.

## Recommended use in repeated waves

When a topic is being hardened across many short passes, use this log as the
human reconstruction layer between artifacts and prose.

Recommended pattern:

1. artifact or gate changes first
2. rerun verifier when the evidence-producing state changed
3. sync topic docs to the new blocker boundary
4. write one concise log entry
5. commit the wave as a scoped unit

Do not backfill a long series of vague entries after the fact if the artifact
history can no longer support them clearly.

## Entry template

### [YYYY-MM-DD] - [Short title]

- Scope: `[topic or file set]`
- Added or changed: `[artifact, manifest, script, doc, or gate]`
- Files touched: `[key files only]`
- Verified with: `[command]`
- Result: `[PASS/WARN/FAIL or other concrete outcome]`
- Blocker narrowed: `[what became clearer]`
- Still open: `[next required artifact or unresolved blocker]`
- Next controller: `[what currently controls the topic-level state now]`
- Claim impact: `[no change / wording narrowed / wording upgraded with reason]`
- Notes: `[optional before/after metric, dependency effect, or why no rerun happened]`

## Entries

### [YYYY-MM-DD] - [Initial entry]

- Scope: `[topic or file set]`
- Added or changed: `[item]`
- Files touched: `[key files only]`
- Verified with: `[command or n/a]`
- Result: `[outcome]`
- Blocker narrowed: `[named blocker]`
- Still open: `[next step]`
- Next controller: `[current controlling blocker]`
- Claim impact: `[status]`
- Notes: `[optional detail]`
