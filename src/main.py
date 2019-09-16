from itertools import cycle
import hashlib
import math
import sys
import os
import urllib.parse
from io import BytesIO
import boto3
from PIL import Image, ImageDraw, ImageFont

FONT = ImageFont.truetype('./HelveticaNeue-Thin.ttf', 28)

HEIGHT = 369
PADDING = 30

BUCKET_NAME = os.environ.get('BUCKET_NAME')
BUCKET_URL = os.environ.get('BUCKET_URL')

def wrap_text(text, width, font):
    text_lines = []
    text_line = []
    text = text.replace('\n', ' [br] ')
    words = text.split()
    font_size = font.getsize(text)

    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
        text_line.append(word)
        w, h = font.getsize(' '.join(text_line))
        if w > width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]

    if len(text_line) > 0:
        text_lines.append(' '.join(text_line))

    return text_lines

def mocking_case(text):
    funcs = cycle([str.lower, str.upper])

    return ''.join(next(funcs)(c) for c in text)

def get_text_height(text):
    image = Image.new('RGB', (480, 500))
    d = ImageDraw.Draw(image)

    width, height = d.multiline_textsize(text, font=FONT, spacing=10)

    return height

def resize_canvas(image_path="mocking-spongebob.jpg", canvas_height=369):
    im = Image.open(image_path)
    width, height = im.size

    # Center the image
    y = canvas_height - height

    mode = im.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)

    newImage = Image.new(mode, (width, canvas_height), new_background)
    newImage.paste(im, (0, y))
    
    return newImage

def generate_image(text):
    text = "\n".join(wrap_text(mocking_case(text), 480, FONT))
    height = get_text_height(text)

    image = resize_canvas(canvas_height=(HEIGHT + PADDING + height))
    d = ImageDraw.Draw(image)
    d.multiline_text((10,10), text, font=FONT, fill=(0, 0, 0), spacing=10)

    return image

def main(event, context):
    text = urllib.parse.unquote(event['pathParameters']['string'])
    image = generate_image(text)
    filename = hashlib.sha1(text.encode()).hexdigest() + '.jpg'

    outputFile = BytesIO()
    image.save(outputFile, 'JPEG')
    outputFile.seek(0)
    s3 = boto3.client('s3')
    s3.put_object(Bucket=BUCKET_NAME, Key=filename, ContentType='image/jpeg', Body=outputFile)

    url = BUCKET_URL+'/'+filename
    response = {}
    response['statusCode'] = 302
    response['headers'] = {
        'Location': url
    }
    response['body'] = url

    return response

if __name__ == '__main__':
    main({
        'pathParameters': {
            'string': sys.argv[1]
        }
    }, None)