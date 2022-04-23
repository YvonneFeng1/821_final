"""People class and method"""
from unicodedata import name
from psutil import pid_exists
from db import conn


class People:
    def __init__(self, name: str, username: str, phone: int) -> None:
        self._book = []
        self._person_key = "person:" + conn.get("PID").decode("utf-8")
        conn.hset(self._person_key, "name", name)
        conn.hset(self._person_key, "username", username)
        conn.hset(self._person_key, "phone", phone)

        conn.sadd("people", self._person_key)
        conn.sadd(name, self._person_key)
        conn.sadd(username, self._person_key)
        conn.sadd(phone, self._person_key)

    def __del__(self):
        """Delete person"""
        name = conn.hget(self._person_key, "name").decode("utf-8")
        conn.srem(name, self._person_key)
        username = conn.hget(self._person_key, "username").decode("utf-8")
        conn.srem(username, self._person_key)
        phone = conn.hget(self._person_key, "phone").decode("utf-8")
        conn.srem(phone, self._person_key)

    @property
    def person_key(self):
        """Getter of self._person_key"""
        return self._person_key


if __name__ == "__main__":
    person = People("ok", "okk", 1234)
    person2 = People("ok2", "okk2", 12342)
    del person2
    print(conn.hgetall("person:2"))
