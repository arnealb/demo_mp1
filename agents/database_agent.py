from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient


def create_database_agent(mcp_clients: dict) -> ChatAgent:
    """
    DatabaseAgent that accesses the SQLite MCP server.
    It only retrieves raw records using MCP tools.
    """
    return ChatAgent(
        name="DatabaseAgent",
        instructions=(
            "You use SQLite MCP tools such as list_all_entries and "
            "list_all_entries_with_id to fetch database records. "
            "When given a list of IDs, fetch the corresponding records. "
            "Return only the raw records as provided by the tools. "
            "Do not summarize or interpret."
        ),
        chat_client=OpenAIChatClient(model_id="gpt-4o-mini"),
        mcp_clients=mcp_clients,
    )
