"""Person class and method."""
from db import conn


class Person:
    """Person class."""

    def __init__(self, name: str, username: str, person_key: None | str = None) -> None:
        """Init a Person object."""
        if person_key is None:
            pid = conn.get("PID")
            self._person_key = "person:" + pid.decode("utf-8")  # type: ignore
        else:
            self._person_key = person_key
        conn.hset(self._person_key, "name", name)
        conn.hset(self._person_key, "username", username)

        conn.sadd("people_set", self._person_key)
        conn.sadd(name, self._person_key)
        conn.set(username, self._person_key)
        if person_key is None:
            conn.incr("PID", 1)

    @property
    def person_key(self):
        """Getter of self._person_key."""
        return self._person_key

    @property
    def username(self):
        """Getter of username."""
        return conn.hget(self._person_key, "username").decode("utf-8")  # type: ignore

    def checks(self, isbn: str) -> None:
        """Check a book."""
        conn.sadd(self.username + "_books", isbn)

    def returns(self, isbn: str) -> None:
        """Return a book."""
        _books_set_name = self.username + "_books"
        if not conn.smismember(_books_set_name, isbn)[0]:
            print(f"username: {self.username} has not checked isbn {isbn}")
            return
        conn.srem(_books_set_name, isbn)
        _books = conn.smembers(_books_set_name)
        if len(_books) == 0:
            conn.delete(_books_set_name)


def locate_person(username: str) -> Person:
    """Locate the person by username in the database."""
    person_key = conn.get(username)
    if person_key is None:
        raise ValueError(f"username: {username} does not exist.")
    name = conn.hget(person_key, "name").decode("utf-8")  # type: ignore
    return Person(name, username, person_key.decode("utf-8"))
