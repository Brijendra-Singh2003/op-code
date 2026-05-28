import asyncio

from langchain.messages import HumanMessage

from agents.main_agent import main_agent


def extract_visible_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for block in content:
            if isinstance(block, str):
                parts.append(block)

            elif isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))

        return "".join(parts)

    return ""


def run_agent(messages):
    try:
        return main_agent.ainvoke({"messages": messages})
    except Exception as e:
        print(f"Error: {e}")
        if input("Retry?[Y/n]: ").lower() == "y":
            return run_agent(messages)
        raise e


async def agent_loop():
    messages = []

    while True:
        message = input("\n> ")

        if message == "/quit":
            break

        messages.append(HumanMessage(message))
        response = await run_agent(messages)
        messages = response["messages"]
        content = response["messages"][-1].content
        print(extract_visible_text(content), end="")


async def main():
    try:
        await agent_loop()
    except Exception as e:
        print(f"error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
