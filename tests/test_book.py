"""Test Book class and functionalities."""

import sys

sys.path.append("../821_FINAL")  # noqa: 504
from book import Book
from db import conn


# init some book objects
book1 = Book("apple", "a100", ["author1", "author2"], 100)
book2 = Book("banana", "b100", ["author2", "author3"], 150)


def test_borrower():
    """Test if the borrower field is None after init."""
    assert book1.borrower is None
    assert book2.borrower is None


def test_is_avaliable():
    """Test if the book is avaliable after init."""
    assert book1.is_avaliable
    assert book2.is_avaliable


def test_is_checked():
    """Test book checking out functionality."""
    book1.is_checked("person1")
    assert not book1.is_avaliable
    assert book1.borrower == "person1"
    book2.is_checked("person2")
    assert not book2.is_avaliable
    assert book2.borrower == "person2"


def test_is_returned():
    """Test book returning functionality."""
    book1.is_returned()
    assert book1.is_avaliable
    assert book1.borrower is None
    book2.is_returned()
    assert book2.is_avaliable
    assert book2.borrower is None
