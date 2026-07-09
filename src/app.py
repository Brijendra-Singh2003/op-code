import asyncio

from langchain_core.messages import HumanMessage

from agents.main_agent import main_agent

show_thinking = True


async def run_agent(input, config):
    stream = await main_agent.astream_events(
        input=input,
        config=config,
        version="v3",
    )

    async for message in stream.messages:
        is_thinking = show_thinking

        async def consume_thinking():
            nonlocal is_thinking

            async for token in message.reasoning:
                if not is_thinking:
                    break
                print(f"\033[2m{token}\033[0m", end="")

        async def consume_response():
            nonlocal is_thinking

            async for token in message.text:
                if is_thinking:
                    is_thinking = False
                    print()

                print(token, end="")
            print()

        promises = [consume_response()]
        if show_thinking:
            promises.append(consume_thinking())

        asyncio.gather(*promises)


def input_lines():
    print("\n > ", end="")
    text = input()

    while text.endswith("\\"):
        text = text.removesuffix("\\")
        text += "\n" + input("   ")

    return text


async def start_session(thread_id="cli_session"):
    while True:
        user_input = input_lines()
        if user_input == "/quit":
            return

        await run_agent(
            input={"messages": [HumanMessage(user_input)]},
            config={"configurable": {"thread_id": thread_id}},
        )
