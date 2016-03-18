from Assignment3 import book


if __name__ == "__main__":
    example = book.create_book("Herman Melville", "Moby Dick", 635)

    print("-"*10 + "Book Information" + "-"*10)
    print("Author: " + example.author)
    print("Title: " + example.title)
    print("Number of pages: " + str(example.num_pages))
    print("-"*35)
