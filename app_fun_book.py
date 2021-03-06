"""Application functions for Book objects."""

from db import conn
from book import Book
from utils import clear_entries
from tkinter import ttk


def add_book(
    title_entry: ttk.Entry,
    author_entry: ttk.Entry,
    isbn_entry: ttk.Entry,
    page_number_entry: ttk.Entry,
):
    """Add a book to the redis db."""
    title = title_entry.get()
    author = author_entry.get()
    author_list = author.split(sep=", ")
    page_number = page_number_entry.get()
    isbn = isbn_entry.get()

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
    print(book.book_key, "added")
    # clear cached book object
    del book
    return


def del_book(book_key_entry):
    """Delete the book given the book key."""
    # check if book_key is in books
    book_key = book_key_entry.get()
    if not conn.sismember("books_set", book_key):
        print(book_key, "is not in the library")
        book_key_entry.delete(0, "end")
        return

    title = conn.hget(book_key, "title").decode("utf-8")
    conn.srem(title, book_key)
    author = conn.hget(book_key, "author").decode("utf-8")
    author_list = author[1:-1].split(
        sep=", "
    )  # [1:-1] is used to strip out the bracket
    for author_elem in author_list:
        conn.srem(
            author_elem[1:-1], book_key
        )  # [1:-1] is used to strip out the quotation mark
    isbn = conn.hget(book_key, "isbn").decode("utf-8")
    conn.delete(isbn)
    page_number = conn.hget(book_key, "pageNumber").decode("utf-8")
    conn.srem(page_number, book_key)
    conn.srem("books_set", book_key)

    # delete from the borrower's book set
    borrower = conn.hget(self._book_key, "borrower").decode("utf-8")  # type: ignore
    conn.srem(borrower + "_books", isbn)

    conn.delete(book_key)
    print(book_key, "deleted")
    book_key_entry.delete(0, "end")
    return


def edit_book(
    title_entry: ttk.Entry,
    author_entry: ttk.Entry,
    isbn_entry: ttk.Entry,
    page_number_entry: ttk.Entry,
    book_key_entry: ttk.Entry,
):
    """Edit book information based on given information."""
    book_key = book_key_entry.get()
    if not conn.sismember("books_set", book_key):
        print(book_key, "is not in the library, so cannot edit anything")
        book_key_entry.delete(0, "end")
        return

    prev_title = conn.hget(book_key, "title").decode("utf-8")  # type: ignore
    prev_author = conn.hget(book_key, "author").decode("utf-8")  # type: ignore
    prev_author_list = prev_author.split(", ")
    prev_isbn = conn.hget(book_key, "isbn").decode("utf-8")  # type: ignore
    prev_page_number = conn.hget(book_key, "pageNumber").decode("utf-8")  # type: ignore

    conn.srem(prev_title, book_key)
    for prev_author_elem in prev_author_list:
        conn.srem(prev_author_elem, book_key)
    conn.delete(prev_isbn)
    conn.srem(prev_page_number, book_key)

    title = title_entry.get()
    author = author_entry.get()
    author_list = author.split(sep=", ")
    isbn = isbn_entry.get()
    page_number = page_number_entry.get()

    if title == "" or author == "" or page_number == "" or isbn == "":
        print("you missed some information; plz try again")
        clear_entries(
            [title_entry, author_entry, isbn_entry, page_number_entry, book_key_entry]
        )
        return
    try:
        int(page_number)
    except ValueError:
        print("incorrect value for page number; plz try again")
        clear_entries(
            [title_entry, author_entry, isbn_entry, page_number_entry, book_key_entry]
        )
        return
    if int(page_number) <= 0:
        print("incorrect page number; it should be positive")
        clear_entries(
            [title_entry, author_entry, isbn_entry, page_number_entry, book_key_entry]
        )
        return

    conn.hset(book_key, "title", title)
    conn.hset(book_key, "author", author)
    conn.hset(book_key, "isbn", isbn)
    conn.hset(book_key, "pageNumber", page_number)

    conn.sadd(title, book_key)
    for author_elem in author_list:
        conn.sadd(author_elem, book_key)
    conn.set(isbn, book_key)
    conn.sadd(page_number, book_key)

    # clear entries
    clear_entries(
        [title_entry, author_entry, isbn_entry, page_number_entry, book_key_entry]
    )
    print(book_key, "edited")
    return


def search_book(
    title_entry: ttk.Entry, author_entry: ttk.Entry, isbn_entry: ttk.Entry
) -> None:
    """Search book based on the given info."""
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    clear_entries([title_entry, author_entry, isbn_entry])

    print("search for: " + ", ".join([title, author, isbn]))

    if isbn is not None and isbn != "":
        book_key = conn.get(isbn)
        if book_key is None:
            print("no book with such isbn.")
            return
        print(book_key, conn.hgetall(book_key))
        return

    title_set = conn.smembers(title)
    author_set = conn.smembers(author)

    book_keys_searched = set.union(title_set, author_set)
    if title != "" and len(title_set) == 0:
        book_keys_searched = set()
    if author != "" and len(author_set) == 0:
        book_keys_searched = set()
    if len(title_set) != 0:
        book_keys_searched = book_keys_searched.intersection(title_set)
    if len(author_set) != 0:
        book_keys_searched = book_keys_searched.intersection(author_set)
    if len(book_keys_searched) == 0:
        print("such book does not exist in this system")
    for book_key in book_keys_searched:
        print(book_key, conn.hgetall(book_key))

    return


def sort_books(sort_by: str) -> None:
    """Sort the books in the system by a field."""
    print(f"sorting by {sort_by}")
    sorted_books = conn.sort("books_set", by=f"*->{sort_by}", alpha=True)
    for book in sorted_books:
        print(book, conn.hgetall(book))
    return
