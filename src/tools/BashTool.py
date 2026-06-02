from subprocess import TimeoutExpired, run

from langchain_core.tools import tool
from pydantic import BaseModel, Field

description = """Executes a given bash command and returns its output.

Usage:
- The command is executed using the system shell.
- User's approvel is asked before executing the command.
- Output contains both stdout and stderr.
- Do not use calls that may overflow the terminal (e.g. ls -R).
- Always keep an upper limit in output if possible.
- Commands exceeding the timeout will be terminated."""


class BashInput(BaseModel):
    command: str = Field(description="The bash command to execute")
    timeout: int = Field(
        description="Maximum time in seconds to wait for the command", default=30
    )


@tool(description=description, args_schema=BashInput)
def bash_tool(
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

        output = result.stdout

        if result.stderr:
            output += f"\nstderr: {result.stderr}"

        return {
            "success": True,
            "data": output or "(no output)",
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


__all__ = ["bash_tool"]
