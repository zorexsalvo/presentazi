import importlib.util
import sys
from pathlib import Path

from markdown_it import MarkdownIt
from PIL import Image as PILImage
from rich_pixels import Pixels
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Markdown, Static

SLIDE_EXTS = (".md", ".MD", ".py")


def load_slide(path: Path) -> type[Screen]:
    """Load a single slide file (markdown or python Textual screen) as a Screen."""
    path = Path(path)
    if path.suffix in (".md", ".MD"):
        return _markdown_slide(path)
    if path.suffix == ".py":
        return _python_slide(path)
    raise ValueError(f"Unsupported slide type: {path.suffix}")


def load_deck(directory: Path) -> list[tuple[str, type[Screen]]]:
    """Load all slides in a directory, sorted by filename."""
    slides = []
    for path in sorted(Path(directory).iterdir()):
        if path.name == "__init__.py":
            continue
        if path.suffix not in SLIDE_EXTS:
            continue
        slides.append((path.name, load_slide(path)))
    return slides


def _markdown_slide(path: Path) -> type[Screen]:
    """Build a Screen from a Markdown file, rendering image-only paragraphs as images."""
    path = Path(path)
    content = path.read_text()
    base_dir = path.parent
    segments = _split_markdown(content, base_dir)

    class Slide(Screen):
        def compose(self):
            with VerticalScroll(id="markdown-slide"):
                for seg_type, seg_data in segments:
                    if seg_type == "markdown":
                        yield Markdown(seg_data)
                    elif seg_type == "image":
                        yield ImageWidget(seg_data)

    return Slide


def _split_markdown(content: str, base_dir: Path) -> list[tuple[str, Path | str]]:
    """Split markdown into text chunks and image blocks.

    Paragraphs that contain only a single image token become ("image", path).
    Everything else becomes ("markdown", text_chunk).
    """
    tokens = MarkdownIt().parse(content)
    lines = content.splitlines()
    images: list[tuple[int, int, Path]] = []

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type == "paragraph_open" and token.level == 0 and token.map is not None:
            inline = tokens[i + 1] if i + 1 < len(tokens) else None
            if inline is not None and inline.type == "inline" and inline.children:
                children = [
                    child
                    for child in inline.children
                    if child.type != "text" or child.content.strip()
                ]
                if len(children) == 1 and children[0].type == "image":
                    src = children[0].attrs.get("src", "")
                    img_path = _resolve_image_path(src, base_dir)
                    start, end = token.map
                    images.append((start, end, img_path))
        i += 1

    segments: list[tuple[str, Path | str]] = []
    last_end = 0
    for start, end, img_path in images:
        before = "\n".join(lines[last_end:start])
        if before.strip():
            segments.append(("markdown", before))
        segments.append(("image", img_path))
        last_end = end

    after = "\n".join(lines[last_end:])
    if after.strip():
        segments.append(("markdown", after))

    return segments


def _resolve_image_path(src: str, base_dir: Path) -> Path:
    """Resolve an image src to an absolute path."""
    path = Path(src)
    if path.is_absolute():
        return path
    return base_dir / path


def _python_slide(path: Path) -> type[Screen]:
    spec = importlib.util.spec_from_file_location(f"termdeck_slide_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Slide


class ImageWidget(Static):
    """A widget that renders an image file as a Rich Pixels renderable, fitted to the viewport."""

    def __init__(self, path: Path, **kwargs):
        super().__init__("", **kwargs)
        self.path = Path(path)
        self._pil_image = PILImage.open(self.path)
        if self._pil_image.mode not in ("RGB", "RGBA"):
            self._pil_image = self._pil_image.convert("RGB")

    def _fit(self, width: int, height: int) -> tuple[int, int]:
        """Return (pixel_width, pixel_height) that fits inside width x (height*2)."""
        img_w, img_h = self._pil_image.size
        max_h = max(2, height * 2)
        scale = min(width / img_w, max_h / img_h, 1.0)
        pixel_w = max(2, int(img_w * scale))
        pixel_h = max(2, int(img_h * scale))
        if pixel_h % 2 != 0:
            pixel_h += 1
        return pixel_w, pixel_h

    def get_content_height(self, container, viewport, width: int) -> int:
        if width < 1 or viewport.height < 1:
            return 0
        # Subtract 6 from the viewport to leave room for the header, footer,
        # and any text above the image; this is approximate but keeps images
        # on screen without requiring the user to scroll.
        budget = max(2, viewport.height - 6)
        _, pixel_h = self._fit(width, budget)
        return pixel_h // 2

    def render(self):
        width = self.content_size.width
        height = self.content_size.height
        if width < 1 or height < 1:
            return ""

        pixel_w, pixel_h = self._fit(width, height)
        resized = self._pil_image.resize(
            (pixel_w, pixel_h), PILImage.Resampling.LANCZOS
        )
        return Pixels.from_image(resized)


def main() -> None:
    if len(sys.argv) > 1:
        deck_dir = Path(sys.argv[1])
    else:
        deck_dir = Path(__file__).parent / "sample"

    if not deck_dir.is_dir():
        sys.exit(f"error: not a directory: {deck_dir}")

    slides = load_deck(deck_dir)
    if not slides:
        sys.exit(f"error: no slides (.md/.py) found in {deck_dir}")

    from termdeck.app import TermDeck

    TermDeck(deck_dir).run()


if __name__ == "__main__":
    main()
