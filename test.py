from pathlib import Path

from PIL import Image as PILImage

from termdeck.deck import load_deck, load_slide

SAMPLE = Path(__file__).parent / "termdeck" / "sample"


def test_load_slide_markdown():
    cls = load_slide(SAMPLE / "p01_intro.md")
    assert cls.__name__ == "Slide"


def test_load_slide_python(tmp_dir):
    py = tmp_dir / "slide.py"
    py.write_text("from textual.screen import Screen\nclass Slide(Screen): pass\n")
    cls = load_slide(py)
    assert issubclass(cls, __import__("textual.screen", fromlist=["Screen"]).Screen)


def test_load_deck_sorted():
    slides = load_deck(SAMPLE)
    names = [name for name, _ in slides]
    assert names == sorted(names)
    assert len(slides) == 2
    assert all(name.endswith((".md", ".MD", ".py")) for name in names)


def test_navigation():
    from pathlib import Path

    from textual.events import Key

    from termdeck.app import TermDeck

    async def _run():
        app = TermDeck(Path(__file__).parent / "termdeck" / "sample")
        async with app.run_test() as pilot:
            assert len(app.names) == 2
            app.on_key(Key("right", "right"))
            await pilot.pause()
            assert app.slide_number == 1
            app.on_key(Key("left", "left"))
            await pilot.pause()
            assert app.slide_number == 0

    import asyncio

    asyncio.run(_run())


def test_markdown_inline_image(tmp_dir):
    from termdeck.app import TermDeck

    img_path = tmp_dir / "diagram.png"
    PILImage.new("RGB", (20, 10), color="blue").save(img_path)

    md = tmp_dir / "slide.md"
    md.write_text("# Title\n\n![diagram](diagram.png)\n")

    async def _run():
        app = TermDeck(tmp_dir)
        async with app.run_test(size=(80, 24)) as pilot:
            await pilot.pause()
            image_widget = app.screen.query_one("ImageWidget")
            renderable = image_widget.render()
            assert renderable is not None

    import asyncio

    asyncio.run(_run())


def test_markdown_without_images(tmp_dir):
    from termdeck.app import TermDeck

    md = tmp_dir / "slide.md"
    md.write_text("# Title\n\nSome text.\n")

    async def _run():
        app = TermDeck(tmp_dir)
        async with app.run_test(size=(80, 24)) as pilot:
            await pilot.pause()
            assert len(list(app.screen.query("ImageWidget").results())) == 0

    import asyncio

    asyncio.run(_run())


def main():
    test_load_slide_markdown()
    test_load_deck_sorted()
    test_navigation()

    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tmp:
        path = Path(tmp)
        test_load_slide_python(path)
        test_markdown_inline_image(path)
        test_markdown_without_images(path)

    print("All tests passed.")


if __name__ == "__main__":
    main()
