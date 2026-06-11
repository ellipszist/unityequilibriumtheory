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

## Entry template

### [YYYY-MM-DD] - [Short title]

- Scope: `[topic or file set]`
- Added or changed: `[artifact, manifest, script, doc, or gate]`
- Files touched: `[key files only]`
- Verified with: `[command]`
- Result: `[PASS/WARN/FAIL or other concrete outcome]`
- Blocker narrowed: `[what became clearer]`
- Still open: `[next required artifact or unresolved blocker]`
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
- Claim impact: `[status]`
- Notes: `[optional detail]`
