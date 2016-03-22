__author__ = "Steven Chaney"


class LexicalException(Exception):
    serialVersionUID = 8968627285835792944

    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message

    def getMessage(self):
        return self.message
