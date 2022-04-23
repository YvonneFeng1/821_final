from db import conn
from book import Book


def add_book(title_entry, author_entry, isbn_entry, page_number_entry):
    title = title_entry.get()
    author = author_entry.get()
    author_list = author.split(sep=", ")
    page_number = page_number_entry.get()
    isbn = isbn_entry.get()

    # TODO: check for missed/incorrect info
    if title == "" or author == "" or page_number == "" or isbn == "":
        print("you missed some information; plz try again")
        clear_entries([title_entry, author_entry, isbn_entry, page_number_entry])
        return
    try:
        int(page_number)
    except ValueError:
        print("incorrect value for page number; plz try again")
        clear_entries([title_entry, author_entry, isbn_entry, page_number_entry])
        return
    if int(page_number) <= 0:
        print("incorrect value for page number; it should be positive")
        clear_entries([title_entry, author_entry, isbn_entry, page_number_entry])
        return

    book = Book(
        title=title, isbn=isbn, authors=author_list, page_number=int(page_number)
    )

    # clear text in entries
    clear_entries([title_entry, author_entry, isbn_entry, page_number_entry])
    print(book_key, "added")

    conn.incr("BID", 1)
    return
