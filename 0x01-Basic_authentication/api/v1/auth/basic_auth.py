#!/usr/bin/env python3
"""Module 'basic_auth.py' """
from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii


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
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or decoded_base64_authorization_header.find(":") == -1
        ):
            return (None, None)
        try:
            output = b64decode(
                decoded_base64_authorization_header,
                validate=True,
            )
            splited_out = output.decode("utf-8").split(":")
            return (splited_out[0], splited_out[1])
        except (binascii.Error, UnicodeDecodeError):
            return (None, None)
