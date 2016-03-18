class Book(object):
    author = ""
    title = ""
    num_pages = 0

    def __init__(self, author, title, num_pages):
        self.author = author
        self.title = title
        self.num_pages = num_pages


def create_book(author, title, num_pages):
    book = Book(author, title, num_pages)
    return book
