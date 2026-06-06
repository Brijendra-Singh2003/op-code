import asyncio

import app

if __name__ == "__main__":
    try:
        asyncio.run(app.start_session())
    except KeyboardInterrupt:
        pass

    print("\nGoodby 👋")
