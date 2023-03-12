import base64
import json
import urllib.parse

import requests
from text_manipulations import generate_slack_blocks

TYPE = "message_action"
MOCK_CALLBACK_ID = "mock_message"
UNMOCKABLE_TEXT = "This content can't be displayed."


def handle_lambda(event, context):  # pylint: disable=unused-argument
    """The main entry point"""
    body = event.get("body")
    if event.get("isBase64Encoded"):
        body = urllib.parse.parse_qs(base64.b64decode(event["body"]).decode())

    for payload in body["payload"]:
        action = json.loads(payload)

        if action["type"] != TYPE or action["callback_id"] != MOCK_CALLBACK_ID:
            continue

        text = action["message"]["text"]
        if text == UNMOCKABLE_TEXT:
            continue

        response = {
            "response_type": "in_channel",
            "thread_ts": action["message"].get("thread_ts"),
            **generate_slack_blocks(text),
        }
        requests.post(
            action["response_url"],
            json.dumps(response),
            headers={"Content-type": "application/json"},
            timeout=10,
        )

    response = {
        "statusCode": 200,
        "body": "",
    }

    return response
