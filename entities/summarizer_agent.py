from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient


def create_summarizer_agent():
    return Agent(
        client=OpenAIChatClient(model_id="gpt-4o-mini"),
        name="SummarizerAgent",
        description="Produces the final answer",
        instructions="""
            Produce the FINAL summary for the user.

            Rules:
            - Summarize the provided information once.
            - After producing the summary, do not perform any further actions.
            - This is the FINAL ANSWER.
            """,
    )
