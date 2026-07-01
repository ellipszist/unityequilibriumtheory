"""Personal UET knowledge-base helper.

This is the small local-first layer for day-to-day research work. It does not
replace the larger MCP/Postgres/GraphQL plan. It gives the repo a cheap way to
answer three questions before heavier infrastructure exists:

- what files are currently indexed?
- what changed since the last ingest?
- where does a term appear in the local research corpus?
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = REPO_ROOT / "docs" / "knowledge_base" / "personal_index.sqlite3"
DEFAULT_PATHS = (
    "docs/UET_Documentation_Details",
    "docs/topics/For Work",
    "docs/topics/README.md",
    "docs/meta",
    "docs/core",
)
TEXT_EXTENSIONS = {".md", ".txt", ".py", ".json", ".toml", ".yaml", ".yml"}
SKIP_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "vectors",
    "media",
    "target",
    "dist",
    "build",
}


@dataclass(frozen=True)
class SourceFile:
    path: Path
    rel_path: str
    content: str
    file_hash: str


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    init_db(conn)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS documents (
            source_path TEXT PRIMARY KEY,
            file_hash TEXT NOT NULL,
            status TEXT NOT NULL,
            indexed_at TEXT NOT NULL,
            chunk_count INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chunks (
            source_path TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            heading_path TEXT,
            text TEXT NOT NULL,
            chunk_hash TEXT NOT NULL,
            PRIMARY KEY (source_path, chunk_index)
        );

        CREATE TABLE IF NOT EXISTS ingest_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT NOT NULL,
            scanned_files INTEGER NOT NULL,
            changed_files INTEGER NOT NULL,
            skipped_files INTEGER NOT NULL,
            deleted_files INTEGER NOT NULL,
            chunks_written INTEGER NOT NULL,
            dry_run INTEGER NOT NULL
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
    )
    fts_version = conn.execute(
        "SELECT value FROM schema_meta WHERE key = 'fts_schema_version'"
    ).fetchone()
    if fts_version is None or fts_version["value"] != "2":
        conn.execute("DROP TABLE IF EXISTS chunks_fts")
        try:
            conn.execute(
                """
                CREATE VIRTUAL TABLE chunks_fts
                USING fts5(source_path UNINDEXED, heading_path, text);
                """
            )
        except sqlite3.OperationalError:
            conn.execute(
                """
                CREATE TABLE chunks_fts (
                    source_path TEXT NOT NULL,
                    heading_path TEXT,
                    text TEXT NOT NULL
                );
                """
            )
        conn.execute(
            """
            INSERT INTO schema_meta (key, value)
            VALUES ('fts_schema_version', '2')
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """
        )
    conn.commit()


def normalize_rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & SKIP_PARTS) or path.suffix.lower() not in TEXT_EXTENSIONS


def iter_files(paths: Iterable[str]) -> Iterable[Path]:
    for item in paths:
        root = (REPO_ROOT / item).resolve()
        if root.is_file():
            if not should_skip(root):
                yield root
            continue
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and not should_skip(path):
                yield path


def read_source(path: Path) -> SourceFile | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw:
        return None
    text = raw.decode("utf-8", errors="replace")
    file_hash = hashlib.sha256(raw).hexdigest()
    return SourceFile(path=path, rel_path=normalize_rel(path), content=text, file_hash=file_hash)


def chunk_markdownish(text: str) -> list[tuple[str, str]]:
    chunks: list[tuple[str, str]] = []
    heading_stack: list[str] = []
    current_lines: list[str] = []
    current_heading = ""

    def flush() -> None:
        nonlocal current_lines, current_heading
        body = "\n".join(line.rstrip() for line in current_lines).strip()
        if body:
            chunks.append((current_heading, body))
        current_lines = []

    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            flush()
            level = len(match.group(1))
            title = match.group(2).strip()
            heading_stack[:] = heading_stack[: level - 1]
            heading_stack.append(title)
            current_heading = " > ".join(heading_stack)
        current_lines.append(line)

    flush()
    if not chunks and text.strip():
        chunks.append(("", text.strip()))
    return chunks


def existing_hashes(conn: sqlite3.Connection) -> dict[str, str]:
    rows = conn.execute("SELECT source_path, file_hash FROM documents WHERE status = 'active'").fetchall()
    return {row["source_path"]: row["file_hash"] for row in rows}


def clear_document(conn: sqlite3.Connection, rel_path: str) -> None:
    conn.execute("DELETE FROM chunks WHERE source_path = ?", (rel_path,))
    conn.execute("DELETE FROM chunks_fts WHERE source_path = ?", (rel_path,))


def upsert_source(conn: sqlite3.Connection, source: SourceFile) -> int:
    chunks = chunk_markdownish(source.content)
    clear_document(conn, source.rel_path)
    for index, (heading, text) in enumerate(chunks):
        chunk_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        conn.execute(
            """
            INSERT INTO chunks (source_path, chunk_index, heading_path, text, chunk_hash)
            VALUES (?, ?, ?, ?, ?)
            """,
            (source.rel_path, index, heading, text, chunk_hash),
        )
        conn.execute(
            "INSERT INTO chunks_fts (source_path, heading_path, text) VALUES (?, ?, ?)",
            (source.rel_path, heading, text),
        )
    conn.execute(
        """
        INSERT INTO documents (source_path, file_hash, status, indexed_at, chunk_count)
        VALUES (?, ?, 'active', ?, ?)
        ON CONFLICT(source_path) DO UPDATE SET
            file_hash = excluded.file_hash,
            status = 'active',
            indexed_at = excluded.indexed_at,
            chunk_count = excluded.chunk_count
        """,
        (source.rel_path, source.file_hash, now_iso(), len(chunks)),
    )
    return len(chunks)


def cmd_ingest(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    started_at = now_iso()
    known = existing_hashes(conn)
    seen: set[str] = set()
    scanned = changed = skipped = chunks_written = 0

    mode = "all" if args.all else "changed"
    for path in iter_files(args.paths):
        source = read_source(path)
        if source is None:
            continue
        scanned += 1
        seen.add(source.rel_path)
        unchanged = known.get(source.rel_path) == source.file_hash
        if unchanged and not args.all:
            skipped += 1
            continue
        changed += 1
        if not args.dry_run:
            chunks_written += upsert_source(conn, source)

    deleted_paths = sorted(set(known) - seen)
    if not args.dry_run:
        for rel_path in deleted_paths:
            conn.execute(
                "UPDATE documents SET status = 'deleted', indexed_at = ? WHERE source_path = ?",
                (now_iso(), rel_path),
            )
        conn.execute(
            """
            INSERT INTO ingest_runs (
                mode, started_at, finished_at, scanned_files, changed_files,
                skipped_files, deleted_files, chunks_written, dry_run
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                mode,
                started_at,
                now_iso(),
                scanned,
                changed,
                skipped,
                len(deleted_paths),
                chunks_written,
                int(args.dry_run),
            ),
        )
        conn.commit()

    result = {
        "mode": mode,
        "dry_run": args.dry_run,
        "scanned_files": scanned,
        "changed_files": changed,
        "skipped_files": skipped,
        "deleted_files": len(deleted_paths),
        "chunks_written": chunks_written,
        "db": normalize_rel(args.db) if args.db.is_relative_to(REPO_ROOT) else str(args.db),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    doc_counts = conn.execute(
        "SELECT status, COUNT(*) AS count FROM documents GROUP BY status ORDER BY status"
    ).fetchall()
    chunk_count = conn.execute("SELECT COUNT(*) AS count FROM chunks").fetchone()["count"]
    last_run = conn.execute(
        "SELECT * FROM ingest_runs ORDER BY id DESC LIMIT 1"
    ).fetchone()
    result = {
        "db": normalize_rel(args.db) if args.db.is_relative_to(REPO_ROOT) else str(args.db),
        "documents": {row["status"]: row["count"] for row in doc_counts},
        "chunks": chunk_count,
        "last_ingest_run": dict(last_run) if last_run else None,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    query = args.query.strip()
    try:
        rows = conn.execute(
            """
            SELECT source_path, heading_path, text
            FROM chunks_fts
            WHERE chunks_fts MATCH ?
            LIMIT ?
            """,
            (query, args.limit),
        ).fetchall()
    except sqlite3.OperationalError:
        like = f"%{query}%"
        rows = conn.execute(
            """
            SELECT source_path, heading_path, text
            FROM chunks
            WHERE text LIKE ?
            LIMIT ?
            """,
            (like, args.limit),
        ).fetchall()

    for row in rows:
        snippet = " ".join(row["text"].split())[: args.snippet_chars]
        print(
            json.dumps(
                {
                    "source_path": row["source_path"],
                    "heading_path": row["heading_path"],
                    "snippet": snippet,
                },
                ensure_ascii=False,
            )
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Personal UET knowledge-base helper")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="Index changed local research files")
    ingest.add_argument("--all", action="store_true", help="Reindex all scanned files")
    ingest.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    ingest.add_argument("paths", nargs="*", default=list(DEFAULT_PATHS))
    ingest.set_defaults(func=cmd_ingest)

    status = sub.add_parser("status", help="Show local index status")
    status.set_defaults(func=cmd_status)

    search = sub.add_parser("search", help="Search the local text index")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=8)
    search.add_argument("--snippet-chars", type=int, default=320)
    search.set_defaults(func=cmd_search)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.db = args.db.resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
