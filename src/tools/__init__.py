from langchain_community.tools import DuckDuckGoSearchRun
from tools import FileEditTool, FileListTool, FileReadTool, FileWriteTool, ShellTool

tools = [
    FileListTool.file_list,
    FileWriteTool.file_write,
    FileReadTool.file_read,
    FileEditTool.file_edit,
    ShellTool.shell_tool,
    DuckDuckGoSearchRun(),
]
