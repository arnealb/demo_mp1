import re
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient


ID_REGEX = r"\b\d{3}\b"  # 3-digit reference IDs (101, 202, 303…)


def extract_ids(text: str) -> list[int]:
    """Extract all 3-digit IDs from text."""
    matches = re.findall(ID_REGEX, text)
    return list({int(m) for m in matches})  # unieke ints


def create_file_agent(mcp_clients: dict) -> ChatAgent:
    """
    Create a FileAgent that uses the filesystem MCP tools.
    """
    return ChatAgent(
        name="FileAgent",
        instructions=(
            "You use filesystem MCP tools to list and read documents. "
            "Return the full content of every document you read. "
            "Do not summarize. Do not analyze. Just return the raw text."
        ),
        chat_client=OpenAIChatClient(model_id="gpt-4o-mini"),
        mcp_clients=mcp_clients,
    )
