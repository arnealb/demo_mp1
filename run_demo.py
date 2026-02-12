import sys
import asyncio
import logging
from agent_framework import MCPStdioTool
from entities.orchestrator import setup
from agent_framework.devui import serve


logging.getLogger("asyncio").setLevel(logging.CRITICAL)

def main():
    filesystem_mcp = MCPStdioTool(
        name="fs",
        command=sys.executable,
        args=["mcp_servers/filesystem_mcp.py"]
    )

    # sqlite_mcp = MCPStdioTool(
    #     name="db",
    #     command="python3",
    #     args=["mcp_servers/sqlite_mcp.py"]
    # )

    sqlite_mcp = MCPStdioTool(
        name="db",
        command=sys.executable,
        args=["mcp_servers/sqlite_mcp.py"]
    )

    orchestrator, file_agent, db_agent, summarizer_agent = setup(filesystem_mcp, sqlite_mcp)
    serve(entities=[orchestrator, file_agent, db_agent, summarizer_agent], port=8080, auto_open=True)

if __name__ == "__main__":
    main()
