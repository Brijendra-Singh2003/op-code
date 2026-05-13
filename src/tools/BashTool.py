import subprocess

bash_tool = {
    "type": "function",
    "function": {
        "name": "bash",
        "description": "Run a shell command and return its output.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute.",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds (default: 30).",
                },
            },
            "required": ["command"],
        },
    },
}


def bash_impl(command: str, timeout: int = 30) -> dict:
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
