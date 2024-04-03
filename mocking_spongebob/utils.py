import base64
from io import BytesIO
from typing import Any, Dict

from PIL import Image


def save_image_respond(image: Image.Image) -> Dict[str, Any]:
    """Save an imaage to memory, encode and return a lambda response"""
    output_file = BytesIO()
    image.save(output_file, "JPEG")
    output_file.seek(0)

    return {
        "statusCode": 200,
        "headers": {"content-type": "image/jpeg"},
        "body": base64.b64encode(output_file.read()).decode("utf-8"),
        "isBase64Encoded": True,
    }
