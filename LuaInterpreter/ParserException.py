__author__ = "Steven Chaney"


class ParserException(Exception):
    serialVersionUID = 2284169084900414715

    # def __init__(self, message):
    #     Exception.__init__(self, message)
    #     self.message = message
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
    #
    # def getMessage(self):
    #     return self.message
