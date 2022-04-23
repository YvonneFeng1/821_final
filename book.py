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

    def __del__(self):
        """Delete the book instance."""
        title = conn.hget(self._book_key, "title").decode("utf-8")
        conn.srem(title, self._book_key)
        author = conn.hget(self._book_key, "author").decode("utf-8")
        author_list = author.split(sep=", ")
        for author_elem in author_list:
            conn.srem(author_elem, self._book_key)
        isbn = conn.hget(self._book_key, "isbn").decode("utf-8")
        conn.srem(isbn, self._book_key)
        page_number = conn.hget(self._book_key, "pageNumber").decode("utf-8")
        conn.srem(page_number, self._book_key)
        conn.srem("books", self._book_key)

    @property
    def book_key(self):
        """Getter of self._book_key."""
        return self._book_key


if __name__ == "__main__":
    book0 = Book("title2", "isbn2", ["a", "b"], 1)
    book1 = Book("title3", "isbn3", ["a", "b"], 1)
