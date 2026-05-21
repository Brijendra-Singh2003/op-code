import asyncio
import json
import os

from config import model
from src.utils import make_message
from tools.index import call_tool

prompt = f"""
## Role
You are a helpful and expert autonomous agent capable of interacting with the local system and external APIs using the tools provided.

# Context
- You are inside a terminal session.
- Your current working directory is {os.getcwd()}.

## Objective
Communicate with the user and solve their request efficiently and accurately.

## Constraints
- If you lack sufficient information for a required argument, ask the user specifically for that information.
- If a tool returns an error, analyze the error and attempt to fix your approach rather than repeating the same failed call.

## Rules:
- Be concise.
- Respond normally in plain text.
- Keep answers short and technical.
- Always use relative path when accessing files.
- Always Read files before editing them, they may have changed after last edit.
- Keep changes minimal.
"""

messages: list[dict[str, str]] = [
    {
        "role": "system",
        "content": prompt,
    }
]


async def agent_loop():
    while True:
        message = input("\n> ")

        if message == "/quit":
            break

        messages.append(make_message("user", message))
        reply, tool_calls = await model.send_messages(messages=messages)
        messages.append(make_message("assistant", reply))

        while tool_calls:
            for tool_call in tool_calls:
                id = tool_call.get("id", None)
                func = tool_call.get("name", None)
                args = tool_call.get("arguments", None)

                if not isinstance(id, str):
                    print(f"error: invalid function id: {id}")
                    continue

                if not isinstance(func, str):
                    print(f"error: invalid function name: {func}")
                    continue

                if not isinstance(args, str):
                    print(f"error: invalid args name: {args}")
                    continue

                result = call_tool(id, func, args)
                messages.append(result)

            reply, tool_calls = await model.send_messages(messages=messages)
            messages.append(make_message("assistant", reply))


async def main():
    print(f"Using model: {model.model_name}")
    try:
        await agent_loop()
    except Exception as e:
        print(f"error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
