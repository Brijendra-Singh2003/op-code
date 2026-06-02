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


async def input_loop(state):
    while True:
        user_input = input("\n > ")
        if user_input == "/quit":
            return

        state['messages'].append(HumanMessage(user_input))
        stream = main_agent.stream_events(state, version='v3')

        for message in stream.messages:
            for token in message.text:
                print(token, end="", flush=True)

        print()
        state = stream.output


async def start_session(history=[]):
    try:
        await input_loop({"messages": history})

    except Exception as e:
        print(f"error: {str(e)}")
