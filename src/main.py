import os

from dotenv import load_dotenv
from fastapi import Body, FastAPI, Header

import model
import t_service
from schemas import Update

load_dotenv()


SECRET_TOKEN = os.getenv("SECRET_TOKEN")
app = FastAPI()


@app.post("/t")
async def hola(
    body: Update = Body(...), x_telegram_bot_api_secret_token: str | None = Header(None)
):
    if x_telegram_bot_api_secret_token != SECRET_TOKEN or body.message is None:
        return {"ok": False}

    print(f"> {body.message.text}")
    print(f"> {body.message.from_user.first_name}")
    print(f"> {body.message.from_user.id}")

    try:
        response = model.chat(body.message.from_user.id, body.message.text)
        print(response)

        t_service.send_message(chat_id=body.message.from_user.id, text=response)
        return {"ok": True}
    except Exception as e:
        print(f"Error: {e}")
        return {"ok": True}


@app.get("/")
async def root():
    return {"docs_at": "/docs"}
