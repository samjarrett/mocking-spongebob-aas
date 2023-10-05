import sys
import urllib.parse
from typing import List, Tuple, Union

from PIL import Image, ImageDraw, ImageFont  # type: ignore
from text_manipulations import mocking_case
from utils import save_image_respond

FONT = ImageFont.truetype("./HelveticaNeue-Thin.ttf", 28)

HEIGHT = 369
PADDING = 30

BackgroundType = Union[int, Tuple[int, int, int, int], Tuple[int, int, int]]


def wrap_text(text: str, width: int, font: ImageFont.FreeTypeFont):
    """Wrap text to new lines to meet a given width"""
    text_lines: List[str] = []
    text_line: List[str] = []
    text = text.replace("\n", " [br] ")
    words = text.split()

    for word in words:
        if word == "[br]":
            text_lines.append(" ".join(text_line))
            text_line = []
            continue

        text_line.append(word)
        text_width = font.getlength(" ".join(text_line))
        if text_width > width:
            text_line.pop()
            text_lines.append(" ".join(text_line))
            text_line = [word]

    if text_line:
        text_lines.append(" ".join(text_line))

    return text_lines


def get_text_height(text: str) -> int:
    """Get the total text height"""
    image = Image.new("RGB", (480, 500))
    drawer = ImageDraw.Draw(image)

    _, top, _, bottom = drawer.multiline_textbbox((10, 10), text, font=FONT, spacing=10)

    height = bottom - top

    return height


def resize_canvas(
    image_path: str = "mocking-spongebob.jpg", canvas_height: int = 369
) -> Image:
    """Resize the canvas to the given height"""
    image = Image.open(image_path)
    width, height = image.size

    # Center the image
    y_position = canvas_height - height

    mode = image.mode
    if len(mode) == 1:  # L, 1
        new_background: BackgroundType = 255
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)

    new_image = Image.new(mode, (width, canvas_height), new_background)
    new_image.paste(image, (0, y_position))

    return new_image


def generate_image(text: str):
    """Generate an image object for a given text"""
    text = "\n".join(wrap_text(mocking_case(text), 460, FONT))
    height = get_text_height(text)

    image = resize_canvas(canvas_height=HEIGHT + PADDING + height)
    drawer = ImageDraw.Draw(image)
    drawer.multiline_text((10, 10), text, font=FONT, fill=(0, 0, 0), spacing=10)

    return image


def handle_lambda(event, _):
    """The main entry point"""
    text = urllib.parse.unquote_plus(event["pathParameters"]["string"])
    return save_image_respond(generate_image(text))


def demo(text: str):
    """Create a demo image"""
    text = urllib.parse.unquote_plus(text)
    image = generate_image(text)

    image.save("output.jpg", "JPEG")


if __name__ == "__main__":
    demo(sys.argv[1])
