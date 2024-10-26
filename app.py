import os

from textual import events

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static


class MyLightningTalk(App):
    slide_number = 0
    directory: str = "slides"

    SCREENS = {}
    for file in os.listdir(directory):

        def compose(self) -> ComposeResult:
            yield Static("T")

        Slide = type(file, (object,), {
            "compose": compose
        })
        SCREENS[file] = Slide

    def on_key(self, event: events.Key) -> None:
        screen_list = list(self.SCREENS.keys())
        screen = screen_list[self.slide_number]

        self.push_screen(screen)
        self.slide_number += 1


if __name__ == "__main__":
    app = MyLightningTalk()
    app.run()

