# Daily Progress Reports

This folder is the standard location for pre-commit and daily progress reporting.

## Purpose

Every work day, write a short but serious report before committing code.
The report should help answer:

- What was changed today
- Why it was changed
- What is already working
- What is still risky or incomplete
- What should happen next

## File Naming Standard

Use one file per day:

- `YYYY-MM-DD.md`

Example:

- `2026-03-20.md`

## Required Sections

Each daily report should contain these sections:

1. `# Daily Progress Report - YYYY-MM-DD`
2. `## Summary`
3. `## Completed Today`
4. `## Current Repository State`
5. `## Risks / Open Issues`
6. `## Recommended Next Actions`
7. `## Pre-Commit Decision`

## Writing Rules

- Be concrete, not vague
- Mention real files, systems, and paths when relevant
- Separate finished work from pending work
- Mention if commit/push has not happened yet
- Mention any local-only files or ignored files that should not be committed
- Mention any structural changes that could affect Git, Docker, docs, APIs, or runtime behavior

## Pre-Commit Rule

Before creating a commit, update the current day's report first.

If there are multiple major work sessions in one day, append a new subsection to the same date file instead of creating many files for the same day.
