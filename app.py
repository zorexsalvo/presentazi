import os
import importlib

from textual import events
from textual.app import App
from textual.widgets import Header, Footer
from utils import generate_slide


directory: str = "slides"


class HeyIMadeThisWithPython(App):
    screen_title = 'Prezi'
    CSS_PATH = "styles/prezi.tcss"
    SCREENS = {}
    slide_number = 0

    for file in sorted(os.listdir(directory)):
        if file == '__init__.py':
            continue

        slide = generate_slide(file)
        SCREENS[file] = slide

    def on_key(self, event: events.Key) -> None:
        screen_list = list(self.SCREENS.keys())

        try:
            if event.key == "right" and self.slide_number < len(self.SCREENS.keys()):
                self.slide_number += 1
            elif event.key == "left" and self.slide_number > 0:
                self.slide_number -= 1
            else:
                # Do nothing
                pass

            screen = screen_list[self.slide_number]
            self.push_screen(screen)

        except Exception:
            pass

    def compose(self):
        yield Header(name="Prezi")
        yield Footer()


if __name__ == "__main__":
    app = HeyIMadeThisWithPython()
    app.run()

