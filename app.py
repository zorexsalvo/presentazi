import os

from textual import events

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static

directory: str = "slides"

def generate_slide(file: str):
    content = ""
    with open(f"{directory}/{file}") as f:
        content = f.read()

    class Slide(Screen):
        def compose(self) -> ComposeResult:
            yield Static(content)

    return Slide


class HeyIMadeThisWithPython(App):
    slide_number = 0
    SCREENS = {}

    for file in os.listdir(directory):
        slide = generate_slide(file)
        SCREENS[file] = slide

    def on_key(self, event: events.Key) -> None:
        screen_list = list(self.SCREENS.keys())
        screen = screen_list[self.slide_number]

        self.push_screen(screen)
        self.slide_number += 1


if __name__ == "__main__":
    app = HeyIMadeThisWithPython()
    app.run()

