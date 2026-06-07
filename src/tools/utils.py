from lib.screenManager import console

def request_approval(stmt: str) -> str | None:
    console.print(stmt)
    reply = console.input("Allow? [y/N]: ")

    if reply.strip().lower() == "y":
        return None

    return reply
