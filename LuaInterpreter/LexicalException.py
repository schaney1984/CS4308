__author__ = "Steven Chaney"


class LexicalException(Exception):
    serialVersionUID = 8968627285835792944

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

    # def getMessage(self):
    #     return self.message
