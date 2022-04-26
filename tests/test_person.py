"""Test Person class and functionalities."""

import sys

sys.path.append("../821_FINAL")  # noqa: 504
from person import Person
from db import conn

person1 = Person("name1", "person1")
person2 = Person("name2", "person2")


def test_books():
    """Test if person has no book under his/her name after the init."""
    assert person1.books == set()


def test_checks():
    """Test person checking book functionality."""
    person2.checks("a100")
    person2.checks("b100")
    assert person2.books == set(["a100".encode("UTF-8"), "b100".encode("UTF-8")])


def test_returns():
    """Test person returning book functionality."""
    try:
        person1.returns("some-isbn")
    except ValueError as e:
        assert "has not checked isbn" in e.args[0]
    person2.returns("b100")
    assert person2.books == set(["a100".encode("UTF-8")])
