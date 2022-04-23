"""Library system GUI."""

import tkinter
from tkinter import ttk

from numpy import sort
from db import conn


def main():
    """Build main."""
    root = tkinter.Tk()
    root.title("Library System")

    make_book_frame(root)
    make_user_frame(root)
    root.mainloop()
    conn.connection_pool.disconnect()


def make_user_frame(root):
    """User frame."""
    person_frame = ttk.Frame(root, padding=20)
    person_frame.grid(row=1)
    # input entries
    name_label = ttk.Label(person_frame, text="name")
    name_entry = ttk.Entry(person_frame, width=8)
    username_label = ttk.Label(person_frame, text="username")
    username_entry = ttk.Entry(person_frame, width=8)
    phone_label = ttk.Label(person_frame, text="phone")
    phone_entry = ttk.Entry(person_frame, width=8)
    person_key_label = ttk.Label(person_frame, text="person_key")
    person_key_entry = ttk.Entry(person_frame, width=8)
    act_with_book_label = ttk.Label(person_frame, text="Enter the searched book key")
    act_with_book_entry = ttk.Entry(person_frame, width=8)

    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    username_label.grid(row=0, column=2)
    username_entry.grid(row=0, column=3)
    phone_label.grid(row=1, column=0)
    phone_entry.grid(row=1, column=1)
    person_key_label.grid(row=1, column=2)
    person_key_entry.grid(row=1, column=3)
    act_with_book_label.grid(row=4, column=0)
    act_with_book_entry.grid(row=4, column=1)


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

    sort_label = ttk.Label(book_frame, text="sort method:")
    sort_label.grid(row=4, column=0)
    sort_method_grid_complex = [
        ("title", 4, 1),
        ("author", 4, 2),
        ("isbn", 5, 1),
        ("pageNumber", 5, 2),
    ]
    v = tkinter.StringVar()

    def show_choice() -> None:
        """Radio-button help command."""
        sort_by = v.get()
        print(sort_by)

    for (method, row, col) in sort_method_grid_complex:
        radio_button = ttk.Radiobutton(
            book_frame, text=method, value=method, variable=v, command=show_choice
        )
        radio_button.grid(row=row, column=col)
