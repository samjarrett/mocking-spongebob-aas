from itertools import cycle

def mocking_case(text):
    value = ''
    prev = ''
    for character in text:
        value += character.lower() if prev.isupper() else character.upper()
        prev = value[-1:] if character.isalpha() else prev

    return value
