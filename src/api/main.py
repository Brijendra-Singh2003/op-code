import os

from dotenv import load_dotenv
from fastapi import Body, FastAPI, Header
from google.genai import types

from config.t_service import send_message
from schemas import Update

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")
app = FastAPI()

histories: dict[int, list[types.Content]] = dict()


@app.post("/t")
async def hola(
    body: Update = Body(...), x_telegram_bot_api_secret_token: str | None = Header(None)
):
    if x_telegram_bot_api_secret_token != SECRET_TOKEN or body.message is None:
        return {"ok": False}

    sender = body.message.from_user
    print(f">{sender.first_name}: {body.message.text}")

    if sender.id not in histories:
        histories[sender.id] = []

    try:
        response = "Hola"
        print(response)

        send_message(chat_id=body.message.from_user.id, text=response)
        return {"ok": True}
    except Exception as e:
        print(f"Error: {e}")
        return {"ok": True}


@app.get("/")
async def root():
    return {"docs_at": "/docs"}
