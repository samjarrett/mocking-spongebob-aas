import base64
import json
import urllib.parse

from text_manipulations import generate_slack_blocks


def generate_slack_response(text):
    """Generate a slack response"""
    body = {"response_type": "in_channel", **generate_slack_blocks(text)}

    response = {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }

    return response


def handle_lambda(event, context):  # pylint: disable=unused-argument
    """The main entry point"""
    body = event.get("body")
    if event.get("isBase64Encoded"):
        body = urllib.parse.parse_qs(base64.b64decode(event["body"]).decode())

    text = body["text"][0]

    return generate_slack_response(text)


if __name__ == "__main__":
    print(generate_slack_response("hello"))
