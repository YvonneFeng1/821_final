"""People class and method"""
from unicodedata import name
from psutil import pid_exists
from db import conn


class People:
    def __init__(self, name: str, username: str, phone: int) -> None:
        self._book = []
        person_key = "person:" + conn.get("PID").decode("utf-8")
        conn.hset(person_key, "name", name)
        conn.hset(person_key, "username", username)
        conn.hset(person_key, "phone", phone)

        conn.sadd("people", person_key)
        conn.sadd(name, person_key)
        conn.sadd(username, person_key)
        conn.sadd(phone, person_key)
