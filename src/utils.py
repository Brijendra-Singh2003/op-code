from typing import Literal


def make_message(role: Literal["user", "assistant", "system"], content: str):
    return {
        "role": role,
        "content": content,
    }
