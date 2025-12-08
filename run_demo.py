import asyncio
from agent_framework import ChatAgent, MCPStdioTool
from agents.orchestrator import run_orchestration
import logging

logging.getLogger("asyncio").setLevel(logging.CRITICAL)




async def main():
    # Start both MCP servers

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

    # Run orchestrator pipeline
    result = await run_orchestration(filesystem_mcp=filesystem_mcp, sqlite_mcp=sqlite_mcp)

    print("\n===== FINAL RESULT =====\n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())


