from langchain_core.messages import HumanMessage

from agents.main_agent import main_agent


def run_agent(input, config):
    stream = main_agent.stream_events(
        input=input,
        config=config,
        version="v3",
    )

    for message in stream.messages:
        print("\n[Thinking]")
        for token in message.reasoning:
            print(token, end="", flush=True)

        print("\n\n[Response]")
        for token in message.text:
            print(token, end="", flush=True)

    print()


async def start_session(thread_id="cli_session"):
    while True:
        user_input = input("\n > ")
        if user_input == "/quit":
            return

        run_agent(
            input={"messages": [HumanMessage(user_input)]},
            config={"configurable": {"thread_id": thread_id}},
        )
