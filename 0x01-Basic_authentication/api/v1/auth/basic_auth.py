#!/usr/bin/env python3
"""Module 'basic_auth.py' """
from api.v1.auth.auth import Auth
from base64 import b64decode
import dec


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
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            b64decode(base64_authorization_header)
        except Exception:
            return None
        return base64_authorization_header.decode("utf-8")
