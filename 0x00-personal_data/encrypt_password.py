#!/usr/bin/env python3
"""Module 'encrypt_password.py' """
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using a random salt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a hashed password is valid"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
