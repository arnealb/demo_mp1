# demo_mp1

A multi-agent prototype that reads documents, extracts reference IDs, looks them up in a database, and produces a summary — all orchestrated through Microsoft's Agent Framework with a web-based DevUI.

## Architecture overview

```
                        DevUI (localhost:8080)
                               │
                         User sends query
                               │
                    ┌──────────▼──────────┐
                    │   Orchestrator      │
                    │  (WorkflowAgent)    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐   ┌───────────┐   ┌─────────────┐
        │ FileAgent │   │ Database  │   │ Summarizer  │
        │           │   │ Agent     │   │ Agent       │
        └─────┬─────┘   └─────┬─────┘   └─────────────┘
              │                │
     ┌────────▼────────┐ ┌────▼─────────────┐
     │ Filesystem MCP  │ │  SQLite MCP      │
     │ (stdio server)  │ │  (stdio server)  │
     └────────┬────────┘ └────┬─────────────┘
              │               │
         data/*.txt      db/example.db
```

The three agents run as a sequential chain via `WorkflowBuilder`:

1. **FileAgent** — reads all files in `data/` through the filesystem MCP server and extracts 3-digit reference IDs (e.g. 101, 202, 303).
2. **DatabaseAgent** — takes the extracted IDs and queries `db/example.db` through the SQLite MCP server to fetch matching records.
3. **SummarizerAgent** — receives the database results and produces a final human-readable summary.

## How it works

### Entry point — `run_demo.py`

The script initializes two MCP tool connections (filesystem and SQLite), builds the workflow via `agents/orchestrator.py`, and starts the DevUI web server on port 8080.

### MCP servers

The agents don't access files or the database directly. Instead, they call tools exposed by two MCP (Model Context Protocol) servers that run as stdio subprocesses:

- **`mcp_servers/filesystem_mcp.py`** — sandboxed to the `data/` directory, exposes `list_all_files()` and `read_files(path)`.
- **`mcp_servers/sqlite_mcp.py`** — connects to `db/example.db`, exposes `list_all_entries()` and `list_all_entries_with_id(entry_id)`.

This keeps tool access isolated and standardized across agents.

### Agents

Each agent is an `Agent` instance from the Agent Framework, backed by OpenAI's `gpt-4o-mini` model:

| Agent | Tools | Role |
|---|---|---|
| FileAgent | filesystem MCP | Read documents, extract IDs |
| DatabaseAgent | SQLite MCP | Query database for matching records |
| SummarizerAgent | _(none)_ | Produce the final summary |

### Orchestration

`agents/orchestrator.py` wires the agents into a sequential chain using `WorkflowBuilder.add_chain()` and wraps the result in a `WorkflowAgent`. This `WorkflowAgent` is what gets served to the DevUI.

### Sample data

**Documents** (`data/`):
- `contracts/contract1.txt` — references IDs 101, 303
- `contracts/contract2.txt` — references IDs 202, 505
- `notes.txt` — references IDs 101, 202, 404
- `references/refs.txt` — reference ID list

**Database** (`db/example.db`):

| ID | Name | Details |
|---|---|---|
| 101 | Alice Janssens | Internal employee — finance department |
| 202 | Bob Peeters | Customer ID — active contract |
| 303 | Carol De Smet | Supplier record — needs verification |
| 505 | Delta Team | Project stakeholder — Project Delta initiative |

ID 404 appears in the documents but has no database record, so the agents report it as unmatched.

## Running the demo

```bash
# Make sure you're in the project root with the venv activated
python3 run_demo.py
```

This starts the DevUI at `http://localhost:8080`. Enter a query (e.g. "Read all documents and summarize the matched records") and the agent chain will execute step by step.

### Prerequisites

- Python 3.12+
- An OpenAI API key in `.env`
- Dependencies installed (agent-framework, mcp, aiosqlite)

To (re)create the database:

```bash
python3 db/create_db.py
```
