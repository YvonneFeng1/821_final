"""Some utility functions."""

from tkinter import ttk
from person import locate_person, Person
from book import locate_book, Book


def clear_entries(entries: list[ttk.Entry]):
    """Clear all the selected entries."""
    for entry in entries:
        entry.delete(0, "end")
    return


def action_checker(username: str, isbn: str) -> tuple[Person, Book] | tuple[None, None]:
    """Check for the username and isbn, and return a Book and a Person."""
    if username == "" or isbn == "":
        print("username and isbn is required.")
        return None, None
    try:
        person = locate_person(username)
    except ValueError as e:
        print(e.args[0])
        return None, None
    try:
        book = locate_book(isbn)
    except ValueError as e:
        print(e.args[0])
        return None, None
    return person, book
