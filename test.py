from rich_pixels import Pixels
from rich.console import Console
from PIL import Image

console = Console()

with Image.open("python-logo-only.png") as image:
    pixels = Pixels.from_image(image)

console.print(pixels)
