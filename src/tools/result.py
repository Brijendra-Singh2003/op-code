from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class ToolResult:
    success: bool
    data: Any = None
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def ok(data: Any = None) -> ToolResult:
    return ToolResult(success=True, data=data)


def err(message: str) -> ToolResult:
    return ToolResult(success=False, error=message)
