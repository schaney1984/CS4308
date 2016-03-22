__author__ = "Steven Chaney"


class Program(object):
    def __init__(self, blk):
        """
        :param blk: cannot be null
        :raises: ValueError if blk is null
        """
        if blk is None:
            raise ValueError("null block argument")
        self.blk = blk

    def execute(self):
        """
        :postcondition: program has been executed
        """
        self.blk.execute()

