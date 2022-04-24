"""Book class and methods."""
from db import conn
from person import locate_person


class Book:
    """Book class."""

    def __init__(
        self,
        title: str,
        isbn: str,
        authors: list[str],
        page_number: int,
        book_key: str | None = None,
    ) -> None:
        """Init a book object."""
        if book_key is None:
            bid = conn.get("BID")
            self._book_key = "book:" + bid.decode("utf-8")  # type: ignore
        else:
            self._book_key = book_key

        conn.hset(self._book_key, "title", title)
        conn.hset(self._book_key, "author", str(authors))
        conn.hset(self._book_key, "isbn", isbn)
        conn.hset(self._book_key, "pageNumber", str(page_number))
        conn.hset(
            self._book_key, "isAvaliable", 1
        )  # 1 means availability, 0 means not available
        conn.hset(self._book_key, "borrower", "none")

        conn.sadd("books_set", self._book_key)
        conn.sadd(title, self._book_key)
        for author_elem in authors:
            conn.sadd(author_elem, self._book_key)
        conn.set(isbn, self._book_key)
        conn.sadd(str(page_number), self._book_key)
        conn.incr("BID", 1)

    @property
    def book_key(self):
        """Getter of self._book_key."""
        return self._book_key

    @property
    def borrower(self) -> str | None:
        """Getter of borrower."""
        borrower = conn.hget(self._book_key, "borrower").decode("utf-8")  # type: ignore
        return borrower if borrower != "none" else None

    @property
    def is_avaliable(self) -> bool:
        """Getter of the status of isAvaliable."""
        check = conn.hget(self._book_key, "isAvaliable")
        return int(check) == 1  # type: ignore

    @property
    def isbn(self):
        """Getter of isbn."""
        return conn.hget(self._book_key, "isbn").decode("utf-8")  # type: ignore

    def is_checked(self, borrower: str) -> None:
        """Make the book be borrowed by someone."""
        conn.hset(self._book_key, "isAvaliable", 0)
        conn.hset(self._book_key, "borrower", borrower)

    def is_returned(self) -> None:
        """Make the book be returned by someone."""
        conn.hset(self._book_key, "isAvaliable", 1)
        conn.hset(self._book_key, "borrower", "none")


def locate_book(isbn: str) -> Book:
    """Locate the book by isbn in the database."""
    book_key = conn.get(isbn)
    if book_key is None:
        raise ValueError(f"isbn: {isbn} des not exist.")
    title = conn.hget(book_key, "title").decode("utf-8")  # type: ignore
    author = conn.hget(book_key, "author").decode("utf-8")  # type: ignore
    author_list = author[1:-1].split(
        sep=", "
    )  # [1:-1] is used to strip out the bracket
    author_list = [elem[1:-1] for elem in author_list]
    page_number = conn.hget(book_key, "pageNumber").decode("utf-8")  # type: ignore
    return Book(title, isbn, author_list, int(page_number), book_key.decode("utf-8"))
