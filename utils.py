from textual.reactive import reactive
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Markdown


directory: str = "slides"


def generate_slide(file: str):
    content = ""
    with open(f"{directory}/{file}") as f:
        content = f.read()

    class Slide(Screen):
        code_dark_theme = reactive('material-light')

        def compose(self) -> ComposeResult:
            yield Markdown(content, id="markdown")

    return Slide


