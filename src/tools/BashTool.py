import subprocess
from .result import ok, err

bash_tool = {
    "type": "function",
    "function": {
        "name": "bash",
        "description": "Run a shell command and return its output.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to execute."},
                "timeout": {"type": "integer", "description": "Timeout in seconds (default: 30)."},
            },
            "required": ["command"],
        },
    },
}


def bash_impl(command: str, timeout: int = 30) -> dict:
    print(f"\n[confirm] bash({command!r})")
    if input("Allow? [y/N] ").strip().lower() != "y":
        return err("user denied permission").to_dict()
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        output = result.stdout
        if result.stderr:
            output += f"\nstderr: {result.stderr}"
        return ok(output or "(no output)").to_dict()
    except subprocess.TimeoutExpired:
        return err(f"command timed out after {timeout}s").to_dict()
    except Exception as e:
        return err(str(e)).to_dict()
