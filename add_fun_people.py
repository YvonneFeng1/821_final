"""Application functions for Person object."""

from db import conn
from person import Person
from utils import clear_entries
from tkinter import ttk


def add_person(
    name_entry: ttk.Entry, username_entry: ttk.Entry, phone_entry: ttk.Entry
):
    """Add a person to the db."""
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

    person = Person(name=name, username=username, phone=int(phone))

    # clear text in entries
    clear_entries([name_entry, username_entry, phone_entry])
    print(person._person_key, "added")
    return


def del_person(person_key_entry: ttk.Entry):
    """Delete a person from the db."""
    person_key = person_key_entry.get()
    if not conn.sismember("people", person_key):
        print(person_key, "is not in the library")
        person_key_entry.delete(0, "end")
        return

    name = conn.hget(person_key, "name").decode("utf-8")  # type: ignore
    conn.srem(name, person_key)
    username = conn.hget(person_key, "username").decode("utf-8")  # type: ignore
    conn.srem(username, person_key)
    phone = conn.hget(person_key, "phone").decode("utf-8")  # type: ignore
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


def edit_person(
    name_entry: ttk.Entry,
    username_entry: ttk.Entry,
    phone_entry: ttk.Entry,
    person_key_entry: ttk.Entry,
):
    """Edit a person in the db."""
    person_key = person_key_entry.get()
    if not conn.sismember("people", person_key):
        print(person_key, "is not in the library, so cannot edit anything")
        person_key_entry.delete(0, "end")
        return

    prev_name = conn.hget(person_key, "name").decode("utf-8")  # type: ignore
    prev_username = conn.hget(person_key, "username").decode("utf-8")  # type: ignore
    prev_phone = conn.hget(person_key, "phone").decode("utf-8")  # type: ignore

    conn.srem(prev_name, person_key)
    conn.srem(prev_username, person_key)
    conn.srem(prev_phone, person_key)

    name = name_entry.get()
    username = username_entry.get()
    phone = phone_entry.get()

    if name == "" or username == "" or phone == "":
        print("you missed some information; plz try again")
        clear_entries([name_entry, username_entry, phone_entry, person_key_entry])
        return
    try:
        int(phone)
    except ValueError:
        print("incorrect value for phone number; plz try again")
        clear_entries([name_entry, username_entry, phone_entry, person_key_entry])
        return

    conn.hset(person_key, "name", name)
    conn.hset(person_key, "username", username)
    conn.hset(person_key, "phone", phone)

    conn.sadd(name, person_key)
    conn.sadd(username, person_key)
    conn.sadd(phone, person_key)

    # clear entries
    clear_entries([name_entry, username_entry, phone_entry, person_key_entry])
    print(person_key, "edited")
    return


def search_person(name_entry: ttk.Entry, username_entry: ttk.Entry):
    name = name_entry.get()
    username = username_entry.get()
    print("search for: " + ", ".join([name, username]))

    name_set = conn.smembers(name)
    username_set = conn.smembers(username)

    person_keys_searched = set.union(name_set, username_set)
    if name != "" and len(name_set) == 0:
        person_keys_searched = set()
    if username != "" and len(username_set) == 0:
        person_keys_searched = set()
    if len(name_set) != 0:
        person_keys_searched = person_keys_searched.intersection(name_set)
    if len(username_set) != 0:
        person_keys_searched = person_keys_searched.intersection(username_set)

    if len(person_keys_searched) == 0:
        print("such person does not exist in this system")
    for person_key in person_keys_searched:
        print(person_key, conn.hgetall(person_key))

    clear_entries([name_entry, username_entry])
    return
