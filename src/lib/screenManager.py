from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.console import Group


console = Console()


class Screen:
    def __init__(self):
        self._current = Text("")
        self._live: Live | None = None


    def start(self):
        if self._live is not None:
            return

        self._live = Live(
            self._current,
            console=console,
            refresh_per_second=20,
            vertical_overflow="visible",
        )
        self._live.start()


    def stop(self):
        if self._live is None:
            return

        self._live.stop()
        self._live = None


    def update(self, renderable):
        self._current = renderable

        if self._live is None:
            self.start()

        self._live.update(renderable, refresh=True)


    def save(self):
        if self._live is None:
            return

        self.stop()
        self._current = Text("")


    def clear(self):
        self.update(Text(""))


screen = Screen()
