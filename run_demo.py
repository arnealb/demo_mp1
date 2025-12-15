import asyncio
import logging
from agent_framework import MCPStdioTool
from agents.orchestrator import setup  

logging.getLogger("asyncio").setLevel(logging.CRITICAL)

async def main():
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

    workflow = await setup(filesystem_mcp, sqlite_mcp)

    # 1) één vraag
    # async for event in workflow.run_stream(
    #     "Read the documents, find relevant IDs, fetch their database records and summarize the result."):
    #     print(event)
    final_answer = None

    async for event in workflow.run_stream(
        "Read the documents, find relevant IDs, fetch their database records and summarize the result."
    ):
        print (event)
        if event.__class__.__name__ == "WorkflowOutputEvent":
            final_answer = event.data.contents

    print("\n===== FINAL RESULT =====\n")
    print(final_answer[0].text)


    
    

    print("\n===== RESULT =====\n")
    # print(result)

if __name__ == "__main__":
    asyncio.run(main())
