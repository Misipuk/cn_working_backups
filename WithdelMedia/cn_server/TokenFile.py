import base64
import hashlib
import json
import time
from typing import Dict, Optional, Union


secret = "jdfkgahlskjhflkj2y3iy187 2rofiulh"


def sha256(s: str) -> bytes:
    m = hashlib.sha256()
    m.update(s.encode())
    return m.digest()


def b64_encode(b: bytes) -> bytes:
    return base64.urlsafe_b64encode(b)


def b64_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s.encode())


class Token:
    login: str
    expire: int
    key: str

    def __init__(self, login: str, expire: int):
        self.login = login
        self.expire = expire
        self.key = b64_encode(sha256(login + "|" + str(expire) + "|" + secret)).decode()

    @staticmethod
    def as_token(authorization: str) -> Optional[str]:
        decoded = b64_decode(authorization).decode()
        d = json.loads(decoded)
        expected_key = Token(d["login"], d["expire"]).key

        if d["key"] != expected_key:
            raise Exception("invalid key")
        if d["expire"] < int(time.time()):
            raise Exception("token expired")

        return d["login"]

    @staticmethod
    def as_authorization(login: str, expire: int) -> str:
        token = Token(login, expire)
        token = json.dumps(token.__dict__)
        return b64_encode(token.encode()).decode()