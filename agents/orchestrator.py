from agents.file_agent import create_file_agent
from agents.database_agent import create_database_agent
from agents.summarizer_agent import create_summarizer_agent
from agents.file_agent import extract_ids

from agent_framework import ChatAgent, MCPStdioTool


async def run_orchestration(filesystem_mcp: MCPStdioTool, sqlite_mcp: MCPStdioTool) -> str:
    """
    Full pipeline:
    1. FileAgent → read files (via filesystem MCP)
    2. Extract IDs (Python)
    3. DatabaseAgent → fetch records (via SQLite MCP)
    4. SummarizerAgent → summarize the matched records
    """

    # 1) Make agents
    file_agent = create_file_agent()
    db_agent = create_database_agent()
    summarizer_agent = create_summarizer_agent()

    # 2) FileAgent → get raw text
    print("→ FileAgent: reading documents...")
    response = await file_agent.run(
        "Read all documents and return their raw text.",
        tools=filesystem_mcp,
        return_intermediate_steps=True
    )
    raw_text = response.text
    # print("raw_text:", raw_text)

    # 3) Extract IDs in Python
    print("→ Extracting IDs...")
    ids = extract_ids(raw_text)

    if not ids:
        return "No IDs found in the documents."

    print(f"→ Found IDs: {ids}")

    # 4) DatabaseAgent → retrieve DB records
    print("→ Fetching DB records...")
    db_response = await db_agent.run(
        f"Fetch all records for the following IDs: {ids}",
        tools=sqlite_mcp
    )

    # 5) Summarize
    print("→ Summarizing...")
    summary = await summarizer_agent.run(
        f"Summarize the following database matches:\n{db_response}"
    )

    # 6) Result
    return summary
