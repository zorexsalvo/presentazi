from rich_pixels import Pixels
from rich.console import Console
from PIL import Image

console = Console()

with Image.open("table.jpg") as image:
    pixels = Pixels.from_image(image)

console.print(pixels)
