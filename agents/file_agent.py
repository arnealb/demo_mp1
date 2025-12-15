import re
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from agent_framework import MCPStdioTool


ID_REGEX = r"\b\d{3}\b"  # 3-digit reference IDs (101, 202, 303…)


def extract_ids(text: str) -> list[int]:
    """Extract all 3-digit IDs from text."""
    matches = re.findall(ID_REGEX, text)
    return list({int(m) for m in matches})  # unieke ints


def create_file_agent(filesystem_mcp):
    return ChatAgent(
        name="FileAgent",
        description="Reads documents from the filesystem",
        instructions="""
        Read the documents ONCE and extract all identifiers.

        Rules:
        - Do not reread documents if already done.
        - After reading, return the raw text AND a list of identifiers.
        - If called again, respond with: FILE_COMPLETE.
        """,
        tools=filesystem_mcp,
        chat_client=OpenAIChatClient(model_id="gpt-4o-mini"),
    )

