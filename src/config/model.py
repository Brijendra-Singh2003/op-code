from dotenv import load_dotenv as _load_env
from langchain.chat_models import init_chat_model as _init_chat_model

_load_env()

gemma_model = _init_chat_model(
    model="gemma-4-31b-it",
    model_provider="google-genai",
)
