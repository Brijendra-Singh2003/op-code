from dotenv import load_dotenv as _load_env
from langchain.chat_models import init_chat_model as _init_chat_model

_load_env()

gemma_model = _init_chat_model(
    model="gemma-4-31b-it",
    model_provider="google-genai",
)

# Groq models
llama_model = _init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq",
)

deepseek_model = _init_chat_model(
    model="deepseek-r1-distill-llama-70b",
    model_provider="groq",
)

mixtral_model = _init_chat_model(
    model="mixtral-8x7b-32768",
    model_provider="groq",
)

qwen_model = _init_chat_model(
    model="qwen/qwen3-32b",
    model_provider="groq",
)