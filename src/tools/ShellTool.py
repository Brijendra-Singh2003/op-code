import platform
from subprocess import TimeoutExpired, run

from langchain_core.tools import tool
from pydantic import BaseModel, Field

description = f"""Executes a given command in {platform.system} system and returns its output.

Usage:
- The command is executed using the system shell.
- User's approvel is asked before executing the command.
- Output contains both stdout and stderr.
- Always keep an upper limit for output if possible.
- If a commands takes longer than `timeout`, it will be terminated."""


class BashInput(BaseModel):
    command: str = Field(description="The bash command to execute")
    timeout: int = Field(
        description="Maximum time in seconds to wait for the command", default=30
    )


@tool(description=description, args_schema=BashInput)
def shell_tool(
    command: str,
    timeout: int = 30,
) -> dict:
    print(f"\nExecuting command: {command!r}")

    if input("Allow? [y/N] ").strip().lower() != "y":
        return {
            "success": False,
            "error": "user denied permission",
        }

    try:
        result = run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except TimeoutExpired:
        return {
            "success": False,
            "error": f"command timed out after {timeout}s",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


__all__ = ["shell_tool"]
