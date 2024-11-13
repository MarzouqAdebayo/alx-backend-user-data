#!/usr/bin/env python3
"""Module 'session_auth.py' """
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Represents Session Auth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a user session and returns session id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
