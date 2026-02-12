import sys
import asyncio
import logging
from agent_framework import MCPStdioTool
from agents.orchestrator import setup
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

    workflow = setup(filesystem_mcp, sqlite_mcp)
    serve(entities=[workflow], port=8080, auto_open=True)

if __name__ == "__main__":
    main()
