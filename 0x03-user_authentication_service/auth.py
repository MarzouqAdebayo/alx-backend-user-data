#!/usr/bin/env python3
"""Module 'auth.py' """
import bcrypt
import uuid
from typing import Union
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes password and returns bytes"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a random uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Logs in a user using their email and password"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(
            password.encode("utf-8"),
            user.hashed_password,
        )

    def create_session(self, email: str) -> str:
        """Creates a session_id, saves it to db and returns it as string"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get user by their session_id"""
        # This guard clause is important because it will result in
        # in the function finding users where their session_id is None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """Destroys a user session"""
        try:
            user = self._db.find_user_by(id=user_id)
        except Exception:
            return None
        self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Returns a reset token for a user"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError
        except Exception:
            return None

    def update_password(self, reset_token: str, password: str):
        """Reset a users password using the reset_token"""
        if not reset_token:
            raise ValueError
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user.id,
                reset_token=None,
                hashed_password=_hash_password(password),
            )
        except NoResultFound:
            raise ValueError
