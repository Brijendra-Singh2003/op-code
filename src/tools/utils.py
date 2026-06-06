def request_approval(stmt: str) -> str | None:
    print(stmt)
    reply = input("\nAllow? [y/N]: ")

    if reply.strip().lower() == "y":
        return None

    return reply
