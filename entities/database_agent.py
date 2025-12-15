from agent_framework import ChatAgent, MCPStdioTool
from agent_framework.openai import OpenAIChatClient


def create_database_agent(sqlite_mcp):
    return ChatAgent(
        name="DatabaseAgent",
        description="Fetches records for identifiers",
        instructions="""
            Fetch database records for the given identifiers.

            Rules:
            - Query the database only once per request.
            - If records are already fetched, respond with: DATABASE_COMPLETE.
            - Do not repeat queries unless new identifiers are provided.
            """,
        tools=sqlite_mcp,
        chat_client=OpenAIChatClient(model_id="gpt-4o-mini"),
    )

