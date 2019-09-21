from itertools import cycle


def mocking_case(text):
    funcs = cycle([str.lower, str.upper])

    return ''.join(next(funcs)(c) for c in text)
