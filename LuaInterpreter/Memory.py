__author__ = "Steven Chaney"

mem = [52]


def store(ch, value):
    """
    :param ch: must be a letter
    :param value: value to be stored
    :postcondition: value has been stored in the memory location
                    associated with ch
    """
    mem[indexOf(ch)] = value


def indexOf(ch):
    """
    :param ch: must be a letter
    :return: index in memory array associated with ch
    :raises: ValueError if ch is not a letter
    """
    if not ch.isAlpha():
        raise ValueError("invalid identifier argument")
    if ch.isLower():
        index = int(ch) - int('a')
    else:
        index = 26 + int(ch) - int('A')
    return index


def fetch(ch):
    return mem[indexOf(ch)]
