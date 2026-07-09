def request_approval(stmt: str) -> dict | None:
    print(stmt)
    reply = input("Allow? [y/N]: ").strip()

    if reply.lower() == "y":
        return None

    response = {
        "success": False,
        "error": "user denied permission",
    }

    if reply and reply.lower() != "n":
        response["user_message"] = reply

    return response
