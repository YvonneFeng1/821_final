"""Application functions for People object"""

from db import conn
from people import People
from utils import clear_entries
from tkinter import ttk


def add_person(
    name_entry: ttk.Entry, username_entry: ttk.Entry, phone_entry: ttk.Entry
):
    name = name_entry.get()
    username = username_entry.get()
    phone = phone_entry.get()

    if name == "" or username == "" or phone == "":
        print("you missed some information; plz try again")
        clear_entries([name_entry, username_entry, phone_entry])
        return
    try:
        int(phone)
    except ValueError:
        print("incorrect value for phone number; plz try again")
        clear_entries([name_entry, username_entry, phone_entry])
        return

    person = People(name=name, username=username, phone=phone)

    # clear text in entries
    clear_entries([name_entry, username_entry, phone_entry])
    print(person._person_key, "added")

    conn.incr("PID", 1)
    return


def del_person(person_key_entry: ttk.Entry):
    person_key = person_key_entry.get()
    if not conn.sismember("people", person_key):
        print(person_key, "is not in the library")
        person_key_entry.delete(0, "end")
        return

    name = conn.hget(person_key, "name").decode("utf-8")
    conn.srem(name, person_key)
    username = conn.hget(person_key, "username").decode("utf-8")
    conn.srem(username, person_key)
    phone = conn.hget(person_key, "phone").decode("utf-8")
    conn.srem(phone, person_key)

    # return all the books and expire the person_book_set
    person_book_set_key = person_key + ":books"
    for book_key in conn.smembers(person_book_set_key):
        conn.hset(book_key, "isAvailable", 1)
    conn.expire(person_book_set_key, 0)

    conn.delete(person_key)
    conn.srem("people", person_key)

    print(person_key, "deleted")
    person_key_entry.delete(0, "end")
    return
