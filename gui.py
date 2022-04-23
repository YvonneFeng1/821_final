import tkinter
from tkinter import ttk
from redis import Redis


def main():
    # connect to redis
    conn = Redis()
    init_bid = 1 if conn.get("BID") is None else int(conn.get("BID").decode("utf-8"))
    init_pid = 1 if conn.get("PID") is None else int(conn.get("PID").decode("utf-8"))
    conn.set("BID", init_bid)
    conn.set("PID", init_pid)

    root = tkinter.Tk()
    root.title("Library System")

    make_book_frame(root, conn)
    make_user_frame(root, conn)
    root.mainloop()
    conn.connection_pool.disconnect()


def make_user_frame(root, client):
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


def make_book_frame(root, client):
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
