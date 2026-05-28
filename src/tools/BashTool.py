import subprocess

from langchain.tools import tool


@tool
def bash_impl(command: str, timeout: int = 30) -> dict:
    """Runs a command in bash terminal and return its output.

    Args:
        command: The bash command to execute.
        timeout: Time in seconds to wait for response.

    Returns:
        Result dictionary containing success status and data/error."""

    print(f"\n[confirm] bash({command!r})")

    if input("Allow? [y/N] ").strip().lower() != "y":
        return {
            "success": False,
            "error": "user denied permission",
        }
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=timeout
        )
        output = result.stdout
        if result.stderr:
            output += f"\nstderr: {result.stderr}"
        return {
            "success": True,
            "data": output or "(no output)",
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"command timed out after {timeout}s",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
