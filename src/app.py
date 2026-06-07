import asyncio

from langchain_core.messages import HumanMessage
from rich.markdown import Markdown
from rich.text import Text
from lib.screenManager import screen, console

from agents.main_agent import main_agent


async def run_agent(input, config):
    stream = await main_agent.astream_events(
        input=input,
        config=config,
        version="v3",
    )

    async for message in stream.messages:

        async def consume_reasoning():
            reasoning_text = ""

            async for token in message.reasoning:
                reasoning_text += token
                reasoning_text = "\n".join(reasoning_text.split("\n")[-5:])

                screen.update(Text(reasoning_text, style="dim"))

            screen.clear()


        async def consume_text():
            answer_text = ""

            async for token in message.text:
                answer_text += token
                screen.update(Markdown(answer_text))

            screen.save()


        await asyncio.gather(consume_reasoning(), consume_text())

    console.print()


async def start_session(thread_id="cli_session"):
    while True:
        user_input = input("\n > ")
        if user_input == "/quit":
            return

        await run_agent(
            input={"messages": [HumanMessage(user_input)]},
            config={"configurable": {"thread_id": thread_id}},
        )
