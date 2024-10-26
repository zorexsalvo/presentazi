import os

from textual import events

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static


def generate_slide(file):

    class Slide(Screen):
        def compose(self) -> ComposeResult:
            yield Static(file)
    return Slide


class HeyIMadeThisWithPython(App):
    slide_number = 0
    directory: str = "slides"
    SCREENS = {}

    # or file in range() os.listdir(directory):
    for file in range(10):
        slide = generate_slide(str(file))
        SCREENS[str(file)] = slide

    def on_key(self, event: events.Key) -> None:
        screen_list = list(self.SCREENS.keys())
        screen = screen_list[self.slide_number]

        self.push_screen(screen)
        self.slide_number += 1


if __name__ == "__main__":
    app = HeyIMadeThisWithPython()
    app.run()

