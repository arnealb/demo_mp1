from entities.file_agent import create_file_agent
from entities.database_agent import create_database_agent
from entities.summarizer_agent import create_summarizer_agent
from entities.file_agent import extract_ids

from agent_framework import ChatAgent, MCPStdioTool, MagenticBuilder, StandardMagenticManager
from agent_framework.openai import OpenAIChatClient

def setup(filesystem_mcp: MCPStdioTool, sqlite_mcp: MCPStdioTool) -> MagenticBuilder: 
    file_agent = create_file_agent(filesystem_mcp)
    db_agent = create_database_agent(sqlite_mcp)
    summarizer_agent = create_summarizer_agent()

    # manager_agent = create_orchestrator_agent()

    
    manager_agent = StandardMagenticManager(
    instructions="""
    Goal:
    Produce a single final answer.

    Process:
    1. Use FileAgent to read documents and extract identifiers.
    2. Use DatabaseAgent to fetch records for those identifiers.
    3. Use SummarizerAgent exactly once to produce the final answer.

    Rules:
    - Do not repeat completed steps.
    - After SummarizerAgent responds, STOP immediately.
    """,
    chat_client=OpenAIChatClient(model_id="gpt-4o-mini"),
    )


    workflow = (
        MagenticBuilder()
        .participants(
            file=file_agent,
            database=db_agent,
            summarizer=summarizer_agent,
        )
        .with_standard_manager(
            manager_agent,
            max_round_count=4,
            max_stall_count=1,
        )

        .build()
    )

    # TODO ARNE: find alternative for this, not clean at all
    orig_run_stream = workflow.run_stream

    def run_stream_compat(message, **kwargs):
        # dev ui stuurt dict, ik wil string tho
        if isinstance(message, dict):
            if "input" in message:
                message = message["input"]
            elif "messages" in message:
                message = message["messages"][-1]["content"]

        return orig_run_stream(message)

    workflow.run_stream = run_stream_compat


    return workflow



def create_orchestrator_agent() -> ChatAgent:
    return StandardMagenticManager(
        instructions="""
            Goal:
            Produce a single final answer.

            Process:
            1. Use FileAgent to read documents and extract identifiers.
            2. Use DatabaseAgent to fetch records for those identifiers.
            3. Use SummarizerAgent exactly once to produce the final answer.

            Rules:
            - Do not repeat completed steps.
            - After SummarizerAgent responds, STOP immediately.
            """,
        chat_client=OpenAIChatClient(model_id="gpt-4o-mini"),
    )
