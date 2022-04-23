"""Book class and methods."""
from db import conn


class Book:
    """Book class."""

    def __init__(
        self, title: str, isbn: str, authors: list[str], page_number: int
    ) -> None:
        """Init a book object."""
        bid = conn.get("BID")
        if bid is None:
            print("Cannot init")
            return
        self._book_key = "book:" + bid.decode("utf-8")

        conn.hset(self._book_key, "title", title)
        conn.hset(self._book_key, "author", str(authors))
        conn.hset(self._book_key, "isbn", isbn)
        conn.hset(self._book_key, "pageNumber", str(page_number))
        conn.hset(
            self._book_key, "isAvailable", 1
        )  # 1 means availability, 0 means not available
        conn.hset(self._book_key, "borrower", "none")

        conn.sadd("books_set", self._book_key)
        conn.sadd(title, self._book_key)
        for author_elem in authors:
            conn.sadd(author_elem, self._book_key)
        conn.sadd(isbn, self._book_key)
        conn.sadd(str(page_number), self._book_key)
        conn.incr("BID", 1)

    @property
    def book_key(self):
        """Getter of self._book_key."""
        return self._book_key
