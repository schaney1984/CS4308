__author__ = "Steven Chaney"


class LiteralInteger(object):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value
