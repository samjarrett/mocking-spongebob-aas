import sys
import urllib.parse

from PIL import Image, ImageDraw, ImageFont  # type: ignore
from utils import save_image_respond

WIDTH = 750
HEIGHT = 557
IMAGE = "./is-this.jpg"

STANDARD_TITLE = "is this"


def generate_image(title: str, text: str):
    """Generate an image object for a given text"""
    title = title.upper()
    text = text.upper()

    image = Image.open(IMAGE)
    drawer = ImageDraw.Draw(image)

    font_size = 60
    font = ImageFont.truetype("./impact.ttf", font_size)

    drawer.text(
        (WIDTH / 2, 70),
        title,
        font=font,
        fill="white",
        spacing=10,
        stroke_fill="black",
        stroke_width=2,
        align="center",
        anchor="md",
    )

    while font.getsize(text)[0] > (WIDTH - 40):
        # iterate until the text size is just larger than the criteria
        font_size -= 1
        font = ImageFont.truetype(font.path, font_size)

    drawer.text(
        (WIDTH / 2, HEIGHT - 15),
        text,
        font=font,
        fill="white",
        spacing=10,
        stroke_fill="black",
        stroke_width=2,
        anchor="md",
    )

    return image


def handle_lambda(event, _):
    """The main entry point"""
    text = urllib.parse.unquote_plus(event["pathParameters"]["string"])
    if not text.endswith("?"):
        text += "?"

    return save_image_respond(generate_image(STANDARD_TITLE, text))


def demo(text: str):
    """Create a demo image"""
    text = urllib.parse.unquote_plus(text)
    if not text.endswith("?"):
        text += "?"

    image = generate_image(STANDARD_TITLE, text)

    image.save("output.jpg", "JPEG")
    print(text)


if __name__ == "__main__":
    demo(" ".join(sys.argv[1:]))
