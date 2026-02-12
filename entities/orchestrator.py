from entities.file_agent import create_file_agent
from entities.database_agent import create_database_agent
from entities.summarizer_agent import create_summarizer_agent

from agent_framework import MCPStdioTool, WorkflowBuilder, WorkflowAgent


def setup(filesystem_mcp: MCPStdioTool, sqlite_mcp: MCPStdioTool) -> WorkflowAgent:
    file_agent = create_file_agent(filesystem_mcp)
    db_agent = create_database_agent(sqlite_mcp)
    summarizer_agent = create_summarizer_agent()

    workflow = (
        WorkflowBuilder(start_executor=file_agent)
        .add_chain([file_agent, db_agent, summarizer_agent])
        .build()
    )

    orchestrator = WorkflowAgent(
        workflow=workflow,
        name="Orchestrator",
        description="Reads documents, fetches database records, and produces a summary.",
    )
    return orchestrator, file_agent, db_agent, summarizer_agent

