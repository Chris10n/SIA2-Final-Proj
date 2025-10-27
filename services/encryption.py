from hashlib import sha256
from os import urandom


def hash_password(password: str) -> bytes:
    salt = urandom(16)
    hash = sha256(salt + password.encode("utf-8"))
    hashedPassword = salt + hash.digest()
    return hashedPassword


def verify_password(storedPassword: bytes, inputPassword: str) -> bool:
    salt = storedPassword[:16]
    storedHash = storedPassword[16:]
    hash = sha256(salt + inputPassword.encode("utf8"))
    return storedHash == hash.digest()
