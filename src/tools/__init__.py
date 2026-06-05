from langchain_community.tools import ShellTool

from tools import FileEditTool, FileListTool, FileReadTool, FileWriteTool

tools = [
    FileListTool.file_list,
    FileWriteTool.file_write,
    FileReadTool.file_read,
    FileEditTool.file_edit,
    ShellTool(ask_human_input=True),
]
