class Foo:
    def __init__(self):
        self.s = ""


def foo(bar: Foo):
    while True:
        print(bar.s)

        if bar.s == "bar":
            yield "need input"
            print("got input:", bar.s)

        yield "done."


class Chat:
    def __init__(self):
        self.inputs = Foo()
        self.generator = foo(self.inputs)

    def send_message(self, msg: str):
        self.inputs.s = msg
        return next(self.generator)


chat = Chat()
while True:
    msg = input("> ")
    res = chat.send_message(msg)
    print(res)
