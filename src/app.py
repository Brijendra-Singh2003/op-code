from langchain_core.messages import HumanMessage
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


async def input_loop(messages):
    while True:
        user_input = input("\n > ")
        if user_input == "/quit":
            return

        messages.append(HumanMessage(user_input))
        response = await main_agent.ainvoke({"messages": messages})
        messages = response["messages"]

        if content := extract_visible_text(messages[-1].content):
            print("\n", content, "\n")


async def start_session(history=[]):
    try:
        await input_loop(history)

    except Exception as e:
        print(f"error: {str(e)}")
