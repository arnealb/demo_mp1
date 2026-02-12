from agent_framework import Agent, MCPStdioTool
from agent_framework.openai import OpenAIChatClient


def create_database_agent(sqlite_mcp):
    return Agent(
        client=OpenAIChatClient(model_id="gpt-4o-mini"),
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
    )
