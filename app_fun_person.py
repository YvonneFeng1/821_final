"""Application functions for Person object."""

from db import conn
from person import Person, locate_person
from utils import clear_entries
from tkinter import ttk


def add_person(name_entry: ttk.Entry, username_entry: ttk.Entry):
    """Add a person to the db."""
    name = name_entry.get()
    username = username_entry.get()

    if name == "" or username == "":
        print("you missed some information; plz try again")
        clear_entries([name_entry, username_entry])
        return

    person = Person(name=name, username=username)

    # clear text in entries
    clear_entries([name_entry, username_entry])
    print(person._person_key, "added")
    # clear the cached person object
    del person
    return


def del_person(person_key_entry: ttk.Entry):
    """Delete a person from the db."""
    person_key = person_key_entry.get()
    if not conn.sismember("people_set", person_key):
        print(person_key, "is not in the library")
        person_key_entry.delete(0, "end")
        return

    name = conn.hget(person_key, "name").decode("utf-8")  # type: ignore
    conn.srem(name, person_key)
    username = conn.hget(person_key, "username").decode("utf-8")  # type: ignore
    conn.delete(username, person_key)

    # # return all the books and expire the person_book_set
    # person_book_set_key = person_key + ":books"
    # for book_key in conn.smembers(person_book_set_key):
    #     conn.hset(book_key, "isAvailable", 1)
    # conn.expire(person_book_set_key, 0)

    conn.delete(person_key)
    conn.srem("people_set", person_key)

    print(person_key, "deleted")
    person_key_entry.delete(0, "end")
    return


def edit_person(
    name_entry: ttk.Entry,
    username_entry: ttk.Entry,
    person_key_entry: ttk.Entry,
):
    """Edit a person in the db."""
    person_key = person_key_entry.get()
    if not conn.sismember("people_set", person_key):
        print(person_key, "is not in the library, so cannot edit anything")
        person_key_entry.delete(0, "end")
        return

    prev_name = conn.hget(person_key, "name").decode("utf-8")  # type: ignore
    prev_username = conn.hget(person_key, "username").decode("utf-8")  # type: ignore

    conn.srem(prev_name, person_key)
    conn.delete(prev_username)

    name = name_entry.get()
    username = username_entry.get()

    if name == "" or username == "":
        print("you missed some information; plz try again")
        clear_entries([name_entry, username_entry, person_key_entry])
        return

    conn.hset(person_key, "name", name)
    conn.hset(person_key, "username", username)

    conn.sadd(name, person_key)
    conn.set(username, person_key)

    # clear entries
    clear_entries([name_entry, username_entry, person_key_entry])
    print(person_key, "edited")
    return


def search_person(username_entry: ttk.Entry) -> None:
    """Search person based on the username."""
    username = username_entry.get()
    if username == "" or username is None:
        print("username is required.")
        return
    try:
        person = locate_person(username)
    except ValueError as e:
        print(e.args[0])
        return
    _key = person.person_key
    print(_key, conn.hgetall(_key))
