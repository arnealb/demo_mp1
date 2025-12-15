import asyncio
from agent_framework import MCPStdioTool
from entities.orchestrator import setup

def _build_workflow():
    filesystem_mcp = MCPStdioTool(
        name="fs",
        command="python3",
        args=["mcp_servers/filesystem_mcp.py"]
    )

    sqlite_mcp = MCPStdioTool(
        name="db",
        command="python3",
        args=["mcp_servers/sqlite_mcp.py"]
    )

    return asyncio.run(setup(filesystem_mcp, sqlite_mcp))

workflow = _build_workflow()
