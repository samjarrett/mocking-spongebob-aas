import sys
import urllib.parse
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from text_manipulations import mocking_case

FONT = ImageFont.truetype('./HelveticaNeue-Thin.ttf', 28)

HEIGHT = 369
PADDING = 30


def wrap_text(text, width, font):
    text_lines = []
    text_line = []
    text = text.replace('\n', ' [br] ')
    words = text.split()

    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue

        text_line.append(word)
        text_width, _ = font.getsize(' '.join(text_line))
        if text_width > width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]

    if text_line:
        text_lines.append(' '.join(text_line))

    return text_lines


def get_text_height(text):
    image = Image.new('RGB', (480, 500))
    drawer = ImageDraw.Draw(image)

    _, height = drawer.multiline_textsize(text, font=FONT, spacing=10)

    return height


def resize_canvas(image_path="mocking-spongebob.jpg", canvas_height=369):
    image = Image.open(image_path)
    width, height = image.size

    # Center the image
    y_position = canvas_height - height

    mode = image.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)

    new_image = Image.new(mode, (width, canvas_height), new_background)
    new_image.paste(image, (0, y_position))

    return new_image


def generate_image(text):
    text = "\n".join(wrap_text(mocking_case(text), 460, FONT))
    height = get_text_height(text)

    image = resize_canvas(canvas_height=(HEIGHT + PADDING + height))
    drawer = ImageDraw.Draw(image)
    drawer.multiline_text((10, 10), text, font=FONT, fill=(0, 0, 0), spacing=10)

    return image


def handle_lambda(event, context): # pylint: disable=unused-argument
    text = urllib.parse.unquote_plus(event['pathParameters']['string'])
    image = generate_image(text)

    output_file = BytesIO()
    image.save(output_file, 'JPEG')
    output_file.seek(0)

    response = {
        "statusCode": 200,
        "headers": {"content-type": "image/jpeg"},
        "body": base64.b64encode(output_file.read()).decode('utf-8'),
        "isBase64Encoded": True,
    }

    return response


def demo(text):
    text = urllib.parse.unquote_plus(text)
    image = generate_image(text)

    image.save('output.jpg', 'JPEG')


if __name__ == '__main__':
    demo(sys.argv[1])
