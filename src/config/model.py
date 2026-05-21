import os
import sys
from typing import cast

from dotenv import load_dotenv
from litellm import CustomStreamWrapper, acompletion

from tools.index import tools

load_dotenv()
DEFAULT_MODEL = os.getenv("MODEL", "gemini/gemini-2.5-flash")
model_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL


async def send_messages(messages: list[dict[str, str]]):
    response = await acompletion(
        model=model_name, tools=tools, messages=messages, stream=False
    )
    # stream = cast(CustomStreamWrapper, response)

    tool_calls_map: dict[int, dict] = {}
    reply = ""

    message = response.choices[0].message
    reply = message.content or ""
    print(reply)

    if message.tool_calls:
        for idx, tc in enumerate(message.tool_calls):
            tool_calls_map[idx] = {
                "id": tc.id or "",
                "name": tc.function.name or "",
                "arguments": tc.function.arguments or "",
            }

    # async for chunk in stream:
    #     delta = chunk.choices[0].delta
    #     content = delta.content or ""
    #     print(content, end="")
    #     reply += content

    #     if delta.tool_calls:
    #         for tc in delta.tool_calls:
    #             idx = 0
    #             try:
    #                 idx = int(tc.index)
    #             except (TypeError, ValueError):
    #                 idx = len(tool_calls_map)

    #             if idx not in tool_calls_map:
    #                 tool_calls_map[idx] = {"id": tc.id, "name": "", "arguments": ""}
    #             if tc.function.name:
    #                 tool_calls_map[idx]["name"] += tc.function.name
    #             if tc.function.arguments:
    #                 tool_calls_map[idx]["arguments"] += tc.function.arguments

    print()

    return reply, tool_calls_map.values()
