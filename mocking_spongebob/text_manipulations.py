import urllib.parse


def mocking_case(text):
    """Create mocking case text"""
    value = ""
    prev = ""
    for character in text:
        value += character.upper() if prev.islower() else character.lower()
        prev = value[-1:] if character.isalpha() else prev

    return value


def generate_slack_blocks(text: str):
    """Generate slack blocks definition for a mocking spongebob"""
    url = "https://mock.sam.wtf/" + urllib.parse.quote_plus(text)

    return {
        "blocks": [
            {
                "type": "image",
                "title": {"type": "plain_text", "text": mocking_case(text)},
                "image_url": url,
                "alt_text": mocking_case(text),
            }
        ],
    }
