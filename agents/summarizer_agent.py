from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient


def create_summarizer_agent() -> ChatAgent:
    """
    SummarizerAgent that creates a concise, accurate summary
    of the provided content without adding new information.
    """
    return ChatAgent(
        name="SummarizerAgent",
        instructions=(
            "You summarize the provided content into a short, clear and factual summary. "
            "Do not add new information. "
            "Do not invent details. "
            "Focus only on the main points contained in the text."
        ),
        chat_client=OpenAIChatClient(model_id="gpt-4o-mini"),
    )
