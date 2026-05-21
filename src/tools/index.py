import json

from tools import BashTool, FileEditTool, FileListTool, FileReadTool, FileWriteTool

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


def call_tool(id: str, name: str, str_args: str):
    print(f"{id[:12]}: {name}({str_args})")
    args = json.loads(str_args)

    if name not in tool_impls:
        print(f"error: function not found: {name}")
        return {
            "role": "system",
            "content": f"No tool named '{name}'. Valid tool names: {tool_impls.keys()}",
        }

    val = tool_impls[name](**args)
    print("result:", json.dumps(val, indent=2), end="\n\n")

    return {
        "role": "tool",
        "tool_call_id": id,
        "name": name,
        "content": json.dumps(val),
    }
