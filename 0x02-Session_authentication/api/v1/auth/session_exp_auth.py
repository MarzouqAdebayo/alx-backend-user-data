#!/usr/bin/env python3
"""Module 'session_exp_auth.py' """
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Represents SessionExp Auth"""

    def __init__(self):
        """Initializes a new SessionExpAuth instance"""
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", "0"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a session id for user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """gets user_id from session_id"""
        if session_id is None:
            return None
        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None
        if self.session_duration <= 0:
            return session_data["user_id"]
        if "created_at" not in session_data:
            return None
        current_time = datetime.now()
        life = timedelta(seconds=self.session_duration)
        expiry_time = session_data["created_at"] + life
        if expiry_time < current_time:
            return None
        return session_data["user_id"]
