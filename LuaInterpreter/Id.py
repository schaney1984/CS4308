from LuaInterpreter import Memory


class Id(object):
    def __init__(self, ch):
        """
        :param ch: must be a valid identifier
        :raises: ValueError if ch is not a valid identifier
        """
        if not ch.isAlpha():
            raise ValueError("invalid identifier argument")
        self.ch = ch

    def getChar(self):
        return self.ch

    def evaluate(self):
        Memory.fetch(self.ch)
