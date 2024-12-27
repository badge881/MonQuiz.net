from random import choice


def getHexString() -> str:
    return ''.join([choice('0123456789abcdef') for _ in range(32)])
