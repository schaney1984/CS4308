__author__ = "Steven Chaney"


class Block(object):

    def __init__(self):
        self.stmts = []

    def add(self, stmt):
        """
        :param stmt: cannot be null
        :raises: ValueError if stmt is null
        """
        if stmt is None:
            raise ValueError("null statement argument")
        self.stmts.append(self, stmt)

    def execute(self):
        for stmt in self.stmts:
            stmt.execute()
