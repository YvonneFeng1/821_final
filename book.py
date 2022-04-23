"""Book class and methods."""
from db import conn


class Book:
    def __init__(
        self, title: str, isbn: str, authors: list[str], page_number: int
    ) -> None:
        bid = conn.get("BID")
        if bid is None:
            print("Cannot init")
            return
        book_key = "book:" + bid.decode("utf-8")
        conn.hset(book_key, "title", title)
        conn.hset(book_key, "author", str(authors))
        conn.hset(book_key, "isbn", isbn)
        conn.hset(book_key, "pageNumber", str(page_number))
        conn.hset(
            book_key, "isAvailable", 1
        )  # 1 means availability, 0 means not available
        conn.hset(book_key, "borrower", "none")

        conn.sadd("books", book_key)
        conn.sadd(title, book_key)
        for author_elem in authors:
            conn.sadd(author_elem, book_key)
        conn.sadd(isbn, book_key)
        conn.sadd(str(page_number), book_key)

    @property
    def get_book_info(self):
        pass
