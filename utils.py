import importlib.util

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Markdown


directory: str = "slides"


def generate_slide(file: str):
    content = ""
    Slide = None
    if file.endswith('.MD'):
        with open(f"{directory}/{file}") as f:
            content = f.read()

        class Slide(Screen):

            def compose(self) -> ComposeResult:
                yield Markdown(content, id="markdown")

    elif file.endswith(".py"):
        filename = file.replace(".py", "")
        module = f"{directory}.{filename}"

        module_path = f"{directory}/{file}"
        spec = importlib.util.spec_from_file_location(
            module, module_path
        )

        if spec is None:
            raise ValueError(f"Failed to load module spec for {module_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        Slide = getattr(module, "Slide")

    return Slide


