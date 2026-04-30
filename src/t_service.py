import os, requests


BOT_TOKEN = os.getenv("BOT_TOKEN")
base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text):
    url = f"{base_url}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    return requests.post(url, json=payload)