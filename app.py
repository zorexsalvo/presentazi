from textual import events

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static

class MyLightningTalk(App):

    class Welcome(Screen):
        def compose(self) -> ComposeResult:
            yield Static("Good Morning")


    class BSOD(Screen):
        def compose(self) -> ComposeResult:
            yield Static("Hello")


    for a in [1, 2, 3]:
        print(a)

    SCREENS = {
        "welcome": Welcome,
        "bsod": BSOD,
    }
    slide_count = 0

    def on_key(self, event: events.Key) -> None:
        screen_list = list(self.SCREENS.keys())
        screen = screen_list[self.slide_count]

        self.push_screen(screen)
        self.slide_count += 1


def screen_factory():
    pass

if __name__ == "__main__":
    app = MyLightningTalk()
    app.run()

