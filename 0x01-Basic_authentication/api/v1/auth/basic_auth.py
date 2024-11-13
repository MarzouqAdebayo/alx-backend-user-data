#!/usr/bin/env python3
"""Module 'basic_auth.py' """
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
from base64 import b64decode
import binascii
import re


class BasicAuth(Auth):
    """Represents Basic Auth"""

    def extract_base64_authorization_header(
        self,
        authorization_header: str,
    ) -> str:
        """Extract base64 auth header"""
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str,
    ) -> str:
        """Decode base64 encoded auth header"""
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            output = b64decode(base64_authorization_header, validate=True)
            return output.decode("utf-8")
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str,
    ) -> (str, str):
        """Extract user credentials from Basic Auth header"""
        if decoded_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str
        ):
            return (None, None)
        pattern = r"(?P<user>[^:]+):(?P<password>.+)"
        match = re.fullmatch(
            pattern,
            decoded_base64_authorization_header.strip(),
        )
        if match is None:
            return (None, None)
        user = match.group("user")
        password = match.group("password")
        return user, password

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str,
    ) -> TypeVar("User"):
        """Searches for user and validates the user password"""
        if (
            user_email is None
            or not isinstance(user_email, str)
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return None
        users = User.search({"email": user_email, "_password": user_pwd})
        if len(users) == 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None
