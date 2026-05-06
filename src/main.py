import asyncio
import json
import os
import sys
from typing import cast

from dotenv import load_dotenv
from litellm import CustomStreamWrapper, acompletion

from tools import BashTool, FileEditTool, FileListTool, FileReadTool, FileWriteTool

load_dotenv()

DEFAULT_MODEL = os.getenv("MODEL", "gemini/gemini-2.0-flash")
model = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL

tools = [
    FileListTool.file_list_tool,
    FileWriteTool.file_write_tool,
    FileReadTool.file_read_tool,
    FileEditTool.file_edit_tool,
    BashTool.bash_tool,
]

tool_impls = {
    "file_list": FileListTool.file_list_impl,
    "file_read": FileReadTool.file_read_impl,
    "file_edit": FileEditTool.file_edit_impl,
    "file_write": FileWriteTool.file_write_impl,
    "bash": BashTool.bash_impl,
}

history = []


async def get_stream() -> CustomStreamWrapper:
    stream = await acompletion(model=model, messages=history, tools=tools, stream=True)

    return cast(CustomStreamWrapper, stream)


async def get_response(model: str) -> dict:
    tool_calls_map: dict[int, dict] = {}
    chunk = None
    reply = ""

    stream = await get_stream()

    async for chunk in stream:
        delta = chunk.choices[0].delta

        if delta.content:
            print(delta.content, end="", flush=True)
            reply += delta.content

        if delta.tool_calls:
            for tc in delta.tool_calls:
                idx = tc.index
                if idx not in tool_calls_map:
                    tool_calls_map[idx] = {"id": tc.id, "name": "", "arguments": ""}
                if tc.function.name:
                    tool_calls_map[idx]["name"] += tc.function.name
                if tc.function.arguments:
                    tool_calls_map[idx]["arguments"] += tc.function.arguments

    finish_reason = chunk.choices[0].finish_reason if chunk else "stop"

    if finish_reason == "tool_calls":
        return {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {"name": tc["name"], "arguments": tc["arguments"]},
                }
                for tc in tool_calls_map.values()
            ],
        }

    print()
    return {"role": "assistant", "content": reply}


def call_tool(name: str, str_args: str):
    result = {"success": False, "error": "unknown tool"}
    args = json.loads(str_args)

    print(f"\nTool: {name}({args})")
    if name in tool_impls:
        result = tool_impls[name](**args)

    print(f"Result: {result}")
    return result


async def handle_input(message: str):
    history.append({"role": "user", "content": message})

    while True:
        res = await get_response(model)
        history.append(res)

        if "tool_calls" not in res:
            break

        for tc in res["tool_calls"]:
            result = call_tool(tc["function"]["name"], tc["function"]["arguments"])
            history.append(
                {
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": json.dumps(result),
                }
            )


async def main():
    print(f"Using model: {model}")

    while True:
        message = input("\n> ")
        await handle_input(message)


if __name__ == "__main__":
    asyncio.run(main())
