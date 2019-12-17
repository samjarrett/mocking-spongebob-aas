import urllib.parse
import base64
import json
from text_manipulations import mocking_case


def generate_slack_response(text):
    url = 'https://mock.sam.wtf/' + urllib.parse.quote_plus(text)

    body = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": mocking_case(text)
                },
                "image_url": url,
                "alt_text": mocking_case(text)
            }
        ]
    }

    response = {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body)
    }

    return response


def handle_lambda(event, context): # pylint: disable=unused-argument
    body = urllib.parse.parse_qs(base64.b64decode(event["body"]).decode())

    text = body['text'][0]

    return generate_slack_response(text)


if __name__ == '__main__':
    print(generate_slack_response("hello"))
