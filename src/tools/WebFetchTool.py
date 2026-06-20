from typing import Type

from langchain.agents import create_agent
from langchain.messages import HumanMessage
import requests
from bs4 import BeautifulSoup
from config import model
from markdownify import markdownify as md

from langchain.tools import tool
from pydantic import BaseModel, Field


description: str = """
- Fetches content from a specified URL and processes it using an AI model
- Takes a URL and a prompt as input
- Fetches the URL content, converts HTML to markdown
- Processes the content with the prompt using a small, fast model
- Returns the model's response about the content
- Use this tool when you need to retrieve and analyze web content
"""


class WebFetchInput(BaseModel):
    url: str = Field(description="URL of the webpage to analyze")
    prompt: str = Field(description="Prompt describing what to extract or analyze")


@tool(description=description, args_schema=WebFetchInput)
def web_fetch(url: str, prompt: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; LangChainBot/1.0)"
        )
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove noisy elements
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    html = str(soup)

    markdown = md(
        html,
        heading_style="ATX",
    )

    # Prevent extremely large contexts
    markdown = markdown[:10000]
    return {
        "success": True,
        "data": _get_model_response(prompt=prompt, markdown=markdown)
    }


def _get_model_response(prompt: str, markdown: str):
    agent = create_agent(
        model=model.gemma_model,
        system_prompt="You analyze webpage content accurately and answer only using the provided webpage.",
    )

    prompt = f"prompt:\n{prompt}\n\nmarkdown:\n{markdown}"
    content = ""

    for message, _ in agent.stream(
        {"messages": [HumanMessage(content=prompt)]},
        stream_mode="messages",
        version="v3",
    ):
        if isinstance(message.content, str):
            content += message.content

    return content
