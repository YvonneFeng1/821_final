"""Person class and method."""
from unicodedata import name
from db import conn
from book import Book


class Person:
    """Person class."""

    def __init__(self, name: str, username: str, phone: int) -> None:
        """Init a Person object."""
        pid = conn.get("PID")
        if pid is None:
            print("Cannot init")
            return
        self._person_key = "person:" + pid.decode("utf-8")
        self._book: list[Book] = []
        conn.hset(self._person_key, "name", name)
        conn.hset(self._person_key, "username", username)
        conn.hset(self._person_key, "phone", phone)

        conn.sadd("people_set", self._person_key)
        conn.sadd(name, self._person_key)
        conn.sadd(username, self._person_key)
        conn.sadd(str(phone), self._person_key)
        conn.incr("PID", 1)

    @property
    def person_key(self):
        """Getter of self._person_key."""
        return self._person_key


if __name__ == "__main__":
    person = Person("ok", "okk", 1234)
    person2 = Person("ok2", "okk2", 12342)
    del person2
    print(conn.hgetall("person:2"))
