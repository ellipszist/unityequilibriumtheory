# UET Work Areas

Use these area ids in `WORK_LEDGER/YYYY/YYYY-MM-DD.md` entries before starting a
substantial section of work.

| Area id | Primary paths | Use for |
| --- | --- | --- |
| `research-core` | `docs/topics/`, `docs/meta/` | Numbered UET research topics, topic status, verifier artifacts, evidence gates |
| `research-standards` | `docs/topics/For Work/`, `AGENTS.md` | Research workflow rules, claim discipline, AI-agent operating standards |
| `documentation-system` | `docs/UET_Documentation_Details/`, `README.md`, `CONTRIBUTING.md` | Project documentation architecture, public explanation, style guidance |
| `theory-history` | `uet_history/1_raw/`, `uet_history/theory/`, `uet_history/equations/` | Theory notes, historical source organization, recovered idea archives |
| `book-writing` | `uet_history/BOOK_WORKFLOW.md`, `uet_history/3_publish/books/` | Long-form book workflow, structure, chapters, source tracking, and publishable narrative drafts |
| `thai-policy` | `thailand_proposals/` | Thailand proposal work, policy framing, public-project concepts, source manifests |
| `services-tools` | `services_and_experiments/` | Local services, experiments, MCP, GraphQL, search, embeddings, automation tools |
| `result-artifacts` | `Result/`, topic `Result/` folders | Small reproducible outputs, reports, figures, verifier outputs |
| `repo-ops` | `.github/`, `.gitignore`, `_config.yml`, root manifests | CI, GitHub Pages, branch hygiene, repo recovery, public-safe publishing rules |
| `raw-private` | local-only raw assets, transcripts, chat exports, audio, PDFs | Source material that needs review or manifest treatment before public commit |

## Classification Rule

If a task touches more than one area, record the primary area first and list the
secondary area in the entry body. If the work contains private or raw material,
mark public safety as `partial`, `private`, or `blocked` even when some markdown
outputs are safe to commit.
