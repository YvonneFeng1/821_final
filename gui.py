"""Library system GUI."""

import tkinter
from tkinter import ttk
import app_fun_book
import app_fun_person
from db import conn


def main():
    """Build main."""
    root = tkinter.Tk()
    root.title("Library System")

    make_book_frame(root)
    make_person_frame(root)
    make_checkout_frame(root)
    root.mainloop()
    conn.connection_pool.disconnect()


def make_person_frame(root):
    """User frame."""
    person_frame = ttk.Frame(root, padding=20)
    person_frame.grid(row=1)
    # input entries
    name_label = ttk.Label(person_frame, text="name")
    name_entry = ttk.Entry(person_frame, width=8)
    username_label = ttk.Label(person_frame, text="username")
    username_entry = ttk.Entry(person_frame, width=8)
    person_key_label = ttk.Label(person_frame, text="person_key")
    person_key_entry = ttk.Entry(person_frame, width=8)

    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    username_label.grid(row=0, column=2)
    username_entry.grid(row=0, column=3)
    person_key_label.grid(row=0, column=4)
    person_key_entry.grid(row=0, column=5)

    # button
    add_person_button = ttk.Button(person_frame, text="add person")
    del_person_button = ttk.Button(person_frame, text="delete person")
    edit_person_button = ttk.Button(person_frame, text="edit person")
    search_person_button = ttk.Button(person_frame, text="search person")

    add_person_button.grid(row=1, column=1)
    del_person_button.grid(row=1, column=3)
    edit_person_button.grid(row=1, column=5)
    search_person_button.grid(row=2, column=3)

    add_person_button["command"] = lambda: app_fun_person.add_person(
        name_entry, username_entry
    )
    del_person_button["command"] = lambda: app_fun_person.del_person(person_key_entry)
    edit_person_button["command"] = lambda: app_fun_person.edit_person(
        name_entry, username_entry, person_key_entry
    )
    search_person_button["command"] = lambda: app_fun_person.search_person(
        username_entry
    )


def make_book_frame(root):
    """Book frame."""
    book_frame = ttk.Frame(root, padding=20)
    book_frame.grid(row=0)
    # input entries
    title_label = ttk.Label(book_frame, text="title")
    title_entry = ttk.Entry(book_frame, width=8)
    author_label = ttk.Label(book_frame, text="author")
    author_entry = ttk.Entry(book_frame, width=8)
    isbn_label = ttk.Label(book_frame, text="ISBN")
    isbn_entry = ttk.Entry(book_frame, width=8)
    page_number_label = ttk.Label(book_frame, text="page number")
    page_number_entry = ttk.Entry(book_frame, width=8)
    book_key_label = ttk.Label(book_frame, text="book_key")
    book_key_entry = ttk.Entry(book_frame, width=8)

    title_label.grid(row=0, column=0)
    title_entry.grid(row=0, column=1)
    author_label.grid(row=0, column=2)
    author_entry.grid(row=0, column=3)
    isbn_label.grid(row=1, column=0)
    isbn_entry.grid(row=1, column=1)
    page_number_label.grid(row=1, column=2)
    page_number_entry.grid(row=1, column=3)
    book_key_label.grid(row=2, column=1)
    book_key_entry.grid(row=2, column=2)

    # buttons
    add_book_button = ttk.Button(book_frame, text="add book")
    del_book_button = ttk.Button(book_frame, text="delete book")
    edit_book_button = ttk.Button(book_frame, text="edit book")
    search_book_button = ttk.Button(book_frame, text="search book")

    add_book_button.grid(row=3, column=0)
    del_book_button.grid(row=3, column=1)
    edit_book_button.grid(row=3, column=2)
    search_book_button.grid(row=3, column=3)

    add_book_button["command"] = lambda: app_fun_book.add_book(
        title_entry, author_entry, isbn_entry, page_number_entry
    )
    del_book_button["command"] = lambda: app_fun_book.del_book(book_key_entry)
    edit_book_button["command"] = lambda: app_fun_book.edit_book(
        title_entry, author_entry, isbn_entry, page_number_entry, book_key_entry
    )
    search_book_button["command"] = lambda: app_fun_book.search_book(
        title_entry, author_entry, isbn_entry
    )

    # radio buttons for sorting

    sort_label = ttk.Label(book_frame, text="sort method:")
    sort_label.grid(row=4, column=0)
    sort_method_grid_complex = [
        ("by Title", "title", 4, 1),
        ("by Author", "author", 4, 2),
        ("by ISBN", "isbn", 5, 1),
        ("by #Pages", "pageNumber", 5, 2),
    ]
    v = tkinter.StringVar()

    def show_choice() -> None:
        """Radio-button help command."""
        sort_by = v.get()
        app_fun_book.sort_books(sort_by)

    for (label, method, row, col) in sort_method_grid_complex:
        radio_button = ttk.Radiobutton(
            book_frame, text=label, value=method, variable=v, command=show_choice
        )
        radio_button.grid(row=row, column=col)


def make_checkout_frame(root):
    """Checkout frame."""
    checkout_frame = ttk.Frame(root, padding=20)
    checkout_frame.grid(row=2)
    # labels and entries
    username_label = ttk.Label(checkout_frame, text="username:")
    username_entry = ttk.Entry(checkout_frame, width=8)
    isbn_label = ttk.Label(checkout_frame, text="ISBN:")
    isbn_entry = ttk.Entry(checkout_frame, width=8)

    username_label.grid(row=0, column=0)
    username_entry.grid(row=0, column=1)
    isbn_label.grid(row=0, column=2)
    isbn_entry.grid(row=0, column=3)
    # buttons
    check_button = ttk.Button(checkout_frame, text="check book")
    return_button = ttk.Button(checkout_frame, text="return book")

    check_button.grid(row=1, column=1)
    return_button.grid(row=1, column=3)

    check_button["command"] = lambda: app_fun_person.check_book(
        username_entry, isbn_entry
    )
    return_button["command"] = lambda: app_fun_person.return_book(
        username_entry, isbn_entry
    )
