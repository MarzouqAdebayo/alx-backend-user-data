#!/usr/bin/env python3
"""Module 'auth.py' """
from typing import TypeVar, List


class Auth:
    """Represents Auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth method"""
        if path is None or excluded_paths is None:
            return True
        for item in excluded_paths:
            if item[-1] == "*" and path.startswith(item[:-1]):
                return False
            elif path == item or path == f"{path}/":
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header method"""
        if request is None:
            return None
        if request.headers.get("Authorization") is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """current_user method"""
        return None
