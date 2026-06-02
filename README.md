# op-code

`op-code` is a Python-based autonomous AI agent built using LangChain, designed to interact with the system and perform tasks through a conversational interface.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install Dependencies**:
   ```bash
   uv sync
   ```

3. **Environment Variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   GROQ_API_KEY=your_groq_api_key
   # Add other necessary keys here
   ```

## Usage

To start the agent in interactive mode:

```bash
uv run python src/main.py
```

Once the session starts, you can chat with the agent. To exit, type `/quit`.
