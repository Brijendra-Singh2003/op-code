import asyncio
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

def run_agent_stream(messages):
    try:
        return main_agent.astream_events({"messages": messages}, version="v2")
    except Exception as e:
        print(f"Error: {e}")
        if input("Retry? [Y/n]: ").lower() == "y":
            return run_agent_stream(messages)
        raise e

async def agent_loop():
    messages = []
    while True:
        message = input("\n> ")
        if message == "/quit":
            break

        messages.append(HumanMessage(message))
        final_messages = None

        print()  # newline before streamed output
        async for event in run_agent_stream(messages):
            kind = event.get("event")

            # Stream token chunks as they arrive
            if kind == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")
                if chunk:
                    text = extract_visible_text(chunk.content)
                    if text:
                        print(text, end="", flush=True)

            # Capture final agent output to update message history
            elif kind == "on_chain_end" and event.get("name") == "LangGraph":
                output = event.get("data", {}).get("output")
                if output and "messages" in output:
                    final_messages = output["messages"]

        print()  # newline after streamed output ends

        if final_messages:
            messages = final_messages
        else:
            # Fallback: re-invoke without streaming to get updated history
            response = await main_agent.ainvoke({"messages": messages})
            messages = response["messages"]

async def main():
    try:
        await agent_loop()
    except Exception as e:
        print(f"error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())