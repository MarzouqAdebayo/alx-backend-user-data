#!/usr/bin/env python3
"""Module 'auth.py' """
from flask import request
import os
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
            elif path == item or f"{path}/" == item:
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
        """current_user method, gets current_user from request"""
        return None

    def session_cookie(self, request=None) -> str:
        """returns a cookie value from a request"""
        if request is None:
            return None
        cookie_name = os.getenv("SESSION_NAME")
        return request.cookies.get(cookie_name)
