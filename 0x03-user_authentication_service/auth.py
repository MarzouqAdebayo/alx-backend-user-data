#!/usr/bin/env python3
"""Module 'auth.py' """
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes password and returns bytes"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str):
        """Registers a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Logs in a user using their email and password"""
        try:
            self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(
            password.encode("utf-8"),
            _hash_password(password),
        )
