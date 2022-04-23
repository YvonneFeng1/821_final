from db import conn
from people import People


def add_person(name_entry, username_entry, phone_entry):
    name = name_entry.get()
    username = username_entry.get()
    phone = phone_entry.get()

    # TODO: check for missed info
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

    people = People(name=name, username=username, phone=phone)

    # clear text in entries
    clear_entries([name_entry, username_entry, phone_entry])
    print(person_key, "added")

    conn.incr("PID", 1)
    return
