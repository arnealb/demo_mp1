# demo_mp1
This demo reads documents from a folder, extracts reference IDs from the text, checks those IDs against a SQLite database through an MCP server, and lets an AI agent generate a final summary. The FileAgent reads the files, the DatabaseAgent retrieves the matching records, and the SummarizerAgent produces the final output. The orchestrator coordinates the entire pipeline.
